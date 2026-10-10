Working...
**Grade: gold** — written to `check.md` in the run folder. Tree restored; nothing else touched.

**What I verified (all in a clean tree at a838a28, from `work/patch.diff` alone):**

- **Reproduction, bit-for-bit:** baseline `d4413b80…`; the 9-cell zero-miss matrix regenerates cell-for-cell (pair *and* rejection counts); full 3×10¹⁰ co-radial both arms `29900350…` with 611,777 contacts, 3,019,749 pairs at 3.98 µs/pair and +8.7% filter overhead; linear in population (cohort 50/100/400, µs/pair flat at ~4).
- **The frontier claims re-derived from my own edits, not the author's binaries:** the 2⁶¹ tightening reproduces both recorded digest breaks exactly (`cad102e0…`, `a27c2800…`, 438 rejected each); the pure word-convention bound rejects 97.7% and loses *every* contact — worse than claimed.
- **My adversarial cells:** held-out seed 99 (3/3 identical), place 0 at 3×10¹⁰ with filter on (digest unchanged), threads 4 (schedule-independent, on=off).
- **Novelty:** no prior kill of a per-pair scan pre-filter anywhere in HISTORY/docs; the run also grows the dense same-doll tier the original silver never measured.

**Why gold:** the previous checker pre-named this experiment's condition — "a safe ≥10× on the scan intercept, **or a kill**, is gold." The kill arm fired with a measured mechanism (rejection information lives behind the decode; h = 2⁴⁰ multiplies bound looseness past every ship-scale gap), adoption is zero code, and it redirects deletion to the encounters seam, matching the 6 Oct gold.

**Noted misses:** "safe on seed 7" is too generous (my 5e8 run breaks it too — strengthens the kill), the variant-1 raw output wasn't kept, the 9% range endpoint is unregenerable, Q5 (FASTDOLL) built but never timed, and the 5e8-vs-3×10¹⁰ matrix deviation unflagged.
