# dossier.md — run 20260930-2250-taleb-3d2c (Taleb lens: the τ regime selector, B14)

## Claim

The τ₀ regime boundary for B14 must be set by the orbit-averaged law's e-pump
tolerance — τ₀(ε_e = 0.1) ≈ 0.25–0.30 R_Hill, far below the escape boundary at
0.45 — and near the Hill limit the discriminating variable is the sun–apsis
(evection-type) angle, not τ and not direction: at every τ from 0.45 to 0.90 the
ejectors are exactly the seeds starting in quadrature to the Sun, while aligned
seeds stay bound; placing the boundary at the escape onset instead of 0.05 R_Hill
inside the calm zone makes straddling moons flip regimes 1454 times per 4096
orbits (0.35 handoffs/orbit ≈ the entire averaged-kick budget of H0190), 100× the
rate of the conservative placement.

## Bottleneck

B14 (tides and the τ regime selector near the Hill limit), #3 on the live list;
feeds B12 (handoff rebinding). Expected gain: deletes the per-switch rebind work
for moons near the boundary (100× at the measured point), sizes the cheap
averaged-kick regime honestly (≤ 1/3 of the moon zone, not up to the stability
edge), and names the certificate variable (sun–apsis angle) that decides
bound/escaped for half the retrograde grid — without it, B14's "≥ 99% of judged
seeds" has to exclude the geometry-split band wholesale.

## Evidence

Model: circular restricted three-body, GM_planet = 1, GM_sun = 1000
(Jupiter-like), R_Hill = 0.0693 a_p; truth = full CR3BP (leapfrog, 128
steps/orbit, barycentric Jacobi conserved to ≤ 1e-4 median, 1.3e-2 worst in the
chaotic band); Law S = orbit-averaged quadrupole (e ≡ e₀, coplanar); Law F =
per-step Hill quadrupole (the dense fallback). Horizon 4096 moon orbits
(= 45 planet orbits at τ = 0.5, 700 at τ = 0.95; B14 uses 50). 8 seeds
(4 mean anomalies × 2 apsidal orientations). Machine: cloud container, 4 vCPU,
16 GB, load 0.88.

Commands (from `lab/results/20260930-2250-taleb-3d2c/`, numpy 2.4.6):

- `python3 tau_selector.py controls` (64 s) — positive control τ=0.2/e=0.05:
  0/8 escaped, max e ≤ 0.079; negative control τ=0.9/e=0.3: 8/8 escaped;
  resolution check 128 vs 256 steps/orbit at τ=0.6/e=0.3: same 8/8 verdict,
  max_e within 0.06 (chaotic band; trajectory identity is not claimed).
- `python3 tau_selector.py sweep fast` (47 s) — reproduction path.
- `python3 tau_selector.py sweep` (122 s, over the 60 s guidance — hence the
  fast path) — writes `sweep.json`, the decisive grid:
  11 τ × {prograde, retrograde} × e ∈ {0.05, 0.3}.
- `python3 tau_selector.py chatter 0.45` / `chatter 0.40` (29 s each) —
  writes `chatter-0.45.json` / `chatter-0.40.json`.

Numbers (`sweep.json`):

- **S's error = truth's e-pump** (pro, e=0.05): 0.107 @ τ=0.30 (grid floor),
  0.47 @ 0.40, 0.83 @ 0.45. Saturated amplitude, not accumulation: a 2-planet-
  orbit horizon gives the same 0.106 at τ=0.30. The error type is bounded
  (principle 13 compatible); the amplitude crosses 0.1 below the grid floor.
- **Escape onset τ=0.45, both directions** (4/8); prograde 8/8 from 0.50;
  retrograde flat 4/8 through τ=0.90, 7/8 at 0.95.
- **The split is geometric:** escape pattern `.EE..EE.` — seeds with
  M₀+ϖ ∈ {π/2, 3π/2} (quadrature to the Sun at t=0) eject; aligned seeds
  survive. Identical pattern for prograde @ 0.45 and retrograde @ 0.45–0.90.
- **Law F verdicts:** mismatch vs truth 0–2/8 seeds across the whole grid;
  mismatches cluster in the transition band τ=0.40–0.55; final-e deviation
  reaches 1.4 in the saturated band (τ=0.50, retro) — verdicts hold,
  trajectories diverge: exactly the error type B14's gate judges.
- **Chatter** (boundary τ*, e=0.3 straddlers): τ*=0.45 → mean 302, p99 1438,
  max **1454** switches per 4096 orbits (sustained ~0.35/orbit for one seed);
  τ*=0.40 → mean 0.79, p99 12, max **14**. 0.05 R_Hill of margin = 100×.
- Costs: S ≈ 0.3 kicks/orbit (H0190); F = 128 steps/orbit here (~400×); a bad
  boundary makes the handoff rate (0.35/orbit) alone equal the whole kick
  budget.

## Predictions

`predictions.md` was written before the decisive runs, tuned only on controls
and 5 break-zone probes. Outcome: **P5 hit** (bursts, median ≤ 20, max ≥ 100 —
1454), **half of P1 hit** (8/8 escape from τ=0.50 prograde) but τ_break(S) < 0.30
missed the window low edge by 7% on the pump criterion; **P2, P3, P7 missed** —
retrograde escape onset equals prograde (no +0.25 shift), e=0.3 shifts onset by
≤ 0.05 (not 1/(1+e)), and S is not element-valid above ~0.3 in either direction
so a prograde-keyed τ₀ wastes only the [0.30, 0.45] strip; **P4 partial**
(mismatch ≤ 2/8 everywhere, but concentrated at 0.40–0.55, not (0.7, 0.95]).
My Hamilton–Burns prior did not transfer at this mass ratio; the geometry
bifurcation it hid is the finding.

## What would make it wrong

Single mass ratio (1000), single horizon (4096 moon orbits), coplanar only (the
inclination/Kozai–Lidov channel untested), e ≤ 0.3, floats exploring where the
law will be integer, 8 seeds with only 2 apsidal orientations — the bifurcation
map needs denser geometry sampling before any B14 criterion freezes on it.
Law F is per-step quadrupole, not the compiled Hill problem: its verdict
validity transfers (same dynamics class), its cost does not — if the
compile-once-per-planet Hill tables (law.md) are cheap, the whole cost argument
softens to the chatter term alone. Adoption cost: a certificate field for the
sun–apsis angle near the Hill limit and a τ₀ table keyed on e-pump tolerance;
no new machinery — the dense fallback already exists in the design. PRINCIPLES
33: "a body resolves only the influences that are significant at its own scale"
— near the Hill limit that influence is the sun–apsis phase, which τ does not
resolve; and 19, "if you find yourself fixing things that's oftentimes a signal
that it is the wrong representation": the standard Schmitt-trigger fix for
chatter is a bandaid; the measured structure says place the boundary with
margin and carry the angle.

## The lens

Taleb hunted the cliff and found two (amplitude at 0.30, verdicts at 0.45) plus
the concave handoff cost — but it under-measured the cheap side of the barbell:
it never priced the compiled-Hill regime's actual cost (compile once, universal
in Hill units — potentially deleting the 400× worry), never tested hysteresis
against placement, and dropped the switch-compounding experiment (error injected
per S↔F handoff; B12 territory) for time. One process note for the lab: the
truth integrator's indirect-term sign error was invisible in the weak-tide
configuration and surfaced only under the strong-tide probe — a control that
cannot fail is a control (principle 10).
