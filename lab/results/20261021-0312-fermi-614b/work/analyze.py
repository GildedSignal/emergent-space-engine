#!/usr/bin/env python3
"""The chain law and the sites, from the census JSONs. Every number the dossier cites."""
import json

ARMS = ["coast-s2-n1e4", "burn-s1-n10000", "burn-s1-n30000", "burn-s1-n100000", "burn-s1-n300000",
        "burn-s1-n10000-30s", "burn-s1-n0-m400", "burn-s1-n1e4-m400"]

def bt(bt: str, n=3):
    fs = [x.strip() for x in bt.split("\n")
          if x.strip() and not x.strip().startswith("at")
          and not any(k in x for k in ("raw_vec", "alloc::", "core::", "census::", "rust"))]
    return " <- ".join(f.split(None, 1)[1] if " " in f else f for f in fs[1:1 + n])

def chains(d):
    """Deduped (site, size) -> (count, first frame, last frame)."""
    out = {}
    for l in d["large"]:
        k = (bt(l["bt"], 1), l["size"])
        c, lo, hi = out.get(k, (0, 1 << 30, -1))
        out[k] = (c + 1, min(lo, l["frame"]), max(hi, l["frame"]))
    return out

print(f"{'arm':20s} {'bodies':>7} {'mem':>4} {'frames':>6} {'game_s':>6} | {'cap_max':>7} {'idx':>5} {'fb':>3} "
      f"{'loop/game-s':>11} {'surv%':>5} | {'large':>5} {'max_B':>8}")
rows = []
for a in ARMS:
    d = json.load(open(f"work/{a}.json"))
    rows.append((a, d))
    lg, m = d["large"], d["arm"].get("members", 48)
    loop, tup, gs = d["capture"]["loop"], d["capture"]["tuples"], max(d["arm"]["game_s_late"], 1e-9)
    print(f"{a:20s} {d['arm']['bodies']:>7} {m:>4} {d['arm']['frames_run']:>6} {round(d['arm']['game_s_late']):>6} | "
          f"{d['capture']['max']:>7} {d['radial']['indexed']:>5} {d['radial']['fallback']:>3} "
          f"{loop / gs:>11.0f} {100 * tup / max(loop, 1):>4.1f}% | {len(lg):>5} {max((l['size'] for l in lg), default=0):>8}")

print("\n[1] Belt-scaled chain: the table crossing at a handout (members 48, belt N). 32.0 B/body exact.")
for a, d in rows:
    n = d["arm"]["bodies"]
    F = {r["f"]: r["ms"] for r in d["frames"]}
    for l in d["large"]:
        if l["size"] == 32 * n:
            print(f"  {a:20s} {l['size']:>9} B = 32.0 B/body at frame {l['frame']:>4}; frames around (us): "
                  f"{[F.get(i) for i in range(l['frame'] - 2, l['frame'] + 2)]} <- {bt(l['bt'], 2)}")

print("\n[2] Fleet-scaled chains (m400 arms): deduped (site, size): count, frames.")
for a, d in rows:
    if d["arm"].get("members", 48) != 400:
        continue
    for (site, size), (c, lo, hi) in sorted(chains(d).items(), key=lambda kv: -kv[0][1])[:6]:
        print(f"  {a:20s} {size:>8} B x{c:>3} (frames {lo}-{hi})  {site[:110]}")

print("\n[3] The capture chain: max content vs arm (fleet-scaled, belt-flat).")
for a, d in rows:
    print(f"  {a:20s} capture.max={d['capture']['max']:>4}  radial ids/capture="
          f"{d['radial']['ids'] / max(d['radial']['indexed'], 1):>6.1f}")

print("\n[4] Rates: leavers (handouts), captures, full-scan weight.")
for a, d in rows:
    gs = max(d["arm"]["game_s_late"], 1e-9)
    st = d.get("stats_end", {})
    print(f"  {a:20s} leavers {st.get('leavers')} in {round(gs)} gs -> {st.get('leavers', 0) / gs:.3f}/gs; "
          f"captures {d['radial']['indexed'] / gs:.2f}/gs; loop iters {d['capture']['loop'] / gs:.0f}/gs")

print("\n[5] The 10^9 composition (copy traffic 2x: read old + write new; bus 60 GB/s).")
for bpb, what in ((496, "recs+info crossing"), (32, "info only")):
    print(f"  {what:18s}: {bpb} B/body -> {2 * bpb * 1e9 / 1e9:.0f} GB traffic -> {2 * bpb * 1e9 / 60e9:.1f} s of bus")
for nn in (1e6, 1e7, 1e8):
    print(f"  crossing at N={nn:.0e}: {2 * 496 * nn / 1e9:>6.2f} GB -> {2 * 496 * nn / 60e9 * 1e3:>5.0f} ms of bus")
