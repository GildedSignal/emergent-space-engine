# Predictions — 20261010-1152-dynamics-ad35

Written after tuning on **one** configuration only (mu_p=0.005, R=5.27, i.e.
eps=3.4e-5, n in {4,16,64}, 4 seeds, 100 orbits; see `probe.json`). The tuning
told me: Jacobi-constant error is a bounded attractor at all tested cadences
(gJ~0), z-error grows linearly (gamma~1, secular frequency offset), map-twin
separation grows identically at every cadence (lambda~0.013-0.06/orbit, origin
unresolved). Everything below is a prediction on cases NOT tuned on.

Decisive grid: R=5.27, mu_p in {0.002, 0.005, 0.02, 0.05, 0.1, 0.2},
n in {2,4,8,16,32,64,128}, 6 seeds, 150 orbits.
Held-out: mu_p=0.035 (R=5.27), and mu_p=0.02 at R=4.0.

Notation: rho = relative precession-rate error vs truth (systematic part);
gz_end = log-log slope of the eccentricity-vector error in the late window
(1 = linear drift / systematic, 0.5 = random walk / diffusion);
d2_end = map-twin end separation; dtwin = truth-twin end separation.

## P1 — the systematic error obeys rho ~ C mu n^-2 (C from tuning: ~2000)

- (mu=0.2, n=128): rho = 2.5%; (mu=0.2, n=32): rho = 40%.
- (mu=0.035 held out, n=32): rho = 7%, at n=16: 28%.
- The rho=10% border sits at n* ~ 143 sqrt(mu): mu=0.2 -> n*=64,
  mu=0.05 -> 32, mu=0.02 -> 20, mu=0.005 -> 10.
- Measured rho within 2x of the law everywhere, border within 1.5x.
- If rho instead scales like mu^2, or n^-1, or n^-3, P1 dies.

## P2 — a diffusion border exists only at strong tide and low cadence

- At mu >= 0.05 and n = 2 (maybe 4): gz_end ~ 0.5 (walk) with e_err at least
  3x the systematic estimate -> behaviour corruption, not phase lag.
- At mu <= 0.02: gz_end ~ 1 for ALL n >= 2 (pure drift, no diffusion).
- Sharpness: at mu=0.2, gz_end goes from ~0.5 at n=2 to ~1 at n=8.
- If gz_end ~ 0.5 appears at mu <= 0.02 as well, or if the transition is
  gradual (no n with gz_end jumping between 0.5 and 1 within a factor 4),
  P2 dies.

## P3 — the twin divergence is the system's own chaos, not the map's

- dtwin (truth-twin, 150 orbits) for seeds 0,3 is >= 1e-7 at mu >= 0.02:
  the physical system is chaotic at these tides.
- d2_end matches dtwin within 3x for every n >= 8: the map inherits
  physical chaos and adds none of its own.
- At n <= 4, mu >= 0.05: d2_end >> dtwin (>= 100x): there the map does
  inject chaos.
- If dtwin stays at the perturbation scale (<1e-9) while map twins grow to
  >=1e-6 at n >= 8, P3 dies inverted: the growth is numerical.

## P4 — the border is nonuniform across seeds

- At the rho ~ 10% border, max/min seed ratio of rho >= 3 for at least one
  mu (islands / phase dependence), so single-seed cadence tuning misleads.

## P5 — held-out distance R=4.0 at mu=0.02

- rho(R=4.0, n) = rho(R=5.27, n) x (5.27/4)^3 = x 2.28 within factor 1.5:
  the driver is the tidal ratio eps = mu/R^3, not mu alone.

## P6 — controls on both sides

- Negative: (mu=0.2, n=2) dz_end >= 1e-2 (gross corruption).
- Positive: (mu=0.002, n=128) dz_end <= 1e-8; gJ ~ 0 (bounded Jacobi
  attractor) at every (mu, n >= 4).
