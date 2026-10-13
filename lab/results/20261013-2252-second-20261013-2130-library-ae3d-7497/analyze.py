#!/usr/bin/env python3
"""Shape of the per-body kick distribution on shipped scenes (rule 2's falsifier).

Reads kick_tail jsonl dumps. Sets (per the shipped law's own split):
- tube bodies (planets, moon, orbiters, skimmers, the idle player): `step_for`
  cadence, 1/2^step_log2 of their own period -> per-orbit normalization;
- clock bodies (the root-doll haulers; the player under burn): the v2 clock;
- members (bodies the fleet handed out mid-run): rate over their lived seconds.

Shape statistics: shares of the total, max/median, CV, Gini, Zipf rank-size slope.
"""
import json, sys, math

def gini(xs):
    xs = sorted(xs)
    n = len(xs)
    if n == 0 or sum(xs) == 0:
        return 0.0
    cum = sum((2 * (i + 1) - n - 1) * x for i, x in enumerate(xs))
    return cum / (n * sum(xs))

def zipf_slope(counts):
    c = sorted(counts, reverse=True)
    pts = [(math.log(r + 1), math.log(x)) for r, x in enumerate(c) if x > 0]
    if len(pts) < 3:
        return None, None
    n = len(pts)
    sx = sum(p[0] for p in pts); sy = sum(p[1] for p in pts)
    sxx = sum(p[0] ** 2 for p in pts); sxy = sum(p[0] * p[1] for p in pts)
    b = (n * sxy - sx * sy) / (n * sxx - sx * sx)
    a = (sy - b * sx) / n
    ss_tot = sum((p[1] - sy / n) ** 2 for p in pts)
    ss_res = sum((p[1] - (a + b * p[0])) ** 2 for p in pts)
    return b, (1 - ss_res / ss_tot) if ss_tot else 0.0

def stats(name, xs):
    xs = [x for x in xs if x > 0]
    if len(xs) < 3:
        return None
    s = sorted(xs, reverse=True)
    tot = sum(s)
    med = s[len(s) // 2] if len(s) % 2 else (s[len(s) // 2 - 1] + s[len(s) // 2]) / 2
    mean = tot / len(s)
    var = sum((x - mean) ** 2 for x in s) / len(s)
    slope, r2 = zipf_slope(s)
    return {"set": name, "n": len(s), "total": round(tot, 3),
            "top1_share": round(s[0] / tot, 4), "top3_share": round(sum(s[:3]) / tot, 4),
            "top10pct_share": round(sum(s[:max(1, len(s) // 10)]) / tot, 4),
            "max_over_median": round(s[0] / med, 2) if med else None,
            "cv": round(math.sqrt(var) / mean, 3), "gini": round(gini(xs), 3),
            "zipf_slope": round(slope, 3) if slope is not None else None,
            "zipf_r2": round(r2, 3) if r2 is not None else None}

for path in sys.argv[1:]:
    rows, scene = [], None
    for line in open(path):
        d = json.loads(line)
        (rows.append(d) if "scene" not in d else None)
        scene = d if "scene" in d else scene
    tag = path.split("/")[-1].replace(".jsonl", "")
    print(f"\n=== {tag}: {scene['scene']} seed {scene['seed']} members {scene['members']} "
          f"{scene['secs']:.0f} game-s ({scene['wall_s']} s wall) | bodies {scene['bodies']} "
          f"kicks body/origin {scene['kicks_body']}/{scene['origin_kicks']} leavers {scene['leavers']} "
          f"lost {scene['lost']} decisions {scene['decisions']}")
    for r in rows:
        r["lived_s"] = max(r["t_last"] - r["born"], 1) * 4.925490947e-6
        r["rate_lived"] = r["kicks"] / r["lived_s"]
    player = [r for r in rows if r["kind"] == "Player"]
    haulers = [r for r in rows if r["name"].startswith("Hauler")]
    members = [r for r in rows if r["name"].startswith("member")]
    tubes = [r for r in rows if r["group"] == "core" and r["kind"] != "Player"]
    tubes += [r for r in rows if r["name"].split()[0] in ("Orbiter", "Skimmer")]
    sets = [
        ("per-orbit tube (planets,moon,orbiters,skimmers)", [r["kicks_per_orbit"] for r in tubes]),
        ("per-orbit tube + idle player", [r["kicks_per_orbit"] for r in tubes + player]),
        ("per-orbit all bodies", [r["kicks_per_orbit"] for r in rows]),
        ("per-scene-second all bodies", [r["kicks_per_sec"] for r in rows]),
        ("per-lived-second members", [r["rate_lived"] for r in members]),
    ]
    out = {"scene": tag, "seed": scene["seed"], "members": scene["members"], "secs": scene["secs"]}
    for name, xs in sets:
        st = stats(name, xs)
        if st:
            print(f"  {st['set']}: n={st['n']} tot={st['total']} top1={st['top1_share']:.1%} "
                  f"top3={st['top3_share']:.1%} top10%={st['top10pct_share']:.1%} max/med={st['max_over_median']} "
                  f"CV={st['cv']} Gini={st['gini']} Zipf={st['zipf_slope']} (r2={st['zipf_r2']})")
            out[st["set"]] = st
    if player:
        p = player[0]
        tot = sum(r["kicks"] for r in rows)
        print(f"  player: {p['kicks']} kicks = {p['kicks']/tot:.1%} of body kicks; "
              f"{p['kicks_per_orbit']:.1f}/orbit, clock {p['clock']}, sub(level>=1) {p['sub']}")
    print("  top tube bodies by per-orbit:")
    for r in sorted(tubes + player, key=lambda r: -r["kicks_per_orbit"])[:6]:
        print(f"    {r['name']:<12} kicks {r['kicks']:>5} sub {r['sub']:>4} {r['kicks_per_orbit']:>9.2f}/orbit "
              f"{r['kicks_per_sec']:>10.5f}/s")
    if haulers:
        print("  haulers (v2 clock):")
        for r in sorted(haulers, key=lambda r: -r["kicks"]):
            print(f"    {r['name']:<12} kicks {r['kicks']:>5} clock {r['clock']:>5} sub {r['sub']:>4} "
                  f"{r['kicks_per_orbit'] if r['period_ticks'] else 0:>12.2f}/orbit(extrap) {r['kicks_per_sec']:>10.5f}/s")
    with open(path.replace(".jsonl", ".stats.json"), "w") as f:
        json.dump(out, f, indent=1)
