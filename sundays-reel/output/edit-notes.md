# Sundays like these: edit notes

**Reel:** LookyBooky at De Haven van Zandvoort. Publishing **Sun 1 Nov 2026, 18:30 (Amsterdam)**.
**Feeling:** togetherness and a Sunday with no rush. One continuous shot of a shared table.

> **Music still needs adding in Instagram.** Upload `sundays_silent.mp4`, then add a warm soul, soft jazz or mellow instrumental track in the app. Fallback: post `sundays_natural-sound.mp4` with the table sound as is.

## Outputs
| File | Details |
|---|---|
| `sundays_natural-sound.mp4` | 5.000 s (150 frames), natural table sound, −16.2 LUFS integrated, −1.4 dBFS peak |
| `sundays_silent.mp4` | 5.000 s (150 frames), silent stereo AAC track |
| `sundays_cover.jpg` | 1080 × 1920 JPG, frame from 4.0 s |
| `contact-sheet.jpg` | Frames at 0, 2.5, 4 and 5 s (last frame, 4.967 s), with headline and safe-zone overlay |

**Specs (verified with ffprobe):**
- 1080 × 1920, 30 fps CFR, H.264 High, yuv420p, BT.709 tagged.
- Video about 13.7 Mbps.
- AAC-LC 48 kHz stereo, 192 kbps.
- MP4 with faststart (moov atom before mdat).

## Exact source trim
| Reel time | Source | Source in → out | Speed |
|---|---|---|---|
| 0.0–5.0 s (frames 0–149) | LB2026_H21.MOV | 0.000 → 5.000 s | Natural (1×) |

- **One continuous shot.** No cuts, speed changes, reversing, loop, zooms, transitions or dynamic reframing.
- **The dish-placing action is intact.** The hand enters at about 1.7 s, sets the dish down from 2.0 to 2.9 s, and is gone by about 3.1 s.
- **No first or last frame adjustment needed.** Both are clean. The last 0.085 s of the 5.085 s source is unused.

## Source footage
iPhone HEVC 3840 × 2160 with −90° rotation metadata, so it displays as 2160 × 3840 portrait (exactly 9:16).
- **Frame rate:** about 60 fps, slightly variable.
- **Duration:** 5.085 s (305 frames), as expected.
- **Colour:** 8-bit **Rec.709 SDR, not HDR** (no HLG or Dolby Vision), so no tone-mapping was needed.
- **Rotation:** applied from the display matrix, then scale-to-fill and centre-crop to 1080 × 1920 (Lanczos). Because the source is already 9:16, nothing is cropped: the full table spread, the candle and the arriving hand are all in frame. Nothing is stretched, letterboxed or padded.
- **Frame rate conversion:** to 30 fps CFR.
- **Audio:** the stereo AAC track is used; the Apple spatial-audio (4-channel) track is ignored.
- **No grading:** no LUTs, colour grading or filters. The warmth is the candle and the room.

## Typography and colour
- **Headline:** "Sundays like these." in Poppins Bold 700, **60 px** (see deviations), white #FFFFFF, centred, one line.
  - Soft Ocean #0E2F39 drop shadow: 3 px down, 8 px blur, 50% opacity. No box, banner or gradient.
  - On screen from the first frame to the last, with no animation or fade (checked on all 150 frames).
- **Position:** ink box x 243–838, y 252–316. It sits on the dark firewood and floor area above the table, outside the Instagram safe-zone margins (top 250, bottom 450, right 140).
- **Font:** `ofl/poppins/Poppins-Bold.ttf` from the official google/fonts GitHub repo.
- **Colours not used:** no turquoise, Coral or Soft Sand.
- **No logo** anywhere in the Reel or on the cover.
- **No other text:** no venue label, offer badge, app instruction or end card.

## Audio
- **Natural sound:** table sound with a 50 ms fade-in at the start and a 50 ms fade-out at the end (measured: no click at either end).
  - The source measures −25.4 LUFS. A static gain of +10.4 dB plus a limiter at −1.5 dBFS sample peak brings it to −16.2 LUFS.
  - The gain was re-measured after the limiter, because the limiter catches the glass and plate clinks.
- **Silent:** a silent stereo 48 kHz AAC track for the full 5.0 s.
- **No music** in either file.

## Cover
- **Frame:** 4.0 s. The full spread with the new dish in place, and no hand.
- **Headline:** "Sundays / like these." in Poppins Bold 700, 66 px, white, with the same soft Ocean shadow. Two lines, left-aligned at x 48, y 322–448.
- **Placement:** over the dark floor in the top-left corner. It's inside the central 4:5 area (y 285–1635) and covers no food, dish, glass or candle.

## Deviations from the brief
1. **Headline size and clearance (option B, chosen in review).**
   - **Why it's smaller:** inside the safe area, the dark space above the table is only about 50 px tall. The top plate's rim reaches y 303 around 2.9 s as the camera drifts slightly, and the arriving hand passes through the left of that space (up to x ~220).
   - **What 72–80 px would do:** a centred line at that size would cover the wrist from 2.2 to 3.0 s and touch the top plate. So the headline is **60 px**, the largest size that keeps the hand and the dishes clear.
   - **Remaining overlap:** for 2–3 frames (2.97–3.03 s), the motion-blurred fingers of the departing hand pass under the left end of the "S" as the hand pulls away. The placing action itself is never covered.
2. **Cover layout.**
   - **No template:** `assets/handpicked-spots-cover-template.png` was not supplied (it was missing from the assets folder and not in the brand guidelines). So the cover follows the brand guidelines rather than the template. **Check it against the template before publishing.**
   - **Why two lines, left-aligned:** the only food-free dark area inside the 4:5 crop is the top-left corner. So the headline is set as two left-aligned lines there, not centred.
3. **Download.** The shared folder downloads as a 13.7 GB zip, so it wasn't downloaded. The clip was fetched on its own from the direct share link you sent instead.

## QC results
- **Duration:** both MP4s are exactly 5.000 s, 150 frames. Audio stream duration is 5.000 s.
- **Natural speed:** each output frame matches the source frame at the same time, at 30 fps (mean difference 0.5/255 outside the headline).
- **Headline:** present on every frame, no typos. It never covers the food, the dishes or the candle. The hand is clear apart from the 2–3 blurred frames noted above.
- **No logo; safe zones respected.**
- **Picture:** no black frames (the darkest frame averages 115/255), no flicker (largest frame-to-frame brightness change is 1.4/255) and no rotation errors.
- **Audio:** no clicks at the start or end.

## Rebuild
```
cd sundays-reel
python3 build.py preview   # headline overlay + review sheet + cover draft in work/
python3 build.py render    # all outputs in output/
```
- **Source clip** goes in `source/`. It's kept out of git.
- **Fonts** go in `work/fonts/` as `Poppins-Bold.ttf` and `Inter-VF.ttf` (Inter is used only for contact-sheet captions). They're also kept out of git.
