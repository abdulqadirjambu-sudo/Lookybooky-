#!/usr/bin/env python3
"""Build "Sundays like these" Reel for LookyBooky.

Usage:
  python3 build.py preview      # overlay + review contact sheet + cover draft -> work/
  python3 build.py render       # 2 MP4s + cover + contact sheet -> output/
"""
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "source" / "LB2026_H21.MOV"
WORK = ROOT / "work"
OUT = ROOT / "output"

W, H, FPS = 1080, 1920, 30
SS, DUR = 0.0, 5.0   # one continuous shot, natural speed

POPPINS_BOLD = WORK / "fonts" / "Poppins-Bold.ttf"   # google/fonts ofl/poppins/Poppins-Bold.ttf
INTER_VF = WORK / "fonts" / "Inter-VF.ttf"           # contact-sheet captions only

WHITE = (255, 255, 255)
OCEAN = (0x0E, 0x2F, 0x39)
SAFE_TOP, SAFE_BOTTOM, SAFE_RIGHT = 250, 450, 140

HEADLINE = "Sundays like these."
# The dark band above the table is only ~50 px tall inside the safe area (plate rim
# reaches y 303 at 2.9 s) and the hand reaches x ~220 (x ~315 while pulling away at
# 2.97-3.03 s), so the headline size is the largest that clears both. See edit-notes.md.
HEADLINE_SIZE = 60
HEADLINE_TOP = 252   # top of the ink

COVER_T = 4.0
COVER_SIZE = 66
COVER_XY = (48, 300)  # top-left of the two-line block, over the dark floor (inside the 4:5 area)


def soft_shadow(mask, offset=(0, 3), blur=8, opacity=0.5):
    """Ocean-coloured soft drop shadow layer from an alpha mask."""
    sh = Image.new("L", mask.size, 0)
    sh.paste(mask, offset)
    sh = sh.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * opacity))
    layer = Image.new("RGBA", mask.size, OCEAN + (0,))
    layer.putalpha(sh)
    return layer


def compose(mask, img=None):
    img = img or Image.new("RGBA", (W, H), (0, 0, 0, 0))
    img.alpha_composite(soft_shadow(mask))
    txt = Image.new("RGBA", (W, H), WHITE + (0,))
    txt.putalpha(mask)
    img.alpha_composite(txt)
    return img


