# UZI Natural Rose Crystal Lip Gloss — "Billboard Gloss Toss"

**แนวคลิป:** FOOH / 3D Billboard (ทำตามคลิปตัวอย่าง: นางนั่งบนจอ LED โค้งหัวมุมตึก แล้วโยนสินค้าออกจากจอมาให้มือจริงรับ)
**สัดส่วน:** 9:16 แนวตั้ง | **ความยาว:** ~15 วิ | **ช็อตที่เพิ่ม:** หยิบลิป → เปิดฝา → ทาด้วยแท่งจุ่ม (doe-foot) → ทาเสร็จ มองกล้อง → ปิดฝา → โยนลงมา

---

## 0. เตรียม Reference ก่อนเจน

| Ref | ใช้ภาพไหน | ใช้ทำอะไร |
|---|---|---|
| @Image1 หน้านาง | IMG_4276 (ครอปเฉพาะหน้า+ไหล่) | ล็อกหน้า ผม ต่างหู |
| @Image2 ชุดเต็มตัว | IMG_4277 | ล็อกชุดฟ้า ลูกไม้ หัวเข็มขัด หางชุด ส้นสูง |
| @Image3 สินค้า | Lip Gloss PNG | ล็อกทรงขวด ฝา สีกลอส ฉลาก |
| (เสริม) ด้านหลัง | IMG_4274 | เชือกผูกหลังชุด |

- **ลบพื้นหลังป้าย Ren Clinic / "The Right Solution For You" ออกก่อน** (Remove BG) ไม่งั้น AI จะเอาโลโก้คลินิกไปโผล่ในวิดีโอ
- ภาพสินค้าไม่เห็นแท่งทา: ต้องบรรยายใน prompt ว่าเป็นแท่งใส ปลายฟองน้ำ doe-foot
- ควรเช็กสิทธิ์/ความยินยอมของนางแบบในการใช้หน้าทำวิดีโอ AI สำหรับโฆษณา

---

## 1. Storyboard

| # | เวลา | มุมกล้อง | แอคชั่น | เสียง |
|---|---|---|---|---|
| 1 | 0:00–0:02 | Wide มุมต่ำ ถือมือถือถ่ายจากฟุตบาท มองขึ้นจอ LED โค้งหัวมุมตึก | นางนอนเอนบนขอบขาวล่างจอ พื้นหลังจอเป็นฟ้ามีเมฆ อมชมพู ลิปกลอสขวดยักษ์ตั้งข้างมือ แท็กซี่วิ่งผ่านด้านล่าง | เสียงเมือง รถ |
| 2 | 0:02–0:04 | Wide (เหมือนเดิม) | ลุกขึ้นนั่ง ไขว่ห้าง **ขา+ส้นสูงยื่นทะลุขอบจอออกมานอกตึก** (3D pop-out) หางชุดผ้าซาตินพลิ้วห้อยลงมา เอื้อมหยิบลิปขึ้นมาระดับคาง | ผ้าพลิ้ว swoosh |
| 3 | 0:04–0:05.5 | มือถือซูมพุ่งเข้าจอ → MCU (ยังเห็นขอบจอ/ตึกนิดๆ ให้รู้ว่าเป็นจอ) | หันฉลากออกกล้อง **บิดเปิดฝา** ดึงแท่งทา doe-foot ออกมา กลอสโรสฉ่ำมีหยดวาว | "คลิก" เปิดฝา |
| 4 | 0:05.5–0:08 | ECU ปาก บนจอยักษ์ | **ทาปากล่าง → ปากบน** เนื้อกลอสใสวาวแบบแก้ว สีโรสอมแดง แสงไล่ประกายบนปาก เห็นเล็บชมพูประดับเพชร | เสียงทากลอสเบาๆ |
| 5 | 0:08–0:09.5 | CU หน้า | เม้มปาก "ป๊อป" แล้ว **ช้อนตามองตรงมาที่กล้อง** ยิ้มมุมปาก เอียงหน้านิดๆ (ลุคเดียวกับรูปงาน) | lip pop |
| 6 | 0:09.5–0:10.5 | CU (สบตาค้าง) | เสียบแท่งกลับ **ปิดฝา** หมุนล็อก ยกขวดโชว์ข้างแก้ม ฉลากหันกล้อง | "คลิก" ปิดฝา |
| 7 | 0:10.5–0:12.5 | ตัดกลับ Wide มุมถนน | ขยิบตา แล้ว **เหวี่ยงแขนโยนลิป** ขวดลอยทะลุขอบจอขึ้นฟ้าจริง หมุนติ้ว ตกลงมาหากล้อง ใหญ่ขึ้นเรื่อยๆ (แบบในคลิป) | whoosh (slow-mo ตอนหลุดจอ) |
| 8 | 0:12.5–0:15 | POV มือจริงรับ | มือโผล่จากล่างเฟรมรับขวดพอดี โฟกัสดึงมาที่ขวด ฉลากชัด แดดส่องทะลุขวดใสสีโรส นางบนจอเบลอด้านหลังโบกมือ/ส่งจูบ + End card | เสียงรับ "ตั้บ" + music hit |

