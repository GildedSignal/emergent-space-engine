# Predictions (written before the decisive run)

Topic: the downward E→1 crossing (Passage→Cycle capture in flight) — the page's named next
experiment, the checker's named gold experiment for 20261013-0236-inversion-57ce.

Probe: `crossing.rs` mode C<level>[.<plog2>] — fly the parent's A-flight to the star flip
(held forward, ×1.25 ladder, brackets), cut, coast to the bcoast state, then a scripted capture:

- Phase 1 (fixed-nose brake): re-assert one burn key every P ticks (default P = 2^(27−level),
  so the flush quantum Δη = α·P ≈ 7.6×10⁻⁶ ≪ the bound window 2·v_esc ≈ 4×10⁻⁴), oracle E at
  every decision, stop when E bottoms and rises (the dip) or the kind flips.
- Phase 2 (the flip): hold the turn key (2⁻³⁰ turns/tick) until the nose is on ±v̂ (error
  < 10⁻⁴ turns), then brake at the same fine cadence, attitude-correcting when the error
  exceeds half the capture window arcsin(√(2μ/r)/v).

Mechanism these predictions come from: `thrust::owed` burns along the fixed heading; a burn
along ±x̂ nulls only v·x̂. Capture needs the untouched perpendicular component v_perp <
v_esc = √(2μ/r) ≈ 1.4×10⁻⁴ c. The parent's A8 (forward pumps to E = 5.03) and B8 (reverse
pumps to E = 4.29) from the same state imply v̂ makes an angle with ±x̂ whose sine is a large
fraction of 1 — so I predict phase 1 walls out at E_min − 1 = v_perp²/2 − μ/r > 0.

1. **P1 (the fixed-nose wall).** Phase 1 brakes (E falls), bottoms at E_min > 1
   (E_min − 1 = v_perp²/2 − μ/r > 0), then pumps; no capture at any decision cadence, zero
   refusals. The measured E_min gives the v̂–nose alignment angle; I predict sin∠(v̂, x̂)
   of order 0.1–1 (not ≈ 0). Falsified (capture in phase 1) iff the arrival v is within
   ~arcsin(v_esc/v) ≈ 2° of ±x̂ — then the timing was the whole story and the checker's
   script works as written.
2. **P2 (the scripted capture compiles).** After the turn, every level tested (5, 8, 11, 15)
   captures: kind Passage→Cycle, zero refusals, alive, within ~v/Δη decisions of brake start.
   The flip lands at 1−E ∈ (0, ~v·α·P] ≈ (0, 1.5×10⁻⁹].
3. **P3 (the captured orbit is real and leave-safe).** k−1/2 > 0 at the flip; apoapsis =
   periapsis/(2k−1) ≈ 10⁸–10¹⁰ < 2⁴⁰ (leave-safe needs k−1/2 > 4.2×10⁻⁵; the landing band
   makes violation ≈ 10⁻³ likely — I expect the landed apoapsis ~10⁹, an orbit crossing
   Giant's).
4. **P4 (the clock at the seam).** |dt/dτ/u^t − 1| ≤ 10⁻¹¹ at the flip bracket — the downward
   crossing is where the clock is best, like the upward one (≤ 6.5×10⁻¹⁴ there).
5. **P5 (the capture survives).** At 2× the capture tick: alive, still Cycle, zero refusals,
   clock still exact.
6. **P6 (defect watch).** No decision observes oracle E < 1 − 10⁻¹⁰ while the compiled kind is
   still Passage (that would be a compile defect at the downward crossing — the gold nugget if
   it appears). Also: zero refusals at every flip, including the capture rebind.
7. **P7 (the coarse bridge to B8).** At L8 with P = 2²⁶ (Δη ≈ 10⁻³ per flush, B8's held-key
   regime), the dip is invisible and no capture — reproducing B8's pump quantitatively from
   the cadence alone, without any law change.

What would make this run matter: a refusal at the capture rebind, a compile defect (P6), a
leave-risk landing (P3 violated), or the fixed-nose capture landing (P1 falsified in the
checker's direction).
