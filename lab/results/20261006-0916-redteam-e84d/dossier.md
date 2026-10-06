# Dossier — red-team of docs/representation.md (run 20261006-0916-redteam-e84d)

**Claim:** The design's cost model and its gate ladder both miss two populations a
player meets early: the steady resonant band of any belt near a planet — priced as
"bursts", gated by nothing (measured: 5.8% of a belt at Jupiter μ, 28.6% at μ=10⁻²,
0% when cold) — and the strong-field comparable-mass binary, where the 1PN doll is
wrong by 10.2% in periastron advance at p=20M and B11's 1PN oracle is structurally
blind to it.

**Bottleneck:** board items "fitting 10⁹ in 8 GB" and "the top scaling risk" lean on
the §6 cost table's premise that chaos is *bursts* and undisturbed motion is *averaged*.
A belt's resonant band is a steady f×N population with no cheap layer (averaging dead
by the design's own rule, first-order conjunction kicks dead by r4 v2, single-resonance
doll inapplicable under overlap): f×N bodies pay exact conjunction work at ~1 event per
synodic period forever, and they are exactly the Kirkwood-gap bodies — averaging them
away to save the row erases the belt's emergent history (principle 29).

## Ranked attacks

### A1 (top, measured): the belt is steady sparse chaos, not bursts
- Premise attacked: §6 row "Chaos and contacts | bursts" and the sparse/dense dichotomy
  ("sparse" = symmetric = certificate-friendly). A belt near a planet is *sparse in
  rate* (about one conjunction per synodic period) but has **no symmetry to compress**:
  orbit averaging is dead (design §3 admits), per-conjunction first-order kicks are dead
  (r4 v2 KILL: 2× e-over-pump, resonant angle circulates), the single-resonance
  rotating doll does not apply where resonances overlap, and the overnight
  m-meso-motion silver marks shallow flybys "conditional". This population is steady,
  not a burst — a third regime between the table's two.
- Falsifier (float, ≤ 60 s per config): 2-D circular restricted three-body (star + one
  planet + 800 massless test particles), a uniform in [0.38, 0.75] a_planet (covers
  4:1…2:1 resonances), e₀ Rayleigh σ=0.1, random angles, T = 1200 planet orbits,
  leapfrog dt = P/150. Classifier: semi-major-axis diffusion (drift = max−min of six
  200-orbit window means of a; chaotic iff drift > τ_a = 0.003 a_J, calibrated on the
  μ=10⁻⁶ control). An earlier renormalized two-particle Lyapunov estimator was
  discarded: it counted Kepler's epicyclic shear as chaos (pure-Kepler control gave
  fake Lyapunov times of 23–115 planet periods). `belt_chaos.py`, data in
  `sweep.jsonl`, commands in `run.log`.
- Numbers (T = 1200 orbits, so lower bounds — slow diffusion is undercounted):
  **f_chaotic = 0.75% (μ=10⁻⁶, control) → 2.1% (3×10⁻⁵) → 5.8% (9.54×10⁻⁴, Jupiter)
  → 28.6% (10⁻²)**; cold belt (σ_e = 0.01) at Jupiter μ: **0.0%**. Median drift of the
  chaotic population 0.005–0.12 a_J — these bodies migrate across the resonance
  network. Their conjunction rate is 1.0–1.3 per planet orbit each. Scale: at Jupiter
  μ, a 2²³-body belt (B18's size) has ≈ 4.9×10⁵ such bodies; at μ ≥ 10⁻² (moon
  systems, engineered fleets) ≈ 2.4×10⁶ — paying exact conjunction work forever, in
  no cost row.
- Rung that should have caught it: **none.** B18-belt is planet-free (a memory gate),
  B15's scene has fleets and a central mass but no belt and no resonances, B17 tests
  two single resonances only. Nothing measures the steady fraction, its event rate, or
  the p99 of a belt-with-planet scene. Fix: extend B15 (or add B20) with a
  belt + Jupiter-mass scene: report the non-averaged fraction, conjunction-event rate,
  and p99 against the flat control.
