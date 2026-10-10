# Predictions — run 20261010-1302-taleb-bb88

Written before the decisive sweep. Question: does the phase-neighbour certificate's
partner-rank bound (gold 20261006-0346: "every real encounter lies within partner rank 4
along the orbit", measured on a circular-ish formation) extend to eccentric fleets
(transfer legs, e up to 0.95)?

Mechanism (derived, not fitted): bodies uniform in mean anomaly have along-track
separation (v(M)/n)·ΔM; the local speed v(M) varies by (1+e)/(1−e) around the orbit.
So the number of partners within a fixed encounter radius R_enc, counted in M-rank,
scales as n/v(M): maximum at aphelion, minimum at perihelion.

- rank_apo(e)/rank_apo(0) ≈ sqrt((1+e)/(1−e))   [4.36× at e=0.9, 6.24× at e=0.95]
- rank_peri(e)/rank_apo(e) = (1−e)/(1+e)        [1/19 at e=0.9]

Two families, n = 3000, a = 1 AU, coplanar, M uniform:

- **Family A (standing-gap regime)**, spreads δa/a = δe = δϖ = 1e-6 (synodic drift
  negligible), R_enc = 3e-3 AU, T = 2 periods:
  - P1: circular max |rank| ≈ 2·R_enc·n/(2πa) ≈ 3 (reproduces the gold's "≤ 4").
  - P2: max |rank| grows ≈ sqrt((1+e)/(1−e))×; at e = 0.77 it crosses 4 (the gold's
    fixed k misses real contacts), at e = 0.9 reaches ≈ 12–13.
  - P3: encounters per body roughly e-independent (bunching moves partner identity,
    not count); conjunctions concentrate at aphelion.

- **Family B (synodic-drift regime**, the gold's own regime), spreads δa/a, δe, δϖ ~ 1e-4,
  R_enc = 1.5e-4 AU, T = 10 periods:
  - P4: circular max |rank| ≈ (3/2)·(δa/a)·(T/P)·n ≈ 4–9, reproducing the gold's order.
  - P5: max |rank| ≈ independent of e (M-dynamics of drift is e-independent; this
    separates the two mechanisms).

Held-out (not tuned on, run in the same sweep but predicted here first):
- H1: family A at e = 0.9 with R_enc doubled → max |rank| doubles (linear in R_enc).
- H2: family A at e = 0, n = 6000, same R_enc → max |rank| doubles (linear in n).
- H3: family A at e = 0.95 → max |rank| ≈ 18–20.

Kill criteria (for my claim, pre-registered):
- If family A's max |rank| is flat in e (no sqrt((1+e)/(1−e)) growth), the mechanism is
  wrong and the certificate is e-robust; I report that as held and the gold stands unbroken.
- If family B circular gives max |rank| ≫ 9 or ≪ 2, my harness disagrees with the gold's
  regime and the instrument is suspect before any e-claim.
- Negative control: family A, e = 0.9, R_enc = 0.02 AU → predicted max |rank| ≈ 80+;
  if the instrument reports small ranks there, it cannot detect the failure mode at all.
