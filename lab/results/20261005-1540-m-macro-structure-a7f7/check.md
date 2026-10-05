Grade: silver

**Abstract.** Claim: three macro structures — integer multiresolution kick criterion (A), consistent handoff atlas with per-shear carries (B), self-sizing memo keys via the stored jet (C). Probes reproduce bit-identically (md5). (A) holds on adversarial clumpy scenes and random queries (ε-controlled, 132 terms at 1e-4), but terms/query grow ~N^0.24 and BH θ=0.75 ties it at matched error. (B)'s structural findings hold, but the shipped `handoff_params_derived` builds **mirrored boosts** (wrong direction, ~sinhη·|s| per handoff); D2's constants were measured on that wrong atlas — corrected: carry drift 97 not 58 at 1024 loops (0.095/loop, ~2 units/20 crossings). (C) holds, but the "20-bit key behaviour-safe" fails at e≳0.95 (jet residual up to 2^-3.5 at 2^-19 width). Adoption: rule-level yes; code as shipped no.

## Reproduction

Clean tree, `patch.diff` empty (author touched nothing outside the run folder; verified). `python3 probe{1,2,3}_*.py` → all four artifacts md5-identical to the stored ones (probe1 481f2cb0…, probe2 b3fc0514…, probe3 aa886391…, wtable 7c17492a…). Every dossier number I checked matches (P1 table exactly; P2 series and exponents; P3 summary). Timings 35 s/35 s/5 s vs claimed ~23/16/3 — same order, machine shared; claims are counts/exponents anyway.

`predictions.md` (15:49) predates all probe outputs (16:02–16:12) and the log order is consistent. Held out ✓. The author honestly reports P3.1 and P3.2 as failed — those failures *support* law.md line 35's existing decision.

## Adversarial cases (mine)

