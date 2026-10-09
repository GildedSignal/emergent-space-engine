Working...
`check2.md` written. Grade: **gold**.

**What I did (45-min budget, ~20 min used of runtime):**

1. **Reproduction** — all six shipped commands (`equiv`, `equiv3`, `truth3`, `sweep2`, `scale2`, `truthres`) re-run in clean processes: **bit-identical** to the stored JSONL, timings within the dossier's stated budgets (48/17/77/42/43/7 s). `work/patch.diff` is empty, correctly — all edits live in the run folder.
2. **Verbatim audit** — AST-level diff vs `orig/exp.py`: `rule`, `truth`, `cone_only`, `ideal_trigger`, `unified_old` are the original modulo docstrings/rename. The 5-constant is in the original's shipped code (`orig/exp.py:103` — its docstring says 3, the code says 5), and predates this run's results by mtime (20:47:42 < predictions 20:48:04 < results 20:53+). Predictions genuinely held out.
3. **Adversarial (5 classes, 8 instances, all pass)** — N=4096 fleet (equality 0/0, per-body 1478 continues the linear trend), H=64 window saturation (the author's "unmeasured trim" is unneeded for correctness; old index drops 133 there), single-e const-p (the exact `dn_bound = 0` float-boundary case), belt e∈[0.6,0.9] and const-p {0,0.7} (beyond the claimed domain, still equality + recall 1.0), H=0.5 single-band. I also verified the domination argument analytically (exact min/max of stored doubles, IEEE monotone rounding, wrap tiling, outer-scan full-rule guarantee) — the index equality is by construction, not just sampled.
4. **Novelty / goal fit** — no prior H entry; deletes the trigger, second certificate and fleet category from the encounters design before they are built; PRINCIPLES 13/19/4 quoted in the check.

**Findings against the record (named, none fatal):** the sweep claim "candidates 0.049×–0.80× of cone-only" mixes denominators — the true cone-relative range is 0.70–0.91×, so "far below cone-only" fails at loose s (s=0.3: 0.91× candidates, 3.35× evals); "e ≳ 0.42" should be e > 0.4; and per-body candidates stay linear in N, so the board's top scaling risk is unchanged — the Diophantine tier below remains mandatory.
