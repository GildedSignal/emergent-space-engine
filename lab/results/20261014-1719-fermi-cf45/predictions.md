# Predictions (written before the decisive run; run id 20261014-1719-fermi-cf45)

Question: which clock steps a root-doll belt body — its own period (`step_for`, the secondary dolls'
law) or its doll's (`ext::constants`: P of the doll's shortest secondary, refined by position through
`dt/ds = f'(U_P + c)`)? The two wiki records disagree by P_own/P_D ≈ 12–22× at the plane's 2–3 AU belt.

Instrument: `cargo run --release -p emergent-universe --example cadence [-- N]` (this run's patch),
seed 1, N=4000 (locals 300, belt 3,700). Read-only on shipped code (one new example; nothing patched).
Two independent readouts: per-body planned interval (`b.kick.len`, ticks), and the global kick
counter delta over the headless advance (the belt is 92% of the population, so the counter is a belt
counter to ~10%). I tuned nothing on this scene; the derived expectations below come from
`ext.rs`/`step.rs` arithmetic and the record's own anchors (Cinder 88 d; the wave at 13.0–14.5 ks).

## Point predictions

- P1 The root doll's shortest secondary period P_D ≈ 88 d ≈ 7.6×10⁶ s (the record's Cinder).
- P2 Belt (root doll) interval p50 ∈ [2.2×10⁴, 5.5×10⁴] s, i.e. P_D/2⁷ (5.85×10⁴) within one octave
  down (log2_floor rounding): the wave's first kicks at half that (1.1–1.5×10⁴ s) must match
  taleb-6138's measured 13,037–14,542 game-s — a reproduced anchor, not a free parameter.
- P3 **The discriminator:** belt interval flat in a across the 2–3 AU quartiles (log–log slope
  < 0.15), against the own-period law's slope 1.5 (a 1.84× rise across the band).
- P4 Belt kicks per own orbit p50 ∈ [1,100, 2,800] (= 2⁷·P_own/P_D × the rounding octave); the
  counterfactual `step_for` on the same bodies gives ∈ [128, 256]×(1±2×) fewer-or-equal: measured
  interval 12–30× shorter than `step_for` at p50.
- P5 Locals (Home/Moon dolls, d≠0): kicks per own orbit ∈ [128, 256] at p50 — effb's rate = 2⁷/P_own
  holds there, and its roster reproduction (202–223 kicks/orbit) is explained by doll membership.
- P6 Steady state (t = 60 ks, ≥ 2 intervals in): belt interval within ±30% of birth (the f'(U_P+c)
  refinement moves with position; the belt is ≥ 0.7 AU from any secondary); no tightening trend.
- P7 The two instruments agree: 1/(interval p50) vs counter delta / belt bodies / elapsed within 25%.

## Held-out / adversarial (not tuned on)

- A: any ladder local placed in the ROOT doll (if the draw puts one out of Home's doll) must sit on
  the doll interval (≈ P_D/2^7-8), not its own period — doll membership, not kind, picks the clock.
- B: belt bodies' interval spread within one quartile comes from position (U_P + c variation), so
  p01–p99 within a factor ~1.3; a much wider spread would mean a per-body term I have not modelled.
- C: the advance's event stream must be belt-dominated: kicks delta / bodies ≈ elapsed / interval
  (up to the locals' small share); if the counter reads ≫ that, the belt is being kicked by
  something else (an encounter/second-order term) and the cadence reading is contaminated.

## If the doll clock wins (expected)

- effb's "rate = 2⁷/P with κ∈[128,256] — a pure birth constant" is the secondary-doll law read onto
  the root doll: wrong for every belt body outside ~Cinder's own orbit, by P_own/P_D (×[0.5–2] more
  from the Δs octave rounding and f' refinement). The 10⁹ quiet-belt kick bill for the plane's
  actual 2–3 AU belt recomposes ~12–22× higher than effb's code-derived 1–2 AU composition.
- ladder.txt's "2⁷ per Cinder period, whatever its own period" is right for the root doll; both
  records are right in their own dolls — the contradiction is a doll-boundary artifact, now measured.
- The `step_log2` dial keeps its 2×/octave leverage but its anchor changes: rate =
  2^step_log2/P_D · (f'(c)/f'(U_P+c))⁻¹ for every root-doll body at once, and the belt's kicks per
  own orbit (1,500–2,700 at 2–3 AU) sits 5–8× over the board's "≤ 512 events per orbit" bar and
  ~50–80× over H0190's 32/orbit averaged ladder — the doll's shortest secondary taxes every body in
  the doll; the physics question (is Cinder's clock the right quantum for a 2–3 AU belt body?) opens.

## If the own-period law wins

- taleb-6138's tight wave (p01–p99 spread 8%) must be explained another way, and ladder.txt's
  belt_first doc comment is wrong on shipped code; effb's composition stands as published.
