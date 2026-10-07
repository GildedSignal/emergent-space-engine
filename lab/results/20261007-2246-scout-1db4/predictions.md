# Predictions — 20261007-2246-scout-1db4 (written before the decisive sweep)

Calibration used only: scout-2098's published frontier (moons hold B14 precession at 4–6
kicks/orbit through 0.4 R_H) and system-27ce's belt floor (8). No case below has been run by me.

Hypothesis under test (the "forcing clock" rule): the minimal cadence N_min (kicks per radial
period, power of two) is set by the fastest forcing harmonic of the perturbation whose amplitude
exceeds the behaviour tolerance, sampled ~4–6 times per period — i.e. by the perturbation's own
clock (synodic + epicyclic content), NOT by the orbit, NOT by the tide strength. Local numbers:
s_syn = Ω_syn/Ω_body, e, μ, detuning from resonance. Prior art: Aarseth/Makino and Pham–Rein–
Spiegel 2024 (step from the force's variation), GROMACS Verlet-buffer tolerance, Nyquist.

Scene: planar elliptical restricted three-body, exact Kepler drift + DKD tide kick at 1/n of the
body's radial period; reference n=256 (512 control on M1/B3). Bars (gate stand-ins): B14
precession relerr ≤ 10% + bound/escaped match; B17 pump ∈ [0.8,1.25], libration amplitude ≥ 0.8,
regime match; error type: ϖ residual exponent ≤ 0.2. N_min = smallest power of two in [1,128]
holding all bars, median of 8 seeds.

| Case | Setup | Prediction (rule) | Basis |
|---|---|---|---|
| M1 | moon f=0.30 e=0.10 μ_p=1e-3 | N_min = 4 | s_syn ≈ 1 (calibration) |
| M2 | moon f=0.30 e=0.30 | N_min = 8–16 | epicyclic harmonics ~n_max(e)≈2–3× more |
| M3 | moon f=0.30 e=0.05 | N_min = 4 | harmonic content below tolerance |
| M4 | moon f=0.40 e=0.10 | N_min = 4–8 | s_syn still ≈ 1; margin from stability edge |
| M5 | moon f=0.50 e=0.10 | N_min ≥ 8 or unstable (escapes vs ref) | near the Hill wall |
| M6 | moon f=0.30 e=0.10 μ_p=1e-4 | **N_min = 4, same as M1** | s_syn is μ-free at fixed f; tide 10× weaker but tolerances are relative. DISCRIMINATOR: if N_min moves ≥ 1 octave, the tide strength τ binds, not the forcing clock |
| B1 | belt a=0.510 e=0.05 (s_syn=1.74, between 3:1 and 5:2) | N_min = 8 | N ≈ 4–6 × s_syn |
| B2 | belt a=0.800 e=0.05 (s_syn=0.40, far from all resonances) | **N_min = 4** | s_syn < 1 → the orbit itself is the clock; would show system-27ce's floor 8 was resonance/e contamination |
| B3 | belt at 2:1, detuned 1W outside (a=0.6352), e=0.02 | N_min ≥ 32 or unattainable | resonant harmonic large, slow libration; cadence expensive near the band edge |
| B4 | belt at 2:1, detuned 3W outside (a=0.6457), e=0.02 | N_min ≤ 16 | back on the synodic clock |
| B5 | belt at 3:2, detuned 1W outside (a=0.7716), e=0.02 | N_min ≥ 16 | same mechanism as B3 |
| B6 | belt at exact 2:1 (a=0.6300), e=0.02 | **no n ≤ 128 holds B17 (regime/pump)** — the rule must REFUSE (escalate to the resonant law), matching dynamics-a9c2 | libration needs phase feedback, not cadence |

Also predicted (error type): at N_min the ϖ residual vs reference is bounded (exponent ≤ 0.2) on
every case; a walk (exponent ~1) appears only below N_min — cadence error is aliasing, and the
right cadence turns it off, it does not average it away.

Kill criteria for the hypothesis: M6 ≠ M1 (τ binds), B2 = 8 with clean far-from-resonance
geometry (orbit clock, not forcing clock), or B3/B4 needing the same N (no resonance effect), or
no single (K, s_syn, e) combination predicting the moon AND belt surfaces within one octave.
