Grade: silver

**Abstract.** Claim: live memory follows the surprise rate, not light-cone volume; belt self-encounters are no 10⁹-in-8-GB risk. Reproduced bit-for-bit (45 s, 77 MB RSS); every dossier number matches metrics.json. My attacks strengthened it: MB/h is sub-linear in Γ (Γ×91 → MB/h ×23), 82% of scars are accumulated multi-kick escapes (instrumented — the author's reading of the sub-linear exponent is right), N-invariance holds to 10⁶, and the saturation store at 10⁹ fully scarred is 0.5–2.1 GB < 4.29 GB. But P1's band failed (0.88–0.94 vs 1.00±0.06), P5's negative is weak, metrics.json's `alpha_partial` (−0.42, fits the saturated plateau) contradicts the dossier's α≈0.8 (correct from the rows: 0.82), and the law rests on a rate-structure toy, not the design's encounter+kick path. Cost to adopt: numbers and fire-at-T_x timing for b-h-live/B18, no engine change.

## Reasons

1. **Reproduction.** `python3 work/hlive_scout.py` in a clean copy: regenerated metrics.json **identical** to the stored one (diff clean), 45 s wall, 77 MB RSS. Positive control Γ=0 passes (D=0, 0 bits). File order supports pre-registration: predictions.md (t−11 min) precedes the final script (t−3) and metrics.json (t−2). `patch.diff` empty; nothing outside the run folder touched.

2. **Predictions.** P2 held (early cone exponent 2.57, flat 1.048 after T_x=4,990 gs; belt-scale T_x = 2.4 AU/c · 3.156e5 = 11.98 gs ✓). P3 held in the partial regime: my refit over ε ∈ [10⁻², 10⁻⁴] gives −0.816; **but the stored `alpha_partial` = −0.418 because `fit_power` includes the saturated plateau** (0.1447 < 1.0 passes its filter) — the field is mislabeled; the dossier's number is right, a metrics.json consumer gets the wrong lever. P4 held (13% shared ≪ 50%). P1 failed its band, honestly; my instrumentation (per-body max single kick vs final cell, return tracking) shows it is structural: exponent falls further when early transients are excluded (0.937 → 0.875 over t > 50%), 82.1% of scars needed ≥ 2 kicks, 528 bodies escaped and returned — the sub-quantum accumulation channel is real, not a fit artifact. P5 failed; the Γ(e) coupling cannot test stirring (author concedes).

3. **Attacks (all inside budget, ≤ 176 MB).**
   - Γ sweep 1.1→100 (m=10⁻¹⁰, ε=10⁻³): MB/h rises 0.43 → 10.05 — **sub-linear** (s drops from 0.0035 to 0.0009 as kicks recycle already-scarred bodies). The lens note "linear in Γ" was pessimistic; the toy is more storm-robust than the author claimed.
   - Saturation: m=10⁻⁶ for 9 orbits → D/N = 0.9998. Honest full-store at 10⁹ = (1-bit map + 3–15.5 bits delta)/body = **0.5–2.1 GB vs 4.29 GB live budget**: the conclusion survives even where the MB/h framing does not apply (m ≥ 10⁻⁸ scars ~everything within ~3 orbits; S7's own D_over_N is 0.55–0.96).
   - N-invariance extends to 10⁶: D/events = 0.00727 vs 0.0071–0.0072.

4. **Novelty.** HANDOFF:70 says H_live "not measured yet"; no H entry measures the live growth law or tests cone-volume vs rate. components-98bc measured the static program (0.126 bits/body), H0173 precision spend (4 bits/collision) — neither answers this. CRAM/git-pack was already a lead (polymath scan, 28 Sep) and half-adopted (law.md populations, idle-time repack); the new part is the measured rate, s(ε), and when to fire the repack. Register OC#50 is refined, not contradicted: galaxy-scale T_x ≈ centuries agrees with "there will always be a point".

5. **Goal fit.** Board: "fitting 10⁹ in 8 GB … decided by distinctions created per game-second." PRINCIPLES 6: "Store the generator, not the generated… influences below one quantum accumulate" — now measured (82% of scars). PRINCIPLES 3 ("Compute only surprises"), 24 ("The memory floor is information": ~3,900× under 88 B/body at R3). Redirects the memory risk to contacts/battles and player news, where the board's attention should be.

**Why not gold:** two of five pre-registered predictions failed, and the quantitative law is measured on a Poisson rate-structure toy (uniform-b impulse kicks, no resonant phase locking, no real conjunction geometry), not the design's encounter+kick path — the same gap that held the 29 Sep premise red-team at silver.

**The one experiment for gold:** wire this accounting into the engine's real path — b-h-live's dashboard on the plane's belt: s(ε) and MB/h against real kicks, a stirring-capable e-coupling, the saturation store at 10⁹ stated against B18 (≤ 2× floor + 2 B), and `alpha_partial` recomputed on the partial regime only.

## What the author missed

- `alpha_partial` in metrics.json is wrong as labeled (includes the ε-saturation plateau); the dossier quotes the right value without saying the stored field disagrees.
- The binding number for m ≥ 10⁻⁸ scatterers is the full-population store at saturation (0.5–2.1 GB at 10⁹ by my probe), not a MB/h rate; it still fits, and it is exactly where rebase quality (bijective program vs histogram entropy) decides — Hj (14.4 bits/body) is a histogram cost, not the 0.126 bits/body program cost, so "repack at unchanged entropy" cannot see bijectivity loss (flagged, but S3b's 15.5 should be read as histogram inflation only).
- MB/h is sub-linear in Γ; the lens self-critique understates the toy's robustness to deliberate contact farming.
- The S7 extrapolation holds Γ=1.1 fixed at 10⁹ bodies; at fixed *surface density* Γ is N-independent (r8), but a same-width belt at 10⁹ would raise Γ ~5× and the saturation store, not the rate, is what answers it.
