#!/usr/bin/env bash
# Regenerates every number in the dossier from shipped code + work/patch.diff (applied by the runner
# before this runs). ~11 minutes: builds (2 min), belt arms 5×9 s, ladder matrix 2×~3 min, frame 2×8 s.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
W=lab/results/20261016-1459-quant-ff8c/work
mkdir -p "$W"

cargo build --release -p emergent-universe --features prof --example pos_carry
cargo build --release -p emergent-universe --example ladder_digest --example frame_digest
B=$(ls -d ~/lab-target-*/release/examples 2>/dev/null | head -1); B=${B:-target/release/examples}
[ -x "$B/pos_carry" ] || B=target/release/examples

# The belt flight, three arms, twice (variance): ROOT stage, kick items, counters, digest.
for arm in off on; do
  for rep in 1 2; do
    [ "$arm" = on ] && export ES_POS_CARRY=1 || unset ES_POS_CARRY
    "$B/pos_carry" 100000 20 1000 > "$W/belt_${arm}${rep}.txt" 2>&1
  done
done
unset ES_POS_CARRY
ES_POS_VERIFY=1 "$B/pos_carry" 100000 20 1000 > "$W/belt_verify.txt" 2>&1

# Digest matrices: every case must print one digest on every schedule, identical across arms.
"$B/ladder_digest" > "$W/ladder_off.txt" 2>&1
ES_POS_CARRY=1 "$B/ladder_digest" > "$W/ladder_on.txt" 2>&1
"$B/frame_digest" 2 > "$W/frame_off.txt" 2>&1
ES_POS_CARRY=1 "$B/frame_digest" 2 > "$W/frame_on.txt" 2>&1

echo "== ROOT stage and cycle (belt, OFF vs ON, two reps each) =="
grep -hE "^(ROOT total|kick_clock total|carry|digest|kicks)" "$W"/belt_{off1,off2,on1,on2,verify}.txt
echo "== ladder digests: identical across arms? =="
diff <(grep -oE '^[^|]+\| [0-9a-f]{32}' "$W/ladder_off.txt") <(grep -oE '^[^|]+\| [0-9a-f]{32}' "$W/ladder_on.txt") && echo "LADDER IDENTICAL"
echo "== frame digests: identical across arms? =="
diff <(grep -oE '\| [0-9a-f]{32} \|' "$W/frame_off.txt") <(grep -oE '\| [0-9a-f]{32} \|' "$W/frame_on.txt") && echo "FRAME IDENTICAL"
echo "== the identity instrument: mismatch must be 0 with hits > 0 =="
grep -E "^carry" "$W/belt_verify.txt"
