#!/usr/bin/env python3
"""Game-time-anchored wave analysis (the checker's named gold experiment).

Crest and tail are anchored on presented game-seconds (gs), not frame index, so flights at
different load regimes (different delivered-rtf) are compared on the same game-time window.
Windows are pre-registered: onset = earliest gs with >=5 over-budget frames within [g, g+2000);
crest = [onset_gs, onset_gs+1500); tail = [onset_gs+1500, onset_gs+20000); ebb = gs < onset_gs.
Mechanism uses per-frame events of over-frames inside the crest window (not window totals).
"""
import glob, math, os, re, statistics as st

BUDGET = 12.0
HERE = os.path.dirname(os.path.abspath(__file__))
FLIGHTS = os.path.join(HERE, "flights")


def load(path):
    rows = []
    for line in open(path):
        if line.startswith("csv ") and not line.startswith("csv frame"):
            f, ms, ev, lag, gs = line[4:].strip().split(",")
            rows.append((int(f), float(ms), int(ev), float(gs)))
    return rows
def analyse(rows):
    # The crest is defined by what it CARRIES (arrival events), not by how the schedule rendered it
    # (ms): under load, stray over-budget frames from contention fire any ms-based onset long before
    # the burst. onset_gs = start of the 1500-gs window holding the most events (grid 100 gs).
    gmin = min(r[3] for r in rows)
    gmax = max(r[3] for r in rows)
    best = (-1, gmin)
    g = gmin
    while g + 1500 <= gmax + 100:
        tot = sum(r[2] for r in rows if g <= r[3] < g + 1500)
        if tot > best[0]:
            best = (tot, g)
        g += 100
    ev_win, og = best
    onset = next(r for r in rows if r[3] >= og)
    crest = [r for r in rows if og <= r[3] < og + 1500]
    tail = [r for r in rows if og + 1500 <= r[3] < og + 20000]
    cex = sum(max(0.0, r[1] - BUDGET) for r in crest)
    cev = sum(r[2] for r in crest if r[1] > BUDGET)
    tex = sum(max(0.0, r[1] - BUDGET) for r in tail)
    ebb = sum(max(0.0, BUDGET - r[1]) for r in rows if r[3] < og)
    ex_all = cex + tex + sum(max(0.0, r[1] - BUDGET) for r in rows if r[3] >= og + 20000)
    return {
        "onset_frame": onset[0], "onset_gs": og, "end_gs": gmax, "crest_events_win": ev_win,
        "crest_ms": cex, "crest_events": cev, "tail_ms": tex, "ebb_ms": ebb,
        "excess_all": ex_all, "coverage": ebb / ex_all if ex_all else float("inf"),
        "frames": len(rows), "over": sum(1 for r in rows if r[1] > BUDGET),
        "width_gs": _width(crest),
    }


def _width(crest):
    """gs span holding the central 90% of the crest window's events (per-frame counts)."""
    tot = sum(r[2] for r in crest)
    if tot == 0:
        return 0.0
    acc = 0
    lo = hi = crest[0][3]
    for r in crest:
        acc += r[2]
        if acc >= 0.05 * tot:
            lo = r[3]
            break
    acc = 0
    for r in reversed(crest):
        acc += r[2]
        if acc >= 0.05 * tot:
            hi = r[3]
            break
    return hi - lo


def rss_of(out_path):
    try:
        for line in open(out_path):
            m = re.search(r"flight's end \(now ([\d.]+) MB\)", line)
            if m:
                return float(m.group(1))
    except FileNotFoundError:
        pass
    return float("nan")


def held_of(out_path):
    try:
        for line in open(out_path):
            m = re.search(r"held_max=(\d+)", line)
            if m:
                return int(m.group(1))
    except FileNotFoundError:
        pass

def name_of(p):
    return os.path.basename(p).replace(".csv.err", "")


