# The sweet detour: edit notes

**Reel 5:** LookyBooky × Sweet Pearl, Zandvoort. Publishing **Wed 21 Oct 2026, 18:30**.
**Feeling:** fun and anticipation. **Joke:** "just having a look" → stroopwafel on the terrace.

> **Music still needs adding in Instagram.** Pick a playful, upbeat trending track available to the business account and time the cut to the stroopwafel (2.0 s in the main version) to a beat. Use the `_silent` file when adding music. Record the track link and time range in the music briefing. Fallback: post the `_natural-sound` file as is.

## Outputs
| File | Length | Audio |
|---|---|---|
| `sweet-detour_main_natural-sound.mp4` | 10.0 s (300 frames) | clip sound, −16.5 LUFS integrated |
| `sweet-detour_main_silent.mp4` | 10.0 s (300 frames) | silent stereo AAC track |
| `sweet-detour_alt-opening_natural-sound.mp4` | 8.0 s (240 frames) | clip sound, −16.8 LUFS integrated |
| `sweet-detour_alt-opening_silent.mp4` | 8.0 s (240 frames) | silent stereo AAC track |
| `sweet-detour_cover.jpg` | 1080 × 1920 | n/a |
| `contact-sheet.jpg` | one frame per shot + safe-zone overlay | n/a |

Only one version (main or alt opening) is published.

**Specs (verified with ffprobe):** 1080 × 1920, 30 fps CFR, H.264 High, yuv420p, BT.709 tagged, around 14 Mbps, AAC-LC 48 kHz stereo 192 kbps, MP4 with faststart (moov atom before mdat).

## Exact source trims (all hard cuts)
### Main (10.0 s)
| Reel time | Source | Source in → out | On-screen text |
|---|---|---|---|
| 0.0–2.0 s | LB2026_SP02.MOV | 0.000 → 2.000 s | "We’re just / having a look." |
| 2.0–4.0 s | LB2026_SP11.MOV | 0.000 → 2.000 s | "Famous last words." |
| 4.0–7.0 s | LB2026_SP08.MOV | 0.000 → 3.000 s | none |
| 7.0–10.0 s | LB2026_SP12.MOV | 0.000 → 3.000 s | "Sweet Pearl · Zandvoort" + white logo |

### Alternate opening (8.0 s)
| Reel time | Source | Source in → out | On-screen text |
|---|---|---|---|
| 0.0–2.0 s | LB2026_SP11.MOV | 0.000 → 2.000 s | "Just looking. / Apparently." |
| 2.0–5.0 s | LB2026_SP08.MOV | 0.000 → 3.000 s | none |
| 5.0–8.0 s | LB2026_SP12.MOV | 0.000 → 3.000 s | "Sweet Pearl · Zandvoort" + white logo |

No trim nudges were needed: sharpness measured at the first, middle and last frames of every trim stays steady, with no blurry frames.

## Source footage
All four clips are iPhone HEVC 3840 × 2160 with −90° rotation metadata (displayed as 2160 × 3840 portrait). They're ~60 fps (slightly variable), 8-bit **Rec.709 SDR, not HDR**, so no tone-mapping was needed and colour is untouched.
- Rotation applied from the display matrix, then a straight Lanczos downscale to 1080 × 1920. The source is already 9:16, so nothing is cropped, stretched or padded.
- Frame rate converted to 30 fps CFR.
- Audio uses the stereo AAC track; the Apple spatial-audio (4-ch) track is ignored.
- No grading, LUTs or filters.

## Typography and colour
- **On-screen lines:** Poppins Bold 700, 76 px, white #FFFFFF, centred, line height 1.18. Soft Ocean #0E2F39 shadow: 4 px down, 10 px blur, 45% opacity. No boxes.
- **Label:** Inter Semibold 600, 40 px, white, centred, top at y = 1290 (lower third). Soft Ocean shadow: 2 px down, 6 px blur, 60% opacity.
- **Accent:** one 10 px Turquoise #18BFCB dot beside the label (the only use of turquoise).
- Coral and Soft Sand are not used. Typographic apostrophe in "We’re".
- **Fonts** come from the official google/fonts GitHub repo: `ofl/poppins/Poppins-Bold.ttf`, and `ofl/inter/Inter[opsz,wght].ttf` fixed at wght 600.
- **Logo:** white horizontal logo, 220 × 58 px, centred at x 430–650, y 1349–1407. It's 30 px below the label, which is more than the height of the "o" (about 16 px). It appears only during the SP12 shot, with no recolour, stretch, outline or shadow.

