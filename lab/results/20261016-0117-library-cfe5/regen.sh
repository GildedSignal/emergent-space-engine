#!/bin/sh
# Regen: every number in dossier.md, from shipped code.
# run.sh's patch capture came back empty (work/patch.diff is 0 bytes), so the probe travels
# here: work/probe.patch carries the sec_probe instrumentation (ctx.rs/step.rs/universe.rs
# counters + ES_SEC_HOIST memo + the example), applied, built, flown on the 8-arm grid,
# then the tree is restored. Each flight is well under 60 s.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
cd "$HERE/../../.." || exit 1
restore() { git apply -R --recount "$HERE/work/probe.patch" >/dev/null 2>&1 || true; }
trap restore EXIT
[ -s "$HERE/work/patch.diff" ] && git apply "$HERE/work/patch.diff"
git apply --recount "$HERE/work/probe.patch"
cargo build --release -p emergent-universe --example sec_probe
P=$(cargo metadata --format-version 1 --no-deps | python3 -c "import json,sys; print(json.load(sys.stdin)['target_directory'])")/release/examples/sec_probe
for n in 10000 100000; do for s in 1 7; do for h in 0 1; do
  ES_BIRTH_SPLIT=1 ES_SEC_HOIST=$h "$P" "$n" "$s"
done; done; done