**End card:** `UZI Natural Rose Crystal Lip Gloss` + โลโก้ UZI + CTA (เช่น "สั่งเลยที่ตะกร้า")

---

## 2. Consistency Block (แปะในทุก prompt)

```
[CHARACTER] the woman from @Image1 and @Image2 (keep exact same face): long voluminous copper-auburn hair in glossy Hollywood waves with a deep side part, light grey-blue eyes, shimmering soft-pink glam makeup, long lashes, rosy blush, sparkling silver star-cluster chandelier earrings, long pink jeweled stiletto nails; strapless powder ice-blue shimmering satin mini dress with ivory floral lace trim along the neckline and asymmetric hem, draped satin sash with a polished silver buckle at her left hip flowing into a long satin train, silver rhinestone ankle-strap stilettos.

[PRODUCT] the lip gloss from @Image3: slim crystal-clear thick-walled acrylic cylinder bottle filled with sheer muted rose-red gloss, tall transparent cylindrical cap with a ridged clear threaded collar and a pale pink inner sleeve, white vertical text "NATURAL ROSE CRYSTAL LIP GLOSS", small "UZI COSMETIC" logo near the base. The cap pulls out a clear stem with a soft doe-foot applicator.

[SCENE] low-angle handheld smartphone view from a busy city street corner looking up at a giant curved corner LED billboard (3D anamorphic FOOH style) wrapped around a high-rise with gold-mirrored glass; inside the screen: soft sky-blue backdrop with fluffy clouds and a blush-pink glow, a glossy white curved ledge along the bottom of the screen; yellow taxis and pedestrians below; late-afternoon natural daylight.

[STYLE] photorealistic, shot on iPhone, natural handheld micro-shake, realistic physics, 4K detail, 9:16 vertical.
```

**Negative prompt:**
```
different face, face morphing, distorted hands, extra fingers, deformed bottle, wrong product shape, garbled text, misspelled label, extra logos, Ren Clinic logo, watermark, subtitles, cartoon, CGI plastic look, flicker, warped billboard
```

---

## 3A. Prompt แบบเจนทีเดียว 15 วิ (Multi-shot: Seedance 2.0 / Kling 3–4 multi-shot / tools ที่ทำได้ 15 วิ)

> แนบ @Image1 หน้า, @Image2 ชุด, @Image3 สินค้า (เปลี่ยนสัญลักษณ์ @ ให้ตรงกับ tool ที่ใช้)

```
9:16 vertical, 15 seconds, photorealistic FOOH 3D billboard ad, filmed handheld on a smartphone from a busy city street corner looking up at a giant curved corner LED billboard on a gold-mirrored glass skyscraper. The woman is @Image1 wearing the outfit in @Image2 (copper-auburn wavy hair, star chandelier earrings, strapless ice-blue satin mini dress with ivory lace trim, silver buckle sash with long train, pink jeweled nails). The product is the lip gloss in @Image3.

[0-2s] On the screen, she reclines on a glossy white ledge against a soft sky-blue cloud backdrop with a blush-pink glow; the giant lip gloss stands beside her hand. Yellow taxis pass below.
[2-4s] She sits up and crosses her legs; her legs and silver stilettos extend past the bottom edge of the screen into the real street (3D pop-out), her satin train spills over the edge and flutters. She picks up the lip gloss.
[4-5.5s] The phone quickly zooms into the billboard, LED screen edges still visible. Medium close-up: she twists open the clear cap and pulls out the doe-foot applicator glistening with sheer rose gloss.
[5.5-8s] Extreme close-up of her lips on the giant screen: she glides the gloss over her lower lip, then upper lip, leaving a glassy high-shine sheer rose finish, light glinting across it.
[8-10.5s] She presses her lips together with a soft pop, then looks straight into the camera with a confident half-smile and slight head tilt; holding eye contact, she slides the wand back in and twists the cap closed.
[10.5-12.5s] Cut back to the wide street shot: she winks and tosses the lip gloss overhand; it flies out of the screen into the real sky, spins, and falls toward the camera, growing larger.
[12.5-15s] A real hand enters from the bottom of the frame and catches it; focus racks to the lip gloss, label "NATURAL ROSE CRYSTAL LIP GLOSS" facing camera, sunlight shining through the clear rose bottle; the billboard behind falls into soft blur as she waves and blows a kiss.

Keep her face, hair, earrings, dress and nails identical in every shot; keep the product shape and label consistent. Natural handheld micro-shake, realistic physics, natural daylight, city ambience sound.
```

---

## 3B. Prompt แบบแยก 4 ท่อน (tools ที่เจนได้ 5–10 วิ / ใช้ First–Last frame)

**ขั้นตอน:** เจนภาพ Start frame ด้วย image model (Nano Banana / Seedream / GPT Image / Kling Image) + แนบ ref → เอาไปทำ Image-to-Video ด้วย Video prompt → ต่อใน CapCut
แต่ละ prompt ให้แปะ Consistency Block ไว้ข้างหน้า

