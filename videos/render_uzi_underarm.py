import subprocess, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = sys.argv[1]
OUT = sys.argv[2]
W, H, FPS = 1080, 1920, 30
F = S + "/fonts/"
fB = lambda s: ImageFont.truetype(F + "Kanit-700-normal.ttf", s)
fBI = lambda s: ImageFont.truetype(F + "Kanit-700-italic.ttf", s)
fM = lambda s: ImageFont.truetype(F + "Kanit-500-normal.ttf", s)
fMI = lambda s: ImageFont.truetype(F + "Kanit-500-italic.ttf", s)

PINK = (214, 74, 140)
DEEP = (156, 52, 102)
WHITE = (255, 255, 255)

# start, end, panel, focus-x (0..1 of panel width), zoom direction, headline lines, voiceover script
SHOTS = [
    (0, 3, 1, 0.45, +1, [("รักแร้สวย", fBI, 112), ("มั่นใจได้ทุกมุม", fBI, 112)], "รักแร้สวย ไม่ต้องรอให้ถึงวันพิเศษ"),
    (3, 6, 2, 0.42, -1, [("ผิวดูเรียบเนียน", fBI, 104), ("กระจ่างใส", fBI, 112)], "เพราะผิวใต้วงแขน ก็ต้องการการดูแลเป็นพิเศษ"),
    (6, 9, 3, 0.48, +1, [("UZI Barbie", fB, 116), ("Clear & Fresh", fB, 96), ("Underarm Mask", fM, 64)], "เติมความมั่นใจด้วย UZI Barbie Clear & Fresh"),
    (9, 12, 4, 0.50, +1, [("เนื้อนุ่มละมุน", fBI, 112), ("เกลี่ยง่าย ซึมสบาย", fBI, 96)], "เนื้อมาสก์เนียนนุ่ม เกลี่ยง่าย บำรุงผิวใต้วงแขน"),
    (12, 16, 5, 0.45, -1, "BULLETS", "ช่วยให้ผิวดูเรียบเนียน กระจ่างใส และดูสม่ำเสมอขึ้น"),
    (16, 20, 6, 0.50, +1, [("OVERNIGHT", fBI, 112), ("UNDERARM CARE", fBI, 96)], "พร้อมบำรุงต่อด้วย UZI White Shot Mask สำหรับดูแลผิวยามค่ำคืน"),
    (20, 25, 7, 0.52, +1, [("BEAUTY", fBI, 120), ("IN EVERY MOVE", fBI, 96)], "ให้ทุกการยกแขน เต็มไปด้วยความมั่นใจ"),
    (25, 30, 8, 0.50, -1, "CTA", "UZI Underarm Mask ดูแลผิวใต้วงแขน ให้คุณมั่นใจในทุกวัน"),
]
BULLETS = ["ผิวดูเรียบเนียนขึ้น", "ดูกระจ่างใสขึ้น", "ผิวดูชุ่มชื้น น่าสัมผัส"]
XFADE = 0.4
TOTAL = 30


def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


# ---------- pre-build panel layers ----------
def build_layer(n, fx):
    im = Image.open(f"{S}/panels/p{n}.png").convert("RGB")
    pw, ph = im.size
    # cover crop to 9:16 around focus x
    cw = ph * W / H
    if cw <= pw:
        x0 = min(max(fx * pw - cw / 2, 0), pw - cw)
        box = (x0, 0, x0 + cw, ph)
    else:
        chh = pw * H / W
        box = (0, (ph - chh) / 2, pw, (ph + chh) / 2)
    big = im.resize((int(W * 1.12), int(H * 1.12)), Image.LANCZOS, box=box)
    big = big.filter(ImageFilter.UnsharpMask(radius=2.2, percent=70, threshold=2))
    # soft glow pass for a dreamy beauty look
    glow = big.filter(ImageFilter.GaussianBlur(14))
    big = Image.blend(big, Image.composite(glow, big, Image.new("L", big.size, 255)), 0.18)
    return big


CARD = {3, 6, 8}  # product shots: show whole panel on a blurred backdrop


