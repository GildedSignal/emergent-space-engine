Working...
Check complete. **Grade: gold** — written to `lab/results/20261016-2229-second-20261016-2138-fermi-e7ef-98cb/check.md`, with one in-place correction to the author's `wiki/kick-cadence.md`.

**Reproduction.** Runner's `regen.sh` (exit 0) matches the author's numbers within shared-box wobble on every claim: interval ratio 8.000× exact, spell 21.1→0.1 s, deficit 36,748→806, controls clamp at 72×/144×, ledger 22.5/8.8 x86 and 13.2/5.1 M1 cores, required kick 23.1 µs. I re-derived the ledger arithmetic independently (RATE0 = 1/(2·14,072) from the belt_first print itself; every cores row checks). Patch applies clean to pristine main.

**Adversarial cases (mine, not the author's):**
- **Decomposition** — stagger-only at 3×10⁵ rtf 1800 does *not* cure (spell 65.8 s, deficit 66,136: demand 0.96 s/s > 0.72 budget); split-only does *not* cure (spell 12.6 s at the un-de-phased crest). Both levers necessary — the composition is real.
- **Burn arm** (the author's named miss) — composed burn is safe: spell 0.6 s, 98.9% delivered, 0 refusals, player alive.
- **10⁴ arm** (below the swept range, and the one number regen.sh doesn't regenerate) — fires = 1,179 exactly, matching 10⁵ and 3×10⁵: the crash-search term is provably N-flat, never the belt's.
- `IMPACT_GUESS=0` vs default-on — byte-identical belt_first output; the guess is outcome-exact as coded.

**Page.** Faithful and correctly placed; main's unresolved conflict header resolved by superseding. Corrected one overstatement: "identical shipped vs composed" fires → N-flat (identical at 10⁵; the 3×10⁵ shipped arm fires 1,098 on its 7×-shorter window).

**Caveats kept in the record:** split legality cited not re-flown (a belt rung at Δs×8 is the named closer), 10⁶ unflyable under the 2 GB cap, `IMPACT_GUESS` defaults on (the "off = shipped" wording overstates for that one lever), and three second-run dossier numbers are unregenerable but bounded by the saved runs.
