Working...
Check complete. Verdict written: **Grade: gold**, with three scope corrections folded into the author's page.

**What I did:**

1. **Reproduced** — the runner's `regen.sh` output matches the dossier digit-for-digit (8-arm table, C50 curves, kick counts 503,014/421,804–422,286, all controls, refactor control IDENTICAL, b4a8 cross-checks: 891 genesis frames, g=3 dues max 17). Applied `work/patch.diff` myself in the restored tree; it applies clean.

2. **Verified the mechanism in shipped code** — `project` (step.rs:611-621) sets `p_t = U_P − H_D`; `kick_clock` (704-716) derives `full` from `y = H_D + p_t + c = U_P(x) + c`: position, not orbit constants. The 37% artifact claim is consistent: 2³² = 4.295×10⁹ is exactly 2^ilog2 of the true min 5.2995×10⁹.

3. **Five adversarial arms** (my own env-parameterized copy of the instrument, since removed):
   - **q1e1** (all 2,700 bodies on ONE exact (a,e)) — 2,700 distinct steps every generation, battalion 1: the od-4 kill at its limit. But σ=3.9% → shear 1.25%/fire, lifetime ~19 fires: the author's "spread-independent lifetime" fails outside their 7.8–10.1% σ band; slope/σ ≈ 0.26–0.37 across all 9 arms (P3's proportional form survives).
   - **seed 7** — 58.5× → 2.3×, battalion 1 (author ran only seed 1).
   - **bigN 35,700** (3× the tested N) — largest battalion 2, birthday pairs, not a comb.
   - **long g=16** (2× the horizon) — C50 plateaus at 2.2–3.0×, never below 2.2, no battalion re-forms in 17/17 censuses: the dossier's "falls below 2× just past g=8" is wrong; a standing ~2× tail.
   - **q32e4** (the pre-registered 4-e-level form the run silently swapped for 16) — same behavior (50.8× → 2.0×).

4. **Novelty** — the calendar page carried od 4 as "unmeasured" and od 2's checker note named this exact census as the next run; f82a/3294's 57× is reconciled, not repeated.

5. **Page corrections in place** — checker note with the three scope corrections plus the confirmations; removed a truncated duplicate refuted bullet. `check.md` written with the abstract and the author's misses (single-class extreme unflown, single seed, plateau extrapolation, m_med imprecision, e-levels drift).

The core claim — a quantized-period belt never sits on the combing side because the step follows position — was strengthened by every attack; the corrections are scope, not structure.
