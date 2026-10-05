# Dossier — gravity travels at c: "news" measured against instantaneous and naive retardation

Run 20261005-1404-q-gravity-at-c-a237. All numbers: `results.json`; raw runs in `runs/`;
probe `gravc.rs` (self-contained, `rustc -O gravc.rs -o gravc`; no deps). Cloud x86/2vCPU
timings — orders of magnitude only.

## Claim

Gravity-as-news — a kick pulls toward the source's **tube version that the consumer's
past light cone last saw, evaluated at the consumer's now** — keeps every orbital
behaviour of instantaneous gravity (to 10⁻⁷ relative, for a source in free fall), delivers a
source's change of motion exactly at light-travel time, and costs ≈ 6× an instantaneous
kick and ≈ 16 B × cadence × (light time in orbits) of tube memory per source; naive
retardation (pull toward the retarded position) spirals binaries apart as Laplace said
(measured: unbound in 4–12 orbits at β = 0.1–0.3, and in ~170 orbits at β = 3.3×10⁻³).

## Bottleneck

Board item 0 (the representation) / Julien's 5 October directive: "gravity must travel
at c". This decides the kick layer's causal contract for the whole plane (law.md
"Gravity travels at c"). Gain: deletes the causality violation from the foundation at
bounded cost; nothing else needs to change — within a doll, news *is* today's
instantaneous kick (the flyby scene matches it to 10⁻⁷ relative).

## The three configurations (one mechanism, three read-outs)

