Working...
Check complete. `check.md` written to the run folder — the only file I changed there.

## Verdict: silver

**Reproduced (clean tree, empty patch.diff — all work lives in the run folder):**
- `validate.py` (31 s): schemes implemented correctly; dkd τ²-then-floor, saba τ⁴, whc3 2.17e-10 at 160 ko vs claimed 2.2e-10. Floor constants differ up to ~5× across libm builds (equal-kicks saba2 gain is 58× here, not 280×) — order-of-magnitude only, conclusion unchanged.
- The S1 moon table reproduces **digit-for-digit** against the author's stored ref: 8 kicks/orbit is the floor at e₀=0.05; dkd passes there, nothing passes below, whc3 pays 40 ko for the same behaviour.
- s4.json/dyadic.json internally consistent with the transcriptions; predictions.md predates the sweeps per file times, tuning confined to validate.py as declared.

**Adversarial runs (mine):**
- **μ=3e-3 resonance** (author's unfinished hardest B17 case): dkd holds +1.3% pump at 8 ko — the claim's declared wrong-maker #2 dissolves.
- **e₀=0.3 moons** (unfinished held-out, inside B14's judged range): dkd floors at 16 ko; every corrector scheme fails at 8–40 ko. Prediction S1h falsified in the claim-*strengthening* direction — but the universal moon cut is 8×, not 16×, once e₀≤0.3 counts.

**The finding that blocks gold:** dossier point 5's telescoping mechanism is wrong for this code. `Z` evaluates sub-kicks at fixed `t`, so the corrector conjugation telescopes **exactly** for any time-dependent accel — verified: whc3 vs whc3b final states agree to 2×10⁻¹² on the stable moon. And sweep3's "whc3b gives exactly dkd's numbers" is a code-path artifact: `runA2` calls `step()`, which applies no corrector for whc3b — bitwise identical to dkd. The conclusion survives (the corrector is *exactly* a relabelling, so it can never move element-behaviours), but a load-bearing point carrying a wrong mechanism plus an artifact leg cannot carry gold.

**Path to gold (named):** `behave` B14/B17 (+ B12's two-doll changeover) on the integer law at `step_log2` 3–4 vs the current 7 — a one-line config change (`Config::step_log2` default 7, confirmed in `crates/universe/src/ctx.rs`) against the engine's dominant cost (29 µs/kick per HANDOFF).
