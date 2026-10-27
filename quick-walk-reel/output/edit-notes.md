# Just a quick walk: edit notes

**Reel:** LookyBooky, Zandvoort. Publishing **Wed 28 Oct 2026, 18:30 (Amsterdam)**.
**Joke:** a POV. You said "just a quick walk" and ended up on a bench by the sea. The "hour" is a playful scenario, not a claim about the filmed visit.

> **Music still needs adding in Instagram.** Upload `quick-walk_silent.mp4`, add the trending track in the app, and put its accent on the cut at **3.0 s** (the punchline). Fallback: post `quick-walk_natural-sound.mp4` as is.

## Outputs
| File | Details |
|---|---|
| `quick-walk_natural-sound.mp4` | 9.000 s (270 frames), natural clip sound, −16.6 LUFS integrated, −1.3 dBFS peak |
| `quick-walk_silent.mp4` | 9.000 s (270 frames), silent stereo AAC track |
| `quick-walk_cover.jpg` | 1080 × 1920 JPG |
| `contact-sheet.jpg` | One frame per shot with its text, plus a safe-zone overlay (red) |

**Specs (verified with ffprobe):**
- 1080 × 1920, 30 fps CFR, H.264 High, yuv420p, BT.709 tagged.
- Video about 13.8 Mbps.
- AAC-LC 48 kHz stereo, 192 kbps.
- MP4 with faststart (moov atom before mdat).

## Exact source trims (hard cuts only)
| Reel time | Source | Source in → out | On-screen text |
|---|---|---|---|
| 0.0–3.0 s (frames 0–89) | LB2026_ZV21.MOV | 0.000 → 3.000 s | "POV: you said / ‘just a quick walk’." |
| 3.0–6.0 s (frames 90–179) | LB2026_ZV09.MOV | 0.000 → 3.000 s | "That was / an hour ago." |
| 6.0–9.0 s (frames 180–269) | LB2026_ZV10.MOV | 0.000 → 3.000 s | "Zandvoort" |

- **No trim nudges needed.** A sharpness scan (Laplacian variance) of every 30 fps frame finds no blurry frames: every frame is at least 93% as sharp as its trim's median. Results are in `work/sharpness.json`.
- **No transitions, zooms, filters or effects.** The Reel ends on the ZV10 sea view, with no end card.

## Source footage
All three clips are iPhone HEVC 3840 × 2160 with −90° rotation metadata, so they display as 2160 × 3840 portrait.
- **Frame rate:** about 60 fps, slightly variable.
- **Durations:** ZV21 12.86 s, ZV09 4.69 s, ZV10 8.09 s.
- **Colour:** 8-bit **Rec.709 SDR, not HDR** (no HLG or Dolby Vision), so no tone-mapping was needed.
- **Rotation:** applied from the display matrix, then scale-to-fill and centre-crop to 1080 × 1920 (Lanczos). Because the source is already 9:16, nothing is actually cropped. Nothing is stretched, letterboxed or padded.
- **Frame rate conversion:** to 30 fps CFR.
- **Audio:** the stereo AAC track is used; the Apple spatial-audio (4-channel) track is ignored.
- **No grading:** no LUTs, colour grading or filters.

## Typography and colour
- **On-screen lines:** Poppins Bold 700, 76 px, white #FFFFFF, centred, line height 1.18. Soft Ocean #0E2F39 drop shadow: 4 px down, 10 px blur, 45% opacity. No boxes or banners.
- **Label:** Inter Semibold 600 (variable font set to wght 600, opsz 32), 40 px, white, centred in the lower third. Soft Ocean shadow: 2 px down, 6 px blur, 60% opacity.
- **Quotes:** typographic ‘ ’ throughout.
- **Text timing:** each line is on screen from its shot's first frame to its last. Frame-checked: frame 89 shows the opening line, frame 90 (3.0 s) the punchline, frame 179 the punchline, frame 180 (6.0 s) the label.
- **Fonts:** from the official google/fonts GitHub repo: `ofl/poppins/Poppins-Bold.ttf` and `ofl/inter/Inter[opsz,wght].ttf`.
- **Colours not used:** turquoise, Coral and Soft Sand do not appear anywhere.

