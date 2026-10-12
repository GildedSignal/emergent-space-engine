Working...
Check complete. **Grade: silver** — written to `check2.md` (blind to the first check; the run folder is otherwise untouched, no commits made, spinners cleaned up).

**What I did (26 fresh cells, all ≤ 45 s each, well under 2 GB):**

| Attack | Result |
|---|---|
| Baseline 3 seeds, paced + unpaced | `6ce636fa` / `c9794984` / `1e05437c` at cut 406050894 — exact match to dossier |
| Load 3.6→7.6 (6 spinners), contended core, threads 8 + ev64 (32.8 ms worst hitch) | all `6ce636fa` |
| `--dt-ms` 16.7–100, `--engine-events` 1–64, cut drift ±1–5 s, 8 paced repeats | all `6ce636fa`; `56f4…` appears nowhere (nor at neighbouring cuts) |
| `ES_DIGEST_PARTS=1` paced vs unpaced vs ev4 | all 76 per-body lines bit-identical; only the un-hashed `resolved` counter moves |
| Fresh unpatched rebuild of a838a284 | `6ce636fa` — probe patch confirmed digest-neutral, rebuild doesn't recreate the flip |

**Why silver, not gold:** everything reproduces, but the run's own held-out predictions (P2, P3) failed — the pre-registered flip never appears — and the first checker's `56f4…` (3/9 runs on their harness) stays unexplained. Two checkers now disagree across harnesses: DISPUTED, resolvable by one named experiment — rerun the first checker's exact session with `ES_DIGEST_PARTS=1`; one line moves and the bisect finishes in a step.

**Found the author missed:** the claimed "wall 5/10/15 ms" budget sweep is absent from the data — all 57 JSONs record `engine_budget_ms = 5.0`, and the probe patch removed the `--engine-ms` flag outright. Harmless (b5 is the disputed cell; ev1→64 spans more deferral), but the claim overstates recorded coverage.
