#!/usr/bin/env python3
"""Comparison table for run 20261015-0250-second-20261015-0128-inversion-3ca8-f50d.

Reads out/*.jsonl, pairs engine vs exact (and engine vs float where present),
and prints the class-metric ratios the dossier quotes. Usage: python3 table.py"""
import json
import pathlib
import sys

OUT = pathlib.Path(__file__).resolve().parent / "out"


def load(name):
    with open(OUT / f"{name}.jsonl") as f:
        return json.loads(f.readline())


def row(scene, q, seed, eng, tw, twin_name):
    r = {
        "scene": scene,
        "seed": seed,
        "q": q,
        "trapped": f"{eng['above05_end']}v{tw['above05_end']}",
        "dwell_tot": f"{eng['dwell05_tot_median'] / max(tw['dwell05_tot_median'], 1):.3f}x",
        "max_dwell": f"{eng['dwell05_max_max'] / max(tw['dwell05_max_max'], 1):.3f}x",
        "contacts": f"{eng['contacts'] / max(tw['contacts'], 1):.3f}x",
        "g_p50": f"{eng['final_gamma_p50'] / max(tw['final_gamma_p50'], 1e-9):.3f}x",
        "g_p90": f"{eng['final_gamma_p90'] / max(tw['final_gamma_p90'], 1e-9):.3f}x",
        "heavy_g": f"{eng['heavy_gamma_final']:.5f}v{tw['heavy_gamma_final']:.5f}",
        "twin": twin_name,
        "passthrough": f"{tw.get('passthrough_frac', 0):.4f}",
        "eng_resid": eng.get("residual", 0),
    }
    return r


def main():
    groups = [
        ("pos", 20, 1, ["exact"]),
        ("neg", 20, 1, ["exact", "float", "srskip"]),
        ("pump", 20, [1, 2, 3, 4, 5], ["exact", "float", "srskip"]),
        ("pump", 16, 1, ["exact"]),
        ("pump", 18, 1, ["exact"]),
        ("soft", 20, [1, 2], ["exact"]),
        ("tall", 20, 1, ["exact"]),
    ]
    hdr = f"{'scene':6} {'q':>3} {'seed':>4} {'twin':5} {'trapped':9} {'dw_tot':8} {'max_dw':8} {'contacts':9} {'g_p50':7} {'g_p90':7} {'heavy_g':17} {'pass':6}"
    print(hdr)
    print("-" * len(hdr))
    for scene, q, seeds, twins in groups:
        if not isinstance(seeds, list):
            seeds = [seeds]
        for seed in seeds:
            try:
                eng = load(f"{scene}_engine_q{q}_s{seed}")
            except FileNotFoundError:
                continue
            for twin in twins:
                try:
                    tw = load(f"{scene}_{twin}_q{q}_s{seed}")
                except FileNotFoundError:
                    continue
                r = row(scene, q, seed, eng, tw, twin)
                print(
                    f"{r['scene']:6} {r['q']:>3} {r['seed']:>4} {r['twin']:5} {r['trapped']:9} "
                    f"{r['dwell_tot']:8} {r['max_dwell']:8} {r['contacts']:9} {r['g_p50']:7} "
                    f"{r['g_p90']:7} {r['heavy_g']:17} {r['passthrough']:6}"
                )
    # micro summary
    micros = []
    try:
        with open(OUT / "micro.jsonl") as f:
            for line in f:
                micros.append(json.loads(line))
    except FileNotFoundError:
        return
    heavy = [m for m in micros if m["mh"] == 1000]
    print(
        f"micro (Q=2^20): max |d_ang eng-law| = {max(m['d_ang_eng_law'] for m in heavy):.2e} rad; "
        f"max |d_beta eng-law| = {max(m['d_beta_eng_law'] for m in heavy):.2e}; "
        f"max |d_ang law-sr| = {max(m['d_ang_law_sr'] for m in heavy):.3f} rad (the tilt)"
    )


if __name__ == "__main__":
    sys.exit(main())
