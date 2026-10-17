Grade: gold

**Abstract.** Claim: `Rebinding::from_state`'s `decoded_event` residual is dead work on the flown path; deleting it is bit-identical. Reproduced in a clean tree: pristine main = inert patch, digests identical under the delete on all five N=3000 cases; checker arms extend identity to all eight N=100/N=1000 cases (4 schedules each), and a checker probe finds 0 `decoded_event` errors on the three heaviest cases — the one corner where the arm could differ never fires. Fit replay mean −13.9/−14.5%, flight ns/call −17.1/−18.6%; engine ~7% (the dossier's −18.3% p50 is one noisy pass). Direction 2 refuted (at_radius 1.1 µs, 4%); compile re-priced 49%. Gain: ~15-18% off the kick's largest term for ~10 lines; certificate = bit-identity itself. Adopt within one step.

## Reasons

**Reproduction (clean tree, patch applied by me).**
- Premise: pristine main (patch reverted, my own run) prints all five N=3000 digests bit for bit (ddd5b1cc…, 69d7abbb…, 253d8aed…, d2632de9…, 4995f384…, kicks/encounters/contacts equal) — the inert patch is digest-neutral, as claimed.
- Runner's regen (exit 0) and my arms agree: delete arm (`FIT_NODECODED=1`) identical on every case; `DIGESTS+KICKS IDENTICAL`.
- Timing, regen vs author (same orders, shared machine): replay mean 25.55→21.84 µs (−14.5%) and p50 16.86→13.25 (−21.4%) vs author 26.16→22.52 / 17.19→13.63; flight `bind_surface` 614.6→509.4 µs/frame, 21,785→18,054 ns/call (−17.1%) vs 617.1→502.6 / 21,892→17,813 (−18.6%); engine `process` −6.6% vs −8.2%; p50 3.146→2.933 (−6.8%) vs 3.530→2.883 (−18.3%). Counter arithmetic internally consistent (quads/bind 18.61→15.63, 2.98 Newton iters/solve, outbound_at halved minus 6 early returns, stage-sum vs total mean within 0.75 µs).
- **The −18.3% engine-p50 headline does not reproduce at magnitude** (−6.8% here; the delete arms agree at 2.88/2.93 ms, the shipped baselines differ 3.53/3.15 — between-arm wall noise). The reproducible engine-level drop is ~7%, inside the author's own P2 (3-8%). Page corrected in place.

**Structural claim verified by reading, not just digests.** `bind_in` (bind.rs:260-288) reads only `fit.trajectory/periapsis_angle/periapsis_time/clockwise` and builds `Bound.residual` from its own `decode`; the universe has zero `Rebinding::reconstruct` calls; the residual's real consumer is `TubeEvent::bind → fit.reconstruct()` (space's handoff path). The engine crate's `from_state` call reads `trajectory` only.

**Adversarial cases (mine).**
1. *Out of the tested domain* (author tested only N=3000; the corpus spans N=100-3000): all eight N=100 and N=1000 cases, wave and belt-crossing regimes included, 4 schedules each — digests, kicks, encounters, contacts identical between arms.
2. *Error-path probe* (the run's own "what would make it wrong"): instrumented `decoded_event()` in `from_state` to report errors — **0 errors** across key mashing / belt crossing / coast through the wave at N=3000, all schedules. The arm's only behavior-changing corner never fires in the corpus.
3. `ending_at` routing: the arm's reach is broader than the dossier states — `ending_at` early-returns `from_state`'s fit (binding.rs:378-379), so surface binds (PLUNGE.md: creation, kicks, handoffs) also lose the residual; still dead (`bind_in` discards it), but the adoption API split must route that path. Noted on the page.

**Predictions.** `predictions.md` predates the held-out runs (file order and content agree). P1 held and extended by my arms; P2 held (3-8% predicted, 6.6-8.2% process); P3 folded into P1, held; P4's spikes reproduced per-input and were honestly not claimed as engine costs. One wobble: the dossier quotes a bench pass (26.16→22.52 mean, 2.755 µs/solve) that matches neither the stored `fitbench_stages.txt` (25.96→21.95, 2.728) nor my regen (25.55→21.84, 2.699) — multiple passes, same orders; quote the stored record.

**Novelty.** This is the read-stream page's own named direction-2 probe ("time `at_radius` and `decoded_event` directly… inferred by subtraction"), previously unexecuted; the delete itself has no prior run (docs/HISTORY.md: no `decoded_event`/`from_state` entry). Not a repetition of 5eb2, which priced the fit total and inferred the rest by subtraction; this run measures stages in situ and corrects the compile share 26%→49% (5eb2's 4.4 µs was a standalone proxy on belt-class keys; the 2.8× gap to 12.33 µs in situ is explained only by the key-mix hypothesis — the page says so).

**Goal fit.** Board #3, the kick at 75-160 µs against a ~50 ns floor: the fit is the kick's largest measured term, and this deletes one of its three trajectory evaluations with a bit-identity certificate. PRINCIPLES §1: "The cheapest compute is compute not done. Delete before optimizing"; §17: "the best part is no part"; §3: compute only surprises — this was compute nobody consumes. Gold bar: reproduced, predictions held, deletes real work (a full Newton solve + cartesian readout per bind), refutes a page premise (direction 2's at_radius hypothesis), adoptable within one step (~10-line API split, no law change). Not three agreeing golds on the page yet — read-stream stays open.

## What the author missed

- The engine-p50 headline (−18.3%) is single-pass wall noise; the reproducible number is ~7% — the honest engine-level claim, and inside their own prediction.
- `ending_at`'s early return inherits the arm for surface binds; the adoption split must route it (page now says so).
- The replay corpus is one flight at one N (belt crossing, first 24,576 calls): the stage shares, in particular compile 49%, are that mix; a key-mix dump would close the 12.33 vs 4.4 µs compile question instead of the key-mix hypothesis.
- The dossier's quoted bench pass differs from the stored evidence file; quote the stored record.
