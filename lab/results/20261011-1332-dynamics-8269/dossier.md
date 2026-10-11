# Dossier — run 20261011-1332-dynamics-8269 (dynamics lens)

**Claim.** The belt's live information is not the kick rate: away from resonance a
body's filtered (proper) semimajor axis is a bounded attractor (median deviation
4.8×10⁻⁶ AU over 5000 Jupiter orbits, at the instrument floor), and only a
resonance-localized diffusing minority (12.2%) produces distinctions, at a measured
steady flux of ~4×10⁻⁴ scar-writes per body per 1000 orbits at quanta 3×10⁻⁴–3×10⁻³
AU — 7.7×10⁵× fewer writes than scarring at the averaged kick law's rate (0.3/orbit),
so the belt program survives ~10⁴–10⁵ orbits between re-programs and 10⁹ bodies add
only ~2 MB of scars per 1000 belt orbits.

**Bottleneck.** The board's named risk "distinctions created per game-second (H_live)
… not measured yet" (HANDOFF, Risks), B18's floor ("bytes per live body ≤ 2× the
measured information floor"), and the Opus memo R2 line 129's opposite claim: under
the kick law "every kicked belt body carries a full scar" (churn = kick rate, 64/orbit
unaveraged, 0.3/orbit averaged), which at 10⁹ bodies forbids a program-backed belt.
Expected gain: memory, 10²–10⁵×; deletes the assumption that the belt store must
degenerate to per-body tubes after the first kick.

**Method (the lens).** Classify each body's information production instead of asking
(as q-secular did) whether one closed-form generator predicts it. Instrument: planar
restricted Sun–Jupiter–Saturn (planets on prescribed Kepler orbits; no mutual J–S
interaction — approximation), test bodies by a symplectic Kepler map (exact Kepler
drift under the Sun + planetary kicks with the indirect term, KDK, dt = P_J/100).
Per body: Lyapunov exponent by shadow renormalization (d0 = 1e-9 AU, each Jupiter
orbit); filtered elements = 81-orbit running mean of 10-per-orbit bin means
(anti-aliased proper-element proxy; floor 2.9×10⁻⁵ AU); hitting = |filtered a(t) −
filtered a(0)| first crossing of ±q. Scene as q-secular's: a₀ uniform 2.0–3.3 AU,
e₀ Rayleigh σ = 0.07 truncated at 0.25, uniform angles, N = 1024, T = 5000 Jupiter
orbits (5.9×10⁴ yr).

**Commands** (this folder; numpy only; each process < 0.6 GB):
`python3 belt_entropy.py C1` / `C2` / `R1` / `R1f` (concurrently; ~4/4/12/3 min on
the shared cloud runner — orders of magnitude only), then `python3 belt_entropy.py
analyze` → `metrics.json`, `bodies_R1.npy`, `dA_series_R1.npy`.

**Evidence.**
- **C1 quiet ring (a₀ = 3.10, e₀ ~0.01, N = 256):** filtered-|Δa| end median
  7.6×10⁻⁶ AU; hits at q = 3×10⁻⁴: **0/256**; at q = 1e-4: 12/256 (4.7%, the filter
  floor). Synodic (unfiltered) a-oscillation 4.1×10⁻³ AU — large, bounded,
  phase-locked: predictable, hence not information. Lyapunov floor 1.56×10⁻³/P_J.
- **C2 planted 3:1 chaos (a₀ = 2.502, N = 256):** filtered-|Δa| end median
  1.55×10⁻³ AU (200× C1); hits at q = 1e-3: **252/256 (98.4%)**. The a-hitting rate
  separates clean from chaotic by two orders of magnitude where the Lyapunov
  estimator cannot (C2/C1 λ median only 1.65×: t_λ(3:1) ~ 10³ P_J sits at the
  instrument's resolution; λ p90 6.1×10⁻³ vs C1 2.6×10⁻³).
- **R1 belt (N = 1024, T = 5000):** diffusing fraction (|Δa_filt| > 3×10⁻⁴ at end;
  classifier calibrated 0/256 false on C1, 255/256 true on C2) = **12.2%**, with
  end-deviation median 1.26×10⁻³ AU vs the quiet majority's 4.8×10⁻⁶ AU (p99
  2.6×10⁻⁴). Localization: ~0% everywhere except 20–24% at the 3:1 (2.45–2.55),
  30% at the 5:2 (2.80–2.85), 23% at the 7:3 (2.95–3.00), and 64–92% at the 2:1
  outer edge (3.20–3.30); the inner edge shows nothing (planar: no ν₆ — a lower
  bound, as declared). Hit fractions by q: 28.2% (1e-4), 18.0% (3e-4), 12.1%
  (1e-3), 7.6% (3e-3), ~2.7% (1e-2). Late-window flux (new first-crossings,
  t ∈ [2500, 5000]): 3.9×10⁻⁴ per body per 1000 orbits (4 events; Poisson
  ±50%), flat across q = 3e-4…3e-3. The e-channel: 87.8% of quiet bodies cross
  e-quanta (the bounded secular cycle; free+forced amplitude > any q_e) but the
  late e-flux is **exactly zero** — crossings stop once the cycle is established:
  a one-time transient, absorbed by one re-program (or by storing the proper
  decomposition at birth).
