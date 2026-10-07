# Predictions — second author on 20261007-0621-scout-6e10

The checker's named experiment: measure the mix on the engine's own path — (a) the
smooth fraction and σ scales of real kicks per workload, (b) whether real flyby kick
shapes sit in a low-order birth-feature basis (its A1). The `b-h-live` build is queued
and the belt is not yet wired into the plane (`b-belt-wire` also queued), so the
cheapest decisive part: integrate B18b's belt scene (the original run's exact scene:
a∈[2.0,3.6] uniform, e Rayleigh 0.1, angles uniform; Jupiter a=5.2, e=0.05, μ=1e-3)
under the plane's own force model — `crates/universe/src/force.rs`: the secondary's
differential pull plus the origin's fall, no truncation — with a fixed-step
velocity-Verlet at 700 steps/orbit (the plane's own cadence regime, board bottleneck 2),
each body for 10 of its own orbits (one ledger epoch). Real kick = Δz (eccentricity
vector change) over the window. All numbers below are for per-component σ and
differential entropy at the ledger's q24 (0.6·2⁻²⁴), sum of the two components, as in
the original.

Fermi first (impulse approximation, Δv = 2Gm_J/(bU) with b ≈ a_J−a, U the synodic
speed): per-conjunction Δe ≈ 2·μ·a·a_J/((a_J−a)²·U)·(a matching factor) gives
~7×10⁻³ at a=2.6 and ~2.7×10⁻² at a=3.6; 4–8 conjunctions per window, random-walked.

## Pre-registered predictions (written before the integration runs)

- **P1 (σ scale).** The real kick after removing the true-Laplace–Lagrange secular
  program has per-component σ ∈ [2×10⁻³, 5×10⁻²], rising by ≥3× from the inner to the
  outer belt (closer to Jupiter), and total entropy (both components) at q24 between
  33 and 48 bits. Kill for the original's ledger: if the σ the original invented
  (≈0.0107/component) is off by more than one order of magnitude either way, its
  40.2-bit pole and 37 MB/epoch line misprice the belt by >3×.
- **P2 (secular program).** The true-LL program (free precession at the theoretical
  rate g = nμαb₃/2⁽¹⁾/4, fitted 6-feature form) recaptures less than half of the total
  Δz entropy: at 10-orbit windows the conjunction residual, not the secular trend,
  dominates. (The original's own LL rate was 2× the theoretical one — noted, not
  load-bearing here.)
- **P3 (A1, the decisive test).** The original's 12-term low-order birth basis
  (1, a, a², e0, cosω0, sinω0, cosM0, sinM0, a·cosM0, a·sinM0, a²·cosM0, a²·sinM0)
  fitted to the real kick recaptures **less than 20%** of the kick's entropy
  (residual ≥ 0.8·H_kick). Reason: the real kick's direction is set by the conjunction
  longitudes, which rotate by ~57 rad across the belt over the window — a steep, not
  low-order, function of birth a. If P3 holds, the original's smooth pole ("smooth
  ⇒ 0 bits") does not apply to real flybys as measured by its own basis: the coin-flip
  smooth/chaotic typing is not the real workload's split.
- **P4 (the fix).** A synodic feature set — for each of up to 10 conjunctions,
  Re/Im of e^{iλ_m} weighted by {1, e^{iω0}, e^{−iω0}, e0} (80 features, the
  event program knowing Jupiter's elements and the window) — recaptures **at least
  60%** of the real kick's entropy (residual ≤ 0.4·H_kick). If P3 and P4 both hold,
  the smooth pole survives with its basis renamed: the typing is event × program, and
  the right program basis for flybys is the synodic ladder, not low-order polynomials.
- **P5 (ledger consequence).** Real conjunctions hit every belt body every epoch, not
  1%/epoch: the belt's scar stock is H(after best program) bits/member from the first
  epoch, growing ~0.5 bit per window doubling (random walk), not 0.29 bits/member/epoch
  of newly-scarred bodies. At q24 that stock is 1.5–5 GB per 10⁹ with the synodic
  program (P4's residual), and the original's "≤0.6 GB + 37 MB/epoch" belt line is
  optimistic by ≥2.5×; with a q16 scar quantum per population it falls to ≤0.3 GB.

Controls: (C1) Jupiter off — the integrator must return z to <10⁻⁵ (its own noise
floor, far below any kick); (C2) in-sample fit sizes are ≤160 features on ≥65536
bodies, so recapture is not overfitting (shrinkage <0.3%).

Kill criteria for my own extension: if P3 fails (the low-order basis recaptures >50%),
the original's smooth pole applies to real kicks as measured and its belt line stands;
if P4 fails (<20% recaptured by the synodic set), real flybys are effectively chaotic
for any bounded program and the belt prices at the full pole with P1's σ.
