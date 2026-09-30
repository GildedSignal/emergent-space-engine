# Encounters without work per orbit: answers before code (Opus, 30 September, 20:12 UTC)

Written before any experiment code, as the brief asks. Predictions at the end. Notation: body i has
semi-latus rectum p, eccentricity e, periapsis angle ϖ, integer period T (ticks), periapsis time t_p.

## Q1. The exact structure of a pair's relative motion in a doll

**Kepler.** Each body's position is a function of one angle, its mean anomaly M = n(t − t_p). Rotation
invariance leaves the pair on a 2-torus (M_i, M_j) with a *linear* flow of frequencies (n_i, n_j). The set
where the pair is closer than ρ is a fixed region of that torus, so an encounter is the linear flow entering
a fixed region: nothing about it changes between kicks.

**Where on the torus: the Binet cone (the representation).** The law already uses u = 1/r. A Kepler orbit is
u(θ) = U + V cos θ + W sin θ with (U, V, W) = (1/p, e cos ϖ / p, e sin ϖ / p): every orbit is one point of a
3-space. Two orbits meet at θ iff ΔU + ΔV cos θ + ΔW sin θ = 0, solvable iff ΔU² ≤ ΔV² + ΔW². **Orbit
intersection is the causal structure of 2+1 Minkowski space in Binet coordinates:** spacelike separation =
two crossings, at θ = atan2(ΔW, ΔV) ± arccos(−ΔU/R) (R = |Δ(V, W)|); null = tangent; timelike = never meet
(MOID ≈ r²(|ΔU| − R) > ρ). Bound orbits are the interior of the future cone of the origin (e < 1 ⟺ R < U).
So the candidate set is static geometry (pairs spacelike to within ε(ρ)), and the torus region is ≤ 2 small
blobs, one per crossing point P (merged near tangency, a diagonal band for nearly identical orbits).

**The section.** Sample the flow each time j passes P: times t_jP + l·T_j. At those times i's passage
through P is offset by s_l = (t_iP − t_jP − l·T_j) mod T_i. **This is an exact circle rotation by T_j on a
circle of circumference T_i**, and the encounter at passage l ⟺ s_l ∈ W_P, a small interval around 0 (width
≈ 2ρ/|v_i × v̂_rel| in time, wider near tangency). With the law's integer clock (T, t_p in ticks) the rotation
is exact integer arithmetic, so **the next close conjunction is the first l ≥ l₀ with (A + l·B) mod M ∈ [L, R]**,
which the Euclid-like recursion (continued fractions in disguise; the three-distance theorem says why the gaps
are so structured) solves exactly in O(log M) steps. No floats decide it and nothing is iterated per orbit.
The window W_P is a guide (a superset); every hit it proposes is decided by an exact per-pair closest-approach
check, and a false proposal just continues the recursion from l + 1.

**GR cycles (precession).** In the law each tube advances by integer (Δt, Δφ) per radial cycle, so a body is
two angles (radial phase, apse angle) and the pair lives on a 3-torus with frequencies (Ω_r,i, Ω_r,j, Δϖ̇). The
section at j's periapsis is an exact integer 2-D rotation (i's radial phase, the apse difference Δϖ). Because
Δϖ changes by β ≪ 1 per return, the window drifts slowly along a smooth curve: over a stretch where the curve
is linear to within the window, the problem is again a 1-D rotation with a tilted step (T_j plus the drift's
slope), solved in O(log); the stretch lasts ≈ √(ρ/(a·e))/β returns, so a pair costs O(√(a·e/ρ)) queries per
differential-precession cycle instead of zero. Negligible in weak fields (β ~ 10⁻⁷ per orbit), a few queries
per 100 orbits per pair near a black hole. The cone test itself becomes time-dependent: R² = E_i² + E_j² −
2E_iE_j cos Δϖ(t) (E = e/p), so a pair enters and leaves the crossing set at closed-form values of Δϖ, two
O(1) events per precession cycle. **Yes for Kepler, exactly; for GR, exactly per linear stretch.**

## Q2. Near-co-orbital pairs (no conjunction in the horizon)

