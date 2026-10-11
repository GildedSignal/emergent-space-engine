# Predictions — 20261011-0517-spacex-d0ea (H_live of the plane's belt)

Written before the decisive run. The probe (512 ships, 6 orbits) is for speed and plumbing only;
no numbers below have been tuned on it.

**The measure.** A belt group = M ships born with the *same* (p, e, phase), differing only in
orientation angle. A store of "program + angle-independent generator" (the shipmem bet, with any
refit absorbing the group's mean path) predicts identical tubes for all M forever. The
within-group spread of the tube's words — key shape (p, k), periapsis angle, periapsis time, in
the store's own integer quanta — is therefore exactly the scar bits the store must pay. H_live =
its growth per orbit and per game-second. Scene: star + one planet (1/999 of the total mass) at
5.2 AU, belt 2.0–3.5 AU, e = 0, the plane's own law (128 kicks per radial period, integer tubes).

## Held-out predictions

1. **Cold radii saturate.** Groups more than ~3% in radius from any low-order resonance with the
   planet (the resonance ladder: 4:1 at 2.06, 7:2 at 2.27, 3:1 at 2.50, 8:3 at 2.72, 5:2 at 2.82,
   7:3 at 2.94, 9:4 at 3.03, 2:1 at 3.28 AU) reach a bounded spread within ~5 belt orbits:
   bits_sum ≤ ~10 bits/body, and the per-orbit growth at the end (last interval) below
   ~0.1 bit/body/orbit. The transient is the short-period terms developing; after that the
   averaged law is the truth to within rounding.

2. **Resonant radii grow without bound.** Groups inside the first-order resonances (3:1, 2:1)
   show secularly growing bits_sum (≥ 5× the cold value by the last snapshot, still rising),
   dominated by the periapsis-time field (mean-motion decoherence) and the k field (e pumped).
   Expected hot fraction (groups with bits_sum > 32 at the end) ≈ 2–6% of bodies: resonance
   widths ~μ^(2/3) ≈ 1% in radius each, and the grid resolves ~1.15% per radius.

3. **The 10⁹ verdict.** bits/body ≈ (1 − hot)·(cold bits) + hot·(≤ 128, a full tube). With
   prediction 1 and 2: ≈ 0.95·8 + 0.05·128 ≈ 14 bits/body → 1.75 GB at 10⁹ bodies: **fits** the
   4 GiB budget, with the birth program (~0.13 bits/body) negligible. The verdict flips only if
   the cold bits grow secularly (no saturation) or the hot fraction exceeds ~20%.

4. **Rounding churn is real but small.** Even cold groups have nonzero nz_k/nz_p (every kick
   moves the exact key; orientation-dependent kicks round differently), but the entropy stays a
   few bits: the spread spans few quanta. If instead the *cold* rounding spread grows with t
   (a random walk in the key grid), the program store pays a growing tax even without physics —
   that would be a representation finding against exact keys (it would argue for the quantized
   memo cell as the *store* quantum, a law-level choice).

5. **Game-seconds.** One mid-belt orbit ≈ 4.4 years ≈ 1.4e8 s of game time; 40 orbits ≈ 5.5e9 s.
   H_live per game-second will be ~1e-9 bits/body/s — the per-orbit rate is the useful number.

## Kill criteria (written before the run)

- Cold groups' bits_sum growing secularly at the end (last-interval growth > 0.3 bit/body/orbit
  on the median cold group) kills "program + generator" for belts: memory would grow with
  simulated time at every radius, and 10⁹ in 8 GB needs a different store (periodic
  reprogramming of the mean is already absorbed; this would be irreducible spread).
- frac_birth_tube should fall to ~0 within the first interval (every kick re-keys the exact
  memo: the standing memo finding). If it stays 1, kicks are not reaching the ships and the run
  is VOID.
- Controls both sides: a group at a radius with no planet (μ = 0 would be the ideal negative,
  but the plane needs a planet for the doll tree; instead) the *coldest* groups act as the
  negative control (spread from rounding only), and the resonant groups as the positive.
