# The motion law v2: one clock per body, dolls as coordinates

Claude Opus, a read-only thinking agent, 6 October. Everything below was measured here, on Julien's M1 Air (AC power, load 2–4, swap 4.9 of 6.1 GB, no thermal warning), each run under 60 s. The tools are in this folder:
- `probe/universe`: a copy of `crates/universe` with ablation switches (`OM_*`, in `om.rs`);
- `probe/jac`: B12's frozen ships, B17's cases and any state, all flown through that copy;
- `probe/ar`: a float replica of the representation proposed in §2;
- `runs/*.py`: the analyses (`enc.py`, `analyze.py`, `win.py`, `decade.py`, `synth.py`, `b13.py`, `b17res.py`);
- `runs/NOTES.txt`: the raw log.

**Bottom line.**
1. **The diagnosis.** The plane's error grows only at encounters, and the leading cause is that the step is re-chosen during them. The plane recomputes it from the osculating heliocentric period, with hysteresis. Each change of step changes the quantity that a symplectic map conserves, so every encounter leaves a permanent offset. The asymmetric handoff (in at R/4, partway through a step; out at R) is the second cause, and it works the same way.
2. **The representation.** Each body lives in extended phase space (t, x, p_t, p). One fixed tick of a fictitious clock s is the only step. A time transformation, a fixed smooth function of the perturbing potential, decides how much physical time each tick covers. Kicks and drifts are exact flows of one Hamiltonian per body. A handoff is a change of coordinates for bound bodies only: an exact Lorentz shear of (event, four-momentum).
3. **What it deletes:** the choice of step, the changeover levels, the Open events, the per-tube cadence rule, alignment stubs and hysteresis, and handoffs for passing bodies.
4. **What it does not do.** It does not make B12's exponent zero by construction. B12's statistic, on a chaotic ship, reads even a bounded error that depends only on the state as growth (a planted test gives 0.22–0.57). The only fully exact form would use the scene's symmetry explicitly, which engineers the law for B12 (§2.6). I don't know a form that is not engineered.

## 1. The diagnosis: measured, not guessed

**Setup.** B12's 16 frozen ships, flown through the plane's own law (the copy, no switch set), with the planet's radius shrunk ×10⁻³ so that no ship is lost. Step 7: median exponent **0.795**, 16 of 16 surviving (`runs/base-s7-r0001.txt`). This reproduces the "about 0.8"; at full radius it is 0.662 with 7 ships lost. The Jacobi error is sampled at P/64 and split into two parts:
- its level while the ship is far from the planet (r₂ > 3 R_H);
- the change of that level across each passage, which I call the **jump** of the encounter (`runs/enc.py`).

**1.1 All the growth happens at encounters; none happens in the far field.** Far from the planet the error drifts by about 10⁻⁹ per period. At step 7 the 314 encounters have jumps of rms 5.4×10⁻⁶ with mean +9.6×10⁻⁷: 55% are positive, a 3.1σ bias. A random walk with a bias gives an exponent between 0.5 and 1, which is what the gate measures.

**1.2 The leading cause: the step is re-chosen inside the encounter.** `step_for` takes 1/128 of the tube's radial period. During a Hill encounter the osculating heliocentric period swings, and the event log (`OM_LOG`, `runs/ev/`) shows the step switching 2³⁸ ↔ 2³⁹ ↔ 2⁴⁰ ticks within one passage, each switch moving the error by about 10⁻⁶.
- **Mechanism.** A symplectic split with step h conserves a shadow Hamiltonian H̃_h, not H. Changing h at a state where H − H̃_h is large switches to another conserved quantity, so the difference stays as a permanent offset. In the Hill zone the perturbation is comparable to the drift's own force (ε ≈ 1), so H − H̃_h is large, about 10⁻⁶.
- **Ablation.** With the star doll's step fixed (`OM_FIXED_STEP=39`) and nothing else changed, the median exponent falls from **0.795 to 0.245**, and the rms of jumps away from handoffs falls from 6.5×10⁻⁶ to 3×10⁻⁷.

**1.3 The second cause: the handoff.** A ship is captured at R_soi/4 at the start of a level-1 or level-2 sub-interval. At that moment the level-0 and level-1 midpoint kicks are only partly spent, and the plan is cleared. The ship is released at R_soi, at a boundary. The two dolls' splits conserve different shadow Hamiltonians.

