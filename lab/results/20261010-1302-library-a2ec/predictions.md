# predictions.md — 20261010-1302-library-a2ec

Written before the decisive probe (`work/probe.py`). Bottleneck: kicks dominate the
engine's cost; the lever is cadence (board focus item 1; taste log 6 Oct: correctors
and higher-order splits buy nothing, `q-cadence` queued). Lesson L1 proposes cadence
as a **per-body certificate**, not a clock: the next kick is scheduled at
`t* = sqrt(2q/a_bound)` where `a_bound` bounds the tidal acceleration along the
current analytic generator orbit (Encke's rectification interval as certificate).

Toy: test particle a=1, e=0.05, mu=1; static secondary m_s=0.01 at R=3.
Truth: RK4 at T/4096, 200 orbits. Policies: no-kick (negative control), fixed-32,
1. **P1 (count):** gated-q fires 10–15 kicks/orbit in config A (vs 32 for fixed-32)
   at certified error q (hand Fermi before any run: grid tide max ≈ 1.5e-3, so
   t* ≈ 0.5, ~12/orbit; the raw analytic bound would give ~19). Stretch: with a
   tighter (averaged-tide) bound, 5–10/orbit, i.e. 3–6× fewer.

2. **P2 (behaviour):** gated-q's final eccentricity error stays within 2× of
   fixed-32; its apsidal drift per orbit is within 2× of fixed-32. (r9 warns
   precession is the sensitive one; if anything fails it will be apsidal.)
   fixed-8 (same kick count, clocked) is worse than gated-q on both — the gain is
   from *when*, not just *how many*.
3. **P3 (bound tightness):** median realized oracle interval / certified t* is in
   [0.5, 2]: the closed-form bound overpays ≤ 4× in count vs a perfect oracle.
4. **P4 (held-out B):** gated-q's count/orbit rises by roughly sqrt(a_B/a_A) ≈ 10×
   (bound tightens automatically; no retuning), while fixed-32 keeps its cadence
   constant and its behaviour error grows ≥10×; gated-q's error stays within 2×
   of fixed-32 in B. If gated instead collapses (count explodes without error
   parity), the certificate does not degrade gracefully near a secondary and
   q-cadence needs a regime switch after all.
5. **P5 (control sanity):** no-kick (pure Kepler) must fail massively (apsidal
   drift ≥ 100× fixed-32); if it doesn't, the tide is too weak to measure and the
   probe is VOID.
