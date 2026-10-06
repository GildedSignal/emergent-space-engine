Grade: silver

**Abstract.** Claim: with the WH truth repaired and verified (Saturn's e-history vs two exacts 1.9e-5; |z_S| truly 0.054→0.0040→0.0403), zero-kick secular phasors (R2) are killed at two-planet belt scale — rings 14.5%, LL 0% against the 50% bar, plus 24 leaks. Everything regenerates: rings_z bit-identical, metrics.json identical to 17 digits, the exact chain number-for-number. My attacks harden the kill: pass rate under rate-only 0.346, evec-only 0.156; and I completed the author's broken rings_tc (one transpose fix): truth-driven rings = 0.253, outer bins 0% — the averaging, not the LL driver, binds. Not gold as submitted: the author's decisive held-out prediction (rings 0.40–0.75) failed at 0.1445, and rings_tc was left unfinished. The kill is adoptable now.

## Reproduction (clean scratch tree; patch.diff is empty — nothing to apply)

- `selector.py`, `laws.py ll`, `analyze.py`: metrics.json regenerated — admitted 822, frac_rings 0.14453125, frac_ll 0.0, leaked 24, pumped 299, convergence 1.2884446e-4/2.554e-4, kick evec 1.8697e-3, zone and bin stats all identical to the stored file.
- `laws.py rings` (361 s): **rings_z.npz bit-identical** (`np.array_equal` True).
- `exact_check.py` rerun: drift self-test 1.79e-15; helio-vs-bary 2.09e-9; exact |z_S| min 0.0040 @ t=83049, end 0.0403; |z_J| max 0.0599; hand-WH 2.63e-5 (h=0.1875) / 1.73e-5 (h=0.125) — monotone in h, all matching the author's chain. The [C] format crash reproduces too (cosmetic; same traceback the author hit and fixed in verify.py).
- `ladder.py 1e-14_bary` (91 s) + `verify.py ce` on my regenerated exact: **[C]+[E] identical** — LL-new max|dz_S| 0.0212, |z_S|(T) 0.0297 vs exact 0.0403 (old 0.0102); truth/conv/kick zp 1.93e-5 / 2.92e-5 / 4.67e-5, no 5e-3 crossing. The truth is the declared scene now.
- Pre-registration: predictions.md (mtime 50 min) precedes every belt artifact (kick 39, ll 34, conv 36, truth 30, rings 28, metrics 26 min); planet-level instrument runs before predictions are disclosed inside it. Amendments honored, failures honestly reported (rings 0.40–0.75 → 0.1445 FAILED; leak 5–40 → 24 held; verdict KILL held; kick-law held: 0.342/0.342, 0.281/0.281, evec 1.9e-3).
- Truth-run wall times confirmed from meta (1100/764/549 s ≈ 18/13/9 min); h and step counts as stated.

## Attacks (mine)

1. **Estimator robustness.** Recomputed pass rates with either criterion alone: rate-only 0.346, evec-only 0.156 — both under the 0.50 bar; the kill is not an artifact of one estimator or their conjunction. Failure decomposition: 456/674 failing admitted bodies fail both criteria.
2. **The decomposition the author left open (rings_tc).** The author's repair failed on a return-shape error (`_pz` returned (2, nt) where planet_z's contract is (nt, 2) — one transpose). Fixed and run (6 min): **truth-driven rings Fraction = 0.253** (inner bin 75% vs 43% under the LL driver; mid/outer bins 0.000, evec median 0.458 ≈ unchanged). So even with the true planet history the outer belt fails: the binding failure is the first-order averaging itself, not the linear driver. This closes 008e's "Touma–Tremaine driver could revive the mid/outer belt" escape route. (Caveat: driver interpolated at 384 stored times; the secular trend is smooth on that grid and the failure margin is 5–19× the bar, far beyond any interpolation artifact.)
3. **Independent exact belt probe — and a control that caught my own instrument.** My DOP853 (rtol 1e-13) test-particle probe first "disproved" the truth (|Δz̄| up to 1.2). Control: truth-vs-conv raw z agreed to 2e-8 at early stored times — two runs of the same code family could not both be right against a third that disagrees at t=388; the bug was mine (a `sf*vy` for `cf*vy` transcription in the probe's velocity rotation). Lesson re-confirmed: a probe that disagrees with a consistent pair is the suspect. Planets of my probe vs the shipped truth over the full run: 1.93e-5 — the truth's scene equations are exact to its discretization everywhere I could test.

## Novelty

No HISTORY.md entry covers secular phasors at belt scale (H0214 freezes the belt gates, no compiler yet; p2 was single-planet at 161 orbits). Run 008e was correctly voided as `lead` on the broken truth (work/check.md in this folder); commit 8294f02 queued exactly this fix-and-decide run. The verification protocol (ladder + two coordinate-frame exacts + h-monotonicity, catching the author's own helio RHS bug at 8.4e-3) is itself new to the lab's runs and worth keeping.

## Goal fit

Board focus "fewer kicks per orbit": R2 promised to delete all 64 kicks/orbit and the ~82 B scars for stable bodies while keeping the 0.126-bit belt program. This kill retires that promise at two-planet scale — a component deletion decided by measurement. PRINCIPLES #9: "A failed experiment kills that configuration, never the method" — what dies is zero-kick phasor laws for belts with a self-interacting planet driver; the selector (80.3% admission), the kick-law cadence result (evec 1.9e-3 at 64 kicks/orbit) and the α-power LL convention survive as leads. #3: the belt's surprise budget is dominated by the planets' own secular exchange; a zero-kick law computes no surprises and misses exactly that.

## Why silver, not gold

- The author's own decisive held-out prediction (rings ∈ [0.40, 0.75]) failed at 0.1445 — disclosed, and it understates the kill, but the gold bar says the held-out predictions held.
- The named decomposition (rings_tc) was left broken at step 0; the dossier says the kill does not rest on it (true), but the driver-vs-averaging question stays open **in the submitted record**. I closed it during this check (0.253); the integrator can treat that number as part of this check's evidence, but the dossier as submitted does not contain it.
- Minor, permanent: kick-law agreement shares the truth's integrator family (disclosed).

If the integrator accepts this check's rings_tc result as completing the record, the kill is gold-grade: reproduced bit-for-bit, robust to estimator choice, robust to the driver, and adoptable in one step.

## What the author missed

- rings_tc was one array-transpose from running; 6 minutes would have completed the decisive decomposition instead of leaving the strongest counter-hypothesis (driver, not averaging) unanswered in the record.
- Unit slip: "|z_S| min 0.0040 at t = 83.0 kyr" (dossier; predictions say "t ≈ 84 kyr") — t=83049 code units is 13.2 kyr (1 yr = 6.286 units; the whole run is 23.7 kyr). Cosmetic, but both documents state it.
- The `pumped` flag tests against the static initial forced term and so measures the driver's secular exchange, not belt chaos (the author says this themselves — it should have been recomputed against zf(t) before being reported at all).
- The corrected LL driver still ends |z_S| 26% low (0.0297 vs 0.0403) — worth stating as "first-order LL remains unfit as a driver for anything planet-level", which my rings_tc result then confirms is irrelevant to the outer-belt failure but relevant to the inner belt's 43% vs 75%.
