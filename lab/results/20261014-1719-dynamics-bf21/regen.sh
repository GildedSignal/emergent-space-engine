#!/bin/sh
# Regenerates every number in dossier.md. ~4 minutes on the lab's Linux box.
# The patch (work/patch.diff) is applied by the runner before this runs.
set -e
cd "$(dirname "$0")/../../.."
R=lab/results/20261014-1719-dynamics-bf21
cargo build --release -p emergent-universe --example wave_train --example wave_flight --example belt_first 2>&1 | grep -E "^error" && exit 1
# 1. The wave's first-item profile (shipped instrument, taleb-6138's arm)
cargo run --release -p emergent-universe --example belt_first -- 100000 2>/dev/null
# 2. The anatomy and the recurrence: the wave is a standing train (steps, second items)
cargo run --release -p emergent-universe --example wave_train -- 100000 2>/dev/null
# 3. The baseline flight: the monster frames (the env unset = shipped behaviour)
cargo run --release -p emergent-universe --example wave_flight -- 200000 burn 160 100 12 2>/dev/null | tee $R/regen-baseline.txt
# 4. The capped pull: same flight, same digest, no monster
ES_PULL_CAP=64 cargo run --release -p emergent-universe --example wave_flight -- 200000 burn 160 100 12 2>/dev/null | tee $R/regen-capped.txt
echo "digests:"; grep -h digest= $R/regen-baseline.txt $R/regen-capped.txt
