# LookyBooky Instagram: Phase 2 Diagnostic Audit

**Account:** @lookybooky.nl · **Window:** 31 Aug – 23 Nov 2026 (all 24 posts since launch)
**Prepared:** 23 Nov 2026 · **Frameworks:** `content-audit` (AUDIT), `instagram-growth` (growth-loop diagnosis), `marketing-psychology`

## Data sources and limits

| Source | What it gave | Limits |
|---|---|---|
| vidIQ → Meta owner insights (`data/ig_posts.csv`, raw JSON in `data/raw/`) | Per-post views, reach, likes, comments, shares, saves; Reels skip rate and watch time; account reach, profile visits, link taps; follows and profile visits per feed post | Meta does not return follows for Reels. Audience demographics (city, age, language) are **withheld below 100 followers**. Metrics are lifetime, so older posts have had longer to accumulate. |
| Metricool (brand 8313107) | Best-time-to-post curve | Connected today, so no post history yet. Its best-time values run into the thousands on a 32-follower account, so the curve is a **general benchmark**, not your audience. The brand timezone is set to Asia/Calcutta; change it to Europe/Amsterdam. |
| September plan, November plan (2–29 Nov), brand guidelines v3.25, Zandvoort profile | The plan to audit against, and the local context | The October calendar was not supplied, so October is audited against what was posted, not what was planned. |

**Sample size warning.** There are 24 posts and 2 of them produced 50% of all reach. Everything below is directional. Rates are given with raw counts so nobody calls a post a winner on 20 reach.

**Possible seeded shares.** Four posts have more shares than accounts reached, or close to it: Mel's carousel (24 shares, 20 reach), the gull carousel (75 / 69), the group-chat carousel (28 / 32) and the launch video (68 / 245). That pattern almost always means the team or partners DM'd the post widely. These four are flagged in `data/post_tags.csv` and left out of the share-rate baselines.

---

## 1. Performance baseline

### Account funnel (last 90 days)

| Stage | Value | Rate |
|---|---|---|
| Accounts reached | 4,848 | **99.3% non-followers** |
| Profile visits | 268 | 5.5% of reach |
| Website link taps | 7 | **2.6% of visits · 0.14% of reach** |
| Followers (total) | 32 | |

**Diagnosis (`instagram-growth`):** two stages are broken.
1. **Follow and click conversion is the biggest leak.** Instagram is already showing the content to strangers; 99% of reach is non-followers. Of 268 profile visits, almost nobody follows or taps the link. The profile is the likely cause: the display name is "Lou", the bio is generic English with no "Zandvoort", no Dutch and no concrete offer (€10, valid one year), and there is no Highlight explaining the pass.
2. **Reach is inconsistent.** It depends on a few hits. October reached 4,245 accounts from 10 posts; November reached 1,356 from 9 posts, even though November had more Reels.

### Format breakdown

| Format | Posts | Median reach | Mean reach | Median ER (by reach) | Shares | Saves | Follows |
|---|---|---|---|---|---|---|---|
| Reel | 15 | **182** | 371 | 5.2% | 129 | 5 | n/a* |
| Carousel | 8 | 47 | 87 | 15.4%† | 128† | **0** | 3 |
| Single image | 1 | 29 | 29 | 13.8% | 0 | 0 | 0 |

\* Meta doesn't return Reel follows. † Inflated by seeded shares; without those posts the carousel median ER is 9.7% and the median share rate is 0%.

- **Reels are the only format that reaches people.** Carousels get roughly a quarter of the median Reel reach.
- **Saves are almost zero.** There are 5 saves across 24 posts and none on any carousel, even the two that asked "Save this". Nothing posted so far is reference material worth saving.
- **Organic sends per reach for Reels is 1.15% pooled** (61 shares on 5,325 reach). That sits in the "solid" band (1–2%), but two Reels supplied 54 of the 61 shares. The median Reel had **0 shares**.

### Top vs bottom performers

Ten percent of 24 posts is about 2, so 3 each way are shown for context.

| | Post | Format | Reach | Skip rate | Shares | Comments | Why |
|---|---|---|---|---|---|---|---|
| **Top** | Juttersgeluk beach walk (9 Oct, Fri 18:52) | Reel 15s | **1,935** | **30%** | 23 | 2 | Opens on an action with a purpose. The lowest skip rate of any Reel, by a wide margin. Tagged a partner. |
| **Top** | "A little less screen time. A little more sea air." (12 Oct, Mon 19:36) | Reel 9s | 1,182 | 65% | **31** | **8** | A relatable contrast plus a send prompt ("Send this to someone who needs a day by the sea"). Most comments of any post. |
| **Top** | Filoxenia kitchen, finishing touches (13 Nov, Fri 17:32) | Reel 6s | 552 | 54% | 2 | 4 | A process shot that people rewatched (119% average watched). The best November post by far. |
| Bottom | "Even the walls have a sea view" (19 Nov, Thu 11:32) | Reel 8s | 53 | 74% | 0 | 0 | A static detail, posted at midday on a Thursday. |
| Bottom | Thalassa lunch (17 Oct, Sat 08:30) | Single image | 29 | n/a | 0 | 0 | A photo with an ambient statement, posted Saturday morning. |
| Bottom | Mel's Kippentrap (8 Nov, Sun 12:33) | Carousel | 20 | n/a | 24* | 0 | 4 profile visits but 0 follows. *Seeded shares. |

