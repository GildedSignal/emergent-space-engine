#!/usr/bin/env bash
# Regenerates every dossier number from shipped code + work/patch.diff (applied by the runner).
# ~7 minutes: build (~45 s), seven sparse arms (~30 s each; sd4/sd2m400 ~10 s), one short dense
# identity arm (timeout is expected after the battle: the census is complete by then), analysis.
set -u
cd "$(dirname "$0")/../../.."   # repo root
# PRIVATE target dir: the machine's shared target directory is also built by sibling lab
# runs from clean trees, which silently replaces this run's patched rlibs mid-flight (it
# happened once: every fast arm came back at shipped speed). A private dir costs one clean
# build (~1 min) and cannot be raced.
TARGET=$PWD/lab/results/20261018-1617-spacex-37c1/target
BIN=${BIN:-$TARGET/release/xtask}
OUT=lab/results/20261018-1617-spacex-37c1
mkdir -p "$OUT/cens"

# unset the ambient CARGO_TARGET_DIR (the shared lab-target-1): sibling runs rebuild it from
# clean trees and replace patched rlibs mid-flight — once, every fast arm silently came back
# at shipped speed. This dir is this run's alone.
env -u CARGO_TARGET_DIR CARGO_TARGET_DIR=$TARGET cargo build --release -p xtask || exit 1

run() { # arm seed members speed_div order seconds
  local arm=$1 seed=$2 mem=$3 sd=$4 ord=$5 secs=$6
  echo "== arm $arm (seed $seed members $mem speed_div $sd order $ord, ${secs}s of game)" >&2
  SPACEX_CENSUS=1 SPACEX_SPEED_DIV=$sd SPACEX_ORDER=$ord timeout 150 "$BIN" universe \
    --bench --unpaced --rtf 100 --seconds "$secs" --seed "$seed" --members "$mem" \
    >/dev/null 2>"$OUT/cens/$arm.cens" || echo "  (arm $arm exited nonzero; census kept)" >&2
}
run ship48   1 48  32768 sparse 30
run ship400  1 400 32768 sparse 30
run sd128    1 48  128   sparse 30
run sd8      1 48  8     sparse 30
run sd4      1 48  4     sparse 30
run sd2      1 48  2     sparse 30
run sd2s2    2 48  2     sparse 30
run sd2m400  1 400 2     sparse 30
# Dense control: the same world through Chronon. 3 s of game covers the whole battle (41
# contacts); the run is then killed by timeout while the dense stepper grinds on — expected.
run sd2dense 1 48  2     dense  3

echo "== summary (skip ⟺ dw ≥ 0 at the resolve instant; ρ = reach/|w|)"
python3 "$OUT/analyze.py" "$OUT"/cens/*.cens | tee "$OUT/cens/summary.txt"

echo "== dense-vs-sparse census identity"
if cmp -s "$OUT/cens/sd2.cens" "$OUT/cens/sd2dense.cens"; then echo "IDENTICAL"; else echo "DIFFER"; fi

echo "== per-contact tau* = −dw/|w|² at resolve (the mechanism table: skips sit in (−1, 0))"
python3 - "$OUT" > "$OUT/cens/tau-star.txt" <<'EOF'
import sys, math
out = sys.argv[1]
for name in ["sd2", "sd2s2"]:
    print(f"== {name}")
    rows = []
    for line in open(f"{out}/cens/{name}.cens"):
        p = line.split()
        if p[0] != "CENSUS": continue
        ww, dw, reach = map(int, p[1:4])
        rows.append((-dw / ww if ww else float("nan"), reach / math.isqrt(ww) if ww else float("inf"), dw >= 0))
    rows.sort()
    for tau, rho, sk in rows:
        print(f"  tau*={tau:+9.3f}  rho={rho:8.3f}  {'SKIP' if sk else ''}")
EOF
cat "$OUT/cens/tau-star.txt"
