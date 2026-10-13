Working...
Check complete. **Grade: gold** — written to `lab/results/20261013-1249-second-20261013-1145-system-549f-f2b7/check.md`, with two overstatements corrected in place in the author's `wiki/a-word.md`. Tree left pristine at c51d3491; no commits.

**What I did:**

- **Reproduced everything from a clean tree** (applied `work/patch.diff` myself): the three frozen readout gates fail with identical numbers (velocity jump 3.85e-2 vs the frozen 1e-4; map-ratio 356.07x vs 3x; bounded and clock gates pass); wired census errors, digests identical wired vs pristine; instrument control reads exactly 0; bench 25,829→17,127 ns/emitter scratch (1.51x), 12,702→8,771 memo (1.46x); strong field r=20 M 4,345,751 events / 0 reads / digest exact.
- **Adversarial 1 — v1 rebuild** (regen.sh does not regenerate it): disabling the boundary refresh gives the claimed **5.07e-2** exactly.
- **Adversarial 2 — dive held 5× longer**, β→0.83 (author stopped at 8 s): wired error reaches 2.07e-3 but stays exactly 40.7% of the term — the first-order-quadrature mechanism extends, no blow-up.
- **Adversarial 3 — r=10 M** (author tested 20 and 4000): ship survives, ~2.84e6 events/orbit (r-independent), 0 gated reads.
- **Bonus instrumentation** (reverted): the v2 refresh fires **56,027 times in the gate scene** and the gate still fails — the freshest-possible-word objection is closed; on plane coast/fwd it fires **0 times**, mechanically confirming the hours-stale word.
- **Novelty**: 7b86 priced the term invisible; 549f's page proposed the word as its accuracy-keeping replacement (open direction 1, "the cheapest", expected to pass). This run wires both write points, refutes the replacement on frozen gates, and shows the census priced an unwritable word (10⁴× off). Not in HISTORY; not a repetition.

**Gold because** it shows a premise wrong (PRINCIPLES 2: the census judged error size and missed the continuity behaviour; PRINCIPLES 9: the configuration dies, the method survives), is reproduced bit-exact including the one number regen.sh skips, and adopts in one step (the page update). Missed by the author, all recorded in check.md: the 56k-refresh measurement was one instrumentation away; a 2.8e9-vs-5.6e9 ticks typo in the claim section; the strong-field 0-read diagnosis still unseparated; the amortization is a plain-scene number only.
