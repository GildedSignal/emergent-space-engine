# Predictions — 20261018-1237-dynamics-9dbb (order-boundary: the seam map's walk class)

Written after smoke (depth 64/256 on a 12-config subset + the twin pair), before the
decisive run (48-chain grid at depth 1024, 4 deep arms at 4096, twins at 8192, 3
retrograde arms at 1024). Smoke showed: e=0.5/p=2^21/phi3 walks k by EXACTLY −13 Q48
ulps/crossing for 255 crossings, w frozen, both w0 twins bit-identical; circles
(e=0, p=8M) walk −26k..−33k ulps/crossing, 0/63 sign flips.

The page's standing read ("bounded, not compounding — but never recovering") was
measured on the position sample, whose radius is sub-2⁻²⁰-invariant (b9c8's dr_rel
floor: integer-scaled, reads 0 below 2⁻²⁰) — the position drift is bounded by
GEOMETRY (a point on a nearly-fixed-radius circle cannot leave the diameter). The
columns (k, w) are the real degrees of freedom.

- **P1 (ratchet class).** Every chain that walks at depth 64 has a one-signed k walk
  at depth: ≥ 90% of crossings carry the median sign, and the rate does not decay:
  median dk over n∈[512,1024] within ±10% of n∈[16,512] for the exact-translation
  class (all dk equal). No chain's k walk saturates or reverses by depth 8192.
  Expect: e>0 classes near −1..−13 ulps/crossing; e=0 classes at −1e4..−4e4.
- **P2 (no ω-limit in practice).** No chain that is walking at depth 64 closes a
  full-column cycle (k,p,w,cw repeat) by depth 8192; the key-cycle census of the
  48-chain grid matches b9c8's ~10% (the same fixed-key subset, w still wobbling
  there per b9c8).
- **P3 (radius invariant, sub-floor).** max |r_n − r_0|/r_0 < 2⁻²⁰ on every chain at
  every depth (b9c8's floor holds; my finer instrument expects 1e-9..1e-12, growing
  at most like √n or log n, never linearly past the floor).
- **P4 (twins contract, held-out).** twin B (w0+1 ulp) stays bit-identical to twin A
  through depth 8192 (the word rounds the 1-ulp w perturbation away at the first
  decode: the map is locally contracting in w, not chaotic).
- **P5 (retro arms, held-out).** cw=true arms either refuse at entry (Domain/Range,
  the page's ~1–2% class) or join the same ratchet classes with their own rates;
  no new walk class (no diffusion, no two-sided walk) appears.
- **P6 (fuel).** The dropped residual is steady per chain (res_pos varies by <1%
  after the first crossing); chains with larger res_pos have larger |rate| — the
  ratchet is powered by the decode defect, one ulp of k per quantum of shape bias.

Kill criteria: P1 fails if any depth-64 walker's k walk goes two-sided (sign census
< 90%) or its rate decays ≥ 2× by depth 1024 (saturation: the page's bounded read
would then be right for k too). P2 fails if a walking chain closes a column cycle —
then the ω-limit is a lattice cycle and the walk is a transient, not a ratchet.
