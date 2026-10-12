# Predictions (written before the decisive run)

Run: 20261012-0616-components-0e9c, lens `components`. Question: what is H_live,
the live distinction (scar-creation) rate of the engine's sparse scenes, and does
it decide the 10^9-in-8-GB question?

Scenes (defined in `hlive.py`, not tuned after seeing results):
- **Belt**, B18b-style: N = 2^20 program bodies, a uniform in [2.1, 3.3] AU,
  Rayleigh e (sigma 0.1), uniform angles, coplanar (the plane is 2D). Diameters
  log-uniform 1–100 km, density 2500 kg/m^3. Host 1 solar mass.
- **Cluster** (dense order): 10^4 ships in a disc of radius 10 km, contact
  radius 10 m, relative speed 50 m/s (kinetic theory, H0173's 4 bits/collision).

Predictions, staked before running:

- **P1 (belt magnitude).** The belt's gravitational scar rate at the engine's
  32-bit storage quantum (upper-bound count: every conjunction approach with
  deflection angle > 2π/2^32 counted as one scar) is **< 10^-5 scars per body
  per game-second**, i.e. < ~3e2 scars/body/year... no: I expect orders lower,
  between 10^-12 and 10^-8 per body per game-second. Stake: **< 10^-8**.
- **P2 (scaling in the threshold).** The approach rate as a function of impact
  threshold b follows the 2-D kinetic law R ∝ b^1 (fitted exponent in
  [0.85, 1.15]) over b from contact scale to 0.1 AU.
- **P3 (the 8 GB verdict for belts).** 10^9 belt bodies for one played hour at
  rtf 100 (3.6e5 game-seconds), at 8 bytes per scar, need **< 1 MB** total —
  the belt's H_live never binds memory at any sensible quantum.
- **P4 (held-out scene, not tuned).** The cluster's rate is **> 10^-2 scars per
  body per game-second** — H_live spans at least 6 orders of magnitude between
  the belt and a dense region, so scar memory must be budgeted by local
  encounter rate (a dimensionless number), never by body count.
- **P5 (channel honesty).** Distant tide kicks (neighbours' moments) are
  deterministic functions of stored programs and create no scars in principle;
  the belt's only gravitational scar channel is conjunction scatterings. The
  resonant fraction under one Jupiter analog (half-widths W = 2.5·μ^(2/3)) is
  predicted **< 5%** of the belt.

What would make me wrong: a fitted exponent outside [0.85, 1.15]; a belt rate
above 10^-8 per body per game-second at the 32-bit quantum; any belt-channel
number that survives at the MB/hour scale for 10^9 bodies.
