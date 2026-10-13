#!/bin/zsh
# Codex continues jobs that a Claude builder started (Julien, 13 October: "use gpt a lot"). Never merges.
# Usage: runner.sh <lane>; queue-<lane>.txt lines: <job> <model> <effort> <job file> [<base branch for a new worktree>]
# A job runs in /private/tmp/emergent-wt-<job> on wt/<job>: the existing worktree if there is one, else a new one from
# the base (default origin/main). On a usage limit it waits 45 min and resumes. Then it commits and pushes the branch.
R=$HOME/Research/emergent-space; C=/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex
D=$R/artifacts/runs/codex-oct13; LANE=$1; Q=$D/queue-$LANE.txt; S=$D/status-$LANE.txt
log() { echo "$(date -u +%FT%TZ) $*" >> $S; }
log "lane $LANE started"
while read -r job model effort file base; do
  [ -n "$job" ] || continue
  grep -q " done $job\$" $S 2>/dev/null && continue
  W=/private/tmp/emergent-wt-$job; J=$D/$job; mkdir -p $J
  cd $R && git fetch -q origin
  [ -d $W ] || git worktree add -q -B wt/$job $W ${base:-origin/main}
  { cat $R/$file
    printf '\n## You continue this job (%s, a builder; Claude Opus integrates)\n\n' $model
    printf 'Work only in `%s` (branch `wt/%s`). A previous builder (Claude Sonnet) did part of this job and was cut off by a usage limit: read `git log origin/main..HEAD` and its last commit first (the last one may be unverified work in progress). Verify what exists, finish the remaining items, run every gate the job file names, and report each before and after in your final message (at most 20 lines). Nothing merges to main. The sandbox may deny `.git/index.lock`: leave the work uncommitted; the runner commits it.\n' $W $job
  } > $J/prompt.md
  log "start $job ($model, $effort)"
  cd $W
  $C exec -m $model -c model_reasoning_effort="$effort" -c sandbox_mode="workspace-write" \
    -c "sandbox_workspace_write.writable_roots=[\"$R/.git\",\"$HOME/.cargo\",\"$W\",\"/private/tmp\"]" \
    -o $J/result.md - < $J/prompt.md > $J/log.txt 2>&1
  for attempt in 1 2 3 4 5 6 7 8 9 10; do
    [ -s $J/result.md ] && break
    grep -qiE "usage limit|rate limit|at capacity|try again" $J/log.txt || break
    log "$job hit a limit (attempt $attempt): waiting 45 min"; sleep 2700
    sid=$(grep -m1 -oE "session id: [0-9a-f-]+" $J/log.txt | cut -d' ' -f3)
    [ -n "$sid" ] || break
    echo "Continue the task from where you stopped; the limit has reset." | $C exec resume $sid -o $J/result.md - >> $J/log.txt 2>&1
  done
  cd $W && git add -A && git commit -qm "codex: $job ($model; continuing a Claude builder's job; not reviewed, not merged)

Built-by: $model
Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" 2>/dev/null
  git push -q -u origin wt/$job 2>>$S && log "done $job" || log "push failed $job"
done < $Q
log "lane $LANE finished its queue"