### Patterns in Reel retention

| Signal | Spearman correlation with reach (n=15) | Reading |
|---|---|---|
| Skip rate (first 3 seconds) | **−0.46** | The strongest lever. Reels with skip rate under 55% have a median reach of **380**; at 55% or above it is **182**. Only 2 of 15 Reels held skip rate under 50%. |
| Duration | +0.39 | The November plan's rule of 6–10 seconds did not hold up. The best Reel was 15s, and November's 8s Reels had the worst median reach (118). |
| Average % watched | −0.21 | Not useful on its own: very short clips loop past 100%. Use average watch time in seconds, or completion, instead. |

### Caption, CTA and hashtag patterns

| Feature | Finding |
|---|---|
| CTA: "Send this to… / Tag your…" (n=5) | Highest median reach (182) and the most comments (9). This is the right CTA family. |
| CTA: "Save this…" (n=2) | Median reach 42 and **0 saves**. Asking for a save doesn't work if the content isn't worth saving. |
| CTA: question (n=10) | 9 comments in total. Specific questions ("What's the oddest thing you've found on a beach?") beat generic ones ("Who's joining you?"). |
| Mentions the pass, deal or € (n=8) | Median reach 110 vs 140 without, and lower ER. Keep selling for the end card or the Stories, not the hook. |
| Caption length | No clear effect; 31–45 words is the norm. |
| Hashtags | 2–5 per post, near-zero correlation with reach (ρ = +0.12). Use them for categorisation only. |
| **Language** | **0 of 24 captions are in Dutch.** |

### Days and times (Europe/Amsterdam)

- **Evening 17:00–19:00 (n=13): median reach 182.** Morning before 11:00 (n=6): 94. Midday 11:00–14:00 (n=3): 53. Afternoon 14:00–17:00 (n=2): 114.
- All three top Reels went out Friday or Monday between 17:30 and 19:40. Midday slots were planned eight times in November but used only twice (8 Nov 12:33 and 19 Nov 11:32), and both were among the weakest posts.
- **Metricool's general curve** peaks at 10:00 and 18:00 on weekdays (Tue–Fri strongest), and weekend values are about half of weekday values. This agrees with the account data on evenings. The 10:00 slot has never been tested on a Reel, so it's in the test backlog.
- Caveat: time is mixed up with format and month. Evenings were mostly October/November Reels, and mornings were mostly the September launch posts.

---

## 2. Plan vs reality

### The November plan (2–29 Nov) against what was published

