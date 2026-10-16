#!/bin/sh
# Regenerates every dossier number from the shipped tree + work/patch.diff (applied by the runner
# before this runs). Wall ~9 min on the lab box (three parallel ladder_digest runs dominate).
set -e
cd "$(dirname "$0")/../../.."
export CARGO_TARGET_DIR=${CARGO_TARGET_DIR:-/home/glmlab/lab-target-917c2}
R="$CARGO_TARGET_DIR/release"
O=lab/results/20261016-0504-second-20261016-0346-spacex-917c-c840
mkdir -p "$O/gates" "$O/digest"

# 1. Build the patched binaries (the stagger + the probe; patch already applied by the runner).
cargo build --release -p xtask -p emergent-universe --example ladder_digest --example stagger_probe

# 2. A pristine ladder_digest (step.rs reverted), for the off-arm identity half of the record.
git diff crates/universe/src/step.rs > "$O/work/step-only.regendelta"
git checkout crates/universe/src/step.rs
cargo build --release -p emergent-universe --example ladder_digest
cp "$R/examples/ladder_digest" "$O/work/ladder_digest_pristine"
git apply "$O/work/step-only.regendelta"
cargo build --release -p emergent-universe --example ladder_digest --example stagger_probe

# 3. The digest record: pristine vs OFF vs ARMED (all three in parallel; timings stripped).
(env -u ES_STAGGER "$O/work/ladder_digest_pristine" > "$O/digest/digest_pristine.txt" 2>&1) &
(env -u ES_STAGGER "$R/examples/ladder_digest" > "$O/digest/digest_off.txt" 2>&1) &
(env ES_STAGGER=1 "$R/examples/ladder_digest" > "$O/digest/digest_armed.txt" 2>&1) &
wait
for f in pristine off armed; do sed "s/ \[[0-9.]* s\]$//" "$O/digest/digest_$f.txt" > "$O/digest/$f.cut"; done
echo "--- off vs pristine (the off arm must be bit-identical):"
diff "$O/digest/pristine.cut" "$O/digest/off.cut" && echo "OFF ARM: bit-identical to pristine"
echo "--- armed vs pristine (the stagger armed changes the digests):"
diff "$O/digest/pristine.cut" "$O/digest/armed.cut" | head -30 || true
echo "armed digest cases changed: $(diff "$O/digest/pristine.cut" "$O/digest/armed.cut" | grep -c '^<')"

# 4. The decisive gate: B13 armed vs off (the plane adapter births its ship bare, so the stagger
#    engages; ship id is 1 in every seed, so every seed eats the same 0.5666-step shift).
env -u ES_STAGGER "$R/xtask" behave --law plane --gates B13 > "$O/gates/B13_off.txt" 2>&1 || true
env ES_STAGGER=1 "$R/xtask" behave --law plane --gates B13 > "$O/gates/B13_armed.txt" 2>&1 || true
echo "B13 off:    $(grep '^B13' "$O/gates/B13_off.txt" | sed 's/ \[.*\]//')"
echo "B13 armed:  $(grep '^B13' "$O/gates/B13_armed.txt" | sed 's/ \[.*\]//')"

# 5. The frozen B14 (times out on the plane in both arms; the record's P3).
env -u ES_STAGGER timeout 100 "$R/xtask" behave --law plane --gates B14 > "$O/gates/B14_off.txt" 2>&1 || true
env ES_STAGGER=1 timeout 100 "$R/xtask" behave --law plane --gates B14 > "$O/gates/B14_armed.txt" 2>&1 || true
echo "B14 off:    $(grep '^B14' "$O/gates/B14_off.txt")"
echo "B14 armed:  $(grep '^B14' "$O/gates/B14_armed.txt")"

# 6. The B13/B14-class probe (fixed times, hex-exact states; moons carry the raw series).
env -u ES_STAGGER "$R/examples/stagger_probe" flyby > "$O/probe_flyby_off.txt" 2>/dev/null
env ES_STAGGER=1 "$R/examples/stagger_probe" flyby > "$O/probe_flyby_armed.txt" 2>/dev/null
env -u ES_STAGGER "$R/examples/stagger_probe" moon > "$O/probe_moon_off.txt" 2>/dev/null
env ES_STAGGER=1 "$R/examples/stagger_probe" moon > "$O/probe_moon_armed.txt" 2>/dev/null

# 7. The analysis (independent RK4 reference; reads the probe outputs).
python3 "$O/analyze.py" "$O" | tee "$O/probe_analysis.txt"
