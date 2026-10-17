# regen.sh — regenerates every dossier number from shipped code + work/patch.diff (< 15 min on the lab box)
set -e
cd "$(dirname "$0")/../.."   # repo root
git apply lab/results/20261017-1535-taleb-ce22/work/patch.diff 2>/dev/null \
  || echo "patch not applied (already present or tree dirty) - continuing"
cargo build --release -p emergent-universe --example nladder --example ladder_digest
B=/home/glmlab/lab-target-3/release/examples
[ -x $B/nladder ] || B=target/release/examples
echo "== A0 exodus (N=0, promotions channel) =="
ES_MEMO_ORACLE=1 timeout 58 $B/nladder 0 coast 8 100 2>&1 | grep -E "memo_oracle: calls|worst frames"
echo "== A1 coast N=1e4 (wave + spread, 45 s at rtf 600) =="
ES_MEMO_ORACLE=1 timeout 58 $B/nladder 10000 coast 45 600 2>&1 | grep -E "memo_oracle: (calls|doll)|game .*after the first"
echo "== A2 burn N=1e4 (held out) =="
ES_MEMO_ORACLE=1 timeout 58 $B/nladder 10000 burn 45 600 2>&1 | grep -E "memo_oracle: calls"
echo "== A3 coast N=3e4 (held out, 5eb2's arm) =="
ES_MEMO_ORACLE=1 timeout 58 $B/nladder 30000 coast 30 600 2>&1 | grep -E "memo_oracle: (calls|doll)"
echo "== digest identity, oracle off vs on (N=3000 mashing), modulo wall-time annotations =="
timeout 120 $B/ladder_digest "N=3000" 2>&1 | grep -v "^\[" > /tmp/r_off.txt || true
ES_MEMO_ORACLE=1 timeout 120 $B/ladder_digest "N=3000" 2>&1 | grep -v "^\[" > /tmp/r_on.txt || true
sed 's/ \[[0-9.]* s\]//' /tmp/r_off.txt > /tmp/r_off2.txt; sed 's/ \[[0-9.]* s\]//' /tmp/r_on.txt > /tmp/r_on2.txt
diff /tmp/r_off2.txt /tmp/r_on2.txt && echo DIGESTS_IDENTICAL_MODULO_TIMES
echo "== window curve (A1): first and late windows =="
echo "regen done"
