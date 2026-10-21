Grade: gold

**Abstract.** Claim: `docs/representation.md` L50's work-rule clause ("in a field, E and L change by the work done") is dead, the shipped `thrust.rs` implements the exact map instead, and no rung has ever judged it. Reproduced bit-for-bit (regen identical) and independently in closed forms: letter/exact ΔE = 0.427 at r=6M, η=0.25 (0.510 at 0.05), escape burn over-called 3.04× at 6M; my adversarial cases extend the kill outside the author's domain: 0.19–0.24 at r=3.5–4M, 0.06 in flat space at γ=2.3. Adoption is editorial — amend L50, `thrust.rs` L7, plus `law.md:42` and `plane.md:21` which the author missed; no engine change. Checker corrections folded: the "FW vs compass coincide ~1e-5" claim is an unconverged-lump artifact (they differ ≈13% of ΔE, 10–15% at oblique attitudes), and "the map is the exact FW rocket" holds exactly only prograde.

## Reproduction

- `regen.sh` rerun: output identical to the runner's log, every dossier number. Controls green.
- Independent closed-form verification (fresh code, no author imports, no integration for the one-event cases):
  - Letter ratios reproduce exactly: 0.4269/0.5101 (6M, η=0.25/0.05), 0.7649 (20M), 0.9511 (10⁴M); dL tracks (0.4313/0.5104/0.7754).
  - Escape over-call by hand: exact η_esc = atanh√(2M/r) − atanh√(M/(r−2M)) = 0.1092 at 6M; letter 0.3321 → 3.04×. 1.61× (10M), 1.22× (20M), 1.04× (100M) all confirmed.
  - Radial impulse three readings: axis-boost ΔL = 0 (4e-16), FW ΔL = L₀(cosh η − 1) = +0.1088 = +3.14%. Held-heading arm: axis E = 0.94570, dL/L = −0.1161 (author: same, exact match); compass E = 0.94138, dL/L = −0.1034 (exact match).
  - `thrust_quantum_log2: 6` confirmed in `ctx.rs`; the flush-quantum model is the shipped one.
- Novelty: `grep thrust|burn lab/rungs/` — empty; no rung arm exists. docs/HISTORY.md's "kink" hits are the engine grammar's (KINK) source-exchange, never this clause. The wiki's thrust entries (gravity-news, birth-stagger) are thrusting *sources* and fleet dolls, not the player's E/L kink law. First oracle judgment of the sentence.

## Held-out predictions

Written before the decisive run (file times order correctly; regen overwrote only `run_output.txt`). P3 held decisively (shipped replica 0.0–1.3e-13). P2 held at 6M; the escape-direction miss was honestly disclosed and self-caught by the control (the author's pre-run Fermi used E = f·γ; the textbook identity confirmed √f·γ). P1 partial fail disclosed, kill stronger (flat SR channel). P4 held (3.95× per 4×, honestly reported as first order, not the predicted second). This is the record the grade asks for.

## Attack (my own cases)

1. **Outside the domain — stronger field (r < 6M, unstable circulars):** letter/exact ΔE = 0.237 (r=4M, η=0.05), 0.189 (r=4M, η=0.25), 0.092 (r=3.5M). The kill extends and deepens.
2. **Outside the domain — higher γ (the player's regime; the plane's own burn red is γ≈120):** flat-space ratio 0.059 at w₀=0.9 (γ=2.3), η=0.25. The SR channel the author bounded at 38–48% (w 0.5–0.66) is ~94% at γ 2.3 and worse beyond. The letter is not a weak-field approximation that "becomes fine"; it is wrong everywhere the player actually burns.
3. **Escape-threshold classification (behaviour bar):** at η = η_esc and η = 1.01·η_esc (r=6M), engine lumps at q=2⁻⁶/2⁻⁸ and the continuous law agree on bound/escape at margins |E−1| ≈ 4e-4 (deferral bias ~5e-5). No flip at realistic margins.
4. **The FW-vs-compass "coincidence" (breaks):** the author's claim "the two clause-1-consistent readings coincide to ~1e-5" is an artifact. Continuous FW-nose E = 0.941556 vs continuous compass E = 0.941377 at the author's own radial case — 1.8e-4 apart, ≈13% of |ΔE|. The author's FW arm was a q=2⁻⁸ lumping, which converges to the FW-nose value (q=2⁻¹⁰: 0.941512; q=2⁻¹²: 0.941545 → 0.941556), not to the compass value; at q=2⁻⁸ the deferral error (−1.8e-4) coincidentally cancelled the FW−compass gap (+1.8e-4). At oblique attitudes/longer burns the two readings differ by 10–15% of ΔE (45°, Δτ=5/20; prograde-held-in-Cartesian, Δτ=20). **This strengthens the under-determination thesis** — the sentence fails to pin the map by a player-visible margin, not by 1e-5 — but the dossier sentence as written is wrong.
5. **"The map is the exact FW nose-carried rocket" (overstates):** a single finite lump is not the flow of its own field at oblique attitude, even in flat space: 45° flat, |Δu| = 1.7e-3 at η=0.25, 9.9e-3 at η=0.6 (7 lumps vs one lump differ 5e-3). Exact prograde at any cadence (verified), felt-α identity exact at any attitude (I verified |along|²−s²=1 analytically), so clause 1 holds instantaneously; the finite lump vs its own continuous law is first order in the flush quantum — consistent with the author's own deferral measurement, but "the exact FW rocket" conflates the lump with the flow.
6. **"The shipped thrust.rs is exact" scoping:** the 0.0–1.3e-13 measures the algebra's coordinate round-trip against the direct proper-velocity path of the same map (lossless — verified in closed form). The shipped `cosh_sinh` is a 6th-order Taylor truncation (~4e-10 at η=0.25, negligible at flush quanta but not "exact"), and the integer quantization path is unmeasured (the replica is float). The doc/code divergence claim is unaffected.
7. **Adoption completeness:** the dead sentence lives in four places, not two — `representation.md:50`, `thrust.rs:7`, **and `law.md:42` and `plane.md:21`** (grep). The dossier's cost-of-adopting misses the latter two.

## The page

The author's `wiki/representation-premises.md` folds the result in at the right rank and keeps budget (211 lines ≤ 300; current best 6 ≤ 15). Corrected in place: the FW/compass coincidence line (now the 13%/10–15% numbers, marked checker-corrected), the "exact FW rocket" line (now the lump-vs-flow scoping), "rapidity clause proven exact" → "in the engine's convention", and the amendment list now names all four copies. The Runs section's duplicate lines pre-date this run (inherited from main's page) and are left for the publisher's id-keyed union.

## Goal fit

PRINCIPLES #30: "what really matters is navigation, knowledge and dynamics those need to be perfect" — this is the navigation law's own sentence, never judged. #19: a fix signalling the wrong representation — the work integral destroys the additive form the doll already has (#3's own rule). The run deletes a wrong premise before builders implement it; the engine needs no change. Not a cost row, and does not need to be: the gold path "shows that a premise is wrong" and is adoptable in one step.

## What the author missed

- The sentence's other two copies (`law.md:42`, `plane.md:21`).
- The FW/compass coincidence was a convergence artifact (item 4) — the strongest form of their own under-determination point sat one refinement away.
- The oblique flat-space lump is not its own continuous law (item 5), which the flat prograde-only control could not see.
- The letter's severity at player-realistic γ (item 2): the "38–48%" framing understates a channel that is ~94% at γ 2.3 and heading to total as γ grows.
- The shipped `cosh_sinh` truncation and the unmeasured integer path (scoping, not a defect at flush quanta).
