Working...
Check complete. `check.md` written to the run folder — grade: **lead**.

**What I did:**

1. **Reproduced** — ran `falsifier.py` in a clean copy: every number matches `metrics.json` bit for bit (light m16 −0.02%…−0.88% toward the ring; r=7 +9.60%, r=8 −6.13%; 4/4 plunge agreement). Re-derived the key numbers with independent code (fresh RK4, different launch convention): shared points match exactly, and the m16 value at r=7 equals the single-band closed form 2π/√(1−6·2^−2.78125) = 17.6167 (dossier's printed exponent is a typo; value correct). My sweep **extends** the wound: exactly-circular m16 fails even at the sampler's own edge (−3.01% at p=10) and reaches −22% at p=6.2; eccentric strong-field orbits cancel, confirming the mechanism.

2. **Attacked where it decides the grade:**
   - The wound is measured on r1's frozen band rule, but the **live law retired that mechanism for this exact error class** (H0207: "viewer found near-circular precession 1–7% off"; law.md records the replacement). I ran the live law's committed independent test: `cargo test -p emergent-space --test near_circular` → 5 passed, worst advance error **6e-10** at p=7..8192 near-circular, 6e-8 within 1e-3 of the separatrix. The "wrong rosette" doesn't exist in the shipped law.
   - "No gate samples the strong field" is contradicted by **B19** (`rotating.rs`): cycles from 1.1× the separatrix, light from 1.05·b_c — exactly the regimes claimed unsampled. True residue: G1/G3 stop at 10 (code-verified), and the Schwarzschild law doesn't yet answer `kerr`.
   - The "held out for the checker" cases are all inside the author's own decisive `metrics.json`; the pre-registered attack (P2/P3) failed; the b=100/b=30 anchors are correct (I regenerate them to 6 decimals) but unprintable from the shipped script.

3. **Salvage recorded** for the integrator: pre-freeze sampler notes for r1/G1–G3, a stale Binet-cells paragraph in representation.md §1, and the genuinely new positive result (band-rule light deflection holds to 0.1% at 1.05·b_crit).
