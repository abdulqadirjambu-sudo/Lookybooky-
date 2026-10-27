#!/usr/bin/env python3
"""Build "Just a quick walk" Reel for LookyBooky.

Usage:
  python3 build.py check        # sharpness scan of every trim (blurry-frame check)
  python3 build.py preview      # overlays + review contact sheet + cover draft -> work/
  python3 build.py render       # 2 MP4s + cover + contact sheet -> output/
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "source"
ASSETS = ROOT / "assets"
WORK = ROOT / "work"
OUT = ROOT / "output"
OVL = WORK / "overlays"

W, H, FPS = 1080, 1920, 30

POPPINS_BOLD = WORK / "fonts" / "Poppins-Bold.ttf"   # google/fonts ofl/poppins/Poppins-Bold.ttf
INTER_VF = WORK / "fonts" / "Inter-VF.ttf"           # google/fonts ofl/inter/Inter[opsz,wght].ttf
# Official asset if supplied, else the white logo extracted from brand guidelines v3.26 (p.1)
LOGO = ASSETS / "lookybooky-logo-white.png"
if not LOGO.exists():
    LOGO = WORK / "brand" / "logo-white_from-guidelines-v3-26.png"

WHITE = (255, 255, 255)
OCEAN = (0x0E, 0x2F, 0x39)

# Instagram safe zones
SAFE_TOP, SAFE_BOTTOM, SAFE_RIGHT = 250, 450, 140

LINE_SIZE = 76
LABEL_SIZE = 40
LOGO_W = 220
LABEL_TOP = 1345   # lower third, on the calm dune grass of ZV10 (below the busy beach strip)
LOGO_GAP = 30      # clear space >= height of the "o" (~13 px at 220 px wide)

# (shot id, source start, duration, overlay name or None)
SEQ = [
    ("ZV21", 0.0, 3.0, "line_1"),
    ("ZV09", 0.0, 3.0, "line_2"),
    ("ZV10", 0.0, 3.0, "label"),
]

# name: (lines, vertical centre of the block, Ocean gradient behind it). Both sit in the sky, above the horizon:
# ZV21 path starts below y~850, ZV09 woman's head starts at y~840.
LINES = {
    "line_1": (["POV: you said", "‘just a quick walk’."], 470, False),
    "line_2": (["That was", "an hour ago."], 470, True),   # sits on bright white cloud
}
LABEL_TEXT = "Zandvoort"

COVER_SHOT, COVER_T = "ZV09", 1.5
COVER_TITLE = "Just a quick walk"


def inter(size, weight=600):
    f = ImageFont.truetype(str(INTER_VF), size)
    f.set_variation_by_axes([min(max(size, 14), 32), weight])
    return f


def soft_shadow(mask, offset=(0, 4), blur=10, opacity=0.45):
    """Ocean-coloured soft drop shadow layer from an alpha mask."""
    sh = Image.new("L", mask.size, 0)
    sh.paste(mask, offset)
    sh = sh.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * opacity))
    layer = Image.new("RGBA", mask.size, OCEAN + (0,))
    layer.putalpha(sh)
    return layer


def ocean_gradient(center_y, peak=0.30, half=330):
    """Soft full-width Ocean band behind a text block (peak opacity <= 40%), fading out top and bottom."""
    y = np.arange(H, dtype=np.float32)
    a = np.clip(1 - np.abs(y - center_y) / half, 0, 1) ** 1.5 * peak * 255
    layer = Image.new("RGBA", (W, H), OCEAN + (0,))
    layer.putalpha(Image.fromarray(np.repeat(a[:, None], W, 1).astype(np.uint8)))
    return layer


def draw_lines(lines, center_y, size=LINE_SIZE, img=None, shadow=(4, 10, 0.45), gradient=False):
    font = ImageFont.truetype(str(POPPINS_BOLD), size)
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    lh = int(size * 1.18)
    top = center_y - lh * len(lines) // 2
    boxes = []
    for i, text in enumerate(lines):
        y = top + i * lh
        d.text((W // 2, y + lh // 2), text, font=font, fill=255, anchor="mm")
        boxes.append(d.textbbox((W // 2, y + lh // 2), text, font=font, anchor="mm"))
    img = img or Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if gradient:
        img.alpha_composite(ocean_gradient(center_y))
    img.alpha_composite(soft_shadow(mask, offset=(0, shadow[0]), blur=shadow[1], opacity=shadow[2]))
    txt = Image.new("RGBA", (W, H), WHITE + (0,))
    txt.putalpha(mask)
    img.alpha_composite(txt)
    return img, boxes


def draw_label(img=None, top=LABEL_TOP, with_logo=True, size=LABEL_SIZE):
    img = img or Image.new("RGBA", (W, H), (0, 0, 0, 0))
    font = inter(size)
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    d.text((W // 2, top), LABEL_TEXT, font=font, fill=255, anchor="mt")
    boxes = [d.textbbox((W // 2, top), LABEL_TEXT, font=font, anchor="mt")]
    img.alpha_composite(soft_shadow(mask, offset=(0, 2), blur=6, opacity=0.6))
    txt = Image.new("RGBA", (W, H), WHITE + (0,))
    txt.putalpha(mask)
    img.alpha_composite(txt)
    if with_logo:
        logo = Image.open(LOGO).convert("RGBA")
        lh = round(logo.height * LOGO_W / logo.width)
        logo = logo.resize((LOGO_W, lh), Image.LANCZOS)  # proportional, no recolour/effects
        lx, ly = (W - LOGO_W) // 2, boxes[0][3] + LOGO_GAP
        img.alpha_composite(logo, (lx, ly))
        boxes.append((lx, ly, lx + LOGO_W, ly + lh))
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
    for name, (lines, cy, grad) in LINES.items():
        img, boxes = draw_lines(lines, cy, gradient=grad)
        check_safe(name, boxes)
        img.save(OVL / f"{name}.png")
        meta[name] = boxes
    img, boxes = draw_label(with_logo=True)
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


def sharpness_scan():
    """Laplacian variance of every 30 fps frame in each trim (+0.5 s nudge room)."""
    report = {}
    for shot, ss, dur, _ in SEQ:
        n = round((dur + 0.5) * FPS)
        r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(SRC / f"LB2026_{shot}.MOV"),
                            "-vf", f"fps={FPS},trim=start={ss},scale=270:480,format=gray",
                            "-frames:v", str(n), "-f", "rawvideo", "-"], capture_output=True, check=True)
        fr = np.frombuffer(r.stdout, np.uint8).reshape(-1, 480, 270).astype(np.float32)
        lap = (fr[:, 1:-1, 1:-1] * 4 - fr[:, :-2, 1:-1] - fr[:, 2:, 1:-1] - fr[:, 1:-1, :-2] - fr[:, 1:-1, 2:])
        v = lap.reshape(len(fr), -1).var(1)
        med = float(np.median(v[: round(dur * FPS)]))
        low = [(round(ss + i / FPS, 3), round(float(x) / med, 2)) for i, x in enumerate(v) if x < 0.7 * med]
        print(f"{shot}: median {med:.0f}, min/median {v[: round(dur * FPS)].min() / med:.2f}, "
              f"frames <70% of median: {low or 'none'}")
        report[shot] = {"median": med, "min_ratio": float(v[: round(dur * FPS)].min() / med), "low": low}
    (WORK / "sharpness.json").write_text(json.dumps(report, indent=1))


def safe_zone_layer():
    z = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(z)
    red = (255, 40, 40, 90)
    d.rectangle((0, 0, W, SAFE_TOP), fill=red)
    d.rectangle((0, H - SAFE_BOTTOM, W, H), fill=red)
    d.rectangle((W - SAFE_RIGHT, SAFE_TOP, W, H - SAFE_BOTTOM), fill=red)
    return z


def contact_sheet(specs, path):
    """specs: list of (title, shot, source_t, overlay or None)."""
    tiles = []
    zone = safe_zone_layer()
    cap_font = inter(30)
    for title, shot, t, ovl in specs:
        f = WORK / f"cs_{shot}_{t:.2f}.png"
        grab(shot, t, f)
        fr = Image.open(f).convert("RGBA")
        if ovl:
            fr.alpha_composite(Image.open(OVL / f"{ovl}.png"))
        fr.alpha_composite(zone)
        fr = fr.convert("RGB").resize((W // 2, H // 2), Image.LANCZOS)
        tile = Image.new("RGB", (W // 2, H // 2 + 60), (20, 20, 20))
        tile.paste(fr, (0, 60))
        ImageDraw.Draw(tile).text((12, 14), title, font=cap_font, fill=(255, 255, 255))
        tiles.append(tile)
    pad, cols = 16, min(len(tiles), 3)
    rows = (len(tiles) + cols - 1) // cols
    tw, th = W // 2, H // 2 + 60
    sheet = Image.new("RGB", (cols * (tw + pad) + pad, rows * (th + pad) + pad), (40, 40, 40))
    for i, t in enumerate(tiles):
        sheet.paste(t, (pad + (i % cols) * (tw + pad), pad + (i // cols) * (th + pad)))
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
    A single static gain keeps the natural dynamics (loudnorm's dynamic mode pumps on 3 s shots)."""
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
        fc.append(f"[{idx}:v]format=rgba,scale=out_color_matrix=bt709:out_range=tv,format=yuva420p[{ovl}]")
    vlabels = []
    for i, (shot, ss, dur, ovl) in enumerate(seq):
        frames = round(dur * FPS)
        # autorotate (display matrix) is applied by ffmpeg before this chain; source is 9:16
        # (2160x3840), so scale-to-fill + centre-crop reduces to a plain downscale
        fc.append(f"[{i}:v]fps={FPS},trim=end_frame={frames},setpts=PTS-STARTPTS,"
                  f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,"
                  f"crop={W}:{H},setsar=1,format=yuv420p[v{i}]")
        if ovl:
            fc.append(f"[v{i}][{ovl}]overlay=0:0:shortest=1:format=yuv420[vo{i}]")
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


