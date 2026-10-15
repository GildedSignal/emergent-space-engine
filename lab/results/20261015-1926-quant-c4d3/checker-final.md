Working...
Check complete. **Grade: gold** — written to `lab/results/20261015-1926-quant-c4d3/check.md`, with three corrections to the author's wiki page.

**What I verified:**

1. **Reproduction** — applied `work/patch.diff` (two bench examples only), rebuilt, reran the decisive command: p50 4.43 µs, e-bands 3.42→8.33, grid and refusal pattern bit-identical to the dossier. Runner's regen had already exited 0 with matching numbers.

2. **Harness faithfulness** (in shipped code, not on trust): `ladder_ship` mints belt ships at `doll: 0`; `DollRec::root` gives `Unit::ONE` so `to_tube` is identity — the bench's key is bit-identical to `spec_binding`'s; `add_body` is exactly compile + catalogue insert + `bind_exact` + store; the wave's rekey (`tube_unit`) compiles the same keys for zero-gm ships. No DCE concern (per-key mean × n matches pass totals).

3. **Adversarial cases**, all past the author's domain: fresh seed 2026 → p50 4.55 (inside pre-registered P1); single-pass/no-min → 4.58 (+3%, method hides nothing); N=4×10⁵ → p50 9.52 µs, 2.08 kB/body, 831 MB peak — flatness and memory hold. Peak stayed well under 2 GB.

4. **Cross-refs at source**: b172's flight files really print `promotions 940718 promote_us p50 4.60` and `132061 … 0.54 s` — the corroboration is grounded. a669's "~30 µs a kick" really was a wave cost attributed to compile via a `from_state` path — the domain error this run corrects is real. Wiki open direction 4 really named this exact number as missing: novel, not a repetition.

**Two flaws found, neither gold-breaking:**
- The "~2.7× regression against the shipped promotion path" multiplier is mislabeled: 12.8/9.2 = **1.4×** the whole path; 2.9× is against the compile alone. Both operands were printed correctly; conclusion unchanged under every reading. Page corrected in place.
- **Missed domain**: under b172's retention cap 16,384, the belt re-promotes 940,718× per 132,278 kicks — promote-compile alone is ~52–56% of wave CPU, not ~7% (which holds only at natural cadence, 7.5–8.1% verified on the uncapped arm). The kill survives there too (12.8 vs 4.6 µs in-flight), but "wave = ~86–93% attendants" is not cap-invariant. Added as a checker caveat to the page.

Tree restored to base (patch reverted, only `lab/results/` untracked); no commits made.
