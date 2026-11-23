"""Phase 2 audit: LookyBooky Instagram (vidIQ owner insights export)."""
import pandas as pd, numpy as np, re, sys
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
D = "data/"
p = pd.read_csv(D+"ig_posts.csv", dtype={"id": str})
t = pd.read_csv(D+"post_tags.csv", dtype={"id": str})
r = pd.read_csv(D+"ig_reels_retention.csv", dtype={"id": str})
c = pd.read_csv(D+"ig_feed_conversion.csv", dtype={"id": str})
df = p.merge(t, on="id").merge(r, on="id", how="left").merge(c, on="id", how="left")
assert len(df) == 24
df["ts"] = pd.to_datetime(df.timestamp_utc).dt.tz_convert("Europe/Amsterdam")
df["date"] = df.ts.dt.date; df["dow"] = df.ts.dt.day_name().str[:3]; df["hour"] = df.ts.dt.hour
df["slot"] = pd.cut(df.hour, [0, 11, 14, 17, 24], right=False, labels=["morning <11", "midday 11-14", "afternoon 14-17", "evening 17+"])
df["format"] = df.media_type.map({"VIDEO": "Reel", "CAROUSEL_ALBUM": "Carousel", "IMAGE": "Single image"})
df["age_days"] = (pd.Timestamp("2026-11-23", tz="Europe/Amsterdam") - df.ts).dt.days
df["interactions"] = df[["likes", "comments", "shares", "saved"]].sum(axis=1)
df["er_reach"] = df.interactions / df.reach * 100
df["share_rate"] = df.shares / df.reach * 100
df["save_rate"] = df.saved / df.reach * 100
df["comment_rate"] = df.comments / df.reach * 100
df["views_per_reach"] = df.views / df.reach
cap = df.caption.fillna("").str.replace(r"\\n", " ", regex=True)
df["cap_words"] = cap.str.split().str.len()
df["first_line"] = df.caption.str.split(r"\\n").str[0].str.strip()
df["hook_words"] = df.first_line.str.split().str.len()
df["n_hashtags"] = cap.str.count(r"#\w+")
df["has_question"] = cap.str.contains(r"\?")
def cta(s):
    s = s.lower()
    if "send this" in s or "tag your" in s: return "Send/Tag"
    if "save this" in s: return "Save"
    if "?" in s: return "Question"
    if "bio" in s or "link" in s: return "Link in bio"
    return "None"
df["cta"] = cap.map(cta)
df["mentions_pass_or_deal"] = cap.str.contains(r"pass|€|deal|discount|offer", case=False)
df["dutch_words"] = cap.str.contains(r"\b(de|het|een|en|je|lekker|gezellig|strand|dorp)\b", case=False)
df.to_csv("analysis/ig_posts_enriched.csv", index=False)

def H(x): print("\n" + "=" * 8, x, "=" * 8)
H("ACCOUNT (90d, Meta via vidIQ)")
print("followers 32 | reach 4848 (followers 32 / non-followers 4816 = 99.3% non-follower) | views 9672 | accounts engaged 210 | interactions 896 | profile visits 268 | website taps 7")
print("reach->profile visit %.1f%% | profile visit->link tap %.1f%% | reach->link tap %.2f%%" % (268/4848*100, 7/268*100, 7/4848*100))

H("TOTALS")
print(df[["reach", "views", "likes", "comments", "shares", "saved"]].sum().to_string())
print("median reach", df.reach.median(), "| mean reach %.0f" % df.reach.mean())

H("FORMAT BREAKDOWN")
g = df.groupby("format").agg(n=("id", "size"), med_reach=("reach", "median"), mean_reach=("reach", "mean"),
    med_views=("views", "median"), med_er=("er_reach", "median"), sum_shares=("shares", "sum"),
    sum_saves=("saved", "sum"), med_share_rate=("share_rate", "median"), sum_follows=("follows", "sum"))
print(g.round(1).to_string())
print("\nexcluding possible seeded-share posts:")
print(df[df.possible_seeded_shares == 0].groupby("format").agg(n=("id", "size"), med_reach=("reach", "median"), med_er=("er_reach", "median"), med_share_rate=("share_rate", "median")).round(1).to_string())

