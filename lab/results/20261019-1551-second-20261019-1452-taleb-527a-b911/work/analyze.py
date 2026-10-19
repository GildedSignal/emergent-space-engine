#!/usr/bin/env python3
"""b911: channel-2 bisect analysis. Reads the probe lines of the three arms.

Arms: live-guard (no freeze), freeze-30k, freeze-60k (ES_FREEZE_LD_AT_GS).
Prints: (1) the RSS regression on the two deep counters, (2) the census level law
extra ~ const x K with K = 2*ld0 + 330 s, (3) distinct-vs-held scans and the fence
arithmetic, (4) the per-arm summary the dossier quotes.
"""
import re, sys
import subprocess

ROW = re.compile(r"gs=(\d+) rss_mb=(\d+) hwm_mb=(\d+) held=(\d+) scan_distinct=(\d+) bpb=\d+ "
                 r"hist_gt1=(\d+) hist_total=(\d+) hist_max=(\d+) gap_s=([\d.]+) "
                 r"scan_mb=([\d.]+) cand_len=(\d+) hist_mb=([\d.]+) ld0_gs=(\d+)")


def load(path):
    rows = []
    for line in open(path):
        m = ROW.search(line)
        if m:
            g = m.groups()
            rows.append(dict(gs=int(g[0]), rss=int(g[1]), held=int(g[3]), distinct=int(g[4]),
                             gt1=int(g[5]), total=int(g[6]), hmax=int(g[7]), gap=float(g[8]),
                             scan=float(g[9]), cand=int(g[10]), hist=float(g[11]), ld0=int(g[12])))
    return rows


def ols(A, b):
    """Least squares for b ~ A x (A: list of rows). Returns x and residuals."""
    n = len(A[0])
    # normal equations via Gaussian elimination (small)
    ata = [[sum(A[k][i] * A[k][j] for k in range(len(A))) for j in range(n)] + [sum(A[k][i] * b[k] for k in range(len(A)))] for i in range(n)]
    for i in range(n):
        p = max(range(i, n), key=lambda r: abs(ata[r][i]))
        ata[i], ata[p] = ata[p], ata[i]
        d = ata[i][i]
        for j in range(i, n + 1):
            ata[i][j] /= d
        for r in range(n):
            if r != i and ata[r][i]:
                f = ata[r][i]
                for j in range(i, n + 1):
                    ata[r][j] -= f * ata[i][j]
    x = [ata[i][n] for i in range(n)]
    resid = [b[k] - sum(A[k][i] * x[i] for i in range(n)) for k in range(len(A))]
    return x, resid


