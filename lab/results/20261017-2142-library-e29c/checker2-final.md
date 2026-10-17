Working...
Check complete. **Grade: gold** — written to `lab/results/20261017-2142-library-e29c/check2.md`.

**Reproduction:** full. `bars.py` and `verify_quotes.py` (5/5, exit 0) rerun independently, byte-identical. Every shipped constant verified in-tree: `AU_LS` (page.html:58), kind-4 2×2 rect + names kind≤2 + `fitLog` kind≤3 (page.html:142/154), belt band (scenario.rs:333), 32-bit periapsis (law.md), 49 m = `Scalar::raw(34,-10)` = 49.06 m (scenario.rs:344), 313 locals (nladder.md), and all of f5bd's flown drift constants. All arithmetic re-derived exactly (T*, k*, break-even 547 m).

**Predictions:** written 2 s before the decisive run; all five held numerically (P2's provenance sentence was mis-attributed — the value right, the source wrong).

**My attacks:** contact radius across the full belt (forcing survives, 5.4× margin at the inner edge); the coarse dial's D*=1.6 km sits *above* q_grid but can't resolve contacts, so the forcing's domain "dials that see contacts (b*≤547 m)" holds; the fence's N-threshold is ≈4.3×10⁸ — ~260× beyond the memory wall, a stronger margin than claimed; coherent drift gives 7.6 orders (not ≥10) on the mass bar — deletion survives; the positional annulus is O(1) wider than the a-band, in the safe direction.

**Corrections made to the author's page:** flipped "38.5% kept" → delete 274/712 = 38.5%, survival 61.5% (kick-cadence.md:251). Checker 1's 49-m provenance fix verified and kept.

**Why gold:** it closes f5bd's explicitly-open requirement ("an angle bar no page has frozen yet"), deletes a component (the re-kick leaves the flight law, 0 firings at every flyable N with ≥4.2× time margin), kills 10c4's q_mass premise, and is adoptable in one step — the compose rung drops the re-kick arm and gains derived `q_view(N)`.
