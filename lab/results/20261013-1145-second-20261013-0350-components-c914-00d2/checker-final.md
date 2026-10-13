Working...
Check complete. **Grade: silver** — written to `check.md`, with the author's wiki page corrected in place.

## Verdict summary

**Reproduced (everything measurable):**
- Applied `work/patch.diff` myself; `mk_arm_bench.sh` regenerates the harness **byte-identical** to `work/` — kernels verbatim.
- TCG wall (my own runs): soft 133.35–133.93, asm 93.97–94.04, newton 387.30–389.70 ns/div → **2.9×**, inside every dossier band; 0 mismatches.
- Instruction census: my streaming full-histogram census returns **bit-identical totals** to the author's (8,351,619 / 12,435,481 → **1.489×**); closure hardened at N=6↔12 (170.08 vs 169.91, 0.1%).
- x86 controls and the known d=3 Newton failure regenerate.

**The attack that landed (from the run's own frozen data):** `census2.py` prints only `most_common(14)`. The full histogram of the *same* census shows `soft` executes **`udiv` 2.796/div** (rank ~23, hidden by the cutoff) plus `bl` 2.0/div; static disassembly of the routine `__udivti3` calls shows **8 static `udiv` sites**. The dossier's "zero `udiv` / multiply-only / same mix / no divide instruction to remove" — the structural mechanism by which the kill was generalized to the target architecture — is a truncation artifact. The author's own pre-registered P2 ("1–3 hardware udivs") was right; the post-hoc reading overrode it. With ~2.8 `udiv`s (~7–9 cycles on M1) on one side and +83 instructions on the other, the 1.49× instruction count cannot bound the silicon ordering — the M1 re-measure **decides** the lever, it doesn't confirm its death.

**My other attacks (two outside the author's range):** Newton still loses at d ∈ [2^62,2^63) (3.3×), d ∈ [1,2^20) (8.9×), and general dividends (3.2×) — the cost ordering is robust; only the mechanism claim breaks.

**Not gold** (headline contradicted by its own log — the lab's explicit grade-killer), **not lead** (reproduced, on-goal, novel instrument). The gold-making experiment: wall-time the three variants on real arm64 silicon. Page corrected at all four overstating spots; tree restored; nothing else in the run folder touched.