### Text position (px, 1080 × 1920 frame)
| Overlay | Bounding box (x0, y0 → x1, y1) |
|---|---|
| We’re just / having a look. | 266, 539 → 813, 710 |
| Famous last words. | 161, 516 → 918, 573 |
| Just looking. / Apparently. | 291, 453 → 788, 623 |
| Label | 307, 1290 → 772, 1319 |
| Logo | 430, 1349 → 650, 1407 |

Everything is outside the Instagram safe-zone margins (top 250, bottom 450, right 140). The build script checks this automatically.

## Audio
- **Natural sound:** a 50 ms fade-in and fade-out on every shot, so each cut dips to near-silence (measured: no clicks). The cut audio is then raised by one fixed gain to about −16 LUFS (+18.0 dB main, +19.4 dB alt), with a limiter at −1.5 dBFS sample peak.
  - The source ambience is quiet (around −34 LUFS), so this gain also lifts background hiss.
  - loudnorm's adaptive mode was tried first, but it only reached −17.5 LUFS on these 2–3 s shots, so a fixed gain was used instead.
- **Silent:** a silent stereo 48 kHz AAC track for the full duration.

## Cover
- Frame: SP11 at 1.0 s (stroopwafel close-up).
- Title: "The sweet detour", Poppins Bold 700, 104 px, white, centred at y = 470.
- Label: "Sweet Pearl · Zandvoort", Inter 600, 44 px, with the turquoise dot, at y = 560.
- The title, label and stroopwafel all sit inside the central 1080 × 1350 (4:5) area, y 285–1635.

## Deviations from the brief
1. **Logo file.** `assets/lookybooky-logo-white.png` was not supplied. The white logo was taken directly from the brand guidelines PDF (v3.25, Aug 2026, the same artwork as page 6, "Wit logo op donker en fotografie"), unedited. Saved as `work/brand/lookybooky-logo-white_from-guidelines-pdf.png`.
2. **Cover template.** `assets/handpicked-spots-cover-template.png` was not supplied, so the cover follows the brand guidelines rather than the Handpicked spots template. **Check it against the template before publishing.** If it needs changes, add the template to `assets/` and re-run `python3 build.py render`.
3. **Text heights.**
   - The SP02 line is at y 539–710 and partly overlaps the SWEET PEARL awning lettering. A lower position would cover the person's head.
   - The alternate opening's line starts at y 453, slightly above the 500–800 band, so "Apparently." clears the drink cup.
   - All text stays well inside the safe zones.
4. **Label shadow.** The label's Ocean shadow is a little stronger (60%) to stay readable over the striped shirt in SP12. No bottom gradient was used.

## Caption to copy
> “We’re just having a look.”
>
> And that’s how a quick stop at Sweet Pearl became part of the afternoon.
>
> Another local favourite to discover with LookyBooky. Who’s joining you?
>
> #Zandvoort #SweetPearl #LookyBooky

## QC results
- Durations: main versions 10.000 s (300 frames), alt versions 8.000 s (240 frames).
- Text is on the correct shot from its first frame to its last, checked frame by frame at each cut. The stroopwafel, faces and hands are never covered.
- blackdetect found no black frames. No flicker and no rotation errors.
- No clicks at any cut. Loudness: main −16.5 LUFS, alt −16.8 LUFS.

## Rebuild
```
cd sweet-pearl-reel
python3 build.py preview   # overlays + review sheet + cover draft in work/
python3 build.py render    # all outputs in output/
```
Source clips go in `source/`. Fonts go in `work/fonts/` (the source clips and fonts are kept out of git).