| Configuration (star step fixed at 2³⁹) | Handoff jumps, median | Bias | Exponent |
|---|---|---|---|
| shipped handoff | 1.7–1.8×10⁻⁶ | +0.6 to +1.9×10⁻⁶ | 0.245 |
| synchronised capture (`OM_SYNC_CAPTURE`) | 0.5–1.8×10⁻⁶ | +0.5 to +2.8×10⁻⁶ | 0.536 |
| plus symmetric release at R/4 (`OM_RELEASE_SHIFT=2`) | 1.6×10⁻⁶ | +1.5×10⁻⁶ | 0.314 |
| plus the planet doll's step 2³³ instead of 2³⁵ | unchanged | | 0.624 |
| plus a 4× finer star step (2³⁷), 8 ships | **1.2×10⁻⁷** | none left | 0.159 |

- A 4× finer star step cuts the handoff jumps 15×, about h², and their bias disappears. Jumps away from handoffs fall to 5×10⁻⁹, about h³: the kinks of the C¹ smoothstep.
- The planet doll's own step does not matter. The jump at a switch is the star split's shadow offset at the switching point, frozen in.

**1.4 The changeover alone cannot replace the handoff.** With no capture (`OM_NO_CAPTURE`), three levels do not resolve deep passes: jumps reach O(1) and 6 ships are lost. The levels and the handoff are therefore one mechanism, and both are history-dependent:
- a level is engaged by a certificate that reads the speed;
- a capture happens wherever a level boundary falls;
- a release happens at another radius.

**1.5 B13** (`runs/b13.py`, a replica of the frozen stream; it agrees with `behave`: 60/64 at steps 7 and 9).
- The four failures at step 7:
  - draw 3 (q = 33 r_p, 6 km/s) got **2 kicks for the whole flyby**: the step is a fraction of a long heliocentric period;
  - draw 31: dE error 1.26, with no handoff;
  - draws 37 and 41: errors of 0.7–3.7%, one handoff each.
- With the star step fixed: 59/64, and **every failure is marginal (1.1–2.3%)**. The catastrophic failures were the osculating step; what is left is cadence, which falls as h².