def build_card(n):
    im = Image.open(f"{S}/panels/p{n}.png").convert("RGB")
    pw, ph = im.size
    bg = build_layer(n, 0.5).filter(ImageFilter.GaussianBlur(40))
    bg = Image.blend(bg, Image.new("RGB", bg.size, (250, 222, 234)), 0.35)
    cw = 860
    chh = int(ph * cw / pw)
    card = im.resize((cw, chh), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    mask = Image.new("L", card.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, cw, chh), radius=36, fill=255)
    bw, bh = bg.size
    x, y = (bw - cw) // 2, int((bh - H) / 2 + 150)
    sh = Image.new("L", bg.size, 0)
    ImageDraw.Draw(sh).rounded_rectangle((x + 6, y + 18, x + cw + 6, y + chh + 18), radius=36, fill=110)
    sh = sh.filter(ImageFilter.GaussianBlur(24))
    bg = Image.composite(Image.new("RGB", bg.size, (150, 60, 100)), bg, sh)
    bg.paste(card, (x, y), mask)
    return bg


layers = {s[2]: (build_card(s[2]) if s[2] in CARD else build_layer(s[2], s[3])) for s in SHOTS}

# bottom gradient (white-pink haze) to carry text
grad = np.zeros((H, W, 4), np.uint8)
for y in range(H):
    a = max(0.0, (y - H * 0.52) / (H * 0.48))
    grad[y, :, :3] = (255, 236, 244)
    grad[y, :, 3] = int(230 * a ** 1.4)
GRAD = Image.fromarray(grad, "RGBA")


def shot_frame(i, t_local, dur):
    st = SHOTS[i]
    big = layers[st[2]]
    p = t_local / dur
    z = 1.0 + 0.07 * (p if st[4] > 0 else 1 - p)
    bw, bh = big.size
    cw, chh = bw / 1.12 / z * 1.0, bh / 1.12 / z
    # bigger crop = less zoom; base crop is W*1.0 of the 1.12 enlarged layer
    cw, chh = W / z, H / z
    cx, cy = bw / 2, bh / 2 + (1 - p) * 10
    box = (cx - cw / 2, cy - chh / 2, cx + cw / 2, cy + chh / 2)
    return big.resize((W, H), Image.BILINEAR, box=box)


def draw_text_center(img, y, text, font, fill, shadow=True, alpha=1.0, glow=WHITE):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    w = d.textlength(text, font=font)
    x = (W - w) / 2
    if shadow:
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ds = ImageDraw.Draw(sh)
        ds.text((x, y), text, font=font, fill=glow + (255,), stroke_width=10, stroke_fill=glow + (255,))
        sh = sh.filter(ImageFilter.GaussianBlur(12))
        layer = Image.alpha_composite(layer, sh)
        d = ImageDraw.Draw(layer)
    d.text((x, y), text, font=font, fill=fill + (255,), stroke_width=2, stroke_fill=WHITE + (255,))
    if alpha < 1:
        a = layer.split()[3].point(lambda v: int(v * alpha))
        layer.putalpha(a)
    img.alpha_composite(layer)


