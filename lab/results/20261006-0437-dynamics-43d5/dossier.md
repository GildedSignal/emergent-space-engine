# Dossier — the encounter process as a dynamical system (dynamics lens, run 20261006-0437-dynamics-43d5)

**Claim.** In the law's own drift+kick representation (a conjunction map of a belt: exact
Kepler drift, one impulse per synodic conjunction), the steady state the design assumes —
"no work per orbit in the steady state, each pair paid once per element change"
(docs/law.md, Finding encounters; board, r8 v2 Next) — does not exist in the elastic regime:
element changes settle to a Poisson-like floor, not to zero, and at the law's own m=16 band
grid the certificate re-setup churn runs ~40–55× the real-encounter rate; separately,
fragmentation (a battle's debris) has a sharp Kessler transition at K = 2 net fragments per
contact, with growth exponent ≈ (K−2)·(contact rate), roughly linear in density.

**Bottleneck.** Board item "finding encounters without work per orbit or per element change"
and (for the fragmentation half) the smoothness bottleneck 4 / a gate we lack. The gain is not
10× compute today; it kills a design premise before it is built on, and it fixes what the
allocator may assume about surprise arrivals (principle 12).

## Model

Coplanar belt about one dominant mass (mu=1): N bodies, a ∈ [1,1.4] uniform (banded p),
Rayleigh e (sigma_e = 0.02), uniform angles — the B18b belt shape. Interactions only at
conjunctions: next conjunction time closed-form in mean longitude, positions/velocities exact
Kepler at that time, impulse |dv| = 2·m_other/(v_rel·d) along the separation (thin-lens
hyperbolic deflection, momentum-conserving, one per synodic period), exact osculating
re-referencing after each kick. Elastic mode; fragmentation mode replaces both members of a
contact (d < b_c = b_max/6) by K fragments with delta-v 3e-3. Encounters inside
b_max = 2 mutual Hill radii. m = 5e-8 (calibrated: de ~ sigma_e/4 per kick), m = 1e-8 for frag runs.

Sanity: total energy drift |<1.5e-3| over 240 orbits (elastic); zero unphysical ejections.

## Evidence (all commands ≤ 60 s except the batch waits; run in this folder)

- `python3 conjmap.py --N 768 --orbits 240 --mass 5e-8 --seed {1,2,3} --out run_elastic_s{1,2,3}.json --dump dump_s{1,2,3}.npz`
- `python3 conjmap.py --N 1536 --orbits 120 --mass 5e-8 --seed 1 --out run_elastic_N1536.json --dump dump_N1536.npz`
- `python3 conjmap.py --N {512,1024,2048,4096} --orbits 120 --mass 1e-8 --frag K --seed 1 --out run_frag_N*_K*.json` (K ∈ {0,1,2,3})
- `python3 analyze.py 'run_*.json'`, `python3 burst.py` (burst anatomy + cone-margin fraction)

**H1, the floor (held).** Kick rate per body per orbit, N=768: settles at 0.012–0.018 and
stays flat to 240 orbits (s1: first10% 0.0180 → last20% 0.0182; s2: 0.0195 → 0.0157;
s3: 0.0184 → 0.0116). It never decays to 0: elastic stirring repopulates the crossing set
forever. Rate scales ~linearly with density at fixed geometry (N=1536: 0.035–0.037).

**H2, the re-setup churn (held).** Per-body log-u quantum crossings (the band grid,
delta-ln-u = ln2/m): m=16 gives 0.0027–0.0032 per body per orbit — a body's band index flips
every ~330 orbits forever. Multiplied by the crossing-window degree (217–240 at birth,
477 at N=1536; and the cone-margin measurement on final elements shows 99.9% of overlap-window
pairs sit within ONE m=16 quantum of the Binet cone boundary, so a quantum crossing
re-examines essentially the whole window): 0.6–1.5 pair re-examinations per body per orbit
against 0.012–0.018 real encounters — **the setup work is 37–55× the encounter work at the
law's own grid** (setup_work_vs_enc_m16), and falls only as 1/quantum (cross16 vs cross32
halves), i.e. it is a random-walk floor, not a transient. The Binet cone does not sparsify
here: it is quantum-limited, not geometry-limited.

**H3, arrivals are Poisson-like, no avalanche (held).** Allan factor 1.2–2.6 (window 0.5–2
orbits) at N=768 over 240 orbits; the denser, shorter N=1536 run reaches 3.2–9.0 at the same
windows (its rate is still relaxing), yet its branching proxy stays ~0.07 — clustering, not
cascading: three orders below the supercritical control. Per-body kick-count Fano
0.85–1.04; branching proxy post/base = 0.01–0.17 vs 0.02–0.04 baseline. Estimator controls
both sides: synthetic Poisson → Allan 0.86–1.10; synthetic supercritical Hawkes (m=1.5) →
Allan ~10^4 growing with window. The allocator may treat elastic surprise arrivals as
Poisson with a slowly drifting rate; no avalanche gate is needed in the pure-gravity regime.