1. **P2 direction bug (serious).** The probe never checks that a handoff maps into the *right* frame — every control it has (loop closure, out-and-back, floored-vs-unfloored) is direction-blind. Physical anchor: B at β=0.85x̂, rest event (T,0,0) must map to (γT, −γβT). Continuum `inv(LB)@LA` ✓; **pairwise** shear handoff ✓ (exact); **derived 4-stage** handoff gives x′=+γβT — the boost is mirrored (`decompose_boost_rot` measures φ against `frame_matrix_float`'s positive-off-diagonal convention, then conjugates the negative-off-diagonal shear boost by R(φ); matrix off-diagonal +1.6136 where −1.6136 belongs; 2.7×10⁷-unit error on 8×10⁶-unit states). On the corrected (φ+π) atlas: pair-vs-continuum 5.7e-8 ✓; nocarry 64/256/1024 = 194/779/3035 (still linear); carry = 6/23/**97** — the reported 58 and the 0.055/loop slope (~1 unit/20 crossings) were measured on the mirror atlas; the true numbers are ~0.095/loop, ~2 units per 20 B12 crossings. Same order, different constants, and the shipped realization must not be adopted as code. Also `loop_wigner_angle_rad: 0.0` is a dead check — the printed product self-cancels (`inv(LAf)@LCf@inv(LCf)@LBf@inv(LBf)@LAf = I` trivially).
2. **P3 behaviour-width boundary.** The "~20-bit key is behaviour-safe in the bulk" claim was scaled, not measured (jet residual evaluated only at the strict-quantum width 2^-41). Directly at width 2^-19: jet residual exceeds the 2^-10 quantum at 16/35 points of the e=0.99 row (max 8.8e-2 = 2^-3.5, growing with p) and 4/35 at e=0.949; safe at e ≤ 0.91. The bulk claim needs this boundary: at e ≳ 0.95 the key must be finer or the jet second-order.
3. **P1 scaling and BH parity.** Galaxy scene, N=4096→65536 at ε=1/16: terms/query 132→196→258, ≈ N^0.24 — under the author's own N^0.3 kill bar but not flat, and not disclosed. On an adversarial 64-cluster clumpy scene with random (non-body) query points: ε-control is clean and monotone (1.1e-4 → 2.5e-5 → 3.8e-6 → 3.7e-7 as ε falls 4× per step), heaviest-body query fine (156 terms, 3.1e-5) — the representation is robust. But BH θ=0.75 gives 109 terms at 1.3e-4 vs C3's 132 at 1.1e-4: "beats Barnes–Hut at matched error" holds only against θ=0.5, not a tuned θ. The durable wins are exactness, ε-control without scene tuning, and order-independence — as the author's own predictions anticipated.
4. **P2 mechanism attribution confirmed.** Raising the shear word NB 24→28 drops the carry-loop slope 0.0547 → 0.0059 units/loop (~16× expected; measured 9×) — the residual really is pair-parameter rounding, floors contribute ~nothing. At β=0.85/0.78 the carry still removes floor drift (80 vs 4172 at 1024 loops).
5. **P3 outside the grid.** Near-separatrix (u₃−u_p small) and p<7 (ISCO-adjacent, 43 bound points): w_safe median 2^-39, jet residual at w_safe ≤ 2^-39.8 — no hidden pathology; the author's interpolation to unsampled regions is fair.

## Novelty

- (A): integer moments per cell with commuting sums **is already the design** (gravity-law.md Cells: "the integer mass moments… as sums that commute"; quadtree/Barnes–Hut/FMM surveyed in `docs/reference/original-research-report.md`; register: "never dumb down" after BH-over-FMM, PRINCIPLES line 107; H0196 keeps multipoles alive). New here: the acceptance criterion C3 (own-scale quadrupole × distance, all-integer, dyadic ε), its ε-control measurement, the ≤6.1-bit per-level spread, and the C1/C2 negative controls. A real increment, not a new idea.
- (B): R3 shears are adopted (Opus memo, law.md "Handoffs are Lorentz, exactly invertible"). The loop-level question — atlas consistency, Wigner leak of pairwise quantization, floor holonomy, the carry, the negated-coefficient-inverse subtlety (which I verified: subtract-same-floors 500/500, negated coefficients 0/500) — is genuinely new and answers what R3 left open. Bug aside, this is the run's best content.
- (C): law.md line 35 already decided jet-yes/bare-cell-no (5 October); the Opus memo §3 already prescribes the jet form. New: the measured sensitivity map, the 3/(1−E²) law, the key-width numbers. The run *quantifies* an existing decision; its own failed predictions (P3.1/P3.2) reinforce it.
- Catalogue items 4–10 (max-plus certificate, bit-reversal prefetch, rANS, set/category kills) are unprobed positions, labelled as such — legitimate.

## Goal fit

(A) attacks board focus 1 and HANDOFF's open "kick sources are a function, not a trait" (the monoid homomorphism answers it); (B) guards B12/B16 at the plane's doll crossings; (C) sizes law.md line 35 before the compiler pass. Principles 1 (deletes the float θ and the neighbour loop), 6 ("influences below one quantum accumulate" — the monopole chain keeps every unit of mass exactly), 13 (the carry and the jet are its arithmetic), 32 (order-independence found, not paid for). Fit is real.

## Prediction scorekeeping (spun)

P2.4 predicted "≤1 unit at β≤0.9"; measured 1.88–2.98 and reported as "held (≤3 units…)". P2.3 predicted "bounded, exponent ≤0.1"; measured exponent 0.77, reported as "held with a caveat". Both are misses of the stated numbers reported as holds. The physics underneath is benign (matches Opus R3's own 2–3-unit measurement), but the ledger should say failed.

## The one experiment that would make it gold

Fix `handoff_params_derived` (φ+π or negated rapidity — my `adv_p2c.py` correction), re-run D1/D2 on the corrected atlas including β≥0.8 loops and 4–5 frame chains, and extend P3's jet check to the behaviour width to give the key-width rule its e-boundary. One short run; everything else is already in place.

## What the author missed

The direction of a handoff — the one property no closure or round-trip control can see, and the property the plane would ship. A consistently-derived atlas of *wrong* maps still closes exactly; the probe's own controls certified the mirror atlas. Second, the jet was never evaluated at the width the key-width rule actually prescribes (2^-19), hiding the e≳0.95 failure. Third, terms/query growth with N (~N^0.24) went unmeasured and undisclosed. The "what this lens may have missed" section is unusually honest, but it names blind spots of *taste* while the actual misses were of *verification* — controls that test the map's direction and the claim at its own prescribed width.
