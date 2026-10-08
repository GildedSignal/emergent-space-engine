# Dossier — 20261008-0743-fermi-fbf8 (Fermi lens)

**Claim.** H_live from belt physics is bounded and negligible at any physical mass — at 10⁹ bodies a
belt program creates ~0.1 bits of live distinguishing information per game-second and never dies
within a play horizon (first-encounter floor 1.4×10⁴ orbits) — so memory never breaks first at 10⁹;
the terms that actually bind are one-time candidate setup (~3×10⁵–3×10⁶ s single-thread, ~10–100 h
on all 8 cores) and, if a game design packs 10⁹ bodies into one r8-width belt (2.5×10⁵× denser than
physical), scar saturation: 8 GB in 0.056 orbits, the memory-side face of the board's O(N²) packing
risk.

**Bottleneck.** HANDOFF's unmeasured risk: "distinctions created per game-second (H_live) … not the
body count, decide whether 10⁹ fit in 8 GB" (docs/plane.md:36). Expected gain: retires the risk with
numbers, redirects attention to the one-time setup term. Deletes nothing yet; sizes B18's "reported
at 10⁹" line.

## Evidence

Belt = `crates/encounters/src/belt.rs` model (μ=1, a∈U[1,1.5], Rayleigh e σ=0.01, random angles,
threshold ρ=10⁻³), propagated analytically in Kepler; kicks by impulse + Gauss equations; floats
(estimate only; canonical outcomes stay integer elsewhere).

