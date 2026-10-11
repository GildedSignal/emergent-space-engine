Working...
Check complete. `check.md` written: **Grade: silver.**

**What I did**

1. **Reproduced** — `python3 inspiral.py`: log identical, `inspiral-out.json` bit-identical, 43 s, 35 MB. `work/patch.diff` empty; predictions.md (11:19) genuinely predates the decisive run (11:38).
2. **Independently verified** the load-bearing wiring: Peters–Mathews flux via my own time-domain Kepler method (5.1e-7 at e=0.3); `flux_G` by exact algebra from Peters' da/dt, de/dt; the cubic/Vieta/circular-family algebra; the wall closed form a_wall^{5/2} = (192π/5)νF̃(e)/ε̄ against measured walls; the 1PN+tail coefficient against the standard Blanchet value; circularization-before-plunge at ν=0.05 and from a₀=1000M. Novelty confirmed — first radiation-reaction numbers in the repo (law.md:35 names the generator unclaimed; HANDOFF #4).
3. **Three attacks landed:**
   - **`circ_L` is wrong by √a** (coded √(a/(a−3)), true a/√(a−3); the author's own `EL_from_ae` e→0 limit proves it). The headline P9 "spurious e = 0.81" was measured on a plunging orbit born off-family; with the corrected L it is **0.0000** (+0.8% L mismatch at ISCO) — the author's pre-registered prediction had actually *held*, and the artifact was promoted into a false design rule ("the two-flux wiring is inconsistent").
   - An **in-domain** birth (ν=0.25, e₀=0.9, a₀=110M, p=20.9M) has its 1% wall ≥15× outside the separatrix — the author's own pre-registered kill line (≥5× at ν≥0.01), never applied.
   - Handoff-band edges are numerically soft (11.57M vs 6.78M vs 6.23M under tiny perturbations), and "690 re-keys"/"0.005 per orbit" are not regenerable from the shipped code (measured: 642 re-keys, 1.34e-3/orbit).

The physics core is real and adopted-grade; one line of code plus a rerun and honest re-claiming separates it from gold. Folder left otherwise untouched (JSON verified still bit-identical; my `__pycache__` removed).
