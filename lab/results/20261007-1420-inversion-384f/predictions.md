# Predictions — inversion run 20261007-1420-384f

Written AFTER calibrating the control S1 only (a single co-orbital formation, the gold
20261006-0346's regime). S2, S2scale and S3 have not been run at this point. Tuned parameters:
R_ENC=1e-3, R_PATH=2e-3, k=4 (k=8 sensitivity), grouping tolerance (Δa/a<1e-3, Δe<5e-3, Δω<2e-2).

Control S1 (measured, tuning run): phase-rank k=4 recall 0.964, k=8 recall 1.000;
window tier 28,680 candidates for 393 encounters (73× per encounter; the gold measured 135×).
Phase concentration 48.7× uniform; one group holds 100% of bodies.

## P1 — S2 crossing lanes (ring formation + elliptical formation, clumps meeting at a node)
- Truth contains BOTH internal (per formation) and cross-family encounters; cross ≥ 20.
- Phase-rank misses **100% of cross-family encounters** at k=4 AND k=8 (partners are in
  different orbit groups ⇒ the pair is never checked). Internal recall stays ≥ 0.9.
- Window tier: every A×B pair has orbit paths crossing (path distance ~0) ⇒ candidates
  ≥ 40,000 cross + internals ⇒ cand/encounter > 300.

## P2 — S2 fixed-density scaling (n = 100/200/400 per family, arcs ∝ n)
- Real encounters grow ~ linearly (∝ n) at fixed linear density.
- Window-tier candidates grow ~ n² (all A×B pairs are geometric candidates regardless of
  density) ⇒ cand/encounter grows ~4× from n=100 to n=400.
- Consequence if it holds: the quadratic tier is forced by **orbit-path intersection**,
  not by concentration; two crossing lanes of any density hit it.

## P3 — S3 pericentre funnel (every orbit distinct, all sharing one pericentre point)
- All groups are singletons ⇒ phase-rank issues 0 checks ⇒ recall 0.000, at any k.
- ≥ 30 real encounters (passages clustered within Δt ~ R_ENC/v).
- Window tier: every pair's paths meet at the shared pericentre ⇒ candidates = C(N,2)
  ⇒ cand/encounter > 200.

## P4 — the repair (time-rank at locus): rank bodies by ARRIVAL TIME at each crossing locus
- S2: catches ≥ 95% of cross-family encounters at k=4, with checks O((n_A+n_B)·k·passes·loci)
  (thousands, not 40,000+).
- S3: one locus (the pericentre point); catches ≥ 95% of encounters at k=4, checks O(N·k·passes).
- Union (phase-rank ∪ time-rank) recall ≥ 0.95 in both scenes.

## P5 — the trigger cannot be one dimensionless number of concentration
- S3 is phase-concentrated (phase_conc > 10) AND spatially concentrated at pericentre,
  yet max_group_frac < 0.01: phase/space concentration does not imply shared orbits.
- S2 is two formations (element-concentrated within each) whose real encounters are
  cross-family: element-space concentration does not imply encounters are internal.
- If the single number is phase/space concentration → S3 fires the override and drops ~100%
  of encounters. If it is element-sharing → S2 does not fire and the quadratic window tier
  runs. The two concentration topologies (standing-along-orbit vs flux-through-locus) are
  independent; routing needs the locus structure, not a scalar.

## Kill criteria for my own claim (pre-registered)
- If S2 cross recall under phase-rank k=4 is ≥ 0.5, or S3 phase-rank recall ≥ 0.5: my attack
  fails; the certificate generalizes better than the board text implies.
- If time-rank@locus recall < 0.8 on S2/S3, the repair is not demonstrated (kill the repair,
  keep the miss).
