# Predictions (written before the decisive flights)

Question: does the V1 contact law's energy carry (`Body.residual`) sit on a bounded
attractor through the belt's full relaxation (genesis → storm → grinder core), or does it
walk/drift? Units: v1 fixed-point energy, per mass 1, E = 2Q² + |k|², so R is comparable
to k²; the momentum carry's quantum is 2Q.

Disclosure: a 2048-ch smoke flight (seed 1, cold) ran before these predictions to
validate output format only. It showed maxAbsR = 144052 at t = 2048 (2.2× the belt
|k| ≈ 65536), maxAbsC ≈ 0.9·2Q, sumR = −194044 over 458 contacts. The arms below are
≥ 8× longer and include the storm; nothing below is tuned to the smoke.

Theory going in (the Σ-Δ picture): each contact re-minimises the contacted pair's
combined carry |R_a + R_b + e| over the candidate velocity lattice, so the pair sum is
driven inside the candidate spread ρ ≈ few·2|k| (energy) — an error-diffusion loop with
a restoring force. Individual |R| can only change at contacts, by e, |e| ≤ ρ. So:
per-body |R| should sit at O(ρ) = O(|k|), inflating only as |k| inflates (grinder), and
the global sum ΣR should not drift macroscopically.

## Pre-registered outcomes (held-out arms: B 98304 cold s1, C 49152 thermal s2,
## E 16384 notide cold s1, D 8192 pass thermal s1)

- **P1 (quantum envelope, the attractor bound).** For every stride sample of every arm,
  maxAbsR(t) < 16·maxk(t) + 32, with maxk(t) the running max |k| component up to t
  (same series' column). KILL if any sample exceeds it.
- **P2 (no walk against contact exposure).** At each arm's final epoch, over live bodies
  with ct > 0, the OLS slope of log(1+|R|) on log(1+ct) is < 0.25 (a random-walk ledger
  gives ≈ 0.5; an |k|-scale attractor gives ≈ 0). KILL if ≥ 0.25 in any Bounce arm.
- **P2b (no macroscopic global debt).** |sumR(t)| < 1e-4 · ke_all(t) at every stride
  sample of every arm. KILL if broken (c644's "ke flat" readings would be debt-financed).
- **P4 (lower-id flow).** Spearman(id, R) < 0 among live contacted bodies at the final
  epoch of B and C (the rule parks the pair's error on the lower index). Observation,
  held if ρ < −0.15.
- **P5 (instrument negatives).** D (Pass): R ≡ 0 and C ≡ 0 at every sample. E (no tide):
  ΣE + ΣR is constant to the unit at every chronon (integer identity, no walls, no
  kicks), while maxAbsR still O(|k|).
- **P6 (panic headroom).** The largest |owe| component ever observed leaves ≥ 12 bits of
  i64 headroom (maxAbsR < 2^51); report the margin and any trend.

Cross-check (not a prediction, a requirement): arm C (49152, s2, thermal 4096) must
reproduce c644's digest `0845a045c1b68a0908b72ec031336f1454dff357f944397ec5151c3053c066df`
and contact count 88881906 bit-for-bit, proving the two new accessors are inert on a
real 89M-contact flight.

What would make the claim wrong: P1 or P2 broken → the anti-compounding ledger itself
accumulates at storm scale (PRINCIPLE 13 channel; a residual-bound gate is then missing).
P2b broken → macroscopic hidden energy debt. P5's identity failing → the instrumentation
(or the law's own ledger claim) is wrong → VOID, not a physics result.
