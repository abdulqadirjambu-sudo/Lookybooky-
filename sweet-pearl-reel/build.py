#!/usr/bin/env python3
"""Build "The sweet detour" Reel for LookyBooky.

Usage:
  python3 build.py overlays     # text/logo overlay PNGs -> work/overlays/
  python3 build.py preview      # review contact sheet  -> work/preview-contact-sheet.jpg
  python3 build.py render       # 4 MP4s + cover + contact sheet -> output/
"""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "source"
WORK = ROOT / "work"
OUT = ROOT / "output"
OVL = WORK / "overlays"

W, H, FPS = 1080, 1920, 30

POPPINS_BOLD = WORK / "fonts" / "Poppins-Bold.ttf"          # Poppins Bold 700
INTER_600 = WORK / "fonts" / "Inter-SemiBold-600.ttf"        # Inter variable, instanced at wght=600
LOGO = WORK / "brand" / "lookybooky-logo-white_from-guidelines-pdf.png"

WHITE = (255, 255, 255)
OCEAN = (0x0E, 0x2F, 0x39)

# Instagram safe zones
SAFE_TOP, SAFE_BOTTOM, SAFE_RIGHT = 250, 450, 140

LINE_SIZE = 76
LABEL_SIZE = 40
LOGO_W = 220

# Main-line block: centred on x, vertical centre of the text block
LINE_CENTER_Y = 650
# Label baseline area (lower third) and logo directly below
LABEL_TOP = 1290
LOGO_GAP = 30  # >= height of the "o" in the wordmark at 220 px (~16 px)

# (shot id, source file, source start, duration, overlay name or None)
MAIN = [
    ("SP02", 0.0, 2.0, "line_main_1"),
    ("SP11", 0.0, 2.0, "line_main_2"),
    ("SP08", 0.0, 3.0, None),
    ("SP12", 0.0, 3.0, "label"),
]
ALT = [
    ("SP11", 0.0, 2.0, "line_alt_1"),
    ("SP08", 0.0, 3.0, None),
    ("SP12", 0.0, 3.0, "label"),
]

# name: (lines, vertical centre of the block). Centres are set per shot to keep text
# off the Sweet Pearl awning (SP02) and above the drink/stroopwafel (SP11).
LINES = {
    "line_main_1": (["We’re just", "having a look."], 618),
    "line_main_2": (["Famous last words."], 545),
    "line_alt_1": (["Just looking.", "Apparently."], 532),
}
LABEL_TEXT = "Sweet Pearl · Zandvoort"


def soft_shadow(mask, offset=(0, 4), blur=10, opacity=0.45):
    """Ocean-coloured soft drop shadow layer from an alpha mask."""
    sh = Image.new("L", mask.size, 0)
    sh.paste(mask, offset)
    sh = sh.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * opacity))
    layer = Image.new("RGBA", mask.size, OCEAN + (0,))
    layer.putalpha(sh)
    return layer


