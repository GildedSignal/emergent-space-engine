Working...
Check complete — `check.md` written at `lab/results/20261021-0106-q-compile-encounters-9e80/check.md` with `Grade: silver` (abstract 119 words), nothing else touched.

**What I verified:**

1. **Reproduction** — `regen.sh` exit 0; every dossier number reproduced verbatim (503→134 lines, current best 224→15, 137→71 run lines, 319/319 curated, 39/40 held-out). Tree page untouched at base; `patch.diff` empty.

2. **Independent instruments (all pass)** —
   - *Full-population sweep* (218 distinct old-body number tokens vs the author's 359 sampled): 12 not inline, every one a non-loss — e-notation spellings of surviving `×10ⁿ` values, id fragments, punctuation, or facts kept in cited run lines (9fd1's "P6 ≥ 50% FAILED" survives as "P3, P4 and P6 pre-registered and failed"; 0.22–0.27 and null 0.28 are inline).
   - *Grades*: 69/71 match branch subjects exactly; the 2 misses are precisely the disclosed no-branch runs. The typo'd id has no branch, the real one does; the truncated id is completed to b509.
   - *Scope*: 12/12 supersession spot-checks (355.3, r→7×10⁻⁹–2.6×10⁻⁸, 7× OVER, 0.57/0.33/0.03/0.88, 3.17×10⁻¹⁴, 95.5–98.0%, 416 ns, 4.4×10⁻⁵…) carry correct values, runs, and arms.

3. **The gold-blocking find (outside the author's tested range)** — the dossier tests `wiki.py index` but never `apply`, the exact gap nladder's checker named. My verbatim simulation of `apply`'s merge: body clean, but the literal Runs union publishes **162 run lines, 59 ids doubled, 225 lines — under budget, index green**, silently undoing the run's central dedup claim. Ground truth confirms the publisher does this: tree `nladder.md` carries 79 duplicated ids (246 lines), `memory-h-live.md` 4. The `fold_runs` fix is on a branch, not at HEAD.

4. **Novelty** — not a repetition bar: `start q-compile-encounters 90` is an integrator-directed queue job; precedent (nladder silver for this same failure, memory-h-live durable silver) makes silver the consistent grade. One experiment from gold: land the id-keyed Runs union (or hand-take the page) and prove the published page at ≤ 300 lines, 71 one-per-id, no flag.