### ท่อน 1 (0:00–0:04) = ช็อต 1–2 · ยาว 4–5 วิ

**Start frame (image):**
```
[SCENE] On the giant curved LED billboard, [CHARACTER] reclines on her side along the glossy white ledge at the bottom of the screen, propped on one elbow, legs extended, satin train draped over the ledge. A giant [PRODUCT] stands upright beside her hand, scaled to her size. Yellow taxis and pedestrians on the street below. [STYLE]
```
**Video:**
```
Handheld smartphone, camera nearly static with natural micro-shake. On the giant curved 3D billboard, the woman slowly rises from reclining to sitting on the ledge and crosses her legs; her lower legs and silver stilettos extend beyond the bottom edge of the screen, out over the street, creating a 3D pop-out illusion; her ice-blue satin train slips over the edge and flutters in the wind. She reaches to her side, picks up the giant lip gloss with her right hand and brings it up near her chin, label facing the camera. Taxis keep moving below. Consistent face and outfit, realistic physics.
```

### ท่อน 2 (0:04–0:08) = ช็อต 3–4 · ยาว 4–5 วิ

**Start frame (image):**
```
Smartphone zoomed in on a giant LED billboard: medium close-up of [CHARACTER] on the screen, holding [PRODUCT] at chin level with the label facing out, fingers on the cap; LED screen edge and gold-glass building facade visible at the frame edges, soft sky-blue cloud backdrop with blush-pink glow. [STYLE]
```
**Video:**
```
Quick handheld digital zoom settles on the billboard. She twists open the clear cap and pulls out the wand: a soft doe-foot applicator loaded with glossy sheer rose-red gloss, a drop glistening at the tip. The camera pushes in to an extreme close-up of her lips on the giant screen as she glides the applicator along her lower lip, then her upper lip, slowly and precisely, leaving a glass-like high-shine sheer rose finish; light glints across the gloss; her pink jeweled nails are visible. Beauty-commercial detail, still clearly a giant screen.
```

### ท่อน 3 (0:08–0:10.5) = ช็อต 5–6 · ยาว 3–5 วิ
> ใช้ **เฟรมสุดท้ายของท่อน 2** เป็น Start frame (ต่อเนียน)

**Video:**
```
Close-up on the billboard. She presses her lips together softly and releases with a subtle lip pop; the fresh rose gloss catches the light. She lifts her gaze and looks straight down into the camera with a confident, flirty half-smile and a slight head tilt, holding eye contact. Without breaking eye contact, she slides the wand back into the bottle and twists the cap closed, then holds the closed lip gloss beside her cheek, label facing the camera. Camera slowly pulls back slightly.
```

### ท่อน 4 (0:10.5–0:15) = ช็อต 7–8 · ยาว 5 วิ
> แนะนำใช้ **First + Last frame**: Last frame = มือจริงถือขวดจริง (ทำจาก PNG สินค้า) เพื่อให้ฉลากตอนจบเป๊ะ

**Start frame (image):**
```
[SCENE] On the billboard, [CHARACTER] sits on the ledge with legs crossed, stilettos extending past the bottom edge of the screen, right arm raised holding the closed [PRODUCT], about to throw, playful smile. [STYLE]
```
**Last frame (image):**
```
Close-up POV: a real human hand in the foreground holding [PRODUCT] upright, label "NATURAL ROSE CRYSTAL LIP GLOSS" and UZI logo sharp and facing camera, sunlight shining through the clear bottle and rose gloss; behind it, the giant curved billboard with the woman waving is softly out of focus. [STYLE]
```
**Video:**
```
Same low-angle handheld street shot. On the 3D billboard, she winks and tosses the lip gloss overhand toward the viewer. The bottle flies out of the screen, breaking through the billboard frame into the real sky above the street, spins in the air, then falls down toward the camera, growing larger. A real hand enters from the bottom of the frame and catches it cleanly. Focus racks from the billboard to the lip gloss in the hand: crisp product, label facing the camera, sunlight glinting through the clear rose bottle; the billboard behind falls into soft bokeh as she waves and blows a kiss.
```

---

## 4. Post / ตัดต่อ (CapCut)

- **Speed ramp:** ตอนขวดหลุดจอ (ประมาณ 0:11) slow-mo 0.5x → เร่งกลับตอนตกใกล้กล้อง
- **SFX:** เสียงเมือง ตลอดคลิป / คลิกเปิดฝา / เสียง lip pop / คลิกปิดฝา / whoosh / เสียงรับ + music hit ตอนจบ
- **ฉลากเพี้ยน?** แปะ PNG สินค้าจริงทับมือในช็อต 8 แล้วใช้ Motion Tracking ตามมือ
- **Option กรุงเทพ:** เปลี่ยน [SCENE] เป็น `Bangkok Ratchaprasong intersection, pink and green-yellow taxis, BTS skytrain track` แท็กซี่ชมพูเข้ากับสีโรสของลิป
