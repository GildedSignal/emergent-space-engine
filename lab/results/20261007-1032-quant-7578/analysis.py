#!/usr/bin/env python3
"""Summarize decisive.jsonl (run 20261007-1032-quant-7578). Usage: python3 analysis.py"""
import json, pathlib
rows = [json.loads(l) for l in open(pathlib.Path(__file__).parent / "decisive.jsonl")]
hdr = f"{'n':>7} {'seed':>4} {'deg_mean':>8} {'max/mean':>8} {'evals p50/p90/p99/p999/max':>28} {'setup mean ms':>13} {'p99 ms':>7} {'ns/pair':>7} {'q p999':>6}"
print(hdr)
for d in rows:
    print(f"{d['n']:>7} {d['seed']:>4} {d['deg_mean']:>8.0f} {d['deg_max']/d['deg_mean']:>8.2f} "
          f"{d['evals_per_pair_p50']:>8}/{d['evals_per_pair_p90']:>4}/{d['evals_per_pair_p99']:>6}/"
          f"{d['evals_per_pair_p999']:>5}/{d['evals_per_pair_max']:>6} "
          f"{d['setup_ns_per_body_mean']/1e6:>13.2f} {d['setup_ns_per_body_p99']/1e6:>7.2f} "
          f"{d['setup_ns_per_pair']:>7.0f} {d['qsteps_per_pair_p999']:>6}")
for s in (888, 999):
    g = {d['n']: d['deg_mean'] for d in rows if d['seed'] == s and d['n'] in (10000, 100000)}
    if len(g) == 2:
        print(f"P1 seed {s}: deg_mean(1e5)/deg_mean(1e4) = {g[100000]/g[10000]:.2f}")
u = [d for d in rows if d['n'] == 10000]
print(f"P7 means 888 vs 999 ns/pair: {u[0]['setup_ns_per_pair'] / u[1]['setup_ns_per_pair']:.2f}x")
