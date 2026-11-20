import sys, numpy as np, cv2
S = '/tmp/claude-0/-home-user-Content-UZI/1b687bd6-9481-56fc-bce1-0bad3a8bf317'
W_ = S + '/scratchpad/work/'
import os
BN = os.environ.get('BANNER', '1')
B = cv2.imread(S + f'/images/{BN}.webp').astype(np.float32)
R = cv2.imread(S + '/images/2.webp').astype(np.float32)
LB = np.load(W_ + f'lm{BN}.npy').astype(np.float32)
LR = np.load(W_ + 'lm2.npy').astype(np.float32)
H, Wd = B.shape[:2]

# params
SHAPE_KEEP = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0   # 1 = keep banner contour, 0 = real contour
OUT = sys.argv[2] if len(sys.argv) > 2 else 'out.png'

OVAL = [10,338,297,332,284,251,389,356,454,323,361,288,397,365,379,378,400,377,152,148,176,149,150,136,172,58,132,93,234,127,162,21,54,103,67,109]
KEY = [33,133,362,263,1,61,291,168,6,4,0,17]

# 1. similarity transform real -> banner
M, _ = cv2.estimateAffinePartial2D(LR[KEY], LB[KEY], method=cv2.LMEDS)
T = (np.c_[LR, np.ones(len(LR))] @ M.T).astype(np.float32)

# 2. destination landmarks: inner = real geometry (T), contour -> banner (B)
oval_poly = LB[OVAL]
face_w = np.linalg.norm(LB[234] - LB[454])
d = np.array([abs(cv2.pointPolygonTest(oval_poly.reshape(-1,1,2), (float(p[0]), float(p[1])), True)) for p in LB])
w = np.clip(d / (0.18 * face_w), 0, 1)
w = w * w * (3 - 2 * w)  # smoothstep
w = 1 - SHAPE_KEEP * (1 - w)
D = (w[:, None] * T + (1 - w[:, None]) * LB).astype(np.float32)

# 3. piecewise affine warp of R onto D
rect = (0, 0, Wd, H)
sub = cv2.Subdiv2D(rect)
for p in D:
    sub.insert((float(np.clip(p[0], 0, Wd-1)), float(np.clip(p[1], 0, H-1))))
idx_of = {(round(float(np.clip(p[0],0,Wd-1)),2), round(float(np.clip(p[1],0,H-1)),2)): i for i, p in enumerate(D)}
tris = []
for t in sub.getTriangleList():
    pts = [(round(t[0],2), round(t[1],2)), (round(t[2],2), round(t[3],2)), (round(t[4],2), round(t[5],2))]
    ids = []
    for q in pts:
        if q in idx_of: ids.append(idx_of[q])
        else:
            dd = np.linalg.norm(D - np.array(q), axis=1); j = int(dd.argmin())
            if dd[j] < 0.5: ids.append(j)
    if len(ids) == 3: tris.append(ids)

warped = np.zeros_like(B); cover = np.zeros((H, Wd), np.float32)
for (a, b, c) in tris:
    src = LR[[a, b, c]]; dst = D[[a, b, c]]
    r1 = cv2.boundingRect(src); r2 = cv2.boundingRect(dst)
    s = src - r1[:2]; t = dst - r2[:2]
    A = cv2.getAffineTransform(s.astype(np.float32), t.astype(np.float32))
    patch = R[r1[1]:r1[1]+r1[3], r1[0]:r1[0]+r1[2]]
    if patch.size == 0: continue
    out = cv2.warpAffine(patch, A, (r2[2], r2[3]), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT_101)
    m = np.zeros((r2[3], r2[2]), np.float32)
    cv2.fillConvexPoly(m, np.int32(np.round(t)), 1.0, cv2.LINE_AA)
    y0, x0 = r2[1], r2[0]
    y1, x1 = min(y0 + r2[3], H), min(x0 + r2[2], Wd)
    out = out[:y1-y0, :x1-x0]; m = m[:y1-y0, :x1-x0]
    warped[y0:y1, x0:x1] = warped[y0:y1, x0:x1] * (1 - m[..., None]) + out * m[..., None]
    cover[y0:y1, x0:x1] = np.maximum(cover[y0:y1, x0:x1], m)

