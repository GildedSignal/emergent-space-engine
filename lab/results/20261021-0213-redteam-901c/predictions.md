# Predictions — 20261021-0213-redteam-901c

Target: `docs/representation.md` L50 — "Thrust grows the rapidity linearly in proper
time; in a field, E and L change by the work done" — the decision/kink law, never
measured against GR by any of the page's 46 runs (checked: no rung has a thrust arm;
`thrust.rs`'s own doc comment repeats the sentence while the code does a local boost +
rebind).

Cases below are NOT tuned on: circular starts at r = 6, 10, 20, 100, 10^4 M
(static-frame orbital speed w0), prograde and radial impulses of Δη = 0.05 and 0.25,
plus a finite-burn composition run (r = 6 and 20 M, total Δη = 0.25, flush quantum
q = 2^-6 and 2^-8 of local speed).

## P1 — controls (must hold, else the instrument is broken)

- Flat space (M=0): lump boosts of any cadence compose the rapidity exactly;
  error in final E-analogue < 1e-10. A failure here means my boost replica is wrong.
- Weak field r = 10^4 M: letter/exact ratio for ΔE and ΔL within 1% of 1.
- Radial impulse: ΔL = 0 in both exact and letter (torque-free control).

## P2 — the letter kill (closed form, one event)

The letter's work rule (a builder's natural reading: Newtonian E = ½|v|² − M/r on
coordinate velocities, L = r·v_t, update from the velocity change at the event)
against exact ΔE = f·Δγ_static, ΔL = r·Δ(γ w_t) at the same event, same boost:

- At r = 6 M, prograde Δη = 0.25: the letter under-reads ΔE by a factor I Fermi at
  0.4–0.6 (i.e. a 40–60% error), and ΔL by a similar factor. [Pre-run Fermi, shown
  in dossier: ΔE_exact = 0.1198 vs ΔE_letter = 0.0639 → ratio 0.53.]
- The error falls roughly like M/r: within a few % at r = 100 M, < 1% at 10^4 M.
- Consequence visible to the player: at r = 20 M a Δη = 0.25 prograde burn crosses
  E = 1 (escape) exactly; I predict the letter reads the same burn as still bound
  (E_letter < 1 by its own scale). Exact-oracle classification (bound vs escape)
  disagrees with the letter's classification.

## P3 — the shipped code vs the letter (closed form, one event)

The shipped `thrust.rs::burn` (exact local boost in the static orthonormal frame,
converted back) reproduces the exact ΔE and ΔL of the same impulse to < 1e-12
relative — i.e. the code is exact and does NOT implement the sentence it cites
("changed by the work done, and nothing else"). If my replica of `burn` misses
exact by more than 1e-12, my replica is wrong, not the code (I will then port the
code's algebra more carefully before claiming anything).

## P4 — composition (finite burn, integration)

Engine semantics (coast on the exact geodesic between flushes, lump the owed rapidity
at each flush) vs exact continuous powered geodesic (a = α(n + (n·u)u)), same total
Δη = 0.25, same fixed global bearing (initially prograde):

- At q = 2^-6 (the shipped quantum): final E error of order 0.1–3% relative to ΔE,
  L error similar order. [Anchored on system-2964's independent "~1% off its own
  fine limit".]
- Refining q = 2^-6 → 2^-8 reduces the error by ≥ 4× (I expect the deferral error
  to be second order per flush; if it scales only 2× the order is first and I report
  the miss).
- Flat-space control at q = 2^-6: < 1e-10 (the lump is exact there; all composition
  error is gravity × deferral).

## What would make each wrong

- P2 failing (letter within 1% at r = 6 M) would refute my attack: the sentence's
  Newtonian reading would be adequate at the strengths that matter.
- P3 failing would mean the shipped code has its own error, bigger than the letter's.
- P4 error at q = 2^-6 above ~10% would mean the flush semantics (not just cadence)
  is a premise break of its own, worth a rung with a tighter bar.