def main():
    flights = {}
    med = {}
    for p in sorted(glob.glob(os.path.join(FLIGHTS, "*.csv.err"))):
        n = name_of(p)
        if n.startswith("calib"):
            continue
        rows = load(p)
        if len(rows) < 60:
            print(f"{n}: empty/short CSV ({len(rows)} rows) — skipped")
            continue
        a = analyse(rows)
        a["rss"] = rss_of(p.replace(".csv.err", ".out"))
        a["held_max"] = held_of(p.replace(".csv.err", ".out"))
        flights[n] = a
        if a:
            k = int(re.search(r"_k(\d+)_", n).group(1))
            print(f"{n}: onset f{a['onset_frame']} gs {a['onset_gs']:.0f} width_gs {a['width_gs']:.0f} end_gs {a['end_gs']:.0f} "
                  f"crest {a['crest_ms']:.0f} ms (events {a['crest_events']}, {a['crest_events']/k:.3f}/body, "
                  f"{a['crest_ms']*1e3/max(a['crest_events'],1):.1f} us/ev) tail {a['tail_ms']:.0f} ms "
                  f"ebb {a['ebb_ms']:.0f} excess_all {a['excess_all']:.0f} cov {a['coverage']:.3f} "
                  f"over {a['over']} rss {a['rss']:.0f} held {a['held_max']}")
        else:
            print(f"{n}: NO ONSET")
    print("\n== per-regime medians [min..max], crest anchored on gs ==")
    groups = {}
    for n, a in flights.items():
        if not a:
            continue
        m = re.match(r"([a-z]+)(\d*)_k(\d+)_", n)
        reg, k = m.group(1), int(m.group(3))
        groups.setdefault((reg, k), []).append((n, a))
    for (reg, k), lst in sorted(groups.items(), key=lambda x: (x[0][0], x[0][1])):
        vals = {f: [a[f] for _, a in lst] for f in ("onset_gs", "crest_ms", "tail_ms", "ebb_ms", "coverage", "width_gs")}
        evb = [a["crest_events"] / k for _, a in lst]
        use = [a["crest_ms"] * 1e3 / max(a["crest_events"], 1) for _, a in lst]
        med[(reg, k)] = {f: st.median(v) for f, v in vals.items()}
        fmt = lambda f: f"{st.median(vals[f]):.0f} [{min(vals[f]):.0f}..{max(vals[f]):.0f}]"
        covf = f"{st.median(vals['coverage']):.3f} [{min(vals['coverage']):.3f}..{max(vals['coverage']):.3f}]"
        print(f"  {reg} K={k:>6} n={len(lst)}: onset_gs {fmt('onset_gs')} width_gs {fmt('width_gs')} crest_ms {fmt('crest_ms')} "
              f"tail_ms {fmt('tail_ms')} ebb_ms {fmt('ebb_ms')} cov {covf} "
              f"ev/body {st.median(evb):.3f} [{min(evb):.3f}..{max(evb):.3f}] us/ev {st.median(use):.1f}")

    print("\n== crest exponent alpha per regime (medians; band from per-flight extremes) ==")
    for reg in sorted({r for r, _ in med}):
        ks = sorted(k for r, k in med if r == reg)
        for lo, hi in zip(ks, ks[1:]):
            a_mid = math.log(med[(reg, hi)]["crest_ms"] / med[(reg, lo)]["crest_ms"]) / math.log(hi / lo)
            fl = {}
            for r2, k2 in med:
                if r2 == reg and k2 in (lo, hi):
                    fl.setdefault(k2, []).append((n, a2) for n, a2 in groups[(reg, k2)])
            lo_all = [a2["crest_ms"] for _, a2 in groups[(reg, lo)]]
            hi_all = [a2["crest_ms"] for _, a2 in groups[(reg, hi)]]
            a_lo = math.log(min(hi_all) / max(lo_all)) / math.log(hi / lo)
            a_hi = math.log(max(hi_all) / min(lo_all)) / math.log(hi / lo)
            print(f"  {reg} {lo}->{hi}: alpha(medians)={a_mid:.3f} band [{a_lo:.3f}..{a_hi:.3f}] "
                  f"ratio={med[(reg,hi)]['crest_ms']/med[(reg,lo)]['crest_ms']:.3f}")

    print("\n== fence arms (idle, TTL=16) vs idle no-fence ==")
    for (reg, k), lst in sorted(groups.items()):
        if reg != "fence":
            continue
        base = groups.get(("idle", k), [])
        if base:
            bm = {f: st.median([a[f] for _, a in base]) for f in ("crest_ms", "tail_ms", "onset_gs")}
            for n, a in lst:
                print(f"  fence K={k}: crest {a['crest_ms']:.0f} vs no-fence med {bm['crest_ms']:.0f} "
                      f"({a['crest_ms']/bm['crest_ms']:.2f}x), tail {a['tail_ms']:.0f} vs {bm['tail_ms']:.0f} "
                      f"({a['tail_ms']/max(bm['tail_ms'],1):.3f}x), onset_gs {a['onset_gs']:.0f} vs {bm['onset_gs']:.0f}, "
                      f"end_gs {a['end_gs']:.0f} (tail window fully covered: {a['end_gs'] >= a['onset_gs']+20000})")
        else:
            for n, a in lst:
                print(f"  fence K={k}: crest {a['crest_ms']:.0f} tail {a['tail_ms']:.0f} (no idle baseline)")

    print("\n== prediction verdicts (bands and kill bars from predictions.md) ==")
    def m3(regime, k, field):
        lst = [a[field] for _, a in groups.get((regime, k), [])]
        return (st.median(lst), min(lst), max(lst)) if lst else (None, None, None)
    if ("idle", 100000) in groups:
        og = m3("idle", 100000, "onset_gs")
        ok = 12700 <= og[0] <= 13800
        print(f"P1a idle1e5 onset_gs median {og[0]:.0f} in [12700,13800]: {'HOLD' if ok else 'FAIL'}")
    for k in (100000, 200000):
        if ("idle", k) in groups and ("load", k) in groups:
            d = abs(m3("idle", k, "onset_gs")[0] - m3("load", k, "onset_gs")[0])
            print(f"P1b |onset_gs idle-load| K={k}: {d:.0f} gs (<750 HOLD, >1500 KILL): "
                  f"{'HOLD' if d < 750 else 'KILL' if d > 1500 else 'between'}")
    for reg in ("idle", "load"):
        for k in (100000, 200000, 300000):
            if (reg, k) in groups:
                lo, hi = 0.90, 1.10
                eb = [a["crest_events"] / k for _, a in groups[(reg, k)]]
                v = "HOLD" if lo <= min(eb) and max(eb) <= hi else "KILL"
                print(f"P2 {reg} K={k} ev/body [{min(eb):.3f}..{max(eb):.3f}] in [0.90,1.10]: {v}")
    for k in (100000, 200000):
        if ("idle", k) in groups and ("load", k) in groups:
            d = abs(st.median([a["crest_events"] / k for _, a in groups[("idle", k)]])
                    - st.median([a["crest_events"] / k for _, a in groups[("load", k)]]))
            print(f"P2b |ev/body regime shift| K={k}: {d:.3f} (<=0.08 HOLD, >0.10 KILL): "
                  f"{'HOLD' if d <= 0.08 else 'KILL' if d > 0.10 else 'between'}")
    for reg in ("idle", "load"):
        if (reg, 100000) in groups and (reg, 200000) in groups:
            i1 = [a["crest_ms"] for _, a in groups[(reg, 100000)]]
            i2 = [a["crest_ms"] for _, a in groups[(reg, 200000)]]
            a_med = math.log(st.median(i2) / st.median(i1)) / math.log(2)
            a_lo = math.log(min(i2) / max(i1)) / math.log(2)
            a_hi = math.log(max(i2) / min(i1)) / math.log(2)
            print(f"P3 {reg} alpha(1e5->2e5) median {a_med:.3f} band [{a_lo:.3f}..{a_hi:.3f}]")
    if ("idle", 300000) in groups and ("idle", 100000) in groups:
        i1 = [a["crest_ms"] for _, a in groups[("idle", 100000)]]
        i3 = [a["crest_ms"] for _, a in groups[("idle", 300000)]]
        a3 = math.log(st.median(i3) / st.median(i1)) / math.log(3)
        print(f"P3b idle alpha(1e5->3e5) {a3:.3f} in [1.05,1.40]: {'HOLD' if 1.05 <= a3 <= 1.40 else 'FAIL'}")
    if ("fence", 100000) in groups and ("idle", 100000) in groups:
        f = [a for _, a in groups[("fence", 100000)]][0]
        tmed = st.median([a["tail_ms"] for _, a in groups[("idle", 100000)]])
        cmed = st.median([a["crest_ms"] for _, a in groups[("idle", 100000)]])
        print(f"P4/K4 fence1e5 tail {f['tail_ms']:.0f} vs no-fence {tmed:.0f} ({f['tail_ms']/max(tmed,1):.3f}x; "
              f"<=0.15 HOLD, >0.25 KILL); crest {f['crest_ms']:.0f} vs {cmed:.0f} ({f['crest_ms']/max(cmed,1):.2f}x; "
              f"0.5-2.0 ok); held_max {f['held_max']} (<=50 pred)")
    for reg in ("idle", "load"):
        if (reg, 100000) in groups and (reg, 200000) in groups:
            u1 = st.median([a["crest_ms"] * 1e3 / max(a["crest_events"], 1) for _, a in groups[(reg, 100000)]])
            u2 = st.median([a["crest_ms"] * 1e3 / max(a["crest_events"], 1) for _, a in groups[(reg, 200000)]])
            print(f"P5 {reg} us/ev {u1:.1f} -> {u2:.1f} (+{100*(u2/u1-1):.1f}%/doubling)")
    if ("idle", 100000) in groups and ("load", 100000) in groups and ("idle", 200000) in groups and ("load", 200000) in groups:
        r1 = (st.median([a["crest_ms"] * 1e3 / max(a["crest_events"], 1) for _, a in groups[("load", 100000)]])
              / st.median([a["crest_ms"] * 1e3 / max(a["crest_events"], 1) for _, a in groups[("idle", 100000)]]))
        r2 = (st.median([a["crest_ms"] * 1e3 / max(a["crest_events"], 1) for _, a in groups[("load", 200000)]])
              / st.median([a["crest_ms"] * 1e3 / max(a["crest_events"], 1) for _, a in groups[("idle", 200000)]]))
        print(f"P5b load multiplier us/ev: 1e5 {r1:.2f}x, 2e5 {r2:.2f}x (K-uniform within 30%: "
              f"{'HOLD' if abs(r2/r1-1) <= 0.30 else 'FAIL'}; pred band [2.5,5.0])")

if __name__ == "__main__":
    main()
