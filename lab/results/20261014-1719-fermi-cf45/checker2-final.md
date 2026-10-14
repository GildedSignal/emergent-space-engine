Working...
Check complete. Verdict: **gold** — written to `lab/results/20261014-1719-fermi-cf45/check2.md`.

**What I did (independent of the first checker):**

- **Reproduced bit-identically**: applied `work/patch.diff` (only adds `examples/cadence.rs`) to a clean tree, re-ran seed 1/N=4000 — every physics number matches (interval p50 2.814×10⁴ s, kicks +101,624, events +205,339); `compose.py` output byte-identical, all products re-derived by hand.
- **Verified the mechanism in shipped code myself**: `step.rs:601` routes doll-0 ships to `plan_clock` → `ext::constants`, documented as `Δs = 2^−k·P_D/f'(c)` per the doll's shortest secondary; `step_for` is unreachable for belt ships. `ladder.txt:123` confirms the 88-day record; Cinder's spec is Kepler-consistent with the measured 77.24 d.
- **Three adversarial cases, all held**: N=12000/seed 7 (3× the largest tested N, fresh seed — constants unchanged at the next decade); a wave-bracket probe (belt events/body 0.008→0.894→1.000 across 13.3–15.3 ks, first kicks at interval/2, matching taleb-6138's window); a step_log2=5 dial probe (interval exactly 4×, verifying the octave anchor on shipped code, not extrapolation).
- **Novelty**: the mechanism was on record, but the live nladder best carried effb's opposite "code-verified 2⁷/P_own" law feeding the 10⁹ ledger and the step_log2 wiring decision. This run arbitrates the contradiction, corrects the constant, and recomposes — a premise correction, adoptable at zero code cost.
- **Predictions**: genuinely pre-registered (17:31 vs outputs 17:45+); discriminating ones held, misses disclosed (the locals bug honestly killed, not quietly dropped).
- **Page**: faithful; I corrected one overstating Runs line in place ("bill corrected 24×" → the *law* corrected 24× at the plane's belt; effb's 1–2 AU core numbers move little). No topic closure — the two pre-existing 16:31 merge conflicts remain, correctly left unresolved.

Tree restored clean (probe files removed); nothing else in the run folder touched; no git operations. Missed items named for the author: the garbage locals lines archived in raw outputs, the 2.1-divisor vs 2-kick counter inconsistency, the "−0.006" slope not derivable from printed means (I get −0.012; immaterial), the inherited cost arms behind the 148× headline, and the un-run P_D-rebind probe.
