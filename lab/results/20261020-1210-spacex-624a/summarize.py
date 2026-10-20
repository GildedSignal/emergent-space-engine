#!/usr/bin/env python3
"""Dossier numbers from the three census arms + digest-neutrality check."""
import json, sys, os

RUN = os.path.dirname(os.path.abspath(__file__))

def load(p):
    return json.load(open(p))

ok = True
print("== digest neutrality (patched vs pristine; the end-state digest must match bit for bit) ==")
for a in ["default", "fleet", "seed3"]:
    r = load(f"{RUN}/work/ref-{a}.json")
    c = load(f"{RUN}/work/cen-{a}.json")
    same = r["digest"] == c["digest"]
    ok &= same
    print(f"  {a:8s} state_digest_match={same} replay_digest pristine={r['replay_digest'][:16]} patched={c['replay_digest'][:16]}"
          f" (build-sensitive: stable per binary, shifts with any crates/space codegen change;"
          f" the end-state digest is the physics identity) refused={c['refused']}"
          f" kicks(made/leavers)={c['kick_us']['samples']}/{c['kick_us_leavers']['samples']}")
print("\n== per-mint span coverage: panels landed in / compiled panels ==")
for a in ["default", "fleet", "seed3"]:
    rows = load(f"{RUN}/work/cen-{a}.json")["mint_census"]["rows"]
    print(f"-- arm {a} ({len(rows)} mints)")
    for cls in ["cycle", "passage"]:
        rs = [r for r in rows if r["class"] == cls]
        panels = sum(max(r["knots"] - 1, 0) for r in rs)
        touched = sum(r["touched"] for r in rs)
        knots = sum(r["knots"] for r in rs)
        walks = sorted(r["touched"] / max(r["knots"] - 1, 1) for r in rs)
        ge90 = sum(w >= 0.9 for w in walks)
        big = [r for r in rs if r["knots"] >= 100]
        bigw = sorted(r["touched"] / max(r["knots"] - 1, 1) for r in big) or [0]
        print(f"  {cls:8s} mints={len(rs):6d} knots={knots:8d} never-landed={1-touched/panels:6.1%}"
              f" cov_median={walks[len(walks)//2]:6.1%} cov_p90={walks[int(len(walks)*0.9)]:6.1%}"
              f" ge0.9={ge90}")
        if big:
            print(f"           big(>=100kn): {len(big)} mints, {sum(r['knots'] for r in big)} knots,"
                  f" cov_median={bigw[len(bigw)//2]:6.1%} cov_max={bigw[-1]:6.1%}")

print("\n== top-decile lifetime mints (most readouts) ==")
rows = load(f"{RUN}/work/cen-fleet.json")["mint_census"]["rows"]
for cls in ["cycle", "passage"]:
    rs = sorted([r for r in rows if r["class"] == cls], key=lambda r: -r["touches"])
    top = rs[: len(rs) // 10]
    w = sorted(r["touched"] / max(r["knots"] - 1, 1) for r in top)
    print(f"  {cls:8s} median touches={sorted(r['touches'] for r in top)[len(top)//2]}"
          f" median coverage={w[len(w)//2]:.1%}")

sys.exit(0 if ok else 1)
