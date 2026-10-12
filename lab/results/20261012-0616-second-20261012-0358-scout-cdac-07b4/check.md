Grade: gold

**Abstract.** Claim: the scout's live-memory law survives real Kepler conjunction geometry, 2.8–8.7× safer per kick than the rate-structure toy at matched rate; belt store 1.7–2.4 B/live-body at 10⁹, inside B18. Reproduced bit-identical (189 s, <0.5 GB); predictions 7/7 held. Verified independently: Gauss kicks against Cartesian impulses (3×10⁻⁴), stream-vs-snapshot accounting exact, B18 arithmetic. My attacks: an undisclosed azimuth-sort hole undercounts kicks 9.4% (K 59.5→65.7 with a one-line wrap fix; no conclusion moves); adversarial σ_e 0.15/0.01 belts stay 2.8–3.1× safer; "zero single kicks reach a quarter cell" is false (0.03% do, max 4 cells), though the 98–100% multi-kick escape evidence stands. Adopt with the named amendments; one step.

## Reasons

1. **Reproduction.** Clean copy of `work/`, `python3 hlive_real.py` (189 s, exit 0, well under 2 GB) then `python3 work/analyze.py`: `metrics-real.json` and `analysis.json` regenerate **bit-identical** to the stored ones (diff: only `machine` load and `wall_s`). Positive control (kick=False → D=0, 0 bits) passes. `patch.diff` empty; nothing outside the run folder touched.

2. **Predictions.** `predictions.md` (mtime 06:44) precedes the decisive run (07:04); the post-prediction script edit (07:00) is the disclosed D(t) replay bug. I verified the disclosure's load-bearing claim myself: final cells from the kick stream equal the propagated snapshots exactly (C6, ε=1e-3: D=295 both ways, cell arrays identical). All 7 predictions held: P1 2.78×/8.69× (ε=1e-3/1e-2, per kick-application — conventions checked, the toy's `events` are single-body applications matching real 2·crossings), P2 α 0.76–0.96, P3 wide-window 0.65–0.79, P4 repeat 0.48–0.93/dispersion 8–21, P5 stirring ×2.02 at m=1e-6 and flat at 1e-10, P6 store 1.69–2.39 B ≤ 2× floor + 2 B, P7 1.3–9.1 MB/h.

3. **Physics verified independently.** `gauss()` against a Cartesian impulse + independent element conversion on 20k random (a,e,f): median relative error 3×10⁻⁴, p99 3×10⁻³ — the linearized equations are right. B18 store arithmetic (Elias–Fano + delta entropy) recomputed: 1.694 and 2.394 B/body confirmed; floors 1.30/1.46–2.16 B confirmed.

4. **Attack 1 — detector hole (found, quantified, one-line fix).** The azimuth sort runs on `th = pom + f ∈ (−π, 2π)`, splitting physical neighbours into interleaved blocks; the wrap block bridges only some seams. Brute force vs the window on 25 sampled steps: 12–16% of near pairs missed every step. Patching `th → mod(pom+f, τ)` and rerunning C1: K 59.54 → 65.72 (**9.4% undercount**), contacts 87 → 111, s(1e-3) 2.56 → 2.35×10⁻⁴ (down, consistent with the run's own recycling story). No headline moves: anchor gap becomes 20–66×, MB/h lines shift <10%, matched-rate comparison and B18 store unaffected (rate-matched / saturation-bound). The dossier discloses only the b_det truncation, not this.

5. **Attack 2 — adversarial regimes.** Eccentric belt (σ_e=0.15): real 2.77× safer than the toy at matched rate; cold belt (σ_e=0.01): 3.09× safer. Direction robust across a 15× dispersion ladder.

6. **Attack 3 — dossier sentence contradicted by its own code.** "Zero single kicks reach a quarter cell at ε=1e-3 in 446k kicks" is false: on the C6 stream, 297 of 891,678 kick-applications (3.3×10⁻⁴) exceed a quarter cell; max single kick = 4.1 cells (deep-tail small-b, capped dv — exactly the ρ_b(0) tail the run itself measures). The substantive accumulation evidence (median 158–420 kicks to escape, 98–100% multi-kick, toy 82%) is measured directly and stands.

7. **Novelty.** No HISTORY entry measures H_live on real conjunction geometry (H entries end at H0215, 6 October; the scout run is today, its silver named exactly this gap). The α correction (−0.817) reproduces the scout checker's refit (−0.816) from the stored rows, as intended.

8. **Goal fit.** Board: "fitting 10⁹ in 8 GB … decided by distinctions created per game-second" — this measures those distinctions on the design's encounter semantics (truth.rs-style conjunctions, Gauss-mapped correlated kicks, recurrence, native stirring). PRINCIPLES 6: "influences below one quantum accumulate" — now measured on the real path (100% multi-kick at belt mass). The engine wiring (b-h-live on the plane's belt) remains queued for Sol/Astra and outside lab authority; the author ran and disclosed the cheapest decisive part, as the second-author brief allows.

## Required amendments before adoption (one step)

- Fold the θ-wrap fix into `hlive_real.py` (one line) and restate K as ≈21.8–72.2 kicks/body/orbit (9.4% undercount measured on C1).
- Delete the "zero single kicks" sentence; keep the multi-kick fractions.
- Relabel ρ_b(0): 27.3/AU is ~6.2× the toy's absolute uniform density (the stated 2.7× holds per unit b/a only).
- Note that `hlive_real.py`'s inline toy-α fixer is dead code (impossible range condition; `metrics-real.json` stores `null` there) — the −0.817 lives in `analyze.py`, which regenerates it.

## What the author missed

- The azimuth-block detector hole (attack 1) — the one instrument defect that touches a headline number.
- The "zero single kicks" flourish is contradicted by the code's own regenerable stream; deep-tail kicks do reach several cells, which the run's own ρ_b(0) story predicts.
- The α fits rest on 3–4 partial rows per config; fine as reported, but the C1 value (3 rows) deserves a wider ε sweep before anyone tunes a repack trigger on it.
- Two dimensions (no inclination) and N ≤ 1500 remain the honest limits stated; the store at true 10⁹ geometry (not fixed-Σ rate extrapolation) is still unmeasured.

Checker's attack scripts (throwaway, this container): `/tmp/check-cdac/work/adv1_physics.py` (Gauss cross-check, brute-force pair audit), `adv2_accounting.py` (stream vs snapshot, single-kick magnitudes, toy ρ(0), cap fraction), `adv3_detect.py` (detector fix, σ_e ladder).