**1.6 B17 is a question about its scene's scale, not about motion** (`runs/b17res.py`, `jac b17`).
- The gate's scene puts the star and planet at sep = 100 M ("the problem is Newtonian: any value will do"). The ship then sits at 34–54 M, where GR's apsidal advance 6πM/a is 0.35–0.55 rad per orbit, and an orbit lasts about 10³ ticks against `MIN_STEP` = 128.
- The plane's controls there pump e to 0.39 and 0.83.
- The same controls at sep = 10⁴, 10⁶ and 5.27×10⁸ M stay within e ∈ [0.0499, 0.0502] and [0.0847, 0.1003]; the Newtonian reference gives [0.0499, 0.0500] and [0.0847, 0.1001].
- Six resonant cases at Jupiter's scale (2:1 and 3:2, μ from 3×10⁻⁵ to 3×10⁻³, both phases, detuned and exact): pump ratio 1.000, regimes all match, amplitude ratio 0.999–1.000.
- **Finding for the integrator** (the invariant at stake is the oracle's domain, as with B12 and B13): a law that is native to GR must disagree with a Newtonian oracle at 50 M. The gate stays frozen; the adjudication is the integrator's.

**1.7 What B12's statistic can see** (`runs/synth.py`). Planted errors were laid on accurate trajectories of the 16 ships (the replica of §2 at k = 11). Each planted error is bounded and a function of the state only, never of its history:

| Planted error (bounded, from the state only) | Median exponent |
|---|---|
| 10⁻⁷·(e − e₀)/0.01 | 0.255 |
| 10⁻⁷·(a − a₀)/(R_H/sep) | **0.574** |
| 10⁻⁷·min(1/r₂, 5), shifted to zero at the start | 0.218 |
| a steady drift | 1.000 |

Over 2,000 periods the values are 0.21, 0.52 and 0.22. A chaotic ship diffuses in a, so any error tied to a grows in its windowed maximum while staying bounded. The gate's positive control (`scaled`: a constant offset of 10⁻¹¹) does not cover this case. **Finding:** above its 10⁻¹² floor, B12 cannot tell "bounded, a function of the state" from growth. A law passes it either by exact conservation or by keeping the offset small.

**1.8 At full radius, a lost ship is chaos, not the law.** The same 16 ships at the planet's true radius:

| Law | Worst Jacobi error | Ships lost of 16 | Which |
|---|---|---|---|
| v2 replica, k = 6 | 7.7×10⁻⁵ | 7 | {1, 2, 3, 4, 8, 13, 15} |
| v2 replica, k = 8 | 1.2×10⁻⁵ | 6 | {1, 7, 10, 13, 14, 15} |
| v2 replica, k = 10 | 1.3×10⁻⁶ | 6 | {1, 2, 5, 10, 12, 13} |
| v2 replica, k = 12 | 4.2×10⁻⁸ | 4 | {1, 2, 5, 14} |
| v2 replica, k = 13 | 1.7×10⁻⁸ | 7 | {1, 3, 5, 7, 8, 9, 15} |
| the shipped plane, step fixed | not measured | 4–5 | not measured |

- Only ship 1 is lost every time; I believe it is the seed whose reference itself passes inside the planet (Sonnet's finding), and I did not check this.
- **Main's new frozen ships** (c1e1b73: `HANDOFF_KEPT` redrawn; 44 of the 160 candidates were replaced because their reference passes inside, a rate of 28%) do not change this. Every reference among them survives, yet at true radius the v2 replica still loses 6, 4 and 4 of 16 at k = 6, 8 and 10 (worst Jacobi error down to 9.3×10⁻⁷), and the shipped plane loses 4.
- The replacement rate (28%) equals the rate at which accurate laws lose ships. The two are one phenomenon.
- `handoff.rs` itself records a closest approach that is not converged: 0.03, 7.9 and 0.07 radii at three tolerances of the reference.
- The Lyapunov time is a few encounters. Every law that is not the reference itself leaves the reference's path long before 200 periods, and then meets the planet at the dynamics' own rate: 25–45% of seeds over 200 periods, against the reference's 1 of 16.
- This is not a bias of the law. A frozen ship was selected for a reference that converges between tolerances, which favours paths without deep passes.
- **Finding for the integrator** (the invariant at stake is the oracle's domain, behaviour against trajectory): since c1e1b73, B12 at true radius counts a ship lost outside the planet as a failure. That judges survival along one chaotic path, which no law other than the reference can reproduce. "The plane fails B12 with ships lost outside the planet" therefore says nothing about the plane's motion. This memo judges B12 on the exponent at radius ×10⁻³, as the coordinator asked.

**The mechanism in one sentence.** The plane conserves no single quantity: through the period-based step, the hysteresis, the alignment stubs, the level certificates and the asymmetric handoff, every encounter re-chooses the conserved shadow Hamiltonian. Each choice leaves an offset of O(h²ε) with a random sign and a bias, so the error grows with an exponent between 0.5 and 1.

## 2. The representation

**The question.** It is not "how many kicks", nor "which doll". It is: *what single Hamiltonian, in which variables, makes the step a property of the state, so that nothing in the law depends on history?* The answer is old and comes from the few-body problem, where it has been run for decades: the Poincaré time transformation in extended phase space, in its separable form (Mikkola and Tanikawa 1999; Preto and Tremaine 1999). Here it is applied to the plane's own split, with the dominant body's drift kept exact.

### 2.1 State
Body i, in its doll D, holds:
- its tube (the drift, exact, as today) with the offset and the turn;
- **p_t**, an integer energy register, minus the body's energy in D's frame;
- **s**, its fictitious clock, a count of ticks;
- the carries.

The event (t, x) and the four-momentum (−p_t, p) are the coordinates on which every frame change acts.

### 2.2 One Hamiltonian per body
In D's frame:
```
K = H_D(x, p) − U_P(x, t) + p_t ≡ 0            H_D: the doll's geodesic Hamiltonian (Kepler in the weak field)
U_P = Σ_j gm_j/|x − x_j(t)| − origin's fall − parent's tide potential   (> 0 after the offset c below)
Γ = f(H_D + p_t + c) − f(U_P + c),     f'(y) = 1/y² + 1/(b·y),     Γ ≡ 0 on K = 0
```
Γ is K reparametrized: on K = 0, dt/ds = f'(U_P + c). Γ is separable: its first term depends on (x, p) only through H_D, and its second only on (x, t). So both flows are exact:
- **Drift** D(σ): along the tube for a physical time Δt = σ·f'(E_tube + p_t + c). E_tube is the tube's constant and p_t does not change during a drift, so Δt is known when the step starts and the next event's time is exact in advance. This is the compiled geodesic, so the drift is zero work and exact.
- **Kick** Kc(σ): with w = σ·f'(U_P + c), Δp = w·∇U_P and Δp_t = w·∂_tU_P = −Σ_j v_j·Δp_j (minus the work of each source's motion). Both read the sources' tubes.

**One step** is Φ = D(Δs/2)·Kc(Δs)·D(Δs/2), with Δs a dyadic constant of the body. Φ is symplectic in (t, x; p_t, p) and time-symmetric. **There is no choice of step**: near a secondary the physical step shrinks as 1/U_P² and then, for U_P > b, as 1/U_P (Sundman's dt ∝ r), all through one smooth function of the state.

**Constants, derived from dimensionless numbers and not fitted to a gate:**
- c_j = gm_j/R_H,j: the secondary's potential at its Hill radius, where it stops being negligible. A floor above the largest |origin's fall·x| (10·μ/sep in the replica) keeps U_P + c > 0.
- b = 30·c: the passage from d² to d refinement at about R_H/30.
- Δs = 2^−k·P_D/f'(c): 2^k steps per period of the doll's secondary, far from it.

In the float replica these were first choices, not tuned, and a short sweep (§2.5) shows the B12 exponent does not follow them monotonically.

### 2.3 What is exact by construction
- **No history.** Φ is a fixed map: there is no step choice, hysteresis, level certificate, stub or anchor. The only error is the shadow offset Γ̃ − Γ, a function of the current state, so it cannot compound. It falls as about Δs²: the rms of encounter jumps is 4.6×10⁻⁸, 3.4×10⁻⁹, 7.2×10⁻¹⁰, 1.5×10⁻¹⁰ and 4.6×10⁻¹¹ at k = 6, 8, 9, 10 and 11.
- **Every symmetry of the sources is kept exactly** (a discrete Noether theorem: both flows are equivariant). For a planet on a circle, J = p_t + Ω·L is conserved to 3.8×10⁻¹⁵–1.2×10⁻¹⁴ relative in float over 200 periods (`ar … noether`). In integers it is conserved to one quantum per kick, and the sigma-delta carry keeps that from accumulating. B12's Jacobi constant is exactly C = 2J − 2K (checked to 6×10⁻¹⁶), so its whole error is the time-constraint residual K.
- **Kicks are bit-reversible:** v ← v ∓ F(x, t) and p_t ← p_t ∓ w·∂_tU depend only on (x, t), as in Levesque and Verlet's integer leapfrog.
- **Handoffs are exactly invertible:** see §2.4.

### 2.4 Dolls are coordinates; handoffs only for bound bodies
- **Passages need no handoff.** The time transformation resolves a flyby or a Hill encounter in the parent doll (§2.5). This deletes the capture at R/4 and the release at R for every passing ship.
- **A bound body** (a moon, a parked ship, a long capture) moves to the secondary's doll, where its drift is exact and only the parent's tide kicks it. This is about 100× cheaper: a moon at 0.3 R_H costs 490 kicks per moon orbit in the star's doll.
- **The selector is one surface, a function of the state, crossed the same way in both directions**, at a synchronised tick of s: planetocentric E_p < 0 and r < r_c = R_H/2, where the tide/pull ratio (r/R_H)³ equals 1/8. The shadow offset left by the switch is measured to scale as h² and to lose its bias when the switch is symmetric (§1.3). Under the time transformation the h at r_c is already the refined one.
- **The map is an exact Lorentz shear of the extended coordinates:**
  - the event (t, x) by Λ, which is R3's nine shears;
  - the four-momentum (−p_t, p) by the same Λ;
  - p_t is the energy component, so a frame change carries the energy register with it.

  A handoff out and back is the identity, bit for bit, and the energy bookkeeping is exactly Lorentz. Only the drift is re-bound.
- **The relativity of simultaneity is included** (the plane builder's open finding: w·r of 15, 68 and 1,400 ticks at the edges). A body's events are held in its doll's clock. The queue's key is the event's exact image in the root clock through the doll chain's shears, (t_root(event), smallest body id, kind), and never "the same tick in every doll". For slow dolls the image equals today's tick to within one tick, so their digests only shift by that much.

### 2.5 Why it passes B13 and B17, and what it does for B12 (float replica, `probe/ar`)

| Law | B12 median exponent | B12 worst error | Kicks per ship per period | B13 within 1% | Regular moons over 2,000 P |
|---|---|---|---|---|---|
| shipped plane, step 7 (radius ×10⁻³) | 0.795 | 1.5×10⁻⁴ | 220 | 60/64 (worst 1.26) | not measured |
| Wisdom–Holman, fixed P/64 (control) | 0.574 | **41.9** | 72 | 11/64 even at P/4096 | not measured |
| v2, k = 6 (LogH, f = ln) | 0.34–0.47 | 4.4×10⁻³ | 78 | 15/64 at k = 7 | not measured |
| **v2, k = 6, composite f, b = 30c** | 0.47 | 4.9×10⁻⁵ | 85 | 16/64 | **bounded (exponent 0.001–0.005)** |
| v2, k = 8 | 0.57 | 1.2×10⁻⁵ | 293 | **61/64 (worst 1.4%)** | not measured |
| v2, k = 9 | 0.60 | 3.5×10⁻⁶ | 587 | **64/64 (worst 0.34%)** | not measured |
| v2, k = 11 | **0.185** | 2.6×10⁻⁷ | 2,319 | not measured | not measured |
| v2, k = 13 | −0.12 | 1.7×10⁻⁸ | 9,128 | not measured | not measured |

On main's new frozen ships, at radius ×10⁻³:

| Law | Median exponent | Worst error | Lost |
|---|---|---|---|
| plane, step 7 | 0.793 | not measured | 1 |
| plane, step fixed (`OM_FIXED_STEP=39`) | 0.389 | not measured | 0 |
| v2, k = 6 | **0.246** | 7.7×10⁻⁵ | 0 |
| v2, k = 8 | 0.729 | 1.7×10⁻⁵ | 0 |
| v2, k = 10 | 0.777 | 9.3×10⁻⁷ | 0 |

The exponent does not follow accuracy, as §1.7 predicts.

- **B13 passes by mechanism.** The physical step near the planet is f'(U_P)·Δs, whatever the heliocentric period. A near-parabolic flyby is no longer starved (the fault law.md's "Perturbed motion" names). At k = 8 a flyby costs 150–190 kicks, against the plane's 110–160; at k = 9 it costs twice that.
- **B17 passes by mechanism at a scale where its Newtonian oracle holds.** There is no averaging and no state-dependent switch, so the resonant phase feedback is kept. Today's split already keeps it at 5×10⁸ M (§1.6).
- **B12: every source of compounding measured in §1 is removed.** The per-encounter jumps are 10²–10⁵ below the plane's (4.6×10⁻⁸ at k = 6 to 4.6×10⁻¹¹ at k = 11, against 5.4×10⁻⁶), and regular satellites at 0.3 and −0.5 R_H stay bounded over 2,000 periods, by decade: 5.4×10⁻⁷ → 5.5×10⁻⁷ → 5.5×10⁻⁷. On the chaotic B12 ships the exponent wanders between 0.19 and 0.79 as k changes; over 2,000 periods the decade-to-decade growth ratio is 1.8–3.9, between bounded and random walk. This is what §1.7 predicts: a bounded offset on a diffusing ship looks like growth to the gate. **So v2 makes B12 small by mechanism, not zero by construction.**

### 2.6 Why "zero by construction" would be engineering here
C = 2J − 2K:
- J is exact (§2.3);
- K is the residual of the time constraint.

Removing K without breaking J needs a projection direction that keeps J, which is the velocity in the rotating frame. That direction exists only because the planet's orbit is circular. It vanishes at the zero-velocity points of horseshoe orbits, and a system of several planets has no such direction at all. Every other projection moves the error from K into J. So an exact Jacobi constant means building the restricted problem's symmetry into the law: the discrete-gradient path the Opus math memo already rejected. I don't know a general form that makes K exact. A symplectic-energy-momentum step (Kane, Marsden and Ortiz 1999: Δt solved each step so that K stays zero) is the one candidate. It is known to fail where dU_P/dt = 0, which is every closest approach. It is listed in §4 as a probe, not recommended.

### 2.7 The other requirements
- **Gravity travels at c.** U_P and ∂_tU_P are read from each source's version as the body's past light cone last saw it (R5's cursor), so the clock itself is causal. q-gravity-at-c found that news equals instantaneous gravity to 10⁻⁷ for free-falling planets, so B12 and B13 are unchanged.
- **Rotating holes (B19).** The drift is the compiled Kerr tube, and Δt comes from that tube's E. χ is invisible to the split, and χ = 0 keeps every digest.
- **Zero work for quiet orbits.**
  - With U_P ≡ 0 there are no kicks: a tube is read, never stepped.
  - A body far from every secondary (U_P < c/2^m) may re-derive its Δs from its own period. That is a schedule, not physics: each change leaves an offset of O(ε_far·h²), as in the far field of §1.1. It is the only place where hysteresis remains.
  - Stable hierarchical bodies keep R2's secular phasors.
- **Every body is real.** Each body has its own s, p_t and tube. Nothing is averaged.
- **The state between kicks** is the partial step Φ_σ, with σ solving t(σ) = t_read: a pure function, which converges in a few Newton steps because t(σ) is almost affine. This replaces the ramp.

## 3. What it deletes; whether it stays exact in integers

**Deleted** (in `crates/universe`):
- `step.rs`:
  - `step_for` (1/128 of the tube's period, and the special case of a passage inside a doll);
  - `aligned` (stubs, anchors, `MIN_STEP`, `MAX_STEP`) and the hysteresis in `plan_interval`;
  - `open`, the Open items and `insert`'s ranks for levels;
  - the capture at R_soi/4 in `open` and the release at the edge in `boundary`;
  - the capping of intervals by `next_exit`: a step crosses a doll's edge freely, and only bound bodies are handed off.
- `force.rs`: `LEVELS`, `RATIO`, `shell`, `weight`, `smooth`, `engaged` and `relative_speed`. What is left is `pull`, `origin_fall` and the parent's tide, plus their potentials, the time derivatives of those potentials and f'.
- `bind.rs` `Kick { len, level, dv }`, `observe::credit` and the ramp: the readout is the partial step Φ_σ.
- In law.md:
  - "at a fixed step in the drift's own phase";
  - "SyMBA's smooth changeover … recursive sub-steps";
  - "Steps are powers of two anchored on multiples of the step (block time steps)";
  - "one tick is the same physical time in every doll" (world.rs).

  Law.md's "a step tied to the body's own phase starves a near-parabolic flyby" is answered rather than worked around.

**Kept:** the tube as the drift; rebinding with its remainder; sigma-delta carries; the origin's fall; R3's shears, now acting on (t, x) and (p_t, p); the tie rule; secular phasors (R2) for stable bodies; the Fermi frame for dense fleets.

**Integers.** The law stays exact in integers:
- Δs is dyadic. w = Δs·f'(y) and Δt = (Δs/2)·f'(y) are fixed-point rationals computed by floor division from integer energies. The fractional tick of Δt is carried by sigma-delta, so the next event's tick is a deterministic function of the integer state.
- p_t is an integer register: Δp_t = −Σ_j v_j·Δp_j, from the same quantized Δp that is applied.
- J is conserved to one quantum per kick, with the remainder carried.
- Kicks and handoffs are bijections of integer words, so they are bit-reversible.
- **The drift is not bit-reversible:** a re-bind re-fits, and I don't know a cheap bit-reversible drift. q-changeover measured that reversibility and bounded error are different properties, and B12 needs only the second.
- The jet red-team (20261006-0346-redteam-df81, gold) applies unchanged: the tube's E and L must be the exact anchored values, re-anchored by an exact recompile when the offset reaches √(floor/C). v2 reads E_tube for Δt, so a jet's error would enter the clock. Peters' a(t) is a generator of the drift, not a kick.

## 4. The cheapest falsifying probes (each under 60 s on the M1; frozen before the first run)

| # | Probe | Kills v2 if | Who |
|---|---|---|---|
| P1 | v2 in the plane's integer law, root doll only, no handoff (§5 step 1): `behave --law plane --gates B12,B13`, plus this folder's `jac` at radius ×10⁻³ for the exponent (lost ships are chaos, §1.8) | B13 < 64/64 at twice today's kicks per flyby, or B12's worst error > 10⁻⁴ at radius ×10⁻³, or B12's per-encounter jump rms not at least 10× below today's 5.4×10⁻⁶ at equal kicks per period | Astra |
| P2 | B12's statistic on planted errors that are bounded and depend only on the state (`runs/synth.py` ported as a planted law in `laws.rs`: echo plus 10⁻⁷·(a − a₀)/(R_H/sep)) | the planted law **passes** B12 (then §1.7 is wrong) | Sonnet; adjudication by the integrator |
| P3 | J = p_t + Ω·L over 200 periods on B12's ships, in integers | \|ΔJ\| grows beyond 2 quanta per kick, or with any trend | Astra (unit test) |
| P4 | regular satellites at 0.3, 0.5 and 0.9 R_H, prograde and retrograde, 2,000 planet periods in the planet's doll: the decade ratio of the median Jacobi error | ratio > 1.3 on any of them (bounded is about 1, a random walk about 3.2) | Astra |
| P5 | a ship captured and released 10³ times through the single surface, at β = 0.01, 0.3 and 0.9 for the doll | the integer state, the event or p_t is not the identity, bit for bit | Astra (extends R3's test) |
| P6 | a relativistic doll (w = 0.5c) with 10³ members: every event's root key equals the shear image of its doll event, and the queue's order is the same under 1, 4 and 8 threads and both orders | any mismatch | Astra |
| P7 | cost: kicks per ship per period on B12 and B13, and µs per kick on the M1 with the machine's state recorded, against today's 220 per period and 29 µs | more than 2× today's kicks at equal B13, or µs per kick more than 1.5× | Astra |
| P8 | the SEM step (§2.6), float, in `probe/ar`: Δt solved each step so that K = 0 | a solution is missing at more than 1% of steps, or B13 or B14 apsides worsen | GLM, optional |

P2 runs first and costs nothing to Astra. It tells the integrator whether B12 can certify "errors never compound" above its floor, before Astra is asked to pass it.

## 5. The build brief for Astra (one window; the steps in order; each step merges only on its gates)

**Contract.** Read §1 and §2 of this memo and law.md's "Perturbed motion", "Handoffs are Lorentz" and "Ties". The law is fixed above; the constants are derived as in §2.2 and are never fitted to a gate. Every gate is frozen. Work in `/private/tmp/emergent-wt-motion2` on `wt/motion2`. The ablation copy in `artifacts/runs/opus-motion/probe/` is evidence, not code: build from `crates/universe`.

1. **The extended state and the time-transformed step, root doll only.**
   - Files: `body.rs` (p_t as an i64 word with an exponent, a carry for Δt, Δs as a power of two per body), `force.rs` (U_P and ∂_tU_P beside the force; f'; delete the levels), `step.rs` (`plan_step`: one kick at mid-s, a boundary at the next s-tick; delete `step_for`, `aligned`, `open`, the levels and the capping; keep the crash plan), `universe.rs` (the queue receives physical event ticks; nothing else changes).
   - Capture is disabled for passages: in this step every ship stays in the root doll.
   - Tests: P3; a unit test that the kick and the unkick return the identical words; that U_P ≡ 0 gives zero events (B9); the far-field step equals Δs·f'(c).
   - **Gates:** B12 and B13 (P1), B9 (crossings, zero work), B1–B5, B7 and B11 unchanged (single-mass digests have no kicks), B8 (determinism: threads, orders), B16 and B19 (χ = 0 digests).
2. **The readout between kicks is the partial step.**
   - Files: `observe.rs` and `bind.rs` (delete the ramp and `Kick`); `view.rs` and `encounter.rs` read through it.
   - Tests: the readout at a step boundary equals the state bit for bit; the readout is monotone in t; the plane's adapter tests in `xtask/src/behave/plane.rs` (far ship, H² cadence).
   - **Gates:** B12 (its P/8 samples fall between kicks), B13, B16.
3. **Bound bodies only: the single-surface handoff on extended coordinates.**
   - Files: `step.rs` (`maybe_capture` and `release`: one predicate, E_p < 0 and r < r_c, checked at s-boundaries, the same in both directions), `lorentz.rs` (a boost of the event (t, x) and of (p_t, p), three plus three shears, beside R3's velocity shears).
   - Tests: P5; a moon born in the planet's doll never leaves (B14's circular births).
   - **Gates:** B14 (Hill: classes and apsides), B12, B13, B17 on the scenes inside its oracle's domain (as the integrator adjudicates §1.6), and P4.
4. **The queue key is the root image of each event** (the relativity of simultaneity; the plane builder's finding).
   - Files: `world.rs` (delete "one tick is the same in every doll"), `ctx.rs`, `universe.rs` (key (t_root, id, kind)), `fleet.rs` (the Fermi frame's members keep their frame's clock).
   - Tests: P6; ties under a relativistic doll.
   - **Gates:** B8 and B12/B13 unchanged within a tick.
5. **Next window, not this one:**
   - gravity as news (U_P, ∂_tU_P from R5's cursor);
   - Peters' generator;
   - re-anchoring the jet;
   - secular phasors for stable bodies (R2);
   - the far-field Δs re-derivation of §2.7.

**Stop rule.** Kill v2 and re-derive it from the goal if P1 fails, or if steps 1–3 pass no new gate in two consecutive windows. A failed P1 kills this configuration (the composite f, b = 30c), not the method: try f = ln first (Preto and Tremaine), then report.

## 6. The lab results folded in, and what I reject

- **Kept from the lab and the Opus math memo:**
  - R3, extended from velocities to (t, x) and (p_t, p);
  - R5's cursor for U_P;
  - R2's phasors for stable bodies;
  - JANUS's result that position-only selection is reversible (the single surface for handoffs);
  - "correctors buy nothing": v2 adds none.
- **m-meso-motion-15d6 (the encounter as one exact pair-flow event).** Rejected as the mechanism for B12 and B13. Its own checker measures 1–15% impulsive error and 60–100% ΔE on B13's deep flybys, and refinement makes it worse. The event is also a switch: a change of splitting at a state-selected time, which is the class measured in §1.3 to compound. Kept: its dimensionless number U/√(μ_p/b), as a diagnostic in the dashboard, never as a switch. v2's f'(U_P) covers both the impulsive regime and the shear regime with one smooth function.
- **m-spacetime-498b (superposed contravariant Kerr–Schild fields).** Outside the motion law; it answers what the cells hold. One dependency: v2 needs a scalar U_P and its ∂_t from the field representation, and Σ fᵢ/2 provides them in the weak field. Kept: its exact dyadic rapidity grid for thrust (which law.md already decides). Rejected for now: nothing, but its retarded kᵢ breaking the gradient structure (its checker's point 2) must be probed before cells feed U_P.
- **q-candidate-degree-5695 and taleb-09b5 (encounter certificates; gold for formations).** Orthogonal to the motion law. They decide contacts between ships, while U_P holds only massive sources (secondaries, the parent, cells). Two interactions:
  - a kick under v2 changes a body's orbit, so the arming tier re-arms that body's candidates. The sound variant, not the slack rule;
  - a fleet in formation is a Fermi frame (dense order), so the phase-neighbour certificate (rank ≤ 4) belongs there.

  Their e > 0.7 tightening hole and the horizon-edge misses must be fixed before either feeds the plane.
- **redteam-df81 (the jet).** Folded in §3: the clock reads E_tube, so re-anchoring is required, and so is Peters as a generator.
- **Rejected here:**
  - A projected exact Jacobi constant, along the rotating-frame velocity (§2.6). It engineers the scene's symmetry, degenerates at zero-velocity points, and does not exist with two planets.
  - The minimal repair of today's design: a fixed step with a symmetric, synchronised handoff (§1.3, exponent 0.159–0.314). It works only by keeping the step and the handoff small, so it is small by tuning, and it does not fix B13's cadence by mechanism.
  - More changeover levels: §1.4.
  - Higher-order kernels: six lab runs.
- **I don't know:**
  - whether the integer v2 reaches B12's 0.2 at a cost close to today's. In float the exponent stays 0.2–0.8 above the floor, and §1.7 explains why;
  - whether a bit-reversible drift exists cheaply;
  - whether the SEM step (P8) is usable;
  - how v2 behaves for B13 in integers at k = 8 (only float was measured);
  - the Fermi frame's members under v2: untested.
