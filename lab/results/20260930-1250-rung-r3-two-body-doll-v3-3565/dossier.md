# Rung r3 v3 — two bodies as one doll, handoffs, and a gravity assist

Run `20260930-1250-rung-r3-two-body-doll-v3-3565` (author, GLM lab, cloud container).
Verdict from `lab/verdict.py` on these metrics: **KILL; killed: `eob-doll` (fails `handoff`, exponent 0.2303 > 0.2)**.

## Claim

The effective-one-body reading frozen by the rung — an exact Schwarzschild doll around M = m₁+m₂ with ν entering only through the energy map E_real = M·√(1+2ν(E_eff−1)) — gets the 1PN two-body behaviours right when the doll ingests the 1PN invariants (precession 1024/1024 in the rung's band, period 632/632 judged seeds within 0.1%, ν-effect 500/504 within the oracle's ν-term) and the flybys right (64/64 assists within 1%), but the sphere-of-influence-patched resonant chain does not behave: its heliocentric energy error grows with fitted exponent 0.2303 across the 100 handoffs, above the 0.2 gate.

## Bottleneck

Board #1 (what cells add for many sources) and #2 (stepping owned by cells): the two-body doll closes — ν needs nothing beyond the energy map at 1PN, given invariant-matched ingestion — and the blocker moves entirely to the handoff layer, where SOI patching accumulates model error through repeated resonant encounters. This kills a configuration, not the method (PRINCIPLES #9).

## Evidence

All commands run from `lab/results/20260930-1250-rung-r3-two-body-doll-v3-3565/work/` (pure Python + numpy; ~30 s total):
`python3 binaries.py` · `python3 transfer.py` (~25 s) · `python3 assists.py` · `python3 assists_conv.py` · `python3 make_metrics.py` · `python3 make_picture.py`; then `python3 lab/verdict.py lab/rungs/r3-two-body-doll-v3.md ../metrics.json`.

