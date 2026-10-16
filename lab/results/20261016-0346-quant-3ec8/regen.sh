#!/usr/bin/env bash
# Regen: every number in dossier.md from shipped code + work/patch.diff (≤ 15 min).
set -eu
# Repo root: walk up from this script to the workspace Cargo.toml (never count '..' — the
# checkout depth differs between the author box and the runner).
D="$(cd "$(dirname "$0")" && pwd)"
while [ "$D" != "/" ] && [ ! -f "$D/Cargo.toml" ]; do D="$(dirname "$D")"; done
cd "$D"
RUN=lab/results/20261016-0346-quant-3ec8

# 1. The patch (idempotent: skip if already applied).
if ! git apply --check "$RUN/work/patch.diff" 2>/dev/null; then
  echo "patch already applied (or tree carries it); continuing"
else
  git apply "$RUN/work/patch.diff"
fi

cargo build --release -p emergent-universe --bin pass_bench
# ab.sh must run exactly the binary built above, whatever CARGO_TARGET_DIR resolves to.
TB="${CARGO_TARGET_DIR:-target}"
case "$TB" in /*) ;; *) TB="$D/$TB";; esac
export REGEN_PASS_BENCH="$TB/release/pass_bench"
# The pristine build: restore the two touched files, build apart, restore the patch.
cp crates/universe/src/step.rs /tmp/regen-step.rs
cp crates/universe/src/universe.rs /tmp/regen-universe.rs
git checkout -- crates/universe/src/step.rs crates/universe/src/universe.rs
CARGO_TARGET_DIR=/tmp/regen-pristine cargo build --release -p emergent-universe --bin pass_bench
cp /tmp/regen-step.rs crates/universe/src/step.rs
cp /tmp/regen-universe.rs crates/universe/src/universe.rs

# 3. The matrix (arms interleaved inside ab.sh; each arm a fresh process).
bash "$RUN/ab.sh" | tee "$RUN/ab.jsonl"

# 4. The pristine digest triangle (must equal the arm=0 digests of the same configs).
/tmp/regen-pristine/release/pass_bench 10000 1
/tmp/regen-pristine/release/pass_bench 300000 7

# 5. Summary table.
python3 - <<'EOF'
import statistics
rows=[]
for line in open('lab/results/20261016-0346-quant-3ec8/ab.jsonl'):
    d=dict(kv.partition('=')[::2] for kv in line.split())
    rows.append(dict(arm=d['arm'],n=int(d['n']),seed=d['seed'],
        plan_pb=int(d['plan_us'])/(int(d['n'])+28), build_pb=float(d['per_body_us']),
        rss=int(d['peak_rss_kb']), digest=d['digest']))
for (n,s) in sorted({(r['n'],r['seed']) for r in rows}):
    g=lambda a,k: statistics.mean([x[k] for x in rows if (x['n'],x['seed'],x['arm'])==(n,s,a)])
    dg={x['digest'] for x in rows if (x['n'],x['seed'])==(n,s)}
    print(f"{n:>7} s{s} | pass {g('0','plan_pb'):6.2f} -> {g('1','plan_pb'):6.2f} "
          f"(cut {g('0','plan_pb')-g('1','plan_pb'):5.2f}, {100*(g('0','plan_pb')-g('1','plan_pb'))/g('0','plan_pb'):4.1f}%) "
          f"| build {g('0','build_pb'):4.1f} -> {g('1','build_pb'):4.1f} | digest_eq={len(dg)==1}")
EOF

# 6. The suite with the patch in.
cargo test --release -p emergent-universe --lib --bins --tests 2>&1 | tail -3 | tee "$RUN/tests.txt"
echo REGEN_OK
