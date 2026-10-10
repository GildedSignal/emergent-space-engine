#!/usr/bin/env python3
"""Median of per-run kick_us medians over N reps, per seed. Digests checked against a map."""
import json, subprocess, sys, statistics

REPS = int(sys.argv[1]) if len(sys.argv) > 1 else 15
BIN = "/home/glmlab/lab-target-1/release/xtask"
KNOWN = {}  # seed -> digest prefix seen in this measurement (first rep)
import os
for seed in [int(x) for x in os.environ.get('SEEDS','1 2 3').split()]:
    meds, p99s = [], []
    for _ in range(REPS):
        out = subprocess.run([BIN, "universe", "--kick-bench", "--seconds", "2", "--seed", str(seed)],
                             capture_output=True, text=True, check=True).stdout
        d = json.loads(out)
        dig = d["digest"][:16]
        KNOWN.setdefault(seed, dig)
        assert dig == KNOWN[seed], f"digest drift on seed {seed}: {dig} != {KNOWN[seed]}"
        meds.append(d["kick_us"]["median"]); p99s.append(d["kick_us"]["p99"])
    print(f"seed {seed}: median {statistics.median(meds):7.3f} us  (reps min {min(meds):.2f} max {max(meds):.2f})  p99 {statistics.median(p99s):7.2f}  digest {KNOWN[seed]}")
