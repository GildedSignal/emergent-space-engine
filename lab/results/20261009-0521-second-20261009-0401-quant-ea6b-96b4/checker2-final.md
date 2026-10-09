Working...
**Grade: silver** — written to `lab/results/20261009-0521-second-20261009-0401-quant-ea6b-96b4/check2.md`.

**Reproduced from a clean tree at `a838a28`** (patch applied/reverted myself; tree left clean):
- All deterministic fields **bit-identical**: m2000 digest `ca74ff5a7b71f200`, memo q-hit 0.970988618611917, 260 shapes / 8962 rebinds, ships_mean 231.7017, cadence 0.0132239, population 9180 legacy + 12 clock (9137+4+39 dolls, 353 made), refused 0.
- Stage shares within 0.3 points: rebind 84.5–84.6% (bench), 84.8% (engine phase), clock path ~59%; cold/warm 1.39× with rebind 1.20×, readout 2.82×, forces 3.24×. Units audit exact from the author's record; capacity arithmetic gives 9.54×10³/core exactly.
- Predictions genuinely preceded the decisive runs (file times 05:25→05:31→05:36); 6/7 held, the mean-band failure honestly reported.

**My adversarial additions:**
1. **Clean-binary m2000 digest control** — the author only proved patch inertness at default args; I proved it at the decisive workload (replay and plane digests both identical). This matters because the patch contains an **undisclosed 9-line engine behavior change** (crash scheduling → immediate death in `kick_clock`) inside a patch the dossier calls "instrumentation only".
2. `--members 500` is bit-identical to m2000 — the scene is handout-rate-bound, so the "2000 target" framing is misleading.
3. Fill-phase sweep (s10/s45): rebind share portable (83.8–86.3%), but cadence drifts 1.1–2.1×10⁻², so 9.5×10³ ships/core is a mid-fill point in a ~5×10³–1.2×10⁴ band.

**Why silver, not gold:** a held-out prediction failed (explicit gold clause), and the hidden hunk is a disclosure defect — though digest-proven inert, so no number is contaminated. Gold path: timers-only patch, steady-state filled-fleet cadence, and a real law-v2 clock-body bench (12 accidental samples today).
