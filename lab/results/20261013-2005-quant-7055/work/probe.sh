#!/bin/sh
# lab run 20261013-2005-quant-7055: the hand-out's compile-key identity and the exact memo.
# Usage: probe.sh <xtask-binary> <outdir>. Arms: A = base, B = keys logged, C = exact memo on.
set -e
X=$1
OUT=$2
cd "$(dirname "$0")/../../.."   # repo root
mkdir -p "$OUT"
run () { # name members rtf seconds seed [env assignments...]
  name=$1; m=$2; rtf=$3; secs=$4; seed=$5; shift 5
  echo "== $name (members $m rtf $rtf s $secs seed $seed) env: $*"
  env "$@" $X universe --bench --seed "$seed" --rtf "$rtf" --seconds "$secs" --unpaced --members "$m" > "$OUT/$name.json"
}
for spec in "m48:48:1:8:1" "m400:400:1:8:1" "m1500:1500:1:8:1" "m4000:4000:1:8:1" "m4000s3:4000:1:8:3" "m400rtf100:400:100:8:1"; do
  name=${spec%%:*}; rest=${spec#*:}; m=${rest%%:*}; rest=${rest#*:}; rtf=${rest%%:*}; rest=${rest#*:}; secs=${rest%%:*}; seed=${rest#*:}
  run "${name}_A" "$m" "$rtf" "$secs" "$seed" ES_PROBE_ARM=A
  run "${name}_B" "$m" "$rtf" "$secs" "$seed" "ES_ORBIT_KEYS=$OUT/${name}_keys.csv"
  run "${name}_C" "$m" "$rtf" "$secs" "$seed" ES_PROBE_ARM=C ES_ORBIT_MEMO=1
done
echo done
