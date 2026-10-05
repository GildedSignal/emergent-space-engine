#!/usr/bin/env bash
# Print one GLM window's three run commands, one per line (`start <lens> <min>` or `rung <file> <min>`):
# the first entries of lab/queue.txt with no published verdict (VOID and DISPUTED are retried, twice at most), then the lens rotation.
cd "$(git rev-parse --show-toplevel)"
git fetch -q origin '+refs/heads/claude/lab-*:refs/remotes/origin/claude/lab-*' 2>/dev/null || true
state() {  # state <slug>: "done" if a published result is not VOID or DISPUTED, else how many were
  local v=0 b
  for b in $(git for-each-ref --format='%(refname:short)' "refs/remotes/origin/claude/lab-*-$1-????"); do
    git log -1 --format=%s "$b" | grep -qE "VOID|DISPUTED" && v=$((v + 1)) || { echo done; return; }
  done
  echo "$v"
}
n=0
while read -r kind arg min; do
  case $kind in rung) slug=rung-$(basename "$arg" .md) ;; start) slug=$arg ;; *) continue ;; esac
  s=$(state "$slug"); { [ "$s" = done ] || [ "$s" -ge 2 ]; } && continue
  echo "$kind $arg $min"; n=$((n + 1)); [ $n -eq 3 ] && exit 0
done < lab/queue.txt
lenses=(dynamics system components scout autoresearch quant spacex taleb library redteam)
k=$(( $(date -u +%s) / 18000 ))
for j in $(seq $n 2); do echo "start ${lenses[$(( (k * 3 + j) % ${#lenses[@]} ))]} 60"; done
