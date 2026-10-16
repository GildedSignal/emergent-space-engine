#!/usr/bin/env python3
"""(lab 20261016-0117-second-…-d86c) Baseline-vs-deletion comparison, judged against the
pre-registered rules in predictions.md (D1 digests, D2 degradation, D3 the standing cut).

usage: compare.py <floor-on.log> <floor-off.log>
"""
import math
import sys

C_LS = 299_792_458.0  # m per light-second


def parse(path):
    cuts = {}  # game_s -> {"digest", "S": {id: (kind, ox, oy, ls, ang, shift)}, "census", "reads"}
    for line in open(path):
        if line.startswith("cut game_s="):
            game_s = float(line.split("=", 1)[1].split()[0])
            digest = line.split("digest=")[1].split()[0]
            cuts[game_s] = {"digest": digest, "S": {}, "census": line.strip(), "reads": ""}
        elif line.startswith("   reads:") and cuts:
            cuts[max(cuts)]["reads"] = line.strip()
        elif line.startswith("S "):
            _, game_s, sid, kind, ox, oy, ls, ang, shift = line.split()
            cuts.setdefault(float(game_s), {"digest": "?", "S": {}, "census": "", "reads": ""})
            cuts[float(game_s)]["S"][int(sid)] = (int(kind), float(ox), float(oy), float(ls), float(ang), float(shift))
    return cuts


def segs_of(cuts):
    """segs/body per cut, from the census line."""
    out = {}
    for game_s, c in cuts.items():
        for tok in c["census"].split("segs ")[1].split("/body")[0].split():
            try:
                out[game_s] = float(tok)
                break
            except ValueError:
                continue
    return out


def main():
    on, off = parse(sys.argv[1]), parse(sys.argv[2])
    d1 = True  # digests identical everywhere
    d2 = True  # no vanished emitter, every disc body's shift inside its own disc
    hdr = (
        f"{'cut':>7} | digest | seen on/off/both | vanish | maxShift(ls) | maxShift(m) | p99(m)"
        f" | >own disc | fleetMax(m)"
    )
    print(hdr)
    for game_s in sorted(set(on) & set(off)):
        a, b = on[game_s], off[game_s]
        same = a["digest"] == b["digest"]
        d1 &= same
        ids_a, ids_b = set(a["S"]), set(b["S"])
        both = ids_a & ids_b
        vanished, appeared = len(ids_a - ids_b), len(ids_b - ids_a)
        shifts, over, fleet_max = [], 0, 0.0
        for sid in both:
            ka, xa, ya, la, ang_a, _ = a["S"][sid]
            _, xb, yb, _, _, _ = b["S"][sid]
            d = math.hypot(xa - xb, ya - yb)
            if ka == 4:
                # A fleet member is a point light extrapolated from the battle's committed tick,
                # not a disc: reported separately, never bounded by a radius.
                fleet_max = max(fleet_max, d)
                continue
            shifts.append(d)
            r_ls = math.tan(ang_a) * abs(la)  # the body's own radius, in light-seconds
            if d > r_ls:
                over += 1
        shifts.sort()
        n = max(len(shifts) - 1, 0)
        mx = shifts[-1] if shifts else 0.0
        p99 = shifts[int(0.99 * n)] if shifts else 0.0
        d2 &= (vanished == 0) and (over == 0)
        print(
            f"{game_s:>7.0f} | {'SAME' if same else 'DIFF'} | {len(ids_a)}/{len(ids_b)}/{len(both)} | {vanished}+{appeared}"
            f" | {mx:.3e} | {mx * C_LS:.3g} | {p99 * C_LS:.3g} | {over} | {fleet_max * C_LS:.3g}"
        )
    sa, sb = segs_of(on), segs_of(off)
    on_s = " ".join("%dk:%.3f" % (g / 1000, sa[g]) for g in sorted(sa))
    off_s = " ".join("%dk:%.3f" % (g / 1000, sb[g]) for g in sorted(sb))
    print(f"\nsegs/body floor-on:  {on_s}")
    print(f"segs/body floor-off: {off_s}")
    steady = [g for g in sorted(set(sa) & set(sb)) if g >= 32_000]
    d3 = None
    if steady:
        g = steady[-1]
        ratio = sa[g] / max(sb[g], 1e-9)
        d3 = sb[g] <= 0.15
        print(f"standing cut at {g:.0f}s: {sa[g]:.3f} -> {sb[g]:.3f} segs/body ({ratio:.1f}x); D3 (<=0.15/body): {'HOLDS' if d3 else 'FAILS'}")
    print(f"D1 digests identical: {'YES' if d1 else 'NO'}")
    print(f"D2 bounded degradation: {'YES' if d2 else 'NO'}")
    verdict = "adopt" if (d1 and d2 and d3) else ("blocked (outcome-free, view blocked)" if d1 else "refuted (floor is law)")
    print(f"VERDICT: {verdict}")


if __name__ == "__main__":
    main()
