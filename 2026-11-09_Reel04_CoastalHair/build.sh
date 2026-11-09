#!/usr/bin/env bash
# LookyBooky Reel #04 "Coastal hair" (De Haven van Zandvoort) — exact build commands.
# Run from anywhere: bash build.sh   (needs ffmpeg with libfreetype + libx264, python3 for loudnorm parsing)
# Sources (copies, never the originals) live in _work/src/.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
W=_work; SRC=$W/src; T=$W/text; Q=$W/qc
mkdir -p "$T" "$Q"

POPPINS="$HERE/$W/fonts/Poppins-Bold.ttf"      # static Poppins Bold 700 (google/fonts ofl/poppins)
INTER="$HERE/$W/fonts/Inter-SemiBold.otf"      # static Inter SemiBold 600
LOGO="$HERE/$W/logo_white.png"                 # white LookyBooky logo, 2397x632 RGBA (from previous export)

H02=$SRC/LB2026_H02.MOV; H08=$SRC/LB2026_H08.MOV; H20=$SRC/LB2026_H20.MOV

# ---------- copy (UTF-8 text files, no trailing newline) ----------
printf 'POV: the coast\ndid your hair.' > "$T/h1.txt"
printf 'Time to head inside.'            > "$T/h2.txt"
printf 'De Haven van Zandvoort'          > "$T/label.txt"

# ---------- layout (px, 1080x1920 canvas) ----------
# Safe zone x 90-960, y 250-1500. ffmpeg 6.1 drawtext (y_align=text) puts y at the top of the visible glyphs.
# Measured rendered boxes: H1 x 93-860, y 520-754 | H2 x 92-950, y 520-589 | label x 93-614, y 1360-1392 | logo 430-650, y 1422-1480.
H1_SIZE=104; H1_Y=520; H1_LS=-27          # 2 lines, ~120 px line pitch; widest line 773 px -> x 90-863
H2_SIZE=84;  H2_Y=520                     # 96 px would be 988 px wide (x 90-1078) -> outside safe zone; 84 px = 864 px wide
LB_SIZE=44;  LB_Y=1360                    # cap top 1360, baseline 1392; text 525 px wide -> x 90-615
LINE_Y=1338                               # 48x4 turquoise rule, 18 px above label cap top
LOGO_W=220; LOGO_X=430; LOGO_Y=1422       # 220x58, centred, bottom edge 1480; 30 px gap above to label baseline

SHADOW="fontcolor=white:shadowcolor=0x0E2F39@0.35:shadowx=0:shadowy=3"

# alpha(start,end,fade_in,fade_out) expression for drawtext
alpha () { local a=$1 b=$2 fi=$3 fo=$4
  if [ "$fo" = "0" ]; then
    echo "if(lt(t,$a),0,if(lt(t,$a+$fi),(t-$a)/$fi,1))"
  else
    echo "if(lt(t,$a),0,if(lt(t,$a+$fi),(t-$a)/$fi,if(lt(t,$b-$fo),1,if(lt(t,$b),($b-t)/$fo,0))))"
  fi; }

# vseg <input-idx> <in> <out> <frames> <label> : trim source, 30 fps CFR, 2160x3840 -> 1080x1920 (exact 9:16, crop 0,0)
vseg () { echo "[$1:v]trim=start=$2:end=$3,setpts=PTS-STARTPTS,fps=30,scale=1080:1920:flags=lanczos,setsar=1,format=yuv420p,trim=end_frame=$4,setpts=PTS-STARTPTS[$5]"; }

# overlays <dur> (input 3 = looped logo PNG) <h1a> <h1b> <h2a> <h2b> <lba> <logoa> : text + rule + logo on [vc] -> [vout]
overlays () { local D=$1 H1A=$2 H1B=$3 H2A=$4 H2B=$5 LBA=$6 LGA=$7
cat <<EOF
[vc]drawtext=fontfile='$POPPINS':textfile='$T/h1.txt':fontsize=$H1_SIZE:line_spacing=$H1_LS:x=90:y=$H1_Y:$SHADOW:enable='between(t,$H1A,$H1B)':alpha='$(alpha $H1A $H1B 0.2 0.15)',
drawtext=fontfile='$POPPINS':textfile='$T/h2.txt':fontsize=$H2_SIZE:x=90:y=$H2_Y:$SHADOW:enable='between(t,$H2A,$H2B)':alpha='$(alpha $H2A $H2B 0.2 0.15)',
drawtext=fontfile='$INTER':textfile='$T/label.txt':fontsize=$LB_SIZE:x=90:y=$LB_Y:$SHADOW:enable='gte(t,$LBA)':alpha='$(alpha $LBA $D 0.25 0)'[vt];
color=c=0x18BFCB:s=48x4:r=30:d=$D,format=rgba,fade=t=in:st=$LBA:d=0.25:alpha=1[rule];
[vt][rule]overlay=x=90:y=$LINE_Y:enable='gte(t,$LBA)'[vr];
[3:v]fps=30,trim=duration=$D,scale=$LOGO_W:-1:flags=lanczos,format=rgba,fade=t=in:st=$LGA:d=0.25:alpha=1[lg];
[vr][lg]overlay=x=$LOGO_X:y=$LOGO_Y:enable='gte(t,$LGA)',format=yuv420p,trim=duration=$D[vout]
EOF
}

