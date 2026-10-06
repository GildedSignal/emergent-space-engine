# Mathematical representations: the taste pass

Claude Opus, read-only thinking agent, 5 October. The five GLM runs (`lab/lenses/m-*.md`) do the broad survey. This memo covers fewer candidates, in more depth. Method: list what the engine actually does, find where each operation is trivial, then search for that representation. Five probes ran here (`p1`–`p5`, each under 15 s, on Julien's M1 Air: battery, load 1.8–5, swap 4.6 of 6.1 GB). Their outputs are next to them (`p*_out.txt`).

**Bottom line.**
1. The engine's dominant cost is the kick: fit, compile and readouts. In weak fields the kick works in the wrong representation. Every kick integrates numerically, with Gauss panels, functions whose antiderivatives are Kepler's equation. **R1** removes this.
2. For stable bodies the right question is not "how many kicks per orbit" but "which part of the perturbation can be integrated exactly, and in which variables". In the secular variables it is rotating phasors, which need zero kicks. They also keep a belt's program valid. Kicks and memory are one problem (**R2**).
3. Frame changes become bit-reversible and exactly Lorentz if each one is three integer shears (**R3**).
4. Category theory gives one habit and three structures, the most useful being R4. Set theory gives nothing we can use directly.

## 1. Set theory and category theory, answered directly

**Set theory: no.** Its content (ZFC, cardinals, forcing, the continuum) concerns infinite objects and foundations. This engine is a finite, constructive integer computation, so nothing in set theory deletes compute or exposes a symmetry here. Three of its neighbours do touch us, and we already use two of them.
- **Order theory.** Causality is a partial order. The tie rule (law.md "Ties") is a linear extension of it. What a body can know at an event is a downset of that order, and on each source's history that downset is a prefix. That is R5.
- **Finite combinatorics.** A set of N bodies needs log₂ N! ≈ N(log₂ N − 1.44) bits less than a sequence of the same bodies. `crates/shipmem` already takes this saving where order carries no information (Elias–Fano scars). Law.md's "identity is provenance" deliberately pays for order where history needs it. That choice is right and needs no theory.
- **Causal set theory** (Bombelli, Lee, Meyer and Sorkin, 1987): spacetime as a locally finite partial order. Its vocabulary fits our event graph. Its dynamics (random sprinklings, sequential growth) does not give GR geodesics cheaply. Take the vocabulary, not the physics.

**Category theory: not as a framework. It contributes one habit and three structures, each cheaper to use by name than through the theory.**
- **The habit:** write every claim of the form "same law at every scale" or "same bits whatever the order" as a commuting square, and test the square bit for bit. Our squares:
  - coarse-grain ∘ evolve = evolve ∘ coarse-grain, wherever a regime claims it (a doll's moments; R2's forced phasor);
  - the gather after the sparse order = the gather after the dense order;
  - handoff ∘ handoff⁻¹ = id (exact under R3);
  - replay ∘ log = run.

  B8 is already one of these squares. Writing the rest makes each claim a test.
- **Monoid homomorphisms.** Aggregation (mass moments, the horizon ledger, digests, population byte counts) must be a homomorphism from the free commutative monoid of bodies. Integer addition is one. Float addition is not, because it is not associative. That is the structural reason "integers decide", and it says which reductions may run in any order on any thread: exactly the homomorphic ones.
- **The trace monoid** (Cartier and Foata, 1969; Mazurkiewicz, 1977): the algebra of events that commute when they are independent. It turns B8 from an empirical test into a local proof obligation, and its normal form is the canonical parallel schedule. See R4.
- **Lenses (optics):** observation is a "get" with no "put". That is already a rule ("observation never writes"), and nothing more is needed from it.
- **What it does not give:** a representation of any physical operation (orbits, light, contacts, frame dragging), any speed, or exactness. Operads, polynomial functors, sheaf cohomology and wiring diagrams would add vocabulary and text (principle 11) and delete no compute. My advice is not to restate the engine in categorical terms.

## 2. Representations, ranked

Ranked by gain × probability ÷ cost of adoption. The first two attack the plane's measured dominant cost: kicks take about 24 µs median, of which 15 µs is the rebinding fit and compile. Every kick compiles a new shape, so the exact memo hits 0% (`sol-kick`, dbd4add).

### R1. The weak-field tube is Kepler's equation: the eccentric anomaly, or universal variables

**Operation:** compile, kick (rebind) and read out every tube with q = M/R small. That is every planet, moon, ship and asteroid outside a black hole's or neutron star's inner zone.

**Representation.** Use the crate's own variables: x = R/r = k + (1−k) cos ψ, with k = 1/(1+e), q = M/R, and ψ Darwin's phase. The radial motion is exactly sinusoidal in ψ at every q, by construction. The crate's weak branch (`orbit.rs` `weak_quad`, q ≤ 2⁻¹⁸) integrates the first-order integrands with Gauss panels: g = 1 + qA/2 with A = 6k + 2(1−k) cos ψ, t′ = 3√k/x, and τ′ from ENVELOPE.md. Change variable to the eccentric anomaly E, defined by tan(E/2) = √((1−e)/(1+e)) · tan(ψ/2). Every integral then has a closed form (times in units of R^{3/2}):

```
φ(ψ) = ψ + q[3kψ + (1−k) sin ψ]                     + q²·(3/8)∫A²dψ   (A² is a trig polynomial)
t(ψ) = α(E − e sin E) + βE,        α = k^{-3/2}(1−e²)^{-3/2},  β = 3q k^{-1/2}(1−e²)^{-1/2}
τ(ψ) = (1 + q(2k − c))·α(E − e sin E) + (β/3)E,      c = (3k² + (1−k)²)/(2k)
```

Hence t = (α+β)(E − e_t sin E), with e_t = αe/(α+β). This is exactly Kepler's equation, with Damour and Deruelle's "time eccentricity" (1985, test-mass limit). It is the same structure the GR oracle already uses (`xtask/src/gr_oracle_extended.rs`).

The operations then become:
- **Readout:** ℓ = t/(α+β), then solve E − e_t sin E = ℓ (Newton, 1–5 iterations), then ψ by the half-angle, r = R/x, and φ(ψ). There are no knots and no panel searches.
- **Kick (rebind):** from the integer state:
  - h = x·v_y − y·v_x;
  - the Laplace vector gives e and ϖ;
  - the energy gives a, so R and k follow;
  - the first-order root corrections are closed form (a series in q; I did not derive them here);
  - E comes from the position;
  - the periapsis time is t_p = t − (α+β)(E − e_t sin E).

  There is no root bisection, no quadrature and no catalogue entry.
- **Gather:** the past-light-cone root t_obs − t(E) − |X − x(E)| = 0 is a one-dimensional Newton in E with analytic derivatives. In the far field it is the Damour–Deruelle pulsar timing formula: the Rømer, Einstein and Shapiro delays, each closed form in E. Pulsar timing works at nanosecond precision, so this representation has been proven where precision carries real consequences.
- **Unbound passages:** take E → iH (hyperbolic). Stumpff's universal variables (Goodyear 1965; Shepperd 1985) give one formula for every k. That keeps ENVELOPE.md's rule of no orbit categories.

**Symmetry:** the eccentric anomaly is the angle of the 2D harmonic oscillator that Kepler becomes under Levi-Civita's map z = w² (Bohlin 1911; Levi-Civita 1920). This is the hidden SO(3) behind the Runge–Lenz vector. There, dt/dE = (1 − e cos E)/n is a trigonometric polynomial of degree 1, and GR at each order adds only terms linear in E plus more trigonometric terms. Darwin's ψ is the right phase for the radial roots. E is the right phase for the clock.

**What it deletes** (for q ≤ q*):
- `OrbitShape::weak_quad` (orbit.rs 297–325) and the band and panel loop for weak shapes (`append`, `bound`, 377–438);
- the weak entries of `ShapeMemo`, `QuantizedMemo` and `MemoCode` (803–905);
- `outbound_at`'s Newton-on-partial-quadrature (682–745);
- the per-binding compiled trajectory (`bind.rs`: `Tube::new(0, …)` with its own `Arc<Entry>` holding the knot vector, 25–64 and 209–227); it becomes about six words;
- for these bodies, the panel rule of law.md line 20 and the "memo keyed by quantized (E, L)" of lines 12 and 14;
- the gather's per-iteration tube readout (`view.rs` `crossing`, line 150).

P1(d) counts the work removed. The crate's rule costs at least 16 nodes per half cycle at e = 0.01, 72 at e = 0.3, 284 at e = 0.9 and 504 at e = 0.99. Each node is a cos, an i128 divide and three products. The closed form's compile has none, and its readout is a Kepler Newton with 1–5 sin/cos pairs where the crate uses panel Newton steps that each re-integrate a panel.

**Integers:** yes. Kepler's Newton step runs in Q62 with the crate's own integer `cos` and `atan` and a fixed iteration schedule. The fit needs one `isqrt`. One known trap: near e → 1 at periapsis, E − e sin E cancels. Use the series for E − sin E, as ENVELOPE.md already does when it rationalizes (g − 1)/q.

**Measured here (P1):**
- the closed forms equal adaptive quadrature (scipy) of the crate's own first-order integrands to 4.6×10⁻¹⁵ (e from 0 to 0.99);
- against exact GR, the first-order precession error is 2.4q–4.5q relative (high e to low e), and the period error at most about 13q²;
- first order holds B1 (1%) down to p ≈ 450M at every e;
- the second-order term (3/8)q²∫A² is also closed form and holds B1 to p ≈ 50M;
- B2 (0.1%) is never the binding gate: wherever first order holds B1, its period error is below 1.2×10⁻⁴.

So the compiled strong-field cycle needs to stay only inside about 50–450M of a hole, where kicks are rare and the crate's care (ISCO, whirls, capture) earns its place.

**Strongest reason it might fail.**
1. It cuts the cost of a kick, not the number of kicks.
2. Moving the switch above today's 2⁻¹⁸ makes q* a law boundary: a kick that moves a body's q across it changes the formula, by O(q*²) relative at first order. At today's switch nothing in the law's definition changes. Only the panel quadrature error disappears, so digests move at about 10⁻¹⁵.
3. The remaining kick cost may sit elsewhere: force evaluation, plan bookkeeping, or the residual.

**Cheapest falsifying probe:**
- **Builder (Rust):** behind a feature in `crates/space`, evaluate shapes with compactness 0 by the formulas above, and the fit by the closed-form elements. Run:
  - the crate's quadrature tests (closed form against panels on the frozen weak seeds; expect agreement to the panel error);
  - `behave` B1–B5 and B9 on those seeds;
  - `cargo run --release -p xtask -- universe --bench`, for the kick median and p99 and the view's frame time.

  Kill R1 if a gate that passes today fails, or if the kick median improves by less than 2×.
- **GLM (Python):** write the integer Kepler solver (Q62, table cos/sin as in `crates/space/src/num.rs`, fixed four Newton steps from a Markley-type starter). Over 10⁶ random (e ≤ 0.999, ℓ), report the bits of agreement with mpmath and the worst case. Also report the bit-exactness of the fit's round trip (state → elements → state).

### R2. Stable bodies as rotating phasors: secular eigenmodes and proper elements

**Operation:** the kicks on bodies whose motion is predictable (hierarchical, non-resonant), and the memory of the populations they belong to.

**Representation.** Use the eccentricity vector z = e·e^{iϖ}. In Binet variables it is p·(V + iW): the spatial part of each body's point on the Binet cone. Laplace–Lagrange theory is first order in mass and second order in e. In it:

```
dz_i/dt = i (A_i z_i + Σ_j B_ij z_j),      A_i = n_i (μ_j/4) α² b^{(1)}_{3/2}(α),  B = −n_i (μ_j/4) α² b^{(2)}_{3/2}(α)
z_i(t) = Σ_k F_ik e^{i(g_k t + β_k)}  +  z_free,i e^{i(A_i t + β_i)}         (forced modes + one free phasor)
λ_i(t) = λ_i0 + n̄_i t,    ⟨da/dt⟩ = 0  (Laplace: a, hence U = 1/p, is a secular invariant)
```

- The forms of A_i and B above are for a test particle inside the perturber; outside, α → 1/α and the prefactor changes.
- GR apsidal precession (3nM/(a(1−e²))) and a host's J2 add to A_i on the diagonal, so the form survives.
- Each body is real: its own a, free amplitude, free phase and λ₀ are its proper elements (Brouwer and van Woerkom 1950; Milani and Knežević's catalogues of 10⁵–10⁶ asteroids).
- What members of one doll share is the forced part: one function of a, stored once.
- Beyond first order in e, or for α near 1, use Gauss's ring method (Gauss 1818): the orbit-averaged interaction of two elliptical rings, as complete elliptic integrals evaluated by the AGM, which needs only square roots. Touma, Tremaine and Kazandjian (2009) built it into an N-ring code.

**The selector,** chosen by dimensionless numbers:
- μ, α, e;
- the distance to the nearest mean-motion resonance p:q in units of its width W_pq ~ μ^{1/2} e^{|p−q|/2}, found exactly by Stern–Brocot descent: the simplest rational in [n/n′ − W, n/n′ + W];
- the Hill distance at conjunction.

Outside the domain, the body is kicked as today.

**Symmetry:** averaging over the fast angles makes a an invariant. What remains, at low order, is linear and Hermitian in z, so it diagonalizes into uniform rotations. These are Ptolemy's epicycles, in the right variables. A distant conjunction (b ≳ 3 Hill radii) adds a phasor of fixed size A/b² to z at the conjunction longitude (Hénon and Petit 1986). So the Diophantine conjunction finder already in `crates/encounters` composes with this state.

**What it deletes,** for selected bodies:
- the 64 kicks per orbit (`step.rs` `plan_interval` and `kick`) and the rebinding at each of them;
- in `crates/shipmem`, the scars of every kicked belt body. **This is the key coupling.** Under the kick law, a belt body's tube changes at its first kick, so the belt program (0.22 bits per body, `wt/belt`) describes it only until then, and afterwards every body carries a full scar. Under phasors, the proper elements are the program's own columns and never change in the secular regime, so the program stays the generator and the scars stay zero until a real surprise. B18 belt's assumed churn of 10⁻² per epoch would be about 100% per 1/64 orbit under today's kick law;
- per-kick candidate re-sets for encounters (law.md line 36). Between two phasor bodies, the Binet cone condition ΔU² ≤ ΔV² + ΔW² changes only at roots of a trigonometric polynomial. That gives one closed-form certificate per pair per secular cycle;
- law.md line 29's "orbit-averaged kicks on stable orbits": the averaged system has a closed-form solution, so they become no kicks at all.

**Integers:** yes.
- Phases are integer accumulators that advance by wrapping addition: exact forever, the numerically controlled oscillator of radio engineering.
- cos and sin come from the crate's tables.
- Laplace coefficients come from their hypergeometric series in fixed point.
- The modes (one small eigenproblem per doll, at a surprise) come from fixed-point Jacobi rotations.

**Measured here (P2).** Scene: Sun and Jupiter (e = 0.048) with 24 test bodies, over 161 Jupiter orbits. Truth was converged Wisdom–Holman at two steps (they differ by 1.25×10⁻⁴ in z).

| Zone | Precession rate | e-vector error (fraction of free amplitude) |
|---|---|---|
| Inner belt (2.20–2.35 AU) | 0.4–3% | median 0.2–3% (worst 6%) |
| Middle (2.62–2.70 AU) | 7–26% off | 2–10% |
| Outer (3.05–3.15 AU) | 16–65% off: first order fails | |
| Controls at 3:1 and 5:2 | 12–387% off: all six fail at a 5% tolerance | 5–129%; one 5:2 seed at e = 0.2 would pass an e-vector-only test (5%) |

So the selector must work from resonance widths, never from outcomes.

The phase (λ) error is a deterministic linear drift, the same error type as the compiler's period error:
- with the osculating n: 0.02–2.9 rad over the run in the inner and middle belt, up to 12.7 rad in the outer belt;
- with n fitted over the first three synodic periods: 0.02–0.5 rad in the inner and middle belt.

So a body's mean elements should be set from one synodic period of the exact law at its last surprise.

**Strongest reason it might fail.** The domain may be small where it matters. Real belts are laced with high-order resonances and secular resonances (ν₆ at the inner edge). If the exact selector can admit only a minority of bodies, the gain shrinks to that minority. Second: a resonant body admitted by mistake silently loses its phase feedback, which is exactly r4's failure and B17's planted law (Laplace–Lagrange is B17's negative control: `xtask/src/behave/resonance.rs:362`). Third: first-order theory is not enough beyond about 2.6 AU. Second-order or Gauss-ring averaging would be needed there, and I did not measure that.

**Cheapest falsifying probe (GLM, at most 120 minutes; each script at most 60 s).** Extend `p2_secular_phasors.py` to:
- Jupiter and Saturn (with their mutual modes) and 1,024 belt bodies on 2.0–3.3 AU, e ≤ 0.25;
- three laws: first-order Laplace–Lagrange, exact double averaging (Gauss rings, quadrature over both mean anomalies), and the plane's 64-kick law;
- truth from converged Wisdom–Holman over 2,000 Jupiter orbits.

Write the selector (Stern–Brocot resonance distance with widths for orders up to 7, plus α and e) before the run.

Report:
- the fraction of bodies admitted;
- for admitted bodies, the rate error and the e-vector error;
- for rejected bodies, whether the kick law reproduces the 3:1 and 5:2 depletion;
- bytes per body after the run under each law (scars against none).

Kill R2 if fewer than 50% are admitted with the rate within 5% and the e-vector within 10% of the free amplitude, or if any admitted body was within a resonance's width.

### R3. Frame changes as three integer shears (lifting)

**Operation:** rebinding at a handoff (translation plus boost), and the sub-quantum turn of a binding.

**Representation.** A boost by rapidity η on (t, x), with c = 1, is three shears:

```
B(η) = S_t(a) · S_x(b) · S_t(a),    S_t(a): t ← t + ⌊a·x⌋,   S_x(b): x ← x + ⌊b·t⌋
a = −tanh(η/2) = p/2ⁿ (dyadic),     b = −sinh η = 2a/(1 − a²) = 2p·2ⁿ/(2^{2n} − p²) (the exact rational a implies)
inverse: the same three shears subtracted in reverse order
```

The unrounded product is exactly a Lorentz boost (equal diagonals, equal off-diagonals, determinant 1). Each shear rounds once, by exact integer division, and the inverse undoes it bit for bit. Rotation is the same with a = −tan(θ/2) and b = sin θ = −2a/(1 + a²) (Paeth 1986; the Pythagorean parametrization). A boost in an arbitrary direction in 2+1 is rotate, boost along x, rotate back: nine shears. This is the integer lifting of Daubechies and Sweldens (1998). It is also how JPEG 2000's reversible transform and every lossless codec's integer rotation work.

**Symmetry:** SO(1,1) and SO(2) are each generated by unipotent (shear) subgroups. Shears are the only linear maps that are exactly invertible after rounding, so the group structure survives quantization.

**What it deletes:**
- the Galilean handoff, `step.rs` `relative` and `absolute` (134–155), which `crates/space/src/binding.rs:30–31` and ENVELOPE.md call "the low-speed approximation". It cannot be right in a game about life near c; the 0.9c stream in ladder v7 crosses doll edges;
- `bind.rs` `turn` (97–107), a second-order rotation that cannot be inverted, and part of what the 4×i128 residual must absorb;
- a handoff out and back becomes the identity, bit for bit. Law v2's "reversible integer handoff" (HANDOFF, gravity at c) is this.

**Integers:** exact by construction.

**Measured here (P3).**
- **Round trips:** 4,000 of 4,000 exact at every β from 10⁻³ to 0.999.
- **Distance to the exact boost:** at most 2 units at β ≤ 0.5, 3 at 0.9, 8 at 0.99 and 23 at 0.999, in 2⁵⁰-unit coordinates.
- **Naive γ, γβ multiply:** 0 of 4,000 exact round trips (errors 146–31,072 units).
- **Rotation:** 2,000 of 2,000 exact. Near θ = π, rotate by π first (an exact negation), because tan(θ/2) amplifies the rounding.

**Strongest reason it might fail:** relativity of simultaneity. A boost maps an event's time too, but world.rs assumes "one tick is the same physical time in every doll". For slow dolls (planets at 10⁻⁴c) the difference is below a tick. For a relativistic doll (a fast fleet's frame), a handoff maps events, not states at a common tick, and the queue's canonical root clock needs that map. This is a real structural question, not a defect of lifting.

**Cheapest falsifying probe (builder):** replace `relative`, `absolute` and `turn` by lifted boosts and rotations. Test:
- capture then release of a ship at β ∈ {0.01, 0.3, 0.9} returns the identical integer state;
- B12 and B13 equal or better;
- B16 unchanged.

Kill R3 if B12 or B13 worsens.

### R4. The event log is a trace: independence means spacelike separation

**Operation:** scheduling by causal deadline within a frame budget, the dense order's parallel waves, and the B8 claim (identical bits for any order, budget or thread count).

**Representation.** Σ is the set of events. Two events are independent, e ∥ f, iff they write disjoint bodies and neither reads, inside its past light cone, a body the other writes. A run is an element of the trace monoid M(Σ, ∥) = Σ*/(ef ≡ fe for e ∥ f).
- **Diamond lemma** (Cartier and Foata 1969): every linearization of a trace gives the same state iff each independent pair commutes on states. That is a local check, testable on random pairs.
- **Foata normal form:** the unique factorization of a trace into steps F₁F₂…F_h. Each step is a set of pairwise independent events, and each event in F_{i+1} depends on one in F_i. This is the canonical, maximally parallel schedule. Representation.md's "parallel waves" need no window parameter: they are the Foata steps.

**Symmetry:** commutation of independent events (partial commutation). Relativity supplies the independence relation: with influence at c, the dependency DAG is the causal order restricted to interacting bodies. Julien (OCC#10): "it allows to cheaply partition compute, even gravity is light speed". The register's hypergraphs ("Drifted") come in here too: the event graph is a hypergraph, and the trace monoid is the algebra that pays on it.

**What it deletes:** B8's reliance on sampling schedules. It becomes a theorem plus a per-event-kind commutation test. It also removes any ad hoc batch window from the dense order, and puts the frame budget's "the budget changes when, never what" (plane.md foundation 7) on a proof instead of a hope.

**Integers:** no arithmetic involved.

**Strongest reason it might fail:** with today's instantaneous kicks, every member's kick reads every secondary, so within a doll the trace is nearly a chain (Foata width ≈ 1) and the parallel gain is zero. The gain arrives with gravity at c (R5). Also, the read sets must be declared exactly: an undeclared read silently breaks the diamond.

**Cheapest falsifying probe:** log the plane's events for 20 s (event, tick, bodies written, bodies read with the read tick). Compute the Foata steps under:
- (a) today's dependency;
- (b) light-cone independence.

Report events per step (median and p10), and the critical path length against the event count. Then replay each step's events in three random orders and compare digests: this checks the diamond property. Kill R4 as a scheduling representation if the median width under (b) is below 2 on both the plane and the 10⁶-ship galaxy scene.

### R5. Gravity at c as a causal prefix, kept by a cursor

**Operation:** propagating gravity as news at c (law.md "Gravity travels at c"; GLM falsifier `q-gravity-at-c`).

**Representation.** A source j's history is a chain of news events (t_k, x_k): thrust, contacts, and rebinding at a handoff. Gravitational kicks are not news: a source in free fall is felt where it is now (Carlip 2000). Body i at event (t, x) sees the prefix

```
k*(t, x) = max{ k : t ≥ t_k  and  (t − t_k)² ≥ |x − x_k|² }        (integer squared forms; no root)
```

k* is non-decreasing along i's timelike worldline, and the chain is causally ordered, so one cursor per (body, source) advances one integer test at a time: amortized O(1) per source per kick. Between news events, the field is the source's present free-fall path. After news that has not yet reached i, it is the path the source would have followed without that news (the "ghost"), until the front passes.

**Symmetry:** the past light cone of a later event on a timelike worldline contains that of an earlier one. Knowledge is a monotone downset (order theory: the useful residue of "set theory?").

**What it deletes:** nothing yet, since gravity at c is not built. It makes "gravity at c" cost one comparison per source per kick, which is about the cost of the force itself. With R4, it is also what makes the trace wide.

**Integers:** exact.

**Strongest reason it might fail:** the ghosts. For one light-crossing time the old path is a second body. In a star system that is minutes against days between kicks, so it is negligible. In a galaxy-scale doll a ghost lives for 10⁴–10⁵ years and needs its own gravitational kicks. History retention per source is also its influence radius divided by c.

**Cheapest falsifying probe** (add to `q-gravity-at-c`):
- cursor advances per kick, expected to be about one;
- agreement with a brute-force retarded search on random worldlines;
- the Laplace control: a pull toward the retarded position must spiral a circular orbit outward, while the news law holds it.

## 3. Where our representations are wrong or merely adequate

- **Wrong: the weak cycle compiled by panels.** The right question is "in which phase is the clock's integrand a polynomial?" Answer: the eccentric anomaly (R1). The crate asked "which phase makes the roots cancel?" (Darwin's ψ), which is right for the radial roots and wrong for time.
- **Wrong question: cadence.** `q-cadence` asks how many kicks each body needs. The prior question is which part of each body's perturbation is integrable, and in which variables (R2). Cadence then serves only the remainder.
  - Memory and kicks are one problem: a population stays at its information floor only if its dynamics preserve its generator.
  - The 5 October memo correction (the exact memo hits 0%; the quantized cell "changes orbits") points the same way. The quantized cell re-rounds (E, L) at every kick, which is a random walk: the wrong error type (principle 13). Do not adopt it. R1 removes the need in weak fields. In strong fields, law.md line 29's "multiply-add" is the right form: a jet. The memo sits at a lattice point of the key, the body keeps its exact offset, and the stored derivatives map that offset to the cycle's constants.
- **Adequate in the map, wrong in the readout: the state between kicks** (measured, P4b). The plane's split with dyadic, aligned per-body steps is second order and bounded: sampled where both bodies sit on step boundaries, the energy error is 2.78×10⁻⁶ at (P_J/74, P_S/46) and 1.72×10⁻⁷ at a 4× finer step, a 16× drop. Read mid-interval, the same run shows 6.4×10⁻⁵: twenty times larger and first order. That is HANDOFF's "pending half kick" (Jacobi 6×10⁻³, the ignored test).
  - **The right question: what is a body's state between kicks?** The split defines states only at boundaries. Between boundaries, read velocities on a linear ramp between the pre-kick and post-kick tubes, or Hermite-interpolate the boundary states. Both are second order.
  - The view, encounter tests and the Jacobi judge should all read that.
  - Keep anchors on multiples of each body's power-of-two step (block time steps, as in Aarseth and Makino), so every pair has common boundaries. With incommensurate or offset anchors there were none, and I could not separate the map's error from the readout's (I don't know).
- **Adequate (measured; my suspicion withdrawn): heliocentric coordinates with the origin's fall.** I expected the indirect term to break symplecticity for massive secondaries and walk the energy. Over 3,000 Jupiter orbits it does not:
  - heliocentric 3.9×10⁻⁷ against democratic heliocentric (Duncan, Levison and Lee 1998) 1.9×10⁻⁷;
  - with masses ×10, 3.6×10⁻⁶ against 1.7×10⁻⁶;
  - every growth exponent is at most 0.04 (P4).
- **Wrong for high c: the handoff boost is Galilean** (R3).
- **Merely adequate: the residual, and a compiled trajectory per binding.** Each binding owns an `Arc<Entry>` with a full knot vector (`Tube::new(0, …)`) and a 4×i128 residual (64 bytes). The residual's actual information is unknown to me.
  - Probe: histogram the residual's bit lengths over a plane run.
  - Under R1 the weak entry shrinks to about six words. Under R3 the turn stops leaking into the residual.
- **Adequate, confirmed: Kerr** (P5, sympy). In Mino time (dτ = r²dλ at the equator):
  - (du/dλ)² is the same cubic as Schwarzschild's, with L² → L² − a²(E² − 1) and 2ML² → 2M(L − aE)²;
  - dφ/dλ = (L − 2Mu(L − aE))/(1 − 2Mu + a²u²), and dt/dλ is rational too.

  So Darwin's ψ carries over unchanged and only the integrands change: law.md line 31's claim, made precise for Astra's compiler and `q-kerr-compile`. In weak fields the Lense–Thirring term is one more closed-form term in E (R1).
- **Solved, and one step from native: the Fermi frame's tide.** `q-fermi2-tide` found Marck's tetrad: a rational core plus one angle Φ, with dΦ/dφ rational. Make Φ the sixth column of the cycle's integrals (`Integral` holds five), so a tube carries its tidal frame's advance per cycle as an addition.
- **Adequate:**
  - the belt's tails: Sol's dyadic survival bands are the right water, because a survival's exponent is a leading-zero count;
  - the Binet cone plus continued fractions for encounters (R2 makes its changes certifiable in closed form);
  - min-plus and the slack queue;
  - the compiled strong-field cycle.

## 4. Rejected, so the survey need not re-propose these

- **Full closed forms for strong-field cycles** (Hagihara's Weierstrass solution, Carlson's integrals, Fujita and Hikida's Kerr solutions in Mino time): correct, and the EMRI community uses them. But the panel compiler already passes there, and kicks are rare in the strong field. Integer AGM or Landen loops would bring their own error analysis. Revisit only if strong-field compiles show in a profile.
- **Levi-Civita or KS regularization as the engine's drift:** a kick is linear in Levi-Civita velocity, which is attractive. But fictitious time must be mapped back to coordinate time by Kepler's equation anyway, which R1 already gives, and near a secondary the planet's doll is already the regularized frame.
- **A memo of Hill's encounter map** (scale-free in Hill units, Jacobi-exact by construction): it needs a three-parameter table with a chaotic core at b ≈ 1.5–2.5 Hill radii, and hundreds of MB before symmetries. Distant encounters are R2's phasor additions; close ones stay with the doll handoff.
- **Discrete-gradient or projection integrators that conserve the Jacobi constant exactly:** they work only on circular restricted scenes (B12's), which would mean engineering the law for a gate, and projection breaks reversibility unless it is symmetric.
- **Bit-reversibility as a law-wide requirement** (register: "ooooh"): `q-changeover` measured that reversibility and bounded error are different properties. Take reversibility where it is free (R3) and not as a constraint on kicks.
- **Higher-order splits and correctors:** killed by six lab runs.
- **Radix heaps and calendar queues:** already named in the original research report and docs/archive/engine.md. Use them only if the queue shows in a profile. I don't know that it does.
- **Posits and unums, residue number systems, p-adic positions:**
  - posits are floats, and floats never decide;
  - residue systems cannot compare or divide cheaply, and our predicates are comparisons;
  - the p-adic metric is not physical distance.
- **A 2D FMM in complex Laurent series:** our potential is 1/r in a plane, not log r, so the complex-analytic 2D FMM does not apply. When multipoles are built, the right one is a planar 3D FMM (spherical harmonics on the equator).
- **Quaternions** (register: "could we use quaternions", open): plane rotations are unit complex numbers, and quaternions are their 3D form, adding nothing in 2D. Split-quaternions are the 2+1 spacetime form, already adopted. R3 is how to apply either exactly in integers. This answers the register line.
- **Twistors, Newman–Penrose and Petrov types:** they add nothing in our equatorial 2+1 setting. Their useful residue (the Marck tetrad) is already in hand.
- **Regge calculus and causal dynamical triangulations:** they evolve dynamical geometry. We need geodesics on compiled backgrounds.
- **Wolfram hypergraph rewriting:** it would have to rediscover geodesics we compile exactly. The useful algebra of our event hypergraph is R4.
- **Persistent homology, information geometry, surreal numbers, umbral calculus, wider tropical geometry:** I found no engine operation they make cheaper. Min-plus is the part of tropical algebra that pays, and we have it.
- **Wavelets for multiresolution:** dyadic dolls and bands already are the multiresolution, and wavelets would compress fields we do not store.
- **Kolmogorov complexity:** uncomputable. Programs plus scars (minimum description length) is the computable form, and we have it.

## Files

All in `artifacts/runs/opus-math/`:
- `p1_weak_closed_form.py` (R1: closed forms, error against GR, q*, work count);
- `p2_secular_phasors.py` (R2);
- `p3_lifting_boost.py` (R3);
- `p4_split_coordinates.py` and `p4b_async_control.py` (§3: coordinates, asynchronous cadence, readout);
- `p5_kerr_cubic.py` (§3: Kerr, sympy).

Outputs are in `p*_out.txt`. Interpreters: `/opt/homebrew/bin/python3.11` (numpy, scipy) for P1–P4, and `/usr/local/bin/python3.11` (sympy) for P5.
