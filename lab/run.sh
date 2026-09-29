#!/usr/bin/env bash
# The GLM lab runner (see lab/README.md). Cloud only: never on Julien's machine.
#   lab/run.sh start <lens> [author-minutes]   starts a run in the background and prints its id
#   lab/run.sh wait <id>                       waits up to 9 minutes; prints the grade line when done
set -uo pipefail
cd "$(git rev-parse --show-toplevel)"
export PATH="$HOME/.local/bin:$PATH"
GLM=(omp -p --model=zai/glm-5.3 --thinking=high --approval-mode=yolo --no-session)

preamble() {  # PRINCIPLES' goal and philosophy, verbatim, then the lab's charter and board
  sed -n '/^## The goal/,/^## Proposed/p' docs/PRINCIPLES.md | sed '$d'
  printf '\n'; cat lab/README.md; printf '\n'; cat lab/board.md; printf '\n'
}
restore() { git reset -q; git checkout -q -- .; git clean -fdq -e lab/results; }

case ${1:-} in
start)
  lens=${2:?lens}; min=${3:-90}
  [ "$(uname)" = Linux ] || { echo "cloud only: never on Julien's machine"; exit 2; }
  [ -f "lab/lenses/$lens.md" ] || { echo "no lens: $lens"; exit 2; }
  [ -n "${ZAI_API_KEY:-}" ] || { echo "ZAI_API_KEY is not set in this cloud environment"; exit 2; }
  command -v omp >/dev/null || bash lab/setup.sh || exit 2
  id=$(date -u +%Y%m%d-%H%M)-$lens
  mkdir -p "lab/results/$id/work"
  nohup bash lab/run.sh _run "$lens" "$min" "$id" > "lab/results/$id/run.log" 2>&1 &
  echo "$id" ;;
wait)
  f=lab/results/${2:?id}/DONE
  for _ in $(seq 54); do [ -f "$f" ] && { cat "$f"; exit 0; }; sleep 10; done
  echo "RUNNING ${2}"; tail -2 "lab/results/$2/run.log" ;;
_run)
  lens=$2; min=$3; id=$4; out=lab/results/$id; base=$(git rev-parse HEAD)
  { preamble; cat "lab/lenses/$lens.md"; cat <<P
## Your run
Run id: $id. Your folder: $out/. Time: $min minutes.
- The machine is a cloud container (Linux, 4 vCPU, 16 GB). Install what you need with pip or cargo.
- For the web, use your search tools if you have them, or else curl: export.arxiv.org/api/query, api.github.com.
- You may edit any file in this tree to experiment. Your edits are saved as a patch, and the tree is then restored.
- Before your decisive experiment, write $out/predictions.md. At the end, write $out/dossier.md in the format given in lab/README.md.
- Keep scripts and data in $out/, each under 5 MB.
- Never run git commit or git push.
- Your final reply: the claim, in one sentence.
P
  } > "$out/author-prompt.md"
  "${GLM[@]}" --max-time="${min}m" @"$out/author-prompt.md" > "$out/author-final.md" 2>&1
  git add -N . && git diff "$base" -- . ':(exclude)lab/results' > "$out/work/patch.diff"; restore

  { preamble; cat lab/lenses/checker.md; cat <<P
## Your check
Run id: $id. The author's folder is $out/: dossier.md, predictions.md, its scripts, and work/patch.diff, its edits (apply them with git apply to reproduce).
- Time: $((min / 2)) minutes. The machine is a cloud container (Linux, 4 vCPU, 16 GB).
- Write $out/check.md. Change nothing else in $out/.
- Never run git commit or git push.
P
  } > "$out/checker-prompt.md"
  "${GLM[@]}" --max-time="$((min / 2))m" @"$out/checker-prompt.md" > "$out/checker-final.md" 2>&1
  git add -N . && git diff "$base" -- . ':(exclude)lab/results' > "$out/work/checker-patch.diff"; restore

  grade=$(head -1 "$out/check.md" 2>/dev/null || echo "Grade: missing")
  if [ "$grade" = "Grade: gold" ]; then  # gold needs a second, blind checker (arch-v3: precision = found by two)
    sed "s#Write \$out/check.md#Write $out/check2.md; do not read check.md#; s#Write $out/check.md#Write $out/check2.md; do not read check.md#" "$out/checker-prompt.md" > "$out/checker2-prompt.md"
    "${GLM[@]}" --max-time="$((min / 2))m" @"$out/checker2-prompt.md" > "$out/checker2-final.md" 2>&1; restore
    [ "$(head -1 "$out/check2.md" 2>/dev/null)" = "Grade: gold" ] || grade="Grade: silver (second checker disagreed)"
  fi
  find "$out" -type f -size +5M -print -delete > "$out/dropped-large-files.txt"
  git checkout -q -b "claude/lab-$id"
  git add "$out" && git commit -q -m "lab $id: $grade" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
  git push -q origin "claude/lab-$id" && push=pushed || push="PUSH FAILED"
  echo "$grade | branch claude/lab-$id | $push" > "$out/DONE" ;;
*) sed -n 2,4p "$0"; exit 2 ;;
esac
