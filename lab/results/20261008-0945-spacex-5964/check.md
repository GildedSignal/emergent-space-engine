Grade: silver

**Abstract.** Claim: the scar's grid, not body count, decides H_live. Reproduced bit-for-bit (validate, main, summarize; 152 s; 11.5 GB peak — over the 2 GB window rule). The MC's dynamics are accurate: converted to true orbits (n = a⁻¹·⁵ rad per time unit ⇒ one orbit = 2π/n̄ = 8.56 time units) it gives 4.5×10⁻² encounters/body/orbit against the repo's frozen truth 3.96×10⁻² at the identical scene (1.13×). But every printed absolute is wrong: rates 8.56× low (36× after a spurious ÷4.2), "100 orbits" is 11.7 real orbits, creation MB/game-h 11.7× high and internally inconsistent ×100, Elias lengths short. The decision survives: cert-grid scars ≈5–10 bits/body at true 100 orbits (fits, ~7–10× slack — not 40–600×), doll-grid 16–20⁺ bits (25–31%⁺ of the whole budget), ship fleets exactly 0. Adoption cost small: the scar layer's exponent from the population.

## Reproduction

- Clean tree, `work/patch.diff` empty (no code outside the run folder).
- `python3 h_live_probe.py validate` → `1.25e-3`, exact.
- `python3 h_live_probe.py main` → `h_live_results.json` **bit-for-bit identical** to the author's (seeded). 152 s wall (claim "≤160 s" honest). **Max RSS 11.5 GB** — the window's rule is 2 GB per process; it survived only because the machine had headroom. A busier window kills reproduction mid-run.
- `summarize.py` reproduces the dossier's table exactly, including its bug (below).
- `predictions.md` (09:52) predates the probe's last edit (10:06) and the results (10:09); the `__pycache__` header records the same source mtime and size as the shipped `h_live_probe.py` — the shipped script is what ran. Pre-registration genuine.

## The central defect: time units (×8.56)

Both sims advance M = M₀ + n·t with n = a⁻¹·⁵ **rad per time unit**, so one orbit = 2π/n time units; for a ~ U[1,1.5], one orbit = 8.56 time units. The repo states the convention explicitly: `crates/encounters/src/kepler.rs` ("Time unit: n = 1 at a = 1"), `belt.rs` ("Horizon in orbits of a = 1 (2 pi time units each)"), `main.rs` (`t_end = orbits * TAU`). The author's Torb=100 is **11.68 real orbits** (Torb=8 in `validate`: 0.935).

Consequence, against frozen repo truth at the author's *exact* scene (`artifacts/evidence/opus-encounters-20260930/scale.jsonl`, n=10⁴, σ_e=0.01, ρ=1e-4): truth = **3.96e-2 encounters/body/orbit** (constant across N at fixed N·ρ, per the crate's own scaling rows). The author's MC ×8.56 = 4.49e-2 = **1.13× of truth — the MC was accurate all along**. The printed 5.24e-3 is 8.56× low; the ÷4.2-corrected table rates are ~36× low. The "measured ÷4.2 MC correction" calibrated the accurate instrument to the inaccurate one: the direct time-stepper (first-order e, periapsis missing from the azimuth formula, one-close-step counting) sits at 0.27× the frozen truth. The anchor comparison "1.25e-3 vs r8's 2.1e-3, sound within ρ uncertainty" is doubly invalid: wrong units, and r8 v2's belt-0 ρ is a log-U draw in [10⁻⁵,3×10⁻⁴] (~10⁻⁵ implied from the crate's scaling — [INFERENCE]), not the author's 1e-4.

## Downstream bookkeeping errors

