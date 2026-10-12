# Dossier — 20261012-0616-second-20261012-0358-scout-cdac-07b4 (second author on 20261012-0358-scout-cdac)

## Claim (one sentence)

The scout's live-memory law **survives real conjunction geometry, and real geometry is 3–9× safer per kick than the toy claimed**: on a real Kepler belt with true-conjunction kicks (Gauss-mapped, recurring, natively stirring), escape at the player floor needs a median 158–420 sub-quantum kicks (98–100% multi-kick), s(ε) obeys α = 0.76–0.96 on the partial regime, MB/h at 10⁹ and fixed surface density is 1.3–9.1, and the saturated belt store — the binding number at 10⁹ — is 1.7–2.4 bytes per live body, inside B18 (≤ 2× floor + 2 B) and inside the 4.29 GB live budget; the toy's `alpha_partial` field is corrected to −0.817.

## Bottleneck

The checker's named experiment, item by item: s(ε) and MB/h against real kicks; a stirring-capable e-coupling; the saturation store at 10⁹ stated against B18; `alpha_partial` on the partial regime only. Board: "fitting 10⁹ in 8 GB … decided by distinctions created per game-second". This closes the "rate-structure toy, not the design's encounter+kick path" gap that held the scout run at silver.

## Evidence (reproduce: `python3 work/hlive_real.py` ~193 s, then `python3 work/analyze.py` ~40 s; <0.5 GB; load1≈0.8/8 vCPU shared)

Real belt per `crates/encounters`' generator (a ~ U, Rayleigh e, uniform angles, GM=1), real Kepler propagation, conjunctions = every local minimum of pair distance below 0.06 (truth.rs semantics: pair tracked in the zone, kick at each r·v sign flip, minimum refined by parabola and re-evaluated analytically at t*), impulse dv = 2m/(b·v_rel) along the separation, both bodies, (δa, δe) by Gauss's equations at the true anomaly. Accounting identical to the scout (same cells, same R1/R2/R3, same entropies), replayed per ε over the recorded kick stream. Six configs (m ∈ {1e-10, 1e-8, 1e-6}, Σ ∈ {1e4, 3e4, 9e4}/AU, two seeds), N = 500–1500, 10–20 orbits. All in `work/metrics-real.json` + `work/analysis.json`.

