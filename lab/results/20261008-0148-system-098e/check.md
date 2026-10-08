Grade: silver

**Abstract.** Claim: the queued `b-news-gravity` build's per-(body,source) cursors repair the never-built cell layer; per-cell version rings read at a static integer lag table (max cell-pair distance/c) carry news-at-c, multipoles and causality certificates, never early. All toy configs and `smear.py` reproduce bit-identically (exact-vs-cell 9.4e-9 / 5.0e-10 / 2.6e-10; Laplace control separates ~2e4×). Adversarial: β_source=0.33 → 1.0e-6; receiver ~3.5 cell widths out → 8.8e-7 — both at the stated exact-pair handoffs; never-early held everywhere. But the headline "≤3.4 source-cell light-crossings at every separation" is falsified across the full doll: max 68.6 source-cell crossings; the bound holds only in larger-cell units (≤3.0). Gain 21–165× state, 83–662× tests; cost: redirect the queued lens before it builds.

## Reasons

1. **Reproduction, exact.** `python3 toy_news.py c30|c300|per` and `python3 smear.py` in a clean tree: JSON outputs bit-identical to the author's (`mine==auth: True` ×3); smear med 2.74 / max 3.36 matches. Each ≤ 60 s. `work/patch.diff` is empty — all work is in the run folder's scripts, so nothing else to apply.
2. **Predictions were pre-registered and honestly graded.** File times: `predictions.md` (5 m) predates every output (1–4 m); tuned case (3 seeds, 8 yr) not even shipped. 7/8 held; #7 falsified and reported as falsified with a proposed replacement — the mark of a real pre-registration.
3. **Premise verified.** `lab/lenses/b-news-gravity.md` does prescribe "a cursor per (body, source) and a version ring"; H0196 and HANDOFF confirm the multipole cell layer was never built; `docs/archive/engine.md` rule 11 says exactly "no region mechanism uses them yet"; representation.md §1's light-crossing-time quote is verbatim. Cost arithmetic checks (2^20: 10.5 M vs 0.51 M words = 21×; 10.5 M vs 126 k tests = 83×; 2^23: 165× / 662×).
4. **Adversarial cases (mine).**
   - Full-doll smear (`smear_wide.py`, sources in rings 0–30, receivers to ring 98): lateness in *source*-cell crossings med 7.6, p90 28, **max 68.6**; in *larger*-cell crossings med 1.3, **max 3.0**; relative smear med 5.5e-2. The author's `smear.py` samples only dk ∈ ±5 rings (r₂/r₁ ≤ 1.24), which hides this. The dossier's corrected invariant ("late by at most ~3 source-cell light-crossings, independent of distance") is wrong in its unit; with "larger-cell" it holds. Same-ring diametric pairs: 2.0 (the wide-table caveat is real but harmless).
   - Fast source: c=10 (β=0.1) → 7.7e-8; c=3 (β=0.33) → 1.04e-6. Scales ~lateness×β as the dossier's own model says; the proposed β-regime gate now has numbers (between 0.1 and 0.33 at this event size). Never-early holds.
   - Big event: dv=0.3 at c=30 → 9.3e-8, exactly 10× the tuned event (linear in change). Laplace control separates ~50×.
   - Near receiver (a=1.15, ≈3.5 cell widths from the source's orbit): max 8.8e-7 vs med 2.5e-10 — crosses 1e-6, confirming the author's stated handoff to the exact pair layer below ~4 widths. Laplace control explodes there (5.9) while exact vs cell still agree: the instrument separates the laws being compared.
5. **Novelty.** No cell-owned version rings + static lag table in HISTORY.md, representation.md or law.md; it builds on q-gravity-cursor's version ring (per pair) and H0196's never-built layer — the ownership move (pairs → cells) and the lag-table mechanism are new. Prior art on retarded gravity (Laplace control, Carlip) is used, not rediscovered.
6. **Goal fit.** It corrects a premise before a one-way build (PRINCIPLES 9's spirit; "question every requirement"). One structure for news, multipoles and certificates is principle 7 verbatim ("Multipoles are the mechanism, for gravity and for causality regions alike"); never-early-by-construction is principle 23; undisturbed sources cost nothing is principle 3.

Not gold: (a) the dossier's stated invariant is falsified in its unit (reason 4) and needs the one-word correction; (b) the evidence is a Newtonian float toy with c exaggerated ~2000×, judged against a reference that is itself first-order (see below) — the claim "adoptable" is a lens redirect, not a measured engine change.

## The one experiment that would make it gold

Build it: redirect `b-news-gravity` to per-cell version rings + the static integer lag table (exact per-pair light cones only inside the encounter layer and above the β gate), implement in `crates/universe`, and pass the lens's own named gates (B13, B14, B17, G1–G6) with the per-pair-cursor design built as the measured control. Restate the smear bound in larger-cell units in the lens.

## What the author missed

- The corrected invariant's unit: "source-cell" → "larger-cell". The ±5-ring sampling window in `smear.py` made "at every separation" true of the sample and false of the doll.
- Numbers for the two regime gates the design needs: β_source ≈ 0.3 and separation ≲ 4 cell widths (both cross 1e-6 at this event size).
- The toy's "exact" reference is itself first-order: arrival uses the receiver's *unperturbed* position *at t_e*, an error ~β_r × light-time (~1.5e-3 yr at c=30, same order as the smear). The 9.4e-9 is "cell vs this reference"; harmless here (both errors are second order in the event), but it should be said, and it grows at small c.
- `toy_news.py`'s docstring says the cell lag is "min distance"; the code (and dossier) use max. Stale doc, not a code bug.
- `engine.md` is archived (`docs/archive/`); cite the live home (law.md / HANDOFF) when redirecting the lens.
