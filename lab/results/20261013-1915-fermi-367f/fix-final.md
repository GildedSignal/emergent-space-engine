Working...
Fixed and proven. Root cause: line 5's `cd ../..` from `lab/results/<id>/` stops in `lab/`, so `$RUN` resolved to `lab/lab/results/.../work/patch.diff` → `git apply` exit 128. regen.sh now roots itself with `git rev-parse --show-toplevel`.

Verification: full regen ran end-to-end (exit 0, 154 s, `regen done`) and regenerates every dossier number — deterministic counters bit-identical (leak 1.12e-3→6.76e-2 per member/game-s, 8257 B marginal, 3003×/145× exchange rates, 14.9 MB/game-s sticky growth, 8 GB in 9 game-min, 449/480 overflow collapse at 1500/rtf100), timings within the dossier's own shared-box qualification (kicks 210–289 µs, handouts 488–913 µs, fleet advance 42→18 176 µs ≈ N^1.9). The checker's rerun on an already-patched tree also works (restore-then-apply fallback), and the tree is left clean.

Claim: regen.sh's repo-root resolution was one directory short, and fixing it makes the full ladder — all thirteen benches, `analyze.py`, and `ladder-table.txt` — regenerate from shipped code in under 3 minutes.