ENC_V=(-c:v libx264 -profile:v high -pix_fmt yuv420p -preset veryfast -crf 18 -r 30
       -color_primaries bt709 -color_trc bt709 -colorspace bt709 -color_range tv)
ENC_A=(-c:a aac -ar 48000 -b:a 192k -ac 2)
MUX=(-movflags +faststart -map_metadata -1 -metadata:s:v:0 rotate=0)

# ======================= MAIN 3-3-3 (9.00 s) =======================
# H02 0.50-3.50 | H08 0.50-3.50 | H20 0.50-3.50 ; hard cuts at 3.00 / 6.00
VIDEO_MAIN="$(vseg 0 0.5 3.5 90 v0);
$(vseg 1 0.5 3.5 90 v1);
$(vseg 2 0.5 3.5 90 v2);
[v0][v1][v2]concat=n=3:v=1:a=0[vc];
$(overlays 9 0.15 2.85 3.15 5.85 6.20 8.00)"

# Natural audio: 0.05 s handles each side of a cut so 0.1 s crossfades are centred on 3.00 / 6.00.
# H02: 2x high-pass 120 Hz (24 dB/oct) + fast compressor on gusts + -10 dB; H08/H20: high-pass 120 Hz.
AUDIO_PRE="[0:a:0]atrim=0.50:3.55,asetpts=PTS-STARTPTS,highpass=f=120,highpass=f=120,acompressor=threshold=-32dB:ratio=10:attack=1:release=150,volume=-4dB[a0];
[1:a:0]atrim=0.45:3.55,asetpts=PTS-STARTPTS,highpass=f=120,highpass=f=120[a1];
[2:a:0]atrim=0.45:3.50,asetpts=PTS-STARTPTS,highpass=f=120,highpass=f=120[a2];
[a0][a1]acrossfade=d=0.1:c1=tri:c2=tri[a01];[a01][a2]acrossfade=d=0.1:c1=tri:c2=tri,atrim=0:9,afade=t=in:d=0.3,afade=t=out:st=8.5:d=0.5"

# Loudness: measure integrated loudness of the pre-chain, apply that gain, then a -2 dBFS limiter
# (keeps true peak <= -1 dBTP); re-measure once and correct the gain for what the limiter took off.
lufs () { local fc=$1; shift
  ffmpeg -hide_banner -nostats "$@" -filter_complex "$fc,ebur128=peak=true[a]" -map "[a]" -f null - 2>&1 | awk '/Summary/{s=1} s&&/ I:/{print $2; exit}'; }
gainchain () { echo "volume=${1}dB,alimiter=limit=0.794:attack=1:release=60:level=0:asc=1,aresample=48000"; }
normalise () { local pre=$1 target=$2; shift 2
  local i0 g i1; i0=$(lufs "$pre" "$@"); g=$(python3 -I -c "print(round($target-($i0),2))")
  i1=$(lufs "$pre,$(gainchain $g)" "$@"); g=$(python3 -I -c "print(round($g+$target-($i1),2))")
  echo "$pre -> pre ${i0} LUFS, gain ${g} dB" >&2; gainchain "$g"; }
NAT_GAIN=$(normalise "$AUDIO_PRE" -14 -i "$H02" -i "$H08" -i "$H20" 2>>"$Q/audio_gain.log")
AUDIO_NAT="$AUDIO_PRE,$NAT_GAIN,atrim=0:9[aout]"

# Main, natural sound
ffmpeg -hide_banner -y -i "$H02" -i "$H08" -i "$H20" -loop 1 -framerate 30 -i "$LOGO" \
  -filter_complex "$VIDEO_MAIN;$AUDIO_NAT" -map "[vout]" -map "[aout]" \
  "${ENC_V[@]}" "${ENC_A[@]}" "${MUX[@]}" -t 9 LB_Reel04_CoastalHair_natural.mp4

# Main, silent stereo track
ffmpeg -hide_banner -y -i "$H02" -i "$H08" -i "$H20" -loop 1 -framerate 30 -i "$LOGO" -f lavfi -i "anullsrc=r=48000:cl=stereo" \
  -filter_complex "$VIDEO_MAIN" -map "[vout]" -map 4:a \
  "${ENC_V[@]}" "${ENC_A[@]}" "${MUX[@]}" -t 9 LB_Reel04_CoastalHair_silent.mp4

