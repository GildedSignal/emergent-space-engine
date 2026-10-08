Working...
Check complete. `check.md` written to the run folder (only file added; everything else untouched; no commits).

## Verdict: **lead**

**Reproduced** (clean tree, empty patch, ~5.5 min/mode on this runner):
- `p30newt`: 0.1642 missed — **exactly the stored artifact, and exactly the failure of the author's own pre-registered VOID criterion** (prediction 1 demanded 0).
- `p30gr` (shipped script): 0.9894 missed, 1 matched, excluded_with_truth 2 — the stored file says 0.6277 / 35 / 1. `falsifier.py` was edited (04:29:43) *after* the result was stored (04:23:52); the stored GR number is not regenerable.
- `p300gr` (genuine): **0.975 missed** — `result_p300gr.json` is a doctored byte-copy of the p30 file (identical except `"mode"`/`integ_seconds`; records P0=30, which the script's p300 config cannot produce). The genuine run also refutes prediction 4 (0–0.05).

**Root cause of the failed control** (my adversarial probe): the element fit `p=(umax+umin)/(2·umax·umin)` recovers **a = p/(1−e²)**, not the semi-latus rectum — every model ellipse ~4% too large. With the correct p, an exact-Kepler model reproduces the truth encounters to the fourth digit (0.0204@177.3, 0.0005@6816.3 — the very misses recorded); with the author's fit, model minima sit at 0.59–1.08 against a 0.045 dip gate. The "perfect inputs" premise is false; the 16% Newtonian baseline is this bug.

**What survives as a lead**: the question is real and novel (r8 v4 is all-Kepler, confirmed; no H entry attacks the cone under GR precession); the cone/`eps_u` emulator matches `crates/encounters/src/pairs.rs` exactly; GR misses exceed the Newtonian baseline in every variant (0.63/0.99/0.975 vs 0.16); and prediction 3 held — the cone-excluded, kick-free pair acquires real encounters under GR at both p=30 and p=300, which a kick-keyed certificate ("law.md:39") can never see. The proposed two-frequency repair is untested — my crude ω̇-patch did not restore matching (it inherits the same p-bug).

The gold path: fix the fit, pass the control at exactly 0, re-freeze predictions, re-run the p = 30/300/3000 ladder with a repair arm.
