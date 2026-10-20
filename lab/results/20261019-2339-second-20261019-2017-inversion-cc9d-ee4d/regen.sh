#!/usr/bin/env bash
# Regen: applies work/patch.diff's tree (the runner applies it before this runs), rebuilds the
# instrumented nladder (the 2017-inversion run's probe + RSS guard, plus this run's ES_ROOT_STREAM
# cure in crates/universe/src/universe.rs, the naive control, and the ES_IDENT canonical-cut digest
# mode), and reflies every arm of the dossier: the cure-on ladder, the disease contrast, and the
# identity quartet at 1e4/5e4. A PRIVATE target dir (a sibling run once replaced the shared target's
# binary mid-regen). Wall: ~4-6 min build (fresh deps) + ~4 min flights.
set -uo pipefail
cd "$(git rev-parse --show-toplevel)"
out=lab/results/20261019-2339-second-20261019-2017-inversion-cc9d-ee4d
mkdir -p "$out/out"
export CARGO_TARGET_DIR="$out/work/target"
cargo build --release -p emergent-universe --example nladder --features prof || exit 1
B="$CARGO_TARGET_DIR/release/examples/nladder"
[ -x "$B" ] || { echo "no binary"; exit 1; }
run() { local tag=$1; shift; echo "=== $tag: $* ==="; env "$@" timeout 120 "$B" ${ARGS[@]} > "$out/out/$tag.log" 2>&1; local rc=$?; grep -q "ladder:\|ident:" "$out/out/$tag.log" || { echo "NO OUTPUT in $tag (exit $rc)"; return 1; }; grep -E "^ladder:|^ident:" "$out/out/$tag.log"; }
# the cure-on ladder (ES_ROOT_STREAM=1) and its controls
ARGS=(10000 burn 20 1000 12);  run a1e4    ES_WAVE_PROBE=1 ES_ROOT_STREAM=1 || exit 1
ARGS=(50000 burn 24 1000 12);  run a5e4    ES_WAVE_PROBE=1 ES_ROOT_STREAM=1 || exit 1
ARGS=(100000 burn 24 1000 12); run a1e5    ES_WAVE_PROBE=1 ES_ROOT_STREAM=1 || exit 1
ARGS=(200000 burn 24 1000 12); run a2e5    ES_WAVE_PROBE=1 ES_ROOT_STREAM=1 ES_RSS_CAP_MB=1750 || exit 1
ARGS=(100000 burn 26 600 12);  run artf600 ES_WAVE_PROBE=1 ES_ROOT_STREAM=1 || exit 1
ARGS=(100000 coast 24 1000 12); run acoast ES_WAVE_PROBE=1 ES_ROOT_STREAM=1 || exit 1
# the disease, same box (the on-record contrast; the shipped path, flag unset)
ARGS=(10000 burn 20 1000 12);  run d1e4 ES_WAVE_PROBE=1 || exit 1
ARGS=(100000 burn 24 1000 12); run d1e5 ES_WAVE_PROBE=1 || exit 1
# the canonical-cut identity quartet at 1e4 and 5e4 (30k game-s past the burn's tick: past the wave)
for n in 10000 50000; do
  ARGS=($n burn 20 1000 12); run i${n}-off    ES_IDENT=30000 || exit 1
  ARGS=($n burn 20 1000 12); run i${n}-on     ES_IDENT=30000 ES_ROOT_STREAM=1 || exit 1
  ARGS=($n burn 20 1000 12); run i${n}-naive  ES_IDENT=30000 ES_ROOT_STREAM=naive || exit 1
  ARGS=($n burn 20 1000 12); run i${n}-ref    ES_IDENT=noflight:30000 || exit 1
done
echo; echo "— the collapse (cure on vs the disease, this box) and the wave's crest:"
python3 - "$out" <<'PY'
import re, sys, pathlib
o = pathlib.Path(sys.argv[1])
def lad(t):
    m = re.search(r"ladder: .*?p99_ms=([\d.]+) max_ms=([\d.]+) over=(\d+) lag_s=([\d.]+)", (o/"out"/f"{t}.log").read_text())
    g = re.search(r"^game ([\d.]+) s", (o/"out"/f"{t}.log").read_text(), re.M)
    return (float(m.group(1)), float(m.group(2)), int(m.group(3)), float(m.group(4)), float(g.group(1))) if m and g else None
print(f"{'arm':<9}{'p99_ms':>8}{'max_ms':>9}{'over':>6}{'lag_s':>8}{'game_s':>9}")
for t in ["a1e4","d1e4","a5e4","a1e5","d1e5","a2e5","artf600","acoast"]:
    r = lad(t)
    if r: print(f"{t:<9}{r[0]:>8.2f}{r[1]:>9.1f}{r[2]:>6}{r[3]:>8.1f}{r[4]:>9.0f}")
for t in ["a1e4","a5e4","a1e5","a2e5"]:
    log = (o/"out"/f"{t}.log").read_text()
    m = re.search(r">500 nested kicks: (\d+)", log)
    crest = re.search(r"heaviest three frames by events.*?\n  f (\d+)\s+([\d.]+) ms items (\d+).*?items_by_class \[(\d+), (\d+), (\d+), (\d+), (\d+)\]", log, re.S)
    if m and crest:
        print(f"{t}: mega-frames {m.group(1)}; crest f{crest.group(1)} {crest.group(2)} ms: {crest.group(3)} items = [{crest.group(4)}, {crest.group(5)}, {crest.group(6)}, {crest.group(7)}, {crest.group(8)}] (planet moon ship player fleet)")
print()
digests = {}
for n in ["10000","50000"]:
    for m in ["off","on","naive","ref"]:
        log = (o/"out"/f"i{n}-{m}.log").read_text()
        d = re.search(r"digest=(\w+) settle_s", log)
        k = re.search(r"kicks (\d+).*?encounters (\d+) contacts (\d+)", log)
        digests[f"{n}-{m}"] = d.group(1) if d else "MISSING"
        if d and k: print(f"i{n}-{m}: {d.group(1)[:16]}… kicks {k.group(1)} encounters {k.group(2)} contacts {k.group(3)}")
for n in ["10000","50000"]:
    same = len({digests[f"{n}-{m}"] for m in ["off","on","ref"]}) == 1
    print(f"{n}: off == on == noflight-reference: {'YES' if same else 'NO'}; naive == them: {'yes (does not bite here)' if digests[f'{n}-naive'] == digests[f'{n}-off'] else 'NO (bites)'}")
PY
rm -rf "$CARGO_TARGET_DIR"