cols = ["date", "dow", "hour", "format", "short_name", "pillar", "reach", "views", "er_reach", "shares", "share_rate", "saved", "comments", "avg_watched_pct", "skip_rate_pct", "follows", "possible_seeded_shares"]
n = max(1, round(len(df) * 0.1))  # 10% of 24 => 2; we show top/bottom 3 for readability
for m in ["reach", "er_reach", "share_rate", "comments"]:
    H(f"TOP 3 / BOTTOM 3 by {m}")
    s = df.sort_values(m, ascending=False)
    print(s[cols].head(3).round(1).to_string(index=False)); print("..."); print(s[cols].tail(3).round(1).to_string(index=False))

H("REELS: retention vs reach (Spearman)")
re_ = df[df.format == "Reel"]
for x in ["skip_rate_pct", "avg_watched_pct", "duration_s", "hook_words", "cap_words", "age_days"]:
    print(f"{x:16s} rho={re_[[x,'reach']].corr(method='spearman').iloc[0,1]:+.2f}")
print(re_[["date", "short_name", "duration_s", "reach", "skip_rate_pct", "avg_watched_pct", "share_rate"]].sort_values("reach", ascending=False).round(1).to_string(index=False))
print("median skip rate %.1f%% | median watched %.1f%% | median duration %ds" % (re_.skip_rate_pct.median(), re_.avg_watched_pct.median(), re_.duration_s.median()))

H("PILLAR PERFORMANCE")
pg = df.groupby("pillar").agg(n=("id", "size"), share_of_posts=("id", lambda x: len(x) / len(df) * 100), med_reach=("reach", "median"),
    total_reach=("reach", "sum"), med_er=("er_reach", "median"), shares=("shares", "sum"), comments=("comments", "sum"), follows=("follows", "sum"))
pg["share_of_reach"] = pg.total_reach / df.reach.sum() * 100
pg["index_reach_vs_posts"] = pg.share_of_reach / pg.share_of_posts
print(pg.sort_values("index_reach_vs_posts", ascending=False).round(1).to_string())

H("HOOK TYPE")
print(df.groupby("hook_type").agg(n=("id", "size"), med_reach=("reach", "median"), med_er=("er_reach", "median"), comments=("comments", "sum")).sort_values("med_reach", ascending=False).round(1).to_string())

H("DAY OF WEEK (Amsterdam)")
print(df.groupby("dow").agg(n=("id", "size"), med_reach=("reach", "median"), med_er=("er_reach", "median")).round(1).to_string())
H("TIME SLOT (Amsterdam)")
print(df.groupby("slot", observed=True).agg(n=("id", "size"), med_reach=("reach", "median"), med_er=("er_reach", "median")).round(1).to_string())
print(df[["date", "dow", "hour", "format", "reach"]].sort_values("date").to_string(index=False))

H("CAPTION FEATURES")
print(df.groupby("cta").agg(n=("id", "size"), med_reach=("reach", "median"), med_er=("er_reach", "median"), med_share_rate=("share_rate", "median"), comments=("comments", "sum")).round(1).to_string())
print(df.groupby("partner_tagged").agg(n=("id", "size"), med_reach=("reach", "median"), med_er=("er_reach", "median")).round(1).to_string())
print(df.groupby("mentions_pass_or_deal").agg(n=("id", "size"), med_reach=("reach", "median"), med_er=("er_reach", "median")).round(1).to_string())
df["words_bin"] = pd.cut(df.cap_words, [0, 30, 45, 200], labels=["<=30", "31-45", ">45"])
print(df.groupby("words_bin", observed=True).agg(n=("id", "size"), med_reach=("reach", "median"), med_er=("er_reach", "median")).round(1).to_string())
print("hashtags: median %d, range %d-%d; rho(hashtags, reach)=%+.2f" % (df.n_hashtags.median(), df.n_hashtags.min(), df.n_hashtags.max(), df[["n_hashtags","reach"]].corr(method="spearman").iloc[0,1]))
print("Dutch-language captions:", int(df.dutch_words.sum()), "of", len(df))

H("TREND: monthly")
df["month"] = df.ts.dt.strftime("%Y-%m")
print(df.groupby("month").agg(n=("id", "size"), reels=("format", lambda x: (x == "Reel").sum()), med_reach=("reach", "median"), total_reach=("reach", "sum")).to_string())
print("\nNov Reels age-adjusted note: most recent 2 posts are <7 days old.")
