#!/usr/bin/env python3
"""Summary of the rows `certified_bank` wrote (stdlib only): python3 certified_bank.py DIR [--by-rung]

Tolerances (frozen with the example, see its header). Position tiers apply while the radial
cycles elapsed n <= 10, where a drift of the law's designed size (1e-6 per cycle) has not
wrapped the angle; beyond that an absolute position is a statement about the period to
better than 1/(2 pi n), which the law never promised (gate B2 is 0.1%). For n > 10 the
error TYPE is judged instead: the angle error against the drift predicted from the law's
own period and advance errors against the Arb diagnostics (G22 only).
  design:    |dX| <= 2 quanta + 1e-5 (1 + n) r        behaviour: |dX| <= 2 quanta + 1e-3 (1 + n) r
"""
import collections, glob, math, sys

TOL = {"design": 1e-5, "behaviour": 1e-3}
NMAX = 10.0
cols_q = "id cat law ref res idx ncyc rref dpos rel drr dphi floor".split()
cols_c = ("id cat law nfree nabs inbound E L rho comp_us knots cross fitp fitv recon turn_p turn_a "
          "per_rel adv_rel defl_abs defl_rel scat diag e_err l_err ecc window law_per law_adv margin deltah edge_ratio").split()


def num(x):
    try:
        return float(x)
    except ValueError:
        return float("nan")


def rows(dirname, kind):
    cols = cols_q if kind == "q" else cols_c
    for f in sorted(glob.glob(f"{dirname}/*.{kind}.tsv")):
        rung = f.split("/")[-1].split(".")[0]
        for line in open(f):
            p = line.rstrip("\n").split("\t")
            if len(p) < len(cols):
                continue
            d = dict(zip(cols, p))
            d["rung"] = rung
            yield d


def group(cat):
    c = cat.split("+")
    for key in ("near-separatrix", "near-isco", "near-circular", "near-horizon", "long-T", "range-exit",
                "T=T0", "T<T0", "far-field-hop", "infall-from-rest", "E=1", "fallback", "radial", "circular"):
        if key in c:
            if key == "E=1":
                return "E=1/" + ("absorbed" if "absorbed" in c else "escapes")
            if key == "circular":
                return "circular/" + ("unstable" if "unstable" in c else "stable")
            return key + ("/" + c[-1] if key == "near-isco" else "")
    if c[0] == "near-integer":
        return "near-integer/" + c[1] + "/" + c[2]
    if c[0] == "R2":
        return "R2"
    if c[0] == "null":
        return "null/" + c[1]
    return "/".join(c[:2])


def q(xs, p):
    xs = sorted(x for x in xs if x == x)
    if not xs:
        return float("nan")
    return xs[min(len(xs) - 1, int(p * len(xs)))]


def fmt(x):
    return "nan" if x != x else (f"{x:.1e}" if (x != 0 and (abs(x) < 1e-3 or abs(x) >= 1e5)) else f"{x:.4g}")


def within(r, t):
    return num(r["dpos"]) <= 2 + t * (1 + num(r["ncyc"])) * num(r["rref"])


