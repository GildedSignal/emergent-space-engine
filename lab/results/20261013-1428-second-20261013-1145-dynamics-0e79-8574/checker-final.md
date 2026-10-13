Grade: silvCheck complete. **Grade: silver.**

**Reproduction (independent, from the shipped tree):**
- `grid-ref.txt`/`grid-d-ref.txt` verified faithful against the `origin/claude/lab-20261013-1145-dynamics-0e79` branch (clean diff); the patch adds only the probe example — engine untouched.
- My own 38-flight run: **22/22 record rows bit-identical** to the 1145 refs, **38/38 rows** identical to the author's grid, refusal decomposition identical (`reflog.py` diff clean). Third independent run agreeing with author + runner.
- The Λ correction verified from shipped code, not just the probe: `scenario.rs:119` Home `mass_log2: -18` (2⁻¹⁸ solar = 1.274 M⊕); my own arithmetic gives g = 12.47 m/s², weight 10.33 at 1.099R, Λ(L) = 0.335·2^L with `TICK_SECONDS` = 4.925490947e-6; the coast row's Ψ = 205.5418 rad cross-checks the period to 5,175 s. Turn tier 2⁻³⁰ turns/tick = 4.09°/min confirmed from `ctx.rs:42`.

**Adversarial cases (each outside the author's tested cells):**
1. **E2.0R L0** (Λ 1.38 from 2.228R): **crashes** at 10.25 km/s — the dossier's and page's "no level crashes at all" from ≥ 2.228R was falsified as worded (L0 was never flown from 2.228R). Corrected in place: Λ*(2.228R) ∈ (1.38, 2.75); the "falls ≥ 2–4×" summary survives.
2. **E1.6R L2** (Λ 3.07): lives, grazing 1.0396R → Λ*(1.665R) ∈ (1.54, 3.07) — the falloff is front-loaded.
3. **off45 at γ₀ 1.5**: storm still fires (13,784, 100% in-burn, doll-constant), first refusal at **γ 1.32** — below the page's band floor; the mechanism reading is confirmed and extended, the bands are trajectory-descriptive.
4. Bonus: **F L5 at 2³⁷** (4× horizon) still bound, minRpost 1.0293 unchanged — the bracket is not a transient.

**Why silver:** two of four pre-registered readings were falsified (honestly reported — the 1-October precedent is silver), predictions.md's mtime (14:56) postdates the decisive grid (14:54) so the freeze is declared but unverifiable, and the headline cell overstated its own grid by exactly the one level I flew. Gold path: the two 1.445R cells (L2/L3) closing the curve's widest bracket, with a verifiably-timed freeze.

Deliverables: `check.md` written; the author's wiki page corrected in place (brackets, storm non-floor, L5 horizon, cos0, e-range, run entry); my probe variants removed — tree clean, nothing committed.
