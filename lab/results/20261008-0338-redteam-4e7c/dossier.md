# Dossier — red-team of docs/representation.md, run 20261008-0338-redteam-4e7c

**Claim.** The encounters representation (law.md "Finding encounters", crates/encounters, r8) is
Kepler-native: inside a GR doll every orbit precesses (Δϖ ≈ 6πM/p per radial period) with (E, L) —
the law's whole bookkeeping — unchanged, which (a) breaks the "exact integer circle rotation"
timing premise, and (b) invalidates cone candidate certificates at a rate set by differential
precession, not by kicks; measured at p = 30M the emulator fed *perfect* inputs misses ≥ half the
true encounters and a cone-excluded pair with zero kicks has real encounters the certificate can
never see.

**Bottleneck.** Board focus "finding encounters without work per orbit or per element change"
(the Binet cone, r8 v3/v4, plus a skin) and the top scaling risk. The premise failure makes
steady-state work per orbit ≠ 0 in strong-field dolls and breaks the zero-miss guarantee exactly
where the game's cinematic scenes live (fleets and belts near compact masses). It deletes no
component by itself; it scopes the current one and demands a two-frequency (synodic × apsidal)
section representation or a declared weak-field-only domain.

**Evidence.** See "The falsifier" below and `falsifier.py` / `result_*.json` / `predictions.md`.

**Lens premise survey** (all six lens premises, judged against the record before my own run):

| Lens premise | Status | Evidence in the record |
|---|---|---|
| 1. Two-body doll, 1PN EOB, ν in energy map only | survived, scoped | r3 v3 (precession 1024/1024, periods 632/632, ν 500/504, assists 64/64) + B11; B11's own margin (1% + 16/p) admits 2PN error at small p; comparable-mass tight binaries outside the gate domain are a known stepping-stone limit (PRINCIPLES 30) |
| 2. Binet cells, band equation as rotation | already killed by the builders | law.md: the in-band area-preserving map "carried a first-order slope error in every cell holding a turning point" → replaced by `space-darwin16-v1` (exact root factoring); errors ~1e-6 per cycle, gated B1–B9 |
| 3. Kicks and cycle derivatives absorb perturbations | killed near resonance; killed as quantized memo | r4 v1/v2 (over-pump 2×, angle circulates), r9 (Clairaut), jet re-anchor C·drift² (20261006-0346-redteam-df81); "not adopted: quantized (E,L) memo for kicks" is in law.md |
| 4. Dense order bit-identical to sparse | survived by construction | the tie rule (20261005-0543-redteam-6254) + canonical batch rule make both orders pop the same sequence (B8); engine test ran a battle bit-identical |
| 5. View gathered at the past light cone | physics survives; gates do not exist | one crossing per tube is exact (timelike vs cone); but **no gate covers observer-motion aberration/Doppler/beaming** (B3 static lens, B16 moving *lens*, B7 clock rates only) and r6 was never written; the gather is 83% of a light frame (H0210) |
| 6. Undisturbed bodies cost ≈ 0 | killed in practice | the memo artifact (5 Oct): the plane recompiles an orbit on ~99% of kicks; cadence is the lever (q-cadence queued) |

**The new attack (ranked first).** Ranks above the view-gate gap because it breaks a correctness
guarantee ("complete: missed_fraction ≤ 0", r8 v4) in a regime a player reaches by flying anywhere
near a compact mass, and because it is a *premise* failure of the representation (closed-ellipse,
one-frequency sections), not a missing test.

1. **GR precession breaks encounter timing and cone certificates** (this run; numbers below).
   The rung that should catch it: r8 v4's `complete`/`missed_fraction ≤ 0` — but every r8 case is
   Keplerian (no precession), so **no existing case can see it**. Suggested case: one belt at
   p ≈ 30–50 M doll units whose truth is integrated on the doll's own Binet law (as here).
2. **The view at high c has no gate.** r6 was never frozen; B16 aberrates the *lens's* frame, the
   observer's own β (the game's core promise: "feel what living at high c") is ungated: colour
   (−p·u), aberration order against lensing, aggregate beaming k⁴ at γ ≫ 1. No rung criterion
   exists → "none does".
