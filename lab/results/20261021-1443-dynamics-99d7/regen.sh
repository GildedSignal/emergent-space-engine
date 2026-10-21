#!/bin/sh
# Regen: every number in dossier.md. Linux x86, ~4 min. Applies nothing: run.sh applies
# work/patch.diff (adds examples/beltzone.rs) before this runs.
set -e
cd "$(dirname "$0")/../../.."   # repo root
OUT=lab/results/20261021-1443-dynamics-99d7/regen.txt
cargo build --release -p emergent-universe --example beltzone
B="cargo run --release -q -p emergent-universe --example beltzone"
{
run() { d="$1"; shift; echo "== $d =="; SEED="${S:-}" timeout 600 env "$@" 2>&1 | grep -E "draws|^step|^phi|gone" || true; }
S= run "zone31 s1 step 8" $B 8 100 6 zone31
S= run "zone31 s1 step 6" $B 6 100 6 zone31
S= run "zone31 s1 step 5" $B 5 100 6 zone31
S= run "zone31 s1 step 4" $B 4 100 6 zone31
S= run "zone31 s1 step 3" $B 3 100 6 zone31
S=88172645463300152 run "zone31 s2 step 4" $B 4 100 6 zone31
S=88172645463300152 run "zone31 s2 step 6" $B 6 100 6 zone31
S= run "zone31 400p step 4" $B 4 400 6 zone31
S= run "core step 4" $B 4 100 6 core
S= run "scan e=0.10 step 6" ECCMILLI=100 $B 6 200 25 scan
S= run "scan e=0.20 step 6" ECCMILLI=200 $B 6 200 25 scan
S= run "scan e=0.30 step 6" ECCMILLI=300 $B 6 200 25 scan
S= run "scan e=0.20 step 4" ECCMILLI=200 $B 4 200 25 scan
S= run "fine grid e=0.20 step 4" ECCMILLI=200 FRACSPAN=0.4 $B 4 200 17 scan
S= run "ridge 400p step 4" ECCMILLI=200 FRACC=-0.22 FRACSPAN=0.16 $B 4 400 9 scan
S= run "5:2 scan e=0.10 step 4" ARESC=1.1295 $B 4 200 25 scan
S= run "5:2 e-law step 4" ARESC=1.1295 $B 4 100 6 zone31
S= run "5:2 e-law step 6" ARESC=1.1295 $B 6 100 6 zone31
S= run "bridge s1 step 6" $B 6 100 6 bridge
S= run "bridge s1 step 5" $B 5 100 6 bridge
S= run "bridge s1 step 4" $B 4 100 6 bridge
S= run "bridge s1 step 3" $B 3 100 6 bridge
S=88172645463300152 run "bridge s2 step 4" $B 4 100 6 bridge
S= run "bridge 400p step 4" $B 4 400 6 bridge
S= run "belte step 4" $B 4 100 6 belte
S= run "strong step 5" $B 5 100 6 strong
S= run "strong step 4" $B 4 100 6 strong
echo "== composed headroom =="
python3 - <<'EOF'
p = 0.334  # mean p_own/p_g over the belt's [2,3) AU at the Giant's 5.194 AU
cons = 2*(0.412*16*p + 0.410*64*p + 0.178*256)
meas = 2*(0.989*16*p + 0.011*256)
allo16 = 2*16*p
print(f"events/body/belt-orbit: ddeb conservative {cons:.1f} (78x) | measured {meas:.1f} -> headroom {9000/meas:.0f}x | all-16 {allo16:.1f} -> {9000/allo16:.0f}x")
EOF
} | tee "$OUT"
