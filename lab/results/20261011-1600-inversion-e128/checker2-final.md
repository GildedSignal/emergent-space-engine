Working...
Check 2 complete. `check2.md` written; `check.md` never read; tree restored to clean `a838a284` (only untracked `lab/results/`).

**Grade: gold** — with three corrections recorded.

**Reproduced (bit-for-bit):** both dossier commands; `work/l15b.csv` and `work/l5.csv` identical to my reruns (5.4 s total). First-refusal row (t=8450728513, γ 1761.398, `Space(Range)`), loss at t=1.7e10 with 3630 refusals, register exact (|viol| ≤ 6.4e−11, pt → −2⁶³), gate crossing 1.0303 at β 0.247, relativistic work 2.4%, τ = 4.206e9 vs SR's 1.8e9.

**Adversarial (4):**
1. Level 13 — dt/dτ saturates at 2.0000 again, wall same fault at γ 1802.7: structural, not one trajectory.
2. High-precision L5 rerun — the "<1e−6" control claim **fails**: measured 0.59% (probe quadrature-dominated; conclusion — gate PASS — holds). The stored CSV can't even express the claim.
3. Code-level: every `proper_time` reader verified — view clock (`view.rs:262-267`, verbatim the probe's formula), burn flush (`step.rs:273`), events scheduler. Found sharper than the dossier: the HUD's rate dial (`rates_of`, √(f−v_r²/f−v_t²)) is computed exactly from the state, so the ship's own panel shows dτ/dt ≈ 1/1262 while its clock ticks at 1/2 — a 630× internal contradiction.
4. Premise verified from the frozen tests' own text: gate burns capped at 2e−4 c (`throttle.rs:68`); the merge's green test asserts only no-refusal (`throttle.rs:231`).

**Novelty:** HANDOFF:73 lists the γ ≈ 2,000 refusal with no cause; the collapse is nowhere in the docs. **Corrections:** the <1e−6 number, P2's bound (worst 3.83e−3), and the mechanism — `fit_key` uses the exact geodesic energy predicate, so the "E_∞ ≈ 2" inference is doubtful; a first-order-in-v² τ integrand (dτ/dt ≈ 1 − v²/2 → 1/2) fits the constant 2.0000 saturation better. Same fix target, different line to read.
