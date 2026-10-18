# Predictions (written before the decisive flights)

Question: the view gather emits `seen = N + 61` rows per frame (dcf1) at a linear ~5 µs/body.
Is that row stream *information* at the instrument that receives it (the wire/the sky), or a
no-op machine like the boundary comb? The sky in this 2-D universe is a circle: a row's place
on it is one angle. An instrument floor θ_f (an 800-px sky band ⇒ θ_f ≈ 8×10⁻³ rad; a 1-px
full-circle ratchet ⇒ ~10⁻³) bounds the distinguishable row count at ~2π/θ_f ≈ 10³, flat in N.

Cases not tuned on (the flights are coast, seed 1, frames 30 and 90, K ∈ {0, 10³, 10⁴, 10⁵, 3×10⁵}):

- P1 (count): seen = K + 61 at every rung (dcf1's law; belt rows are kind 3, light-seconds ~10³).
- P2 (the crossing): the *alone-in-cell* fraction of belt rows at θ_f = 8×10⁻³ falls from
  ~e⁻¹·(K→K/800 small) ≈ 80–90% at K = 10³ to under 5% at K = 10⁴ and under 0.1% at K = 10⁵;
  occupied sky cells saturate ≈ 2π/θ_f ≈ 6–8×10² cells by K = 10⁴ and stay flat to 3×10⁵.
- P3 (the control on the other side): the near set (locals, planets, moon, fleet: light-seconds
  < 100) stays sparse on the sky — alone-in-cell fraction ≥ 95% at every K; it is the
  resolvable content and it is ~61 rows, flat in K.
- P4 (cost/content divergence): view_gather p50 grows linearly in K (≈ 50 ms at 10⁴, ≈ 500 ms
  at 10⁵, dcf1's 5 µs/body) and the seen array's serialised bytes grow linearly in K, while
  the distinguishable content (occupied cells + near rows) is flat in K beyond 10⁴.
- P5 (the wire): the seen array's JSON is ≥ 100 B/row ⇒ ≥ 10 MB/s of wire at K = 10⁵ at 60 Hz,
  for ≤ ~10³ distinguishable rows.

Kill criteria for my own claim (if any fires, the "no-op machine" reading is wrong or scoped):
- If the belt's alone-in-cell fraction at 8×10⁻³ stays above 50% at K = 10⁵ (the sky is not
  saturated; each row is a distinct place the instrument can show).
- If occupied cells at 10⁻³ grow linearly with K between 10⁴ and 3×10⁵ (no saturation at the
  ratchet floor either).
- If the near set is NOT sparse (the resolvable content itself grows with K).

Blind spot I accept: sub-pixel rows still carry aggregate signals (colour/shift spread — the
patina) and any body can go hot and must re-enter the resolvable tier exactly when it
separates; the aggregate must also re-ratchet under zoom (OC#30). This probe measures the
*static* information content only; the trigger/churn constants are scan-locality's, not mine.
