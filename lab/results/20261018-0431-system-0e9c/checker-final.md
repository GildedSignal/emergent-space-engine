Working...
Check complete. **Grade: silver** — written to `lab/results/20261018-0431-system-0e9c/check.md`, with the author's wiki page corrected in place where it overstated.

**Reproduced (bit-exact):** seam census both arms via the reconstructed command (`SCAN_CENSUS=1 [ES_LOCAL_BAIL=1] ladder_digest belt` — missing from regen.sh): off `bails=2920 fb_walk=5,374,600 doll_discard=4,336,560 fb_cand=972,248`, on `filt_walk=1,437,104 filt_cand=1,201,472` — every counter equal to the author's, candidates identical, walked −75.1%, digests bit-identical and equal to the frozen record (11 shared cases, not the claimed 12). Wall-paced census cells wobble ≤0.5% (bails 414 vs 416).

**Adversarial (3, one outside range):** chaotic key mashing — 15,564 bails, candidates exactly equal, digests identical (the registration-gap case survives); N=10⁴ burn — 0 bails, inert; **N=10⁴ belt crossing — 0 of 1,152 captures bail, windows ~97 bodies, digest identical both arms.** The bail's trigger (window bin-entries vs `bodies/4+64`, the universe's count) ends the bail regime between 3×10³ and 10⁴ on the ladder's own seam flight.

**The finding that demotes:** the 10⁹ headline ("10⁹ reads ≈ 100 s → 333") describes a configuration the shipped threshold cannot produce — at 10⁹ a small-doll scan never bails, and in 3999's in-band regime (where bails do fire at scale) the doll *is* the belt, so the doll-local answer is as big as the walk. The fix's real scale role is enabling 604c's local threshold; the 3×10⁶× saving belongs to that composition. **Gold experiment:** compose with the local threshold, fly the frozen digests plus 3999's in-band probe at 10⁵, both arms.

Tree restored to pristine (patch reverted, throwaway example deleted); checker evidence in `/tmp/checker-0e9c/`; nothing else in the run folder touched; no git operations.
