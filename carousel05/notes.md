# Carousel 05: notes

**Story:** "To Haarlem. On foot. Carrying fish." → the fact → where to see it (Zandvoortse Vrouwen, Zandvoorts Museum, until 4 April 2027).
**Template:** the LookyBooky photo-post template, which has a white Poppins Bold headline set straight on the photo, a 90 px left margin, the cap line at about y 140 and tight leading (1.0). It matches the Beachcomber, Wave Chaser, Terrace Regular and Foodie posts. The template's spaced-caps eyebrow ("THE BEACHCOMBER") is left out because the brief gives no eyebrow copy.

## Status
| File | State |
|---|---|
| `output/LB_Carousel05_slide2.png` | final |
| `output/LB_Carousel05_slide1-alt_textcard.png` | final (Mist text on Ocean) |
| `output/LB_Carousel05_gridcheck_textcard.png` | final |
| slide 1 and slide 3 (with and without credit), both side-by-sides, photo grid check | **waiting for photos**. Proofs with a grey photo slot are in `proofs/` (not committed). |

`LB2026_KimKramer_ZM18.jpg` and `LB2026_KimKramer_ZM01.jpg` were not in this repo or in Dropbox (searched recursively). Put the originals in `work/src/` and run `python3 build.py`: all the finals are written to `output/` with the requested names.

## Shared layout (identical on every slide)
- Margins: 90 px left and right.
- Headline: Poppins Bold, left-aligned at x 90, line box top at y 118 (cap line about y 141), leading 1.0. Slides 1 and 1-alt use 92 px; slide 3 uses 84 px.
- Line breaks: "To Haarlem. / On foot. / Carrying fish." and "Meet the women / behind the story." The brief's copy had the breaks run together, so they were read at the full stops.
- Slide 2: a 48 × 4 Turquoise rule, then a 48 px gap, then Poppins SemiBold 58 / 1.25 Ocean, then a 40 px gap, then Inter 36 / 1.4 in Ocean at 80% (#3E5961 flattened on Mist). The block is centred vertically; the 900 px column wraps the fact over 4 lines.
- Slide 3: label in Inter SemiBold 34, top at y 1160 (190 px from the bottom). The date line is Inter 28, 16 px below it.
- Logo (slide 3 only): white horizontal logo, 180 × 47, at x 810–990, y 1263–1310. **Compromise:** the label is 734 px wide (it ends at x 824), so a logo in the label's row would sit 14 px from it. The logo goes on the bottom row, right-aligned, instead. That leaves 78 px of vertical clear space below the label, against about 14 px needed (the height of the "o").
- Credit: "Photo: Kim Kramer", Inter 22, white at 80%, baseline 40 px from the bottom edge, left at x 90. There are versions with and without it.

## Crops
- **ZM18 (slide 1):** to set once the photo is in. The aim is a 4:5 window that keeps the visitor whole and the panel as context, with nothing cut through a face. The headline sits in the upper third over a calm area, never on the panel or pointing at it. Set `focus_x`, `focus_y` and `zoom` in `PHOTOS` in `build.py`.
- **ZM01 (slide 3):** a 4:5 window on the entrance. `keystone` corrects vertical perspective only and stays 0 unless the building is clearly tilted.
- The only processing is EXIF rotation, conversion from the embedded ICC profile to sRGB and a Lanczos resize. There are no filters, grading or retouching.

## Legibility
- On photos the headline is plain white with no overlay, gradient or shadow, as in the template. `build.py` measures the lightest 10% of the photo behind the headline. If white falls below 3:1 (WCAG large text), it switches automatically to Ocean on a small Mist panel, as the brief allows, and logs the contrast it measured.
- The small white label, date line and credit carry a very soft Ocean text shadow (2 px down, 6 px blur, 50%), the same treatment as in Reel 5. It's a text effect, not a box or an overlay. Remove it if the photo allows.
- Grid check: at real phone size (a tile about 124 px wide), the three-line hook still reads at roughly 11 px cap height.

## Fonts and logo
- Poppins Bold and SemiBold come from google/fonts (`ofl/poppins`). Inter Regular and SemiBold are Inter 4 OTFs. Put them in `work/fonts/`.
- The logo is `work/brand/lookybooky-logo-white_from-guidelines-pdf.png`, the same file Reel 5 uses.
