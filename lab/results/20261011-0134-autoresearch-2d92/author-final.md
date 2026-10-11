Working...
Run complete — all suites green (lattice incl. the new equivalence test, event-core equality vs Chronon), tree carries exactly the three-file patch, artifacts in `lab/results/20261011-0134-autoresearch-2d92/` (dossier, predictions, loop log, A/B raw runs, patch).

**Claim:** exact i64 fast paths for the lattice law's visit predicates — `hit64`/`first_hit64` guarded by the GPU crate's own exactness certificate with i128 fallback — cut the contact engine's cost per event 11–16% on the contact-dense tracks with bit-identical digests everywhere, and the profile shows the remaining cost is the neighbour-visit loop (43%) and the calendar heap (16%), not the exact arithmetic.