3. **Certificate invalidation is driven by precession, not kicks** (measured here as the excluded-
   pair kill): B9's "zero work per orbit until an event" and r8's `steady` case (10⁵ orbits, no
   kicks) silently assume Kepler; in a GR doll "no kick" does not mean "no change".
4. Two-body doll outside B11's domain (e ≤ 0.6, p ≥ 20, ν ≤ 0.25): the gate's own +16/p margin
   concedes it; lead, not a kill.
5. Lens premise list itself is stale: premise 2 was already replaced; a red-team lens re-run
   against law.md (the live spec) rather than representation.md §1 would aim better.

**The falsifier** (`falsifier.py`, numpy, ~2–4 min per mode on this 8-vCPU runner):

- Truth: exact Schwarzschild timelike Binet law u″ + u = M/L² + 3Mu² (the doll's own law),
  RK4 in t, dt/dφ = E/(L·u²·(1−2Mu)); 62 bodies (60-belt p = P0·(1±1.5%), e ∈ [0.18,0.22],
  random ϖ, at periapsis at t=0, plus one cone-excluded pair p = (P0, 1.04·P0), e = (0.20, 0.21),
  ϖ = 0). ρ = 1e-3·P0 (r8's loose end). Encounter = local distance minimum < ρ with dip quantum
  1e-6·ρ (r8 v4's definition).
- Crate emulator: fed the *exact* osculating (p, e, ϖ) from the truth's own trajectory and the
 exact radial period (least-squares over all periapses, as exact as the law's memo would supply);
 the check set is a **generous superset** of the crate's: every conjunction dip of the
 closed-ellipse one-frequency model below 1.5ρ (the crate's cross windows × safety, numeric
  windows {D < 1.05ρ} and full sections at every periapsis are all subsets of this); each check
  reads the truth's minimum distance within ±CAP of the model dip time; encounter iff < ρ.
  Cone-excluded pairs (|ΔU| − R ≥ ε_u) are never checked. No kicks anywhere. Superset + exact
  inputs means any miss measured is a miss the real crate would also make, never more.
- Controls: the Newtonian twin (u″ + u = M/L²) must give missed = false = 0, or the run is VOID.
  Two emulator bugs were caught by exactly this control and fixed before any GR number was
  recorded (sections limited to the two-crossing-arcs kind; grid-measured periods accumulating
  ~16 time-units of model-truth phase drift — the least-squares fix). The control is part of the
  protocol, not decoration: prediction 1 in `predictions.md` is what caught both.

**What would make it wrong.** If the law's kick layer were specified to re-set candidate
certificates on apsidal advance (not only on kicks), the timing miss would shrink to the window
problem alone and the excluded-pair kill would vanish; the cost then scales with differential
precession (measured drift, below), which at p ≈ 30M re-sets every near-tangent pair within
~10² orbits — still not "zero work per orbit". If encounters are declared weak-field-only
(Δϖ·horizon ≪ arc width ⇒ p ≳ 10⁵ M over a 10⁵-orbit horizon), the kill is scoped, not undone:
the plane's scene (p ≈ 5.27×10⁸ M) is safe, every compact-mass scene is not.

**Cost of adopting / fit with PRINCIPLES.** The fix is representational (principle 19: a fix
signals the wrong representation): sections become two-frequency — sample at periapsis passages
(the radial period stays exactly constant between kicks, so that half of the circle rotation
survives) with the window carried in the co-precessing frame; the first-hit becomes a
2-dimensional Diophantine (Kronecker) problem, still integer. Cost: one more dimension in the
certificate, not a per-orbit scan. Alternatively scope the crate to weak field and route
strong-field dolls to per-conjunction skins. "Symmetry is found, not given" (principle 32): the
symmetry that produced the cone (Binet space) is the *static* symmetry; the rosette's symmetry is
the torus, and the certificate must live there.

**The lens.** The red-team lens overweighted representation.md's six premises, four of which the
builders had already killed or gated; I nearly re-attacked the banded Binet tangent error (found
and fixed on 30 September as `space-darwin16-v1`). What the lens made me miss: the record's own
"top scaling risk" framing pulled me toward N-scaling; the kill is not about N at all — it fires
at N = 2. Ranking by player visibility (the lens's own correction) is what surfaced it: fleets
near compact masses are flagship scenes.