- **Real rate:** K = 19.7–65.3 kicks/body/orbit (scales with N at fixed width: 19.7→59.5 for N 500→1500). The toy's Γ=1.1 anchor is 18–60× low at belt surface densities.
- **Matched-rate comparison (the decisive row):** at m=1e-10, ε=1e-3, K=59.5, real s_part = 2.56e-4 vs the toy replayed at the same rate 7.14e-4 — **2.8× safer**; at ε=1e-2, 8.7× safer. Direction uniformly safe. Mechanism (measured): a synodic-conjunction kick is mostly radial, and Gauss suppresses δa by e·sin f (~30× at e=0.07) — the toy's random-sign full-magnitude da manufactured an a-channel that real geometry does not have; escapes ride e and the deep tail (ρ_b(0) = 27/AU, 2.7× fatter than the toy's uniform, still not enough to compensate).
- **Accumulation is the whole story at belt mass:** median kicks before escape 158–420 at m=1e-10 (98–100% of escapers needed ≥2 kicks; the toy: 82%); zero single kicks reach a quarter cell at ε=1e-3 in 446k kicks. At m=1e-6 the channel flips: median 1 kick, 90% single-kick. PRINCIPLES 6 ("influences below one quantum accumulate"), now measured on the real path.
- **Concentration is real and large:** 48–93% of kicks are repeat-pair, per-body kick dispersion 8–21× Poisson — the toy's independence is false — yet escapes are *fewer* (recurrence recycles already-scarred bodies).
- **α (partial regime only, D/N < 0.5):** −0.96, −0.76, −0.94, −0.84 across configs. Toy corrected from its own stored rows: **−0.817** (the stored `alpha_partial` −0.418 included the saturated plateau; m ≥ 1e-8 has no partial regime — None, saturated).
- **Inflow exponent (wide window, D < 0.3N, snapshot-based):** 0.65–0.79, sub-linear as claimed.
- **Native stirring (the toy's failed P5):** σ_e 0.0708→0.0708 at m=1e-10 (no runaway), →0.0719 at m=1e-8, **×2.03 at m=1e-6** (real viscous stirring; K drops 59→41/orbit as the belt puffs).
- **Saturation:** m=1e-8 saturates at every ε ≥ 1e-5 within 20 orbits (D/N = 0.998); m=1e-6 instantly (D/N = 1.0). A 10⁹-body belt at real widths sits far above these surface densities: the store, not the rate, answers.
- **B18 at 10⁹:** store = Elias–Fano map + delta entropy = **1.69 B/live-body** (m=1e-8, H_Δ=11.6 b) to **2.39 B** (m=1e-6, H_Δ=17.2 b) vs floors 1.30 (histogram) and 1.46–2.16 (program 0.126 b + H_Δ): ≤ 2× floor + 2 B holds at both floors; **1.7–2.4 GB at 10⁹ vs the 4.29 GB live budget**.
- **10⁹ fixed-Σ rate line (below saturation):** 1.3 MB/h (Σ=1e4), 2.8 (3e4), 3.9 (9e4) at m=1e-10, ε=1e-3; 9.1 at m=1e-8 — inside the scout's 0.44–17.8 envelope.
- **Controls:** Γ=0 → exactly 0 live bits (passes); the toy at matched rate is the negative control and loses by 2.8–8.7× on the safe side. Determinism: every rerun bit-identical.

## Predictions (predictions.md, written before the decisive run)

7/7 held, two with caveats: P1 held at the player floor (2.8× ≤ 3, safe side) and was exceeded at coarse ε (8.7×, safe side); P3's band [0.6, 1.05] was written against the toy's narrow fit window — the corrected wide-window exponents (0.65–0.79) sit inside it, and my first narrow-window numbers (0.27–0.55) were a replay bug (below), not dynamics. P2 (α 0.76–0.96 ∈ [0.4, 1.6]), P4 (repeat ≥ 0.05 → measured 0.48–0.93; dispersion > 1.2 → 8–21), P5 (×2.03 at m=1e-6 ≥ 1.5; no runaway at 1e-10), P6 (B18 holds, ≤ 4.29 GB), P7 (≤ 50 MB/h → 1.3–9.1) all held.

## What would make it wrong

The kick is the impulse approximation (capped at 0.5·v_rel; gravitational focusing negligible at these masses: 2m/v_rel² ≪ b); b_det = 0.06 truncates the sub-quantum background (~15% RMS undercount, second-order for tail-driven escapes); N ≤ 1500 with fixed-Σ extrapolation to 10⁹ (the checker extended the toy to 10⁶; I did not — the N-scaling of K and s is measured, not the store at 10⁶); two dimensions (no inclination); one star. The final wiring — b-h-live's dashboard on the plane's belt — is still not on `main` (B18b's wired belt is queued for Sol/Astra); until it runs, "real path" means real conjunction geometry at research-crate fidelity, not the engine's shipped belt. Strong scattering (m ≥ 1e-6) saturates so fast that the store number there is a ceiling, not a prediction of the m=1e-10 delta entropy at 10⁹-scale saturation.

## Cost of adoption, fit with PRINCIPLES

No engine change: numbers and one corrected field for b-h-live/B18/shipmem. The law's magnitudes shift (K in tens per orbit at belt Σ, not 1.1; saturation from m=1e-8 up) but every shift is safe-direction. Fits PRINCIPLES 6 ("influences below one quantum accumulate" — median 158–420 kicks to escape, 100% multi-kick at belt mass), 3 (memory follows surprises), 24 (the floor is information: 1.7–2.4 B/live-body at saturation vs 88 naive), 12 (the escape stream is bursty per body but tiny in aggregate — no frame-spike risk at these rates).

## Reproduction note (a bug I found and fixed in my own first pass)

My first replay computed D(t) by a global time search over a per-body-grouped kick stream — invalid (records sorted by body, then time), producing blocky bogus intermediate curves (e.g. 17→255 in one orbit). Caught by cross-checking against live orbit-boundary snapshots; final-cell accounting (D, s, entropies, stores) was never affected (295 = 295 bit-identical before/after), and the shipped `hlive_real.py` computes D(t) from snapshots. The earlier inflated "burst" reading was my error, not the dynamics.

## The lens

Second-author lens: it confirms the run it re-examines, which is exactly the failure mode "agreement is not independence" warns about — mitigated here by attacking with a different generator (real Kepler geometry vs Poisson rate structure), a matched-rate negative control the original lacked, and one prediction (P3) initially failing on a bug I introduced myself. What this lens may miss: the engine's actual scheduler behaviour under bursty scar inflow, and whether the plane's belt (once wired) reproduces ρ_b(0) — the small-b tail density is the one quantity the whole escape rate hangs on.