### Text position (px, 1080 × 1920 frame)
| Overlay | Bounding box (x0, y0 → x1, y1) | Sits on |
|---|---|---|
| POV: you said / ‘just a quick walk’. | 180, 391 → 901, 561 | Sky. The horizon is at about y 680, and the path starts below y 850. |
| That was / an hour ago. | 294, 396 → 785, 562 | Sky. The woman's head starts at about y 840. |
| Zandvoort | 446, 1345 → 635, 1374 | Dune grass, below the beach strip |

All text is outside the Instagram safe-zone margins (top 250, bottom 450, right 140). `build.py` checks this on every build.

## Audio
- **Natural sound:**
  - 50 ms fade-in and fade-out on every shot, so each cut dips to near-silence. Measured at the cuts: sample level stays at or below 0.035 within ±10 ms of each cut, with no clicks.
  - The source ambience is quiet (−35.2 LUFS), so the cut audio is raised by one fixed gain of +19.2 dB, with a limiter at −1.5 dBFS sample peak. Result: −16.6 LUFS.
  - A fixed gain keeps the natural dynamics; loudnorm's adaptive mode pumps on 3 s shots. The gain also lifts some wind and background hiss.
- **Silent:** a silent stereo 48 kHz AAC track for the full 9.0 s.
- **No music** in either file.

## Cover
- **Frame:** ZV09 at 1.5 s. The woman is settled on the bench, facing the sea.
- **Title:** "Just a quick walk", Poppins Bold 700, 104 px, white, centred at y = 520, with a soft Ocean shadow.
- **Label:** "Zandvoort", Inter 600, 44 px, white, centred, top at y = 622.
- **4:5 crop:** the title, label and woman all sit inside the central 1080 × 1350 area (y 285–1635), so the profile-grid crop keeps them.

## Deviations from the brief
1. **No logo.** The brief asked for the white logo under "Zandvoort" in the final 3 seconds. It was removed on request, so the logo doesn't appear in the Reel or on the cover.
   - `assets/lookybooky-logo-white.png` was never supplied. The white logo was extracted from the brand guidelines v3.26 PDF and is kept in `work/brand/` for future use.
2. **Cover template.** `assets/handpicked-spots-cover-template.png` was not supplied (and it's not in the guidelines PDF). The cover follows the brand guidelines and the layout of the earlier Sweet Pearl cover instead. **Check it against the template before publishing.** If it needs changes, add the template to `assets/` and run `python3 build.py render` again.
3. **The punchline is on two lines.** On one line, centred, "That was an hour ago." is 817 px wide even at 72 px. That breaks the right-hand 140 px safe margin. It's set as "That was / an hour ago." at the same 76 px and position as the opening line, so it still replaces it in place on the cut.
4. **Ocean gradient behind the punchline.** The ZV09 line sits on bright white cloud. A soft full-width Ocean #0E2F39 band (peak 30%, under the 40% maximum) fades out above and below the text for legibility. It's only on the 3–6 s shot.
5. **Label position.** The label top is at y 1345, on the calm dune grass. It was moved down from the busy beach-pavilion strip.

## QC results
- **Duration:** both MP4s are exactly 9.000 s, 270 frames. Audio duration is also 9.000 s.
- **Text:** correct shot and timing, checked frame by frame at each cut. No typos.
- **Safe placement:** no text covers the woman, the bench or the path.
- **Black frames:** blackdetect found none.
- **Flicker:** none. The only large brightness changes are at the two cuts (frames 90 and 180).
- **Rotation:** no errors.
- **Audio:** no clicks at the cuts. Loudness is −16.6 LUFS.

## Rebuild
```
cd quick-walk-reel
python3 build.py check     # sharpness scan of each trim
python3 build.py preview   # overlays + review sheet + cover draft in work/
python3 build.py render    # all outputs in output/
```
- **Source clips** go in `source/`. They're kept out of git; download links are in the session.
- **Fonts** go in `work/fonts/` as `Poppins-Bold.ttf` and `Inter-VF.ttf` (Inter[opsz,wght].ttf renamed). They're also kept out of git.
