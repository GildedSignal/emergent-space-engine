Working...
Check complete. **Grade: silver** — written to `lab/results/20261020-0036-system-e9a1/check.md`, with the author's wiki page corrected in place.

**What held under reproduction and attack:**
- The census reproduced exactly (regen exit 0; 0 violations all arms; the 40 s arm bit-identical to 20 s — the determinism control passed in my regen too).
- Two out-of-range arms of my own (5×10⁴ and 3×10⁵ burn, the latter at 1.5 GB peak): 0 violations, `pull_ships` pulls 0, skip 98.46/98.51% — the claim extends a decade in both directions.
- A 300,005-pair exact-integer attack on the cone-vs-`hit` never-miss (boundary pins, relativistic |w|≫|d| crossers, scales to 2⁶⁰): 0 violations. The certificate is a theorem on the predicate's own exact inputs — I verified `hit`'s three-branch exact implementation.

**The strongest finding:** no `crates/` commit since 18 October, so cc9d ran this exact code — and e9a1's direct probe (`pulled=0` at every scene while wave frames persist at cc9d's digits) falsifies cc9d's `pull_ships` mechanism attribution on its own tree. Genuinely new premise correction.

**Why not gold:** the fleet-loop replacement is attributed by elimination, not instrumented (the probe pattern was in hand); the cone is prior-art-adjacent — `encounter.rs`'s own doc and ce694696 hold an exact bound skipping 70–86%, uncited by the author; and nothing is adoptable in one step (the record's transition decade is untouched). One experiment to gold: instrument `resolve_fleet`/`resolve_handout` in the player's item at the wave, which must also reconcile ee4d's collapsed freeze with pulls = 0.

**Digit errors corrected on the page:** max hit ratio 0.974 not 0.95 (tighter than claimed, but wrong); the headline mixed arms (6,111 scans counted the bit-identical control, 432,403 cands excluded it → 4,377/432,403/2,570); "80×" is pooled (65× burn, 132× coast).

Tree restored bit-clean; no commits or pushes.
