#!/bin/sh
# Regen for 20261018-1237-dynamics-9dbb: every dossier number, from shipped code
# + work/patch.diff (adds crates/universe/examples/seam_walk.rs, the walk-class
# probe; carries b9c8's seam_cycle.rs for the control). Cold build ~1-2 min;
# probe 7 s; control 20 s.
set -e
cd "$(dirname "$0")/../../.."
RUN=lab/results/20261018-1237-dynamics-9dbb

if [ ! -f crates/universe/examples/seam_walk.rs ]; then
  git apply "$RUN/work/patch.diff"
fi
cargo run --release -p emergent-universe --example seam_walk -- "$RUN/series" | tee "$RUN/probe-stdout.txt"
python3 "$RUN/analyze.py" "$RUN/series" | tee "$RUN/analysis.txt"

# Control: b9c8's own probe, unmodified, on this tree must reproduce its stored
# record (all dr_rel below the 2^-20 integer floor; 92/864 key-cyclic). This is
# the check that the shipped fit/decode code is unchanged since 14 October and
# that this run's nonzero (finer) dr numbers are sub-floor, not a code change.
git show origin/claude/lab-20261014-1137-second-20261014-1010-taleb-292a-b9c8:lab/results/20261014-1137-second-20261014-1010-taleb-292a-b9c8/work/patch.diff > /tmp/b9c8-control.patch
git apply /tmp/b9c8-control.patch 2>/dev/null || echo "seam_cycle.rs already present (carried by this run's patch)"
cargo run --release -p emergent-universe --example seam_cycle -- "$RUN/b9c8-control.json" 256 > "$RUN/b9c8-control-stdout.txt" 2>&1
rm -f crates/universe/examples/seam_cycle.rs
python3 - "$RUN/b9c8-control.json" <<'EOF'
import json, sys
NL = chr(10)
rows = json.loads(open(sys.argv[1]).read().replace('},' + NL + ']', '}' + NL + ']'))
nz = [r for r in rows if r['dr_rel'] != 0]
cyc = sum(1 for r in rows if r['cycle_at'] is not None)
print(f"b9c8 control on this tree: chains={len(rows)} nonzero-dr_rel={len(nz)} (expect 0: sub-floor) key-cyclic={cyc} (expect 92)")
assert len(rows) == 864 and not nz and cyc == 92, "control mismatch: shipped code changed or probe broken"
EOF
echo "regen: all numbers regenerated"