- **Convergence (R1f, dt/2, T = 1000):** λ-1k median 1.05×10⁻² vs 1.08×10⁻² (+3%);
  hit fraction at q = 1e-3 within 1000 orbits 11.9% vs 11.5% (−4%). Converged.

**Memory synthesis.** At 10⁹ bodies and q = 1e-3 AU: initial transient ~12% scarred
over the first ~5000 orbits (mostly the secular cycle in e and the resonant
walkers), then ~4×10⁻⁴ × 10⁹ = 4×10⁵ new scars per 1000 belt orbits ≈ 2 MB per 1000
orbits at ~5 B per scar. A re-program (one O(N) idle-time refit) every 10⁴ orbits
holds the scar layer at ~0.4% of bodies (~20 MB). Against kick-rate scarring
(0.3/orbit averaged): 300 writes per body per 1000 orbits vs 4×10⁻⁴ → **7.7×10⁵×**
fewer; against the 64-kick law, ~1.6×10⁸× fewer.

**Predictions** (predictions.md, written first). Held: C1 floor (0/256 at 3e-4,
λ 1.56×10⁻³ < 3×10⁻³, synodic 4.1×10⁻³ ≥ 3×10⁻⁴); C2 a-hitting ≥ 30% (98.4%);
belt hit fraction at 1e-3 in 10–50% (12.1%, low end); late flux < 3×10⁻¹ per body
per 1000 orbits (4×10⁻⁴, 770× under); quiet-majority hits at 3e-4 < 20% (5.8%);
filtered-e bounded with no late flux (exactly 0); steep q-falloff (28%→2.7% over
100× in q); resonance localization (3:1, 5:2, 7:3, 2:1 — exact; inner edge
correctly absent planar). Failed: the λ-based chaotic fraction (predicted 15–60%
at λ > 10× floor; measured 0.1% — the shadow instrument at T = 5000 resolves only
t_λ ≲ 600 P_J, and C2's 5× separation prediction with it, 1.65×); the
classifier-equivalent fraction (12.2% at 3e-4) landed just below the predicted
15–60% band. Both failures are instrument resolution, disclosed above, and the
quantity the band aimed at is measured by the hitting rates instead.

**What would make it wrong.** Prescribed planets (no J–S interaction): the forced
secular spectrum is approximate; the chaos structure is set by Jupiter's MMRs,
which are exact here. Planar: no inclination-driven ν₆, so 12.2% is a lower bound
for the inner edge. T = 5000 orbits: Lyapunov certification is impossible (only
t_λ ≲ 600 P_J visible); slow chaos (t_λ ~ 10⁵ yr) is invisible in λ and
under-counted in the 5000-orbit hitting rates — the flux 4×10⁻⁴ is a lower bound
on the true asymptotic flux, though the late window being flat across q argues
the walkers are the same population, not a growing one. q = 1e-4 hit fractions
are filter-floor-limited (upper bounds). Self-stirring (belt–belt encounters at
planetesimal masses) is unmeasured and adds on top; the player's seeds and any
population the game actually flies are unmeasured terms.

**Cost of adopting.** The scar policy becomes "write on filtered-quantum crossing,
not on kick": the kick layer keeps a per-body running mean of osculating elements
(the averaging it already computes) and writes only at crossings; the allocator
re-programs a population when its scarred fraction crosses a budget (measured
dial: 4×10⁻⁴ per body per 1000 orbits planet-driven). No gate changes; B18's floor
computation and the b-h-live dashboard build gain their physical calibration.
Exactness untouched: scars, when written, are the law's exact integers; only the
write schedule changes.

**Fit with PRINCIPLES.** "Compute only surprises" (P3): a predictable kick is not a
surprise and must not allocate memory. "Store the generator, not the generated"
(P6): program + attractor is the generator; scars are only its innovations. "The
memory floor is information-theoretic" (P24, standing decision): the floor is the
measured hitting flux, not bytes × count. "A failed experiment kills that
configuration, never the method" (P9): q-secular-v2 killed LL phasors as the
predictor; this run shows the information those bodies still do not produce.

**The lens may have made me miss:** the transient — the first ~5000 orbits scar
12% (secular e-cycle + walkers): a gate built on the early flux would
over-provision by ~30×; steady state needs the late window. Long-run slow chaos
and the Kirkwood-gap leak (bodies wandering into resonance over 10⁵⁺ yr) are
invisible at this T. Belt–belt self-stirring and player-seeded structure are the
unmeasured terms; the next rung is the same instrument at T = 2×10⁴ with a
self-interacting subsample.
