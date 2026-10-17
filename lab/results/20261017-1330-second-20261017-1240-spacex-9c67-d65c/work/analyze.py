#!/usr/bin/env python3
"""Summarize the belt A/B: pristine (position walk) vs patched (hand-off), interleaved pairs.

Reads the belt-*.txt outputs (waveprobe stdout), prints the per-arm table, the paired deltas
(raw and control-normalized), the digest identity check, and the belt verify-mode census.
"""
import re
import sys
from pathlib import Path

WORK = Path(__file__).parent
PAT = {
    "wave_cpu": re.compile(r"us_per_kick: total_wave_cpu=([\d.]+)"),
    "digest": re.compile(r"digest=([0-9a-f]{64})"),
    "kicks": re.compile(r"wave: kicks=(\d+) boundaries=(\d+) other_events=(\d+)"),
    "root": re.compile(r"position walk \(root_state_raw\)\s+([\d.]+)\s+(\d+)\s+([\d.]+)\s+([\d.]+)"),
    "apply": re.compile(r"apply \(whole\)\s+([\d.]+)\s+(\d+)\s+([\d.]+)\s+([\d.]+)"),
    "process": re.compile(r"process \(whole\)\s+([\d.]+)\s+(\d+)\s+([\d.]+)\s+([\d.]+)"),
    "requeue": re.compile(r"requeue\s+([\d.]+)\s+(\d+)\s+([\d.]+)\s+([\d.]+)"),
    "probe": re.compile(r"pos probe \(handed, walked, mismatch\): \((\d+), (\d+), (\d+)\)"),
    "wave_s": re.compile(r"wave_s=([\d.]+)"),
}


def read(tag):
    txt = (WORK / f"belt-{tag}.txt").read_text()
    return {k: m.groups() for k, p in PAT.items() if (m := p.search(txt))}


def num(tag, key, i=0):
    v = read(tag).get(key)
    return float(v[i]) if v else float("nan")


def main():
    print("== steady-state wave (70-150 ks, N=1e5, seed 1), interleaved pairs ==")
    print(f"{'run':<14} {'wave_cpu':>8} {'apply_ns':>9} {'root_calls':>10} {'root_ns':>8} {'proc_ns':>8} {'event_ns':>9} {'digest'}")
    pairs = []
    for p in (1, 2, 3):
        row = {}
        for arm in ("pristine", "patched"):
            t = f"p{p}-{arm}"
            r = read(t)
            ev_ns = float(r["process"][2]) + float(r["apply"][2]) + float(r["requeue"][2])
            d = r["digest"][0][:8] if "digest" in r else "MISSING"
            print(f"{t:<14} {num(t,'wave_cpu'):>8.2f} {num(t,'apply',2):>9.1f} {int(num(t,'root',1)):>10} {num(t,'root',2):>8.1f} {num(t,'process',2):>8.1f} {ev_ns:>9.1f} {d}")
            row[arm] = (num(t, "wave_cpu"), ev_ns)
        pairs.append(row)

    dp = sorted((r["pristine"][0] - r["patched"][0]) / r["pristine"][0] * 100 for r in pairs)
    de = sorted((r["pristine"][1] - r["patched"][1]) / r["pristine"][1] * 100 for r in pairs)
    # Control-normalized: process(whole) is untouched by the patch (the resolver's own interior),
    # so its drift measures each run's load. wave_cpu/process_ns pairs out the common inflation.
    dn = sorted(
        (1 - (num(f"p{p}-patched", "wave_cpu") / num(f"p{p}-patched", "process", 2))
             / (num(f"p{p}-pristine", "wave_cpu") / num(f"p{p}-pristine", "process", 2))) * 100
        for p in (1, 2, 3)
    )
    print(f"wave CPU drop per pair (raw): {['%.1f%%' % x for x in dp]}  median {dp[len(dp)//2]:.1f}%")
    print(f"event cycle (process+apply+requeue) drop per pair: {['%.1f%%' % x for x in de]}  median {de[len(de)//2]:.1f}%")
    print(f"wave CPU drop, control-normalized (wave_cpu/process_ns): {['%.1f%%' % x for x in dn]}  median {dn[len(dn)//2]:.1f}%")
    for p in (1, 2, 3):
        drift = (num(f"p{p}-patched", "process", 2) / num(f"p{p}-pristine", "process", 2) - 1) * 100
        print(f"  p{p} control drift (process ns/call): {num(f'p{p}-pristine','process',2):.0f} -> {num(f'p{p}-patched','process',2):.0f} ({drift:+.1f}%)")
    ap = [(1 - num(f"p{p}-patched", "apply", 2) / num(f"p{p}-pristine", "apply", 2)) * 100 for p in (1, 2, 3)]
    rt = [(1 - num(f"p{p}-patched", "root", 2) / num(f"p{p}-pristine", "root", 2)) * 100 for p in (1, 2, 3)]
    print(f"  apply stage drop per pair: {['%.1f%%' % x for x in ap]}")
    print(f"  ROOT stage drop per pair:  {['%.1f%%' % x for x in rt]}")
    saved = [num(f"p{p}-pristine", "apply", 2) - num(f"p{p}-patched", "apply", 2) for p in (1, 2, 3)]
    print(f"  apply ns/call saved per pair: {['%.0f' % x for x in saved]}  (x 2.08 events/kick = {['%.1f' % (x*2.08/1000) for x in saved]} us/kick)")

    print("\n== first wave (13-15 ks) ==")
    for arm in ("pristine", "patched"):
        t = f"w1-{arm}"
        r = read(t)
        print(f"{t:<14} wave_cpu={num(t,'wave_cpu'):.2f} apply_ns={num(t,'apply',2):.1f} root_calls/kick={num(t,'root',3):.3f} digest={r['digest'][0][:16]}…")

    print("\n== digest identity across arms ==")
    byd = {}
    for t in ("p1-pristine", "p1-patched", "p2-pristine", "p2-patched", "p3-pristine", "p3-patched", "w1-pristine", "w1-patched", "census"):
        r = read(t)
        if "digest" in r:
            byd.setdefault(r["digest"][0], []).append(t)
    for d, ts in byd.items():
        print(f"{d[:16]}… : {len(ts)} runs: {', '.join(sorted(ts))}")
    print(f"distinct digests: {len(byd)} (5ade pristine anchors: 0789136370007234… steady, 0d8ced8083d27963… first wave)")

    print("\n== belt verify census (ES_POS_VERIFY=1, patched arm) ==")
    txt = (WORK / "belt-census.txt").read_text()
    for l in txt.splitlines():
        if l.startswith("pos probe") or re.match(r"^\w+\s+handed=", l):
            print(l)
    h, w, m = (int(x) for x in read("census")["probe"])
    print(f"coverage: {h}/{h+w} = {h/(h+w)*100:.2f}% of all non-player applies (the {w} fallbacks are the belt's birth replans)")
    print(f"census wave_cpu={num('census','wave_cpu'):.2f} (verify mode pays both paths; not a timing arm)")


if __name__ == "__main__":
    sys.exit(main())
