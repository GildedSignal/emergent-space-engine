# Check — 20261007-0842-inversion-0a7a

Grade: gold

**Abstract.** The claim: the train certificate adopted from gold taleb-09b5 is not O(n·k) — its watch churns ∝ e·n_c/σ_λ, re-importing quadratic work per orbit, and the gold's contact-rank statistic cannot see it. Reproduced bit-for-bit: s0-control (churn 46/86 per body per orbit, ev 601, ratio 69.15×), s1-e005 (199/302.5, 50 encounters), cone-s0/s1 (19900/19900 pairs, 0 missed). I measured the author's missing n_c point: churn/nc ≈ 0.20 flat over nc = 200→1600 (46/79/158/344), and the gold's λ-uniform corner goes 0→4→16 over nc = 200→800→3200. Cost: the b-coorbital-cert trigger gains one dimensionless number (2e·n_c/σ_λ) and per-orbit budgets, before that build lands. The dossier's tier-2 "blindness" side-claim is refuted (see below).

## Reproduction (clean tree, `git apply work/patch.diff`, same build command)

- `invert s0-control`: every field matches the stored JSON (encounters 64, churn p50/p90 46/86, ev 601/807, work ratio 69.15, ranks ≤ 1, leads capped, window_churn 132, 14/64). Only `brute_us` (wall time) differs, as expected.
- `invert s1-e005`: exact (churn 199/302.5, 50 encounters, ev 0, ratio NaN — the disclosed ∞-regime).
- `invert cone-s0`, `cone-s1`: exact (64 and 50 encounters, cone saturated at 19900/19900, 0 missed — the O(n²) control validates the binned brute force).

## Predictions

`predictions.md` mtime 08:51:17; all scenario JSONs 09:03–09:04; dossier 09:09. Pre-registered before the decisive runs. P2 (the kill), P3 (non-vacuity at σ_e = 0.02), P4 (statistic blindness) held. P1 under-predicted churn 2.3× (46 vs ≲20 — in the kill's favour, reported); P5 failed (reported; its charitable branch was pre-registered as "the cost is then the kill").

## My adversarial cases

1. **The n_c slope the author could not run** (nc=800 died with the author's shell timeout; slope was [INFERENCE]). Churn at σ_e=0.001, σ_λ=0.05, 1 orbit, exact author metric: nc 200/400/800/1600 → p50 46/79/158/344. churn/nc = 0.230/0.198/0.198/0.215 — flat: linear in n_c confirmed. Per-orbit watch events = n_c·churn ∝ n_c² while encounters ∝ n_c: the board's "candidate work must track real encounters" is violated by the adoption at scale, as claimed.
2. **The gold's own safe corner.** λ-uniform, σ_e=0.001, ϖ clustered: churn p50 0 (p90 4) at nc=200 — confirming the author's scoping honesty (the gold's measured corner was genuinely safe) — rising to 4 at nc=800 and 16 at nc=3200. The mechanism enters the gold's corner well before 10⁶ (spacing TAU/n_c vs wobble 4e-3), so "any 10⁶ fleet is deep in the violating regime" holds on both λ distributions.
3. **The author's named next experiment, adjudicated.** For all 50 real encountering pairs at σ_e=0.005, the shipped tier 2 emits windows (84 Cross + 16 Wide, zero pairs with no window) and `pair_events` finds 50/50, 0 missed. The dossier's "sections() emits zero windows for e-spread pairs" misread the instrument: `ev` counts numeric-window state evaluations; analytic Cross sections cost 0 evals and are full windows. Tier 2 is **not** blind to e-spread encounters. This removes the dossier's side-anomaly and simplifies adoption (the cone tier saturates and misses nothing here; tier 2 stays sound).

## Novelty

No HISTORY entry or board note measures watch maintenance/overtake churn; the gold's adoption (board taste log, 6 October; taleb-09b5: "rebuild on overtakes", "~4×10⁶ sections (~300 MB), setup falls 10⁵×" at 10⁶) asserted the cost model the run falsifies. components-4643 killed deferred *setup* on the old tier — a different tier and question. The nearest prior instrument lesson (agreement ≠ independence, 5 October) is cited by the author and obeyed (the O(n²) control caught the author's own velocity-angle binning bug, disclosed).

## Goal fit

Top board risk (5 October): candidate work must track real encounters. Measured: the adopted remedy's work ∝ n_c² per orbit at fixed spread, with events outnumbering real encounters by ~10⁵× at 10⁶. It shows a premise of an adoption is wrong before the queued b-coorbital-cert build encodes it, and names the missing dimensionless number — PRINCIPLES #4 ("regimes are chosen by dimensionless numbers") and #19 ("a fix signals the wrong representation"); #13's ruin shape. Adoptable within one step: amend the trigger and state the certificate's budget per orbit, not per setup.

## Reservations (do not change the grade)

- The 69× headline uses churn p90 × k=4 (full-watch rebuild). The charitable reading (p50, incremental, one sections per change) gives 9–17× — still ≥ 3× (P2's own threshold). The formula is printed, so the choice is auditable; the kill survives every reading.
- The 0.9 TB pool constant (1.3e10 pairs) does not reconstruct cleanly from the stated parameters (I get 0.9–3 TB depending on the wobble reading); the conclusion (≫ 8 GB, well under the quadratic's ~36–40 TB) holds under all of them; "55×" is ~43×.
- "Even in the gold's own near-circular control" conflates the gold's λ-uniform fleet (safe; churn 0) with the gold's bunched σ_λ=0.05 rank scenario (where the gold also claimed the certificate and where churn is 46). The dossier's evidence section keeps the two corners straight; the claim sentence is the loosest sentence in it.
- At σ_e ≥ 0.005, per-rebuild sections are analytic Cross windows (0 evals), so churn there is event-count, not evals, cost — the dossier prints those ratios as NaN and says so.

## What the author missed

- `ev` is not a window counter: the "zero windows / wholesale blind" reading was an instrument artifact, and the adjudication (my case 3) refutes it. It was honestly parked as unadjudicated, but printed as measured fact in evidence point 5.
- The n_c slope was one 12-second run away (my ladder ran 200→1600 in ~11 s single-threaded, no brute force needed); the killed nc=800 point did not require the full probe with its 300 s parent timeout.
- The churn law follows in one line from the equation of center (wobble ≈ 2(e_i+e_j), swaps ≈ 2 per orbit per pair within wobble, pairs within wobble = 4e·n_c/σ_λ); the author's own lens section says a dynamics lens would have derived it — correct, and the measured ladder agrees with that line (predicted 0.2·n_c, measured 0.198–0.230).
