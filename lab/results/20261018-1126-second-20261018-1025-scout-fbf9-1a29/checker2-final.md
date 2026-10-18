Working...
**Grade: gold** — written to `check2.md`, page annotated in place.

**What I did (blind to the first checker's verdict):**

1. **Reproduced:** isolated rebuild of `flight/` against the shipped `crates/encounters` (clean tree, empty patch) — every deterministic field of `flight.out` **IDENTICAL**, 69 s. Verified instrument fidelity in the shipped source: `Sorted` scan → `is_candidate` → `arm_pair` (SAFETY 1.1, `ext = pi+2pj`, integer `first_hit`) is exactly the path `main.rs::kick` drives. The GM=TAU² kick model is element-space convention-free on the crate's GM=1 doll clock (v²/GM invariant).

2. **Predictions:** `predictions.md` (11:49) precedes the final `flight.out` (11:54); the smoke run (11:45) is a disclosed amendment that pre-registered its own P3 failure; the pre-registered kill line fired as written (0.1075 at 10⁴, 1.2 at 10⁵).

3. **Adversarials (my own, all outside or beyond the author's range):**
   - **n=10⁶** (two decades out): 6.6×10⁻⁶ flips-on/candidate, 79/79 outside the band, 6 real events, violator |Δn| tracking cell width — Θ(n) and the leak extend.
   - **Fresh 10⁵ seed + cold σ_e=0.01 belt:** reproduce (5.5×10⁻⁶/cand, all outside).
   - **Reach probes bracket ρ*≈4.4×10⁻⁵ AU:** at 6×10⁻⁵ (above), quantum flips collapse to 2/100 with violator dues ~4×10² intervals and 2⁻¹⁷ gives 138 — the dv-dependent walk regime; boundary real, quant-c9c7 reconciled.
   - **All 3 leaked events re-derived real** by an independent Kepler solver: 1.411/1.481/1.976×10⁻⁶ AU < reach 3.342×10⁻⁶. (My first pass rejected them — a 6.28× clock slip in *my* propagator, not theirs.)
   - **One miss found:** at dv=2⁻²⁶ the channel dies (0 flips vs ~11 expected) — "re-rolls under any kick" holds only for kicks ≳ the belt quantum. Annotated on the page.

4. **Novelty:** the published page holds only the toy-silver and smooth-regime slack; the shipped-tier refutation, ρ*, and the leak rate are new — this is the scout checker's named gold experiment, done exactly.

Gold by the rubric: reproduced, the decisive pre-registered prediction held, a premise (the due-band rule) is deleted from the design space at zero adoption cost, and the measured leak (~10⁻⁶ events/candidate/kick) is the number any future skip rule must gate.