def overlay(img, i, tl, dur):
    st = SHOTS[i]
    img.alpha_composite(GRAD)
    # timecode chip top-left like the storyboard header
    chip = Image.new("RGBA", img.size, (0, 0, 0, 0))
    dc = ImageDraw.Draw(chip)
    img.alpha_composite(chip)

    base_y = 1300
    if st[5] == "BULLETS":
        draw_text_center(img, 1180, "ปาดบางๆ ผิวดูชุ่มชื้น", fM(54), DEEP, alpha=ease(tl / 0.4))
        for k, b in enumerate(BULLETS):
            a = ease((tl - 0.3 - k * 0.6) / 0.4)
            if a <= 0:
                continue
            y = 1290 + k * 120 + (1 - a) * 40
            draw_text_center(img, y, "• " + b, fBI(80), PINK, alpha=a)
    elif st[5] == "CTA":
        a1 = ease(tl / 0.5)
        draw_text_center(img, 1270 + (1 - a1) * 40, "UZI UNDERARM MASK", fBI(96), PINK, alpha=a1)
        a2 = ease((tl - 0.5) / 0.5)
        if a2 > 0:
            pulse = 1 + 0.04 * math.sin(tl * 2 * math.pi * 1.2) * (tl > 1.0)
            bw, bh = int(620 * pulse), int(150 * pulse)
            btn = Image.new("RGBA", img.size, (0, 0, 0, 0))
            db = ImageDraw.Draw(btn)
            bx, by = (W - bw) // 2, 1440 + (150 - bh) // 2
            db.rounded_rectangle((bx, by, bx + bw, by + bh), radius=bh // 2, fill=PINK + (int(255 * a2),))
            db.text((W / 2, by + bh / 2 - 6), "ช้อปเลยวันนี้", font=fB(int(84 * pulse)), fill=WHITE + (int(255 * a2),), anchor="mm")
            img.alpha_composite(btn)
    else:
        lines = st[5]
        total_h = sum(int(s * 1.25) for _, _, s in lines)
        y = base_y + (330 - total_h) / 2
        for k, (txt, fn, sz) in enumerate(lines):
            a = ease((tl - 0.15 - k * 0.25) / 0.45)
            if a > 0:
                draw_text_center(img, y + (1 - a) * 40, txt, fn(sz), PINK, alpha=a)
            y += int(sz * 1.25)

    # voiceover subtitle
    a = ease((tl - 0.2) / 0.4) * (1 - ease((tl - (dur - 0.25)) / 0.25))
    if a > 0:
        sub = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ds = ImageDraw.Draw(sub)
        font = fM(44)
        words = st[6]
        # wrap to max width
        lines, cur = [], ""
        for w_ in words.split(" "):
            test = (cur + " " + w_).strip()
            if ds.textlength(test, font=font) > W - 160 and cur:
                lines.append(cur); cur = w_
            else:
                cur = test
        lines.append(cur)
        y = 1760 - (len(lines) - 1) * 32
        for ln in lines:
            tw = ds.textlength(ln, font=font)
            ds.rounded_rectangle(((W - tw) / 2 - 22, y - 34, (W + tw) / 2 + 22, y + 36), radius=18, fill=DEEP + (int(190 * a),))
            ds.text((W / 2, y), ln, font=font, fill=WHITE + (int(255 * a),), anchor="mm")
            y += 64
        img.alpha_composite(sub)
    return img


def frame_at(t):
    # find shot
    for i, st in enumerate(SHOTS):
        if st[0] <= t < st[1] or (i == len(SHOTS) - 1):
            break
    s0, s1 = SHOTS[i][0], SHOTS[i][1]
    tl = t - s0
    img = shot_frame(i, tl, s1 - s0).convert("RGBA")
    img = overlay(img, i, tl, s1 - s0)
    # crossfade from previous shot at the start of this one
    if i > 0 and tl < XFADE:
        p = SHOTS[i - 1]
        prev = shot_frame(i - 1, (p[1] - p[0]) + tl, p[1] - p[0] + XFADE).convert("RGBA")
        prev = overlay(prev, i - 1, (p[1] - p[0]) - 0.001, p[1] - p[0])
        k = ease(tl / XFADE)
        img = Image.blend(prev, img, k)
        # sparkle flash
        flash = Image.new("RGBA", img.size, (255, 240, 248, int(90 * math.sin(math.pi * tl / XFADE))))
        img.alpha_composite(flash)
    # fade in / out
    if t < 0.3:
        img = Image.blend(Image.new("RGBA", img.size, (255, 255, 255, 255)), img, ease(t / 0.3))
    return img.convert("RGB")


if __name__ == "__main__":
    if len(sys.argv) > 3:  # preview stills
        for t in map(float, sys.argv[3:]):
            frame_at(t).save(f"{S}/prev_{t:05.2f}.jpg", quality=88)
        sys.exit()
    ff = subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
         "-i", "-", "-i", f"{S}/music.wav", "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", OUT],
        stdin=subprocess.PIPE)
    n = TOTAL * FPS
    for f in range(n):
        ff.stdin.write(frame_at(f / FPS).tobytes())
        if f % 90 == 0:
            print(f"{f}/{n}", flush=True)
    ff.stdin.close()
    ff.wait()
