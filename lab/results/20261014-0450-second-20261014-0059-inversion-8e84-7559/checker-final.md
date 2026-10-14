Working...
Check complete. **Grade: gold** — written to `check.md`.

**What I verified:**

- **Reproduction:** the runner's `regen.sh` (exit 0) matches the dossier's table exactly — 91/0/3 under both M-kick and M-prune (23 binaries, 3 ignored = the γ-clock, the frozen T1, the known-chaos test), M-wrap killed at `law.rs:711`, restore = baseline, distinct rlib fingerprints per arm (liveness). Every quoted number in the dossier traces to a raw log: the B10 `["G5","B10"]` vs `["G5"]` panic, the bit-identical `across_a_kick` values (1.0/3.0/1.0/24.4 quanta, ×4 arms), the behave clean-fail strings.
- **Predictions:** `predictions.md` predates every run log by ~14 min (mtimes); P1–P3 held, P4 vacuous with substance confirmed.
- **My three attacks, two outside the author's range:** M-kick3 (`>>(2L+3)`) and M-prune at margin `1<<2` both still pass 91/0/3 with live builds — the darkness is a coverage hole, not a knife-edge at +1 — and the running readout test prints **bit-identical** per-ship values under M-kick: the suites never even observe the slip. Source confirms the mechanism (`partial` uses `k.len` only as a window bound; the `credit` ramp's test is `#[ignore]`d; the digest never hashes `b.kick`). Tree restored clean after my arms.
- **Novelty/page:** the published wiki's open direction 4 named this exact experiment; the run closes it, and the proposed page is faithful — no correction needed. Topic stays open (not three golds).

**Warts recorded:** "all numbers regenerate with regen.sh" overstates (xtask/behave arms regenerate from their own scripts); `work/patch.diff` is the M-prune mutant snapshot, not an author edit — a future checker must not apply it; and the author undersold the behave arm: the four outputs are gate-line identical, so even where it runs on this box it wouldn't bite these mutants.
