Working...
**Grade: gold** — written to `lab/results/20261007-0800-fermi-a91f/check.md`; tree restored to its pre-check state, nothing else in the run folder touched.

**Reproduction.** Applied `work/patch.diff` in a clean tree and ran all four dossier commands: the seven state-floor points, both shelf runs (all 24 epochs: bits/ship, floor gaps, `mismatches:0` including the K̄≈4.5 repack 66.6→62.5) and `verify a` (rates 1.75×10⁻⁴–4.96×10⁻³, exactly the claimed band) are **bit-identical**; only timing fields moved a few percent. The "frozen ladder's 50.0" anchor reproduces (`ladder 1` → `floor_bits: 50.0001`). Predictions (08:09:23) precede the first decisive artifact (08:12:43); P1–P5 held.

**My attacks, all survived:** fresh seeds (same curve); saturation to K=16384 (69.6 bits, slope decelerating — the kill criterion at 140 bits is unreachable); correlated contiguous victims (bit-exact, gap ≤9.4, no compounding); full churn x=1.0 (saturates at ~62 bits, bit-exact, compaction 2.7 µs/kick — 2× the 2²⁰ figure, confirming the author's own scale caveat).

**Why gold, not silver:** it converts HANDOFF's named "not measured yet" risk into shipped-code numbers, kills the 44-bits/kick compounding premise (173× below the draw account at K=256) and the kick-side "190 cores" framing (8% of one core), and adoption is zero code — an f-dial plus one B18 scene. Novel on the record: fermi-aab3 measured creation analytically, b-h-live never delivered.

**Author's misses (recorded):** the 0.8–7-bit gap range hides a transient 12.0-bit pre-repack reading; the `model_bits` formula undercounts Δt (17 bits, not 11); empirical-entropy bias makes "68.3 bits" really ≈71; the store gap is measured on one convoy shape only; the 1.2 µs p99 recurs every epoch, not just first-touch.