def main():
    dirname = sys.argv[1]
    by_rung = "--by-rung" in sys.argv
    Q = list(rows(dirname, "q"))
    C = list(rows(dirname, "c"))
    byid = {(c["rung"], c["id"]): c for c in C if len(c) > 12}
    print(f"answers {len(Q)}  cases {len(C)}")
    # ---- what maps
    status = collections.Counter()
    for r in Q:
        law, ref = r["law"], r["ref"]
        if ref == "F":
            if r["res"] == "ok":
                s = "FREE mapped (position compared)"
            elif r["res"] == "before":
                s = "FREE query before T0 (skipped)"
            elif law in ("cycle", "passage"):
                s = f"FREE law fitted, readout {r['res']} (beyond the window or no root)"
            elif law.startswith("photon"):
                s = "FREE photon (no position generator; class and deflection only)"
            elif law.startswith("skip:radial"):
                s = "FREE skipped: radial path (L=0), not supplied"
            elif law.startswith("skip"):
                s = f"FREE skipped: {law}"
            else:
                s = f"FREE law {law}"
        elif ref == "A":
            if law == "refused:NoBoundOrbit":
                s = "ABSORBED, law refuses (no turning point): reads as absorbed"
            elif law in ("cycle", "passage"):
                s = "ABSORBED, law returns an orbit: CLASS DISAGREES"
            elif law == "photon:absorbed":
                s = "ABSORBED photon, law absorbed: class agrees"
            elif law == "photon:escaped":
                s = "ABSORBED photon, law escaped: CLASS DISAGREES"
            elif law.startswith("skip:radial"):
                s = "ABSORBED, radial (not supplied)"
            elif law.startswith("skip:inside"):
                s = "ABSORBED, starts inside the horizon (not an orbit)"
            else:
                s = f"ABSORBED, law {law}"
        else:
            s = {"O": "OutOfRange (skipped)", "B": "Before (skipped)", "U": "Unsettled (skipped)"}[ref]
        status[s] += 1
    print("\n== answers by what the law could be asked ==")
    for k, v in sorted(status.items(), key=lambda kv: -kv[1]):
        print(f"{v:8d}  {k}")
    mapped = [r for r in Q if r["res"] == "ok"]
    # ---- positions in the first cycles
    print(f"\n== positions, n <= {NMAX:g} radial cycles (ref Free, law fitted, readout ok) ==")
    print("group                                  n  floor%   median      p90      p99      max  design%  behav%")
    G = collections.defaultdict(list)
    for r in mapped:
        if num(r["ncyc"]) <= NMAX:
            G[((r["rung"] + " ") if by_rung else "", group(r["cat"]), r["law"])].append(r)
    tot = collections.Counter()
    for key, rs in sorted(G.items()):
        rel = [num(r["rel"]) for r in rs]
        fl = [r["floor"] for r in rs if r["floor"] in ("0", "1")]
        fpct = 100.0 * sum(1 for f in fl if f == "1") / len(fl) if fl else float("nan")
        d = 100.0 * sum(within(r, TOL["design"]) for r in rs) / len(rs)
        b = 100.0 * sum(within(r, TOL["behaviour"]) for r in rs) / len(rs)
        print(f"{key[0] + key[1] + ' ' + key[2]:36s}{len(rs):7d} {fmt(fpct):>6s} {fmt(q(rel,.5)):>8s} {fmt(q(rel,.9)):>8s} {fmt(q(rel,.99)):>8s} {fmt(max(rel)):>8s} {d:7.1f} {b:7.1f}")
        tot["n"] += len(rs)
        tot["d"] += sum(within(r, TOL["design"]) for r in rs)
        tot["b"] += sum(within(r, TOL["behaviour"]) for r in rs)
    print(f"TOTAL n<={NMAX:g}: {tot['n']} positions; design tier {tot['d']} ({100*tot['d']/max(tot['n'],1):.2f}%), behaviour tier {tot['b']} ({100*tot['b']/max(tot['n'],1):.2f}%)")
    far = [r for r in mapped if num(r["ncyc"]) > NMAX]
    print(f"positions with n > {NMAX:g}: {len(far)} (not judged in absolute terms; see the drift check)")
    # ---- failures inside the tiers, by group
    print("\n== positions outside the behaviour tier (n <= 10) ==")
    bad = [r for r in mapped if num(r["ncyc"]) <= NMAX and not within(r, TOL["behaviour"])]
    cnt = collections.Counter((group(r["cat"]), r["law"]) for r in bad)
    for k, v in cnt.most_common():
        print(f"{v:6d}  {k[0]} {k[1]}")
    # ---- passage error vs eccentricity
    print("\n== passages (unbound, with turning point): error against eccentricity e = 1/k - 1 (law's Q48 k) ==")
    P = collections.defaultdict(list)
    for r in mapped:
        if r["law"] == "passage":
            c = byid.get((r["rung"], r["id"]))
            e = num(c["ecc"]) if c else float("nan")
            b = "e<1e3" if e < 1e3 else "1e3-1e6" if e < 1e6 else "1e6-1e9" if e < 1e9 else "1e9-1e12" if e < 1e12 else "e>=1e12"
            P[b].append(num(r["rel"]))
    print("e bucket          n    median      p90      max     (k quantum 2^-48: relative error of k is 3.6e-15 e)")
    for b in ("e<1e3", "1e3-1e6", "1e6-1e9", "1e9-1e12", "e>=1e12"):
        xs = P.get(b, [])
        if xs:
            print(f"{b:10s}{len(xs):8d} {fmt(q(xs,.5)):>9s} {fmt(q(xs,.9)):>8s} {fmt(max(xs)):>8s}")
    # ---- drift consistency (G22 with Arb diag): angle error against the drift the law's own invariants predict
    print("\n== error type: bound orbits with Arb diagnostics (G22): angle error against the predicted linear drift ==")
    print("pred = n [ (2 pi + A) eP + A eA ] with eP, eA the law's period and advance errors against Arb, A its advance per cycle")
    D = collections.defaultdict(list)
    for r in mapped:
        if r["law"] == "cycle" and r["rung"] == "G22":
            c = byid.get((r["rung"], r["id"]))
            if not c:
                continue
            eP, eA = num(c["per_rel"]), num(c["adv_rel"])
            if eP != eP:
                continue
            n = num(r["ncyc"])
            A = num(c["law_adv"])
            pred = n * ((2 * math.pi + A) * eP + A * eA)
            if 0 < pred < 0.3 and n > 1:
                # 3e-9 rad is the tube's 32-bit orientation (one quantum 1.5e-9 rad), not drift
                D[group(r["cat"])].append(max(abs(num(r["dphi"])) - 3e-9, 0.0) / pred)
    print("group                    n  (|dphi|-3e-9)/pred: median   p90    max   (a pure linear drift gives a ratio near or below 1)")
    for g, xs in sorted(D.items()):
        print(f"{g:22s}{len(xs):6d}   {fmt(q(xs,.5)):>10s} {fmt(q(xs,.9)):>8s} {fmt(max(xs)):>8s}")
    # ---- passage error vs window ratio
    print("\n== passages: error against window/periapsis (the phase word x = R/r is Q62: resolution 2^-62 / x) ==")
    W = collections.defaultdict(list)
    for r in mapped:
        if r["law"] == "passage":
            c = byid.get((r["rung"], r["id"]))
            er = num(c["edge_ratio"]) if c else float("nan")
            b = "<1e3" if er < 1e3 else "1e3-1e6" if er < 1e6 else "1e6-1e9" if er < 1e9 else "1e9-1e12" if er < 1e12 else "1e12-1e15" if er < 1e15 else ">=1e15"
            W[b].append(num(r["rel"]))
    print("window/periapsis      n    median      p90      max")
    for b in ("<1e3", "1e3-1e6", "1e6-1e9", "1e9-1e12", "1e12-1e15", ">=1e15"):
        xs = W.get(b, [])
        if xs:
            print(f"{b:12s}{len(xs):8d} {fmt(q(xs,.5)):>9s} {fmt(q(xs,.9)):>8s} {fmt(max(xs)):>8s}")
    # ---- near the separatrix: bound-class cases by margin (p - p_sep)/p
    print("\n== bound-energy cases (E < 1, three real roots) by separatrix margin (p - 6 - 2e)/p: what the law does ==")
    print("margin          cases  cycle  Range  NoBound  other   median knots  p99 compile us   whirl(d<2^-10 h)   period vs Arb p99   advance vs Arb p99")
    M = collections.defaultdict(list)
    for c in C:
        if len(c) < 12:
            continue
        m = num(c["margin"])
        if m == m and m > 0 and num(c["E"]) < 1.0:
            b = "<1e-3" if m < 1e-3 else "1e-3-1e-2" if m < 1e-2 else "1e-2-1e-1" if m < 1e-1 else ">=1e-1"
            M[b].append(c)
    for b in ("<1e-3", "1e-3-1e-2", "1e-2-1e-1", ">=1e-1"):
        cs = M.get(b, [])
        if not cs:
            continue
        cnt = collections.Counter("cycle" if c["law"] == "cycle" else "Range" if c["law"].endswith("Range") else "NoBound" if c["law"].endswith("NoBoundOrbit") else "other" for c in cs)
        kn = [num(c["knots"]) for c in cs if c["law"] == "cycle"]
        cu = [num(c["comp_us"]) for c in cs if c["law"] == "cycle"]
        wh = sum(1 for c in cs if num(c["deltah"]) < 2 ** -10)
        pe = [num(c["per_rel"]) for c in cs if num(c["per_rel"]) == num(c["per_rel"])]
        ad = [num(c["adv_rel"]) for c in cs if num(c["adv_rel"]) == num(c["adv_rel"])]
        print(f"{b:11s}{len(cs):8d}{cnt['cycle']:7d}{cnt['Range']:7d}{cnt['NoBound']:9d}{cnt['other']:7d}   {fmt(q(kn,.5)):>12s}  {fmt(q(cu,.99)):>14s}   {wh:12d}   {fmt(q(pe,.99)):>17s}   {fmt(q(ad,.99)):>17s}")
    # ---- classes
    print("\n== case classes: reference class against what the law does (cases) ==")
    CC = collections.defaultdict(collections.Counter)
    for c in C:
        if len(c) < 12:
            continue
        refc = "absorbed-at-some-T" if num(c["nabs"]) > 0 else "free-throughout"
        CC[((c["rung"] + " ") if by_rung else "", group(c["cat"]), refc)][c["law"] + (" (inbound)" if c["inbound"] == "1" and c["law"].startswith("refused") else "")] += 1
    for key, cnt in sorted(CC.items()):
        print(f"{key[0] + key[1]:34s} {key[2]:19s} " + ", ".join(f"{k}: {v}" for k, v in cnt.most_common()))
    # ---- invariants, by group
    print("\n== per-case invariants (fitted cases), by group ==")
    fields = (("fit |dpos|/r", "fitp"), ("turn periapsis*", "turn_p"), ("turn apoapsis*", "turn_a"), ("period vs Arb", "per_rel"), ("advance vs Arb", "adv_rel"))
    print(f"{'group':26s} " + " ".join(f"{n:>26s}" for n, _ in fields))
    IG = collections.defaultdict(list)
    for c in C:
        if len(c) > 12 and c["law"] in ("cycle", "passage"):
            IG[group(c["cat"])].append(c)
    for g, cs in sorted(IG.items()):
        cells = []
        for _, f in fields:
            xs = [num(c[f]) for c in cs if num(c[f]) == num(c[f]) and not (f.startswith("turn") and c["diag"] != "1")]
            cells.append(f"{len(xs):4d} {fmt(q(xs,.5)):>7s} {fmt(q(xs,.99)):>7s} {fmt(max(xs)) if xs else 'nan':>7s}" if xs else " " * 26)
        print(f"{g:26s} " + " ".join(cells))
    print("(each cell: n, median, p99, max; * against the Arb roots, G22 only)")
    for name, field in (("photon deflection abs vs Arb", "defl_abs"), ("photon deflection rel vs Arb", "defl_rel"),
                        ("adapter E vs Arb diag (control)", "e_err"), ("adapter L vs Arb diag (control)", "l_err"),
                        ("fit + compile time, us (loaded M1)", "comp_us"), ("shape knots per bound orbit", "knots"), ("crossings per half orbit", "cross")):
        xs = [num(c[field]) for c in C if len(c) > 12 and num(c[field]) == num(c[field]) and num(c[field]) >= 0]
        if xs:
            print(f"{name:38s} n={len(xs):6d} median {fmt(q(xs,.5))} p90 {fmt(q(xs,.9))} p99 {fmt(q(xs,.99))} max {fmt(max(xs))}")
    rec = collections.Counter(c["recon"] for c in C if len(c) > 12 and c["law"] in ("cycle", "passage"))
    print("exact left inverse (reconstruct() == input state):", dict(rec))
    # ---- capture
    print("\n== capture: every reference answer that says Absorbed or that is a plunge, against the law ==")
    CAP = collections.Counter()
    for c in C:
        if len(c) < 12:
            continue
        g = group(c["cat"])
        refabs = num(c["nabs"]) > 0
        law = c["law"]
        inbound = c["inbound"] == "1"
        if law == "refused:NoBoundOrbit":
            lawc = "absorbed (no turning point, inbound)" if inbound else "refused (outbound, no turning point)"
        elif law in ("cycle", "passage"):
            lawc = "turns (" + law + ")"
        elif law.startswith("photon"):
            lawc = law
        else:
            lawc = law
        CAP[(g, "ref absorbs" if refabs else "ref free", lawc)] += 1
    for k, v in sorted(CAP.items()):
        if k[1] == "ref absorbs" or "plunging" in k[0] or "E=1" in k[0] or "horizon" in k[0] or "photon" in k[2] or "null" in k[0]:
            print(f"{v:6d}  {k[0]:34s} {k[1]:12s} law: {k[2]}")
    # ---- worst cases
    print("\n== worst mapped positions with n <= 10 (rel error) ==")
    for r in sorted([r for r in mapped if num(r["ncyc"]) <= NMAX], key=lambda r: -num(r["rel"]))[:12]:
        c = byid.get((r["rung"], r["id"]), {})
        print(f"{r['id']:14s} {r['cat'][:40]:40s} {r['law']:8s} n {fmt(num(r['ncyc'])):>8s} r {fmt(num(r['rref'])):>9s} rel {fmt(num(r['rel'])):>8s} dphi {fmt(num(r['dphi'])):>8s} e {fmt(num(c.get('ecc','nan')))}")


main()
