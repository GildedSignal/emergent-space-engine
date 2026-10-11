Working...
Check complete. `check.md` written; tree restored to clean (only untracked `lab/results/`).

**Grade: silver.**

**Reproduced exactly** — all six dossier commands, every count field bit-identical to `decisive-a/b.log` (growth, speed, anchor 831/831, knee k=206442, RSS 1,057,428 kB at 3×10⁷); speedup 12–49× on this loaded box (author claimed 19–40×). Predictions were frozen before the decisive runs (mtimes verified) and `decisive-a.log` contains the narrated b16 catch.

**Why not gold:**
- One held-out invariant ("miss=0 at all widths") failed on the decisive run; root-caused to a genuine sign slip, fixed, re-run clean — H0183-compliant and disclosed, but the corrected bound was validated after seeing held-out data.
- My adversarial mixed doll (a∈[0.5,3], the dossier's own named-but-untested case) **falsifies the unscoped "provable superset" at b30**: 268k–578k float candidates rejected (15% on mixed-hot); whole-belt containment confirms 1.0M/4.6M float pairs missing. Mechanism (instrumented): with vmax>1 the `shift≠0` path scales the V/W side by c² instead of 1/c² — a 16× systematic error on a branch dead in every belt the harness can generate (a∈[1,1.5], e≤0.5 ⇒ shift=0 always). At b16/b24 the u-grid saturates at span>1: still safe, but growth 1.86 vs the ≤0.6% shape.
- Within the game's belt family (U-span<1, vmax<1) everything passes, including my fresh seeds, keys=64, tiny-ρ and narrow-doll probes.

**Gold is one experiment away:** fix the shift direction (`rs << −shift` with round-up), fence per-doll width (bits from u-span and vmax), re-run mixed-belt growth + containment at miss=0. The 40× constant on the per-kick re-scan — board risk #1's measured hot path — is real and worth adopting once fenced. Novel on the record; `Body` is 80 B, not 88 (argument unaffected).
