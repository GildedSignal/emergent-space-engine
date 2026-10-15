Working...
**Grade: gold** — written to `check2.md`, page corrected, tree restored to base `c989260f`.

What I did and found:

**Reproduction.** Applied `work/patch.diff` to the clean base, built in a private target dir, flew all 23 arms. Every deterministic number regenerates exactly: per-scene digest identity across 5–7 arms, the full cap curve (512 → 83.6%/1.12×dem … 65,536 → 85.3%/1.00×dem), the exact containment result on burn at 65,536 (promotions = 40,187 demotions exactly, 0 evictions, hits = global's 584,807), and inertness without the seam. Suite: 77/0/3 (the dossier's "46/0/2" undercounts; same verdict).

**The runner's regen was contaminated — diagnosed, not the author's fault.** A sibling checkout rebuilt the shared `lab-target-0` binary at 15:34, mid-run: flights 13–23 printed a counter format that doesn't exist anywhere in this patch and `table.py` crashed on it, while `regen.sh` still exited 0. `regen.sh` should fly a frozen private copy of the binary; my clean rerun stands as the reproduction.

**Adversarial (all beyond the author's domain).** Seed 7: identity, 1.02×dem at cap 4,096. Burn at 10⁵ (author's burn domain was 10⁴): identity, but cap 16,384 thrashes — 7.22×dem, 43% hits — **burn's working set scales with N** (130,187 at 10⁵); at cap 131,072 containment is exact again. Cap 1: identity, bound holds, graceful. rtf 100 (10× frames): digest unchanged — eviction scheduling cannot leak into the canonical digest. Code review concurs: pure `Orbit::compile`, single-decrement ring accounting, ring→slot-only lock nesting.

**Page correction.** Open direction 1 claimed 16,384 "covers burn" and 65,536 matches global "everywhere flown" — true only at burn 10⁴; I rewrote it with the measured N-scaling so the integrator doesn't ship a fixed default.

**Misses recorded (non-blocking):** the 10⁹ composition's rate is 3.5×10⁻⁷, not 10⁻⁸ (typo; the ~0.15-core headline is right), seed 1 throughout the run itself, and the suite tally. Gold because: exactly reproduced, pre-registered predictions with honest misses, identity and the bound survive everything I could fly, and it closes 1d52's named experiment — 962 B/body kept with the promotion bill composed ~800× down at 10⁹, adoptable in one step.
