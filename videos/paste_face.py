"""Paste the real face from the source frame onto the AI-edited image (aligned, colour-matched, feathered)."""
import sys, numpy as np
from PIL import Image, ImageFilter, ImageDraw

base_p, edit_p, out_p = sys.argv[1], sys.argv[2], sys.argv[3]
W, H = 1080, 1920
base = np.asarray(Image.open(base_p).convert("RGB").resize((W, H), Image.LANCZOS), np.float32)
edit = np.asarray(Image.open(edit_p).convert("RGB").resize((W, H), Image.LANCZOS), np.float32)

# face box in base (eyes..mouth) used for alignment
CX, CY, HW, HH = 527, 590, 150, 200
tpl_box = (CX - 120, CY - 110, CX + 120, CY + 120)   # brows to lower lip

def gray(a): return a @ np.array([0.299, 0.587, 0.114], np.float32)

def ncc(a, b):
    a = a - a.mean(); b = b - b.mean()
    return float((a * b).sum() / (np.sqrt((a * a).sum() * (b * b).sum()) + 1e-6))

bg = gray(base); eg = gray(edit)
x0, y0, x1, y1 = tpl_box
tpl = bg[y0:y1, x0:x1]
best = (-2, 1.0, 0, 0)
for s in np.arange(0.90, 1.121, 0.02):
    th, tw = int(tpl.shape[0] * s), int(tpl.shape[1] * s)
    t = np.asarray(Image.fromarray(tpl).resize((tw, th), Image.BILINEAR), np.float32)
    cxs, cys = (x0 + x1) / 2, (y0 + y1) / 2
    for dy in range(-90, 91, 6):
        for dx in range(-90, 91, 6):
            ex0 = int(cxs + dx - tw / 2); ey0 = int(cys + dy - th / 2)
            if ex0 < 0 or ey0 < 0 or ex0 + tw > W or ey0 + th > H: continue
            v = ncc(t, eg[ey0:ey0 + th, ex0:ex0 + tw])
            if v > best[0]: best = (v, s, dx, dy)
# refine
v0, s0, dx0, dy0 = best
for s in np.arange(s0 - 0.02, s0 + 0.021, 0.005):
    th, tw = int(tpl.shape[0] * s), int(tpl.shape[1] * s)
    t = np.asarray(Image.fromarray(tpl).resize((tw, th), Image.BILINEAR), np.float32)
    cxs, cys = (x0 + x1) / 2, (y0 + y1) / 2
    for dy in range(dy0 - 6, dy0 + 7, 1):
        for dx in range(dx0 - 6, dx0 + 7, 1):
            ex0 = int(cxs + dx - tw / 2); ey0 = int(cys + dy - th / 2)
            v = ncc(t, eg[ey0:ey0 + th, ex0:ex0 + tw])
            if v > best[0]: best = (v, s, dx, dy)
v, s, dx, dy = best
print("align ncc=%.3f scale=%.3f dx=%d dy=%d" % best)

# transform base so its face lands on the edited face: scale about template centre then shift
cxs, cys = (x0 + x1) / 2, (y0 + y1) / 2
bimg = Image.fromarray(base.astype(np.uint8))
bw, bh = int(W * s), int(H * s)
bs = bimg.resize((bw, bh), Image.LANCZOS)
canvas = Image.new("RGB", (W, H))
ox = int(round(cxs + dx - cxs * s)); oy = int(round(cys + dy - cys * s))
canvas.paste(bs, (ox, oy))
moved = np.asarray(canvas, np.float32)

# elliptical feathered mask at the target face position
mcx, mcy = cxs + dx + (CX - cxs) * s, cys + dy + (CY - cys) * s
m = Image.new("L", (W, H), 0)
ImageDraw.Draw(m).ellipse([mcx - HW * s, mcy - HH * s, mcx + HW * s, mcy + HH * s], fill=255)
m = np.asarray(m.filter(ImageFilter.GaussianBlur(28)), np.float32)[..., None] / 255.0

# colour match the pasted face to the edited image's lighting (inside an inner region)
inner = (m[..., 0] > 0.9)
for c in range(3):
    ms, ss = moved[..., c][inner].mean(), moved[..., c][inner].std() + 1e-3
    me, se = edit[..., c][inner].mean(), edit[..., c][inner].std() + 1e-3
    moved[..., c] = (moved[..., c] - ms) * (0.5 * se / ss + 0.5) + (0.6 * me + 0.4 * ms)

out = edit * (1 - m) + np.clip(moved, 0, 255) * m
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(out_p, quality=95)
print("saved", out_p)
