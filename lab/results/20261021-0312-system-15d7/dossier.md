# Dossier — 20261021-0312-system-15d7 (lens: the whole system)

## Claim

On the belt's own stream the BOUNDARY comb never does certificate work — over a completed
flight of 500,000 game-s (~18 eras) at 3×10⁴ bodies it fired **0** crash, **0** leave and **0**
handoff for the 510,004 clock-stepped (belt) combs, while its certificates are
derived-when-looked-at from state the body already holds (the energy register the kick
updates); what actually survives the comb is the ramp re-anchor (`anchor = t`, hashed into the
digest), so the "-50% of stream events" cut (nladder od 2) is a *law-visible* change whose
price is the anchor, not the certificates.

## Bottleneck

Board row **Macro, kicks per body (~10³ at stake)**. The nladder page prices the boundary comb
(5.9–8.6 µs/boundary, 49.7/50.7% of the belt's stream, ~2.4 h/era at 10⁹) and names its deletion
"the cheapest first cut" (od 2, a31c) — but never measured whether the comb's certificates ever
fire. If they never fire and are derivable, the comb is compute for a surprise the stored
generator already rules out (PRINCIPLES 3: "Nothing is evolved that can be derived when looked
at"; 14: "no work for no reason, so no ticks") — and the deletion's real cost is named for the
first time (the anchor), which changes what od 2 must build.

## Evidence

Shipped code read first: `boundary_clock` (crates/universe/src/step.rs, the clock branch used by
belt bodies) checks exactly two certificates — surface and leave — and writes `anchor = t`;
`universe.rs:1327` hashes `r.anchor` into the digest; `kick_clock` already checks the surface at
every kick, including the planets' surfaces; `boundary_clock` has no handoff arm at all.

Instrument (print-only, no behaviour change; the run's `work/patch.diff`): atomic counters at
every `What::Boundary` dispatch, split clock/non-clock and by fire kind (crash / leave /
handoff), plus a per-fire stderr trace and the kick's own surface fires for contrast.

1. **Belt, completed flight** — `cargo run --release -p emergent-universe --example
   boundary_bill -- 30000 5000` (the horizon arg is wall-s at rtf 100, i.e. **500,000 game-s ≈
   18 eras**; 1/60 s frames, settled at the cut, seed 1, the page's own scene
   `scenario::plane_extra`, 111.1 s wall; `belt-era.txt`):
   `digest f9af771e9887a6fbc704a60b567aff26 | kicks 1,290,749 encounters 24,264 contacts 0 |
   boundary combs 1,267,977 (clock-stepped 510,004) | fires: crash 0 leave 0 handoff 18 |
   kick-surface fires 0`. Combs are 49.6% of the combined comb+kick stream (the page's
   49.7/50.7%); the 18 handoffs are all `release` in doll 2 — the *locals* leaving Home's doll,
   the non-clock handoff mechanism working (`belt-short-err.txt`). **Zero fires of any kind for
   the belt's 510,004 clock combs.**
2. **Determinism cross-check** — two longer runs (killed at the runner's 420/600 s caps)
   reproduce the identical deterministic prefix: the same 18 releases, zero clock fires
   (`belt-long1-fires.txt`, `belt-long2-fires.txt`).
3. **Control, plunges** — `cargo test --release -p emergent-universe --test plunge --
   --nocapture`: 2 passed, **zero boundary fires**: plunges are ended by the kick's own surface
   check or the planned `What::Crash` item, never by the boundary.

Controls on both sides: the locals' 18 releases prove the counters see fires when they exist;
the belt's zero is not a deaf instrument. The plunge control narrows the boundary's crash arm to
apoapsis-phased kicks (if the kick sits at periapsis, the boundary checks r at its maximum,
where it cannot precede the kick's check).

The derivation (design consequence, unimplemented): for a clock body the register holds the
energy; `E < 0` (bound) ⇒ apoapsis ≤ −μ/E, so leave-safe is **one comparison on the register**
(`−μ/E < 2^leave_log2`) at each kick — no readout. The surface certificate at apoapsis cannot
fire before the kick's own surface check for a periapsis-phased kick. Both certificates are
therefore derivable from state the body already holds; the comb's 5.9–8.6 µs readout computes
what the key implies.

## Predictions

Written before the decisive run (`predictions.md`). P1 held in its fires half (0 fires; the comb
totals: 1,267,977 combs, 40.2% clock-stepped, in `belt-era.txt`). P2 held (0 crash fires; the
mechanism reading stands). P3 took its first branch exactly as registered: plunges fire **0** at
the boundary, so the crash arm's domain is narrower than its cost; the locals' releases serve as
the positive control instead. P4 held by mechanism (0 leave fires; bound belt). The registered
"one era" windows understated the flown horizon: the completed flight covers ~18 eras.


## What would make it wrong

- A belt stream where kicks sit at **apoapsis** (a different birth phase or the cadence job's
  per-body clocks): then the boundary's surface check is the *periapsis-side* one and carries
  the crash certificate — the deletion would need the kick to take the check over (it already
  has the arm). The wt/cadence merge must re-fly this census.
- A population with E crossing 0 (assists, ejections — the 3b88 wall class): leave fires become
  real; the derivation must gate the deletion per body per kick (E<0 and −μ/E < edge), which is
  the one-comparison form above, not a global off switch.
- Encounters/handoffs among belt bodies: `boundary_clock` has no capture arm, but if the cadence
  work moves belt bodies to the non-clock branch, the locals' release fires show that arm is
  live and must stay.

**Adoption cost:** the anchor. Deleting the comb leaves `anchor` at the last kick, changing the
mid-step ramp readers see (`observe::credit`) and the digest input — so od 2's "1.2× cheapest
first cut" is not bit-for-bit bookkeeping; it needs either (a) the anchor written by the kick
(the lead field it already computes) and the digest re-frozen, or (b) the comb kept only for
bodies whose register fails the one-comparison gate. Fit with PRINCIPLES: 3 ("Compute only
surprises… Nothing is evolved that can be derived when looked at (clocks…)"), 14 ("no work for
no reason, so no ticks"), 19 (the comb is the clock's artifact, not the law's).
same structure the board's cadence row is re-deriving per body. What this lens may have missed:
the anchor's ramp may be load-bearing for readout fidelity in a way 18 eras of coast cannot
show (burns, encounters and the view read mid-step); and the window samples one seed and one
birth phase — the class, not the tail, is measured.
