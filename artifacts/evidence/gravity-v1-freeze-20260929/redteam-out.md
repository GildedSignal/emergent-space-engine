Reading prompt from piped stdin (waiting for EOF; ctrl+c to abort)…
Working...
# Red-team: `docs/gravity-law.md` (es-lattice-gravity-v1, draft H0195)

**Verdict.** The framework is sound and most numbers are right, but the contract does not yet contain its own physics: the kick rule as written integrates the wrong equation (Finding 1), two gates are unexercised or vacuous on their own frozen case sets (Findings 2, 3), and the determinism gate contradicts the step rule (Finding 4). Freeze after fixing those four; the rest is pinning.

Everything below cites `gravity-law.md` by line (L##) and, for case-set facts, `artifacts/evidence/g2-reference-20260928/PROVENANCE.md` (P##).

---

## Rank 1 — the gate outcome would be wrong

### 1. The force law is absent; the literal text has a wrong continuum limit

L37–38: *"Within a step, the body drifts straight in the local sheet. At the step boundary, the change in tilt is applied as an integer velocity kick."* Taken literally (also L19, *"local physics is the lattice's special relativity applied to u"*, and L45), the kick is Δβ and **u is conserved**: du/dT = 0, hence dv/dT = (∇β)·v with β = −Q√(2M/r)·X/r.

Consequences of that limit, both derived, not guessed:

- **No GR-like circular orbits.** ṙ = u_r − Q√(2M/r) has only an *unstable* equilibrium requiring |u_r| = Q√(2M/r) (0.45c outward at r = 10M). GR circular motion has u_r = 0. B2/B3 cannot pass at any η.
- **Light has exactly zero deflection at every b.** u is a constant vector, β→0 at both ends of the scattering orbit, so outgoing v = incoming v. B4's deflection clause fails identically.

The correct river dynamics is not stated anywhere in the contract. From the same metric (L15) the exact per-coordinate-time Lagrangian is −√(Q²−|v−β|²), giving d(γ_u u)/dT = −γ_u(∇β)ᵀu; its parabolic truncation gives the useful cross-check dv/dT = (∇β)β = −MQ²x̂/r²·(1/Q²-scaled) — *exactly Newtonian*, hence zero GR precession. So even the natural "cheap" choice (Newtonian force in river form) passes nothing in B2 (GR precession 6πM/p is precisely the γ_u correction). Only the fully relativistic force law can pass, and the contract never says so; L39 defers *"the integrator and its order, η, the step rule, the rounding recipe and the horizon test"* to Astra's crate text. That defers the discretization — fine — but not the equation being discretized. As frozen, the gates test whatever Astra writes, not this contract, and a literal implementation of the contract fails all of B2–B6.

**Corollary (tolerance vs order).** Steps per orbit at η = 1/64 are 2π/η ≈ 402 (B9's 512 is consistent). A 2nd-order time-symmetric scheme has per-orbit phase error ≈ C·(2π/n)² ≈ (0.3–3)·10⁻⁴ rad (C = O(1) for e ≈ 0, larger at high e). B2's budget at p = 10⁴M is 1%·(6π/10⁴) + 10⁻⁶ ≈ 2·10⁻⁵ rad/orbit — **10–100× below what 2nd order achieves**. B2 therefore silently requires integrator order ≥ 4 (error ~ (2π/n)⁴ ≈ 10⁻⁹). Achievable and cheap, but it must be stated, because it feeds B9: a 4th-order step costs ≥ 3 field evaluations, and B9 counts "events" (L79) without saying whether force evaluations are events.

**Fix.** One sentence: the kick integrates the exact PG geodesic equation (state it), the integrator is time-symmetric of stated order ≥ 4, and Δ(x,k) = Δ(x,−k). The premise probe should be required to test the *contract's literal* tilt-only kick as a negative control — it is the cheapest kill in the whole plan.

### 2. B5 is vacuous on its own frozen case set

L75: *"For E = 1 inward anchors: absorbed iff |L| < 4M, with a ±1% band."* The frozen E = 1 anchors are the conic families: P106–108 — all 120 have |L|/4M − 1 ∈ [8.5·10⁻⁵, 10⁻²], G24edge's 59 have 1.5·10⁻⁶–9.9·10⁻⁶. **Every one lies inside the ±1% exemption band.** The only other E = 1-ish cases are infall from rest (k0 = 0, L = 0). So B5 passes any law that absorbs radial infall, whatever its capture threshold (2M, 3.9M, 4.1M — all pass). A wrong law passes; the gate verdict is wrong. (The threshold value 4M is itself correct GR.) **Fix:** add E = 1 (or certified-E ≈ 1, classified by the judge's exact integer E test, P47) anchors at |L|/4M ≈ 0.5, 0.9, 1.1, 1.5 — the exact-E conic construction targets 4M by design, so this needs a new family or a ball-E relaxation.

### 3. B4's capture clause has no cases

L74: *"capture iff b < 3√3·M, with a ±1% band"*. The case list (L65) supplies "its light anchors" = G2.2's 95 *scattering* anchors (deflection regime) — G2.4 is massive-only (P104–108). No light case straddles b_c = 3√3M on either side of the band. The capture clause is never exercised; a law that never captures light passes B4. (The deflection clause itself is fine: b ≥ 10M excludes the whirl zone 5.2M < b < 10M where deflection is hyper-sensitive and no honest 1% comparison exists.) **Fix:** pin light cases at b/b_c ≈ 0.9, 0.99, 1.01, 1.1 with escape/capture verdicts; R2/R3/R5 already contain absorbed light (164,000 in R2, P127) — curate from there.

### 4. B8 contradicts the step-clip rule

L36: the step is *"clipped to the next cell boundary"*; L7 and B8 (L78) demand outcomes *"independent of … partition"* / *"bit-identical … across different cell partitions."* Subdividing a drift-kick at a cell boundary changes the trajectory at O(Δ²): the kicks sum identically (β(x₁)−β(x₀) is telescoping) but the second half drifts at a different velocity. With clipping, the integer trajectory is a function of the partition; bit-identity across *spatial* partitions is impossible for any drift-kick. Either "partitions" means work assignment (threads/regions — then say so), or steps must not clip. Note that in step 2 the certificate *"never expires"* (L33) and there are no contacts, so cell-crossing events (L41) have no function there at all — deleting them from step-2 scope fixes this cleanly and cells enter with the solved field in step 5.

---

## Rank 2 — ambiguities that could change canonical outcomes

5. **Light state is unrepresentable as specified.** L27: state is *"integer x and k"*; L45: light has |u| = Q. Since v = u + β and β = −Q√(2M/r)·X/r is irrational, v is irrational: integer k cannot hold |u| = Q exactly outside β = 0. Undefined whether k is v or u, what the light carry holds, and whether L45's *"anchor direction"* is the direction of u or v (they differ at finite r₀). Light trajectories are canonical outcomes; this must be pinned.

6. **E and L are never defined in the contract.** L27 carries them, B1 gates them, but the formulas (E = γ(1+β·u), L = γ x×v) exist only in the judge's provenance (P28). Also undefined: the scale (per unit mass? the 2Q² of law v1?), the base of B1's *"relative excursion"* (relative to E ≈ 2Q²γ including rest energy, the 10⁻⁶ bar is nearly automatic; relative to the kinetic/GR part it is very hard), the growth-exponent fit (window, weighting), and the *"long-run cases"* of L65 — the only unfrozen case class named.

7. **B2's p-range excludes the case set's strongest fields.** L72 gates p ∈ [10M, 10⁴M], but G2.2 includes 1,216 near-ISCO (p ≈ 6–8M) and 624 near-separatrix anchors (P100). Those are excluded from precession by B2's own range while B3 (no range) includes them — inconsistent scoping, and precession at the most relativistic radii the cases reach is ungated. State the intent either way.

8. **B9's "orbit" and case set.** If "orbit" = radial period, a correct law *fails*: a margin-10⁻⁴ near-separatrix case at p ≥ 10M whirls ~O(√(p/(p−p_sep))) ≈ 100 azimuthal turns per radial period ⇒ ~4·10⁴ events. If azimuthal, 402 + cell crossings ≤ 512 needs a bound on crossings from the undefined *"density-sized"* cells. Also: do multi-stage force evaluations (Finding 1 corollary) count as events? The 512 and the 2 µs are individually plausible (402 steps, and the 0.1-core gloss checks out at ~0.19 core for 10⁶ ships on a 90-min orbit); the accounting is what's undefined.

9. **Horizon mechanics underdetermined.** L43: *"whose step would reach r ≤ 2M"* — chord test or endpoint test? Absorbed *"at that step's chronon"* — start or end? What happens if a kick would push |u| ≥ Q (possible near |β| → Q)? And the B6 tolerance "within one step" is ~1% of T_h when M/Q ≫ 1 (step ≈ η·2√2·M/Q chronons — loose) but sub-chronon when M/Q ≪ 1, where the law must then hit ⌈T_h⌉ *exactly* — achievable only if the crossing chronon is computed from the step analytically, which should be stated. M ≤ 2⁸⁰ with Q as low as 2⁴ is inside the ranges (L51) and inside the sampler (P80–82).

10. **The probe does not test the premises at the gate edges.** L56–59 kill criteria are genuine independent kills, but: no p = 10M (probe starts at 20M; B2 starts at 10M); no eccentricity is named at all, while G2.2 runs to e = 0.99996 (H0193) with whirls at margin 10⁻⁴; B3's 0.1% periods — the tightest percentage gate — has no probe criterion; B6 horizon timing has none; B1's max-excursion clause (10⁻⁶) has none (only the exponent). Each is a premise the freeze depends on, discovered late instead of cheaply.

11. **Sequencing circularity.** L3/L39: the gates freeze after the probe, but the law text is written after that, before the first gate run. The probe (run by GLM, who chooses the integrator, L55) certifies a *family*; the shipped law is a different member. Minimum mitigation: require the probe to report its kick formula, order and η, and require the crate's law text to fall inside the probed envelope or trigger a re-probe.

---

## Rank 3 — cosmetic

12. **Step-2 cell crossings are cost without function** (analytic, never-expiring field, no contacts) — against engine.md rule 2; see Finding 4.
13. **B7's 10⁻⁹ is fidelity in disguise.** Both sides compute clock rates *"from the flow-frame Lorentz factor"* (selfcheck, P153); in exact arithmetic the identity is exact (√(1−|v−β|²/Q²) = √(1−2M/r) static; = √(1−3M/r) circular, since |u|² = M/r + 2M/r). State it as an exact identity on exact-circular states; it still catches the v-for-u confusion. The tested state set ("at a given state", L77) is also unpinned.
14. **The B9 gloss** *"about 0.1 core for a million ships"* holds for hour-scale orbits only (0.19 core at 90 min); for a 10M orbit around a 10 M☉ object (T ≈ 10 ms) it is ~0.1 core *per ship*. The gate numbers themselves are fine.
15. **L38 mis-cites H0190.** K4 measured *handoff* carries over 100 handoffs (a different rounding mechanism), not drift-kick rounding over 10⁴ orbits. The right evidence is the probe's exponent criterion — cite that.
16. **No gate checks L23's reduction** ("with no source, β = 0 and the law is today's lattice exactly"). It is the cheapest regression invariant in the document; a B0 running one lattice-v1 scene through the gravity crate with M absent would be nearly free.

---

## Per-gate achievability, correct vs wrong implementation

- **B1** — 10⁴ orbits × 402 events × 2 µs ≈ 8 s: fits the 60 s cap per case (case count undefined). Achievable *if* E, L are carried rationals (Finding 6); if derived from rounded k at small Q (sampler draws Q down to 2⁴, P80), a correct law fails outright. Wrong-pass: rest-inclusive relative base.
- **B2** — budget at p = 10⁴M is ≈ 2·10⁻⁵ rad/orbit; 2nd-order symmetric error ≈ (0.3–3)·10⁻⁴: a correct 2nd-order law **fails**; order ≥ 4 passes with margin. Wrong-pass: none within range; but p < 10M is excluded (Finding 7).
- **B3** — 0.1% is achievable even at 2nd order (frequency error ~ (2π/n)²/24 ≈ 10⁻⁵); periapsis-detection protocol on integer trajectories undefined. Discriminates (1PN period correction is 3/a: 30% at a = 10M).
- **B4** — deflection at b ≥ 10M achievable at 2nd order (0.518 rad vs error ~10⁻⁴). Capture clause: no cases (Finding 3). Threshold values 3√3M and 4M are correct GR.
- **B5** — vacuous (Finding 2).
- **B6** — well-cased (closed-form T_h, P104); tolerance ranges from ~1% (loose) to sub-chronon (Finding 9); achievable with exact crossing prediction.
- **B7** — exact identity, trivially achievable once restated (Finding 13).
- **B8** — contradicted by L36 (Finding 4); the queries-never-change clause is good and testable.
- **B9** — 512 vs 402 is right; orbit/accounting undefined (Finding 8); 2 µs/event with 128–512-bit integer kicks and exact isqrt is plausible on the M1 but untested by a float probe by construction.

## Principles (question 3)

No violation found of locality (step-2's analytic field is exact-by-construction; step 5's retarded commutative moments are right) or of observables-on-demand (L9, L20, L47 are consistent). Determinism: Finding 4, plus one honest tension: an undisturbed body pays ~402 events/orbit forever in a static field — internally consistent with "a body pays at events", but it is cost on schedule, not on change; worth one line in the contract acknowledging it.

## Probe (question 4)

The four kill criteria are independent, each sufficient, and correctly target precession, error type, capture threshold and deflection. They do **not** test the premises the plan most depends on: the literal motion rule of the contract (Finding 1 — it would be killed instantly), periods, horizon crossing, eccentric/whirl and p = 10M edges, and B1's excursion clause (Finding 10).

## Continuum fidelity in disguise / busywork ( question 5)

B7's 10⁻⁹ band (Finding 13) and, mildly, B1's 10⁻⁶ *magnitude* (the exponent already secures the error *type*; the magnitude serves ledger conservation and could be justified or loosened). Step-2 cell crossings are busywork (Finding 12). Nothing else: reusing G2.2/G2.4 as the case base is good economy, and the +10⁻⁶ rad/orbit floor in B2 is the right way to handle Δφ_GR → 0.

## What is right, plainly

The PG/river formulation and every continuum identity in the document check out exactly: static clock √(1−2M/r), circular clock √(1−3M/r) (|u|² = 3M/r at a GR circular orbit), horizon at |β| = Q ⇔ r = 2M, E = 1 capture at L = 4M, photon b_c = 3√3M, dependency bound Q + max|β| ≤ 2Q, and the no-source reduction to today's lattice. Separating the oracle (Arb judge, `gr-oracle`, the retired evaluator) from the implementation, freezing gates before any run, running the red-team and the probe before the freeze, per-kill criteria, the 512/402 event arithmetic, the ranges' bit-widths (consistent with universe-quanta.md's E ≈ 2⁹⁷ at Q = 2⁴⁰), and queries-never-mutate are all right. The design wants one sentence of physics (the kick's equation and order) and three case-set pins (B4 capture, B5 range, B9 orbit) to be freezable.
