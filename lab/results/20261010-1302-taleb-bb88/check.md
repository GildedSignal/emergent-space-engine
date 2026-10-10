Grade: silver

**Abstract.** Claim: the gold's "every real encounter within partner rank 4" is a circular-orbit scene property; on eccentric fleets, contact count and rank scale as √((1+e)/(1−e)) exactly. Reproduced bit-for-bit (36 runs, 173.6 s); the law is exact Kepler geometry and extrapolates: e = 0.99 gives 40.3–40.5 vs 40.5 predicted, 10× density gives 28.68 vs 28.7. A rank-4 window drops 39% of contacts at e = 0.9, and 72% on a 10× denser circular fleet — the gold's constant breaks even at e = 0. Adoption before wiring: size k by bunching × Poisson tail, gate the trigger on √((1+e)/(1−e)). Not gold: the pre-registered letters P1/H1/H2/NEG failed as written (disclosed numbers, reported as held), and the fix is argued, not measured.

`python3 probe.py /tmp/check_out.json` in a clean tree (patch.diff empty; self-contained folder): 36/36 runs **bit-for-bit identical** to `probe_out.json` on every field (pairs, enc/body, max/p999/mean rank, aphelion fractions), wall 173.6 s vs claimed ≈175 s, well under the memory cap. `summary.txt` and the dossier table match the JSON exactly. File order confirms predictions-first: predictions.md 13:10:28 → probe.py 13:15:03 → probe_out.json 13:17:59 (one run).

## Held-out and adversarial (mine, pre-registered before running)

- **e = 0.99** (beyond the sweep): enc/body 40.28/40.44/40.53 (seeds 11/12/13) vs 2.87·√199 = 40.48; max rank 32–36. The scaling law is exact 6× beyond the gold's regime.
- **Direct drop fraction at e = 0.9, k = 4**: 39.3/39.0/38.9% of unique pairs dropped. The dossier's "roughly a third" is correct (the author derived it; it is now measured). Rank 6 still drops 17%.
- **n = 30000, circular, same R**: enc/body 28.675 (pred 28.7), max rank 30, **72% of contacts beyond rank 4**. Confirms the fat-tail claim (ii) with e = 0: rank 4 is a scene property of n·R_enc, not a law.
- **K-doubling** at e = 0.9 seed 11: K = 480 gives counts and ranks bit-identical to K = 240. The author's sampling-adequacy control holds.
- **τ-order ≡ M-order** at n = 3000 (identical rank multisets): for a single-a fleet the proposed apsis-time keying changes the window's *size*, not the ordering.
- Independent derivation of the count law: |dP/dM| at apoapsis = a√((1−e)/(1+e)), so the contact window in mean anomaly is (R/a)·√((1+e)/(1−e)) and per-body contacts = 2Rn/(2πa)·√((1+e)/(1−e)) = 2.87·√((1+e)/(1−e)). Exact geometry (Kepler's second law), not a fit. The circular mean rank 1.74 also matches the Poisson-gap model (1.69): the instrument is sound.

## Predictions: substance held, letter did not

H3 held (19–21 vs 18–20). H1/H2 held exactly on enc/body (×2.000: 24.95, 5.72) but their letter ("max |rank| doubles") failed (15→25, 7→10). P1's letter ("circular max ≈ 3, reproduces the gold's ≤ 4") failed (measured 7). NEG's letter ("max ≈ 80+") failed (59–63). All four fail in one direction — the mean-reach formula was pre-registered against a max statistic — all numbers are disclosed in the evidence table, and the author's own fat-tails section gives the explanation; but the Predictions section reports them as "Held", and P1's fail is the run's own thesis wearing the gold's number. P3 was falsified and reported as falsified (honest).

## Novelty

No H entry (latest is H0215) or doc measures eccentricity in the phase-neighbour certificate; `docs/law.md`'s encounters text has no rank/fleet clause yet (HANDOFF "Headed next" #5 — the certificate is unwired). Closest priors are different mechanisms: q-candidate-degree's "Wide misses 23% at e 0.7–0.9" (element-based tier, dilute belts) and B16's √((1+β)/(1−β)) (aberration, not arc density). Novel and correctly cited against the gold (board, 6 October).

## Goal fit

Board's top scaling risk (candidate work must track real encounters). This bounds an adopted gold before its one-way door and gives the sizing law; PRINCIPLES #19 ("a fix signals the wrong representation"), #32 (Kepler's second law as the symmetry to borrow), and the lens's own fat-tail rule. The author honestly flags "no 10× cost move".

## What the author missed

1. **The "overpays 19× at perihelion" line is misleading as a cost claim.** In a standing fleet an aphelion-sized window has zero structural waste: it contains exactly the real contacts (2k = 12.5 candidates vs enc/body = 12.48 at e = 0.9). The 19× exists only for an epoch-local implementation that re-checks windows every frame; the deliverable is the sizing law, not the overpay.
2. The gold's own scene was not reproduced (family B circular max rank 12–15, not ≤ 4); the run bounds the constant's domain but cannot confirm what the gold measured. The encounters crate could pin it.
3. `run.log` is empty while the dossier says machine state is "recorded in run log".
4. Family B enc/body grows 30% at e = 0.9 (2.4 → 3.1) though the dossier calls the drift regime "e-robust" — true for rank (the certificate's quantity); a count-level reader would be misled.
5. Family A contact locus "aphelion_frac ≈ 0.57–0.68" sits in the JSON but not the dossier; the pile-up is the mechanism and deserves the number.

## The one experiment to gold

Implement the re-sized window in this harness — k = ⌈bunching √((1+e)/(1−e)) × Poisson-clump tail × drift reach⌉ (equivalently the uniform apsis-time window R/v_apo) — with pre-registered letters that distinguish max from mean, and show zero missed contacts at candidate cost ∝ real contacts across e ∈ {0, 0.6, 0.9, 0.99} × density {3000, 30000} plus family B. That converts the argued fix into a measured one and cleans the prediction record; the integrator can then adopt it as the certificate's sizing rule in one step.
