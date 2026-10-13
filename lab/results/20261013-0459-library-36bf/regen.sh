#!/usr/bin/env bash
# Regen: every dossier number, from shipped code + work/patch.diff. Run from the repo root.
# 1) quotes verbatim (re-fetches Readwise if no token-free cache), 2) the patched probe,
# 3) the unpatched digest control. ~1 min of builds, flights are seconds.
set -euo pipefail
RUN="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

echo "== quotes =="
python3 "$RUN/verify_quotes.py" || true

echo "== apply patch (idempotent) =="
if git apply --check "$RUN/work/patch.diff" 2>/dev/null; then
  git apply "$RUN/work/patch.diff"
elif git apply --check --reverse "$RUN/work/patch.diff" 2>/dev/null; then
  echo "already applied"
else
  echo "patch does not apply" >&2; exit 1
fi

echo "== patched tree: the three silent ends =="
cargo test -q -p emergent-universe --release --test lab_faulttag -- --nocapture

echo "== unpatched tree: digest control =="
git stash push -q -- crates/universe/src
trap 'git stash pop -q || true' EXIT
cargo run -q -p emergent-universe --release --example lab_digest
git stash pop -q
trap - EXIT
echo "== regen done (compare digests with the dossier's two-build table) =="
