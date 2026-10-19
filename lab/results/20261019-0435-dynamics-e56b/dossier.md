# Dossier — 20261019-0435-dynamics-e56b

## Claim

The game case's leftover is closed: a coherent fleet crossing a belt is **not a
wall-reflection train** — it is **one crossing season, then a permanently elevated,
area-extensive hot plateau** (the belt at ~15× its cold rate for as long as the region
confines the fleet's energy), and **in free space one season with no step at all**; the
formation itself dies in the first crossing (velocity exchange), so checker2's "the fleet
stays coherent through a dilute cloud forever" misreads energy persistence as formation
coherence.

## Bottleneck

Board item 4 (smoothness/allocator) feeding the belt wiring (item 3 of "Headed next"):
chaos-shadowing open direction 2's unflown half — the mixed fleet×belt scene, the
wall-reflection train, and free-space one-crossing geometry (90b7's dossier names all
three). Gain: deletes the last unpriced formation class for the allocator (no train guard
is ever needed for fleet×belt), and hands the belt wiring a confinement trigger: a
crossing inside a confined region leaves a standing ~15× rate step, an open-space crossing
does not.

## Evidence

Shipped `Chronon` + `Law::RelativisticV1`, Q = 2²⁰. Scene `--scene mixed` (harness
`crates/lattice/examples/fleetburst.rs`, 90b7's file extended): coherent n/2 fleet at
drift q/4 crossing a thermal n/2 belt at cloudvmax q/16 in the band [1.5e, 2.5e] (e =
6·⌈√(n/2)⌉); `--boxscale` moves only the far wall; `--nofleet` is the matched control
(same box, same belt, same seed); `--free` drops the container. 17 flights (15-arm grid + H=24576 arm + digest-identity rerun)
horizon, every flight ≤ 100 s, one rerun digest-identical; regenerates in ~7 min
(`./regen.sh`). All numbers: `work/final.json`, table in `work/analysis.json`.

- **No clock anywhere (P1/P2 killed).** The predicted 4·w round-trip clock appears in
  neither series. Wall hits are a continuous rain: max 4-10 per chronon in every mixed
  arm (control 3) — the fleet never bounces as a block (a block hit is n/2 = 200-3200
  bodies in a few chronons). Contacts autocorrelation over the late two-thirds peaks at
  lag 64 ch (one window; broad structure, |r| 0.38-0.98), never at 4·w (1740-6840);
  smoothed maxima spacings drift and wash out (mb1600_bs2 s1: 1089 → 3841 → 6145, i.e.
  2752, 2304 against a predicted 3480 constant; mb400: 1472, 1920 against 1800).
- **The attractor is an extensive plateau.** At n = 1600 with w = 435/870/1305 (boxscale
  1/2/3, belt and fleet fixed, only the far wall moves): late (last third) 64-ch mean
  1007.5 / 496.0 / 357.0 → **mean × w = 438k / 431k / 466k, constant within 9% while the
  box triples**: the late rate follows density (energy per area), not any period. F64_late
  1.29-2.61, m_late 3.6-8.6% — near-Poisson; checker2's m_late 8.2% is this plateau.
  Versus the matched cold control (late 31.9/32.4, F64 0.91/0.92, flat — the negative
  control passes): **15.5×**.
- **The formation dies; the energy stays.** Season 1 (first crossing, ends t ≈ 2560 at
  n = 1600) costs **39.2-39.5 contacts per fleet body** (n = 1600; 16.8-17.2 at n = 400 —
  ≈ 1.35·per_row at both, the lane optical depth at fixed belt density, 90b7's √(n/2)
  exponent); jitter-fleet 38.9, coherent 39.5 — the formation's internal structure is
  irrelevant to both season cost and late state. The echo (the momentum front's return)
  carries **0.31-0.35 of season 1 at per_row 29 but ~1.15 at per_row 15** — arrival-time
  diffusion through the belt kills the echo chain exactly as σₓ killed 90b7's fleet-fleet
  train, with the belt's thickness (∝ per_row) setting the diffusion dose.
- **The plateau stands at the top rung.** n = 6400, H = 24576: 8192-ch block means
  3373 → 2286 → **2209** (−3.4% over the last block pair) — stationary within horizon;
  F64_late 27.7 (undulation residual at the largest n, same ringdown tail 84b2 measured).
- **Free space: one season, no step (P5 held).** `--free`: single season peaking at
  t = 1152/960/640 (the geometric meet time), then dispersal to late means of 0.4-1.6
  contacts/window, walls = 0 throughout. The persistent modulation checker2 measured is
  the box's doing (walls confine the injected energy), not the fleet's.
- **Determinism:** mb1600_bs2_s1 rerun digest-identical
  (`012568e5…` both runs); every flight's digest is in its TSV header.

## Predictions

`predictions.md` was written before the decisive grid, with the kill branch pre-stated.
Scored honestly: **P1 and P2 fired their kill branches** — no 4·w clock in either series,
so the wall-driven-train reading dies (the run's central result). **P3's alternative
branch fired**: not a limit cycle; the recurrence ablates (echo 0.31-0.35 at n = 1600)
into a stationary plateau. **P5 held** (one season, flat tail, walls = 0); its
"late ≈ cloud-only rate" half is void as stated — the free belt also self-disperses
(late mean → 0), so free-space flatness is dispersal, not a matched-rate equilibrium;
reported as such. P4 half-held (F64_late grows with boxscale 1.29 → 1.56/1.91 → 2.61;
maxW/late does not order monotonically). P6 held in exponent, not constant: 1.35·per_row
per fleet body per crossing vs 90b7's 0.4·per_row (different baseline and relative
speed). P7 held (seed 2: late 490.3 vs 496.0, F64 1.91 vs 1.56, same verdicts, echo 0.311
vs the s1 window-glitch arm reported from s2/mj).

## What would make it wrong

The plateau law (mean × w constant) is flown only on the boxscale ladder at n = 1600;
across n the box height changes with the fleet, so cross-n rate comparisons are not
area-normalised here. The "energy, not formation" mechanism is carried by three measured
signatures (no block wall hits, extensive plateau, free-space collapse) plus
bookkeeping — per-body velocity trajectories were not instrumented, so the two-temperature
reading (fast identities permuting through the belt, wall rain 8× the cold control) is
[INFERENCE]. Horizons ≤ 24576: a decay law slower than ~3%/8k ch would read as
stationary. `--free` cannot test confinement without also losing the belt (everything
disperses); a confined-but-wallless belt (gravity-held) is the unflown discriminator the
game itself will supply.

## Cost of adoption, fit with PRINCIPLES

Zero code: a measurement plus one trigger for the belt/formation wiring. "Compute only
surprises" (3): the crossing is the one surprise; what it leaves behind is a rate step,
not a schedule. "Regimes are chosen by dimensionless numbers" (4): the discriminator is
confinement (does the region recycle the fleet's energy?) times the belt's optical depth
per_row (season cost ∝ per_row; echo survival flips between per_row 15 and 29). "A failed
expectation is not a failed method" (9): two of seven predictions died and both deaths
are the result. Via negativa: no train guard for fleet×belt, ever; the allocator budgets
one season of ~14·extent chronons (peak window ~65× the cold belt's late rate, 3.8-5.8×
the post-crossing plateau), and the wiring treats a
post-crossing 15× belt rate inside a confined region as the standing cost of the fleet's
energy, not as a stutter to fix.

## The lens

Dynamics asked "where does it go when left alone" and found the attractor directly: not
the limit cycle the wiki's leftover implied (the wall-reflection train) but a relaxation
to an extensive stationary state, with the echo chain as the transient — the same
arrival-time-diffusion death 90b7 measured inside fleets, now delivered by the belt. What
the lens may have missed: the plateau's slow decay constant (needs horizons ≥ 10⁵ ch to
pin), the two-temperature decomposition per body, and the game's real confined belts
(gravity-held, not wall-held), where the step's lifetime is the open question.
