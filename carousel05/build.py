#!/usr/bin/env python3
"""LB Carousel 05: "To Haarlem. On foot. Carrying fish."

Renders the 3-slide Instagram carousel (1080 x 1350, sRGB PNG) in the LookyBooky
house template (same as Carousel 03): Poppins headline at a 90 px left margin in the
upper third, Inter labels, Ocean / Mist / white, Turquoise only as a small rule.

Source photos go in work/src/ (unaltered originals from "Use of LookyBooky"):
    LB2026_KimKramer_ZM18.jpg   slide 1
    LB2026_KimKramer_ZM01.jpg   slide 3
While a photo is missing, its slides are rendered to proofs/ only, with a grey
"photo pending" slot, and never with the final export names.

Run:  python3 build.py
"""
from pathlib import Path

from PIL import Image, ImageCms, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent
WORK, OUT, PROOF = ROOT / "work", ROOT / "output", ROOT / "proofs"
SRC = WORK / "src"
FONTS = WORK / "fonts"
LOGO = WORK / "brand" / "lookybooky-logo-white_from-guidelines-pdf.png"

W, H = 1080, 1350
M = 90                       # left / right margin on every slide
HEAD_TOP = 118               # line box top; puts the cap line at ~y 140, as in the house template
HEAD_LH = 1.0                # tight leading, as in the house template

OCEAN = (14, 47, 57)
MIST = (243, 247, 246)
TURQ = (24, 191, 203)
WHITE = (255, 255, 255)

POPPINS_700 = FONTS / "Poppins-Bold.ttf"
POPPINS_600 = FONTS / "Poppins-SemiBold.ttf"
INTER_400 = FONTS / "Inter-Regular.otf"
INTER_600 = FONTS / "Inter-SemiBold.otf"

HEAD_1 = ["To Haarlem.", "On foot.", "Carrying fish."]
HEAD_3 = ["Meet the women", "behind the story."]
FACT = "Zandvoort’s fish sellers carried heavy baskets from the beach to Haarlem to sell the catch."
FACT_SUB = "Their work helped support their families."
LABEL = "Zandvoortse Vrouwen · Zandvoorts Museum"
DATE = "Until 4 April 2027"
CREDIT = "Photo: Kim Kramer"

# Crops: the 4:5 window is the largest that fits the photo; focus_x / focus_y (0..1)
# place it. zoom > 1 tightens. Tuned per photo once the originals are in work/src/.
PHOTOS = {
    "ZM18": dict(file="LB2026_KimKramer_ZM18.jpg", focus_x=0.5, focus_y=0.0, zoom=1.0, keystone=0.0),
    "ZM01": dict(file="LB2026_KimKramer_ZM01.jpg", focus_x=0.5, focus_y=0.0, zoom=1.0, keystone=0.0),
}
# Headline treatment on photos: "auto" picks white unless the area behind it is too
# light for 3:1 (large-text WCAG), then falls back to Ocean on a small Mist panel.
HEAD_MODE = {"ZM18": "auto", "ZM01": "auto"}


def font(path, size):
    return ImageFont.truetype(str(path), size)


def srgb(im):
    """Convert to sRGB using the embedded ICC profile, if any. No other colour change."""
    icc = im.info.get("icc_profile")
    if icc:
        import io
        src = ImageCms.ImageCmsProfile(io.BytesIO(icc))
        im = ImageCms.profileToProfile(im, src, ImageCms.createProfile("sRGB"), outputMode="RGB")
    return im.convert("RGB")


def load_photo(key):
    cfg = PHOTOS[key]
    p = SRC / cfg["file"]
    if not p.exists():
        return None
    im = srgb(ImageOps.exif_transpose(Image.open(p)))
    if cfg["keystone"]:
        # Vertical-perspective correction only: pull the top corners in/out by k * width.
        w, h = im.size
        k = cfg["keystone"] * w
        quad = (k, 0, 0, h, w, h, w - k, 0)  # UL, LL, LR, UR source points
        im = im.transform((w, h), Image.QUAD, quad, Image.BICUBIC)
        crop = int(abs(k)) + 2
        im = im.crop((crop, 0, w - crop, h))
    w, h = im.size
    cw = min(w, h * W / H) / cfg["zoom"]
    ch = cw * H / W
    x0 = (w - cw) * cfg["focus_x"]
    y0 = (h - ch) * cfg["focus_y"]
    box = tuple(round(v) for v in (x0, y0, x0 + cw, y0 + ch))
    cfg["_crop"] = box
    cfg["_size"] = (w, h)
    return im.resize((W, H), Image.LANCZOS, box=box)


