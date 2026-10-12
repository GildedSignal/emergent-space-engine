Working...
Check written to `lab/results/20261012-1227-system-8685/check.md` — **Grade: silver**.

**What held:**
- **Exact reproduction.** 11 cells rerun from a clean compile are bit-identical to `work/`; `analyze.py` regenerates every dossier number. Belt/resonant W-sweeps verified from the author's CSVs (ϖ̇ up to 147% off; resonant ē 337–513% until W=π; seg8 aliasing 165 MADs, Jacobi 110× the floor). Predictions predate the decisive runs; failures honestly scored.
- **The kills are solid**: conjunction windows can't carry secular precession (non-monotonic in W, the W=0.25 pass is an accident), resonance needs its own clock, event-scheduled cadence doesn't walk Jacobi, and tick-quantized averaging aliases — sign-robust across my seg4/seg16 probes.

**What died under attack:**
- **The impulsive-regime win inverts at 64 seeds.** Against u4096-converged truth, ė deviations: u8 = 2.43, w0.5 = 2.78 (worse, with more kicks), u16 = 0.60 MADs. The 16-seed "3.6× over u8" and "matches u16" were median luck inside the author's own stated noise floor. Only w1.0≈u32 survives.
- **The "impulsive" scene never engages the SyMBA shell** (q=1.1875 vs 0.097); my shell-engaged probes (e₀=0.15/0.20) show no clock effect or degenerate. The conditional adoption of window-keyed cadence must not happen from this evidence.

**Net for the integrator:** a negative package that sharpens q-cadence — the window clock buys nothing measurable at matched count anywhere; keep the averaged term orbit-anchored, never tick-anchored. The belt/resonant kills largely re-confirm H0204/H0205. One experiment from gold: an orbit-anchored averaged kick that provably kills the subharmonic while closing the belt ϖ̇ break. Also flagged: the scene correction claimed to be "logged in predictions.md" isn't there, and the belt truth cell exceeds the "≤60 s" claim.
