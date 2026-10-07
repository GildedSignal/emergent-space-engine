# Predictions (written before the decisive run)

Question: at 10⁹ bodies on the M1 (8 GB), which term of H_live (live distinguishing bits
created per game-second, minus reabsorption) breaks the 8 GB promise, and by how much?

Held-out cases (not tuned on):

1. **Belt-0 encounter count (claim check, r8 v2).** With belt 0's geometry
   (a ∈ [1, 1.5] game units, σ_e = 0.01, N = 10⁴, 20 orbits, 1.7M orbit-crossing pairs),
   the reported truth was 427 encounters. My independent conjunction-geometry estimate
   reproduces 427 within a factor of 3 for some threshold ρ ∈ [10⁻⁵, 10⁻³]; I predict the
   matching ρ is ≈ 1–3 ×10⁻⁵ (units of a=1) — i.e. r8's "encounter" is a ~10⁻⁵-close pass,
   not a Hill-scale event.
2. **Impulse bits per encounter, ship/rock scale.** For mutual encounters between bodies
   of mass ≤ 10¹⁵ kg (any miss distance above physical contact), the velocity impulse
   δv/v_K ≤ 10⁻⁶, i.e. below every plausible program quantum: bits/encounter ≈ 0
   (< 1 bit even at q = 10⁻⁹). Encounter-created distinctions from asteroid/ship mutual
   gravity are a *compute* problem (candidate work), not a memory problem.
3. **Impulse bits per encounter, embryo scale (10²² kg).** At the matching ρ from (1),
   δv/v ~ 10⁻⁵–10⁻³ → 5–40 bits/encounter at quantum q = 10⁻⁶; each such encounter also
   starts a phase-drift clock (1 rad in ~ 1/δn_orb orbits) that ends in full
   individualization (128 bits) if nothing reabsorbs.
4. **Scaling honesty.** Scaling the same belt volume to N = 10⁹ multiplies the per-body
   encounter rate by 10⁵ (n × 10⁵): the belt becomes optically thick at the r8 encounter
   threshold (per-body rate ≥ 0.1/orbit). So "10⁹ in one belt annulus" is not a
   gravitationally smooth population: 10⁹ needs doll layering or wider spreads. I predict
   the distinction rate at 10⁹ in ONE annulus exceeds 10⁶ bits/s game-time (memory death),
   while the same 10⁹ spread over dolls/bands (density per doll unchanged) keeps
   belt-wide encounter distinctions < 10³ bits/s.
5. **The gate.** The only H_live term that can reach the 6 GB usable floor at 10⁹ is
   *individualized* per-body state for a resonant/id population: f_ind × 10⁹ × ~128 bits.
   f_ind = 5% → 8 GB (dead); f_ind = 1% → 1.6 GB (fits). Battles and the player are
   bounded by participants/attention (≤ 16 MB for a 10⁶-ship fleet fully individualized).
   Smooth-belt peacetime creation rate: 10⁰–10² bits/s game-time (8+ orders below the
   floor over a session).