Each body records a **tube version** every kick epoch: (t, x, v, a) plus pre-compiled
Kepler elements of its orbit about its dominant body (the plane's 16-byte tube + epoch).
A kick on consumer B from source S at time t solves the retarded time t_ret (light left
S), selects the newest version of S with t_ver ≤ t_ret, and:

- **instantaneous** (today's plane): pulls toward S's current position — knows the future of the cone.
- **naive retarded**: pulls toward S's position *at* t_ret (where it WAS) — Laplace.
- **news**: evaluates that same old tube version *at t* (where its known law says it IS now).

Same machinery for ret and news; the only difference is which end of the tube you read.

## Evidence

**S1 binaries (Laplace).** Equal masses, relative orbit v/c = β, 300 orbits.
| cfg | β=0.1 | β=0.3 | β=3.3e-3 |
|---|---|---|---|
| inst | bound, dE 8e-11 | bound | bound |
| ret | **unbound in 12.1 orbits, a→20** | unbound in 4.2, a→41 | a grows 0.0072/orbit, unbound in 173 (e=0.3) |
| news | bound, a=1.0006, dE 5.6e-4 | bound, a=1.0016, dE 1.6e-3 | bound, dE 2.3e-5 |

Ret's spurious apsidal precession at β=0.1 is −0.149 rad/orbit — **1.03× the 1PN
oracle** (6πGM/(a(1−e²)c²) = 0.145): naive retardation injects 1PN-sized-or-larger
error. News's is 2.5e-5 rad/orbit, 4.5 orders below the oracle. News's energy drift is
*dt-quadratic* (2.7e-3 → 6.7e-4 → 1.7e-4 as dt halves 2×, ratios 4.03, 3.94):
integrator truncation of the delayed force, not representation error — it converges away.

**S2 system (star + planet A + moon at 0.30 r_H + planet B), 95 planet orbits.**
All bodies stay bound and the moon survives for inst and news at both β; ret loses the
moon at 5.9 orbits (β=0.3) and 104.5 (β=0.1), with system energy errors 0.23/0.11.
News's max|dE| = 5.9e-5 (β=0.1), 1.4e-3 (β=0.3) vs inst floor 3.1e-6 — the difference
is the delayed news of inter-planet perturbations (real causality, small). Moon Jacobi
errors: news 4.8e-2/1.3e-1 vs inst 1.0e-1 — same class; the drift is dominated by
planet-B pumping for every config including inst (the scene is not a B12 gate; ret is
in a different class entirely).

**S3 ship crossing a Hill sphere (16 seeds).** News matches inst to **5×10⁻⁸ / 6×10⁻⁷
relative** (max |Δv∞_out| = 1.0×10⁻⁸ / 1.3×10⁻⁷ absolute on v∞ ≈ 0.2, at β = 0.1/0.3;
the residual is exactly the ship's own 10⁻¹²-pull news arriving late): an isolated
planet lies on its Kepler tube, so the light-cone-delayed tube evaluated at now *is*
the instantaneous position. This is the deep claim: for a freely falling source, gravity at
c costs no orbital behaviour at all — the aberration cancels exactly, by construction,
because what travels is the generator, not the position. Ret scatters v∞ by 2.9%/7.5%
median (6.6%/21.4% max) at β=0.1/0.3 and its Jacobi error is 3–10× inst's.

**S4 a struck source (Δv = 0.06 at t_e = 8, watcher at 6 AU, c = 3.333 ⇒ light delay 1.5).**
Twin runs (struck/free) are bit-identical (residual 5e-20) until the switch.
| cfg | onset | exact light arrival |
|---|---|---|
| news | 9.504 | 9.500 (**one step, dt=0.004**) |
| news (c=10) | 8.504 | 8.500 |
| inst (today) | 8.112 | 9.500 — reacts 1.4 time units *before* the light cone |
| ret | 10.008 | 9.500 — starts at the cone but ramps; the field after arrival is still wrong (no extrapolation) |

**Cost per kick (per pair-eval, N=1024).** inst 298 ns; ret 1545 (5.2×); news 1834
(6.1×, 1.19× ret). Linear in N (64→1024 flat at 256+). Upper bounds: the probe does a
binary search per version lookup and allocates per pass; the plane's per-pair cursor is
O(1) and its kick is already a table hit — the news *addition* is one tube evaluation +
one version select per kick.

**Memory (tube versions a light cone still sees).** One ring per source, depth =
(light window)/(kick cadence). Probe (f64, 112 B/version): 59 kB/source at c=3.33,
D=9, dt=0.005. Plane (16-byte tube, cadence 32/orbit): **20 B/source** for a
within-doll pair (0.04 orbit light time), 512 B for neighbouring planets (1 orbit),
2 kB for a 4-orbit light time. Version rings are shared by all consumers.

## Predictions (predictions.md, written before the matrix)

Held: P1 (ret spirals outward; e-folds ~1/(2πβ), unbound 4–12 orbits at the two β —
measured 4.2/12.1; at β=3.3e-3 unbinds within the 300-orbit run — 173 measured);
P2 (news bound, spurious precession ≤ 1e-3 vs oracle 0.145, measured 2.5e-5; drift
dt-quadratic); P5 exactly (one-step arrival; inst violates causality by the full light
time); P4 direction (ret ≥ 10% deviations on some seeds at β=0.3 — max 21%).
Missed, honestly: (a) P3's "news max|dE| < 1e-4 at β=0.3" — measured 1.4e-3 (the
delayed inter-planet perturbations are larger than I guessed; still 170× below ret);
(b) P4's "half the seeds > 10%" — median was 7.5%; (c) P6's absolute ns numbers
(predicted 30–60 ns for inst, measured ~300 — allocation overhead; the *ratios* held:
news/ret 1.19 vs predicted 1.2–1.5).

## What would make it wrong

The tube must actually describe the source between kick epochs (true in the plane: the
drift *is* the compiled geodesic). Fast sources: for β_source → 1 the field magnitude
and direction are the *boosted* ones (B16's moving-lens analogue — a static evaluation
is off by √((1+β)/(1−β)) head-on); at β = 0.3 my 0PN probe cannot see this, so the
game's 0.9c fleets need the boosted kick. Radiation reaction: news's free-fall
extrapolation cancels aberration to 1PN exactly as GR does, so the first missing effect
is the 2.5PN inspiral — by design at these scales, wrong for tight binaries at real c.
Also: this is a float behaviour probe on the plane's representation, not the integer
law; and its integrator (leapfrog with delayed forces) is not symplectic — the drift it
shows (1.6e-3 at β=0.3) is an upper bound that converges quadratically in dt.

## Where news departs from GR, and the cheapest exact add for each

1. **Radiation reaction (2.5PN).** Add the Peters–Mathews orbit-averaged (Δa, Δe) per
   *cycle* as an integer decrement in the doll's ledger — it rides the tube advance
   (one table per (a,e) band, compiled like the cycle memo; zero per-kick cost). This
   is the plane's "inspiral rides on gravity at c" (law.md) made exact and free.
2. **Fast sources (the boosted field).** The tube gives the pair's relative velocity at
   zero cost; when β_pair exceeds a threshold (symmetry: at β=0 news = inst exactly, so
   this is a pure correction layer), evaluate the kick in the source doll's rest frame
   and boost the 4-force — the same machinery B16 builds for moving lenses, reused for
   massive consumers (~20 flops per pair).

## PRINCIPLES fit

- #23 "Nothing past c… it allows to cheaply partition compute": news is the causal
  contract made mechanical — the version switch at the light cone is the partition.
- #3 "Compute only surprises": a freely falling source generates no news; the kick is
  unchanged to 1e-7, and only *changes* (thrust, contact, kicks) propagate — measured
  as the near-bit-identical flyby twins.
- #6 "Store the generator, not the generated": the tube travels, not the position;
  naive retardation is what you get when you ship the generated instead.
- #2 error type: news's error is truncation (dt-quadratic, converges); ret's is a
  systematic 1PN-scale sink (compounds: "errors never compound", #13).

## The lens (what it may have made me miss)

The causality lens made me measure arrival sharpness and orbital behaviour, but not
*observational* consistency: what the player sees (light) and what bends them (gravity)
now both travel at c, and I did not test a scene where the two differ observably (e.g.
a lensing body whose thrust changes the deflection of a star behind it — the photon and
the kick should switch on the same cone). Also untested: mutually-perturbing comparable
binaries at β=0.3 (the 2.5PN gap is largest there), and the news contract *inside* a
SyMBA changeover (sub-step kicks see each other's versions mid-hierarchy). The probe
lowered c globally; the real engine lowers it per doll (c = 1 cell/update), where the
news ring depth is one or two versions — memory is a non-issue there.

## Reproduce (each ≤ 60 s except bench-1024 ≈ 90 s)

```
cd lab/results/20261005-1404-q-gravity-at-c-a237 && rustc -O gravc.rs -o gravc
./gravc binary_e3 ret 3.333 0.0042 1885 runs/x.json    # Laplace spiral
./gravc binary_e3 news 3.333 0.0042 1885 runs/x.json   # bound
./gravc flyby   news 3.333 0.00025 1.5 runs/x.json     # = inst to 1e-7
./gravc thrust  news 3.333 0.004 20 runs/x.json        # arrival 9.504 vs 9.500
./gravc system  news 3.333 0.005 600 runs/x.json       # moon survives, ret loses it
./gravc bench   news 3.333 0.002 100 runs/x.json 256 120
```
Raw matrix outputs in `runs/m-*.json`; consolidated in `results.json`.
