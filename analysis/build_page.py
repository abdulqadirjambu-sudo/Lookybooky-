"""Builds output/NL_Strategy_Page.html (shareable page) from the calendar CSV + strategy content."""
import csv, html, datetime as dt
E = html.escape
rows = list(csv.DictReader(open("output/Next_30_Days_Calendar.csv", encoding="utf-8")))

def kind(fmt):
    f = fmt.lower()
    if f.startswith("reel"): return "reel"
    if f.startswith("carousel"): return "carousel"
    if f.startswith("stories"): return "stories"
    return "community"
KLABEL = {"reel": "Reel", "carousel": "Carousel", "stories": "Stories", "community": "Community"}

weeks = {}
for r in rows:
    d = dt.date.fromisoformat(r["date"])
    monday = d - dt.timedelta(days=d.weekday())
    weeks.setdefault(monday, []).append(r)

def day_html(r):
    k = kind(r["format"]); d = dt.date.fromisoformat(r["date"])
    is_give = "giveaway" in r["format"].lower()
    det = []
    def add(label, val, cls=""):
        if val and val.strip() not in ("", "—"):
            det.append(f'<div class="kv {cls}"><dt>{label}</dt><dd>{E(val).replace(chr(10), "<br>")}</dd></div>')
    add("Hook on screen", r["hook_onscreen_NL"], "nl")
    add("Visual", r["visual_direction"])
    add("Caption (NL)", r["caption_NL"], "nl")
    add("English line", r["caption_EN_line"])
    add("CTA", r["CTA"]); add("Hashtags", r["hashtags"])
    add("Collab / partner", r["collab_or_partner"]); add("Stories", r["story_support"])
    add("Watch", r["primary_KPI"]); add("Test", r["test_id"])
    add("Check before posting", r["checks_before_posting"], "check")
    badge = '<span class="badge">Giveaway</span>' if is_give else ""
    test = f'<span class="test">{E(r["test_id"].split(" ")[0])}</span>' if r["test_id"].startswith("T") else ""
    time = E(r["time_CET"]) if r["time_CET"] != "—" else ""
    return f'''<details class="day" data-kind="{k}">
<summary><span class="d"><b>{d.strftime("%a")}</b> {d.day} {d.strftime("%b")}</span><span class="t">{time}</span><span class="chip {k}">{KLABEL[k]}</span><span class="ti">{E(r["working_title"])}{badge}{test}</span></summary>
<dl>{"".join(det)}</dl></details>'''

cal = []
for monday, rs in weeks.items():
    end = monday + dt.timedelta(days=6)
    cal.append(f'<h3 class="wk">Week of {monday.day} {monday.strftime("%b")} – {end.day} {end.strftime("%b")}</h3><div class="days">' + "".join(day_html(r) for r in rs) + "</div>")
CAL = "\n".join(cal)

PILLARS = [("Impact & beachcombing", 16.7, 40.6), ("Coastal mood", 16.7, 25.2), ("Product explainer", 16.7, 11.3),
           ("Partner venue (ambient)", 33.3, 19.3), ("Village & heritage", 8.3, 2.0), ("Relatable humour", 8.3, 1.6)]
pbars = "".join(f'''<div class="pb"><div class="pn">{n}</div>
<div class="bars"><div class="bar posts" style="width:{p*1.6}%"><span>{p:.0f}% of posts</span></div>
<div class="bar reach" style="width:{q*1.6}%"><span>{q:.0f}% of reach</span></div></div></div>''' for n, p, q in PILLARS)

