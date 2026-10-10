Working...
Check complete: `lab/results/20261010-1302-taleb-bb88/check.md` written, first line `Grade: silver`.

**What I did**

- **Reproduction**: `python3 probe.py /tmp/check_out.json` — 36/36 runs bit-for-bit identical to the stored `probe_out.json` (173.6 s vs claimed ≈175 s). File mtimes confirm predictions-first (13:10:28 → 13:15:03 → 13:17:59). `patch.diff` empty; run self-contained.
- **Adversarial (pre-registered)**: e = 0.99 → enc/body 40.3–40.5 vs 40.5 predicted (law extrapolates); measured drop fraction of a rank-4 window at e = 0.9 = **39%** (dossier's "a third" was derived, now measured); n = 30000 circular same R → enc/body 28.68 (pred 28.7), **72% of contacts beyond rank 4** — the gold's constant breaks even at e = 0, confirming "rank 4 is a scene property"; K-doubling bit-identical; τ-order ≡ M-order at n = 3000. I also re-derived the count law independently — |dP/dM| at apoapsis = a√((1−e)/(1+e)), so it is exact Kepler geometry, not a fit.
- **Novelty**: no H entry (latest H0215), no rank/eccentricity text in `docs/law.md`; closest priors (q-candidate-degree's e 0.7–0.9 miss, B16's √((1+β)/(1−β))) are different mechanisms.

**Why silver, not gold**: the physics is exact, reproduced, extrapolated, and premise-relevant (one-step adoption before the certificate is wired), but four pre-registered letters failed as written in one consistent direction (P1 "max ≈ 3" vs measured 7; H1/H2 "max doubles" vs ×1.67/×1.43; NEG "80+" vs 59–63) — numbers disclosed in the table, yet reported "Held"; and the fix (bunching-sized window) is argued, not measured. Plus the "overpays 19× at perihelion" line conflates epoch-local re-checking with the contact set — an aphelion-sized window has zero structural waste in a standing fleet (12.5 candidates = 12.48 contacts/body). The named gold experiment: implement the re-sized window in this harness with clean pre-registered letters and show zero misses at cost ∝ real contacts across the e- and density-ladder.
