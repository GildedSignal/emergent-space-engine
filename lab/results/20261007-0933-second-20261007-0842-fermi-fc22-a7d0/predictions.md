# Predictions (held out before the decisive runs)

Question (the checker's named experiment): count element-word writes and recertifications per
game-second on a live belt with the far quantum in force, and reconcile against the flux model —
closing the 32× gap with an engine-side measurement instead of r8 v2 geometry transfer.

Setup already measured (not predictions): `ledger.py` regenerates bit-identically from this folder;
the plane anchor gives 2349 B/body at N = 28. The shipped live-belt machinery is `crates/encounters`
(planar belts); the plane (28 bodies) and shipmem (static store) cannot host a 10⁶-body live belt,
so the measurement belt is the encounters crate's own belt spec (planar, a ∈ [1, 1.5], σ_e, rung
units μ = 1), driven by an event loop on top of the shipped `pair_events`/`cone_pairs`/`Body` — no
crate edits; masses and impulses added in a standalone crate in this folder.

## Part A — the 32× (shipped `verify` on the r8-like belts, massless, planar)

The flux model has two cross-section forms: a 3-D tube `n₃D·v·πb²` (what ledger.py's P6 evaluated,
with a guessed width w = 0.1 and vertical H = σ_e/2) and a 2-D strip `σ_n·v·2b` (the rung belt is
planar, a ∈ [1, 1.5], so σ_n = N/(2π·ā·w) with w = 0.5).

- **PA1.** On `r8like-s1e-2-r1e-4` (N = 1000, σ_e = 1e-2, ρ = 1e-4): the truth's encounters per
  body per orbit lie in [2×10⁻³, 1.2×10⁻²] — *not* the remembered ~10⁻², which I predict came from
  a different belt of the set (higher σ_e or larger ρ).
- **PA2.** The 2-D strip form, evaluated at each belt's own geometry with v_rel in [σ_e, 3σ_e] in
  Kepler units, matches the measured rate within a factor 2 at every σ_e in the set; the 3-D tube
  form (P6's) is 30–200× under at every σ_e. The 32× is then decomposed as: dimensionality
  (≈ 4H/(πρ) ≈ 60–80×) partially cancelled by P6's width guess (w = 0.1 vs the real 0.5 overstates
  density ~6×), times the rate-recollection factor (~2–3×).
- **PA3.** Across σ_e ∈ {1e-3, 3e-3, 1e-2, 3e-2} at ρ = 1e-4, the measured rate scales between
  σ_e^0.5 and σ_e^1 (the strip form says ∝ v_rel ∝ σ_e; epicyclic correlation may soften it).

## Part B — the live belt (masses on, far quantum in force, event-driven on shipped machinery)

Belt: planar, a ∈ [1, 1.5], σ_e = 1e-2, N ∈ {2000, 4000}; bodies of mass m ∈ {10¹⁷, 10¹⁸, 10¹⁹} kg
(μ = m/M_sun); drift = exact Kepler (the shipped `Body`), kicks = symmetric impulses at every pair
event with b < b_cap = 10·b_q, b_q = 2G(m_i+m_j)/(v_rel·q), q = 10⁻⁶·v_kep (the ledger's far
quantum), saturated at δv = v_rel below b_90; element words re-derived after each kick. Counted:
quantum crossings of the accumulated kick vector (|v_acc| ≥ q, reset — exactly the ledger model's
quantity), element-word changes, kicks applied (each = one recertification of that body's candidate
pairs, per law.md), and the kick/v_rel regime signatures.

- **PB1.** At (N = 4000, m = 10¹⁸ kg): crossings per body per orbit ∈ [4×10⁻³, 4×10⁻²]. Model
  (planar form, no fitted constants): single-kick rate 2σ_n·v·b_q = 4σ_nμ/q plus the sub-quantum
  walk 4σ_nμ/q ≈ 1.3×10⁻² per orbit at this point.
- **PB2.** Model/measured ratio ∈ [1/3, 3] at every rung of the mass ladder and both N, with the
  ratio flat (within 2×) across the ladder; measured rate scales as m^(1±0.25) (planar belts are
  threshold-dominated — linear in m, no Coulomb log) and as N^(1±0.15).
- **PB3.** Regime signature: the crossing rate is dominated by near-threshold kicks (the largest
  sub-q steps), so measured crossings ≈ (rate of kicks δv ≥ q)·(1–3); the mean |δv| of kicks that
  complete a crossing is within 3× of q (not ≪ q, which would mark a many-tiny-kick diffusion).
- **PB4.** Extrapolation to the claim's own belt (a = 2.5 AU, N = 10⁹, m = 10¹⁵ kg, q = 10⁻⁶·v_kep,
  300-h game): the **3-D** form stays ≤ 1 MB/game (the dossier's 18 KB stands). The **planar** form
  gives ~0.03 crossings per body per game, i.e. a ledger of order 100–300 MB/game at 50 bits per
  write and ~30 writes/s at 10⁹ bodies: the "≤ 1 MB per 300-h game" headline **fails for planar
  belts by about two orders of magnitude** while the recertification compute stays negligible
  (≤ ~2 ms/s at the shipped µs-per-kick). Every engine belt today is planar; the game's physical
  belts are 3-D. This is the boundary the checker's experiment was built to find.

If PA2 fails (the strip form misses by > 2×), the Kepler-correlated conjunction rate is not the
kinetic strip rate and the ledger's cross-section needs a belt-measured correction. If PB2 fails,
the flux model's constants are wrong engine-side and the P1 ledger number is unanchored in both
geometries.
