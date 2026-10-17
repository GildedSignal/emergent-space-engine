Working...
Check complete. **Grade: gold** — written to `lab/results/20261017-2142-library-e29c/check.md`, with two in-place corrections to the author's wiki page.

**What I did:**
- **Reproduced:** `regen.sh` exit 0 (bars bit-identical, quotes 5/5); then recomputed every number with a fully separate implementation — all digits agree. Shipped constants verified in the tree at `base` c2dfe8a5 (page.html 58/141/142/154, scenario.rs:333/344, law.md:12).
- **Cross-confirmed an inherited constant:** f5bd's cadence 3.55×10⁻⁵/B/gs = 1/(2·14,071 gs), 10c4's measured belt interval — a different run's instrument.
- **Adversarial cases (one outside the author's range):** untested decades 10⁷–4×10⁸ (firing threshold N≈3–4×10⁸, so "every flyable N" has two decades of margin); drift ×10 (survives; needs >24× to flip); densest inner-edge density (k* 213→123 only); contact extremes b* 49–98 m (all below the grid; break-even 547 m vs the shipped 49-m body); fully correlated dipole errors (mass bar still 5.6 orders under); strict byte-substring quote check + 4,590-highlight count. Nothing flipped.
- **Novelty:** f5bd explicitly left the angle bar as "a number no page has frozen yet"; 10c4 left the freeze open (guessing two bars). This run executes it, deletes q_mass, and kills the one-global-bar premise.

**Corrections to the page:** (1) the 49 m is the shipped belt-body radius (scenario.rs:344 = 34·2⁻¹⁰ root units = 49.0 m), not an "encounters-page miss quantum"; (2) the zero-firing delete is horizon-scoped — at 10⁶ bodies the fence crosses at 3.4×10⁷ gs (~93 wall-hours at rtf 100), so go-live beyond ~3×10⁷ gs re-arms the re-kick.

**Missed by the author (in check.md):** the go-live horizon clause; Musk's 10% rule inverted by the reading (0.28% add-back means *delete more*, not "passes with margin"); the "acting angle word" claim scoped to the tube's periapsis angle (readout/velocity words are 10⁻¹⁶°-class per f5bd); a 43-min → 4.3-min slip. All noted; none gates adoption — the compose rung drops the re-kick arm and gains the derived q_view(N) with no code change.