def pending(key):
    im = Image.new("RGB", (W, H), (126, 138, 142))
    d = ImageDraw.Draw(im)
    f = font(INTER_600, 30)
    d.text((W // 2, H // 2), f"PHOTO PENDING: {PHOTOS[key]['file']}", font=f, fill=(225, 230, 231), anchor="mm")
    return im


def rel_lum(rgb):
    def c(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (c(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def headline(d, lines, size, color, top=HEAD_TOP):
    f = font(POPPINS_700, size)
    step = round(size * HEAD_LH)
    boxes = []
    for i, line in enumerate(lines):
        y = top + i * step
        d.text((M, y), line, font=f, fill=color, anchor="la")
        boxes.append(d.textbbox((M, y), line, font=f, anchor="la"))
    return (min(b[0] for b in boxes), min(b[1] for b in boxes),
            max(b[2] for b in boxes), max(b[3] for b in boxes))


def text_box(lines, size, top=HEAD_TOP):
    tmp = ImageDraw.Draw(Image.new("L", (W, H)))
    f = font(POPPINS_700, size)
    step = round(size * HEAD_LH)
    bs = [tmp.textbbox((M, top + i * step), l, font=f, anchor="la") for i, l in enumerate(lines)]
    return (min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs))


def worst_contrast(photo, box):
    """Contrast of white against the lightest 10% of the area behind the text."""
    region = photo.crop(box).filter(ImageFilter.BoxBlur(6)).resize((64, 32))
    lums = sorted(rel_lum(p) for p in region.get_flattened_data())
    l90 = lums[int(len(lums) * 0.9)]
    return 1.05 / (l90 + 0.05)


def soft_shadow(base, draw_fn, offset=2, blur=6, alpha=0.45):
    """Small, soft Ocean text shadow (as in Reel 5); a text effect, not an overlay box."""
    mask = Image.new("L", base.size, 0)
    draw_fn(ImageDraw.Draw(mask))
    mask = mask.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * alpha))
    sh = Image.new("RGB", base.size, OCEAN)
    shifted = Image.new("L", base.size, 0)
    shifted.paste(mask, (0, offset))
    base.paste(sh, (0, 0), shifted)


def photo_headline(im, lines, size, key, log):
    box = text_box(lines, size)
    mode = HEAD_MODE[key]
    pad = 36
    if mode == "auto":
        c = worst_contrast(im, tuple(v + d for v, d in zip(box, (-pad, -pad, pad, pad))))
        mode = "white" if c >= 3.0 else "panel"
        log.append(f"{key}: white-on-photo contrast (lightest 10% behind headline) = {c:.2f}:1 -> {mode}")
    d = ImageDraw.Draw(im)
    if mode == "panel":
        d.rectangle((box[0] - pad, box[1] - pad, box[2] + pad, box[3] + pad), fill=MIST)
        headline(d, lines, size, OCEAN)
    else:
        headline(ImageDraw.Draw(im), lines, size, WHITE)  # template: clean white, no shadow
    return mode


def credit(im):
    f = font(INTER_400, 22)
    y = H - 40
    soft_shadow(im, lambda md: md.text((M, y), CREDIT, font=f, fill=255, anchor="ls"), offset=1, blur=4, alpha=0.5)
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((M, y), CREDIT, font=f, fill=(255, 255, 255, 204), anchor="ls")  # 80%
    im.paste(layer, (0, 0), layer)


def slide1(with_credit, log):
    im = load_photo("ZM18")
    final = im is not None
    im = im if final else pending("ZM18")
    photo_headline(im, HEAD_1, 92, "ZM18", log)
    if with_credit:
        credit(im)
    return im, final


def slide1_alt():
    im = Image.new("RGB", (W, H), OCEAN)
    headline(ImageDraw.Draw(im), HEAD_1, 92, MIST)
    return im


def wrap(text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if f.getlength(t) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def slide2():
    im = Image.new("RGB", (W, H), MIST)
    d = ImageDraw.Draw(im)
    fm, fs = font(POPPINS_600, 58), font(INTER_400, 36)
    main = wrap(FACT, fm, W - 2 * M)
    sub = wrap(FACT_SUB, fs, W - 2 * M)
    m_step, s_step = round(58 * 1.25), round(36 * 1.4)
    rule_h, rule_gap, sub_gap = 4, 48, 40
    # Height of the text block from cap-top of the first line to the last sub line.
    asc_m = fm.getbbox("Z")[1]
    block = rule_h + rule_gap + (len(main) - 1) * m_step + 58 * 1.0 + sub_gap + (len(sub) - 1) * s_step + 36
    y = round((H - block) / 2)
    d.rectangle((M, y, M + 47, y + rule_h - 1), fill=TURQ)
    y += rule_h + rule_gap
    for i, l in enumerate(main):
        d.text((M, y + i * m_step - asc_m), l, font=fm, fill=OCEAN, anchor="la")
    y += (len(main) - 1) * m_step + 58 + sub_gap
    ocean80 = tuple(round(o * 0.8 + m * 0.2) for o, m in zip(OCEAN, MIST))  # Ocean at 80% on Mist
    asc_s = fs.getbbox("T")[1]
    for i, l in enumerate(sub):
        d.text((M, y + i * s_step - asc_s), l, font=fs, fill=ocean80, anchor="la")
    return im


def slide3(with_credit, log):
    im = load_photo("ZM01")
    final = im is not None
    im = im if final else pending("ZM01")
    photo_headline(im, HEAD_3, 84, "ZM01", log)
    fl, fd = font(INTER_600, 34), font(INTER_400, 28)
    label_top = H - 190
    date_top = label_top + 34 + 16

    def info(md, fill=255):
        md.text((M, label_top), LABEL, font=fl, fill=fill, anchor="lt")
        md.text((M, date_top), DATE, font=fd, fill=fill, anchor="lt")
    soft_shadow(im, info, offset=2, blur=6, alpha=0.5)
    info(ImageDraw.Draw(im), WHITE)
    # No logo on slide 3 (removed on request: it landed on the walking visitor).
    if with_credit:
        credit(im)
    return im, final


def save(im, path):
    im.convert("RGB").save(path, "PNG", icc_profile=ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes())


def side_by_side(slides, path, title):
    g, pad, top = 40, 60, 110
    sw = 700
    sh = round(sw * H / W)
    canvas = Image.new("RGB", (pad * 2 + 3 * sw + 2 * g, top + sh + pad), (232, 237, 236))
    d = ImageDraw.Draw(canvas)
    d.text((pad, 50), title, font=font(INTER_600, 34), fill=OCEAN, anchor="ls")
    for i, s in enumerate(slides):
        canvas.paste(s.resize((sw, sh), Image.LANCZOS), (pad + i * (sw + g), top))
    save(canvas, path)


def grid_check(s1, path):
    # Instagram profile grid on a phone: 3 columns, 4:5 tiles, ~2 px gutters.
    tw, gut = 360, 3
    th = round(tw * H / W)
    canvas = Image.new("RGB", (3 * tw + 2 * gut, 3 * th + 2 * gut), WHITE)
    for r in range(3):
        for c in range(3):
            tile = s1 if (r, c) == (0, 0) else Image.new("RGB", (tw, th), (226, 231, 230))
            canvas.paste(tile.resize((tw, th), Image.LANCZOS), (c * (tw + gut), r * (th + gut)))
    # Real phone size: a tile is ~124 px wide on a 390 pt screen. Show it at 1x, bottom-right.
    small = s1.resize((124, 155), Image.LANCZOS)
    canvas.paste(small, (canvas.width - 124 - 24, canvas.height - 155 - 24))
    save(canvas, path)


def main():
    OUT.mkdir(exist_ok=True)
    for f in OUT.glob("*.png"):
        f.unlink()
    log = []
    s1, ok1 = slide1(False, log)     # photo credit removed on request
    s1a = slide1_alt()
    s2 = slide2()
    s3, ok3 = slide3(False, log)
    if not (ok1 and ok3):
        raise SystemExit("Missing source photo(s) in work/src/: " + ", ".join(
            PHOTOS[k]["file"] for k, ok in (("ZM18", ok1), ("ZM01", ok3)) if not ok))
    save(s1, OUT / "LB_Carousel05_slide1.png")
    save(s1a, OUT / "LB_Carousel05_slide1-alt_textcard.png")
    save(s2, OUT / "LB_Carousel05_slide2.png")
    save(s3, OUT / "LB_Carousel05_slide3.png")
    side_by_side([s1, s2, s3], OUT / "LB_Carousel05_side-by-side_photo-hook.png",
                 "Carousel 05, version A: photo hook (ZM18)")
    side_by_side([s1a, s2, s3], OUT / "LB_Carousel05_side-by-side_textcard-hook.png",
                 "Carousel 05, version B: text-card hook")
    grid_check(s1, OUT / "LB_Carousel05_gridcheck_photo.png")
    grid_check(s1a, OUT / "LB_Carousel05_gridcheck_textcard.png")
    # Crops for the design canvas (photo only, no type).
    for k in PHOTOS:
        load_photo(k).save(WORK / f"crop_{k}.jpg", quality=90)
    for k, cfg in PHOTOS.items():
        log.append(f"{k}: source {cfg['_size']}, crop box {cfg['_crop']}, keystone {cfg['keystone']}")
    print("\n".join(log))


if __name__ == "__main__":
    main()
