#!/usr/bin/env bash
# Regen: every number in dossier.md from pristine main + work/patch.diff
# (= f134's composed-law patch verbatim on crates/ + 87fd's doll_probe example verbatim
# + this run's print-only mixture-witness lines). Ten flights of <= 14 s wall each; ~1 min
# of flights plus one ~20 s build (deps cached).
set -euo pipefail
RUN="$(cd "$(dirname "$0")" && pwd)"
cd "$RUN/../../.."  # repo root

# 1. Apply the patch if the tree is clean of it.
if ! grep -q "ES_SECULAR" crates/universe/src/step.rs || [ ! -f crates/universe/examples/doll_probe.rs ]; then
  git apply "$RUN/work/patch.diff"
  grep -q "ES_SECULAR" crates/universe/src/step.rs && [ -f crates/universe/examples/doll_probe.rs ] \
    || { echo "ERROR: patch did not apply"; exit 1; }
fi
echo "tree: $(git rev-parse HEAD) (composed patch + doll_probe applied)"

# 2. Build.
cargo build --release -p emergent-universe --example doll_probe
B="$(cargo metadata --format-version 1 --no-deps | sed -n 's/.*"target_directory":"\([^"]*\)".*/\1/p')/release/examples/doll_probe"
[ -x "$B" ] || { echo "ERROR: no doll_probe binary"; exit 1; }
mkdir -p "$RUN/flights"

run () {  # run <label> <seconds> <seed> <env...>
  local label=$1 secs=$2 seed=$3; shift 3
  echo "=== $label: doll_probe 1000 ${secs}s rtf 100 seed $seed ($*)"
  env "$@" "$B" 1000 "$secs" 100 "$seed" > "$RUN/flights/$label.txt" 2>&1
  grep -hE "frames:|dE/E0|dL/L0" "$RUN/flights/$label.txt" | head -4
}
BOTH=(ES_SECULAR=1 ES_CHAIN=1 ES_LOCAL_STAGGER=1); CS=(ES_CHAIN=1 ES_LOCAL_STAGGER=1)

# 3. Arming controls: OFF and chain+stagger at 4,500 gs must reproduce 87fd's frozen table
#    (off: 251/136/7,736/183, med 2.0e-6; cs: med 7.4e-6), and BOTH must reproduce f134's
#    collapse class (max 41).
run off_45        45 1
run cs_45         45 1 "${CS[@]}"
run both_45       45 1 "${BOTH[@]}"

# 4. The decisive arms: 9,000 and 11,000 gs (the worst horizons; 87fd-checker's crossing).
run off_90        90 1
run cs_90         90 1 "${CS[@]}"
run both_90       90 1 "${BOTH[@]}"
run off_110      110 1
run cs_110       110 1 "${CS[@]}"
run both_110     110 1 "${BOTH[@]}"

# 5. Held-out seed at the worst horizon.
run off_110_s2   110 2
run both_110_s2  110 2 "${BOTH[@]}"

# 6. The ensemble deviations (P4): med of E1/L1/r1, cross-arm (composed vs OFF), per horizon.
echo "--- ensemble deviation (composed vs OFF), med of E1/L1/r1, relative ---"
python3 - "$RUN/flights" <<'EOF'
import sys, os, re
d = sys.argv[1]
def med(path, name):
    for line in open(path):
        if line.strip().startswith(name + ":"):
            return float(re.search(r"med ([-\d.e+]+)", line).group(1))
    raise SystemExit(f"no {name} in {path}")
for h in ("45", "90", "110"):
    for name in ("E1", "L1", "r1"):
        o = med(f"{d}/off_{h}.txt", name); b = med(f"{d}/both_{h}.txt", name)
        print(f"h{h} {name} off {o:.6e} both {b:.6e} reldev {abs(b-o)/abs(o):.2e}")
for name in ("E1", "L1", "r1"):
    o = med(f"{d}/off_110_s2.txt", name); b = med(f"{d}/both_110_s2.txt", name)
    print(f"s2 h110 {name} off {o:.6e} both {b:.6e} reldev {abs(b-o)/abs(o):.2e}")
EOF
echo DONE
