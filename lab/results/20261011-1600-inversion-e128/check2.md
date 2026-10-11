# Check 2 — 20261011-1600-inversion-e128 (blind; written without reading check.md)

Grade: gold

## Abstract (for the integrator)

Reproduced bit-for-bit. The merge's green point certifies no physics: above it the tube's proper time — the same `orbit_state` the view's clock, the burn flush and the events Clock read — stops dilating (dt/dτ → 2.0000 while γ → 1761; 3.7× wrong at β 0.999, 112× at the freeze), and the HUD's rate dial, computed exactly from the state, then contradicts the ship's clock by ~630×. The wall is `Error::Range` from the orbit key's k word in the kick's rebind (γ 1761 at L15, 1802 at L13: the known "γ ≈ 2,000" refusal, now with a cause). The frozen work gate crosses 3% at β 0.247. Adopt: re-aim b-high-gamma — raising the wall would optimize clocks wrong by ~γ/2. Cost: none.

## Reproduction

- Clean tree at `a838a284`, `git apply work/patch.diff`, both dossier commands rerun: `work/l15b.csv` and `work/l5.csv` **identical to my outputs, byte for byte** (78 and 140 rows; both commands together 5.4 s).
- Loss line matches: `lost at t=17035876708 (refusals 3630): Some((Kick(0), Space(Range)))`. First-refusal row matches exactly: t=8450728513, γ 1761.398, β 0.999999839, r 7.97e9, 168 refusals. Register: `pt_exp` −64 throughout, |violation| ≤ 6.44e−11, pt → −2⁶³; τ = 4.206e9 at t = 7.742e9 (dossier: 4.21e9; SR affords 1.8e9). Relativistic work vs ΔE_∞: 2.4% (dossier: 2.3%). Gate ratio 1.0303 at β 0.2474, 27.2 at γ 1262, 111.7 at the freeze (dossier: 1.030, 27×, 112).
- Determinism: `l15.csv` vs `l15b.csv` identical on every engine column and on `work_gate`; only `work_rel` differs (the disclosed probe fix — the engine was never edited). predictions.md (mtime 1791735725) predates the decisive l15 run (1791735735); log order consistent.

## Predictions

Written before the decisive run. P2 held (γ_pred tracks the readout across five decades of γ, worst 3.8e−3 — see corrections), P4 held exactly, P5 held, P1's conclusion held with the shape corrected and disclosed. P3 failed exactly along the branch predictions.md pre-registered as a finding ("a refusal before the leave → the wall is a word/register failure after all; the γ at refusal and the fault reason become the finding"). The headline (the collapse) was unpredicted and reported as such — honest.

## Adversarial cases (mine)

1. **Level 13** (second α, 4× slower burn): dt/dτ saturates at 2.0000 again from γ ≈ 400; same fault `Space(Range)`, wall at γ 1802.7 (vs 1761.4 at L15); deficit 3.65 at the merge-green β. The saturation and the wall are structural, not artifacts of one trajectory; the wall's γ varies slightly with the trajectory's angular momentum, as a key-word limit should.
2. **High-precision L5 control** (probe variant at 12-digit output): the dossier's "|work−ΔE|/ΔE < 1e−6" is **not reproduced**: measured |work_gate−ΔE_N|/ΔE_N = 0.59% (and work_rel vs ΔE_∞ = 0.31%), dominated by the probe's own 141-point trapezoid. The stored CSV cannot express the claim at all (6-decimal formatting; both columns print 0.000000). The *conclusion* holds — 0.6% ≪ 3%, the gate's own regime, PASS — but the number looks like the theoretical γ³−1 ≈ 1.7e−7 at β 3.4e−4, not a measurement.
3. **Code-level attack on the interpretation** (is τ really the player's clock?): every reader of `orbit_state().proper_time` checked. `view.rs:262-267` computes `proper_seconds` exactly as the probe does; `step.rs:273-276` (`proper_since`) is the burn flush — so a held burn's rapidity per coordinate tick is α·dτ/dt = α/2 at high γ, not α/γ; `events/clock.rs` schedules dolls on the same map. Sharper than the dossier: the HUD's **rate dial** (`observe.rs rates_of`, √(f − v_r²/f − v_t²), computed from the state, nothing stored) is exact — at γ 1262 the ship's own panel shows dτ/dt ≈ 8e−4 while its clock ticks at 0.5: two player-facing instruments disagree by ~630×.
4. **The premise, from the frozen tests' own text**: `throttle.rs:68-69` caps the work gate's burns at 2e−4 c; the merge's green test (`throttle.rs:231-252`) asserts only β 0.999 reached, no refusal, no loss. "No refusal" indeed certifies no physics there.

## Novelty

`docs/HANDOFF.md:73` lists "flying past γ ≈ 2,000 is refused" as a known limit **without a cause**; the run supplies the cause (the k word of the orbit key in the kick's rebind — `binding.rs fit_key`, where k = 1/(1+e) falls toward 2⁻²⁸ and the 48-bit word's relative error trips the 2⁻²⁰ check → `Error::Range`; the author's "orbit.rs periapsis/k bounds" is right in substance). The dilation collapse appears nowhere in HISTORY.md or the docs; PRINCIPLES.md:105 shows dτ/dt is a shipped HUD reading. Not known, not tried.

## Goal fit

PRINCIPLES 30 — "I want the player to feel what a human would feel in space, it's about immersion": the one instrument of that feeling saturates at ×2. PRINCIPLES 2 — "error type over error size": a silent saturation is the worst type. PRINCIPLES 34 — "the oracles are guards, not shepherds": the gate guards only β < 0.25, and the merge's test guarded nothing above it. It deletes the belief that the register or the word is the wall and re-aims the queued `b-high-gamma` build. Adoptable within one step: it is a measurement; adoption is a decision, not a merge.

## Corrections to the record (do not block the finding)

- The L5 control number is wrong as stated (<1e−6 → 0.59% measured); conclusion unchanged.
- P2's "≤ 3e−3" is exceeded: worst 3.83e−3 (at γ 1.8, no growth with γ — substance holds).
- The [INFERENCE] mechanism is doubtful as phrased. `fit_key` (binding.rs:181-288) uses the **exact** geodesic energy predicate (`den = lapse − kinetic` is literally (dτ/dt)²; "preserves symbolic E=1") — no saturating Newtonian energy map there, and an E_∞ pinned at exactly 2.0000 across γ 400–1800 and two levels is implausible as an energy. The constant 2.0000 fits a clock integrand that carries time dilation only to **first order in v²** (dτ/dt ≈ 1 − v²/2 → 1/2 at v → 1), consistent with the shape tables' first-order-in-q design. Same fix target (the tube's time map), different line to read; the integrator should pin it in the τ quadrature before fixing.

## What the author missed

- The HUD's rate dial is computed independently and exactly (`clocks_with`/`rates_of`) — the ship's own panel contradicting its clock by ~630× is a stronger, more player-visible statement of the bug than "the star's frame runs 2× fast".
- The control number was not regenerable by the shipped probe (formatting and quadrature); a claim the artifact cannot reproduce, in an evidence section.
- The events scheduler (`events/clock.rs`) also reads the saturated map — the known "fast dolls need root-clock event keys" item (HANDOFF:72) may be entangled with this, worth one look when the time map is fixed.
- One scene, one seed, forward burn only (disclosed); the turn keys and a reverse burn at high γ remain unread.
