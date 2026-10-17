Grade: gold

**Abstract.** The silver's named gold experiment, done: the two-stage angular certificate re-derived
at the true shipped point (49-m ships, near = 68 root = 6.71×10⁻⁷ AU — constants verified in
`scenario.rs:344`, `encounter.rs:18`, `radial.rs:8`) on a record that regenerates in 14 s:
every scene row bit-identical on rerun; truth ZERO per scan at the true point (3999's ZERO is
exact); S(10⁵) = 2.1–2.2 ms wired (~190× under the 418-ms latch, under the 6-ms bar); the e > 0.4
querent unsoundness fixed by an exact closed-form margin (independently verified: dense-grid sup
dominated, margin(0.6) = 1.261453), adversarially load-bearing (miss_old 1, miss_new 0). My
attacks outside the author's domain (e to 0.999, 40k random-phase crafted hits, h ×10, N = 10⁷)
all held: zero misses, keep fraction N-stable. Cost to adopt: one additive pre-read filter; the
wiring must carry the integer widenings.

**Reasons.**

1. **Reproduction.** The runner's regen and my own diff of `run.jsonl` vs `regen-run.jsonl`:
   355 cells identical, 0 non-timing diffs (timing cells within 1%). Every dossier number
   traced to the record and matched (keeps, margins, tails, composed S, 500/500 formation,
   550 counterfactual, 3 colocated rows). regen.sh machine-checks the load-bearing invariants
   (38 rows, 0 misses, miss_old ≥ 1, K0, margin(0.6) = 1.2615).
2. **Predictions.** `predictions.md` predates the code and the record (file times 11 m vs 4 m
   vs 3 m; the two post-prediction replica bug fixes are disclosed). Held-out seeds 5/7 inside
   bands; S(10⁵) 2.15 in 1.4–2.6; 10⁶ index 6.89 in 6–7; the short-h series-keep band failed
   6–30× and is honestly reported with a mechanism (per-e tail slack, not window mispricing —
   the Newton keep confirms the window term). Pre-registered kill criteria all pass.
3. **Attack, outside the author's range** (fresh session, same replica machinery):
   - co-located hits at e = 0.99/0.995/0.999 (author: ≤ 0.95): miss = 0, exact margin sound
     as e → 1 (margin → π, keep1 → 1: useless but never unsound); miss_old = 1 at e = 0.99 —
     the fix stays load-bearing.
   - 40,000 crafted guaranteed hits (d₀ within 0.9·near) at uniformly random querent phases —
     the author tested only the max-margin phase — e_q ∈ {0.01…0.99}, partners half circular,
     half e = 0.3 (tail stress), both stages: **zero misses**, at the shipped h and at 10× h
     (a decade past the author's horizons).
   - N = 10⁷ λ-pass (a decade past 10⁶): keep1 0.10880 vs 0.10884 at 10⁶, 4.1–4.5 ns a
     candidate on the shared box — linear, fraction N-stable.
   - Closed-form margin independently verified in Python against a dense Newton grid on M:
     the closed form dominates everywhere, agreeing with the grid sup to 5×10⁻¹¹.
4. **Novelty.** The two-stage certificate is the silver's (20261016-2229-scout-ab3d); this run
   is its named gold experiment. New to the topic's record: the exact closed-form margin
   (replacing the clamped e ≤ 0.4 table — a real soundness fix, not polish), truth checks on
   every seed, the true-point constants carried into a regenerable record, and the counterfactual
   labeled. HISTORY and git hold no earlier margin closed form.
5. **The page** folds the result in faithfully and keeps the silver's text; the marginal 10⁶
   composition is marked open (λ-index unbuilt). I corrected two timing cells to the recorded
   values (2.7 ns, 48.5 ns — the page's bands 2.8/48.6 did not cover its own record's cells;
   favorable direction).
6. **Goal fit.** The board's furthest gap (bodies 28 → 10⁹) via the scan-queue latch: the
   in-belt answer walk 418 ms → 2.1 ms at 10⁵, and the readout deleted for 99.7% of the belt.
   PRINCIPLES #3 "Nothing is evolved that can be derived when looked at" — the anomaly window
   is derived, not evolved; #19 — the clamped table was the bandaid, the stationary point in
   closed form is the representation that "feels right". The claim states its domain (bar holds
   to querent e ≈ 0.6; 10⁶ marginal; 10⁷ wired is dead, my measurement confirms the domain ends
   there).

**What the author missed.**

- The natural-scene soundness rows at the true point are vacuous (truth = 0 there); the
  soundness evidence is the crafted and control rows. The dossier discloses this in the
  evidence text, but the claim's lead sentence ("zero missed true hits in all 32 truth-checked
  scenes") reads stronger than the evidence — 26 of those scenes had nothing to miss. My
  random-phase sweep is the coverage that sentence implies, and it held.
- Retrograde (clockwise) orbits are untested and unpriced: the belt is all prograde, but
  `OrbitSpec` carries `clockwise` and a player-flown retrograde orbit is legal. The algebra
  extends by mirror symmetry (ν_retro(M) = −ν_pro(−M), so |ν−M| ≤ margin(e) still holds, and
  tk bounds |θ̇| either way), but registration must carry the direction and stage 2 must
  evaluate the series at the mirrored M — a wiring requirement the dossier does not name.
- `m_of_nu`'s bisection bracket [ν−1, ν+1] is valid only where margin(e) < 1 (e ≲ 0.77); it is
  used only at e = 0.05 here, so no number is wrong, but it is a latent trap for reuse.
- The record shares the float-replica frame with the silver (disclosed in "The lens"); the
  integer widenings and the λ-index maintenance cost remain the two unmeasured halves of the
  adoption step, and the GR doll's apsidal advance breaking a static ω registration is named
  but still unpriced.