# 4. hand masks
hand_B = np.array([(95,380),(198,398),(206,440),(218,462),(236,478),(236,512),(222,526),(264,534),(276,556),(266,578),(244,588),(236,612),(205,628),(95,665)], np.int32)
hand_R = np.array([(190,470),(272,476),(304,536),(306,600),(334,612),(374,648),(376,700),(352,742),(338,800),(190,810)], np.int32)
mB = np.zeros((H, Wd), np.uint8); cv2.fillPoly(mB, [hand_B], 255)
mR = np.zeros(R.shape[:2], np.uint8); cv2.fillPoly(mR, [hand_R], 255)
k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (19, 19))
mB = cv2.dilate(mB, k); mR = cv2.dilate(mR, k)
# warp real-hand mask into banner space via same mesh (approx with similarity M)
mRw = cv2.warpAffine(mR, M, (Wd, H))

# 5. face mask: oval of D shrunk toward centre
cen = D[OVAL].mean(0)
poly = (cen + (D[OVAL] - cen) * 0.93)
# cut forehead lower (keep banner hairline)
top_cut = LB[10][1] + 0.35 * (LB[168][1] - LB[10][1])
fm = np.zeros((H, Wd), np.uint8); cv2.fillPoly(fm, [np.int32(poly)], 255)
fm[:int(top_cut)] = 0
fm = cv2.bitwise_and(fm, cv2.bitwise_not(mB)); fm = cv2.bitwise_and(fm, cv2.bitwise_not(mRw))
fm = (fm.astype(np.float32) / 255) * (cover > 0.99)
fm = cv2.erode(fm, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
alpha = cv2.GaussianBlur(fm, (0, 0), 9)
alpha = np.clip(alpha * 1.15, 0, 1) * (cv2.GaussianBlur(fm, (0,0), 3) > 0.01)

# 6. colour match (LAB mean/std) on skin core
core = cv2.erode((fm > 0.5).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))).astype(bool)
def feat_mask(L, shape):
    m = np.zeros(shape, np.uint8)
    for ids in ([33,7,163,144,145,153,154,155,133,173,157,158,159,160,161,246],
                [362,382,381,380,374,373,390,249,263,466,388,387,386,385,384,398],
                [70,63,105,66,107,55,65,52,53,46], [300,293,334,296,336,285,295,282,283,276],
                [61,146,91,181,84,17,314,405,321,375,291,409,270,269,267,0,37,39,40,185]):
        cv2.fillPoly(m, [np.int32(cv2.convexHull(L[ids]))], 1)
    return cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))).astype(bool)
skin = core & ~feat_mask(D, (H, Wd)) & ~feat_mask(LB, (H, Wd))
labB = cv2.cvtColor(np.clip(B,0,255).astype(np.uint8), cv2.COLOR_BGR2LAB).astype(np.float32)
labW = cv2.cvtColor(np.clip(warped,0,255).astype(np.uint8), cv2.COLOR_BGR2LAB).astype(np.float32)
for ch in range(3):
    mb, sb = labB[..., ch][skin].mean(), labB[..., ch][skin].std()
    mw, sw = labW[..., ch][skin].mean(), labW[..., ch][skin].std()
    ratio = np.clip(sb / (sw + 1e-6), 0.7, 1.3)
    labW[..., ch] = (labW[..., ch] - mw) * ratio + mb

# 7. low-frequency lighting match (masked normalized blur)
def mblur(x, m, s):
    return cv2.GaussianBlur(x * m, (0, 0), s) / (cv2.GaussianBlur(m, (0, 0), s) + 1e-4)
sm = skin.astype(np.float32)
SIG = float(sys.argv[3]) if len(sys.argv) > 3 else 14
for ch in range(3):
    diff = mblur(labB[..., ch], sm, SIG) - mblur(labW[..., ch], sm, SIG)
    diff2 = mblur(labB[..., ch], sm, 40) - mblur(labW[..., ch], sm, 40)
    labW[..., ch] += (diff * 0.75 + diff2 * 0.25) * (1.0 if ch == 0 else 0.85)