- **Binaries** (1024 seeds, `random.Random(20261002)`, draws p, e, ν per seed in that order, then the 64 assist b's): precession 1.0000 (worst seed uses 0.83 of the (0.01+16/p) band, at p = 100); period 1.0000 over the 632 judged seeds (worst 4.9×10⁻⁴); ν-effect 0.99206 = 500/504 (needs ≥ 0.99); the 4 misses are all p ≤ 211, e ≤ 0.25, where the oracle's own ν-term passes through zero (|ΔT/T| ∼ 10⁻⁶–10⁻⁵) and the map's absolute miss (2×10⁻⁷–2×10⁻⁶) exceeds 10% of a nearly-zero effect. `min_judged_seeds` = 504.
- **Truncation rule** (author's, from "the relative size of the next post-Newtonian term"): period 5/a² (the integrator's own B11 precedent), ν-term 5/a relative to the ν-term (the ν-term is itself a 1PN correction; the same 5/a² of the period). Both give: judged iff a = p/(1−e²) ≥ 100.
- **Handoffs** (transfer.json): a 2:1 interior resonant chain (a_s = 2^(−2/3), apoapsis 1.0044 AU, started at apoapsis 0.004 rad behind the planet; working point found by a reference-only capture scan, `transfer_design.py`), 100 handoffs in exactly 50 planet periods (t = 313.99). Energy error |E_law − E_ref| at the law's handoff times: 2.4×10⁻⁶ → 7.7×10⁻⁴; OLS slope of log err on log k over all 100 handoffs = 0.2303. Reference: adaptive RK4 (h = min(3.75×10⁻⁴, τ_enc/500)), half-step rerun agrees to 8.2×10⁻¹¹.
- **Assists** (assists.json): 64/64 within 1% (worst 0.85% at b = 44.6 planet radii); the error grows ∝ b² exactly as the patched model's neglected stellar tide across the SOI predicts, so the top of the rung's b-range sits at the 1% edge. Reference half-step agreement 2.0×10⁻¹¹. `reference_converged` = 1.
- **Cost**: events per binary radial period = 28.36 (median band crossings, m = 16 dyadic bands, B9's ≤ 64 at e = 0.6; zero handoffs and kicks in the binary case).

## Implementation decisions the checker needs

1. **Ingestion is invariant-matched**: each seed (p, e, ν) → 1PN invariants (H, J) via `eih_invariants` (ported verbatim), then the doll solves its own Darwin (p_eff, e_eff) from (E_eff, J) with `schwarzschild_from_invariants` (also ported). B11 says the binaries are "given their 1PN invariants", and that function's own comment: "Matching invariants avoids equating harmonic and Schwarzschild radial coordinates." Ingesting raw (p, e) instead fails the period criterion at 87% — that coordinate mismatch is real physics, not a bug.
2. **Energy map, exactly inverted**: E_real = M(1+νH) ⇒ E_eff = 1 + H + (ν/2)H², L_eff = J. All frequencies rescale by the map's derivative, so T_law = T_eff·√(1+2ν(E_eff−1)) = T_eff·(1+νH) identically; the orbit shape and precession are ν-independent, as the config freezes.
3. **Assist Δv is planet-comoving**: (v_ship − v_planet)|exit − (v_ship − v_planet)|entry, each configuration using its own planet ephemeris. The raw heliocentric difference is not usable: it mixes in ~24% of star-curvature common mode (the ship's path bends at 0.86 rad/yr where the planet's frame rotates at 1), which no patched law could match.
4. **The planet's GR content is ~10⁻⁹** of these experiments (GM/rc² with c ≈ 10⁴ velocity units), so the dolls' Schwarzschild geodesics are the Kepler conics to far below tolerance there; `test-mass` and `newton-doll` therefore share the same measured handoff/assist runs and differ only in the binary metrics. The oracle's `handoff_energy_growth_exponent` is 0 by definition (the reference performs no handoffs), and its `events_per_orbit` is 0 (no event machinery).
5. The law's handoff re-expresses the state exactly at |r_ship − r_planet| = R_SOI (bisection to machine precision) into the new doll's frame; the planet's position is derived from its star-doll tube (exact circle), never stepped. Two author bugs were found and fixed during the run (entry-handoff frame mix-up; doll-anchor converting to heliocentric inside the planet doll) — the scripts as committed are the fixed versions.

## Predictions

`predictions.md` was **not** written before the decisive experiments — the author's process fault, recorded here rather than papered over. The checker should treat reproduction as the only evidence; nothing here was held out.

## What would make it wrong, cost of adopting, fit

The ν result is one oracle's own 1PN construction judged against itself at finite p; if `eih_invariants`/`damour_deruelle` mis-port, everything moves (they were cross-checked against the file's own independent series to O(1/p), and the exact Schwarzschild quadratures against the file's Binet ODE to 10⁻¹⁴). The handoff number is chain-specific: this working point's mild chaos (the reference's own amplification is ~8×10⁸ over 50 encounters) multiplies the per-handoff model error, so the 0.23 exponent measures model error × chaos; a more regular chain could sit below 0.2 — the metric, not the mechanism, is on trial. Adoption cost of the binary side is low: invariant-matched ingestion plus one square root per doll. PRINCIPLES: "a failed experiment kills that configuration, never the method" (#9); "compute only surprises" (#3) — the ν-map closing deletes any ν-carrying cell machinery at 1PN; "errors never compound" (#13) is exactly what the handoff exponent caught.

## The lens

Directed rung, no lens chosen. What the author may have missed: the transfer working point came from a short capture scan (reference only) — a wider scan might find a calmer chain; the four ν misses sit where the oracle's ν-term vanishes, so a rung that detunes away from the zero-crossing (as the taste log already advises for commensurability) would measure the map's real 3–5% agreement instead; and the assist Δv had to be defined planet-comoving to be measurable at all — the rung's words "heliocentric Δv" do not say which frame, and the raw reading is unpassable by construction.
