#!/bin/bash
# Regenerates every number in the dossier from shipped code. ~12 min on 8 vCPU Linux.
set -eu
cd "$(git rev-parse --show-toplevel)"
RUN=lab/results/20261014-0059-inversion-8e84
STALE=artifacts/flights
FRESH=$RUN/corpus-fresh
OUT=$RUN/regen-logs
mkdir -p "$OUT"
gate() { local out rc; out=$(cargo run --release -q -p xtask -- universe --replay-all --flights "$1" 2>&1); rc=$?
  { echo "$out"; echo "exit=$rc"; } | tee "$OUT/$2.txt" | tail -1; }

echo "== build (clean law crates) =="
find crates -name '*.rs' -exec touch {} +
cargo build --release -q -p xtask

echo "== baselines =="
gate "$STALE" "baseline-stale"        # expect: 3 changed, 0 regression(s), exit=0
gate "$FRESH" "baseline-fresh"        # expect: 3 same, 0 regression(s), exit=0  (if corpus-fresh absent, build it below first)

# Build the fresh corpus from the current tree if it is missing (the committed one was built at 33c83f1ab483).
if [ ! -d "$FRESH" ]; then
  mkdir -p "$FRESH"
  python3 - <<'PY'
import json, glob, subprocess, re
digs, law, commit = {}, None, None
for f in sorted(glob.glob("artifacts/flights/*.json")):
    out = subprocess.run(["cargo","run","--release","-q","-p","xtask","--","universe","--replay",f],
                         capture_output=True, text=True).stdout
    d = re.search(r"^digest\s+(\S+)", out, re.M).group(1)
    digs[f.split("/")[-1]] = d
    law = law or re.search(r"law \S+ #(\S+)", out).group(1)
    commit = commit or re.search(r"now\s+(\S+)", out).group(1)
for f in glob.glob("artifacts/flights/*.json"):
    j = json.load(open(f)); n = f.split("/")[-1]
    j.update(digest=digs[n], law_hash=law, commit=commit, dirty=False)
    json.dump(j, open(f"lab/results/20261014-0059-inversion-8e84/corpus-fresh/{n}","w"))
PY
  gate "$FRESH" "baseline-fresh"
fi

echo "== mutant panel (git-checkout + touch restores; the v2 protocol) =="
apply() { python3 - "$1" <<'PY'
import sys
mid = sys.argv[1]
def edit(path, lineno, old, new):
    ls = open(path).read().split("\n")
    assert old in ls[lineno-1], f"{path}:{lineno} !contains {old!r}"
    ls[lineno-1] = ls[lineno-1].replace(old, new); open(path,"w").write("\n".join(ls))
if mid=="M-wrap": edit("crates/lattice/src/law.rs",337,"hit_narrow(d, w, reach).unwrap_or_else(|| hit_in(d.map(Wide::of), w.map(Wide::of), Wide::of(reach)))","hit_in(d, w, reach)")
elif mid=="M-sign": edit("crates/universe/src/force.rs",89,"Ok((scale2(d, k)?, r))","Ok((scale2(d, k.negate())?, r))")
elif mid=="M-thrust": edit("crates/universe/src/ctx.rs",44,"thrust_log2: -44","thrust_log2: -45")
elif mid=="M-kick": edit("crates/universe/src/step.rs",440,"len: self.rec.interval >> (2 * level as i64)","len: self.rec.interval >> (2 * level as i64 + 1)")
elif mid=="M-bind": edit("crates/universe/src/bind.rs",233,"if len <= cur_len && vel <= cur_vel {","if len <= cur_len + 1 && vel <= cur_vel + 1 {")
elif mid=="M-prune": edit("crates/universe/src/universe.rs",1105,"+ (1 << 26)","+ (1 << 20)")
PY
}
for m in M-wrap M-sign M-thrust M-kick M-bind M-prune; do
  case $m in
    M-wrap) f=crates/lattice/src/law.rs;; M-sign) f=crates/universe/src/force.rs;;
    M-thrust) f=crates/universe/src/ctx.rs;; M-kick) f=crates/universe/src/step.rs;;
    M-bind) f=crates/universe/src/bind.rs;; M-prune) f=crates/universe/src/universe.rs;;
  esac
  git checkout -- "$f"; apply "$m"; touch "$f"
  cargo build --release -q -p xtask
  gate "$STALE" "$m-stale"; gate "$FRESH" "$m-fresh"
  git checkout -- "$f"; touch "$f"
done
cargo build --release -q -p xtask
gate "$STALE" "restore-stale"; gate "$FRESH" "restore-fresh"   # must equal the baselines
echo "== done: compare $RUN/regen-logs against the dossier table =="
