# Predictions — missmap of the pairwise tier's silent misses (written before any of my own runs)

Question: where in (e-spread, rho, a-spread, phase concentration) does the shipped pairwise tier
(`cone_pairs` + `sections` + `run_section`, main's encounters crate, gold patch applied) silently
drop real sub-rho encounters, is the cliff one dimensionless number, and which construction drops
them (cone / arcs / window / check)?

Cases here are NOT tuned on: I have run nothing yet. The two controls reproduce published numbers
(gold `taleb adj` 4/233 misses; run 20261010-0306's dilute-fleet 0 misses).

- **P1 (controls).** adj scene (nc 200, a_hw 1e-5, sig_e 1e-3, rho 1e-4, sig_lam 0.01, seed 27,
  1 orbit) reproduces a nonzero miss rate of order 1–5% of true encounter pairs; the dilute control
  (a_hw 2.5e-3, sig_e 2e-3, rho 5e-3, sig_lam 0.1) gives 0 misses.
- **P2 (breathing cliff).** Miss fraction among true pairs rises from ~0 to ≥ 10% as
  R1 = a·(e_i+e_j)/rho grows from ≤ 1 to ≥ 10; transition within ~half a decade (guardable by one
  number). If misses are spread smoothly over 2+ decades of R1 with no cliff, P2 fails.
- **P3 (Δa protects).** At a_hw ≥ 1e-3 (sig_e 1e-3, rho 1e-4 fixed), misses ~ 0: faster relative
  motion makes wider, easier dips.
- **P4 (rho protects).** At rho ≥ 2.5e-3 (gold geometry otherwise), misses ~ 0.
- **P5 (mechanism).** At least half of missed pairs are window misses (i's true passage offset
  s_true outside [−w1, w2]) or dropped/arcs-missed sections; Cross-kind sections are rarely the
  dropping one (misses concentrate on Wide/Full). If check-miss (window contains s_true but the
  exact check found nothing) dominates instead, P5 fails.
- **P6 (mixture, far side).** Fleet + same-a eccentric debris (e ~ 0.05, rho 1e-4, R1 ~ 500):
  miss fraction among debris-involving true pairs ≥ 20%. The dangerous regime is the whole far
  side, not a corner.
- **P7 (fix probe).** Raising the d_of_s sampling grid k 32 → 256 does NOT remove the misses
  (mechanism is in windows/arcs, not the s-advancement grid). If k=256 removes them, P7 fails and
  the bug is grid resolution inside d_of_s.

Truth instrument: uniform-in-time sampling (4096 samples/orbit, motion per sample < 2ρ for all
scenes here), coarse min < 4ρ refined by dense re-sampling (2048) + golden section on ±3 samples;
no binning, no cones — independent of the method's axes (the gold's instrument lesson).
