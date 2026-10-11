Working...
Check complete. `check.md` written to the run folder; nothing else there changed (regeneration used the dossier's own in-place commands; stored numbers verified bit-identical before overwrite).

**Grade: gold.**

What I did:

- **Reproduction** — full 20-run sweep from the dossier's commands, 58 s total. Every table number exact: A's −2.42 fit, B's 21,668 vs A's 14 evals at D=1e-5 (1,548×), C's slopes 0.83–1.00, D on A's curve, the behaviour row. The suspicious mtime order resolved: `sim.py`'s 22:46 edit added schemes C/D and is bit-compatible with the stored A/B JSONs; `jA64b` is the author's determinism re-run (numerics identical). `predictions.md` (22:40) precedes the decisive runs.
- **Controls audited** — oracle verified analytically (`jacobi1` is the exact PCR3BP invariant; the rotating-velocity identity cancels the barycentric correction exactly for a circular parent), `jacobi2` correctly rejected, A converges at ratio 4.0, Kepler drift re-verified independently (4.4e-14 round-trip).
- **Four adversarial axes of my own** — seed 999, μ=1e-4, e≤0.7 (apocentre 0.935, near the parent), 3× horizon. The walk reproduces everywhere (B slopes 0.65–0.96); A/D stay bounded; the admitted D@m=8 slope 0.37 is slow saturation, not an incipient walk.
- **Novelty** — probe 1 killed per-body steps wholesale; the new delta is the split (precomputed per-body cadence is *safe*, never tested before) plus the B12 slope-register spec. Queue top is indeed `q-b12-design`.

One correction the integrator should fold into the adopted wording: a precomputed **alternating** (state-independent) interval partially walks in my probe — slope 0.49 med / 0.73 p90, 16× worse D at equal rate. The dangerous property is cadence modulation correlated with synodic phase, of which state-feedback is the worst case, not the only case. The rule should read "uniform precomputed per-body cadence", not "precomputed". The kill and both adoptables (drop state-gated cadence; B12 registers the walk slope) stand untouched.
