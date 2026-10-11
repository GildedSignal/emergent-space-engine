# Dossier — run 20261011-2028-system-3b42 (lens: the whole system)

## Claim

The doll's tube store sorted by (key, phase) is already the encounter index: the cycle memo's key
lattice, the Binet cone's U-axis and the co-orbital phase rank are three orders on that one
structure, so the encounter tier needs **zero per-body state beyond the tube's 16 bytes** —
`crates/encounters`' per-body element space (`Body`, 80 B) plus its `Sorted` U-index (~16 B/body)
delete, a second full copy of every body's state that at 10⁹ bodies is ~96 GB against an 8 GB
machine.

## Bottleneck

Board focus item 3 (finding encounters without work per orbit or per element change) and item 6
(the top scaling risk: candidate work must track real encounters). The gain is not a speedup of
the window setup (components-4643's finding stands) but a **deletion**: the encounter layer stops
carrying and maintaining its own per-body element state, which is the only way it can ship at the
goal's scale (B18's bar: no second full copy per body) and removes the per-kick maintenance of
that state (re-derivation, re-sort, re-setup bookkeeping) that the crate pays on every element
change.

## Evidence

All numbers from `cargo run --release -p emergent-encounters --example tube_lattice --offline
{belt,coorbital,formation}` (each mode ≤ 48 s, single-threaded truth, Linux x86 runner, 8 vCPU;
source saved at `work/tube_lattice.rs`, raw JSON at `metrics-{belt,coorbital,formation}.json`;
it reuses the crate's own `make_belt`, `radial_pairs`, `cone_pairs` and `truth_pair`).

**Zero misses (the truth tier ⊆ the lattice, conservative per-key ranges).** Three belts
(n = 600, σ_e ∈ {1e-3, 3e-2, 0.1}, ρ = 1e-3) × three key quanta (a-cells 256/1024/4096 over the
range, 256 e-cells): `missed_radial = 0` in all nine runs — every pair of the crate's own truth
tier (`radial_pairs`, r8 v2's candidate set) lies inside the key-quantized lattice. Candidate
inflation vs the exact per-body cone: **1.26–1.41×** on warm/hot belts, **2.1–2.6×** on the cold
belt (vs the truth tier: 1.005–1.9×). The quantum is the one dial: coarser cells share more memo
entries but inflate more (cold belt: 2.62× at 256 cells → 2.10× at 4096). Same-key pairs vanish on
spread belts (549 → 35 → ~0 as the quantum refines).

**The phase rank is the co-orbital certificate, on the tube's own axis (the crate's own adversarial
specs, held out).** `coorbital` (n = 300, a ∈ [1, 1.0001], 50 orbits): 2,093 truth encounters,
**every one within mean-longitude rank 2** (taleb-09b5's rank-4 certificate holds with margin).
`equal-period-keys` (spread ϖ on 3 equal-period keys — the case I flagged as the rank rule's
breaker): 1,496 truth encounters, rank 4 covers 94.0%, **rank 10 covers 100%** (worst rank 10) —
the crossing-class stragglers are bounded, not a blow-up.

**Concentration (one key cell, the taleb-09b5 regime).** A formation on one orbit (one key cell by
construction, clustered ϖ, arc of phases, sub-quantum period spread): truth at n = 256/512 —
rank 4 covers **100% / 99.7%** of 9,562 / 39,469 truth encounters. Candidate counts at scale:
lattice = **4n − 10 exactly** (4,086 at n = 2¹⁰; 65,526 at n = 2¹⁴) vs the quadratic tier's
n(n−1)/2 (523,776 / 134,209,536): the ratio is n/8 — **128× at 2¹⁰, 2048× at 2¹⁴**, growing
linearly in n, matching taleb-09b5's 135× at their scale and explaining its growth.

**Memory (arithmetic).** `crates/encounters`' `Body` = 8×f64 + 2×u64 = 80 B/body, `Sorted` order
16 B/body; the tube = key 4 B + ϖ 4 B + t_p 8 B = 16 B, lattice adds 0. At 10⁹ bodies:
~96 GB of second structure vs 0. Per-key constants (radial range, e, period) live in the memo
entry, amortised over the cell's population.

## Predictions

Written before the run (`predictions.md`). Held: zero misses on all belts (1); inflation under 4×,
measured 1.26–2.6× (2); the rank rule holds on `coorbital` (100% at rank 2) and **misses on
`equal-period-keys` exactly as predicted** — 91 events beyond rank 4, bounded at rank 10 (3);
formation candidates linear, 4n, quadratic tier ratio growing as n/8 (4); memory arithmetic (5).
One number moved: I predicted ≥ 95% within rank 4 on the co-orbital spec, measured 100% at rank 2.

## What would make it wrong, and the cost of adopting it

- **The strong-field doll.** Newtonian U = μ/L² is monotone in L, so the key order is the U order
  exactly; in Schwarzschild p depends on both E and L, and past the ISCO-adjacent region U(L) can
  turn. The fix costs no per-body state (each memo entry knows its own compiled turning points, so
  the key order reads the memo table) but the U-band scan's contiguity guarantee weakens: the
  strong-field belt is **unmeasured** here.
- **The straggler rule.** Same-key cells with spread ϖ need either rank scaled by the
  closure/spacing number (the dimensionless trigger) or a birth-fixed exact check (equal periods ⇒
  status never changes ⇒ paid once per key entry). Measured bounded (≤ 10) but not frozen.
- **The exact per-pair check** (sections, Diophantine windows) still needs the binding's exact
  state; this claim only replaces candidate *finding* and its per-body state, and composes with
  the slack skin (which defers the setup the lattice does not remove).
- **Adoption cost:** re-point the candidate tier at the tube store (per-key constants from the
  memo; within-key phase order maintained by the swaps `element-sort` already pays — the crate's
  own `steady` experiment measures that swap rate). The plane's `Encounters` seam (plane.md
  foundation 6) already isolates the swap; no rewiring.

## Fit with PRINCIPLES

- #6 "Store the generator, not the generated": the Binet point is generated — derived from the
  tube plus the memo entry; storing it per body is storing the generated.
- #24 "The memory floor is information… why do you need so many bytes per entity?": a 96 GB
  element cache at 10⁹ bodies fails the goal by itself.
- #32 "Symmetry is found, not given": the cone's 2+1 Minkowski structure and the phase rank are
  orders on the lattice the memo already implies — one representation, three services.
- #1 "The cheapest compute is compute not done": no second structure to derive, sort and repair
  per kick.

## The lens

What this lens may have made me miss: the elegant unification is measured on Newtonian Kepler
belts (the crate's own domain); the GR doll's non-monotone U(L) is the hard special case named
above, and the window-setup cost — the measured 92% of per-kick work — is untouched by it. The
system-level reading stands: the memo, the cone and the co-orbital certificate were being built as
three mechanisms (three rungs, two crates, a trigger); they are one lattice on the tube's own
16 bytes.
