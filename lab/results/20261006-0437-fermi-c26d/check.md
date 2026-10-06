Grade: silver

**Abstract.** Claim: a belt's live memory floor is not the born program's 0.126 bits/body but a heating trajectory — ~92 bits/body by 10 Gyr at (2e16 kg, 1e9/belt), with the phase column alone pinning ~20 bits within ~1.3e4 orbits for any belt massive enough to exist; an identity-reassigning repack every ≤1.2e4 orbits holds it, and collisions (2.5e5/body at that corner vs 1.0 tame) forbid a middle. Reproduced bit-identically (heat.json md5 equal, 1.4 s, controls pass); seeds, sample size, Coulomb log and an exact scattering reduction of κ agree. Held-out predictions 4/7, misses disclosed. Gain: B18's newborn floor under-certifies 160–730×; shipmem lacks identity reassignment (verified in code). Silver: the 11.5-GB headline sits at a corner whose own collision count destroys the identities the number is computed for.

**Reasons.**

*Reproduction.* `cd <run> && python3 work/belt_heat.py` from a clean copy: stdout diff-identical to `work/run4.txt`, `heat.json` md5 `79fe98bb…` unchanged; 1.4 s, negligible memory. `patch.diff` is empty (no tree edits). Controls behave: κ=0 → 0.0 bits (instrument sanity, the bug run1 documents and v2 fixes); 10×κ → 80.5 vs 62.8 bits at 1e6. `predictions.md` (04:45:06) predates run1–run4 (04:47–04:51), so the predictions were held out.

*Predictions.* 4 held (saturation window, ceiling, 48-bit crossing, allocator rate), 3 missed (κ 2.9e-3 vs [2e-4,2e-3]; bits 62.8 vs [8,40] at 1e6 and 88.5 vs [30,75] at 1e9; coherence ratio ~1.0 vs [0.5,0.9]). All misses disclosed and in the direction that strengthens the memory conclusion; the pre-registered kill criterion (κ > 100× band) not triggered. Gold requires the predictions to have held; they did not.

*Independent checks (mine).*
- κ formula: importance-sampled paired hyperbolic scattering reduces exactly to the code's `kappa_of` (zero-variance estimator, identity to machine precision); λ = 1.65e7 kicks/orbit (CLT valid); largest single kick 0.057 m/s vs 146 m/s cumulative at horizon (no heavy tails); gravitational focusing at contact (v_esc/v)² ≈ 3e-5, negligible.
- Robustness: seeds 7/13/101/202 → 92.1–92.2 bits, crossing 1.23e4; NB 32768 identical; b_max 1e9…4.5e10 → κ ±10% → ±0.5 bits.
- Arithmetic: n = 2.24e-25/m³, v_rel = 1884 m/s, T_orb = 3.95 yr, the four sweep corners' collision counts, the 1.6e8-kg tame threshold (= 24.6-m radius, exactly the ≤1-collision corner), 92.19 bits × 1e9/8 = 11.52 GB — all re-derived and confirmed.
- Adoption targets exist as claimed: B18 reads "≤ 2× the measured information floor + 2 bytes"; `crates/shipmem` shelf.rs states "identity is provenance" and `compact`'s repack folds scars into fresh blocks without reassigning ordinals, so uniform phase entropy is indeed never reabsorbed.

*The core weakness.* The headline corner (2e16 kg, 1e9/belt) has 2.5e5 collisions/body over the horizon: the belt the 92-bit number is computed for cannot keep the identities the number assumes. The universal, collision-independent result is the phase floor (19.9 bits = 2.49 GB — *inside* the 6 GB share) plus the dichotomy; "over the ~6 GB engine share" belongs to a belt that grinds. The claim sentence does state the fork, but the breach framing overreaches the physics.

*Novelty.* The gold components-98bc measured the born program (0.126 bits/body); H02xx's shipmem defines program-plus-scars; nothing in HISTORY or docs measures the aged/heated floor, a repack cadence, or the collision squeeze. New question on a live focus item.

*Goal fit.* Directly the board's "fitting 1e9 in 8 GB … decided by distinctions created per game-second". Fits PRINCIPLES 24 (floor is information-theoretic — and moves with time) and 6 ("influences below one quantum accumulate" — the sub-quantum walk is the scar).

**The one experiment for gold.** Measure the aged floor on the belt the game can actually have: the collision-tame corner (m ≤ 1.6e8 kg at 1e9/belt) with real dynamics — direct paired scattering without CLT, mergers/removals, plus the unprobed channels (parent tide, mean-motion resonances) and m-meso strong-encounter scars. If that floor is phase-only ≈20 bits, the B18 clause and the repack cadence are gold with no self-inconsistent corner behind the headline.

**What the author missed.**
- The 92-bit/11.5-GB corner is self-inconsistent under its own collision count; the adoptable content is the phase floor + dichotomy + repack, not the breach.
- "Every belt with bodies larger than ~10 m reaches the phase floor" overstates: pinning by the horizon needs κ ≈ 4e-11, i.e. ≳25–30-m bodies at 1e9/belt (10-m bodies reach ~16 bits); the stated κ threshold 1.5e-10 is ~4× conservative.
- "A long play session at 100×" for 49 kyr is 490 wall-years; the result binds persistent/aged universes or ≳1e5× compression, not a session.
- The stated phase-walk constant σ_M ≈ 5.4e-6·T^1.5 is ~5× the measured ~1.1e-6 (conclusion unaffected; saturation is measured directly).
- Kick directions are isotropic in the toy but ⊥ v_rel in reality — column split shifts, total does not (untested).
- The tame corner's 20 bits is a lower bound: resonance/tide channels (acknowledged unprobed) would add element scars there, possibly collapsing the "scenery" arm of the dichotomy.
- Repack cost is asserted "idle-time work" without a bytes/second estimate, though the allocator line implies it is negligible.
