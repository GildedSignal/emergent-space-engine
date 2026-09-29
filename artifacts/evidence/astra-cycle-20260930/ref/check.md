# Check of rung r1 (rings), run 20260929-1857-rung-r1-rings-cae4

**Abstract.** The author delivered scripts but no run: `metrics.json`, `dossier.md`, `predictions.md`, the picture and `run.log` are all absent; `author-final.md` reads "Deadline exceeded". Reproduction had to fix two startup crashes (`oracle.bound_constants` used `math.sqrt` on numpy arrays — the author's own cached `.pyc` shows the same code, so its session crashed identically — and a `NameError` on dead code in `square_config`). After fixes, `verdict.py` on my `metrics-check.json`: **binet-m16 and binet-m32 pass every criterion** (m16: prec 0.996, period 0.996, defl 1.0, capture 0/10, isco 1, shape 1.0, repeat 1.0, 38 crossings/cycle; m32 perfect, 77 crossings). Killed: binet-m8 (period 0.957, strict precession 0.984), river-m16/m32 (precession, prograde, period, deflection all ~0), square and tiltonly fail as required. Binet rings deliver correct orbits at ~38 events/radial-cycle — ~10–20× fewer events than the 350–700 fixed steps the board cites — at m=16.

## Reasons

### 1. Reproduction and what differs from the author's scripts

Author's script cannot run as delivered; fixes applied to a copy (`/tmp/r1check`, author folder untouched):
- `oracle.py:123-124` `math.sqrt` → numpy `sqrt` (called with arrays from `bound_EL`); the bytecode cached at run time (`__pycache__/oracle.cpython-311.pyc`, 28 min before my session) contains the identical `math.sqrt`, so this crash is what the author hit.
- `rung.py:753` `square_init(r_, L_ / r_ * 0 + pt_ / 1.0)` references undefined `L_` (dead term, algebraically `pt_`).

Numbers that differ between the author's script and `metrics-check.json`, all documented, none silent:
- **`capture_misclassified`**: the author's binet and river drivers run the photon-capture cases with `light=False`, i.e. as massive E=1 particles with L=b (the `lightc` array is built and never used), giving 2 misclassified each. Under the rung's light model (`light=True`) the photon cases classify correctly **[1,1,0,0]** for every ring config; the massive cases [1,1,1,0,0,0] are correct in the author's path too. Corrected value: 0 for all five ring configs. (The author's `square` used `light=True` correctly; its 6 misses are real.)
- **`precession_pass_fraction`**: the author's `assemble` tests |full periapsis-to-periapsis angle − (Δφ_GR+2π)| ≤ 1% of the full angle, but the frozen rung defines Δφ as the advance and 1% of the advance. At p≥100 the advance is ≪2π, so the author's gate is far weaker. Strict values: binet-m8 0.996→**0.984375** (fails <0.99), binet-m16 1.0→**0.99609375**, binet-m32 1.0→**1.0**. Only binet-m8's pass/fail flips.
- **`crossings_per_cycle` (river)**: `river_run` never increments `nc_c`, so the author prints 0.0. With counting restored the true median is 1.0 — itself diagnostic: the median orbit is caged inside one ring (see §3).
- **`isco_correct`**: the author's `ncyc=2` deactivates the ISCO lanes after ~2 radial cycles, long before the required 100/50 orbits of φ. I re-ran with `ncyc=400` so `phi_max` governs: binet m8/m16/m32 all still correct (r=7 bound through φ=628–630; r=5.5 plunges at φ≈9); river still fails (no plunge within 50 orbits). Values unchanged.
- **square/tiltonly**: the author's runs never terminate (lanes that never absorb, escape or complete a cycle; the square `stall` path crawls at ~1e-15-sized steps; `max_iter` 4M–30M ⇒ hours). Metrics computed with the author's own functions and cases, only `max_iter` capped (short 120k, long 200k, single 60k; caps documented in `/tmp/r1check/capped.py`). Lanes cut by the cap count as fail, matching `assemble`'s `isfinite` semantics. Both negatives fail 8 of 9 criteria regardless of cap.

Runtime (4 vCPU container): binet-m8 146 s, binet-m16 271 s, binet-m32 514 s, river-m16/m32 ~5 s, square-capped 193 s, tiltonly-capped 66 s.

### 2. Oracle check (the rung's "checker verifies each ported value")

Port is line-faithful to `xtask/src/gr_oracle.rs` and `gr_oracle_extended.rs` (`ellip_k`, `ellip_k_minus_half_pi`, `periapsis_elliptic`, `gauss_legendre`, `deflection_quadrature`, `null_turning_radius`, `bound_constants`, `bound_period_quad`, `integrate_gl`). Numerically: author's RK4 agrees with the elliptic advance to 1e-11–1e-12 from p=7.9 to p=1000 (strong and weak field); my independent adaptive RKF45 converges onto the ported values as tolerance drops (my residual error, not the port's); deflection quadrature at b=1000 differs from the 2nd-order series by 4.2e-8 absolute = the known next term 128/(3b³) = 4.27e-8; `ellip_k(0.5)` = 1.8540746773013717; GL weights sum to 2; `light_tail` flat limit = asin(b·u_s) exactly. Sampler reproduced independently from the rung text: identical 256 bound + 64 light seeds, constraint p ≥ 6.5+2e holds, long-run seeds are the first 32 drawn.

### 3. Why river dies (mechanism), and adversarial cases

Ring probe, seed 0 (p=84.25, e=0.441, peri r=58.45): at the first ring edge r=58.688 the continuum A² is +5.8e-5 but the frozen-β model gives −6.9e-4 ⇒ the rung's own rule ("no real root means reflection") reflects the orbit at r≈58.7 against a true apoapsis of 150.8. Every metric at 0.0 follows from this cage: it is the model/configuration that dies, not the method.

Adversarial cases of my own: (i) circular e=0, p=20 — advance error 0.6–2% depending on where u falls inside its band, no clean m-convergence: the band-quantization error does not average out for fixed-radius orbits, which explains the strict-precession failing tail near e≈0; (ii) e=0.9, p=12 (outside the seed range) — advance −3.7e-4 relative, peri/apo repeat to machine zero over 20 cycles; (iii) light near the critical impact parameter — b=3,4 absorbed; b/3√3=1.000 escapes with deflection 8.58 rad, monotone to b=6; (iv) m=1 extreme coarsening still integrates (−1.6e-2 advance error).

### 4. Novelty and goal fit

Directed rung, frozen before any run; no prior H entry tests this cell model (related: H0194 made exact geodesics the oracle; the board's bottleneck 2 cites 350–700 fixed steps per orbit). Result moves bottleneck 2: binet-m16 holds every behaviour gate at ~38 events per radial cycle, ~10–20× fewer than the fixed-step control, and `cycle_repeat_fraction` 1.0 at 1e-12 over 10⁴ cycles is the "one radial cycle repeats exactly" property the rung asked for. It respects "Compute only surprises" and "It's a game" (behaviour gates, oracle independent). The square negative failing while binet-m16 passes also confirms the rung's discrimination: the win is rings following the rotational symmetry, not cell quantization per se.

### 5. What the author missed

Everything past the code: no metrics, dossier, predictions or picture; two startup crashes; three metric-implementation deviations from the frozen text (photon capture model, precession tolerance, river crossing count) plus the ISCO early stop; and no discovery that square/tiltonly never terminate. The script itself, once fixed, is a clean and fast harness — the next author should reuse it, add the three fixes, and give square/tiltonly an iteration budget or a proper termination condition.