def draw_lines(lines, center_y=LINE_CENTER_Y):
    font = ImageFont.truetype(str(POPPINS_BOLD), LINE_SIZE)
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    lh = int(LINE_SIZE * 1.18)
    top = center_y - lh * len(lines) // 2
    boxes = []
    for i, text in enumerate(lines):
        y = top + i * lh
        d.text((W // 2, y + lh // 2), text, font=font, fill=255, anchor="mm")
        boxes.append(d.textbbox((W // 2, y + lh // 2), text, font=font, anchor="mm"))
    img = soft_shadow(mask)
    txt = Image.new("RGBA", (W, H), WHITE + (0,))
    txt.putalpha(mask)
    img.alpha_composite(txt)
    return img, boxes


def draw_label(img=None, top=LABEL_TOP, with_logo=True, size=LABEL_SIZE):
    img = img or Image.new("RGBA", (W, H), (0, 0, 0, 0))
    font = ImageFont.truetype(str(INTER_600), size)
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    tb = d.textbbox((0, 0), LABEL_TEXT, font=font, anchor="lt")
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    x0 = (W - tw) // 2
    d.text((x0, top), LABEL_TEXT, font=font, fill=255, anchor="lt")
    boxes = [(x0, top, x0 + tw, top + th)]
    shadow_src = mask.copy()
    logo_box = None
    if with_logo:
        logo = Image.open(LOGO).convert("RGBA")
        lh = round(logo.height * LOGO_W / logo.width)
        logo = logo.resize((LOGO_W, lh), Image.LANCZOS)
        lx, ly = (W - LOGO_W) // 2, top + th + LOGO_GAP
        logo_box = (lx, ly, lx + LOGO_W, ly + lh)
        boxes.append(logo_box)
    img.alpha_composite(soft_shadow(shadow_src, offset=(0, 2), blur=6, opacity=0.6))
    txt = Image.new("RGBA", (W, H), WHITE + (0,))
    txt.putalpha(mask)
    img.alpha_composite(txt)
    if with_logo:
        img.alpha_composite(logo, logo_box[:2])  # logo untouched: no shadow, outline or recolour
    return img, boxes


def check_safe(name, boxes):
    for b in boxes:
        ok = b[1] >= SAFE_TOP and b[3] <= H - SAFE_BOTTOM and b[2] <= W - SAFE_RIGHT and b[0] >= 0
        print(f"  {name}: box {tuple(int(v) for v in b)} safe={'OK' if ok else 'VIOLATION'}")
        if not ok:
            raise SystemExit(f"safe-zone violation in {name}")


def build_overlays():
    OVL.mkdir(parents=True, exist_ok=True)
    meta = {}
    for name, (lines, cy) in LINES.items():
        img, boxes = draw_lines(lines, cy)
        check_safe(name, boxes)
        img.save(OVL / f"{name}.png")
        meta[name] = boxes
    img, boxes = draw_label(with_logo=False)
    check_safe("label", boxes)
    img.save(OVL / "label.png")
    meta["label"] = boxes
    (OVL / "boxes.json").write_text(json.dumps(meta, indent=1))


def run(cmd):
    print("+", " ".join(str(c) for c in cmd))
    subprocess.run([str(c) for c in cmd], check=True)


def grab(shot, t, path):
    run(["ffmpeg", "-v", "error", "-y", "-i", SRC / f"LB2026_{shot}.MOV",
         "-vf", f"fps={FPS},trim=start={t}:duration={1 / FPS + 0.001},scale={W}:{H}:flags=lanczos",
         "-frames:v", "1", path])


def safe_zone_layer():
    z = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(z)
    red = (255, 40, 40, 90)
    d.rectangle((0, 0, W, SAFE_TOP), fill=red)
    d.rectangle((0, H - SAFE_BOTTOM, W, H), fill=red)
    d.rectangle((W - SAFE_RIGHT, SAFE_TOP, W, H - SAFE_BOTTOM), fill=red)
    d.rectangle((0, 500, W - SAFE_RIGHT, 800), outline=(255, 230, 0, 200), width=3)
    return z


def contact_sheet(seq_specs, path):
    """seq_specs: list of (title, shot, source_t, overlay or None)."""
    WORK.mkdir(exist_ok=True)
    tiles = []
    zone = safe_zone_layer()
    cap_font = ImageFont.truetype(str(INTER_600), 34)
    for title, shot, t, ovl in seq_specs:
        f = WORK / f"cs_{shot}_{t:.2f}.png"
        grab(shot, t, f)
        fr = Image.open(f).convert("RGBA")
        if ovl:
            fr.alpha_composite(Image.open(OVL / f"{ovl}.png"))
        fr.alpha_composite(zone)
        fr = fr.convert("RGB").resize((W // 2, H // 2), Image.LANCZOS)
        tile = Image.new("RGB", (W // 2, H // 2 + 60), (20, 20, 20))
        tile.paste(fr, (0, 60))
        ImageDraw.Draw(tile).text((12, 12), title, font=cap_font, fill=(255, 255, 255))
        tiles.append(tile)
    pad = 16
    sheet = Image.new("RGB", (len(tiles) * (W // 2 + pad) + pad, H // 2 + 60 + 2 * pad), (40, 40, 40))
    for i, t in enumerate(tiles):
        sheet.paste(t, (pad + i * (W // 2 + pad), pad))
    sheet.save(path, quality=90)
    print("wrote", path)


def audio_chain(seq):
    """Inputs + per-shot audio chains (50 ms fade in/out at every cut) and their concat."""
    inputs, fc = [], []
    for i, (shot, ss, dur, _) in enumerate(seq):
        inputs += ["-ss", ss, "-t", dur + 0.5, "-i", SRC / f"LB2026_{shot}.MOV"]
        fc.append(f"[{i}:a:0]atrim=end={dur},asetpts=PTS-STARTPTS,aresample=48000,"
                  f"aformat=channel_layouts=stereo,"
                  f"afade=t=in:d=0.05,afade=t=out:st={dur - 0.05}:d=0.05[a{i}]")
    fc.append("".join(f"[a{i}]" for i in range(len(seq))) + f"concat=n={len(seq)}:v=0:a=1")
    return inputs, fc


def loudness_gain(seq, target=-16.0):
    """Measure integrated loudness of the cut audio; return the static gain (dB) to reach target.
    A single static gain keeps the natural dynamics (loudnorm's dynamic mode pumps on 2-3 s shots)."""
    inputs, fc = audio_chain(seq)
    fc[-1] += ",ebur128=framelog=quiet"
    r = subprocess.run(["ffmpeg", "-nostats", "-hide_banner", *map(str, inputs),
                        "-filter_complex", ";".join(fc), "-f", "null", "-"],
                       capture_output=True, text=True, check=True)
    lufs = float(r.stderr.split("Integrated loudness:")[1].split("I:")[1].split("LUFS")[0])
    print(f"  measured {lufs:.1f} LUFS -> gain {target - lufs:+.1f} dB")
    return target - lufs


def render(seq, out, audio):
    """audio: 'natural' (clip sound, -16 LUFS, 50 ms fades at each cut) or 'silent'."""
    total = sum(d for _, _, d, _ in seq)
    cmd = ["ffmpeg", "-v", "error", "-y"]
    for shot, ss, dur, _ in seq:
        cmd += ["-ss", ss, "-t", dur + 0.5, "-i", SRC / f"LB2026_{shot}.MOV"]
    ovl_inputs = {}
    for _, _, _, ovl in seq:
        if ovl and ovl not in ovl_inputs:
            ovl_inputs[ovl] = len(seq) + len(ovl_inputs)
            cmd += ["-loop", "1", "-framerate", FPS, "-i", OVL / f"{ovl}.png"]
    fc = []
    for ovl, idx in ovl_inputs.items():
        # convert overlay with the BT.709 matrix so colours match the video
        n = sum(1 for s in seq if s[3] == ovl)
        fc.append(f"[{idx}:v]format=rgba,scale=out_color_matrix=bt709:out_range=tv,format=yuva420p,"
                  f"split={n}" + "".join(f"[{ovl}{k}]" for k in range(n)))
    used = {k: 0 for k in ovl_inputs}
    vlabels = []
    for i, (shot, ss, dur, ovl) in enumerate(seq):
        frames = round(dur * FPS)
        # autorotate (display matrix) is applied by ffmpeg before this chain
        fc.append(f"[{i}:v]fps={FPS},trim=end_frame={frames},setpts=PTS-STARTPTS,"
                  f"scale={W}:{H}:flags=lanczos,setsar=1,format=yuv420p[v{i}]")
        if ovl:
            fc.append(f"[v{i}][{ovl}{used[ovl]}]overlay=0:0:shortest=1:format=yuv420[vo{i}]")
            used[ovl] += 1
            vlabels.append(f"[vo{i}]")
        else:
            vlabels.append(f"[v{i}]")
    fc.append("".join(vlabels) + f"concat=n={len(seq)}:v=1:a=0[vout]")
    if audio == "natural":
        _, afc = audio_chain(seq)  # same inputs 0..n-1 as the video
        gain = loudness_gain(seq)
        fc += afc[:-1]
        fc.append(afc[-1] + f",volume={gain:.2f}dB,alimiter=limit=0.84:level=false:attack=1:release=50,"
                  f"atrim=end={total},apad=whole_dur={total}[aout]")
    else:
        fc.append(f"anullsrc=r=48000:cl=stereo,atrim=end={total}[aout]")
    cmd += ["-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]",
            "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-pix_fmt", "yuv420p",
            "-b:v", "14M", "-maxrate", "16M", "-bufsize", "28M", "-r", FPS, "-g", FPS,
            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            "-t", total, "-movflags", "+faststart", "-map_metadata", "-1", out]
    run(cmd)


def cover(shot, t, path):
    f = WORK / f"cover_src_{shot}_{t:.2f}.png"
    grab(shot, t, f)
    img = Image.open(f).convert("RGBA")
    font = ImageFont.truetype(str(POPPINS_BOLD), 104)
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    # central 4:5 area is y 285..1635; title + label sit in its upper part, above the food
    d.text((W // 2, 470), "The sweet detour", font=font, fill=255, anchor="mm")
    img.alpha_composite(soft_shadow(mask, offset=(0, 5), blur=12, opacity=0.5))
    txt = Image.new("RGBA", (W, H), WHITE + (0,))
    txt.putalpha(mask)
    img.alpha_composite(txt)
    img, _ = draw_label(img, top=560, with_logo=False, size=44)
    img.convert("RGB").save(path, quality=93, subsampling=0)
    print("wrote", path)


if __name__ == "__main__":
    step = sys.argv[1] if len(sys.argv) > 1 else "render"
    sheet_specs = [
        ("1  SP02 @0.0-2.0s  (main 0-2s)", "SP02", 1.0, "line_main_1"),
        ("2  SP11 @0.0-2.0s  (main 2-4s)", "SP11", 1.0, "line_main_2"),
        ("3  SP08 @0.0-3.0s  (main 4-7s)", "SP08", 1.5, None),
        ("4  SP12 @0.0-3.0s  (main 7-10s)", "SP12", 1.5, "label"),
        ("ALT  SP11 opening (alt 0-2s)", "SP11", 1.0, "line_alt_1"),
    ]
    if step == "overlays":
        build_overlays()
    elif step == "preview":
        build_overlays()
        contact_sheet(sheet_specs, WORK / "preview-contact-sheet.jpg")
        cover("SP11", 1.0, WORK / "preview-cover.jpg")
    elif step == "render":
        OUT.mkdir(exist_ok=True)
        build_overlays()
        render(MAIN, OUT / "sweet-detour_main_natural-sound.mp4", "natural")
        render(MAIN, OUT / "sweet-detour_main_silent.mp4", "silent")
        render(ALT, OUT / "sweet-detour_alt-opening_natural-sound.mp4", "natural")
        render(ALT, OUT / "sweet-detour_alt-opening_silent.mp4", "silent")
        cover("SP11", 1.0, OUT / "sweet-detour_cover.jpg")
        contact_sheet(sheet_specs, OUT / "contact-sheet.jpg")