| Plan # | Planned | Published | Reach | Plan's own test → result |
|---|---|---|---|---|
| 01 Take your break outside | Mon 2 Nov 12:00 | Mon 2 Nov **17:18** | 102 | "Can an invitation repeat the coastal Reel's sharing?" **No:** 0 shares, 82% skip (worst in November). |
| 02 What is that on the beach | Wed 4 Nov 18:30 | Wed 4 Nov 18:30 | 116 | Re-ran the beachcombing win. **Novelty fell off:** 116 reach vs 1,935 in October. |
| 03 Not Delft but Zandvoort | Fri 6 Nov 12:00 | **Sun 8 Nov 12:33** (Mel's) | 20 | Slipped to a weekend midday slot: lowest reach on the account. |
| 04 Coastal hair | Mon 9 Nov 18:30 | Mon 9 Nov 18:30 | 182 | Humour hook, but 0 shares. A send prompt on a weak payoff doesn't produce sends. |
| 05 Women who walked to Haarlem | Wed 11 Nov 12:00 | Wed 11 Nov 17:10 | 72 | Low reach, but **1 follow** (1.4 per 100 reached, the best follow rate on the account). |
| 06 Finishing touches | Fri 13 Nov 18:30 | Fri 13 Nov 17:32 | **552** | "Humour and preparation vs static atmosphere": **preparation won clearly.** |
| 07 Look up | Mon 16 Nov 18:30 | Mon 16 Nov 18:36 | 118 | "Wonder" lost: 1 like, 0 shares. |
| 08 Even the walls have a sea view | Wed 18 Nov 18:30 | **Thu 19 Nov 11:32** | 53 | Slipped to a midday slot; second-lowest Reel. |
| 09 Two pours and a colour change | Fri 20 Nov 12:00 | **Not published** | – | Visible transformation, the one action idea in week 3, didn't go out. It's moved into the new calendar. |
| 10–12 | 23–27 Nov | Pending | – | 11 and 12 are kept in the new calendar. |

**Execution: 8 of 9 posts due by 20 Nov were published (89%).** The weak points were slots slipping (3 of 8 moved, mostly to weaker times) and a strategic bet that didn't pay off. The plan said "start with the moment", which in practice meant short ambient clips. Its own best evidence pointed the other way, towards **action, purpose and process**.

### The September plan
Four brand-statement posts (launch video, impact carousel, "spots that made the cut", World Cleanup Day). They drew **0 organic shares and 0 comments**. Explaining the brand does not reach strangers.

### Pillar balance: what's over-used and what's under-used

| Pillar (tagged from captions) | Share of posts | Share of reach | Reach index | Verdict |
|---|---|---|---|---|
| Impact & beachcombing (Juttersgeluk, CleanHub) | 17% | **41%** | **2.4** | **Under-used winner.** Action with a purpose is the account's strongest theme. |
| Coastal mood | 17% | 25% | 1.5 | Works only with a relatable contrast plus a send prompt (12 Oct). Ambient versions (2 and 16 Nov) failed. |
| Product explainer / brand statement | 17% | 11% | 0.7 | Low reach, no comments. Move it to Stories and Highlights. |
| **Partner venue** | **33%** | 19% | **0.6** | **Over-used and under-performing.** Ambient venue posts ("A seat by the fire…", "Good food. Time to enjoy it.") have a median reach of **43**. The exception is process content (Filoxenia kitchen, 552). |
| Village discovery / heritage | 8% | 2% | 0.2 | Low reach, but **1 of only 3 recorded follows.** A good converter; run it as carousels. |
| Relatable humour | 8% | 2% | 0.2 | Low reach (carousels), but **2 of 3 recorded follows** and the most profile visits per post. A hidden winner, worth trying as Reels. |

**Hidden winners:** (1) a visible action with a purpose (beachcombing), (2) process and behind-the-counter footage, (3) relatable humour, which brings follows.
**Over-used:** ambient venue atmosphere, generic "discover local favourites" sign-offs, and English-only brand statements.

---

## 3. Fit with the local Dutch market

| Local fact (Zandvoort profile, brand guide) | Current messaging | Gap → action |
|---|---|---|
| **~85% of residents have a Dutch background**; day-trippers come mainly from Haarlem and Amsterdam; the brand guide itself is written in Dutch | 100% English captions and overlays | **Major gap.** Switch to Dutch first with a one-line English summary. The NL vs EN test is set up to confirm this (demographics unlock at 100 followers). |
| 27–28% of residents are 65+ (national average ~21%), but Instagram's biggest group is 25–34 and 55% female | Content aimed at a generic "traveller" | Aim Instagram at **25–44 day-trippers and locals planning a weekend**. Reach older locals through partners and Facebook, not Instagram. |
| Off-season: the town calls the low season "saai" (dull), and many seasonal beach pavilions close in winter | Coastal clips with no time context | Own the **winter** coast: uitwaaien (a bracing walk in the wind), storm-finds beachcombing, indoor spots that stay open, the short days. Give people a reason to come *now*. |
| Dutch daily life runs on WhatsApp, Buienradar (rain radar), NS trains and Tikkie | Generic sign-offs | Use these as cultural references: send prompts ("stuur naar je groepsapp", send it to your group chat), Buienradar-proof plans, the train from Amsterdam or Haarlem. |
| 2026 was the **last Dutch Grand Prix**; the town is moving towards business visitors and the off-season | Not mentioned | Opportunity: "Zandvoort after the F1". The local story is the village and coast that were there before and remain after. Tier 2 sensitivity: no F1 branding. |
| Dutch consumer psychology: directness, plain sobriety ("nuchterheid"), dislike of hype; anchoring on a clear price works | Taglines such as "Explore more. Spend less. Make an impact." and "real deals" | Lead with concrete facts: €10, valid one year, a named deal (10% / €10 off / 2-for-1, per partner). No superlatives, no fake scarcity. Black Friday is a chance to stand out by **not** shouting. |
| Brand voice: "Fris in uitstraling, lokaal in selectie, menselijk in toon en doelgericht in impact" (fresh in look, local in selection, human in tone, purposeful in impact) | Human tone is good; "local" is generic | The tone holds up. Make "local" specific with names, streets and people (Kerkstraat, Kippentrap, Boulevard de Favauge, the fish women). |

---

## Keep / kill / refresh (`content-audit`)

- **Keep and scale:** action-with-purpose Reels (beachcombing), process Reels (kitchen, counter), relatable-contrast Reels with a send prompt, heritage carousels (for follows).
- **Refresh:** venue posts (turn atmosphere into process, a person or a situation), the how-it-works explainer (re-cut as a Dutch Story Highlight), humour (move from carousel to Reel).
- **Stop:** ambient one-line Reels with nothing happening in them, "Save this" on content that isn't saveable, single images, weekend-midday slots, and mass-DMing posts within the team without logging it, which spoils the share data. Nothing needs deleting.

## Quick wins (this week)
1. Rename the profile from "Lou" to **"LookyBooky Zandvoort"**. Rewrite the bio in Dutch with a short English line and the concrete offer (draft in the strategy). Add a UTM to the bio link.
2. Create Highlights: "Zo werkt het" (how it works), "Open in de winter" (open in winter), "Impact".
3. In Metricool, set the brand timezone to Europe/Amsterdam.
4. Start logging every internal or partner DM send of a post.
