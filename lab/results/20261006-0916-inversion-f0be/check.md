Grade: gold

**Abstract (for the integrator).** Attack on the adopted gold `taleb-09b5`'s phase-neighbour train. Reproduced bit-for-bit (S1, S3b, S4, plus an independent ring reimplementation): overtakes/orbit = 16 449 / 263 795 / 1 052 179 at n = 128/512/1024 — exponent 2.000, coefficient ≈ 1.0, 26×–257× the n·k watch, robust under a new seed, the trimmed n = 256 point, and 16× finer sampling (+0.5%, so the report is conservative). The gold's O(n·k) cost premise is wrong: rebuild-on-overtakes is Θ(n_c²) events/orbit, 26× the watch in the gold's own control scene. The rank claim survived even my extra attacks (2D-compressed blob, 668 dense contacts, max λ-rank 1). Adoption: re-derive maintenance before freezing, add wiggle/spacing to the trigger; a design note, no code.

## Reasons

**1. Reproduction (clean copy, author's folder untouched).** `python3 probe.py s1`, `python3 probe.py s4`, `python3 s3b.py` in a scratch copy: S1, all three S4 points and S3b match `results-all.json` field-for-field, including float fields. `work/patch.diff` is content-free (one line: a failed `python3 probe.py s4` from the wrong cwd); nothing to apply. A file-time anomaly (probe.py mtime after results-s4.json) is resolved: the shipped code regenerates every number exactly.

**2. Predictions.** `predictions.md` predates the decisive runs (S2a–S3b results are all younger; S1, the self-declared instrument control, legitimately ran first). S1 and S4 held (exponent [1.7,2.3] → 2.000; >10× watch at n=1024 → 257×; correctness intact). S2/S3 prongs failed and were reported as failed exactly as the pre-registered kill criteria required. One gap: pre-registered prediction #5 (quadrature clustering) is never reported. I tested it: refuted, and inverted — quadrature fraction 0.222 against 0.509 chance on S4's 9 contacts (my pipeline independently reproduces those 9). A dropped prediction is a reporting fault, not a load-bearing one.

**3. My attacks (beyond the author's).**
- **2D-compressed swarm** (the attack the lens missed: the author only compressed phase, never radius): n = 64, radial extent ~6ρ and phase extent ~10ρ, 668 contacts verified by a 65 536-node dense all-pairs scan — max λ-rank at contact still 1, k = 4 misses 0. The rank-survival conclusion is *stronger* than the author claimed.
- **Overtake-count artifact hunt:** mean 221 swaps/body at S2b (max 477 of 511) — broadly distributed, not a near-tie flip-flop; S4 at 16 368 samples gives 1 057 696 (+0.5%), so the Θ(n²) count is sampling-robust. S2b at 4× density gives +19% — the 4 096-sample Kendall *under*counts there, i.e. the maintenance number is conservative.
- **Ladder:** added n = 256 (66 003) and seed 99 (exponent 1.998); my independent ring code reproduces the author's three points exactly.
- **LB-gate sensitivity at e = 0.9:** densifying the gate T = 256→4096 adds 464 candidate pairs of which exactly 1 hides a contact (d = 5.7×10⁻⁵): S3 contact counts are ~0.4% low. Immaterial to the dwell refutation.

**4. Novelty.** No overtakes/maintenance measurement exists in docs/HISTORY.md or the board (searched; the gold appears only in the 6 October taste-log entry, whose text claims "a phase-neighbour certificate at O(n·k) replaces the quadratic tier"). The gold's own folder is absent from this tree, so the board entry is the record; this run supplies the term that claim omitted.

**5. Goal fit.** Direct hit on the encounters design (focus list). The premise shown wrong is the adopted gold's cost claim, with the mechanism (λ-wiggle ≫ local spacing ⇒ every pair within one wiggle swaps twice per orbit) measured at exponent 2.000 with coefficient ≈ 1. PRINCIPLES #1: "The cheapest compute is compute not done" — ~10¹² rebuild events/orbit at 10⁶ ships is the opposite; #4: "regimes are chosen by dimensionless numbers" — the trigger lacks the wiggle/spacing number this run exposes. Cost to adopt: one design-note change to the encounters spec plus a trigger invariant; no code.

## What the author missed

- Prediction #5 was registered and then silently dropped; it is false (contacts avoid quadrature, 0.222 vs 0.509).
- Radial compression was never attacked; I ran it and the rank claim survives it — the "watch is stronger than its proof" conclusion could have been stated more strongly.
- The ~19% Kendall undercount at 4 096 samples in the low-e jam scenes (conservative, but the dossier asserts sampling adequacy without the finer run I did).
- The 10¹²-events extrapolation to 10⁶ ships borrows the e = 0.3 scene's coefficient ≈ 1; the gold's own control scene measures 0.53 (21 052/200²), giving ~5×10¹¹ — same order, but the dossier should say which coefficient it extrapolates.
- The kill binds the *flat* rebuild-on-overtakes design as specified. A hierarchical maintenance (a tree over the λ-ring, rebuilds amortized by level) is neither measured nor discussed; the frozen-ring pad alternative is argued, not measured — the author discloses this honestly. If the integrator wants the alternative closed, that is the one experiment to queue: measure the pad width k needed for a frozen mean-longitude ring in the gold's control scene (predicted Θ(n_c) in wiggle/spacing).
