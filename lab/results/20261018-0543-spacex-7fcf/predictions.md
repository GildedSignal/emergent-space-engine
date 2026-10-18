# Predictions (written before any flight of this run)

Question: does the composed law (ES_SECULAR + ES_CHAIN + ES_LOCAL_STAGGER, f134's strictly
dominant arm) carry a legality debt on the population it cures — the doll-born locals — at
the worst horizon, where 87fd's checker found the chain+stagger medians crossing OFF's
(6,700 gs) and OFF growing ~×10 per horizon doubling (19.8e-6 at 9,000 gs)?

Instrument: 87fd's `doll_probe` verbatim (print-only, shipped `Binding::readout`), plus one
disclosed print-only addition: the fraction of doll bodies with |ΔE/E0| < 1e-12 (the
mixture witness — a deleted body is a pure tube whose E/L read out identical between
checkpoints up to f64 noise) and the drift p25/p75. Flights: budget-free coast, N=1000,
rtf 100, seed 1; held-out: horizons 9,000/11,000 gs and seed 2. The composed patch is
f134's verbatim (`work/f134.patch`); arming controls reproduce 87fd's and f134's records.

## P1 — arming (known class, must hold or everything is VOID)

both@4,500 collapses the storm: max ev/fr ≤ 55 vs OFF ≥ 200; doll census {2: 310, 3: 3};
dead 0; encounters within ±3 of OFF's.

## P2 — the decisive inversion (held-out)

At 9,000 and 11,000 gs the composed arm's doll-born |ΔE/E0| MEDIAN is ≤ OFF's — the
opposite of chain+stagger alone at 4,500 gs (3.7× OFF, 87fd's kill) — because the deleted
majority stops sampling the tide at all. Concretely: median(both) < median(off) at both
horizons, and median(both) < median(chain+stagger) at every horizon flown.

## P3 — the spared quarter keeps the tail

The composed arm's p99 (and max) stays within 2× of OFF's and chain+stagger's at every
horizon: the spared set (resonant quarter + illegal in-situ) still rides real kicks.

## P4 — the ensembles hold

Cross-arm relative deviation of the med and p99 of E1/L1/r1 ensembles ≤ 1e-3 at every
horizon (87fd's band was 3e-5 at 4,500; I allow a widening at 11,000 but not past 1e-3).

## P5 — the mixture witness (held-out)

Under the composed arm, ≥ 50% of doll bodies read |ΔE/E0| < 1e-12 (the deleted pure tubes);
under OFF and chain+stagger that fraction is ~0 (< 5%).

## P6 — seed 2 (held-out)

Same ordering at 11,000 gs: median(both) < median(off), dead 0.

## Kill criteria (pre-registered)

- K1: median or p99 of |ΔE/E0| (or |ΔL/L0|) under the composed arm exceeds OFF's by > 2×
  at any horizon → the composed law adds an unpriced legality channel; adoption stays
  blocked.
- K2: any ensemble deviation > 1e-3 relative → the delete's carried sub-quantum debt is
  ensemble-visible at the worst horizon; the sparse re-kick cadence moves from "one law
  choice to price" to "required before adoption".
- K3: census ≠ 313, dead > 0, or encounters off by > 10% from OFF in any arm → instrument
  or scene mismatch: VOID, not a kill.
