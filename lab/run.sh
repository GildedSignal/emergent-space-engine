#!/usr/bin/env bash
# The GLM lab runner (see lab/README.md). Linux only: agonbox as glmlab, or GitHub's machines; never Julien's Mac.
#   lab/run.sh start <lens> [author-minutes]   starts a run in the background and prints its id
#   lab/run.sh rung <rung.md> [author-minutes] the same for a committed, unchanged rung file (lab/canaries/)
#   lab/run.sh wait <id>                       waits up to 9 minutes; prints the grade or verdict line when done
set -uo pipefail
cd "$(git rev-parse --show-toplevel)"
export PATH="$HOME/.local/bin:$PATH"
GLM=(omp -p --model=zai/glm-5.3 --thinking=high --approval-mode=yolo --no-session)

preamble() {  # PRINCIPLES' goal and philosophy, verbatim, then the lab's charter and board
  sed -n '/^## The goal/,/^## Proposed/p' docs/PRINCIPLES.md | sed '$d'
  printf '\n'; cat lab/README.md; printf '\n'; cat lab/board.md; printf '\n'
}
restore() { git reset -q; git checkout -q -- .; git clean -fdq -e lab/results; }
guard_linux() { [ "$(uname)" = Linux ] || { echo "Linux only (GitHub's machines or agonbox as glmlab): never on Julien's Mac"; exit 2; }; }
guard_key() {
  [ -n "${ZAI_API_KEY:-}" ] || { echo "ZAI_API_KEY is not set in this cloud environment"; exit 2; }
  command -v omp >/dev/null || bash lab/setup.sh || exit 2
}
launch() { mkdir -p "lab/results/$id/work"; nohup bash lab/run.sh "$@" > "lab/results/$id/run.log" 2>&1 & echo "$id"; }
phase() {  # phase <name> <minutes> [patch]: one GLM session on $out/<name>-prompt.md; its edits saved as work/<patch>; tree restored
  "${GLM[@]}" --max-time="${2}m" @"$out/$1-prompt.md" > "$out/$1-final.md" 2>&1
  [ -z "${3:-}" ] || { git add -N . && git diff "$base" -- . ':(exclude)lab/results' > "$out/work/$3"; }
  restore
}
finish() {  # finish <grade or verdict line> [extra]: commit, push, and write DONE (LAB_PUBLISH=none: the host's clean job publishes)
  find "$out" -type f -size +5M -print -delete > "$out/dropped-large-files.txt"
  cp "$out/run.log" "$out/run-log.txt" 2>/dev/null
  if [ "${LAB_PUBLISH:-}" = none ]; then push="published by the host"; else
    git checkout -q -b "claude/lab-$id"
    git add "$out" && git commit -q -m "lab $id: $1${2:+ | $2}" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
    git push -q origin "claude/lab-$id" >/dev/null 2>&1 && push=pushed || push="PUSH FAILED"
  fi
  echo "$1${2:+ | $2} | branch claude/lab-$id | $push" > "$out/DONE"
}
machine() { echo "Linux, $(nproc) vCPU, $(awk '/MemTotal/{printf "%d", $2/1048576}' /proc/meminfo) GB, shared with the window's other runs: keep every process under 3 GB of memory, or it is killed"; }

case ${1:-} in
start)
  lens=${2:?lens}; min=${3:-90}
  guard_linux
  [ -f "lab/lenses/$lens.md" ] || { echo "no lens: $lens"; exit 2; }
  guard_key
  id=$(date -u +%Y%m%d-%H%M)-$lens-$(od -An -N2 -tx1 /dev/urandom | tr -d " \n")
  launch _run "$lens" "$min" "$id" ;;
rung)
  f=${2:?rung file}; f=${f#"$PWD"/}; min=${3:-90}
  { git ls-files --error-unmatch -- "$f" && git diff --quiet HEAD -- "$f"; } >/dev/null 2>&1 \
    || { echo "refused: rung file must be committed and unchanged"; exit 2; }
  guard_linux; guard_key
  id=$(date -u +%Y%m%d-%H%M)-rung-$(basename "$f" .md)-$(od -An -N2 -tx1 /dev/urandom | tr -d " \n")
  launch _rung "$f" "$min" "$id" "$(git rev-parse "HEAD:$f")" ;;
wait)
  f=lab/results/${2:?id}/DONE
  for _ in $(seq 54); do [ -f "$f" ] && { cat "$f"; exit 0; }; sleep 10; done
  echo "RUNNING ${2}"; tail -2 "lab/results/$2/run.log" ;;
