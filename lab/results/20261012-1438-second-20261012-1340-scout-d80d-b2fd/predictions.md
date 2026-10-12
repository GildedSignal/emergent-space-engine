# Predictions — second-author run (written before the decisive T = 3e4 run)

Question: does the twin-rate framing predict the engine's own event-based
scar production (shipmem semantics: departure from the packed base sealed as
a delta, reabsorbed on return), and is the "99.9% regenerable" claim a
horizon artifact as the checker says?

Instrument: `second.py` — same belt/ICs as the shipped run (verified
`bodies_match_A005: true` in the smoke test), T = 3e4 periods, A = 0.05,
free twin sampled at 64 quadratically spaced checkpoints (horizon ladder),
plus two scar twins with correction quanta b* = 8 and 16 bits, scanned once
per period, counts split at the half. First half fits, second half is the
held-out target. Smoke test (T = 3e3) tuned nothing; it only fixed two
broadcast/slice bugs before any look at per-body structure.

## S1 — Horizon ladder (the checker's missed point 1)
The chaotic fraction under the shipped gates falls with horizon: ≥ 0.3% at
T = 1e3, ≈ 0.1% at 1e4, and ≤ 0.15% at 3e4; at least 10 bodies chaotic at
1e3 reclassify regular at 3e4 (transient divergence). If the fraction is
flat in T, the horizon objection weakens.

## S2 — Rate spectrum and floor
(a) The regular class's median second-half slope shrinks ≈ like 1/T between
the 1e4 and 3e4 horizons (log-growth signature: slope ≈ 1 bit per doubling
over the second half, ~6.7e-5 bits/period at T = 3e4).
(b) No more than 0.2% of bodies have a second-half free-twin slope exceeding
3× their own first-half log-fit extrapolation. The binomial 95% upper bound
on that excess fraction is reported; sub-floor bodies could still carry
λ ≤ floor, so the honest deliverable is the spectrum + floor, not a class.

## S3 — Boundary body (missed point 4)
The A005 "regular" body ending at 41.85 bits (found by index in the stored
npz) saturates by T = 3e4 → the chaotic count is 5, not 4.

## S4 — Scar cross-validation (the named experiment's core)
Fitting each body on the first half only (λ̂ from the free-twin slope for the
exponential class, k̂ from the log-model for the shear class), the predicted
second-half scar counts satisfy: Spearman ρ(predicted, actual) ≥ 0.6 over
all bodies at b* = 8; each class×quantum total within a factor of 2.

## S5 — Scaling signature (what separates the classes)
Median per-body count ratio count(b*=8)/count(b*=16): ≥ 30 for the shear
class (log-model: interval ~ 2^{b*}/k → ratio ~256, reduced by k
inhomogeneity and beats), and ≤ 4 for the exponential class (interval
~ b*/λ ln 2 → ratio 2).

## S6 — Budget arithmetic
Forced scar bytes (exponential class only) are < 1% of total scar bytes at
both quanta over 3e4 periods: the event measure without the rate class
budgets ~100× more memory than the engine is forced to hold; the difference
is the shear class, avoidable by recompute (the engine's `compact`
reabsorption/repack).

## Kill criteria
S4 failing (ρ < 0.3, or any class×quantum total off > 10×) refutes the
adoption claim: the twin framing would then NOT predict the engine's own
scar production. S1 failing flat (fraction stable in T at ~0.1% with few
reclassifiers) weakens the checker's horizon objection instead.

## Disclosed limitations
Drive-coupled local form (libration period = drive period) as in the shipped
run; T = 3e4 is 3× the shipped horizon — the λ ~ 1e-5 band ( Wisdom-scale
secular chaos) stays invisible; I bound its population share, I do not
measure it. One belt seed (index-alignment with the shipped record is the
point), checker already ran seed 777 adversarially.
