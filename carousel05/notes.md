# Carousel 05: notes

**Story:** "To Haarlem. On foot. Carrying fish." → the fact → where to see it (Zandvoortse Vrouwen, Zandvoorts Museum, until 4 April 2027).
**Template:** the LookyBooky photo-post template (Beachcomber, Wave Chaser, Terrace Regular, Foodie). It has a Poppins Bold headline at a 90 px left margin, the cap line at about y 140 and tight leading (1.0). The template's spaced-caps eyebrow is left out because the brief gives no eyebrow copy.

## Files (`output/`)
| File | What |
|---|---|
| `LB_Carousel05_slide1.png` | hook, photo ZM18 |
| `LB_Carousel05_slide1-alt_textcard.png` | alternative hook: Mist text on Ocean, no photo |
| `LB_Carousel05_slide2.png` | the fact, Ocean on Mist |
| `LB_Carousel05_slide2-alt_artwork.png` | the fact with an archive watercolour of a Zandvoort fish seller above it |
| `LB_Carousel05_slide3.png` | where to see it, photo ZM01 |
| `LB_Carousel05_side-by-side_photo-hook.png` / `_textcard-hook.png` / `_photo-hook_artwork.png` | the full set with each slide-1 version, and with the artwork version of slide 2 |
| `LB_Carousel05_gridcheck_photo.png` / `_textcard.png` | slide 1 in a 3-column profile grid, plus a tile at real phone size (about 124 px wide) |

All files are 1080 × 1350 sRGB PNGs, except the previews.

**Changes from the brief (on request):** no photo credit on any slide, and no logo on slide 3. The logo's bottom-right spot fell on the visitor's white skirt.

## Shared layout (identical on every slide)
- Margins: 90 px. Headline in Poppins Bold, text left edge at x 90, line box top at y 118 (cap line about y 141), leading 1.0. Slide 1 and 1-alt use 92 px; slide 3 uses 84 px.
- Line breaks are at the full stops: "To Haarlem. / On foot. / Carrying fish." and "Meet the women / behind the story."
- Slide 2: a 48 × 4 Turquoise rule, then a 48 px gap, then Poppins SemiBold 58 / 1.25, then a 40 px gap, then Inter 36 / 1.4 in Ocean at 80%. The block is centred vertically, and the fact wraps over 4 lines.
- Slide 3: label in Inter SemiBold 34, top at y 1160 (190 px from the bottom). The date line is Inter 28, 16 px below it.

## Crops
Both sources are 4672 × 7008 (2:3). The 4:5 crop uses the full width at 4672 × 5840, with no zoom.
- **ZM18 (slide 1):** top-aligned (y 0–5840). The visitor's head, face and hair are fully in frame. Her body is cut at the waist by the bottom edge, as in the original photo, and nothing cuts through her face. Every 4:5 window puts the history panel in the upper third. The top crop lets the headline panel cover the panel's own title and the top of the image strip, so the headline doesn't read as a caption for any particular image or line of text.
- **ZM01 (slide 3):** top-aligned, to keep the most sky above the flags. The entrance, both flags and the ZM window sign stay clear. The building's verticals and the flagpoles are already straight, so there's no perspective correction (keystone 0). The visitor is cut at the skirt by the bottom edge; she's seen from behind.
- The only processing is EXIF rotation, conversion from the embedded ICC profile to sRGB and a Lanczos resize. There are no filters, grading or retouching.

## Legibility compromises
- **Headlines are white, as in the house template (requested).** White against the lightest 10% of the photo behind the headline measures only 1.85:1 on ZM18 (white museum walls) and 1.57:1 on ZM01 (pale sky). To keep it readable without a box, overlay or gradient, the headline has a soft, wide Ocean text shadow (2 px down, 14 px blur, 55%). If it still reads too faint, the fallback is `HEAD_MODE = "panel"` in `build.py`: Ocean on a small Mist panel.
- **Slide 1:** in every 4:5 crop of ZM18, the history panel fills the upper third, so the white headline crosses the panel's title ("HET ZANDVOORTS MUSEUM"). It isn't aligned to or pointing at any image or line of text, but it does sit on the panel.
- **Slide 3:** the headline overlaps the top of the left flag. "…Museum" in the label runs over the visitor's bag and skirt; its soft shadow keeps it readable.
- **Grid check:** the photo hook is noticeably weaker as a thumbnail than the text card.

## Slide 2 artwork (alternative)
- Wybrand Hendriks (1744–1831), watercolour of a fish seller from Zandvoort with a basket, c. 1797–1802. Noord-Hollands Archief, Beeldcollectie Haarlem, inv. NL-HlmNHA 1100 KNA006003500. Licence: **CC0 1.0** (public domain dedication), via Wikimedia Commons: <https://commons.wikimedia.org/wiki/File:Visvrouw_Malle_Kee,_Inventarisnummer_NL-HlmNHA_1100_KNA006003500.JPG>. No credit is legally required. A courtesy line ("Wybrand Hendriks, c. 1800 · Noord-Hollands Archief") in the post caption is good practice.
- The archive title names her by her nickname, so the slide doesn't name or caption her.
- The crop is a 1080 × 760 band from head to basket, with the scan border trimmed. It uses the 960 px Commons version enlarged 1.125×, because the full-size original (1194 × 1918) was rate-limited from here. For the sharpest result, download the original from the Commons page and put it at `work/src/Hendriks_Visvrouw_NHA_KNA006003500.jpg`.
- The original brief said slide 2 should have no artwork. This version was added on request, and the text-only slide 2 is kept.
- Also checked: Rijksmuseum RP-F-2001-7-1107B-67, "Vissersvrouw in Zandvoort" (Maurice Bucquet, c. 1890, CC0). It's a page from an 1895 photography book where the fish seller is only a small vignette, so it isn't usable at slide size.

## Rebuild
Put the originals in `work/src/` (gitignored) and the fonts in `work/fonts/` (Poppins Bold and SemiBold from google/fonts `ofl/poppins`; Inter Regular and SemiBold OTF), then run `python3 build.py`.
