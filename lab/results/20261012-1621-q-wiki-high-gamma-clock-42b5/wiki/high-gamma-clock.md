topic: high-gamma-clock
status: open
closed-by:
valid-while:
updated: 20261012-1621-q-wiki-high-gamma-clock-42b5

# The ship at high γ: its clock, its energy, the wall near γ 2,000

## Current best

- The shipped tube's clock stops dilating above γ ≈ 2 and the flight dies near γ 1,800 in the kick's rebind — both measured, both with causes (20261011-1600-inversion-e128, gold; two blind checkers reproduced it byte-identically, and the integrator re-measured it on the M1 — docs/HANDOFF.md, 12 Oct):

- **The clock saturates at dt/dτ = 2.** The proper time the player's page reads (`view.rs:262–267`), the burn flushes against (`step.rs:311–314`) and the event scheduler uses (`events/clock.rs`) carries time dilation only first order in v² (dτ/dt ≈ 1 − v²/2 → 1/2): local dt/dτ tails 1.96, 1.96, 2.00, and the compile pins E_∞ at exactly 2.0000 across γ 400–1,800 at two levels. A held burn therefore reaches γ its own coordinate time cannot afford: γ/γ_ext = 1.06 at γ 2.2, 3.72 at the merge's green point (β 0.999177), 87 at γ 1262, 112 at the freeze; at t = 7.74×10⁹ ticks the clock reads 4.21×10⁹ where relativity affords 1.8×10⁹. The HUD's rate dial — computed exactly from the state — then contradicts the ship's clock by ~630×. The burn and the i128 register are exact *in this τ* (γ_pred ≤ 3.8×10⁻³ from β 0.03 to γ 1262; |p_t − (U_P − H_D)| ≤ 6.4×10⁻¹¹, zero register refusals): the defect is the time map alone.
- **The wall is a key word, not the tube.** The flight ends at γ 1761 (L15), 1791 (L12), 1803 (L13) with `Space(Range)`: during the kick's rebind, the orbit key's k = 1/(1+e) falls toward 2⁻²⁸ and the 48-bit word's relative error trips the 2⁻²⁰ check — 137× short of the leave radius. The ψ-panel tube itself covers the whole regime: plunge, direct-capture, near-radial, γ 2000 and photon orbits compile into it exactly (≤ 1.3×10⁻¹⁰ against an independent oracle, horizon crossing finite and smooth in Kerr–Schild time; near-critical orbits need panels ∝ ln(1/δ); 0.55 ms compile, 3.1 µs/readout) (20261009-2043-scout-a1a4, silver).
- **The frozen 3% work gate certifies nothing above β 0.2474** (ratio 1.0303 there, 27.2× off at γ 1262): its work grows as γ−1 while the Newtonian energy it compares against saturates at c²/2 — the criterion is the law's Newtonian limit (20261011-1600-inversion-e128).
- **The frame around the ship survives.** The light-cone crossing solver written in the tube's frame never fails and never picks a wrong root at any γ ≤ 2×10⁶ (second checker: still 0 fails at γ 2808 under acceleration), while the same solver in raw observer-frame magnitudes mis-locates emission at γ 2×10⁶ (~12,700 events; root ambiguity ≈ ulp/slope ≈ 10⁴ s): crossings stay in the tube's parameter (20261008-1947-redteam-efb2 and its second check, silver). The view's aliasing boundary (≥ ~1 received orbit per frame) already falls inside the plane's envelope at slow emitters (γ ≈ 1.9×10³ at β_o = 0.01) — that line is the view page's.
- **Domain:** one scene, one seed per level (12/13/15), forward held burn, star frame. Not measured: reverse burns, turn keys at high γ, the `seen`/Doppler instruments, near-star passages, level 8, directions. The fix in flight is the integrator's, not a lab result: `wt/clock` — an exact-in-E clock and the Q48 gap as mantissa + exponent, behind gate C1 (dt/dτ vs u^t ≤ 1%, γ vs closed form ≤ 1%, zero refusals, levels 8 and 15; docs/HANDOFF.md, 12 Oct).

## Refuted
- "The register or the word is the wall" — the register is exact through the freeze; the wall is the rebind's k-word check, and the deeper defect is the clock (20261011-1600-inversion-e128).
- "No tube past γ ≈ 2,000, nor for plunges" — the same tube *form* compiles γ 2000, plunge, near-radial and photon orbits to 1.3×10⁻¹⁰, proven standalone; the shipped engine still refuses until it is wired in (20261009-2043-scout-a1a4).
- e128's author mechanism ("a saturating weak-field energy map") — `fit_key`'s energy predicate is exact; the constant 2.0000 is a clock integrand first order in v² (20261011-1600-inversion-e128, check2).
- e128's L5 control "< 1×10⁻⁶" — not regenerable (0.59% measured, probe-quadrature-limited); the conclusion (the gate passes in its own regime) stands (20261011-1600-inversion-e128, check2).

## Open directions

1. **The unmeasured regimes** (the board's line: levels, directions, near the star — never the same forward-burn probe again): reverse burns (the playability fix brakes to rest), turn keys at high γ, near-star perihelion passages, level 8, fresh seeds (20261011-1600-inversion-e128).
2. **The `seen`/Doppler instruments at high γ** — they read retarded states and could mask or double the wrongness the player perceives; unread (20261011-1600-inversion-e128).
3. **The scheduler's entanglement** — `events/clock.rs` schedules dolls on the saturated map; the standing "fast dolls need root-clock event keys" item may be this bug seen from the events side; one look when the time map is fixed (20261011-1600-inversion-e128, check2).
4. **After the fix:** re-measure the wall (does it track the Q48 gap as the build's pin says?) and the clock–rate-dial agreement; e128's γ 1761/1791/1803 and 137×-short-of-leave are the before-picture (20261011-1600-inversion-e128).

## Contradictions

None open. The one disagreement inside the record — the saturation's mechanism — was resolved against the source by the second checker (the energy predicate is exact; the clock integrand is first order in v²), and the `wt/clock` pin (dt/dτ = 2E²/(E²+1)) agrees with that reading.

## Runs

- 20261011-1600-inversion-e128 (gold): clock saturates at dt/dτ 2; the wall (γ≈1800) is the rebind's k word; gate dead above β 0.25.
- 20261009-2043-scout-a1a4 (silver): plunge, capture and γ-2000 orbits compile into the same ψ-panel tube, exact to 1.3×10⁻¹⁰.
- 20261008-1947-redteam-efb2 (silver): doll-frame crossing solver exact to γ 2×10⁶; observer-frame form mis-locates emission; the view aliases (→ view).
- 20261008-2031-second-20261008-1947-redteam-efb2-4d7e (silver): confirms the solver (0 fails to γ 2808 under acceleration); the view's PASS is convention-carried (→ view).
