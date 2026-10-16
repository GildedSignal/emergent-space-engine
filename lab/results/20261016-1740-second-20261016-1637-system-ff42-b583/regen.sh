#!/bin/sh
# Regenerates every number in dossier.md from shipped code + work/patch.diff (applied by the
# runner before this runs; measured ~7 min). Arms are run interleaved pristine/patched so wall
# medians compare under one load; counts and digests are deterministic.
set -e
cd "$(dirname "$0")/../../.."   # repo root
D="$(dirname "$0")"
T=${CARGO_TARGET_DIR:-/home/glmlab/lab-target-0}
P="$D/work/patch.diff"

# --- pristine arm: reverse the patch, build, run ---------------------------------
git apply -R "$P"
cargo build --release -p xtask -p emergent-universe --example frame_digest 2>/dev/null
cp "$T/release/xtask" "$D/work/xtask-pristine"
cargo run --release -p emergent-universe --example frame_digest -- 3 burn 2>/dev/null | tee "$D/digest-pristine.txt"
for s in 3 7 11; do
  "$D/work/xtask-pristine" universe --kick-bench --seed $s --rtf 100 --seconds 8 > "$D/work/kb_pri_fly$s.json" 2>/dev/null
  "$D/work/xtask-pristine" universe --kick-bench --seed $s --rtf 1 --seconds 8 --members 4000 > "$D/work/kb_pri_bat$s.json" 2>/dev/null
done

# --- patched arm: re-apply, build, run --------------------------------------------
git apply "$P"
cargo build --release -p xtask -p emergent-universe --example frame_digest --example levelbench 2>/dev/null
cp "$T/release/xtask" "$D/work/xtask-patched"
cargo run --release -p emergent-universe --example frame_digest -- 3 burn 2>/dev/null | tee "$D/digest-patched.txt"
for s in 3 7 11; do
  "$D/work/xtask-patched" universe --kick-bench --seed $s --rtf 100 --seconds 8 > "$D/work/kb_pat_fly$s.json" 2>/dev/null
  "$D/work/xtask-patched" universe --kick-bench --seed $s --rtf 1 --seconds 8 --members 4000 > "$D/work/kb_pat_bat$s.json" 2>/dev/null
done

# --- the benches: the author's grid, the held-out battery, one case told in full ----
cargo run --release -p emergent-universe --example levelbench 2>/dev/null | tee "$D/bench.txt"
cargo run --release -p emergent-universe --example levelbench -- adv 2>/dev/null | tee "$D/adv.txt"
cargo run --release -p emergent-universe --example levelbench -- diag 2>/dev/null | tee "$D/diag.txt"

# --- the interleaved comparison table (digests, kick medians, guess counters) -------
python3 - "$D" <<'EOF' | tee "$D/flights.txt"
import json, sys
D = sys.argv[1]
print("seed arm   digest   pri_med pat_med  pri_p99  pat_p99   fires fallbacks win_reads reads/fire")
for s in (3, 7, 11):
    for pace in ("fly", "bat"):
        p = json.load(open(f"{D}/work/kb_pri_{pace}{s}.json"))
        q = json.load(open(f"{D}/work/kb_pat_{pace}{s}.json"))
        imp = q.get("impact_search", {"fires": 0, "fallbacks": 0, "window_readouts": 0})
        same = "SAME" if p["digest"] == q["digest"] else "DIFF!"
        pm, qm = p["kick_us_leavers"]["median"], q["kick_us_leavers"]["median"]
        pp, qp = p["kick_us_leavers"]["p99"], q["kick_us_leavers"]["p99"]
        rf = imp["window_readouts"] / max(imp["fires"], 1)
        print(f"s{s} {pace:3} {same:>5} {pm!s:>8} {qm!s:>8} {pp!s:>8} {qp!s:>8}  {imp['fires']:>5} {imp['fallbacks']:>9} {imp['window_readouts']:>10} {rf:.2f}")
EOF
diff -q "$D/digest-pristine.txt" "$D/digest-patched.txt" && echo "frame_digest: bit-identical"
echo DONE