- Principles: 14 (no work for no reason — steady tick-like work through the back door),
  12 (p99), 29 (gaps are the emergent history the scene promises).

### A2 (measured): the 1PN two-body doll has no domain fence, and B11 cannot see the error
- Premise attacked: "Two bodies are one doll… ν enters only through the energy map"
  (§1) — true at 1PN, unfenced beyond it. The doll's internal dynamics is *exact*
  Schwarzschild with M = m₁+m₂ behind the phase-locked (time-preserving) 1PN map, so
  at matched invariant frequency X = (MΩ)^{2/3} its advance is the test-mass one,
  k_doll = 3X(1 + 3.5X). The true 2PN advance (Damour–Schäfer 1988; Kopeikin 2020,
  eq. 13, circular, e_T = 0) is k_true = 3X(1 + (b₁−b₂)X), b₁−b₂ = 3.5 → 6.17 as
  ν goes 0 → 0.25. Parse validated at ν→0: 27/4 − 13/4 = 3.5, the exact Schwarzschild
  coefficient from (1−6u)^{−1/2}. `eob_2pn.py` (instant), source PDF kept.
- Numbers (relative advance error of the doll vs 2PN truth): ν = 0.25: **10.2% at
  p = 20M** (B11's floor), 4.7% at 50M, 2.7% at 100M, crossing 1% at **p ≈ 267M**;
  ν = 0.1: 3.3% at 20M, 1% at 80M. B11's own tolerance at p=20 is (1% + 2·8/p) ≈
  1.8% — the true error exceeds it 5×, **but B11's oracle is 1PN, so it measures
  zero**: the gate certifies the doll where both agree by construction. r3 v3's
  "ν effect 500/504" tested the 1PN energy map, not this.
- Player-visible: a tight comparable-mass pair (a black-hole binary, the GR set piece)
  — periastron advance is *the* signature a player watches; 10% over a few orbits is
  plainly visible.
- Fix: B11 sweeps p down against a **2PN oracle** (closed form above), and the design
  grows a ν/p fence: below it the doll's A(u) takes its 2PN term 2νu² (one more
  constant per doll, like χ) or the pair goes to the dense order. Principle 33: the
  regime is *chosen* by the dimensionless number, not discovered by the player.
- Caveat: circular coefficient (parse exact there); eccentricity moves it at O(e²),
  not the order.

### A3 (analytic): longitude continuity across kicks is ungated
- The cycle memo stores ∂(Δφ, Δt, Δτ)/∂(E, L) — the *increments'* derivatives. A kick
  lands mid-cycle; the new cycle must inherit the *event* (r, φ, t), i.e. the phase
  map, which those derivatives do not express. A systematic longitude slip would
  mistime every later conjunction (the encounters crate's continued-fraction
  scheduling trusts phases) and misplace ships on screen, while every existing gate
  stays green: B5 reads E, L growth and shape; B13 reads ΔE and ΔL; B12 reads the
  Jacobi constant. None reads a longitude. Fix: extend B13 to bound the final true
  longitude too, or a small rung: N kicks on a fixed cadence, longitudes compared
  against a float integration of the same kicks.

### A4 (named): r5's bit-identity must plant a handoff inside a dense region
- The tie rule (canonical same-epoch batches) covers events sharing a body; a
  handoff's boost-and-shear re-expression is exactly invertible *in isolation*. The
  adversarial case is a handoff resolved between two kicks within one light-crossing
  window of both dolls: sparse resolves it in queue order, dense in lockstep, and the
  integer rounding at the re-expression can differ unless the batch rule spans the
  handoff. r5 is queued (law.md's open list) — it must include this case, or B8's
  "sparse and dense identical bits" is tested only where they trivially agree.

### A5 (analytic, low rank per blind-spot rule): multi-doll lensing composition
- "Lensing adds crossings, from each doll's memoized deflection(b)" composes per-doll
  deflections additively — valid weak-field, untested when two strong fields sit along
  one ray. B16 gates a single moving lens. Rare on screen; name B16's extension (two
  lenses, strong field) and leave it.

