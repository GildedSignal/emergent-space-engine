#!/usr/bin/env bash
# The contradiction probe (this run's one sanctioned experiment, ≤ 10 min):
# 3cfc says the fleet exodus is one indivisible 0.6–1.5 s item breaking
# smoothness at ~1,600 members; ba35 says the time is hand-out events already
# split across frames by the 5 ms budget. Decisive observable on shipped code:
# the delivered frame loop's worst_hitch_ms at overlapping member counts.
# Requires work/patch.diff applied (the one-line --members clamp lift).
set -euo pipefail
B="${XTASK:-/home/glmlab/lab-target-probe/release/xtask}"
for m in 1600 3200 4000 6400; do
  echo "=== members $m"
  timeout 110 "$B" universe --bench --seconds 10 --rtf 100 --members "$m" 2>&1 \
    | python3 -c "
import sys, json
txt = sys.stdin.read(); i = txt.find('{')
d = json.loads(txt[i:]) if i >= 0 else {}
for k in ('worst_hitch_ms', 'worst_hitch_at_frame', 'frames',
          'events_per_second', 'digest'):
    if k in d:
        print(f'  {k}: {d[k]}')
"
done
# 12,800 members exceeds the 110 s window on this box (the scene alone builds
# for tens of seconds); left unmeasured and disclosed in the dossier.
