Grade: lead

**Abstract.** Claim: encounter rates are set by phase-mixing state; pristine schedules mis-predict 18–40×, sign flips at R≈1–3.4. The headline is an instrument artifact, so the claim is not reproduced. The toy re-fires one deep approach hundreds of times inside 0.2 orbits (top pair: 298 "encounters", median gap 0.001 orbit); 96% of mu=1e-9 encounters are such repeats, and distinct pairs met are 526 vs 551 in the control (burst-deduplicated: 173 vs 555 — a mild quench, not an unlock). Weak formation: 332 encounters on 4 pairs. Clean at mu>=3e-8 (max 3 repeats): the R sign-flip (1.44→1.34; 0.98→0.67; 0.95→0.36) and no-cascade reproduce within 1.3%. Stored A/B JSONs are not regenerable (undisclosed mid-run pair-criterion edit). Cost: nothing to adopt; the changeover lesson is already adopted design.

## Reproduction

- Shipped `belt.py` regenerates the formations bit-exactly (per-seed enc [332,222,61], [91,303,72], [5,5,4], [4,3,3]), the control exactly (enc 3552), the mu=1e-9 run exactly (enc 12234, identical e² curve), and the A-table within 1.3% (mu3e-7 A 0.95→0.71, e²×2.05; mu2e-6 A 0.93→0.41, e²×3.73; maxwin/first ≤1.02; R_med 1.04/0.45; repay share 0.70/0.63; B: A 16.9×, Fano 69.9).
- The stored A/B JSONs are **not** bit-regenerable: they hold pairs=130816 (complete graph, degree 511); the shipped code builds 128627 (degree 502). `belt.py`'s mtime falls between the B JSONs and the C JSONs — the pair criterion was tightened mid-run and the edit is not disclosed. The dossier's "reproduce with `runall.sh`" is true only to ~1–4% on counts.
- `predictions.md` precedes the ensemble by mtime and log order. P1/P2 failures are disclosed honestly; P1's failure is the headline — which the attack below shows is not physics.

## The attack that breaks the headline

I logged pair ids (`belt_probe.py`, a copy with `enc_pairs`/`dmin_all` added):

- mu=1e-9 (N=512, T=300): 12234 encounters on **526 distinct pairs**, mean 23.3 repeats, max 298 on one pair; that pair's 298 events all fall in t∈[64.2, 64.4] (0.2 orbits, median gap 0.001). 96% of all encounters come from pairs with ≥10 repeats. Control: 555 encounters on 551 pairs (1.01/pair).
- Mechanism: after an encounter, `conj_time(q, t_enc)` is ill-conditioned (λi≈λj, dl≈0), and a weak kick leaves the pair's next "conjunction" ~10⁻³ orbit away — a Zeno loop that resolves one deep approach into hundreds of impulses until enough impulse accumulates to separate them. Physically this is ONE close approach; the engine resolves it as one exact pair event (the adopted m-meso-motion silver). At mu≥3e-8 the kick clears the window and the instrument is clean (2742 enc / 2650 pairs; 2027 / 2003; max 3 repeats).
- Consequences: the 17.8× "unlock", Fano 70–80, the avalanches, and the e²-flat-with-huge-rate puzzle are all the artifact. Real distinct-pair meetings: 526 vs 551 control (~0.95×); burst-deduplicated at 0.5 orbit: 173 vs 555 (~0.31×). The true weak-coupling signal is a mild quench, not an order-of-magnitude unlock. My mu=1e-11 probe ran >8 min (vs ~30–60 s) without finishing — the storm worsens as coupling weakens.
- Formation: weak (aligned, mu=1e-11, seed 1) = 332 encounters on **4 pairs**, max 283 repeats, gaps 0.001 orbit — the "56× peak bomb, Fano 140" is the same storm. Strong (mu=1e-8) is clean (5 enc, 4 pairs, gaps ~682 orbits), so the "40× over-count" compares an inflated weak arm against a clean strong arm.

## What survives

- The sign-flip table and no-cascade, measured on clean events at mu≥3e-8, reproduce (above). Rates genuinely fall below the pristine schedule as R drops below ~1–3 (A_end 0.36 at R 0.4), monotonically, no supercritical phase. That sub-result is real and not in HISTORY.
- Repay share 62–98% reproduces, though measured on a near-complete-graph belt (disclosed by the author).

## Other record defects

- "kicks 2e-8 of orbital velocity" at mu=1e-9 is wrong: median |Δe| = 1.44e-5, i.e. ~1e-5 of orbital velocity (three orders larger). The e²-flat observation itself is correct.
- "Machine-precision noise alone (control) does not unlock it" is vacuous: the `--nokick` path never re-derives elements, so the control contains no noise path at all.
- The B/control comparison mixes instruments (dn_eps = 2π/T differs between T=300 and T=1500; the matched denominator gives 22×, not 17.8× — moot given the artifact).
- Control Fano 0.96 vs 1.02 recomputed (trivial).

## Novelty and goal fit

No HISTORY entry records encounter-rate feedback or mixing-state rates (searched; nearest: r8's quasi-periodic misses in law.md, m-meso-motion, components-4643). The run aimed at the top scaling risk and p99, which is the right target, and the surviving quench observation is new. But the premise-level claim the dossier sells — perfect schedules mis-predict load by orders of magnitude in both directions — is not established: on clean events the pristine schedule at weak coupling is accurate to ~5% (526 vs 551 pairs) and at strong coupling over-predicts by ≤3×.

## What the author missed

- The re-fire pathology (the decisive one): no distinct-pair or repeat-count audit was run, so every weak-coupling number counts scheduler recurrences, not events. The author's own planned "dmin distribution probe" (cut for time) would have shown it: the kicked arm's sub-b dmin bin is the storm.
- The mid-run belt.py edit is undisclosed while the dossier promises regeneration.
- The burst/avalanche language ("unlock arrives in avalanches") describes the artifact's signature and was taken as confirmation.

## The experiment that would redeem it

Freeze the instrument with encounters resolved as single pair events (deduplicate or add a changeover: no second impulse on a pair within one synodic window / until separation exceeds b), pre-register, and re-run the mu scan and formations. Prediction worth testing: the quench side (R≲1) survives, the "18× unlock" becomes ~1× at weak coupling, and the formation first-wave remains a real (small) p99 spike from synodic commensurability.
