Grade: gold

**Abstract.** f790 closes de7b's two named misses and de7b's claim now stands measured, not inferred. Reproduced from `work/patch.diff` in a clean tree: 98cb's actual `BELT_SPLIT` patch stretches both combs 8× together — h p50 112,565 = 8.0005× shipped, 9,700/9,700 welded pairs, every identity 1.0000, 4 events K,B,K,B, rate 0.1250× shipped — and seeds 2/3 hold to the digit (14,075/14,073). de7b's arms 6/7/8 byte-reproduce from the published branch. Ledger recomputes: 79.71→3.85 M1 riding cores, 15.67-core pinned floor dead, S* = 19.9×. My adversarial flights extend the domain: plain lever 4 bit-identical to the split arm, seed 42, effective lever 3 — all weld. Nothing to adopt in code; the design consequence (split ≈ 20× closes the belt ledger) hardens to measured.

**Reasons.**

1. **Reproduction.** The runner's `regen.sh` exited 0 and every number in the dossier's table matches `regen.log`; the author's own regen (`regen-log.txt`) and the runner's agree byte for byte on all 24 `combs:` lines. I re-applied `work/patch.diff` to the clean tree, rebuilt, and flew three adversarial cases of my own (below) — the instrument and patch behave exactly as documented.

2. **Record regeneration, verified against the published branch.** From `remotes/origin/claude/lab-20261017-1149-fermi-de7b`: arm 7 seed 1's scan/end/ladder lines are byte-identical to de7b's `arm7.txt`, and arms 6/8's ladder lines to `arm6-scan2.txt`/`arm8.txt`; the only diffs are the disclosed instrument extensions (`seed=` field, mixture counter, build seconds). This doubles as the toggle-off control: patched tree, toggles unset, shipped numbers byte for byte.

3. **Predictions.** `predictions.md` (12:45:51) precedes every logged flight (12:50:14+). S1 held (seeds: h within 0.03% vs the ±2% bound, 9,700/9,700, identities 1.0000, 4 events, dead 0); S2.4 held (100% split class vs the ≥90% floor; h 112,565 vs predicted 112,570±60); S2.5, the decisive one, held with the pre-registered falsifier (B/2h ≈ 0.25, boundaries outnumbering kicks ~8:1) absent in all 9,700 bodies; S3.8 controls held to the digit. The two misses (S2.6 window labelling, S2.7 guard raise after two disclosed failed attempts) are honestly reported and immaterial to the substance.

4. **Adversarial cases (mine, each outside the author's tested set).**
   - **Plain `step_log2=4`, seed 1** — lever 4 had only ever been observed through the split path. Genesis h distribution is *bit-identical* to the split arm (112,565/107,003/115,784), 9,700/9,700 welded, identities exact, 4 events: the split is a pure step lever on the bulk, and the "effective lever 4" framing is measured, not assumed.
   - **Split, seed 42** — the split flight was seed 1 only. Holds: h p50 112,595, 9,700/9,700 welded, identities 1.0000, 4 events, dead 0.
   - **Split at base lever 6 → effective lever 3** — the octave below the tested 4–9 family. Holds: h p50 225,130 = 8.0002× the lever-6 h, 9,700/9,700 welded, identities 1.0000 (p01 0.9985 — the same quantization spread the author reported), K,B,K = 3 events by 3.11 intervals, boundaries/kicks 0.9998, dead 0. The welding family now spans seven octaves of the effective lever, four seeds, and both paths (plain and split).

5. **Internal consistency.** The split distribution is the shipped one stretched ×8.0005 with the same relative spread (p01/p50 0.9505→0.9506, p99/p50 1.0285→1.0286) — an exact stretch, not a resample. Events p01 = 3 at 460,400 gs matches 4h > end for the top ~1% (h p99 115,784 → 4h = 463,136). Genesis plans hold Kick items only (0 boundaries) — the boundary is planned by the kick itself, which is the mechanism claim. `ledger.py` arithmetic checks by hand (79.71 riding at S=1; 15.67 pinned floor; S* = 79.71/4 = 19.9; anchor rates 0.1250/1.0000/4.0003×), with constants page-cited and disclosed as such.

6. **Novelty.** The canonical `lab/wiki/kick-cadence.md` (updated by de7b's publication) held only the anchor inference ("`BELT_SPLIT` is a step lever by 98cb's own 8.000× first-kick anchor"); the proposed page replaces it with the direct flight, adds seeds 2–3, and the runs line. Nothing in `docs/HISTORY.md` holds the direct-flight result. This is the named-experiment closure, not a repetition.

7. **Goal fit.** The board's furthest gap (bodies: 28 vs 10⁹, the belt's 10⁹ CPU ledger). The flight decides riding (3.85 M1 cores at S = 20.7) against a 15.67-core pinned floor no split could touch — the whole ~20× consequence rested on this composition, and it is now measured on the real patch. PRINCIPLES #1 ("the best part is no part" — the boundary-cadence component stays deleted) and #20 (behaviours over many seeds — the welding now has four seeds and seven lever octaves, not one).

**What the author missed.**
- `arm7.txt` is cited in the Reproduce section but absent from the folder; its content is regenerable (regen.log holds it and it matched de7b's branch artifact byte for byte), but the record set is incomplete as delivered.
- The rtf-12,000 byte-identity claim has no saved artifact from the author's session (both guard-hit attempts were discarded); determinism is nonetheless corroborated by the two independent regen invocations and my flights at different box load.
- The mixed-belt case remains unmeasured (disclosed in the lens): this scene is 100% bulk at `BULK_HILL` = 4, so per-class welding on each class's own h is still inference; a belt whose inner edge sits within 4 Hill radii of a source band is the next falsifier, and it is cheap to fly with the same instrument.
- The M1 boundary cost (7.17 µs) is an x86-ratio inference — disclosed, unrunnable here, and cost-independent for the riding/pinned branch structure.

The page (`wiki/kick-cadence.md`) is faithful to the evidence as it now stands: every f790 number matches the logs, and the domain claims are scoped. No correction needed.