def headline_overlay():
    font = ImageFont.truetype(str(POPPINS_BOLD), HEADLINE_SIZE)
    asc = -font.getbbox(HEADLINE, anchor="ls")[1]
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    d.text((W // 2, HEADLINE_TOP + asc), HEADLINE, font=font, fill=255, anchor="ms")
    box = d.textbbox((W // 2, HEADLINE_TOP + asc), HEADLINE, font=font, anchor="ms")
    ok = box[1] >= SAFE_TOP and box[3] <= H - SAFE_BOTTOM and box[2] <= W - SAFE_RIGHT and box[0] >= 0
    print(f"  headline box {box} safe={'OK' if ok else 'VIOLATION'}")
    if not ok:
        raise SystemExit("safe-zone violation")
    img = compose(mask)
    WORK.mkdir(exist_ok=True)
    img.save(WORK / "headline.png")
    return box


def run(cmd):
    print("+", " ".join(str(c) for c in cmd))
    subprocess.run([str(c) for c in cmd], check=True)


def grab(t, path):
    """Frame at output time t (same fps/trim path as the render)."""
    run(["ffmpeg", "-v", "error", "-y", "-i", SRC,
         "-vf", f"fps={FPS},trim=start={SS + t}:duration={1 / FPS + 0.001},scale={W}:{H}:flags=lanczos",
         "-frames:v", "1", path])


def safe_zone_layer():
    z = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(z)
    red = (255, 40, 40, 90)
    d.rectangle((0, 0, W, SAFE_TOP), fill=red)
    d.rectangle((0, H - SAFE_BOTTOM, W, H), fill=red)
    d.rectangle((W - SAFE_RIGHT, SAFE_TOP, W, H - SAFE_BOTTOM), fill=red)
    return z


def contact_sheet(times, path):
    zone = safe_zone_layer()
    ovl = Image.open(WORK / "headline.png")
    cap = ImageFont.truetype(str(INTER_VF), 30)
    cap.set_variation_by_axes([32, 600])
    tiles = []
    for t in times:
        # the last frame of a 5.0 s / 150-frame edit is at 4.967 s
        tt = min(t, DUR - 1 / FPS)
        f = WORK / f"cs_{tt:.3f}.png"
        grab(tt, f)
        fr = Image.open(f).convert("RGBA")
        fr.alpha_composite(ovl)
        fr.alpha_composite(zone)
        fr = fr.convert("RGB").resize((W // 2, H // 2), Image.LANCZOS)
        tile = Image.new("RGB", (W // 2, H // 2 + 60), (20, 20, 20))
        tile.paste(fr, (0, 60))
        label = f"{t:.1f} s" + (" (last frame, 4.967 s)" if tt != t else "")
        ImageDraw.Draw(tile).text((12, 14), label, font=cap, fill=WHITE)
        tiles.append(tile)
    pad = 16
    sheet = Image.new("RGB", (len(tiles) * (W // 2 + pad) + pad, H // 2 + 60 + 2 * pad), (40, 40, 40))
    for i, t in enumerate(tiles):
        sheet.paste(t, (pad + i * (W // 2 + pad), pad))
    sheet.save(path, quality=90)
    print("wrote", path)


LIMITER = "alimiter=limit=0.84:level=false:attack=1:release=50"


def measure_lufs(gain):
    r = subprocess.run(["ffmpeg", "-nostats", "-hide_banner", "-ss", str(SS), "-t", str(DUR), "-i", str(SRC),
                        "-map", "0:a:0", "-af", f"{AFADE},volume={gain:.2f}dB,{LIMITER},ebur128=framelog=quiet",
                        "-f", "null", "-"], capture_output=True, text=True, check=True)
    return float(r.stderr.split("Integrated loudness:")[1].split("I:")[1].split("LUFS")[0])


def loudness_gain(target=-16.0):
    """One static gain (keeps natural dynamics). The limiter catches the table clinks and
    lowers the result, so re-measure after the limiter and correct until within 0.2 LU."""
    gain = 0.0
    for _ in range(4):
        lufs = measure_lufs(gain)
        print(f"  gain {gain:+.1f} dB -> {lufs:.1f} LUFS")
        if abs(lufs - target) < 0.2:
            break
        gain += target - lufs
    return gain


AFADE = (f"aresample=48000,aformat=channel_layouts=stereo,"
         f"afade=t=in:d=0.05,afade=t=out:st={DUR - 0.05}:d=0.05")


def render(out, audio):
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", SS, "-t", DUR + 0.2, "-i", SRC,
           "-loop", "1", "-framerate", FPS, "-i", WORK / "headline.png"]
    frames = round(DUR * FPS)
    fc = [
        # autorotate (display matrix) is applied before this chain; source is 9:16
        # (2160x3840), so scale-to-fill + centre-crop is a plain downscale
        f"[0:v]fps={FPS},trim=end_frame={frames},setpts=PTS-STARTPTS,"
        f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},"
        f"setsar=1,format=yuv420p[v]",
        "[1:v]format=rgba,scale=out_color_matrix=bt709:out_range=tv,format=yuva420p[t]",
        "[v][t]overlay=0:0:shortest=1:format=yuv420[vout]",
    ]
    if audio == "natural":
        gain = loudness_gain()
        fc.append(f"[0:a:0]atrim=end={DUR},asetpts=PTS-STARTPTS,{AFADE},volume={gain:.2f}dB,"
                  f"{LIMITER},apad=whole_dur={DUR}[aout]")
    else:
        fc.append(f"anullsrc=r=48000:cl=stereo,atrim=end={DUR}[aout]")
    cmd += ["-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]",
            "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-pix_fmt", "yuv420p",
            "-b:v", "14M", "-maxrate", "16M", "-bufsize", "28M", "-r", FPS, "-g", FPS,
            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            "-t", DUR, "-movflags", "+faststart", "-map_metadata", "-1", out]
    run(cmd)


def cover(path):
    f = WORK / f"cover_src_{COVER_T:.2f}.png"
    grab(COVER_T, f)
    img = Image.open(f).convert("RGBA")
    font = ImageFont.truetype(str(POPPINS_BOLD), COVER_SIZE)
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    d.multiline_text(COVER_XY, "Sundays\nlike these.", font=font, fill=255, spacing=int(COVER_SIZE * 0.12))
    box = d.multiline_textbbox(COVER_XY, "Sundays\nlike these.", font=font, spacing=int(COVER_SIZE * 0.12))
    print("  cover headline box", box, "(4:5 area is y 285-1635)")
    compose(mask, img).convert("RGB").save(path, quality=93, subsampling=0)
    print("wrote", path)


if __name__ == "__main__":
    step = sys.argv[1] if len(sys.argv) > 1 else "render"
    if step == "preview":
        headline_overlay()
        contact_sheet([0.0, 2.5, 4.0, 5.0], WORK / "preview-contact-sheet.jpg")
        cover(WORK / "preview-cover.jpg")
    elif step == "render":
        OUT.mkdir(exist_ok=True)
        headline_overlay()
        render(OUT / "sundays_natural-sound.mp4", "natural")
        render(OUT / "sundays_silent.mp4", "silent")
        cover(OUT / "sundays_cover.jpg")
        contact_sheet([0.0, 2.5, 4.0, 5.0], OUT / "contact-sheet.jpg")
