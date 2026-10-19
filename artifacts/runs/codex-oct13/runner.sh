#!/bin/zsh
# Codex continues jobs that a Claude builder started (Julien, 13 October: "use gpt a lot"). Never merges.
# Usage: runner.sh <lane>; queue-<lane>.txt lines: <job> <model> <effort> <job file> [<base branch for a new worktree>]
# A job runs in ~/Research/emergent-wt/<job> on wt/<job> (never /private/tmp: a restart wiped it on 14 October): the existing worktree if there is one, else a new one from
# the base (default origin/main). On a usage limit it waits 45 min and resumes. Then it commits and pushes the branch.
R=$HOME/Research/emergent-space; C=/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex
D=$R/artifacts/runs/codex-oct13; LANE=$1; Q=$D/queue-$LANE.txt; S=$D/status-$LANE.txt
log() { echo "$(date -u +%FT%TZ) $*" >> $S; }
# Julien's GPT time (14 October: "let me have usage from 4 to 12pm"): no GPT call from 12:45 to midnight Paris time, so his
# window from 16:00 is whole.
inquiet() { local hm=$(TZ=Europe/Paris date +%H%M); [ "$hm" -ge 1245 ]; }
quiet() { while inquiet; do sleep 300; done; }
# The Mac froze at 00:26 on 14 October (a watchdog reset) under a night job: at most two compile jobs, and no job starts
# while less than 15% of memory is free.
export CARGO_BUILD_JOBS=2
roomy() { while [ "$(memory_pressure -Q | grep -oE '[0-9]+%' | tr -d %)" -lt 15 ]; do log "waiting for memory"; sleep 300; done; }
# A real Codex error line, never the prompt's own words (the log echoes the prompt).
limited() { grep -E "^ERROR" $J/log.txt | grep -qiE "usage limit|rate limit|at capacity|try again"; }
log "lane $LANE started"
while read -r job model effort file base; do
  [ -n "$job" ] || continue
  grep -q " done $job\$" $S 2>/dev/null && continue
  W=$HOME/Research/emergent-wt/$job; J=$D/$job; mkdir -p $J $HOME/Research/emergent-wt
  cd $R && git fetch -q origin
  if [ -d $W ]; then cont=1; else cont=0; git worktree add -q -B wt/$job $W ${base:-origin/main}; fi
  { cat $R/$file
    printf '\n## You continue this job (%s, a builder; Claude Opus integrates)\n\n' $model
    printf 'Work only in `%s` (branch `wt/%s`, started from `%s`). ' $W $job ${base:-origin/main}
    [ $cont = 1 ] && printf 'A previous builder did part of this job and was cut off: read `git log origin/main..HEAD` and its last commit first (the last one may be unverified work in progress). Verify what exists and finish the remaining items. '
    printf 'Run every gate the job file names, and report each before and after in your final message (at most 20 lines). Nothing merges to main; never edit docs/HANDOFF.md or lab/wiki. The sandbox may deny `.git/index.lock`: leave the work uncommitted; the runner commits it.\n'
  } > $J/prompt.md
  quiet; roomy; log "start $job ($model, $effort)"
  cd $W
  $C exec -m $model -c model_reasoning_effort="$effort" -c sandbox_mode="workspace-write" \
    -c "sandbox_workspace_write.writable_roots=[\"$R/.git\",\"$HOME/.cargo\",\"$W\",\"/private/tmp\"]" \
    -o $J/result.md - < $J/prompt.md > $J/log.txt 2>&1
  for attempt in 1 2 3 4 5 6 7 8 9 10; do
    [ -s $J/result.md ] && break
    if limited; then
      if grep -E "^ERROR" $J/log.txt | grep -qi "capacity"; then log "$job: model at capacity (attempt $attempt): retry in 10 min"; sleep 600
      else log "$job hit a limit (attempt $attempt): waiting 45 min"; sleep 2700; fi
    elif inquiet; then log "$job paused for Julien's GPT hours (12:45-24:00 Paris): resuming at midnight"
    else break; fi
    quiet
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
