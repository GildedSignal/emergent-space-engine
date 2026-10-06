#!/usr/bin/env bash
# Print one GLM window's run commands, one per line (`start <lens> <min>` or `rung <file> <min>`): at most DIRECTED
# entries of lab/queue.txt with no published verdict (VOID and DISPUTED are retried, twice at most), then free lenses
# (each picks its own question) up to SLOTS. Julien, 6 October: "abuse GLM more, more diversity and usefulness".
SLOTS=${SLOTS:-4}; DIRECTED=${DIRECTED:-2}   # five spent GLM's 5-hour window in about 4 h 20 (6 October): four fit it
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
  echo "$kind $arg $min"; n=$((n + 1)); [ $n -eq "$DIRECTED" ] && break
done < lab/queue.txt
lenses=(dynamics system components scout autoresearch quant spacex taleb library redteam inversion fermi constraint)
k=$(( $(date -u +%s) / 3600 ))
for j in $(seq $n $((SLOTS - 1))); do echo "start ${lenses[$(( (k * SLOTS + j) % ${#lenses[@]} ))]} 60"; done