| Quantity | Value | Source |
|---|---|---|
| R (encounters < ρ per body per orbit, N=4000, width 0.5) | 7.5×10⁻⁵ | measured |
| R scaling 8k/4k bodies | ×2.04 (linear ✓) | measured (1k point is 2-event noise) |
| conjunctions per body per orbit | 1.95, linear in N ✓ | measured |
| candidate radial pairs per body (fixed density) | 128, constant ✓ | measured |
| conjunctions per encounter | 2.7×10⁴ | measured (reproduces r8's premise) |
| R at r8's implied density (N≈1.4×10⁴) | ≈2.6×10⁻⁴ | extrapolated, inside r8 v2's implied 2.7×10⁻⁴ |
| Δe per encounter at mass m | rms = m·C·√(2 ln(ρ/d0))/ρ, C=90 measured, d0=max(4m/v², r_phys) | model, validated against measured rms (3.9×10⁵–2.6×10⁶ per unit m, tail-dominated as predicted) |

Budget at N=10⁹, M1 (8 GB, 4 GiB sim, 10¹⁰ ops/s, 60 GB/s), 1 AU belt (orbit = 3.16×10⁷ game-s),
campaign = 100 real h at RTF 100 = 1.14 orbits:

| Term | Value | Verdict |
|---|---|---|
| generator memory | 0.126 b/body × 10⁹ = **15.75 MB** | 2.4 OoM below budget; never breaks |
| scar memory (fixed physical density) | R·N·campaign·8 B = **0.65 MB**; every scar is a first encounter | never breaks; H_live creation **0.14 bits/game-s** |
| first-encounter floor | 1/R = **1.4×10⁴ orbits** (≥10⁶ real h at RTF 100) | no mass can beat it at fixed density: t_d ≥ 1/R always |
| one kick ≈ quantum (q=10⁻³) | m = **3.9×10⁻⁹ M☉**/body → aggregate 3.9 M☉ | unphysical for any real belt |
| steady-state event compute | 2.2×10⁻³ encounters/game-s (×10³ ops) ≈ 10⁻⁶ of machine | never breaks |
| one-time candidate setup | 128 pairs/body × 10⁹ × 2.5–24 µs = **3.2×10⁵–3.1×10⁶ s** (4×10⁴–3.8×10⁵ s on 8 cores) | the largest term; idle-time/light-cone streamable, one-time |
| packed belt (same width, 10⁹) | R=17.7/orbit → all distinguished in **0.056 orbits** → **8 GB scars** | breaks 8 GB; = co-orbital/O(N²) packing risk on the memory side; mass to do it in ≤10 orbits: 2.2×10⁻¹⁰ M☉/body = 0.22 M☉ aggregate |

Claim check (lens item 3), "10⁹ at today's rates ≈ 190 cores" (board, 29 Sept): pre-pivot per-body
steps (500/orbit × 200 ops) × 10⁹ = 10¹⁴ ops/orbit → 3.2×10⁻⁴ cores at RTF 1, **≈320 cores at RTF
10⁶**. The 190-core headline silently assumed a fast-forwarded (RTF ~6×10⁵) view; consistent in
order. Post-pivot (events-only, B9 "zero work per orbit until an event") the steady state per orbit
is ~0 at any RTF — the pivot bought the ~300 cores back.

Commands (each ≤ 60 s, Linux x86, orders of magnitude only):
```
cd lab/results/20261008-0743-fermi-fbf8
python3 h_live_fermi.py     # anchor belt: R, kick stats, random-walk t_d  (~2 s)
python3 budget.py           # N-scaling check, kick model, budget table    (~6 s)
```
Data: `h_live_result.json`, `budget.json`, raw stdout `run_out.txt`, `budget_out.txt`.

## Predictions (predictions.md, written before the runs)

1. R in 2×10⁻⁴–2×10⁻³ per body/orbit: **missed low by ~3×** at N=4000 (7.5×10⁻⁵); held once the
   pre-registered N-linearity is applied (r8's belt was N≈1.4×10⁴ → 2.6×10⁻⁴, inside the band). The
   flat-in-N-at-fixed-density premise itself was confirmed (8k/4k = 2.04).
2. Δe ~ 10⁻⁵–10⁻⁴ at m=10⁻¹⁰: **held** (median 1.2×10⁻⁵, rms 3.5×10⁻⁵).
3. t_d > 10⁶ orbits at m=10⁻¹⁰: **held** (1.1×10⁷ by diffusion; 1.4×10⁴ by the first-encounter cap,
   which I had not modeled — a stronger bound than predicted).
4. m* in 10⁻⁸–10⁻⁷: **missed** — thresholds are lower (3.9×10⁻⁹ one-kick, 2.2×10⁻¹⁰ packed); the
   conclusion (aggregate ≥ 0.2–4 M☉, unphysical) is unchanged.
5. Budget verdict: **held** except the setup term, which I predicted at 10³–10⁴ s and measured at
   4×10⁴–3.8×10⁵ s on 8 cores — 1.5 OoM worse than my band; still one-time and idle-streamable.
6. 190-cores re-derivation: **held** with the RTF assumption exposed.

## What would make it wrong

- The kick model is impulse + Gauss with random deflection side and p(d)∝d conjunction geometry;
  correlations between successive conjunctions of the same pair (quasi-periodic misses, r8's
  Diophantine structure) could cluster kicks — that lowers t_d, but the first-encounter cap
  (1.4×10⁴ orbits at fixed density) bounds any such effect from below.
- ρ=10⁻³ (r8's belt b) is the anchor; R ∝ ρ² and the kick ∝ 1/ρ roughly cancel in t_d's diffusion
  term, so the verdict is insensitive to ρ. A hot belt (σ_e=0.1) is even safer (fewer sub-ρ
  encounters, weaker kicks).
- The setup term borrows r8 v3's 2.5–24 µs/pair on the cone pairs; my 128 radial pairs/body is an
  upper bound on cone pairs. If the co-orbital certificate replaces the pairwise tier for
  concentrated workloads (taleb-09b5, adopted), packed-belt setup drops to O(n·k) — but packed-belt
  *scars* (8 GB) remain: packing 10⁹ into one belt width needs a program, not pairwise certificates.
- Adoption cost: none for code; the numbers size B18's report line and warn the belt design away
  from same-width packing. Fit: PRINCIPLES 24 ("the memory floor is information-theoretic") and 6
  ("store the generator, not the generated") — confirmed for belts at any mass a star can carry;
  principle 3 ("compute only surprises") — the steady state is already surprise-only.

## The lens (what Fermi may have missed)

Orders of magnitude only, one belt family (cold, 2D, Kepler), and the light-cone/player side of
H_live (births, battles, the player's c-bounded region) is asserted from the design, not measured —
it needs the plane's dashboard (b-h-live build) to confirm. Cloud numbers; the integrator
re-measures on the M1.