PAGE = f'''<title>LookyBooky Zandvoort Instagram Plan</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700&family=Inter:ital,wght@0,400;0,600;1,400&display=swap">
<style>
/* Layout: Ocean hero band, then alternating white/Mist sections; square panels, pill chips (LookyBooky design system) */
:root {{
  --turquoise:#18bfcb; --ocean:#0e2f39; --coral:#ff6f61; --sand:#fff2cc; --mist:#f3f7f6; --white:#ffffff;
  --surface:#ffffff; --surface-alt:#f3f7f6; --ink:#0e2f39; --ink-muted:rgba(14,47,57,.72); --border:rgba(14,47,57,.16);
  --band:#0e2f39; --on-band:#ffffff; --hl:#18bfcb; --focus:#0e2f39; --bar-a:rgba(14,47,57,.22); --sand-ink:#0e2f39; --sand-bg:#fff2cc;
  --display:Poppins, ui-sans-serif, system-ui, sans-serif; --text:Inter, ui-sans-serif, system-ui, sans-serif;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --surface:#0e2f39; --surface-alt:#143a46; --ink:#ffffff; --ink-muted:rgba(255,255,255,.75); --border:rgba(255,255,255,.2);
  --band:#0a242c; --focus:#18bfcb; --bar-a:rgba(255,255,255,.28); --sand-bg:#2a3a2c; --sand-ink:#fff2cc; color-scheme:dark }} }}
:root[data-theme="dark"] {{
  --surface:#0e2f39; --surface-alt:#143a46; --ink:#ffffff; --ink-muted:rgba(255,255,255,.75); --border:rgba(255,255,255,.2);
  --band:#0a242c; --focus:#18bfcb; --bar-a:rgba(255,255,255,.28); --sand-bg:#2a3a2c; --sand-ink:#fff2cc; color-scheme:dark }}
* {{ box-sizing:border-box }}
body {{ background:var(--surface); color:var(--ink); font:400 16px/1.55 var(--text); }}
.wrap {{ max-width:1080px; margin:0 auto; padding-left:max(16px, env(safe-area-inset-left,0px)); padding-right:max(16px, env(safe-area-inset-right,0px)); }}
section {{ padding-block:72px; }} section.alt {{ background:var(--surface-alt); }}
h1,h2,h3 {{ font-family:var(--display); text-wrap:balance; margin:0; }}
h2 {{ font-size:clamp(28px,4.2vw,44px); line-height:1.08; font-weight:600; letter-spacing:-.01em; }}
h3 {{ font-size:20px; font-weight:600; line-height:1.3; }}
p {{ margin:0; max-width:66ch; }}
.eyebrow {{ font:600 13px/16px var(--text); letter-spacing:.08em; text-transform:uppercase; color:var(--ink-muted); margin-bottom:12px; }}
.lead {{ font-size:18px; line-height:28px; color:var(--ink-muted); margin-top:14px; }}
.head {{ margin-bottom:36px; }}
a {{ color:inherit; text-underline-offset:3px; }}
:focus-visible {{ outline:2px solid var(--focus); outline-offset:2px; }}
/* hero */
.hero {{ background:var(--band); color:var(--on-band); margin-top:calc(-1 * env(safe-area-inset-top,0px)); padding-top:calc(env(safe-area-inset-top,0px) + 56px); padding-bottom:0; }}
.hero h1 {{ font-size:clamp(40px,7vw,76px); line-height:1.02; font-weight:700; letter-spacing:-.02em; }}
.hero h1 em {{ font-style:normal; color:var(--hl); }}
.hero .eyebrow {{ color:rgba(255,255,255,.75); }}
.hero p.lead {{ color:rgba(255,255,255,.82); }}
.meta {{ display:flex; flex-wrap:wrap; gap:8px 20px; margin-top:28px; font-size:14px; color:rgba(255,255,255,.75); }}
.meta b {{ color:#fff; font-weight:600; }}
.diag {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:1px; margin-top:44px; background:rgba(255,255,255,.14); }}
.diag div {{ background:var(--band); padding:22px 20px 26px; min-width:0; }}
.diag .n {{ font:600 32px/1 var(--display); color:var(--hl); font-variant-numeric:tabular-nums; }}
.diag .l {{ margin-top:10px; font-size:15px; color:rgba(255,255,255,.85); }}
.wave {{ display:block; width:100%; height:44px; margin-top:40px; }}
.wave path {{ fill:var(--surface); }}
/* generic */
.grid2 {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); gap:24px; }}
.panel {{ background:var(--surface); border:1px solid var(--border); padding:24px; min-width:0; }}
.alt .panel {{ background:var(--surface); }}
.panel h3 {{ margin-bottom:8px; }}
.muted {{ color:var(--ink-muted); }}
.small {{ font-size:14px; }}
table {{ border-collapse:collapse; width:100%; font-size:15px; }}
.tbl {{ overflow-x:auto; border:1px solid var(--border); background:var(--surface); }}
th,td {{ text-align:left; padding:12px 14px; border-bottom:1px solid var(--border); vertical-align:top; }}
th {{ font:600 12px/16px var(--text); letter-spacing:.08em; text-transform:uppercase; color:var(--ink-muted); background:var(--surface-alt); }}
tr:last-child td {{ border-bottom:0; }}
td.num {{ font-variant-numeric:tabular-nums; white-space:nowrap; }}
.nl {{ font-style:normal; }}
/* profile fix */
.bio {{ font:400 15px/1.6 var(--text); background:var(--surface-alt); padding:16px 18px; border-left:0; }}
.alt .bio {{ background:var(--surface); }}
/* pillars */
.pillars {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:16px; }}
.pil {{ border-top:4px solid var(--turquoise); background:var(--surface); padding:20px; min-width:0; }}
.pil .sh {{ font:600 13px/16px var(--text); letter-spacing:.06em; color:var(--ink-muted); text-transform:uppercase; }}
.pil h3 {{ margin:8px 0 2px; }}
.pil .tr {{ font-size:14px; color:var(--ink-muted); margin-bottom:10px; }}
.pil p {{ font-size:15px; }}
.pil .ev {{ margin-top:12px; font-size:14px; padding-top:12px; border-top:1px solid var(--border); }}
.pil.sig {{ border-top-color:var(--ink); }}
.pb {{ display:grid; grid-template-columns:minmax(120px,200px) 1fr; gap:12px; align-items:center; padding:8px 0; border-bottom:1px solid var(--border); }}
.pn {{ font-size:14px; font-weight:600; }}
.bars {{ display:grid; gap:4px; min-width:0; }}
.bar {{ height:22px; position:relative; min-width:2px; }}
.bar span {{ position:absolute; left:calc(100% + 8px); top:2px; font-size:12px; white-space:nowrap; color:var(--ink-muted); font-variant-numeric:tabular-nums; }}
.bar.posts {{ background:var(--bar-a); }} .bar.reach {{ background:var(--turquoise); }}
.legend {{ display:flex; gap:18px; font-size:13px; color:var(--ink-muted); margin:6px 0 4px; }}
.legend i {{ display:inline-block; width:12px; height:12px; margin-right:6px; vertical-align:-1px; }}
/* rules */
.rules {{ display:grid; grid-template-columns:1fr 1fr; gap:0; border:1px solid var(--border); background:var(--surface); }}
.rules > div {{ padding:20px 22px; min-width:0; }}
.rules > div + div {{ border-left:1px solid var(--border); }}
.rules ul {{ margin:10px 0 0; padding-left:18px; }} .rules li {{ margin:6px 0; }}
@media (max-width:640px) {{ .rules {{ grid-template-columns:1fr; }} .rules > div + div {{ border-left:0; border-top:1px solid var(--border); }} section {{ padding-block:48px; }} .pb {{ grid-template-columns:1fr; gap:6px; }} }}
pre.fw {{ font:400 14px/1.7 ui-monospace, SFMono-Regular, Menlo, monospace; background:var(--surface-alt); padding:16px 18px; overflow-x:auto; margin:0; white-space:pre; }}
.alt pre.fw {{ background:var(--surface); }}
/* week rhythm */
.rhythm {{ display:grid; grid-template-columns:repeat(7,minmax(0,1fr)); gap:6px; }}
.rhythm div {{ background:var(--surface); border:1px solid var(--border); padding:10px 8px; min-height:88px; font-size:13px; }}
.rhythm b {{ display:block; font:600 12px/16px var(--text); letter-spacing:.06em; text-transform:uppercase; color:var(--ink-muted); margin-bottom:6px; }}
@media (max-width:700px) {{ .rhythm {{ grid-template-columns:repeat(2,minmax(0,1fr)); }} }}
/* chips */
.chip {{ display:inline-block; font:600 12px/1 var(--text); padding:6px 10px; border-radius:9999px; border:1px solid var(--border); white-space:nowrap; }}
.chip.reel {{ background:var(--turquoise); color:#0e2f39; border-color:var(--turquoise); }}
.chip.carousel {{ background:var(--ink); color:var(--surface); border-color:var(--ink); }}
.chip.stories {{ background:transparent; color:var(--ink); border-color:var(--ink); }}
.chip.community {{ background:transparent; color:var(--ink-muted); }}
.badge {{ display:inline-block; margin-left:8px; font:600 11px/1 var(--text); letter-spacing:.08em; text-transform:uppercase; background:var(--coral); color:#0e2f39; padding:5px 9px; border-radius:9999px; vertical-align:2px; }}
.test {{ display:inline-block; margin-left:8px; font:600 11px/1 var(--text); color:var(--ink-muted); border:1px solid var(--border); padding:4px 7px; border-radius:9999px; vertical-align:2px; }}
/* calendar */
.filters {{ display:flex; flex-wrap:wrap; gap:8px; margin-bottom:20px; }}
.filters button {{ font:600 14px/1 var(--display); padding:10px 16px; border-radius:9999px; border:1px solid var(--border); background:var(--surface); color:var(--ink); cursor:pointer; }}
.filters button[aria-pressed="true"] {{ background:var(--turquoise); border-color:var(--turquoise); color:#0e2f39; }}
.wk {{ font:600 13px/16px var(--text); letter-spacing:.08em; text-transform:uppercase; color:var(--ink-muted); margin:28px 0 10px; }}
.days {{ border:1px solid var(--border); background:var(--surface); }}
.day + .day {{ border-top:1px solid var(--border); }}
.day summary {{ display:grid; grid-template-columns:92px 104px 104px 1fr; gap:12px; align-items:center; padding:14px 16px; cursor:pointer; list-style:none; }}
.day summary::-webkit-details-marker {{ display:none; }}
.day summary:hover {{ background:var(--surface-alt); }}
.day .d {{ font-variant-numeric:tabular-nums; }} .day .d b {{ font-weight:600; }}
.day .t {{ font-variant-numeric:tabular-nums; color:var(--ink-muted); font-size:14px; }}
.day .ti {{ font-weight:600; min-width:0; }}
.day summary .chip {{ justify-self:start; }}
.day dl {{ margin:0; padding:4px 16px 18px; display:grid; gap:10px; background:var(--surface-alt); }}
.kv {{ display:grid; grid-template-columns:170px 1fr; gap:12px; font-size:15px; }}
.kv dt {{ font:600 12px/20px var(--text); letter-spacing:.06em; text-transform:uppercase; color:var(--ink-muted); }}
.kv dd {{ margin:0; min-width:0; overflow-wrap:anywhere; }}
.kv.check dd {{ background:var(--sand-bg); color:var(--sand-ink); padding:8px 10px; }}
@media (max-width:640px) {{ .day summary {{ grid-template-columns:auto auto 1fr; }} .day .ti {{ grid-column:1 / -1; }} .kv {{ grid-template-columns:1fr; gap:2px; }} }}
.give {{ background:var(--sand-bg); color:var(--sand-ink); padding:24px; }}
.give h3 {{ margin-bottom:6px; }}
.give .muted {{ color:inherit; opacity:.8; }}
footer {{ padding-block:40px; font-size:14px; color:var(--ink-muted); border-top:1px solid var(--border); }}
@media (prefers-reduced-motion: reduce) {{ * {{ transition:none !important; }} }}
</style>

<header class="hero"><div class="wrap">
  <div class="eyebrow">@lookybooky.nl · Instagram plan · 24 Nov 2026 – 21 Feb 2027</div>
  <h1>Zandvoort sees us.<br><em>Now make them stay.</em></h1>
  <p class="lead">What 24 posts taught us, the Dutch-first plan that follows from it, and the next 30 days, post by post. Built from Meta insights (via vidIQ), the September and November plans, brand guide v3.25 and the Zandvoort profile.</p>
  <div class="meta"><span><b>32</b> followers</span><span><b>4,848</b> accounts reached in 90 days</span><span><b>24</b> posts since 31 Aug</span><span>Prepared 23 Nov 2026</span></div>
  <div class="diag">
    <div><div class="n">99.3%</div><div class="l">of reach is non-followers. Instagram already shows us to strangers.</div></div>
    <div><div class="n">7</div><div class="l">link taps from 268 profile visits. The profile doesn't convert.</div></div>
    <div><div class="n">380 vs 182</div><div class="l">median reach for Reels that hold people past 3 seconds vs the rest.</div></div>
    <div><div class="n">0 of 24</div><div class="l">captions in Dutch, in a town that is about 85% Dutch.</div></div>
  </div>
</div>
<svg class="wave" viewBox="0 0 1440 44" preserveAspectRatio="none" aria-hidden="true"><path d="M0 26 C 240 2, 480 2, 720 22 S 1200 44, 1440 18 L1440 44 L0 44 Z"/></svg>
</header>

<section><div class="wrap">
  <div class="head"><div class="eyebrow">What the data says</div><h2>Action and process travel. Atmosphere doesn't.</h2>
  <p class="lead">Venue atmosphere is a third of our posts but a fifth of our reach. Beachcombing and impact is a sixth of posts and 41% of reach. The kitchen Reel at Filoxenia (552 reach, watched 119%) is the one venue post that worked, because something happens in it.</p></div>
  <div class="legend"><span><i style="background:var(--bar-a)"></i>Share of posts</span><span><i style="background:var(--turquoise)"></i>Share of reach</span></div>
  <div>{pbars}</div>
  <div class="grid2" style="margin-top:36px">
    <div class="panel"><h3>Best performers</h3><p class="small muted">Juttersgeluk beach walk: 1,935 reach, 30% skip rate (the lowest). "Less screen time, more sea air": 1,182 reach, 31 shares, 8 comments. Filoxenia kitchen: 552 reach.</p></div>
    <div class="panel"><h3>What failed</h3><p class="small muted">November's 8-second mood clips (median reach 118), "Save this" on content nobody saves (0 carousel saves), weekend and midday slots, English brand statements (0 organic shares).</p></div>
    <div class="panel"><h3>Read with care</h3><p class="small muted">24 posts, 2 of them half of all reach: directional, not proof. Four posts show shares above reach, likely internal DMs, so they're left out of the baselines. Meta withholds demographics under 100 followers.</p></div>
  </div>
</div></section>

<section class="alt"><div class="wrap">
  <div class="head"><div class="eyebrow">Day 1 · quick win</div><h2>Fix the profile before posting more</h2>
  <p class="lead">Reach isn't the leak. The profile is. These changes take an hour.</p></div>
  <div class="tbl"><table>
    <tr><th>Field</th><th>Now</th><th>New</th></tr>
    <tr><td>Name</td><td>Lou</td><td><b>LookyBooky Zandvoort</b> (makes "Zandvoort" searchable)</td></tr>
    <tr><td>Bio</td><td class="muted">Curated local favourites with real deals and impact built in. Explore more. Spend less. Make an impact.</td><td><div class="bio" lang="nl">Lokale favorieten in Zandvoort 🌊<br>€10 pass · 1 jaar geldig · voordeel bij lokale adressen<br>Elke pass: 1 kg ocean-bound waste weg via CleanHub<br>EN ↓ local deals + impact</div></td></tr>
    <tr><td>Link</td><td>lookybooky.nl</td><td>lookybooky.nl with <code>utm_source=instagram&amp;utm_medium=social&amp;utm_campaign=bio</code></td></tr>
    <tr><td>Highlights</td><td>none</td><td>Zo werkt het · Open in de winter · Cadeau · Impact · Strandvondsten</td></tr>
    <tr><td>Pinned</td><td>none</td><td>Juttersgeluk beach walk · "Less screen time" · "Open in de winter" carousel</td></tr>
  </table></div>
</div></section>

<section><div class="wrap">
  <div class="head"><div class="eyebrow">Positioning</div><h2>Five pillars, tuned to Zandvoort</h2>
  <p class="lead">The local friend who shows you what's worth your time in Zandvoort, all year round, and what your visit does for the coast.</p></div>
  <div class="pillars">
    <div class="pil sig"><div class="sh">Signature · 30%</div><h3 lang="nl">Kijk beter aan zee</h3><div class="tr">Look closer at the coast</div><p>Beachcombing, what the sea brings in, the winter coast in action, impact you can see.</p><div class="ev">17% of posts, 41% of reach. Our best Reel.</div></div>
    <div class="pil"><div class="sh">25%</div><h3 lang="nl">Van dichtbij bij lokale adressen</h3><div class="tr">Up close at local spots</div><p>Hands, process and people behind the counter. Replaces ambient venue posts.</p><div class="ev">Process: 552 reach. Ambient: median 43.</div></div>
    <div class="pil"><div class="sh">15%</div><h3 lang="nl">Het dorp achter de boulevard</h3><div class="tr">The village behind the boulevard</div><p>Heritage, streets, archive photos, then and now. The real Zandvoort after the F1.</p><div class="ev">Best follow rate on the account.</div></div>
    <div class="pil"><div class="sh">15%</div><h3 lang="nl">Herkenbaar aan zee</h3><div class="tr">So Zandvoort</div><p>Wind, uitwaaien, Buienradar, the gull at your table, the group chat.</p><div class="ev">2 of 3 recorded follows; the most comments.</div></div>
    <div class="pil"><div class="sh">Max 15% · conversion</div><h3 lang="nl">Slim uit in Zandvoort</h3><div class="tr">A smart day out</div><p>How the pass works, open in winter, a day trip by train, the pass as a gift, giveaways.</p><div class="ev">Price mentions cut reach. Keep it to Stories and end cards.</div></div>
  </div>
</div></section>

<section class="alt"><div class="wrap">
  <div class="head"><div class="eyebrow">Language and tone</div><h2>Dutch first, one line of English</h2>
  <p class="lead">Captions and overlays in Dutch, then one line starting "EN:". The tagline stays in English. We use "je", never "u". A 30-day test (T1) confirms it, and at 100 followers Meta unlocks the audience data to recheck.</p></div>
  <div class="rules">
    <div><h3>Do</h3><ul>
      <li>Concrete facts: €10, 1 jaar geldig, Kerkstraat, 1 kg via CleanHub</li>
      <li>Plain and direct (nuchter): "Gewoon €10. Een jaar geldig."</li>
      <li>Real names, streets and people</li>
      <li>Local references: <span lang="nl">uitwaaien, strandjutten, Buienradar, groepsapp, NS-trein, lootjes trekken</span></li>
      <li>Impact claims exactly as in the brand guide; CleanHub (global) kept apart from Juttersgeluk (local)</li>
    </ul></div>
    <div><h3>Don't</h3><ul>
      <li>Superlatives: "de beste", "ultiem", "verborgen pareltje", "magisch"</li>
      <li>Fake urgency: countdowns, "laatste kans!"</li>
      <li>"Lokale favorieten ontdekken" in every caption</li>
      <li>More than 2 emoji, stacked exclamation marks, "gezellig" more than once a month</li>
      <li>AI tells: "het is niet X, het is Y", one sentence per line, em dashes in posts</li>
    </ul></div>
  </div>
  <div class="grid2" style="margin-top:24px">
    <div><h3 style="margin-bottom:10px">Caption framework</h3><pre class="fw" lang="nl">1  HAAK      ≤125 tekens · het moment
2  CONTEXT   wat · waar (straat) · wie
3  LOOKYBOOKY  1 feitelijke zin
4  CTA       Stuur dit naar… · vraag · Bewaar
5  EN:       1 regel
6  #Zandvoort #LookyBooky + 1–2 NL tags</pre></div>
    <div><h3 style="margin-bottom:10px">Reel rules</h3><ol class="small" style="margin:0;padding-left:20px">
      <li>Something happens in frame 1: a hand, a pour, a pick-up. No establishing shots.</li>
      <li>2–6 Dutch words on screen that open a question. Works muted.</li>
      <li>Length follows the story until test T3 reports (the best Reel was 15s).</li>
      <li>A payoff worth sending: who sends this, to whom, and why?</li>
      <li>Original, no watermark, licensed sound, real people.</li>
    </ol><p class="small muted" style="margin-top:12px">All Dutch copy is an original draft. A native speaker proofs it before posting.</p></div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="head"><div class="eyebrow">Format and funnel</div><h2>The weekly rhythm</h2>
  <p class="lead">Three Reels for discovery, one carousel for saves and follows, Stories on 4–5 days for community and conversion. If production is tight, drop the Monday Reel. A steady 3 a week beats an abandoned 4.</p></div>
  <div class="rhythm">
    <div><b>Mon</b><span class="chip reel">Reel</span><div class="small" style="margin-top:6px">18:00</div></div>
    <div><b>Tue</b><span class="chip stories">Stories</span><div class="small" style="margin-top:6px">12:00 / 19:00</div></div>
    <div><b>Wed</b><span class="chip reel">Reel</span><div class="small" style="margin-top:6px">18:00 (10:00 on test weeks)</div></div>
    <div><b>Thu</b><span class="chip carousel">Carousel</span><div class="small" style="margin-top:6px">18:00</div></div>
    <div><b>Fri</b><span class="chip reel">Reel</span><div class="small" style="margin-top:6px">18:00</div></div>
    <div><b>Sat</b><span class="chip stories">Stories</span><div class="small" style="margin-top:6px">10:00</div></div>
    <div><b>Sun</b><span class="chip community">Community</span><div class="small" style="margin-top:6px">Replies, partners</div></div>
  </div>
  <p class="small muted" style="margin-top:14px">Why 18:00: our evening posts have a median reach of 182 (13 posts) against 53 at midday (3 posts). Metricool's general curve also peaks at 18:00 and 10:00 on weekdays; 10:00 is tested in T5. Partner Collab posts run on half the venue Reels (test T4).</p>
</div></section>

<section class="alt"><div class="wrap">
  <div class="head"><div class="eyebrow">Gifting and giveaways</div><h2>Passes as gifts, and one giveaway a month</h2>
  <p class="lead">Lootjes trekken for pakjesavond runs on a €10–€20 budget, and the pass is digital, so it works as a last-minute Christmas gift too. Giveaways are a follow tool: they help us reach 100 followers, which unlocks the audience data.</p></div>
  <div class="grid2">
    <div class="panel"><h3>Gifting</h3><ul class="small" style="margin:8px 0 0;padding-left:18px">
      <li><b>3 Dec</b> carousel: <span lang="nl">"Lootjes getrokken? Budget: €10."</span></li>
      <li>New <b>Cadeau</b> Highlight with the gift steps and a UTM link</li>
      <li><b>19 Dec</b> Story: <span lang="nl">"Last-minute kerstcadeau? De pass is digitaal."</span></li>
      <li>Plain tone: price, validity, what the receiver gets. No "perfect gift!!"</li>
    </ul></div>
    <div class="give"><h3>Kerstgiveaway: 3 x 2 passes <span class="badge">15–20 Dec</span></h3>
      <p class="small"><b>Prize:</b> two passes per winner, one for you and one for who you'd bring.<br>
      <b>Enter:</b> follow @lookybooky.nl, tag <i>one</i> person you'd bring, and say where you'd go first. That last step filters out prize hunters.<br>
      <b>Format:</b> a Reel co-hosted with one partner as Collab. Stories reminders on 15, 17 and 19 Dec; closes Sun 20 Dec 23:59; winners in Stories on Mon 21 Dec.<br>
      <b>Rules:</b> publish actievoorwaarden first (Gedragscode Promotionele Kansspelen): organiser, period, prize, how winners are drawn, free to enter, 18+ or parental consent, privacy. Say it isn't run by Instagram.<br>
      <b>Measure:</b> left out of all tests and baselines. Log giveaway follows separately; aim for 70% or more still following after 30 days.</p></div>
  </div>
</div></section>

<section id="calendar"><div class="wrap">
  <div class="head"><div class="eyebrow">Next 30 days · 24 Nov – 23 Dec · times in CET</div><h2>The calendar, post by post</h2>
  <p class="lead">17 feed posts (13 Reels, 4 carousels), Stories on 9 days and a community block on 4. Open any day for the hook, visual, Dutch caption, English line, CTA, test and what to check before posting.</p></div>
  <div class="filters" role="group" aria-label="Filter by format">
    <button type="button" id="f-all" data-f="all" aria-pressed="true">All</button>
    <button type="button" id="f-reel" data-f="reel" aria-pressed="false">Reels</button>
    <button type="button" id="f-carousel" data-f="carousel" aria-pressed="false">Carousels</button>
    <button type="button" id="f-stories" data-f="stories" aria-pressed="false">Stories</button>
  </div>
  {CAL}
  <p class="small muted" style="margin-top:18px">Three posts need a short shoot: a gull clip (4 Dec, fallback given), the beach walk with a bag (14 Dec) and the De Haven fireplace on video (16 Dec). Every event post waits for the organiser's own confirmation.</p>
</div></section>

<section class="alt"><div class="wrap">
  <div class="head"><div class="eyebrow">KPIs</div><h2>Targets from our own baseline</h2>
  <p class="lead">One North Star and four supporting numbers. Reel figures are read at 7 days so old and new posts compare fairly.</p></div>
  <div class="tbl"><table>
    <tr><th>KPI</th><th>Baseline</th><th>30 days<br>23 Dec</th><th>60 days<br>22 Jan</th><th>90 days<br>21 Feb</th></tr>
    <tr><td><b>North Star:</b> median non-follower reach per Reel</td><td class="num">182 (Nov 118)</td><td class="num">250</td><td class="num">350</td><td class="num">500</td></tr>
    <tr><td>Median Reel skip rate</td><td class="num">65%</td><td class="num">58%</td><td class="num">52%</td><td class="num">≤48%</td></tr>
    <tr><td>Sends per reach, Reels</td><td class="num">1.15% (Nov 0.24%)</td><td class="num">1.0%</td><td class="num">1.5%</td><td class="num">2.0%</td></tr>
    <tr><td>Followers</td><td class="num">32</td><td class="num">55</td><td class="num">100</td><td class="num">160</td></tr>
    <tr><td>Website link taps per month</td><td class="num">~2</td><td class="num">10</td><td class="num">20</td><td class="num">30</td></tr>
    <tr><td class="muted">Guardrail: carousel saves per 100 reach</td><td class="num">0</td><td class="num">0.5</td><td class="num">1.0</td><td class="num">1.5</td></tr>
    <tr><td class="muted">Guardrail: giveaway followers still following at 30 days</td><td class="num">–</td><td class="num">logged</td><td class="num">≥70%</td><td class="num">≥70%</td></tr>
  </table></div>
  <div class="grid2" style="margin-top:24px">
    <div class="panel small"><h3>When to act</h3><p>Three Reels in a row above 65% skip: re-cut openings first. Reach up but followers flat 2 weeks after the profile fix: try a second bio. Sends below 0.5% for a month: more "Herkenbaar aan zee". A missed target means new tactics, not a new target.</p></div>
    <div class="panel small"><h3>Review rhythm</h3><p>Log every post at 48 hours and 7 days. A 30-minute review every Monday. At 30 days, re-pull vidIQ and re-run the audit script. A full content audit at 90 days.</p></div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="head"><div class="eyebrow">Experiments</div><h2>Five tests to run now</h2>
  <p class="lead">With 100–2,000 reach per post, classic A/B significance isn't possible. Each test uses a Trial Reel (the same footage as a second version, shown only to non-followers) or alternating posts, with a decision rule set in advance.</p></div>
  <div class="tbl"><table>
    <tr><th>Test</th><th>Question</th><th>Design</th><th>We decide when</th></tr>
    <tr><td><b>T1</b> Language</td><td>Do Dutch overlays and captions hold people longer?</td><td>NL main post vs EN Trial Reel · 30 Nov, 7 Dec, 18 Dec</td><td>NL wins skip rate in 2 of 3 without losing sends</td></tr>
    <tr><td><b>T2</b> Hook</td><td>Does action in frame 1 beat a scenic opening?</td><td>Action-first vs scenic-first Trial Reel · 4 Dec, 14 Dec, +1 in Jan</td><td>2 of 3 wins with a gap of 5+ points in skip rate</td></tr>
    <tr><td><b>T3</b> Length</td><td>Do 13–16s cuts reach further than 7–9s?</td><td>Same footage, two lengths · 11 Dec, 23 Dec, +1 in Jan</td><td>The winner of 2 of 3 sets the default length</td></tr>
    <tr><td><b>T4</b> Collab</td><td>Does a partner as co-author beat a tag?</td><td>Collab (27 Nov, 11 Dec) vs tag only (2 Dec, 16 Dec)</td><td>Collab averages 1.3× the reach: make it the default</td></tr>
    <tr><td><b>T5</b> Time</td><td>Can 10:00 match 18:00?</td><td>10:00 Reels on 9 and 21 Dec vs that week's 18:00 median</td><td>Keep 18:00 unless both 10:00 posts win</td></tr>
  </table></div>
</div></section>

<section class="alt"><div class="wrap">
  <div class="head"><div class="eyebrow">First week</div><h2>Who does what</h2></div>
  <div class="tbl"><table>
    <tr><th>When</th><th>Task</th><th>Owner</th></tr>
    <tr><td class="num">Tue 24 Nov</td><td>Profile rename, Dutch-first bio, UTM link, Highlights, pinned posts. Metricool timezone to Europe/Amsterdam. Start the DM-send log.</td><td>Social lead</td></tr>
    <tr><td class="num">Wed 25 Nov</td><td>Gift steps for the 3 Dec carousel and the Cadeau Highlight. Draft the giveaway actievoorwaarden; pick the co-host partner.</td><td>Product / Isabel</td></tr>
    <tr><td class="num">Wed 25 Nov</td><td>Partner emails: Collab acceptance and filming slots (gull, beach walk, De Haven fireplace).</td><td>Partnerships</td></tr>
    <tr><td class="num">Every Fri</td><td>Cut and approve next week's 4 feed posts.</td><td>Abdul + reviewer</td></tr>
    <tr><td class="num">Daily</td><td>15-minute community block; log post numbers at 48h and 7 days.</td><td>Social lead</td></tr>
    <tr><td class="num">23 Dec</td><td>30-day review: decide on tests T1, T4 and T5.</td><td>Social lead</td></tr>
  </table></div>
</div></section>

<footer><div class="wrap">
  <p><b>Explore more. Spend less. Make an impact.</b></p>
  <p style="margin-top:8px">Sources: Meta owner insights for @lookybooky.nl via vidIQ (pulled 23 Nov 2026), Metricool best-time benchmark, LookyBooky brand guidelines v3.25, Social Media planning September, Content Plan 2–29 November 2026, Zandvoort municipality profile.</p>
</div></footer>

<script>
(function () {{
  var btns = document.querySelectorAll('.filters button');
  var days = document.querySelectorAll('.day');
  var weeks = document.querySelectorAll('.days');
  function apply(f) {{
    btns.forEach(function (b) {{ b.setAttribute('aria-pressed', String(b.dataset.f === f)); }});
    days.forEach(function (d) {{ d.hidden = !(f === 'all' || d.dataset.kind === f); }});
    weeks.forEach(function (w) {{
      var any = Array.prototype.some.call(w.querySelectorAll('.day'), function (d) {{ return !d.hidden; }});
      w.hidden = !any; var h = w.previousElementSibling; if (h) h.hidden = !any;
    }});
    try {{ localStorage.setItem('lb-cal-filter', f); }} catch (e) {{}}
  }}
  btns.forEach(function (b) {{ b.addEventListener('click', function () {{ apply(b.dataset.f); }}); }});
  var saved = 'all'; try {{ saved = localStorage.getItem('lb-cal-filter') || 'all'; }} catch (e) {{}}
  apply(saved);
}})();
</script>
'''
open("output/NL_Strategy_Page.html", "w", encoding="utf-8").write(PAGE)
print("written", len(PAGE))
