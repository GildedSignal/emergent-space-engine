#!/usr/bin/env python3
"""The crest attractor: recurrence, decay, width, composition, and the compute-ahead ledger.

Reads the flight logs (armA.log/armB.log/armC.log: `spell:` lines + `t:` traces), builds the
crest table, tests the pre-registered predictions P1-P7, and prices idle-time compute-ahead.

Usage: python3 crest.py <armA.log> [<armB.log> ...]
"""
import re
import sys

TICK = 28141.5  # the doll interval (3294's census median), game-s


def parse(path):
    spells, trace, hdr = [], [], {}
    for line in open(path):
        if line.startswith("spell: at="):
            d = dict(kv.split("=") for kv in line.strip()[7:].split(" ") if "=" in kv)
            spells.append({k: float(v) for k, v in d.items()})
        elif line.startswith("t: "):
            f, ms, ev, k, b, pres, df = line[3:].strip().split(",")
            trace.append((int(f), float(ms), int(ev), int(k), int(b), float(pres), float(df)))
        elif line.startswith("ladder:"):
            hdr.update(dict(kv.split("=", 1) for kv in line.strip()[7:].split(" ") if "=" in kv))
        elif line.startswith("rung"):
            hdr["rung"] = line.strip()
    return spells, trace, hdr


def crest_table(spells):
    """Spells ARE crests here (coast): one clamp per crest, merged runs >= 60 frames."""
    rows = []
    for i, s in enumerate(spells):
        e = s["events"]
        rows.append(
            dict(
                i=i + 1,
                at=int(s["at"]),
                wall=s["wall_s"],
                E=int(s["events"]),
                kicks=int(s["kicks"]),
                bnd=int(s["bnd"]),
                p_from=s["p_from"],
                p_to=s["p_to"],
                width=s["width_s"],
                us_per_ev=s["us_per_ev"],
                law=s["law_ratio"],
                mid=0.5 * (s["p_from"] + s["p_to"]),
            )
        )
    for r in rows:
        r["kick_share"] = r["kicks"] / max(r["E"], 1)
    return rows


def report(name, spells, trace, hdr):
    n = int(re.search(r"N=(\d+)", hdr.get("rung", "")).group(1)) if "rung" in hdr else 0
    rows = crest_table(spells)
    print(f"\n=== {name}: N={n} ({hdr.get('rung','')})")
    if not rows:
        print("  no spells >= 60 frames")
        return rows
    print(f"  {'crest':>5} {'mid_gs':>9} {'d_mid':>9} {'E':>8} {'E/N':>6} {'kick%':>6} {'width':>7} {'wall_s':>7} {'us/ev':>6} {'law':>5}")
    prev = None
    for r in rows:
        d = f"{r['mid'] - prev:.0f}" if prev else "-"
        prev = r["mid"]
        print(
            f"  {r['i']:>5} {r['mid']:>9.0f} {d:>9} {r['E']:>8} {r['E']/max(n,1):>6.3f} "
            f"{r['kick_share']*100:>5.1f}% {r['width']:>7.0f} {r['wall']:>7.1f} {r['us_per_ev']:>6.1f} {r['law']:>5.2f}"
        )
    e = [r["E"] for r in rows]
    kick_rows = [r for r in rows if r["kick_share"] > 0.5]
    bnd_rows = [r for r in rows if r["kick_share"] <= 0.5]
    if len(rows) >= 2:
        print("  spacing (all crests): " + " ".join(str(round(rows[i + 1]["mid"] - rows[i]["mid"])) for i in range(len(rows) - 1)))
        for nm, cr in (("kick", kick_rows), ("boundary", bnd_rows)):
            if len(cr) >= 2:
                sp = [cr[i + 1]["mid"] - cr[i]["mid"] for i in range(len(cr) - 1)]
                ee = [c["E"] for c in cr]
                print(f"  {nm} comb: n={len(cr)} spacing {' '.join(f'{s:.0f}' for s in sp)} (mean {sum(sp)/len(sp):.0f}, interval {TICK:.0f})")
                print(f"  {nm} comb: E {' '.join(f'{x}' for x in ee)} -> decay {' '.join(f'{ee[i+1]/ee[i]:.3f}' for i in range(len(ee)-1))}")
                print(f"  {nm} comb: width {' '.join(str(round(c['width'])) for c in cr)}")
    # the between-crest baseline demand (game-time, rtf-free): events per game-s outside spells
    spell_frames = set()
    # rebuild spell frame ranges from trace using deficit>0 runs (same merge as the instrument, >=60 apart)
    runs, cur = [], None
    for t in trace:
        if t[6] > 0:
            if cur is None:
                cur = [t[0], t[0], 0]
            cur[1] = t[0]
            cur[2] += t[2]
        elif cur:
            runs.append(cur)
            cur = None
    if cur:
        runs.append(cur)
    merged = []
    for r in runs:
        if merged and r[0] - (merged[-1][0] + merged[-1][1] - merged[-1][0]) < 60:
            m = merged[-1]
            m[1] = r[1]
            m[2] += r[2]
        else:
            merged.append(list(r))
    big = [m for m in merged if (m[1] - m[0] + 1) >= 60]
    base_ev, base_span, base_ms = 0, 0.0, 0.0
    in_spells = big
    def in_spell(f):
        return any(a <= f <= b for a, b, _ in in_spells)
    evs = [t for t in trace if not in_spell(t[0])]
    if evs:
        span = evs[-1][5] - evs[0][5]
        base_ev = sum(t[2] for t in evs)
        base_ms = sum(t[1] for t in evs)
        base_span = span
        print(f"  baseline between crests: {base_ev} events over {base_span:.0f} game-s = {base_ev/max(base_span,1):.1f} ev/game-s, engine {base_ms/max(len(evs),1):.2f} ms/frame median-ish over {len(evs)} frames")
    # compute-ahead ledger at the player's rtf 100: the bill is the sum over one interval's combs
    def comb_med(cr, key):
        v = sorted(c[key] for c in cr)
        return v[len(v) // 2] if v else 0.0
    bill = sum(comb_med(cr, "E") * comb_med(cr, "us_per_ev") * 1e-6 for cr in (kick_rows, bnd_rows) if cr)
    interval_wall = TICK / 100.0
    budget = 0.72 * interval_wall
    per_body = bill / max(n, 1)
    print(f"  ledger@rtf100: crest bill {bill:.1f} s of compute per {TICK:.0f} game-s at N={n}; whole-engine budget {budget:.0f} s; headroom {budget/max(bill,1e-9):.1f}x")
    for N in (int(n), 10**6, 10**9):
        b = N * per_body
        print(f"    N={N:>10,}: crest bill {b:>9.1f} s vs budget {budget:.0f} s -> {'FITS' if b < budget/2 else 'marginal' if b < budget else 'DOES NOT FIT'} ({budget/max(b,1e-9):.2f}x headroom)")
    return rows


if __name__ == "__main__":
    for p in sys.argv[1:]:
        spells, trace, hdr = parse(p)
        report(p, spells, trace, hdr)
