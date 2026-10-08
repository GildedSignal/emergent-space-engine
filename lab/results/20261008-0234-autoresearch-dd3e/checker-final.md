Working...
Check complete. `check.md` written to the run folder; tree restored to pristine.

**Grade: silver.**

**Reproduced from a clean tree, my own builds of both sides** (base = reverted src + identical bench, final = patch applied, interleaved A/B):

| | base → final | digest |
|---|---|---|
| seed 1/7/23/3 pure kick | 36.2–36.5 → 28.9–29.1 µs (−20%, ~7.2 µs everywhere) | bit-identical, all 4 |
| adversarial: seeds 11/m16, 5/m64, 42/m4 sparse, 9/m8 dense | −6.6 to −7.3 µs everywhere | bit-identical, all 4 |

Plus 54/54 tests green, clippy clean on the patched lines, and the pre-registration order holds (`baseline.txt` → `predictions.md` → final binary → `heldout.txt`). The identity is structural, not approximate: `tau_event` caches the construction-time `decode` of the same immutable fields, `Bound.orbit` comes from that exact call. All four predictions held on my numbers too. Novel — `tau_event`/`readout_with` exist nowhere in history; the dead exact-key memo (dbd4add) is a different, cross-kick mechanism the author cited honestly.

**Why silver:** reproduced and adoptable in one trivial step, but a ~1.25× constant factor on the kick event (5–7% at settle) — short of gold's 10×/component-deletion/premise-kill bar. The dossier admits this itself. The gold experiment is named: the cross-body `(binding, tick)` memo for the three remaining same-tick decodes, measured at fleet scale and on the leaver-dominated kick population.

**What the author missed:** the 73%-leaver kick population was never measured (single-ship bench only), the +16 bytes/Binding memory delta was asserted not measured, the A/B base binary ran bench code absent from the patch (I closed it by rebuilding both sides), and `run.log` is empty.
