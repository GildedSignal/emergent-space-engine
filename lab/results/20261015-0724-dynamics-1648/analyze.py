#!/usr/bin/env python3
"""Analysis for run 20261015-0724-dynamics-1648: skip-gate distortion of a cold dense gas.

Reads work/results.jsonl (one JSON object per scene-arm, scenes in order
c1, c2, d1, d2, h1 with arms shipped, skip, contact, cross, tau) and prints the
dossier's tables. Pure stdlib.
"""
import json
import sys
from collections import defaultdict

SCENES = ["c1", "c2", "d1", "d2", "h1"]


def t_half(t, ta, tb):
    if not t:
        return -1.0
    i0 = abs((ta[0] - tb[0]) / (ta[0] + tb[0]))
    half = i0 / 2.0
    for k in range(len(t)):
        it = abs((ta[k] - tb[k]) / (ta[k] + tb[k]))
        if it <= half:
            return float(t[k])
    return -1.0


def main(path):
    rows = []
    for line in open(path):
        rows.append(json.loads(line))
    by_scene = defaultdict(dict)
    order = []
    for r in rows:
        key = None
        if key is None and r not in order:
            pass
        # scenes were printed in SCENES order, 5 arms each
        order.append(r)
    for i, r in enumerate(order):
        by_scene[SCENES[i // 5]][r["arm"]] = r

    for sc in SCENES:
        arms = by_scene[sc]
        print(f"\n=== scene {sc} ===")
        print(f"{'arm':8s} {'contacts':>8s} {'skipfr':>6s} {'t_half':>8s} "
              f"{'TA_end':>10s} {'TB_end':>10s} {'dropped/tot':>11s} {'agree':>7s} {'ledger':>6s}")
        th = {}
        for arm in ["shipped", "skip", "contact", "cross", "tau"]:
            if arm not in arms:
                continue
            r = arms[arm]
            skips = r.get("skips", r.get("skips_obs", 0))
            th[arm] = t_half(r["t"], r["TA"], r["TB"])
            agree = r.get("classifier_agree")
            agree = f"{agree}/{r['contacts']}" if agree is not None else "-"
            tr, dr = r.get("transport", 0.0), r.get("dropped_transport", 0.0)
            print(f"{arm:8s} {r['contacts']:8d} {skips / max(1, r['contacts']):6.3f} "
                  f"{th[arm]:8.0f} {r['TA'][-1]:10.1f} {r['TB'][-1]:10.1f} "
                  f"{(dr / (dr + tr)) if (dr + tr) > 0 else 0:11.4f} {agree:>7s} "
                  f"{str(r.get('ledger_ok', '-')):>6s}")
        if "skip" in th and "contact" in th and th["skip"] > 0 and th["contact"] > 0:
            print(f"t_half(skip)/t_half(contact) = {th['skip'] / th['contact']:.3f}")
        # per-rho skip rates vs max(0, 1-rho)
        r = arms.get("shipped") or arms.get("skip")
        if r:
            edges = [0.3, 0.5, 0.7, 1.0, 1.5, 2.0]
            lo, centres = 0.0, [0.15, 0.4, 0.6, 0.85, 1.25, 1.75]
            lines = []
            for bi in range(7):
                n, s = r["rho_bins"][bi], r["rho_skips"][bi]
                if n:
                    c = centres[bi] if bi < 6 else 3.0
                    pred = max(0.0, 1.0 - c)
                    lines.append(f"rho~{c:4.2f}: {s / n:5.3f} (n={n:6d}, 1-rho={pred:4.2f})")
            print("  per-rho skip rate vs 1-rho: " + "; ".join(lines))
        for arm in ["contact", "cross", "tau"]:
            if arm in arms:
                a = arms[arm]
                print(f"  {arm}: contaminated={a.get('contaminated', 0)} "
                      f"degenerate={a.get('degenerate', 0)} "
                      f"reenc(skip)={a.get('reenc_after_skip', 0)} "
                      f"reenc(exch)={a.get('reenc_after_exchange', 0)} "
                      f"fano={a.get('fano_active', 0):.2f}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "work/results.jsonl")
