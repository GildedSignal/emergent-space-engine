Grade: gold

**Abstract.** The view premise (representation.md §2 / law.md:53 — memoized one-argument `deflection(b)`) is measured broken as a *key*: a rotating doll needs (b, sense) in-plane — critical |b| differs by 2.37× at χ = 0.998 as published, **3.32× after my correction** (true retro b_crit 6.14/6.83/7.00 M, not 4.83/4.95/5.00; the code took the wrong square-root branch) — plus (b, Q) off-plane; and the cone's Shapiro delay is unmemoized (0.5c emitter behind a hole, observer 10 M: shown 9.8° off, 27% of the lens displacement the design *does* correct). Static-spherical composition is sound to ≤ 0.6% (0.95% at r_o = 6 M, my case). Gate audit verified: no composed-view gate exists; r5/r6 never frozen. Reproduced bit-identically, 5.4 s. Adopt: one key bit + one delay table in the design docs, and an r6 behaviour gate.

## Reproduction

`python3 falsifier2.py` in a clean tree: bit-identical to `work/out2.json` (only `runtime_s` differs, 5.15 vs 5.02). `work/patch.diff` is empty — no repo edits, as claimed. The premise is quoted verbatim (representation.md:57, law.md:53). Every dossier number traces to `out2.json`; P4 arithmetic checks independently (0.5·8.58/24.99 rad = 9.84°; weak-field delay 2M·ln(4r_o·r_s/b²) = 10.3 M vs measured 11.29 at 50/200).

## Predictions

`predictions.md` (21:02:38) precedes the decisive run (`out2.json` 21:18:05). Credible as held-out: the author's P1 predicted > 1% / > 5° and measured ≤ 0.59% / 0.29° — an author who had peeked would not have been wrong in the pessimistic direction. Outcomes honestly reported: P1 refuted, P2 partially refuted, P3 held, P4 held for the named near case (27% ≥ 10%).

## Adversarial checks (mine)

1. **The Kerr retrograde table is wrong — and the claim is understated.** `kerr_photon_orbits` uses the plus branch `b = (r²+a²+a√Δ)/(a+√Δ)` for both senses; a circular photon orbit needs R = 0 *and* R′ = 0, which selects the minus branch for retrograde. Verified three ways: (i) R′/|R| at the code's retro values is ~10¹³ (not circular); at the minus-branch values it is rounding-level; at a = 1 the minus branch gives −7 exactly (Bardeen's limit; the code's gives 5). (ii) All three published retro values lie *below* 3√3 ≈ 5.196, impossible for retrograde (≥ Schwarzschild). (iii) The code contradicts itself: its own `kerr_alpha(−6, 0.9, …)` returns null — captured, consistent only with the true critical 6.83, not with its own table's 4.95. Corrected: b_retro = 6.14/6.83/7.00 at a = 0.5/0.9/0.998 → ratios 1.50/2.41/3.32 (published 1.18/1.74/2.37). The a = 0 self-check ("3√3 both senses") cannot catch this — the branches coincide at a = 0.
2. **The same-|b| bend split is sound.** Schwarzschild α(|b| = 8) = 0.859 sits exactly between α_pro = 0.676 and α_retro = 1.254 (a = 0.9) — the textbook ordering; the 0.578 rad delta is real, reproduced, and independent of the branch bug (`kerr_alpha` uses the full potential).
3. **My extreme case, r_o = 6 M, r_s = 30 M** (deeper than the dossier went): composition error ≤ 0.95% across β = 0.02°–40°; exact gather finds 4 images (2 bright + 2 winding), the point-lens construction places 2 (its equation has at most 2 roots). P1's refutation is robust; P2's missing-winding part is structural, not numerical.
4. **P4's static control** is trivially exact; the delay magnitudes match the weak-field estimate.

## Novelty

No H entry or doc attacks the view's memo key or the view's delay. Closest: H0178/H0183 (oracle *gains* Shapiro, for judging), B16 (moving-lens bend, board), H0186 (plan reorder). The gate audit is accurate against the repo: `lab/rungs/` holds r1–r4, r7–r10; law.md:88 still lists r5/r6 open; representation.md §7:130 scopes r6 as cost-only ("Newton iterations and samples per frame"); B3/B16 gate bend only; B19 gates the doll's geodesics, not the view's memo. B12-style premises 1–3 quoted in the dossier match B11, H0205 and the plane gates.

## Goal fit and grade

Principle 30: "what really matters is navigation, knowledge and dynamics those need to be perfect"; principle 28 makes the view the player's only instrument. The run shows a frozen-design premise (the memo key and the missing delay) is wrong, with measured numbers, honest self-refutation, and the cheapest possible fix in the design's own idiom (one bit, one table — "the right representation always just feels right", 19). Adoptable within one step: a design-doc edit plus freezing an r6 behaviour gate. Gold despite the retro-branch error because the error *strengthens* the load-bearing claim (3.32×, not 2.37×) and the corrected numbers are supplied and verified above; the integrator must adopt the corrected values, not the dossier's table.

## What the author missed

- The wrong square-root branch, and a degenerate control: a = 0 verifies both branches at once ("a control that cannot fail is a control" — here, one that cannot discriminate). The |b_retro| ≥ 3√3 sanity bound was one line away.
- The retro `alpha_retro = null` at |b| = 6 was reported as "quadrature diverged" instead of recognized as capture — which itself refutes the published b_retro = 4.95.
- Already self-named: magnification of winding images, off-plane (Q) behaviour, multi-doll composition — all argued, not measured.
- P4's comparator could also have included the *knowledge/navigation* error (ranging with a flat cone), which the author notes in predictions.md but does not measure.
