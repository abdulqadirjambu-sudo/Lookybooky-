"""Builds output/LookyBooky_December_Plan.html and renders it to PDF with Playwright."""
import csv, html, datetime as dt, subprocess, sys
E = html.escape
rows = list(csv.DictReader(open("output/Next_30_Days_Calendar.csv", encoding="utf-8")))
def kind(f):
    f = f.lower()
    for k in ("reel", "carousel", "stories", "community", "rest"):
        if f.startswith(k): return k
    return "other"
LBL = {"reel": "Reel", "carousel": "Carousel", "stories": "Stories", "community": "Community", "rest": "Rest"}
def d(r): return dt.date.fromisoformat(r["date"])
def ds(r): x = d(r); return f'{x.strftime("%a")} {x.day} Dec'
def pil(p): return "" if p.strip() in ("", "—") else p.split(" ", 1)[1].replace(" (signature)", "").replace(" (conversion)", "")
def nl(t): return E(t).replace("\n", "<br>")
def test(t): return t.split(" ")[0] if t.startswith("T") else ("–" if not t else "Excluded")

# glance table
glance = "".join(f'<tr class="{kind(r["format"])}"><td class="nw">{ds(r)}</td><td class="nw">{E(r["time_CET"]) if r["time_CET"]!="—" else ""}</td><td><span class="chip {kind(r["format"])}">{LBL.get(kind(r["format"]),"")}</span></td><td><b>{E(r["working_title"])}</b></td><td lang="nl">{E(pil(r["pillar"]))}</td><td class="nw">{test(r["test_id"])}</td></tr>' for r in rows)

# feed briefs
def kv(label, val, cls=""):
    if not val or val.strip() in ("", "—"): return ""
    return f'<div class="kv {cls}"><dt>{label}</dt><dd>{nl(val)}</dd></div>'
briefs = []
for r in rows:
    k = kind(r["format"])
    if k not in ("reel", "carousel"): continue
    give = "giveaway" in r["format"].lower()
    briefs.append(f'''<div class="brief{' give' if give else ''}">
<div class="bh"><span class="bd">{ds(r)} · {E(r["time_CET"])}</span><span class="chip {k}">{E(r["format"])}</span>{'<span class="badge">Giveaway</span>' if give else ''}</div>
<h3>{E(r["working_title"])}</h3>
<div class="sub">{E(pil(r["pillar"]))} · {E(r["funnel_stage"])} · Test: {E(r["test_id"] or "–")}</div>
<dl>{kv("Hook on screen", r["hook_onscreen_NL"])}{kv("Visual", r["visual_direction"])}{kv("Media", r["media"], "media")}{kv("Caption (NL)", r["caption_NL"], "cap")}{kv("English line", r["caption_EN_line"])}{kv("CTA", r["CTA"])}{kv("Hashtags", r["hashtags"])}{kv("Partner", r["collab_or_partner"])}{kv("Stories", r["story_support"])}{kv("Watch", r["primary_KPI"])}{kv("Check first", r["checks_before_posting"], "check")}</dl></div>''')
BRIEFS = "\n".join(briefs)

stories = "".join(f'<tr><td class="nw">{ds(r)}</td><td class="nw">{E(r["time_CET"]) if r["time_CET"]!="—" else "–"}</td><td><b>{E(r["working_title"])}</b><br><span class="muted">{E(r["visual_direction"])}</span>{("<br><span class=\"mt\">Media: " + E(r["media"]) + "</span>") if r["media"] else ""}</td><td>{E(r["CTA"])}</td><td class="muted">{E(r["checks_before_posting"])}</td></tr>' for r in rows if kind(r["format"]) in ("stories", "community", "rest"))

