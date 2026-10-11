# Predictions (written before the cadence sweep)

Question: where is the fixed-cadence knee of the motion-law-v2 plane, judged by the frozen
gates B12–B14, B17 (`behave --law plane --plane-step N`, N = log2 kicks per radial period;
shipped default N=7 → 128 kicks/orbit)?

Prior data (pre-v2 plane, cited in lab/lenses/q-cadence.md): 8/orbit held behaviours except
at e=0.3 (16) and inside resonance bands (no rate ≤64 matches a librating truth); B17 on v2
passes at N=4–6, times out at N=7 (law.md). H0215: on v2, B13 is 60/64 at the default with
all failures marginal.

Theory: the WH split error is O(h²) in the step, so each halving of cadence quarters the
behavioural error; thresholds are 1% (B13), 10% apsidal (B14), 25% e-pump (B17).

Held-out cases (not tuned on; the sweep at N=7,6 is the known/control end):

1. **B13 (assists, 1% energy/ang-momentum):** holds (≥63/64) down to N=3 (8 kicks/orbit);
   breaks at N=2 (4/orbit), with errors ~4× the N=3 errors per halving (h² scaling).
2. **B14 (Hill moons, 50 planet orbits):** holds to N=4; at N=3 the e₀≤0.3 births near
   0.9 R_H start to misclassify (the prior plane needed 4–6 through 0.4 R_H).
3. **B17 (resonance, weak field):** passes at N=4,5,6 (known); at N=3 the e-pump ratio
   leaves [0.8, 1.25] for μ = 3×10⁻³ (resonance is the sharp one; prior data says no fixed
   rate fixes the band, so the knee should be highest here). At N=2 it fails outright.
4. **B12 (Jacobi; statistic known miscalibrated — evidence only):** the error population's
   median scales ≈4× per cadence halving; the exponent stays ≤ 0.2 wherever the gate's
   pass/fail is meaningful.
5. **Negative control:** N=1 (2 kicks/orbit) fails at least B13 and B17 decisively
   (not marginal). If nothing fails at N=1, the gates do not see cadence at all and this
   sweep measures nothing (a control that cannot fail is a broken instrument).
6. **Cost:** kick count per orbit is 2^N by construction; per-kick µs (kick bench) is
   cadence-independent within noise, so engine cost scales as 2^N exactly. If the knee is
   N=3, the shipped default wastes 16× on the engine's dominant cost for these scenes.

What would make the knee question moot: if the gates fail at N=7 (the default) too — then
cadence is not the plane's problem on v2 and the bottleneck is elsewhere (the encounter
representation, per H0214).