def cover(path):
    f = WORK / f"cover_src_{COVER_SHOT}_{COVER_T:.2f}.png"
    grab(COVER_SHOT, COVER_T, f)
    img = Image.open(f).convert("RGBA")
    # central 4:5 area is y 285..1635; title + label sit in the sky, above the woman (y~840)
    img, tb = draw_lines([COVER_TITLE], 520, size=104, img=img, shadow=(5, 12, 0.5))
    img, lb = draw_label(img, top=622, with_logo=False, size=44)
    print("  cover boxes", tb, lb)
    img.convert("RGB").save(path, quality=93, subsampling=0)
    print("wrote", path)


SHEET = [
    ("1  0–3 s  ZV21 src 0.0–3.0", "ZV21", 1.5, "line_1"),
    ("2  3–6 s  ZV09 src 0.0–3.0", "ZV09", 1.5, "line_2"),
    ("3  6–9 s  ZV10 src 0.0–3.0", "ZV10", 1.5, "label"),
    ("first frame 0.0 s", "ZV21", 0.0, "line_1"),
    ("cut frame 3.0 s (ZV09 src 0.0)", "ZV09", 0.0, "line_2"),
    ("cut frame 6.0 s (ZV10 src 0.0)", "ZV10", 0.0, "label"),
]

if __name__ == "__main__":
    step = sys.argv[1] if len(sys.argv) > 1 else "render"
    if step == "check":
        sharpness_scan()
    elif step == "preview":
        build_overlays()
        contact_sheet(SHEET, WORK / "preview-contact-sheet.jpg")
        cover(WORK / "preview-cover.jpg")
    elif step == "render":
        OUT.mkdir(exist_ok=True)
        build_overlays()
        render(SEQ, OUT / "quick-walk_natural-sound.mp4", "natural")
        render(SEQ, OUT / "quick-walk_silent.mp4", "silent")
        cover(OUT / "quick-walk_cover.jpg")
        contact_sheet(SHEET[:3], OUT / "contact-sheet.jpg")