# ======================= ALT 2-2-3 (7.00 s), silent =======================
VIDEO_ALT="$(vseg 0 0.5 2.5 60 v0);
$(vseg 1 0.5 2.5 60 v1);
$(vseg 2 0.5 3.5 90 v2);
[v0][v1][v2]concat=n=3:v=1:a=0[vc];
$(overlays 7 0.15 1.85 2.15 3.85 4.20 6.00)"
ffmpeg -hide_banner -y -i "$H02" -i "$H08" -i "$H20" -loop 1 -framerate 30 -i "$LOGO" -f lavfi -i "anullsrc=r=48000:cl=stereo" \
  -filter_complex "$VIDEO_ALT" -map "[vout]" -map 4:a \
  "${ENC_V[@]}" "${ENC_A[@]}" "${MUX[@]}" -t 7 LB_Reel04_CoastalHair_ALT_2-2-3_silent.mp4

# ======================= COVER =======================
# Timeline 0.80 s = H02 source 1.30 s: hair fanned out by a gust, headline 1 at full opacity, no label/logo.
COVER_T=0.80
ffmpeg -hide_banner -y -ss $COVER_T -i LB_Reel04_CoastalHair_silent.mp4 -frames:v 1 -q:v 2 -update 1 "$Q/cover_raw.png"
python3 -I -c 'import sys;from PIL import Image;im=Image.open(sys.argv[1]).convert("RGB");im.save(sys.argv[2],quality=92,subsampling=0);im.crop((0,285,1080,1635)).save(sys.argv[3],quality=92,subsampling=0)' \
  "$Q/cover_raw.png" LB_Reel04_cover.jpg LB_Reel04_cover_grid-preview.jpg

# ======================= STORY (H02, 5.00 s, no text) =======================
# H02 source 0.30-5.30: continuous gusts, hair in motion, open sky in the upper middle for the slider sticker.
STORY_PRE="[0:a:0]atrim=0.3:5.3,asetpts=PTS-STARTPTS,highpass=f=120,highpass=f=120,acompressor=threshold=-32dB:ratio=10:attack=1:release=150,afade=t=in:d=0.3,afade=t=out:st=4.5:d=0.5"
STORY_GAIN=$(normalise "$STORY_PRE" -18 -i "$H02" 2>>"$Q/audio_gain.log")   # gentle: -18 LUFS
ffmpeg -hide_banner -y -i "$H02" -filter_complex \
  "$(vseg 0 0.3 5.3 150 vs);
   $STORY_PRE,$STORY_GAIN[as]" \
  -map "[vs]" -map "[as]" "${ENC_V[@]}" "${ENC_A[@]}" "${MUX[@]}" -t 5 LB_Story_2026-11-09_H02.mp4

# ======================= TEXT DELIVERABLES =======================
printf 'Does your hair do this too?\nSticker: emoji slider 💨\n' > story-text.txt
printf 'Coastal hair. A very good reason to head inside.\nDe Haven van Zandvoort is one of our local stops for a pause by the beach. Find it on LookyBooky. The pass is in our bio.\nSend this to the friend whose hair never survives a beach walk.\n#Zandvoort #LookyBooky\n' > caption.txt
printf "A visitor's hair blowing in the coastal wind, then walking into De Haven van Zandvoort, then a close-up of a flickering fire.\n" > alt-text.txt

# ======================= REVIEW SHEETS =======================
# Contact sheet: 19 frames, every 0.5 s (last = 8.967 s, the final frame), 7 per row.
rm -f "$Q"/cs_*.png
i=0
for t in 0 0.5 1 1.5 2 2.5 3 3.5 4 4.5 5 5.5 6 6.5 7 7.5 8 8.5 8.967; do
  ffmpeg -v error -y -ss $t -i LB_Reel04_CoastalHair_natural.mp4 -frames:v 1 -update 1 \
    -vf "scale=270:480,drawtext=fontfile='$INTER':text='$(printf '%.2f' $t) s':x=8:y=8:fontsize=22:fontcolor=yellow:box=1:boxcolor=black@0.6:boxborderw=4" \
    "$(printf "$Q/cs_%02d.png" $i)"; i=$((i+1)); done
ffmpeg -v error -y -framerate 1 -i "$Q/cs_%02d.png" -vf "tile=7x3:padding=6:margin=6:color=black" -frames:v 1 -q:v 2 LB_Reel04_contact-sheet.jpg

# Safe-zone check: 1.5 / 4.5 / 7.0 / 8.5 s, safe zone (x 90-960, y 250-1500) in thin red.
rm -f "$Q"/sz_*.png
i=0
for t in 1.5 4.5 7.0 8.5; do
  ffmpeg -v error -y -ss $t -i LB_Reel04_CoastalHair_natural.mp4 -frames:v 1 -update 1 \
    -vf "drawbox=x=90:y=250:w=870:h=1250:color=red:t=2,drawtext=fontfile='$INTER':text='$t s':x=20:y=1840:fontsize=48:fontcolor=yellow:box=1:boxcolor=black@0.6" \
    "$(printf "$Q/sz_%d.png" $i)"; i=$((i+1)); done
ffmpeg -v error -y -i "$Q/sz_0.png" -i "$Q/sz_1.png" -i "$Q/sz_2.png" -i "$Q/sz_3.png" \
  -filter_complex "hstack=4,scale=2160:-1" -q:v 2 LB_Reel04_safezone-check.jpg

echo "done"
