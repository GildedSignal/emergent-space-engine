# Dossier — 20261015-2041-fermi-99b5 (Fermi)

**Claim.** The belt's shipped kick cadence is **1.9×10⁻⁴ per body per game-second**
(5.4× the doll-interval law on the wiki), every 10⁵-and-up coast flight on this box
measures the 12 ms budget rather than that law (14% delivered at 10⁵, predicted 17%),
and at 10⁹ the composed bill is **memory-bound at 163–220×** (the record stack,
0.98–1.32 TB) against **CPU-bound at 1.1×** today (kicks 8.3–31 cores + re-mints
0.71 cap'd / 9.1 uncapped) — so 0757's "~0.15 cores re-mint at 10⁹" understates the
steady state **4.8× (cap'd) to 60× (uncapped)**.

**Bottleneck.** The board's #1 item (bodies: 10⁶ flown against 10⁹) reads through
composed ledgers: effb's 10⁹ ledger (silver, 14 Oct) was corrected 24× by cf45's
cadence law the same day, and today's adoption prose was off 10³ on both 10⁹ terms
(d6ba's checker). This run re-anchors the ledger on the shipped law itself. What it
lets us delete: re-mint arithmetic built on throttled 10⁵ counters, and any further
seam-line work aimed at memory terms the record stack already dominates by 100×+.

## Evidence

Shipped code, no behaviour patch (`work/patch.diff` only cfg-gates the macOS
footprint call so the example links on Linux). Four flights of
`crates/universe/examples/nladder.rs` (seed 1, coast, the standard ladder scene —
my `catalogue 10,076 entries` at 10⁴ equals 8b89's published ctl bit for bit):
a shallow cut (pre-settle) and a deep cut (past ~26k game-s) at 10⁴ (rtf 900,
unthrottled: p50 3.2–3.8 ms against the 12 ms budget) and 10⁵ (rtf 3000).

**The law's cadence (the 10⁴ rung, depth-differenced):**

| arm | kick rate /body/game-s |
|---|---|
| 10⁴ shallow (0.9–18.6k gs) | 2.08e-4 |
| 10⁴ deep (0.9–44.6k gs) | 1.99e-4 |
| 10⁴ differenced (18.6–44.6k gs) | **1.93e-4** |
| 10³ rtf 100 (ladder.txt, shipped artifact) | 1.86e-4 |
| 10⁴ rtf 100 (ladder.txt, shipped artifact) | 1.90e-4 |

Depth-invariant, rtf-invariant, no first-settle step (shallow ≈ deep). Implied
interval 5.2×10³ game-s ≈ 86 min — **5.4× shorter than cf45's 2.814e4 s doll
interval**, and cf45's law is the standing correction on this page's ledger. Either
cf45's interval belongs to a different belt (the plane's own, not the ladder's
2–3 AU one) or the constant is off; the discriminator is which doll owns the
ladder belt's step.

**The throttle (the 10⁵ rung delivers the budget, not the law):** measured depth
rate 2.69e-5 = **14% of the law**; held_max climbs 67 → **2,048**; lag saturates
≈50 s. Predicted from arithmetic alone: the law at 10⁵ needs 20 kicks/game-s; at
rtf 3000 that is 4.34 cores of kick work against the 0.72-core budget
(12 ms × 60 fps) → **17% deliverable**. Measured 14%. So every per-body-per-game-s
counter read off a 10⁵+ paced flight on this box (mine, ladder.txt's 1.96e-5, the
wiki runs' promotion/demotion rates under rtf pacing) is a budget reading —
3294's checker already saw the jitter; here it is 7×, and it has a signed cause.

**Memory (shipped, both rungs):** birth state 2,347–2,464 B/body RSS, dashboard
1,373–1,437 (engine accounting), catalogue N+76 entries, all matching 8b89's ctl.
Depth-invariant at 10⁴ (birth 2,461→2,464; flight growth 0.0077 B/body/game-s);
at 10⁵ the flight grows 0.086 B/body/game_s — the held scans hold their retention
too (the throttle's memory shadow, 11× the 10⁴ rate).

**The 10⁹ composition** (`compose.py`, every constant cited):
law 1.93e-4 × 10⁹ = 1.93e5 kicks/game-s.
- kicks: **8.3 cores** at c01c's 43 µs, 30.9 at the scoreboard's 160 µs, **0.01 at the 50 ns floor**;
- re-mints (promotions = demotions = fired kicks: 3294's fire-rate 1.000 census + the seam's demote-on-settle): **0.71 cores** cap'd coast (p50 3.7 µs, d6ba), **9.1 uncapped** (12.7 reads/dem, f55d);
- CPU today (cap'd, c01c cost): **9.0 cores = 1.13× the M1's ~8 sustained**;
- memory: record stack 980–1,317 B/body (d6ba bpb_engine) = **0.98–1.32 TB** against the ~6 GB budget = **163×**; the seam's arcs add 8.6 GB;
- **memory binds 145× harder than the CPU overage.** The retention alternative is no escape: the burn knee at 10⁹ is ~1.4 TB (quant-0619).

**0757's check:** their "~0.15 cores re-mint at 10⁹" divides the 20k-cut promotion
count (1.31/body, a paced 10⁵ arm) by game-time. At the law's cadence the steady
bill is 0.71 cores cap'd (4.8×) and 9.1 uncapped (60×). The direction of their
adoption sentence survives (re-mints are cheap with a cap on the belt); the number
does not.

**Commands** (≤ 60 s each; full regen ≈ 4 min): `lab/results/20261015-2041-fermi-99b5/regen.sh`
(builds with the patch, freezes the binary, flies the four arms, prints the JSON).

## Predictions

Pre-registered in `predictions.md` before the flights. **P1 failed** (the rate is
5.4× *above* cf45's law, not within ×2 of it — the interesting failure: the standing
correction is itself off, or scoped to another belt). **P2 failed** (no first-settle
step at 10⁴: shallow ≈ deep; the 26k settle is the *seam's* demote event, not the
law's kick onset). **P3 half-held** (no growth past the settle — memory pins at
birth; the ≤5 kB half held: 2.35–2.46 kB gross per body at depth). **P4 half-held**
(memory ≥100 GB: 0.98–1.32 TB ✓ binds ≥25× harder than CPU ✓; but the CPU bands
missed — kicks 8.3 not ≤4, re-mints 0.71 not 0.1–0.3 — both because the law's
cadence is 5.4× the constant I composed from).

## What would make it wrong

The law rate is measured only where the engine is unthrottled (10³–10⁴); if the
cadence mechanism is N-dependent (it should not be — it is the doll's step clock,
per-body), the 10⁹ kick term moves proportionally. The re-mint chain assumes
promotions = fired kicks at steady state (3294 + the seam's demote-on-settle);
if a future cadence split (kick-cadence direction 2) cuts the belt's kicks 8×,
kicks fall to ~1 core and re-mints to 0.09–1.1. The record-stack constant is
d6ba's engine accounting at 10⁵ depth (my RSS anchors agree at birth); if the
demoted record shrinks below ~100 B (3dc8's 113 B record is already the slot's
content), the 10⁹ memory term falls with it — that is the point: it is the one
term that must fall next.

**Cost of adoption:** none (no code change; `work/patch.diff` is a Linux link fix).
**Fit with PRINCIPLES:** "Measure before claiming" and "the simulation tells us
what's next not us" — the 10⁵ counters were telling us the budget, not the law;
"Fermi-estimate before building" — the composition kills the next seam iteration
before it is built.

## The lens

Fermi estimates trust their constants; this run's value came from refusing to —
two of the four pre-registered bands failed on the constants, not the arithmetic,
and both failures are the result. What the lens may have missed: the throttle is
also an instrument finding (per-body rates are only law at rungs the budget
clears; a rung's lawness is checkable from held_max and the budget arithmetic,
and future runs should report it).