### A6 (doc truth, no falsifier): representation.md is stale where law.md moved
- §1 still presents the Minsky/Binet in-cell map as "the primary in-cell solution";
  law.md replaced it after the turning-point first-order slope error
  (`space-darwin16-v1`, 30 September). Two homes, one truth (AGENTS "Text has a
  cost"): the design doc asserts a premise the law already killed. One edit, zero
  physics.

### A premise that survives (worth recording)
- The past-light-cone gather's uniqueness: for |β| < 1, dt_ret/dt = 1/(1 − n̂·β) > 0 —
  strictly monotone, so each timelike tube crosses the observer's past cone exactly
  once, and Newton from the previous frame's root sits on a monotone function
  (converges). The view's cheapness premise stands on solid ground; only the
  multi-doll composition (A5) is open.

## Predictions
Written before the decisive run (`predictions.md`). Outcome:
- P1 (Jupiter f_chaotic ∈ [5%, 25%]): **held at the low edge** — 5.8%. Its
  "additional ≥ 10% regular librators" part **failed**: the resonant-angle classifier
  found ~0 — at this run length the librating islands sit inside the drifting
  population, so the instrument cannot separate them. The non-averaged total is
  f_chaotic plus an unmeasured regular-resonant remainder.
- P2 (μ scaling): 3×10⁻⁵ → 2.1%, a 2.8× drop, **short of the predicted ≥ 4×**;
  10⁻² → 28.6%, a 4.9× rise, **passes** the predicted ≥ 2×.
- P3 (control ≤ 0.125%): **failed** — 0.75% (6/800 drift even at μ=10⁻⁶; thin
  separatrix layers exist at any μ and the floor sits near τ_a).
- P4 (cold belt drops ≥ 3×): **passed with room** — 0.0%; chaos needs e.
- P5 (conjunction rate 1–3 per planet period): **held** — median 1.0–1.3 (NaN where
  drifters leave the belt at high μ; the rate is analytic in mean a).
- P6 (longer runs raise f): not run — out of time; f is a lower bound either way.
- My pre-registered kill criterion for the "bursts" premise (f_chaotic + f_librating
  ≥ 15% at Jupiter μ) **did not fire at Jupiter μ** (5.8%); it fires at μ = 10⁻²
  (28.6%). Honest reading: at solar-system mass ratios the missing population is real
  but three times below my threshold; at moon-system and fleet ratios the premise is
  dead by a factor of two.

## What would make this wrong
- A1: if longer runs show the drifting fraction decaying (a transient) or the
  classifier is overcounting near its floor, the "steady population" claim weakens to
  "slowly evolving". The μ=10⁻⁶ control (0.75%) and the cold belt (0%) bound both
  overcount modes; undercount is the live risk (T = 1200 orbits only).
- A2: if the doll's map is not phase-locked at 1PN (Ω_real ≠ Ω_eff), part of the error
  is absorbed — but then it is not the 1PN EOB the design names. The eq.-13 parse is
  the other risk, mitigated by the exact ν→0 check (3.5).

## Cost of adopting, fit with PRINCIPLES
- A1: one gate (B20 or a B15 extension) and one cost row in §6 — measurement first,
  no representation change yet. Julien: "the algorithm that allocates the work to
  prevent those heavy tails, it's the most important one" — a steady unpriced
  population is exactly a heavy tail.
- A2: a ν/p fence plus the 2PN A(u) term in the strong-field doll (one constant, like
  χ), and a 2PN oracle for B11. "what really matters is navigation, knowledge and
  dynamics those need to be perfect" (OC#16).
- A3/A4: gate extensions only.

## The lens: what this lens may have missed
- Red-teams overweight exotic cases; I ranked by commonness, but the belt scene (A1)
  is still a *chosen* archetype — the lab's own B18-belt is planet-free, so the
  integrator's taste may differ. I did not attack the memory floor (bottleneck 5) or
  the Fermi frame's Kerr tide (phase 2) at all, and A3/A4 are unmeasured hunches. The
  2-D restriction of the belt toy misses inclination-dependent resonances, which only
  add population.
