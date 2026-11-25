"""Flatten vidIQ Instagram owner-insights media export into a per-post CSV."""
import json, sys, csv
src, dst = sys.argv[1], sys.argv[2]
d = json.load(open(src))
rows = []
for m in d["data"]:
    ins = {}
    for x in (m.get("insights") or {}).get("data", []):
        v = x.get("values", [{}])[0].get("value")
        if v is None and "total_value" in x: v = x["total_value"].get("value")
        ins[x["name"]] = v
    rows.append({
        "id": m["id"], "timestamp_utc": m["timestamp"], "media_type": m["media_type"],
        "product_type": m.get("media_product_type"), "permalink": m["permalink"],
        "n_children": len((m.get("children") or {}).get("data", [])) if isinstance(m.get("children"), dict) else len(m.get("children") or []),
        "caption": (m.get("caption") or "").replace("\n", " \\n "),
        **{k: ins.get(k) for k in ["views","reach","likes","comments","shares","saved","total_interactions"]},
    })
with open(dst, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(len(rows), "rows")