They are not special in the section: a small |Δn| is a small rotation step, and the first-hit query is exact
for every step, including a first hit thousands of orbits away. The leak in r8 v2's truth came from sampling
only near mean-longitude conjunctions; the section samples every passage of j through the crossing point,
whether or not the guiding centres cross. Three exact sub-cases:
- **Equal integer periods** (the same memo key, so Δt_i = Δt_j exactly, common once keys are coarse): step 0,
  the pair is exactly periodic. One exact check over one period decides it until a kick: never, or at the
  same phase every period.
- **Nearly identical orbits** (|ΔU| + R < ε: the near-set is the whole orbit): section at j's periapsis,
  window from the spread of the time offset t_i(θ) − t_j(θ) over θ plus ρ/v_min; exact check over the return.
- **A pair continuously within ρ over many passages** (a formation) is not an encounter stream but a bound
  group: report entry and exit (two first-hit queries: into W, then out of W) and hand the pair to a shared
  free-fall frame, as the law's dense order already does for battles.
The truth for this experiment is brute force over all radially overlapping pairs, dense in time by rigorous
conservative advancement (a step is taken only if the bound |d''| ≤ |a_i| + |a_j| (or the tidal bound when
close) proves d cannot fall below ρ inside it), so it has no conjunction leak.

## Q3. Keeping the candidate set implicit at 10⁹ bodies

- **Sorted by U** (U = 1/p comes from the key's L; V, W from e and the tube's periapsis angle, so the tube's
  16 bytes already hold the Binet point). A body's candidates lie in a contiguous U-range
  (|ΔU| ≤ E_i + E_max + ε) and pass the cone test: enumerated on demand in O(log N + range), never stored.
- **Group envelopes** are blocks of the sorted order with bounding boxes in (U, V, W). Two blocks are certified
  disjoint forever (until a member's kick leaves its box) iff min|ΔU| − max|Δ(V, W)| > ε: timelike boxes.
  This certifies all non-candidate pairs at O(1) per block pair, and far blocks in U are never even visited.
- **Candidate pairs inside overlapping envelopes need their own timing.** Their phases are independent, so no
  group bound on (U, V, W) certifies "no hit before t" for them; only phase-structured groups (a population
  program, whose t_p are affine in the ordinal) could share one rotation, which is the lead I would test next.
- **Storage choice.** (a) Per pair, the next hit (≈ 12 B per candidate pair): zero work per orbit, but memory
  ∝ candidate pairs, impossible at 10⁹ when a body has hundreds of candidates. (b) Per body, a scan
  certificate "all my partners examined through horizon H" (≈ 32 B per body) plus the hits found (real future
  events, one queue entry each); rescan at H. Work per orbit = C_b/H, memory = r_enc·H per body, so work per
  encounter ≈ 1 + C_b/m for m stored hits per body: memory × overhead ≥ C_b. For contacts (tiny ρ) r_enc·H is
  tiny, so H can be the kick interval and (b) costs nothing per orbit.
- **A kick costs** an O(log N) move in the sorted order, a block-box update, and C_b(i) pair setups
  (closed-form crossing, passage times, window, one O(log) query), with lazy deletion of stale events by a
  per-body epoch. A per-body slack budget (half the minimum distance of the certified returns to their windows)
  lets kicks smaller than the budget skip re-certification.
- **So the cost moves from per synodic period (element-sort) to per element change.** It wins iff elements last
  longer than a candidate pair's synodic period, ≈ 1/(1.5 σ_e) orbits.

## Predictions (before code)

1. missed = 0 and false = 0 against the leak-free truth on every belt, including the adversarial narrow belt.
2. Steady-state events per body per orbit fall as 1/H toward the encounter rate; with per-pair storage at
   H = 10⁴ orbits they are within 2× of it (the rest: false window proposals ≈ 0.3–1 per hit, setup/H).
3. Setup ≈ 1 query per candidate pair, 0.3–3 µs; a first-hit query ≤ 60 recursion steps, < 1 µs.
4. A kick re-certifies C_b(i) pairs (≈ 2 × pairs / N): hundreds at N = 10⁴, σ_e = 10⁻².
5. Candidate pairs (cone) ≈ 0.6–0.8 × r8's radial-overlap set; ∝ N²·σ_e; encounters ∝ N·C_b·ρ.
6. Crossover with element-sort (its cost = conjunctions ≈ C_b·|Δn|/2π per orbit) at H ≈ 30–300 orbits.
7. The truth finds conjunction-less encounters: a few % on r8-like belts, a majority on the narrow belt.