Wc = cv2.cvtColor(np.clip(labW, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR).astype(np.float32)

# 8. retouch skin of warped face (soften texture, keep features)
fmask = feat_mask(D, (H, Wd)).astype(np.float32)
fmask = cv2.GaussianBlur(fmask, (0, 0), 6)
smooth = cv2.bilateralFilter(Wc.astype(np.uint8), 9, 28, 7).astype(np.float32)
lowW = cv2.GaussianBlur(Wc, (0, 0), 2.2)
detail = Wc - lowW
smooth_keep = cv2.GaussianBlur(smooth, (0, 0), 1.0) + detail * 0.35
Wr = Wc * fmask[..., None] + smooth_keep * (1 - fmask[..., None])

# 9. blend (Laplacian pyramid)
def lap_blend(a, b, m, levels=5):
    ga, gb, gm = [a], [b], [m]
    for i in range(levels):
        ga.append(cv2.pyrDown(ga[-1])); gb.append(cv2.pyrDown(gb[-1])); gm.append(cv2.pyrDown(gm[-1]))
    out = ga[-1] * gm[-1][..., None] + gb[-1] * (1 - gm[-1][..., None])
    for i in range(levels - 1, -1, -1):
        size = (ga[i].shape[1], ga[i].shape[0])
        la = ga[i] - cv2.pyrUp(ga[i + 1], dstsize=size)
        lb = gb[i] - cv2.pyrUp(gb[i + 1], dstsize=size)
        out = cv2.pyrUp(out, dstsize=size) + la * gm[i][..., None] + lb * (1 - gm[i][..., None])
    return out
res = lap_blend(Wr, B, alpha)
res = res * alpha[..., None] + B * (1 - alpha[..., None]) if False else res
# outside mask region keep banner exactly
hard = cv2.dilate((alpha > 0.002).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31))).astype(np.float32)
hard = cv2.GaussianBlur(hard, (0, 0), 6)
res = res * hard[..., None] + B * (1 - hard[..., None])
# 10. transfer banner's glass-skin specular highlights
GL = float(sys.argv[4]) if len(sys.argv) > 4 else 0.9
faceB = np.zeros((H, Wd), np.uint8); cv2.fillPoly(faceB, [np.int32(LB[OVAL])], 1)
skinB = (faceB.astype(bool) & ~feat_mask(LB, (H, Wd)) & ~(mB > 0)).astype(np.float32)
LBl = labB[..., 0]
spec = np.clip(LBl - mblur(LBl, skinB, 18), 0, None) * skinB
spec = cv2.GaussianBlur(spec, (0, 0), 2.0)
nf = 1 - cv2.GaussianBlur(feat_mask(D, (H, Wd)).astype(np.float32), (0, 0), 5)
labR = cv2.cvtColor(np.clip(res, 0, 255).astype(np.uint8), cv2.COLOR_BGR2LAB).astype(np.float32)
labR[..., 0] += spec * GL * alpha * nf
res = cv2.cvtColor(np.clip(labR, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR).astype(np.float32)
# 11. lift grey shadow on upper lip (philtrum)
ph_ids = [61,185,40,39,37,0,267,269,270,409,291,322,391,393,164,167,165,92]
pm = np.zeros((H, Wd), np.float32); cv2.fillPoly(pm, [np.int32(cv2.convexHull(D[ph_ids]))], 1)
lipm = np.zeros((H, Wd), np.float32); cv2.fillPoly(lipm, [np.int32(cv2.convexHull(D[[61,185,40,39,37,0,267,269,270,409,291,375,321,405,314,17,84,181,91,146]]))], 1)
pm = np.clip(pm - cv2.dilate(lipm, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))), 0, 1)
pm = cv2.GaussianBlur(pm, (0,0), 4) * alpha
labR = cv2.cvtColor(np.clip(res, 0, 255).astype(np.uint8), cv2.COLOR_BGR2LAB).astype(np.float32)
ring = cv2.dilate((pm>0.05).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(41,41))).astype(np.float32)
ring = ring * (1 - (pm>0.05)) * (1 - cv2.dilate(lipm, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9))))
for ch in range(3):
    ref = mblur(labR[..., ch], ring, 12)
    if ch == 0:
        lift = np.clip(ref - labR[..., ch], 0, None)
        labR[..., ch] += lift * 0.9 * pm
    else:
        labR[..., ch] += (ref - labR[..., ch]) * 0.6 * pm
res = cv2.cvtColor(np.clip(labR, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR).astype(np.float32)
res = res * hard[..., None] + B * (1 - hard[..., None])
cv2.imwrite(W_ + OUT, np.clip(res, 0, 255).astype(np.uint8))
cv2.imwrite(W_ + 'alpha.png', (alpha * 255).astype(np.uint8))
print('done', OUT, 'tris', len(tris))