HTML = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>LookyBooky Zandvoort · December 2026 Instagram plan</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700&family=Inter:ital,wght@0,400;0,600;1,400&display=swap">
<style>
@page {{ size: A4; margin: 16mm 15mm 18mm; }}
:root {{ --t:#18bfcb; --o:#0e2f39; --c:#ff6f61; --sand:#fff2cc; --mist:#f3f7f6; --mut:rgba(14,47,57,.72); --b:rgba(14,47,57,.16); }}
* {{ box-sizing:border-box; }}
body {{ margin:0; font:400 10pt/1.5 Inter, Arial, sans-serif; color:var(--o); -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
h1,h2,h3 {{ font-family:Poppins, Arial, sans-serif; margin:0; }}
h2 {{ font-size:18pt; font-weight:600; margin:0 0 4mm; break-after:avoid; }}
h3 {{ font-size:11.5pt; font-weight:600; }}
p {{ margin:0 0 2.5mm; }}
.eyebrow {{ font:600 8pt/1 Inter, sans-serif; letter-spacing:.08em; text-transform:uppercase; color:var(--mut); margin-bottom:2.5mm; }}
.muted {{ color:var(--mut); }}
.sec {{ margin-top:9mm; break-inside:avoid; }}
.grid2, .box, .sand, .pills, .rhythm {{ break-inside:avoid; }}
.eyebrow {{ break-after:avoid; }}
.pb {{ break-before:page; }}
/* cover */
.cover {{ background:var(--o); color:#fff; padding:11mm 11mm 10mm; margin-bottom:7mm; }}
.cover .eyebrow {{ color:rgba(255,255,255,.75); }}
.cover h1 {{ font-size:30pt; line-height:1.05; font-weight:700; letter-spacing:-.01em; }}
.cover h1 em {{ font-style:normal; color:var(--t); }}
.cover p {{ color:rgba(255,255,255,.85); font-size:10.5pt; margin-top:5mm; max-width:150mm; }}
.stats {{ display:grid; grid-template-columns:repeat(4,1fr); gap:0; margin-top:8mm; border-top:1px solid rgba(255,255,255,.2); }}
.stats div {{ padding:4mm 3mm 0 0; }}
.stats b {{ display:block; font:600 17pt/1.1 Poppins, sans-serif; color:var(--t); }}
.stats span {{ font-size:8.5pt; color:rgba(255,255,255,.85); }}
.box {{ background:var(--mist); padding:5mm 6mm; }}
.sand {{ background:var(--sand); padding:5mm 6mm; }}
ol.tight, ul.tight {{ margin:0; padding-left:5mm; }} .tight li {{ margin:1.2mm 0; }}
table {{ width:100%; border-collapse:collapse; font-size:8.8pt; }}
th {{ text-align:left; font:600 7.5pt/1.2 Inter, sans-serif; letter-spacing:.06em; text-transform:uppercase; color:var(--mut); background:var(--mist); padding:2mm 2.2mm; }}
td {{ padding:1.8mm 2.2mm; border-bottom:1px solid var(--b); vertical-align:top; }}
tr {{ break-inside:avoid; }}
.nw {{ white-space:nowrap; }}
tr.community td, tr.rest td {{ color:var(--mut); }}
.chip {{ display:inline-block; font:600 7.5pt/1 Inter, sans-serif; padding:1.2mm 2.4mm; border-radius:99px; border:1px solid var(--o); white-space:nowrap; }}
.chip.reel {{ background:var(--t); border-color:var(--t); }}
.chip.carousel {{ background:var(--o); color:#fff; }}
.chip.community, .chip.rest {{ border-color:var(--b); color:var(--mut); }}
.badge {{ display:inline-block; margin-left:2mm; font:600 7pt/1 Inter, sans-serif; letter-spacing:.08em; text-transform:uppercase; background:var(--c); padding:1.2mm 2.4mm; border-radius:99px; }}
.grid2 {{ display:grid; grid-template-columns:1fr 1fr; gap:5mm; }}
.pill {{ border-top:3px solid var(--t); padding-top:2.5mm; }}
.pill.sig {{ border-top-color:var(--o); }}
.pill h3 {{ font-size:10.5pt; }} .pill .en {{ font-size:8.5pt; color:var(--mut); margin-bottom:1.5mm; }}
.pill p {{ font-size:9pt; margin:0; }}
.pills {{ display:grid; grid-template-columns:repeat(3,1fr); gap:5mm; }}
.rhythm {{ display:grid; grid-template-columns:repeat(7,1fr); gap:1.5mm; margin-top:3mm; }}
.rhythm div {{ border:1px solid var(--b); padding:2mm; font-size:8pt; min-height:17mm; }}
.rhythm b {{ display:block; font:600 7.5pt/1 Inter, sans-serif; letter-spacing:.06em; text-transform:uppercase; color:var(--mut); margin-bottom:1.5mm; }}
/* briefs */
.brief {{ border:1px solid var(--b); padding:4mm 5mm; margin-bottom:4mm; break-inside:avoid; }}
.brief.give {{ border-color:var(--c); }}
.bh {{ display:flex; align-items:center; gap:2.5mm; margin-bottom:2mm; }}
.bd {{ font:600 9pt/1 Inter, sans-serif; }}
.sub {{ font-size:8.3pt; color:var(--mut); margin:1mm 0 2.5mm; }}
dl {{ margin:0; display:grid; gap:1.6mm; }}
.kv {{ display:grid; grid-template-columns:28mm 1fr; gap:3mm; font-size:9pt; }}
.kv dt {{ font:600 7.3pt/1.6 Inter, sans-serif; letter-spacing:.06em; text-transform:uppercase; color:var(--mut); }}
.kv dd {{ margin:0; }}
.kv.cap dd {{ background:var(--mist); padding:1.5mm 2.5mm; }}
.kv.check dd {{ background:var(--sand); padding:1.5mm 2.5mm; }}
.kv.media dd {{ border-left:3px solid var(--t); padding-left:2.5mm; }}
.mt {{ font-size:8pt; }}
.foot {{ margin-top:8mm; font-size:8pt; color:var(--mut); border-top:1px solid var(--b); padding-top:3mm; }}
</style></head><body>

<div class="cover">
  <div class="eyebrow">LookyBooky Zandvoort · @lookybooky.nl · Instagram plan</div>
  <h1>December 2026<br><em>Zandvoort sees us. Now make them stay.</em></h1>
  <p>The Instagram plan for 1–31 December: what our 24 posts taught us, the Dutch-first approach that follows from it, and every post for the month. Built from Meta insights (via vidIQ, pulled 23 Nov), the September and November plans, brand guide v3.25 and the Zandvoort profile.</p>
  <div class="stats">
    <div><b>99.3%</b><span>of reach is non-followers: Instagram already shows us to strangers</span></div>
    <div><b>7</b><span>link taps from 268 profile visits: the profile doesn't convert</span></div>
    <div><b>380 vs 182</b><span>median reach of Reels that hold viewers past 3s vs the rest</span></div>
    <div><b>0 of 24</b><span>captions in Dutch, in a town that is about 85% Dutch</span></div>
  </div>
</div>

<div class="eyebrow">In short</div>
<h2>Five decisions for December</h2>
<ol class="tight">
  <li><b>Fix the profile before 1 December.</b> Name "LookyBooky Zandvoort", a Dutch-first bio with the €10 offer, a tracked link and Highlights. Reach isn't the leak; the profile is.</li>
  <li><b>Show action and process, not atmosphere.</b> Beachcombing was 17% of posts and 41% of reach. Ambient venue posts were a third of posts and a fifth of reach.</li>
  <li><b>Go Dutch first.</b> Dutch captions and on-screen text, one English line. A test runs all month to confirm it.</li>
  <li><b>Four feed posts a week</b>: Reels Mon, Wed, Fri at 18:00 and a carousel on Thursday. Stories on 4–5 days. Rest at Christmas.</li>
  <li><b>Use gifting and one giveaway</b> to turn viewers into followers: the €10 pass as a Sinterklaas and Christmas gift, and a Christmas giveaway on 15–20 December.</li>
</ol>

<div class="sec grid2">
  <div class="box"><h3>What worked</h3><p class="muted" style="margin-top:2mm">Juttersgeluk beach walk: 1,935 reach, 30% skip rate. "Less screen time, more sea air": 1,182 reach, 31 shares, 8 comments. Filoxenia kitchen: 552 reach, watched 119%. Something happens in each of them.</p></div>
  <div class="box"><h3>What didn't</h3><p class="muted" style="margin-top:2mm">November's 8-second mood clips (median reach 118), "Save this" on content nobody saves (0 carousel saves), weekend and midday slots, English brand statements (0 organic shares).</p></div>
</div>
<p class="muted" style="margin-top:3mm;font-size:8.5pt">24 posts, 2 of them half of all reach, so read this as direction, not proof. Four posts show shares above reach (likely internal DMs) and are left out of the baselines. Meta withholds audience demographics below 100 followers.</p>

<div class="eyebrow" style="margin-top:9mm">Strategy</div>
<h2>Five content pillars</h2>
<div class="pills">
  <div class="pill sig"><h3 lang="nl">Kijk beter aan zee</h3><div class="en">Look closer at the coast · signature · 30%</div><p>Beachcombing, what the sea brings in, the winter coast in action, impact you can see.</p></div>
  <div class="pill"><h3 lang="nl">Van dichtbij bij lokale adressen</h3><div class="en">Up close at local spots · 25%</div><p>Hands, process and people behind the counter. Replaces ambient venue posts.</p></div>
  <div class="pill"><h3 lang="nl">Het dorp achter de boulevard</h3><div class="en">The village behind the boulevard · 15%</div><p>Heritage, streets, archive photos, then and now. Best follow rate on the account.</p></div>
  <div class="pill"><h3 lang="nl">Herkenbaar aan zee</h3><div class="en">So Zandvoort · 15%</div><p>Wind, uitwaaien, Buienradar, the gull at your table. Brought 2 of our 3 recorded follows.</p></div>
  <div class="pill"><h3 lang="nl">Slim uit in Zandvoort</h3><div class="en">A smart day out · conversion · max 15%</div><p>How the pass works, open in winter, day trips, gifts, giveaways. Mostly in Stories.</p></div>
  <div class="pill"><h3>Retire</h3><div class="en">&nbsp;</div><p>Brand statements, single images, one-line mood clips where nothing happens.</p></div>
</div>

<div class="sec grid2">
  <div><h2 style="font-size:14pt">Language and tone</h2>
  <ul class="tight">
    <li>Dutch caption and overlays, then one line starting "EN:". Tagline stays English.</li>
    <li>"je", never "u". Plain and direct: "Gewoon €10. Een jaar geldig."</li>
    <li>Real names and streets; local words: <i lang="nl">uitwaaien, strandjutten, Buienradar, lootjes trekken</i>.</li>
    <li>No superlatives, countdowns or "laatste kans". Max 2 emoji.</li>
    <li>Impact claims exactly as in the brand guide. CleanHub (global) stays separate from Juttersgeluk (local).</li>
    <li>A native speaker proofs all Dutch copy before posting.</li>
  </ul></div>
  <div><h2 style="font-size:14pt">Profile fix (before 1 Dec)</h2>
  <div class="box" lang="nl" style="font-size:9pt"><b>Name:</b> LookyBooky Zandvoort<br><b>Bio:</b> Lokale favorieten in Zandvoort 🌊 / €10 pass · 1 jaar geldig · voordeel bij lokale adressen / Elke pass: 1 kg ocean-bound waste weg via CleanHub / EN ↓ local deals + impact<br><b>Link:</b> lookybooky.nl + UTM tag<br><b>Highlights:</b> Zo werkt het · Open in de winter · Cadeau · Impact · Strandvondsten</div></div>
</div>

<div class="sec"><h2 style="font-size:14pt">Weekly rhythm</h2>
<div class="rhythm">
  <div><b>Mon</b><span class="chip reel">Reel</span><br>18:00</div><div><b>Tue</b><span class="chip">Stories</span><br>12:00 / 19:00</div>
  <div><b>Wed</b><span class="chip reel">Reel</span><br>18:00 (10:00 test)</div><div><b>Thu</b><span class="chip carousel">Carousel</span><br>18:00</div>
  <div><b>Fri</b><span class="chip reel">Reel</span><br>18:00</div><div><b>Sat</b><span class="chip">Stories</span><br>10:00</div><div><b>Sun</b><span class="chip community">Community</span><br>Replies</div>
</div>
<p class="muted" style="margin-top:3mm;font-size:8.5pt">Our evening posts reach a median of 182 accounts against 53 at midday. If production is tight, drop the Monday Reel: a steady 3 a week beats an abandoned 4.</p></div>

<div class="sec"><div class="eyebrow">Images and video</div><h2 style="font-size:14pt">Where the media comes from</h2>
<div class="grid2">
  <div><ul class="tight">
    <li><b>Our own library first</b> (Dropbox "Images" and "Videos", 468 files): every feed post uses it. Image names below drop the <i>LB2026_KimKramer_</i> prefix; .MOV files are videos.</li>
    <li><b>Codes:</b> ZV village (images) / beach (videos) · ZM, U Zandvoorts Museum and the explanation video · SA, SZ beach · JG, JGS Juttersgeluk · F Filoxenia · H De Haven · M Mel's · N Noya · SP Sweet Pearl · T Thalassa · IMG_ iPhone village clips.</li>
    <li><b>No new shoots needed</b> for December. The gull Reel works with a cut (gulls, then a fish dish), the beach walk uses Juttersgeluk footage, De Haven's fire is on video.</li>
  </ul></div>
  <div class="box"><h3>Zandvoort Marketing beeldbank</h3><p style="margin-top:2mm;font-size:9pt">beeldbankzandvoortmarketing.nl states: <i lang="nl">"Vermeld altijd de naam van de fotograaf. Foto's zijn alleen voor redactioneel gebruik."</i> So we use it only where our library has a gap and the post sells nothing: the shortest-day Reel (sunset), the Nieuwjaarsduik and event Stories. Always credit the photographer by name, and ask Zandvoort Marketing to confirm this use before 21 Dec.</p>
  <p style="font-size:9pt;margin-top:2mm"><b>Gaps in our own library:</b> no sunset, no train, no gull next to food, nothing Christmassy or wintry. Worth adding to the next shoot.</p></div>
</div></div>

<div class="sec grid2">
  <div><h2 style="font-size:14pt">Gifting</h2><ul class="tight">
    <li><b>3 Dec</b> carousel: <i lang="nl">"Lootjes getrokken? Budget: €10."</i></li>
    <li>"Cadeau" Highlight with the gift steps and a link.</li>
    <li><b>19 Dec</b> Story: the pass as a last-minute Christmas gift.</li>
    <li>Plain tone: price, validity, what the receiver gets.</li></ul></div>
  <div class="sand"><h3>Kerstgiveaway · 3 × 2 passes <span class="badge">15–20 Dec</span></h3>
    <p style="margin-top:2mm;font-size:9pt">Two passes per winner: one for you, one for who you'd bring. Enter by following, tagging one person and saying where you'd go first. A Reel co-hosted with one partner. Closes Sun 20 Dec 23:59; winners in Stories on Mon 21 Dec.<br><b>Before posting:</b> publish actievoorwaarden (Gedragscode Promotionele Kansspelen) and say it isn't run by Instagram. Kept out of tests and baselines; aim for 70%+ of new followers still following after 30 days.</p></div>
</div>

<div class="pb"></div>
<div class="eyebrow">December 2026 · times in CET</div>
<h2>The month at a glance</h2>
<p class="muted">16 feed posts (13 Reels including the giveaway, 3 carousels), Stories on 10 days, community or rest on 5. No carousel in Christmas week.</p>
<table><tr><th>Date</th><th>Time</th><th>Format</th><th>Post</th><th>Pillar</th><th>Test</th></tr>{glance}</table>
<p class="muted" style="margin-top:3mm;font-size:8.5pt">Already scheduled before December (November plan): CleanHub carousel (25 Nov) and Thalassa window-seat Reel (27 Nov). Post Thalassa as a Collab: it counts as a collab arm of test T4.</p>

<div class="pb"></div>
<div class="eyebrow">Post briefs</div>
<h2>Every feed post</h2>
{BRIEFS}

<div class="pb"></div>
<div class="eyebrow">Stories and community</div>
<h2>Story days and rest days</h2>
<table><tr><th>Date</th><th>Time</th><th>What</th><th>Sticker / link</th><th>Check</th></tr>{stories}</table>

<div class="sec"><div class="eyebrow">Targets</div><h2>KPIs from our own baseline</h2>
<table><tr><th>KPI</th><th>Baseline</th><th>31 Dec</th><th>31 Jan</th><th>28 Feb</th></tr>
<tr><td><b>North Star:</b> median non-follower reach per Reel (at 7 days)</td><td>182 (Nov 118)</td><td>250</td><td>350</td><td>500</td></tr>
<tr><td>Median Reel skip rate</td><td>65%</td><td>58%</td><td>52%</td><td>≤48%</td></tr>
<tr><td>Sends per reach, Reels</td><td>1.15% (Nov 0.24%)</td><td>1.0%</td><td>1.5%</td><td>2.0%</td></tr>
<tr><td>Followers</td><td>32</td><td>55</td><td>100</td><td>160</td></tr>
<tr><td>Website link taps per month</td><td>~2</td><td>10</td><td>20</td><td>30</td></tr>
<tr><td class="muted">Guardrail: carousel saves per 100 reach</td><td>0</td><td>0.5</td><td>1.0</td><td>1.5</td></tr>
<tr><td class="muted">Guardrail: giveaway followers still following at 30 days</td><td>–</td><td>logged</td><td>≥70%</td><td>≥70%</td></tr></table></div>

<div class="sec"><div class="eyebrow">Experiments</div><h2>Five tests running in December</h2>
<p class="muted">At our size, classic A/B significance isn't possible. Each test uses a Trial Reel (a second version shown only to non-followers) or alternating posts, with the decision rule set in advance.</p>
<table><tr><th>Test</th><th>Question</th><th>When</th><th>Decision rule</th></tr>
<tr><td><b>T1</b> Language</td><td>Do Dutch overlays and captions hold people longer than English?</td><td>7, 18, 28 Dec</td><td>Dutch wins skip rate in 2 of 3 without losing sends</td></tr>
<tr><td><b>T2</b> Hook</td><td>Does action in frame 1 beat a scenic opening?</td><td>4, 14 Dec (+1 Jan)</td><td>2 of 3 wins, 5+ points apart</td></tr>
<tr><td><b>T3</b> Length</td><td>Do 13–16s cuts reach further than 7–9s?</td><td>11, 23, 30 Dec</td><td>Winner of 2 of 3 sets the default</td></tr>
<tr><td><b>T4</b> Collab</td><td>Does a partner as co-author beat a tag?</td><td>Collab 27 Nov, 11 Dec · tag 2, 16 Dec</td><td>Collab averages 1.3× the reach</td></tr>
<tr><td><b>T5</b> Time</td><td>Can 10:00 match 18:00?</td><td>9, 21 Dec</td><td>Keep 18:00 unless both 10:00 posts win</td></tr></table></div>

<div class="sec"><div class="eyebrow">Before 1 December</div><h2>Open items</h2>
<table><tr><th>Task</th><th>Owner</th><th>By</th></tr>
<tr><td>Profile fix: rename, Dutch-first bio, UTM link, Highlights, pinned posts; Metricool timezone to Europe/Amsterdam</td><td>Social lead</td><td>30 Nov</td></tr>
<tr><td>Gift steps for the 3 Dec carousel and the Cadeau Highlight</td><td>Product</td><td>1 Dec</td></tr>
<tr><td>Pull the listed files from Dropbox for each week's edits; check Juttersgeluk and Filoxenia openings differ from the October/November posts</td><td>Abdul</td><td>Weekly</td></tr>
<tr><td>Ask Zandvoort Marketing to confirm using beeldbank photos (sunset, Nieuwjaarsduik) with photographer credit</td><td>Social lead</td><td>15 Dec</td></tr>
<tr><td>Giveaway: co-host partner, actievoorwaarden published</td><td>Social lead</td><td>12 Dec</td></tr>
<tr><td>Confirm event details (Nieuwjaarsduik 1 Jan, any winter events) and partner opening days for 26 Dec</td><td>Social lead</td><td>Before each Story</td></tr>
<tr><td>Native-speaker proof of all Dutch copy, one week ahead</td><td>Reviewer</td><td>Weekly</td></tr>
</table></div>

<div class="foot">Explore more. Spend less. Make an impact. · Sources: Meta owner insights for @lookybooky.nl via vidIQ (23 Nov 2026), Metricool best-time benchmark, LookyBooky brand guidelines v3.25, September and November 2026 content plans, Zandvoort municipality profile. Interactive version and full strategy available on request.</div>
</body></html>'''
open("output/LookyBooky_December_Plan.html", "w", encoding="utf-8").write(HTML)
print("html ok")
