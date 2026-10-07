Working...
**Grade: gold** — written to `check2.md`. The run folder is back to the author's files plus my report; scratch builds removed.

What I did as the blind second checker:

**Reproduced (all from the dossier's commands, clean build):**
- Correctness: `corner` OK (4194304, ids 0–7); F diffs at N=2/4/16/64 clean; full A–S × 2 sizes × 3 seeds battery clean; long sparse `S 2²⁰ 300k` clean.
- Record regenerates: the three stored 97bf digest rows byte-identical for both heap and wheel.
- Steady-state ratios: E 2²⁰ **2.5×** (stored 2.4×), E 2²² **2.5×** (2.4×), E 2²⁴ **2.07×** (median 2.23×), S 2²⁴ **2.7×** (2.9×), F 2¹⁶ **heap wins 2.38×** (2.39×) — every digest matched, so heap and wheel provably delivered identical streams.

**Adversarial:**
- Rebuilt the **pre-fix** wheel by reverting the three staleness-aware call sites to raw `over.first()`: it fails exactly as recorded (corner 3145728 vs 4194304; F diverges) yet still matches the stored digests — the bug was real, the regime was as claimed, and the fix touches no old-correct path.
- My own diff battery beyond the author's (n=1 for F and D, D/F at 65 536 ×300k, E/S long): all clean — the one-live-slot invariant holds.

**Novelty:** the parent (silver, `59f154f`) named this exact experiment to gold; the new content is the fix, the steady-state methodology, and the quantified all-far inversion. Prior-art lead is `original-research-report.md:643`, first measured by the parent.

**The gold basis:** the parent checker's pre-committed condition — ≥2× at DRAM scale with correctness closed — holds in my independent reproduction (marginal at E 2²⁴: 2.07×), plus the measured premise correction that the wheel is the wrong structure beyond W. Named gaps in the report: thin E margin, `deliver`'s drain+sort still unsampled for p99, no W-sensitivity sweep, arbitrary storm mix, the one-shot 6× row still in the table.
