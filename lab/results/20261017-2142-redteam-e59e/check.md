Grade: gold

**Abstract.** Premise kill, reproduced byte-identically: `docs/representation.md` §2's
observable set omits opacity, and the shipped gather (`view.rs` "(no lensing yet)") draws
stars through black holes and planets. Synge arcs verified against RK4 bisection to
4.2×10⁻⁵: **25.0% of the sky fabricated at r_o = 6 M (2,500/10⁴ rows), 46.6% at 3.2 M,
1.64% at 100 M; a 2-radii planet approach shines 16.7% (1,667) through the ground.**
deflection(b)'s domain ends at the rim (6.51 rad at 1.001·b_c = the analytic law; both
b ≤ b_c wirings fail eclipse parity). No rung, gate or criterion sees it — r6's presence
bar (`rows_found ≥ 0.999`) requires the rows occlusion must remove; Julien's conversation
requires it. Cost to adopt: one interval test per occluder per row + one asin per black
hole; freeze the eclipse-parity rung.

## Reasons

1. **Reproduction.** `python3 falsifier.py` in a clean run: `evidence.json`
   byte-identical (0.2 s). `regen.sh` re-verifies the greps: "occlu|eclipse" → NONE in
   `docs/representation.md`, `docs/law.md`, `lab/rungs/`; `view.rs:15` "(no lensing yet)"
   confirmed by my own read. The doc's L53–59 list and the L28 spoke-count bug (2π·16/ln2
   = 145.0, not 128) verified in place.
2. **Predictions.** mtime order: `predictions.md` 21:51:30 → `falsifier.py` 21:52:50 →
   `dossier.md` 21:53:49; the runner's evidence 21:55:38. Pre-registered, and all seven
   held (164/793/2,500/4,662; 319/1,667; 25.0% exact; >3 rad at 1.01 b_c). The one
   mid-run event (P5 sign) is disclosed in the dossier.
3. **Adversarial cases (mine, independent instruments — no author code reused).**
   - *Finer deflection* (periapsis method, dphi = 2×10⁻⁵): 0.55693 / 0.90217 / 2.08057 /
     3.17093 / 4.22969 / 6.51065 at b/b_c = 2…1.001 — the author's values match within
     his 0.002-rad step quantization; extended outside his sweep to 1.0001: 8.81049 vs
     the strong-deflection law's 8.81011. P5 stands.
   - *Outside the tested domain* (he stopped at 3.2 M): my full-range bisection agrees
     with his formula down to 3.05 M (0.4910 = 0.4910) but at r_o = 2.5 M the true shadow
     is **62.0%** of the sky where the Synge-formula reading gives 38.0% (at 2.05 M:
     87.0% vs 13.0%) — the reading inverts inside the photon sphere. Every reported
     number is at r_o ≥ 3.2 M and correct; the omission claim is *stronger* inside 3 M.
   - *Aberrated occlusion* (the regime he flagged, unmeasured): planet dead ahead at
     2 R, closing β = 0.5 → blocked arc 16.7% → 27.7%; β = 0.9 → 54.9%. The static
     numbers are a lower bound; the claim survives with margin.
4. **Novelty.** `lab/wiki/view.md` (45 runs): multiplicity (6eae), delay
     (5977/ace6/0b45/fb64), deflection keys (8be2), k=0 pair (8f00), photon-ring
     newborns (a616, ungraded) — no run measured opacity. `docs/HISTORY.md`'s occlusion
     entries (H0014 etc.) are the pre-pivot inertial law, exactly as the dossier's blind
     spot says; the September G6 line is verified ("The observatory provides …
     occlusion"). The premise gap is new on this record.
5. **Citations verified in place.** r6's oracle is literally "every live emitter must
   have a `Seen` row each frame" (`rows_found >= 0.999`, branch
   `claude/lab-20261017-1018-redteam-13c6`) — its presence bar demands the rows true
   occlusion must remove. `kerr.rs:717` "captured rays return None". All seven
   conversation lines exist verbatim (L984/4283/4864/4872/5032/6450/7375).
6. **Goal fit.** Shows a premise is wrong (the spec every view run inherited), with a
   player-visible size, the missing criterion named (eclipse parity), and a
   one-interval-test adoption cost. PRINCIPLES 30: "what really matters is navigation,
   knowledge and dynamics those need to be perfect" — this gather is the knowledge half;
   and §2's own "Light is gathered at the observer, never broadcast" makes opacity the
   cheapest possible form: a per-row predicate. The page's proposed adoption now carries
   the r_o ≥ 3 M domain note (my correction).
7. Not three agreeing golds on this topic — no closure; the page stays open.

## What the author missed

- **The instrument's validity boundary.** Synge's α_sh reading is valid only for
  r_o ≥ 3 M; inside the photon sphere it returns the complement (62.0% true vs 38.0%
  from the formula at 2.5 M). No reported number is affected; the page now says so,
  because the formula is written into the proposed §2 amendment and would be wrong as
  adopted below 3 M.
- **Occlusion is observer-velocity-dependent** (aberration): 16.7% → 27.7% at β = 0.5
  closing on a 2 R planet, 54.9% at β = 0.9. Static arcs are a lower bound; the
  eclipse-parity rung must gate moving observers too. Added one clause to the page.
- **P5 quantization undisclosed**: all his exact values are n·0.002 − π (π's tail
  visible in the shared digits). Harmless — my dphi = 2×10⁻⁵ run confirms to 5×10⁻⁴ —
  but the dossier should have said the integrator's angular resolution.
- **"names six times"** — seven lines are cited (five verbatim "occlusion" plus the
  shadow and eclipse lines). Trivial.
- The 2-D-sky reading is right for this engine (view.rs is `[f64; 2]`), but the
  dossier argues it from game design rather than from the shipped geometry that
  settles it.
