# predictions.md — written before probe.py runs

Data: quant-5022's published per-seed, per-cadence results (kdk method only; 1024-events/orbit
reference per seed; gates exactly as that run's `verdict.py` froze them: apsidal rate within 10%,
emax within 1.2×, maxdJ within 10× of its 64-cadence control). Seeds: T1 (a 0.55, e 0.05),
T2 (0.70, 0.20), T3 (1.70, 0.05), H1 (0.62, 0.30), H2 (0.48, 0.10, μ 3e-4), H5 (0.55, 0.60).
B1/H3/H4 stay judged-out (resonant/chaotic) exactly as the author ruled.

Question the probe answers: does a per-body ×2 cadence ladder, driven by one dimensionless
sensor, reproduce the per-seed minimum cadences — i.e. what any sensor rule can buy on these
hierarchical scenes, and is e alone a sufficient sensor?

- P1 (ceiling): at least 3 of 6 seeds pass below 64 events/orbit, so a per-body ladder's ceiling
  is ≥ 2× the uniform 64 in total kicks on these scenes. If fewer than 3, the uniform cliff binds
  per-body too and q-cadence's 4× must come from resonance-diverse or mixed scenes, not these.
- P2 (sensor): the per-seed minimum cadence is monotone non-decreasing in e0 (Spearman ρ = 1,
  ties allowed); it is NOT monotone in a0 (ρ < 1). If e0 also fails to order it, no single
  recorded number is the sensor and τ/detuning must be measured (q-cadence's brief is right to
  list them).
- P3 (held out): a threshold ladder on e0 fitted only on T1/T2/T3 predicts H1, H2 and H5's
  minimum cadence within one ladder step each. If it misses any seed by ≥ 2 steps, an e-only
  sensor is dead on arrival.
- P4 (binary beats graded): the min-cadences sit on the ×2 grid by construction, so a graded
  rate offers no extra pass on this data — stated as a check, not a prediction: every seed's
  minimum is a power of two (trivially true) but the fit residual of the ladder must be ≤ 1 step
  on all six seeds for the binary rule to be the right representation here.

Kill criterion for my dossier claim: if P1 fails, the library lesson "delete before you automate"
loses its cadence application (no savings to route); the run reports that as the negative result.