_run)
  lens=$2; min=$3; id=$4; out=lab/results/$id; base=$(git rev-parse HEAD)
  { preamble; cat "lab/lenses/$lens.md"; cat <<P
## Your run
Run id: $id. Your folder: $out/. Time: $min minutes.
- The machine is a Linux machine ($(machine)). Install what you need with pip or cargo.
- For the web, use your search tools if you have them, or else curl: export.arxiv.org/api/query, api.github.com.
- You may edit any file in this tree to experiment. Your edits are saved as a patch, and the tree is then restored.
- Before your decisive experiment, write $out/predictions.md. At the end, write $out/dossier.md in the format given in lab/README.md.
- Keep scripts and data in $out/, each under 5 MB.
- Never run git commit or git push.
- Your final reply: the claim, in one sentence.
P
  } > "$out/author-prompt.md"
  phase author "$min" patch.diff

  { preamble; cat lab/lenses/checker.md; cat <<P
## Your check
Run id: $id. The author's folder is $out/: dossier.md, predictions.md, its scripts, and work/patch.diff, its edits (apply them with git apply to reproduce).
- Time: $((min / 2)) minutes. The machine is a Linux machine ($(machine)).
- Write $out/check.md. Change nothing else in $out/.
- Never run git commit or git push.
P
  } > "$out/checker-prompt.md"
  phase checker "$((min / 2))" checker-patch.diff

  grade=$(head -1 "$out/check.md" 2>/dev/null || echo "Grade: missing")
  if [ "$grade" = "Grade: gold" ]; then  # gold needs a second, blind checker (arch-v3: precision = found by two)
    sed "s#Write \$out/check.md#Write $out/check2.md; do not read check.md#; s#Write $out/check.md#Write $out/check2.md; do not read check.md#" "$out/checker-prompt.md" > "$out/checker2-prompt.md"
    phase checker2 "$((min / 2))"
    [ "$(head -1 "$out/check2.md" 2>/dev/null)" = "Grade: gold" ] || grade="Grade: silver (second checker disagreed)"
  fi
  finish "$grade" ;;
_rung)  # a directed rung: the frozen file is the question; verdict.py decides, never a grade
  f=$2; min=$3; id=$4; frozen=$5; out=lab/results/$id; base=$(git rev-parse HEAD)
  { preamble; cat "$f"; cat <<P

## Your run (a directed rung)
Run id: $id. Your folder: $out/. Time: $min minutes. The machine is a Linux machine ($(machine)).
The rung above is frozen: never edit it, and report what each configuration does, whatever it is.
- Implement every configuration listed in its configs block, on the cases the rung defines.
- Write $out/metrics.json as {"<config>": {"<metric>": number}}, with exactly the criteria's metric names, for every configuration.
- Write $out/dossier.md (a short summary) and one picture of the behaviour for Julien to look at: $out/picture.svg or $out/picture.png.
- Keep scripts and data in $out/, each under 5 MB. Never run git commit or git push.
- Your final reply: one sentence on what the numbers show.
P
  } > "$out/author-prompt.md"
  phase author "$min" patch.diff
  { preamble; cat lab/lenses/checker.md; printf '\n'; cat "$f"; cat <<P

## Your check (a directed rung)
Run id: $id. The author's folder is $out/: dossier.md, metrics.json, the picture, its scripts, and work/patch.diff, its edits (git apply to reproduce).
The rung above is frozen, and lab/verdict.py computes the verdict from the metrics files: ignore the Grade line rule above.
Time: $((min / 2)) minutes. The machine is a Linux machine ($(machine)).
- Reproduce the author's numbers from the author's scripts, and fix nothing silently: report every number that differs.
- Check the author's implementation independently against the rung's specification, and check each oracle value.
- Write $out/metrics-check.json in the same shape as metrics.json, from your reproduced numbers.
- Write $out/check.md: the abstract, then your reasons. Change nothing else in $out/. Never run git commit or git push.
P
  } > "$out/checker-prompt.md"
  phase checker "$((min / 2))" checker-patch.diff
  python3 lab/verdict.py "$f" "$out/metrics-check.json" "$out/metrics.json" > "$out/verdict.txt"
  verdict=$(head -1 "$out/verdict.txt" | grep '^Verdict: ' || echo "Verdict: VOID; verdict.py failed")
  case $verdict in "Verdict: PASS"*)  # a PASS needs a second, blind checker to pass it too
    { sed "s#$out/check\.md#$out/check2.md#g; s#$out/metrics-check\.json#$out/metrics-check2.json#g" "$out/checker-prompt.md"
      echo "- You are the second checker, blind to the first: never read $out/check.md or $out/metrics-check.json."; } > "$out/checker2-prompt.md"
    phase checker2 "$((min / 2))"
    python3 lab/verdict.py "$f" "$out/metrics-check2.json" "$out/metrics.json" > "$out/verdict2.txt"
    [ "$(head -1 "$out/verdict2.txt" | cut -c1-13)" = "Verdict: PASS" ] || verdict="Verdict: DISPUTED; second checker disagreed" ;;
  esac
  finish "$verdict" "frozen $frozen" ;;
*) sed -n 2,5p "$0"; exit 2 ;;
esac
