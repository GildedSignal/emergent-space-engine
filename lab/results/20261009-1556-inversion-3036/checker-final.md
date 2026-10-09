Working...
Check complete. **Grade: silver**, written to `lab/results/20261009-1556-inversion-3036/check.md`.

**Reproduction** — clean tree + `work/patch.diff`: all five scene lines of `run5.jsonl` identical bit for bit; 4.88 s / 5.8 MB vs claimed 4.95 s / 5.9 MB. Every derived number in the dossier recomputes from the JSON (cone work/encounter 107→856 under ÷8 dilution, node 10.8→13.6, candidates ÷6.32 vs encounters ÷7.99). `predictions.md` predates `run1.jsonl`; run1 shows the disclosed probe bug (S2 `cross_enc=0`). Truth and cone are the crate's own calls throughout.

**Attack** — three scenes of my own on the same harness:
- C1 (e=0.9, detuned, transversal): node cert 0/305 misses — the cure holds at high e when crossing is transversal.
- C2 (exact tangency, a_B=2/e_B=0.5): node cert misses **292/1447 = 20.2%** despite its adaptive window ballooning 10×.
- C3 (near-tangent): **12/280 = 4.3%** misses.

The author's own pre-registered kill criterion for the cure fires at the tangential end; the crate's per-pair `sections` already models this as `Kind::Wide` — the group tier lacks that analogue. The negatives (phase cert 100% cross-group blindness, cone = all n_A·n_B pairs) held in every scene, mine included; the secondary rank-4 intra finding (1.4–6.4% maintained, up to 43% static) also reproduced.

**Why silver, not gold** — the hole and the dilution-tracking failure are real and directly on HANDOFF's top risk, but the deliverable cure is falsified outside transversal crossings, and the claim is contingent on the in-flight `b-coorbital-cert` build not already carrying a cross-group tier. Gold experiment named: a group-pair tier with tangential treatment (passage-overlap over the |Δr|<ρ band), zero misses at O(n) candidates, adjudicated against the in-flight build.

Working tree restored clean; no commits or pushes; only `check.md` added to the run folder.