def main(live, f30, f60, fkey=None, fkeep=None):
    L, B, C = load(live), load(f30), load(f60)
    print(f"== arms: live {len(L)} probes to gs {L[-1]['gs']}; f30 {len(B)} to {B[-1]['gs']}; f60 {len(C)} to {C[-1]['gs']}")

    # (1) regression on the live arm, past the build settle (gs >= 20k): rss ~ scan + hist
    rows = [r for r in L if r["gs"] >= 20000]
    A = [[1.0, r["scan"], r["hist"]] for r in rows]
    b = [float(r["rss"]) for r in rows]
    x, resid = ols(A, b)
    import math
    rmse = math.sqrt(sum(e * e for e in resid) / len(resid))
    rss_range = max(b) - min(b)
    print(f"== (1) live RSS ~ c0 + c1*scan_mb + c2*hist_mb  (n={len(rows)}, gs {rows[0]['gs']}..{rows[-1]['gs']})")
    print(f"    c0={x[0]:.1f} MB  c1={x[1]:.3f}  c2={x[2]:.3f}  rmse={rmse:.1f} MB  (rss span {rss_range:.0f} MB)")

    # (2) census level law: extra = total - baseline(~30k) vs K = 2*ld0 + 330
    base = 30028  # bodies
    def law(rows, lo, hi, tag):
        sel = [r for r in rows if lo <= r["gs"] <= hi]
        if not sel:
            print(f"    {tag}: no rows")
            return
        ex = [r["total"] - base for r in sel]
        ks = [2 * r["ld0"] + 330 for r in sel]
        mid = sel[len(sel) // 2]
        ratios = [e / k for e, k in zip(ex, ks) if k > 3000]
        print(f"    {tag}: gs {sel[0]['gs']}..{sel[-1]['gs']} extra/K median "
              f"{sorted(ratios)[len(ratios)//2]:.2f} (min {min(ratios):.2f} max {max(ratios):.2f});"
              f" mid gs={mid['gs']} total={mid['total']} ld0={mid['ld0']} K={2*mid['ld0']+330:.0f}")
    print(f"== (2) census level law, extra = (hist_total - {base}) vs K = 2*ld0+330 s")
    law(L, 150000, 300000, "live late   ")
    law(L, 120000, 130000, "live onset  ")
    # frozen arms: K is the frozen value 2*ld0(T)+330, read from the arm's own trace at T
    for tag, rows, T in [("f30 flat    ", B, 30000), ("f60 flat    ", C, 60000)]:
        at = min(rows, key=lambda r: abs(r["gs"] - T))
        K = 2 * at["ld0"] + 330
        sel = [r for r in rows if r["gs"] >= T + 2 * K]
        extras = [r["total"] - base for r in sel]
        mid = sorted(extras)[len(extras) // 2]
        print(f"    {tag}: frozen K={K:.0f} s (ld0({T})={at['ld0']}); flat extra median {mid}"
              f" -> extra/K = {mid / K:.2f} bindings per frozen-keep-second (n={len(sel)}, gs {sel[0]['gs']}..{sel[-1]['gs']})")

    # slopes: census and RSS growth post-settle, live vs freeze
    def slope(rows, lo, hi, key, scale=1.0):
        sel = [(r["gs"], r[key]) for r in rows if lo <= r["gs"] <= hi]
        (x1, y1), (x2, y2) = sel[0], sel[-1]
        return (y2 - y1) * scale / (x2 - x1)
    print("== (2b) post-settle slopes (per 10k gs):")
    for tag, rows, lo, hi in [("live", L, 150000, 300000), ("f30 ", B, 45000, 170000), ("f60 ", C, 75000, 235000)]:
        print(f"    {tag}: census {slope(rows, lo, hi, 'total')*1e4:+.0f} bindings, hist_mb {slope(rows, lo, hi, 'hist')*1e4:+.1f} MB, rss {slope(rows, lo, hi, 'rss')*1e4:+.1f} MB")

    # (3) distinct scans, duplication, per-distinct bytes, fence arithmetic
    print("== (3) scan channel: distinct captures vs held entries, per-distinct bytes")
    for tag, rows, lo, hi in [("live", L, 100000, 320000), ("f30 ", B, 60000, 170000), ("f60 ", C, 80000, 235000)]:
        sel = [r for r in rows if lo <= r["gs"] <= hi]
        r = sel[len(sel) // 2]
        dup = r["held"] / max(r["distinct"], 1)
        per = r["scan"] / max(r["distinct"], 1)
        print(f"    {tag}: gs={r['gs']} held={r['held']} distinct={r['distinct']} (x{dup:.2f}) scan={r['scan']:.1f} MB"
              f" -> {per:.2f} MB/distinct, {r['cand']/max(r['distinct'],1):.0f} cand/distinct")
    r = [r for r in L if r["gs"] >= 100000][-1]
    entries_at_2048 = 2048 / (r["held"] / max(r["distinct"], 1))
    print(f"    fence: SCAN_BACKLOG=2048 entries ~ {entries_at_2048:.0f} distinct x {r['scan']/max(r['distinct'],1):.2f} MB"
          f" = {entries_at_2048 * r['scan'] / max(r['distinct'],1) / 1000:.1f} GB licensed at gs {r['gs']}; guard fired at held {L[-1]['held']}")

    # (4) guard-window attribution and per-binding constant
    print("== (4) guard-window split (live arm, last probe before the guard):")
    r = L[-1]
    print(f"    gs={r['gs']}: rss={r['rss']} scan={r['scan']:.0f} hist={r['hist']:.0f} -> scan share "
          f"{100*r['scan']/r['rss']:.0f}%, hist share {100*r['hist']/r['rss']:.0f}% (raw); "
          f"regression-split: scan {x[1]*r['scan']:.0f} hist {x[2]*r['hist']:.0f} of {r['rss']}")
    extra = r["total"] - base
    print(f"    per-binding: hist {r['hist']:.0f} MB / extra {extra} = {r['hist']*1e6/extra:.0f} B/binding deep;"
          f" regression c2 says {x[2]*r['hist']*1e6/(extra) if extra else 0:.0f} B/binding in RSS")

    # (5) determinism anchors: end stats
    # (4b) term-split bisect: does either single-term freeze still ratchet?
    if fkey and fkeep:
        print("== (4b) term-split bisect at T=30k (P6/P7):")
        for tag, path in [("key ", fkey), ("keep", fkeep)]:
            rows = load(path)
            if not rows:
                print(f"    {tag}: no probes")
                continue
            last = rows[-1]
            lad = [l for l in open(path).read().splitlines() if l.startswith("ladder:")][0]
            guard = [l for l in open(path).read().splitlines() if "guard hit" in l]
            p99 = re.search(r"p99_ms=([0-9.]+)", lad).group(1)
            mx = re.search(r"max_ms=([0-9.]+)", lad).group(1)
            print(f"    {tag}: end gs={last['gs']} hist_total={last['total']} rss={last['rss']} MB"
                  f" p99={p99} max={mx} ms {guard[0].split(': ')[1] if guard else '(no guard)'}")

    print("== (5) arm ends:")
    for tag, path in [("live", live), ("f30 ", f30), ("f60 ", f60)]:
        last = open(path).read().strip().splitlines()
        lad = [l for l in last if l.startswith("ladder:")][0]
        st = [l for l in last if l.startswith("game ")][0]
        kicks = re.search(r"kicks (\d+) \(([\d.e-]+)", st).group(2)
        ref = re.search(r"refused (\d+)", st).group(1)
        end = re.search(r"foot_end_mb=(\d+)", lad).group(1)
        trunc = re.search(r"truncated=(\w+)", lad).group(1)
        guard = [l for l in last if "guard hit" in l]
        print(f"    {tag}: kicks/b/gs={kicks} refused={ref} end_rss={end} MB truncated={trunc} {guard[0].strip() if guard else ''}")


if __name__ == "__main__":
    main(*sys.argv[1:6])
