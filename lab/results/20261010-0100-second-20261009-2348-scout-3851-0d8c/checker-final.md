Working...
Check complete. **Grade: gold**, written to `lab/results/20261010-0100-second-20261009-2348-scout-3851-0d8c/check.md` (only file changed; scratch dirs removed).

**What I did, in evidence order:**

1. **Reproduction** — `run-all.sh` in a clean copy: `val.json` and `analysis.txt` byte-identical to the author's, exit 0, 258 s, every command < 60 s, memory trivial. All 144/144, 127/144, 124/144, 142/144 and quantization numbers print from shipped code.

2. **Pre-registration** — `predictions.md` mtime predates every results file, the dossier, and the final regeneration log; 6/8 held, 2 failed and honestly reported (P6 chan2, P8 no gaps → converted into the ruin-speed finding).

3. **Independent physics** (no author code in the Riemann path) — my own sympy Schwarzschild tensor reproduces their `R6` pair components exactly, and my own frame + contraction reproduces all three closed channels (Λ₁₁, Λ₃₃, and the shear Λ₁₃ with its u_r sign) at machine precision; circular geodetic anchor −2π√(1−3u) hand-verified. One scare along the way (my wedge replication off by 0.67×) traced to my own transcription bug — their transport = closed = my direct contraction exactly.

4. **Attacks** — e = 0.9 (chart = truth at 2 of 3 radii, near-threshold fragmentation at the third; avg ruin overstatement grows to 4.4×), untested cell (10⁶, 0.6) holds 18/18, and the Ω-ceiling probe: at e ≤ 0.6 the leak above 16×Ω_r is ≤ 0.09/orbit, but at e = 0.9 strong bands (> 2/orbit) live above it — the main adoption boundary the dossier understates.

**Verdict:** the scout run's named gold-lock experiment, done and verified — the coupled monodromy chart (4-column quantized table per (E, L) tube) is the certificate; the frozen scalar one misses 142/144 bands. Missed by the author: the e-boundary/ceiling quantification, the 1.67× circular gloss on "1.8–3.6×", and dead code in `floquet2x2`.