1. "bits/body@100orb" are bits at **11.68** orbits. My probe at true 100 orbits (N=2000, same density family; 100 real orbits = 856 time units): cert 1.76 bits, touched 41%, growth visibly sub-linear (saturation, P5's mechanism confirmed); doll 15.8 bits, touched 100%. Scaling kicks to the author's density (~9 kicks/body/100 orbits): cert ≈ **5–10 bits/body** (0.6–1.2 GB at 10⁹, ~7–10× inside the budget — not "40–600×"), doll ≈ **16–20⁺ bits** and still growing (25–31%⁺ of the whole 64-bit/body budget). The cert-vs-doll decision survives; both margins were misstated, in opposite directions.
2. `summarize.py` divides the whole run's bits by one orbit's game-hours (`per_h = b / ORBIT_GAME_H`): creation rates are 11.7× high in true game-time, and inconsistent with the dossier's own GB column by exactly ×100 under its own labels (1.64 MB/game-h × 8766 h = 14.4 GB vs its 0.144 GB). True belt0 cert creation ≈ 0.14 MB/game-h.
3. `elias_delta_bits` returns n + ln − 1; Elias-delta is L + 2M − 2: short by (bit-length of bit-length − 1) per value (1998 of 1999 tested values wrong; δ(2)=4 not 3). Small; biases doll low.
4. P6 was reported "missed by 1.6×" but **holds** on corrected numbers (0.14 ≤ 1 MB/game-h).
5. P1's pre-registered ">10× from the anchor ⇒ VOID" clause fires under correct units (21× from the cited anchor) — but the model is 1.13× from the *correct* matched truth. The instrument was miscalibrated; the physics was not.

## What is solid

- Zero-control exact: ship-mass belts and fleets create **exactly 0** scar bits on both grids, reproduced; the scale physics (Δv ≈ 2μ/(b·v_rel) ~ 10⁻¹⁸–10⁻²¹, sub-quantum on both grids; ~10⁸ encounters per cert quantum) is robust and needs no simulation.
- Fleet proximity 99.8%, contacts (R_c/ρ)² ≈ 5×10⁻¹¹, kick p90 2.7×10⁻⁴ (P2's band) — all check out.
- Premises grounded in law.md, verbatim: the memo key is "quantized E and L, 32 bits"; "Per band, fixed point with one shared exponent"; "Kicks are orbit-averaged on stable orbits". q_doll = 20·2⁻³² is one defensible reading (if the 32 bits are shared E+L it shifts ±4×) — the cert-vs-doll ratio is driven by kick-size ÷ quantum ~300 and is decision-invariant.
- Honest disclosure of the doll "touched" artifact and of the 4.2× gap (though misattributed).
- Novelty: HANDOFF line 70 names H_live "not measured yet"; the gold components-98bc measured the *birth program* (0.126 bits/body), not dynamic scars; no HISTORY entry covers scar rates. First measurement.
- Goal fit: the board's named open question (10⁹ in 8 GB decided by distinctions per game-second). "The memory floor is information-theoretic" (P24) — the doll grid stores bits no certificate reader resolves; "a fix signals the wrong representation" (P19) — the overpay is removed by changing the grid, not compressing harder; "compute only surprises" (P3) — the fleet's zero.

## The one experiment for gold

Re-derive the table in true orbital time: Torb = orbits × 2π/n̄; anchor on the crate's frozen rows at matched (N, σ_e, ρ) (`scale.jsonl`, `verify.jsonl`); drop the ÷4.2; fix `summarize`'s game-time and the Elias length; measure cert/doll bits at true 100 *and* 1000 orbits (steady state past saturation, where the Elias(√n) claim is actually decided). Everything needed is already in the repo; my probe's numbers are a first point. Then the headline margins (7–10× cert slack, doll 25–31%⁺) are the shipped code's own numbers.

## What the author missed

- A matched frozen truth already existed in the repo (`artifacts/evidence/opus-encounters-20260930/`, 30 September) at the author's exact scene; the chosen anchor (r8 v2's belt-0) differs in ρ and was compared across incompatible time units.
- Their MC was the accurate instrument and the direct validator the biased one — the opposite of the dossier's story.
- The 2 GB memory rule (11.5 GB peak in `main`).
- The lens (delete-first, "which stored bits have no reader") found the right question, but the same speed-first lens skipped instrument calibration: one cross-check against the repo's frozen encounter rates would have exposed the 8.56× immediately.
