Grade: gold

The 2 "lost" emitters are dead handed-out fleet members (bodies 10,054/10,069, killed by the battle at 3,915/6,012 gs; 4 by 200k gs, 30 dead in all, no belt ship) — the crossing search drops zero emitters, and the od-2 clamp is a flown no-op. Reproduced by regen and by three fresh adversarial arms outside the author's domain (burn 221k gs; N=10⁵; rtf 6×10⁴): all read alive-missing 0, drop-none 0, every missing fleet id engine-confirmed dead. Burn re-measures the halving (24.48 → 10.3 segs/body, −58%), confirming the coast's 2.5% as cadence, not noise. Adoption: delete the fix idea, keep the shipped search; the keep decision is now pure memory arithmetic.

## Reasons

**Reproduction (clean tree + patch.diff, `regen.sh`).** Every certificate line reproduces exactly: `alive-missing in 0` gathers in all five arms; `drop none` = 0 in every gather; identical missing-id sets (fleet 25, 47 at bench; 13, 25, 27, 47 at depth); worst seen 10,048/10,046; death times 3,915/6,012/26,857/27,683 gs identical; 30 distinct dead members at depth; 0 `from=None` deaths. Digests and game-s drift (16.1–22.2k / 174–222k), exactly the wall coupling the dossier flags as known (c8d5 finding 6). Clamp vs stock: worst equal, same ids, readouts 19,825 vs 19,821, gather ms 383 vs 385 — the no-op holds.

**Predictions.** `predictions.md` (20:14:22) precedes every decisive arm (clamp 20:15:19, one-leg 20:16:07, deep 20:19–20:20); it honestly declares the smoke arm already read. P1 (attribution at depth), P2 (clamp no-op), P3 (keep-independence of the dead) held. P4 failed (−2.5% vs ≥30%) and P5 failed (no belt deaths) — both reported as failures, and P4's failure is itself the cadence-bound finding. Honest and informative.

**Adversarial (mine, 3 arms, one outside the author's tested range; same binary as `regen.sh`, patch applied).**
1. *Burn at depth*: `keep_probe2 10000 burn 60 6000 300` and with `ES_KEEP_LEGS=1` — the dossier's "what would make it wrong" names burn, but no burn arm was flown. Result: 221k gs, alive-missing 0, drop-none 0, same 4 dead ids; one-leg 24.48 → 10.28 segs/body (−58%), dashboard bytes 6,079 → 3,137 — the halving is real exactly where the page now says it is. Notably one-leg burn fires 34,502 eval-Nones with zero drops: a None probe is not a dropped emitter — the mechanism refutation is stronger than the author's own evidence.
2. *N=10⁵* (next decade; the author flew 10⁴ only): `keep_probe2 100000 coast 15 6000 300` — alive-missing 0, drop-none 0, worst 100,048 of 100,055; 7 missing ids.
3. *rtf 6×10⁴* (10× the author's rtf — deepest probe stress against the keep): `keep_probe2 10000 coast 20 60000 60` — alive-missing 0, drop-none 0, deepest none 39.8k gs back; 11 missing ids.

**Instrument hole found and closed.** `keep_probe2` never alive-checks ids ≥ n_bodies (fleet ids) — a live-but-dropped fleet member would be misclassified as dead-by-design. I closed it by cross-checking the engine's own drop-dead census: every missing fleet member in every arm (mine and the author's) has a death line with matching member identity and a death time before its first missing gather. The attribution stands independent of the hole; the page's od 5 now carries the caveat for the prune-storm rung.

**Novelty.** The published page's od 2 named this exactly ("attribute the 2 ids first — if they are fleet members..., the mechanism is misread" — c8d5 even anticipated the answer's branch). No HISTORY.md entry attributes them; no prior run refutes c8d5's mechanism reading. This is the named open question executed, with the prior run's premise killed: not a repetition.

**Goal fit.** Memory at 10⁹, the ratchet's channel 2: the adoption case for the demand-measured keep was blocked on a view fix that turns out to cure nothing; the blocker is deleted and the decision is now pure memory arithmetic. PRINCIPLES: "the best part is no part" (deleting the fix); "Compute only surprises" (retention is supply the demand never reads); "A failed experiment kills that configuration, never the method" — od 2 is killed by measurement, the page's method stands. Two honest failed predictions, both load-bearing.

**Engine-unchanged (the author's open item).** `cargo test --release -p emergent-universe --test view --test memo` with the patch applied: 5 + 1 passed. The author could not run this because plain `cargo test` also builds the `nladder` example, which does not link on Linux (`proc_pid_rusage` is macOS-only) — a pre-existing platform issue, not the patch.

**Discrepancies (all minor, none load-bearing).** (a) "264 gathers" undercounts: 384 were flown (it excludes the clamp arm); page corrected. (b) The dossier's domain sentence "coast and burn, 10⁴–10⁵ bodies" describes arms this run did not fly (coast, 10⁴ only); my arms now cover burn and 10⁵, so the sentence is true post-check but was overstated at writing. (c) The retained-depth p50 "keep-independent" clause is run-coupled — the regen flips its sign (39.5k vs 33.7k); the reproducible certificate is segs/body (2.47 → 2.41 author, 2.35 → 2.31 regen). Page annotated. (d) The patch deletes a shipped doc line in view.rs (`//! (no lensing yet).`) to place an import — harmless in a lab patch, worth restoring if anything is ever merged.

## What the author missed

The probe's fleet-id alive-check hole (above); the burn arm that their own domain sentence presupposed; the p50's run-coupling; and that `--test view --test memo` sidesteps the Linux `nladder` link failure that blocked their test run. The wreck-visibility design question is surfaced well but its one-line cost is asserted, not priced.

## Page

Faithful and properly scoped to the coast; corrected in place on the three points above (gather count, p50 precision, od-5 instrument caveat) and annotated with my three adversarial extensions. Not a closing run: one gold (this) on the topic; c7a6 and c8d5 are not gold — the topic stays open.
