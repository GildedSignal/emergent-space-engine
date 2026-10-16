Working...
**Grade: silver** — `check.md` written; the author's page corrected in place where it overstated; tree restored clean.

**Reproduction.** Applied `work/fix.diff` myself on the clean tree at `b07f5a0b`, rebuilt, re-flew. The runner's regen.log matches every deterministic number in the dossier (all ten rows, envelope `212 240 207 251 229 195 334` → `52 27 26 12 13 13 12`, all digests); I recomputed the CPU sums from the dump CSVs (1,613→1,458 ms this box, −9.6% vs the recorded −11%) and confirmed patched-OFF = pristine main bit for bit (`6895ce06…`, 13/13 cases × 4 schedules). One record defect: `work/patch.diff` is **doubled** (d31c's defect again — `git apply` fails on a clean tree; `fix.diff` is the usable copy).

**My three adversarial cases.**
1. **Burn** (the author's named unflown gap): OFF max 328 (= 4c22's checker) → arm **112**, p99 152→49, +15.8% events — a *partial* collapse, not the floor class, burn engine tail unmoved.
2. **N=10⁵**, a decade above the flown range: 240/146 → 52/27 — N-flat confirmed.
3. **Full 13-case digest under the arm** (author flew 2 per arm): one digest × 4 schedules everywhere, including burns, key-mashing, belt crossings — determinism holds under the chained law.

**Why silver, not gold.** The pre-registered kill criterion fired on its letter (total events +40% @1,900 s, +20% @5,400 s > +15%); the author's diagnosis is arithmetically sound (excess 97.7% one-time fleet-slice wakeups, incremental rates 3.17 vs 3.16 ev/game-s, kicks +0.6%) — but a fired frozen letter is not a held prediction, and the B13/B14 legality gates (the lost pair-shared boundaries) remain unflown. Also corrected: "beats ES_LOCAL_PHASE's permanent +19–41% stream" overstates — the page's own direction-3 note records the phase price as the *same* front-loaded ≈+4.4k slice bill (8,337 vs 8,300 slices); the real differential is parsimony (no phase grid, no stubs) plus the −11% CPU. Gold experiment: fly the legality rung under the chained+stagger law.