**H4, the Kessler transition (held, controls on both sides).** Population exponent per orbit
for fragmentation at K fragments per contact: K=0 (annihilation) decays (N2048: −8.0×10⁻⁴/orbit,
82 contacts), K=1 decays, K=2 is exactly flat (by construction: net 0 per contact), K=3 grows
(N512 +1.3×10⁻⁴, N1024 +3.5×10⁻⁴, N2048 +6.8×10⁻⁴ per orbit; 156 contacts) — the transition
is sharp in K (crosses zero between K=2 and K=3, one unit, as predicted) and the growth
exponent tracks (K−2)·(contact rate), rising with density but mildly sublinear (see the
N4096 extension below). E-folding time at this geometry is ~1.5×10³ orbits at N=2048;
a battle debris field needs on the order of 10–40× this density for a 100-orbit e-folding —
the player's wildcard can create that locally. **Gate we lack:** nothing today notices a debris
field crossing criticality; a cheap online estimator (contact rate per body × net fragments
per contact) is one multiply.

**N4096 extension (post-freeze, disclosed):** run after the sweep was frozen, to test the
density-scaling extrapolation. Measured: K3 slope +8.1×10⁻⁴/orbit (+11.8%, pop 4106→4592,
497 contacts, 109 orbits, wall-limited), K0 −1.4×10⁻³/orbit (−16.4%, pop →3416). The K3
growth series with density is 1.3, 3.5, 6.8, 8.1 ×10⁻⁴/orbit at N = 512, 1024, 2048, 4096 —
rising but mildly sublinear (≈ N^0.8). My working extrapolation of strict linearity
(1.3×10⁻³ at N4096) overshot by 1.6×; that number was briefly drafted into this dossier
before the run delivered and is corrected here — the frozen sweep's H4 claims (the transition
and its direction) are unaffected.

## The artifact I found in myself (the run's sharpest systems lesson)

My first scheduler emitted one event per *alignment condition crossing* — after each kick the
osculating re-referencing jumps the mean-longitude difference slightly past the alignment it
just fired on, so ONE physical close passage was chopped into up to 342 bookkeeping
"conjunctions" per orbit, each applying a full impulse. Symptom: Allan ~30–120 "growing with
window", branching ~30 — a fake avalanche. Fix: an event's identity is the synodic period
(one impulse per conjunction), not the alignment condition. This is the same failure class as
the plane's re-timed pending kick (taste log, 5 October: "they all re-timed one pending kick
every frame; on distinct kicks the exact memo hits 0%"): **event identity must be the physical
encounter, never a re-evaluable condition.** The engine's kick epochs and the law's
second-order ramp exist to prevent exactly this; any new event source (Binet-cone
conjunctions, Fermi-frame contact epochs) needs the same one-event-per-physical-encounter
rule, and checkers should count distinct physical encounters, not condition crossings.

## Predictions (`predictions.md`, written before the decisive runs)

- H1 held (floor, not decay). H2 held (churn 37–55× encounters, quantum-limited cone).
- H3 held on branching (<0.3) and "no avalanche"; the Allan plateau sat at 1.2–2.6 rather
  than "<2" on one seed at long windows — slow rate drift, reported as held-with-margin.
- H4 held (sharp K transition between 2 and 3; controls both sides behaved).

## What would make it wrong

The conjunction map is Newtonian, coplanar, one dominant mass, impulse-per-conjunction: it is
the regime where the Binet cone and orbit-averaged kicks apply (the law's own scope), not the
strong-field or resonant regimes; a belt locked in resonance or damped by contacts (energy
loss) could quench the stirring floor. The churn multiple assumes re-setup touches the whole
overlap window (measured: 99.9% of window pairs within one quantum of the cone) — a finer
quantum or a much more dilute belt would shrink it proportionally (1/quantum, measured).
Fragmentation K is a parameter, not physics chosen; the transition's *existence* at net
fragment production > 0 is structural (branching ratio > 1), only its location moves.

## Cost of adopting, fit with PRINCIPLES

Adoption is informational: (a) drop "no work per orbit in the steady state" from law.md's
encounter paragraph; the steady state is a stirring-set floor, so the skin/deferral design
(taleb-3ec1) must be perpetual, not wait-for-quiescence, and the quantum choice trades churn
1:1; (b) the allocator may assume Poisson arrivals with drifting rate in gravity-only regions;
(c) add a criticality readout (contact rate × net fragments) wherever debris is created.
Quotes: "Compute only surprises. Cost follows change and entropy" (3) — the floor IS the
surprise rate; "A failed expectation is not automatically a failed method" (H0183) — the
steady-state assumption failed, not the candidate representation; "make expensive work
bounded, movable, predictable, or avoidable" (plane.md §7) — the readout makes the Kessler
tail predictable.

## The lens (what it may have made me miss)

The attractor-and-burst lens nearly sold me its own artifact (the fake avalanche); it was the
unit test on synodic impossibility, not the lens, that caught it. I did not measure
Lyapunov times of the belt itself (the kick diffusion is a proxy), nor 3-D/inclined geometry,
nor the resonant belts where r4's normal form governs; the fragmentation model is
minimal-parameter and ignores fragment size distributions.
