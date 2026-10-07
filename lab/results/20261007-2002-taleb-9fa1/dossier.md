# Dossier — 20261007-2002-taleb-9fa1

## Claim

The phase-neighbour certificate adopted from gold `20261006-0346-taleb-09b5` (feeding the
pending `b-coorbital-cert` build) is safe **only** if the sort key is the *true longitude*
θ and the rank budget k scales with the bundle: a mean-longitude (λ) or mean-anomaly (M)
sort silently drops 33–60% of real encounters under apsidal spread — including in the
gold's own co-orbital corner — and "rank 4" holds only while C = n·thickness/(τa) ≲ 1.5;
at fixed internal eccentricity the needed rank grows ∝ n (measured: k_p95 = 6 → 13 → 24 at
n = 300 → 600 → 1200, σ_e = 1e-2), so the O(n·k) tier is asymptotically O(n²·σ_e), not a
quadratic-killer for fat swarms.

## Bottleneck

Board: "finding encounters without work per orbit" and the co-orbital concentration gold;
HANDOFF's risk list line 1. This is the pre-freeze red-team of an adopted result before its
build lands ("before any freeze, one GLM red-team and the cheapest falsifying probe must
have run"). Gain: it stops the build from shipping the wrong key with a silent ~30%
encounter loss (errors that compound: a lost encounter leaves wrong elements, which mis-schedule
future encounters — principle 13), and hands it the correct key, the k-budget law and the
rebuild-cadence term. Cost of the probe: ~35 s of compute.

## Evidence

All numbers from `main.jsonl` / `scale.jsonl` (commands in [README.md](README.md); truth =
the crate's own `truth_pair`, every pair, exact radial prefilter; miss_k over true
encounters, key sorted at t = 0; the gold's co-orbital corner is scene `gold-corner-s3e-4`:
n=300, σ_e=3e-4, ρ=1e-3, ϖ uniform, da=1e-4, 30 orbits, 1146 encounters).

**Key choice decides everything** (miss at k=4, same scenes):

| scene (σ_e, ρ) | C | λ | M | θ | θ k_max |
|---|---|---|---|---|---|
| gold corner 3e-4, 1e-3 | 0.11 | 0.33 | 0.97 | **0.000** | 4 |
| 1e-3, 1e-3 | 0.37 | 0.26 | 0.99 | **0.000** | 4 |
| 3e-3, 1e-3 | 1.1 | 0.36 | 0.98 | **0.032** | 6 |
| 1e-2, 1e-3 | 3.7 | 0.40 | 0.97 | **0.145** | 12 |
| 3e-2, 1e-3 | 11.0 | 0.60 | 0.97 | **0.455** | 25 |

Under ϖ uniform (the belt generator's own convention), λ and M orders are effectively
scrambled (partner at random rank); θ reproduces the gold's number exactly at its corner
(max rank 4). Mechanism, confirmed by encounter-time geometry: two bodies can approach
only at true-longitude alignment — median |Δθ(t_enc)| ≈ 0.5·ρ/a in every scene — while
Δλ(t_enc) ≈ O(e) and ΔM(t_enc) ≈ −Δϖ (arbitrary). A t=0 sort by λ or M carries the ϖ
offset in its order; θ never does.
**Rank budget grows with the bundle, not with ρ.** Scaling at σ_e = 1e-2, 20 orbits:
θ miss4 = 0.12 → 0.35 → 0.57 and k_p95 = 6 → 13 → 24 at n = 300 → 600 → 1200 (k_max =
10 → 23 → 41; k=32 already leaks 0.7% at n=1200). Fit across scenes: k_p95 ≈ 1.5·C,
k_max ≈ 2.3·C with C = n·(r_apo,max − r_peri,min)/(τa). Raising ρ from 1e-3 to 1e-2 at
σ_e = 1e-2 moves θ miss4 only 0.145 → 0.114: the budget is set by the e-scale, not by
the encounter radius. So "rank 4" is a C ≲ 1.5 statement; at fixed σ_e the phase tier
costs n·k ∝ n²·σ_e per rebuild — it serves tight formations (C = O(1)), not fat co-orbital
swarms at scale; those stay on the cone tier or need the 2D (θ, r) skin (below).

**Controls.** Positive: gold corner, θ key, zero miss at k=4 (max 4). Negative: aligned
apsides (pom_window=0, same thickness, same C=11): λ=M exactly, and θ miss4 = 0.20 vs
0.455 under spread — the ϖ spread is the mechanism, and no purely radial bundle number can
gate λ/M; only the key change removes it. Shear control (da=1e-2, thin e, C=0.52): θ
miss16 = 0.009 but k_max = 23 at 30 orbits — a-spread adds a horizon-linear rank drift
(~1.5·Δa per orbit), so the certificate needs a rebuild cadence or a drift-margin
k += n·1.5·Δa_max·W/(τa).

## Predictions

[predictions.md](predictions.md) was written before the runs. Held: mean-anomaly
catastrophe (>0.9 everywhere), the e-scale rank growth ∝ n, ρ's negligible share, θ-alignment
at encounter (~0.5ρ/a), aligned-apses isolation (λ=M), the shear drift. **Two failed, and
both failures are the finding:** my λ-key predictions (miss4 = 0 at the gold corner,
<10% aligned) were wrong — λ is not a valid certificate key under ϖ spread at all, which
is precisely what the build must not ship. My own first-draft gate (S = thickness/ρ ≲ 1)
also failed as predicted in point 5: the gate must budget k, not compare thickness to ρ.

## What would make it wrong

If the gold's rank-4 measurement already sorted by true longitude (their corner's θ k_max
is exactly 4), this probe confirms rather than kills — the constraint then lands entirely
on the build: key = θ, k ≈ 2.3·C + drift, cadence for shear. If real fleets are and remain
apsidally aligned to ≲ k·τ/n, λ works — but the belt convention is uniform ϖ, and apsidal
precession (J2, tides, 1PN) walks any aligned fleet out of that corner; θ is invariant to
precession ([INFERENCE], not measured here: this probe's Keplerian orbits do not precess).
Adoption cost: one line in `b-coorbital-cert` (sort by θ, budget k from C_effective =
n·(radial spread + 1.5·Δa·window)/(τa), rebuild each window), no new tier; fat swarms
(C ≫ k) keep the cone tier — the phase tier's domain is written down instead of implied.

Fit with PRINCIPLES: "a fix signals the wrong representation" (19) — λ is the wrong
coordinate, θ is the water the fish needs; "behaviours over many seeds" (20) — seeds
agreed (s1e-2 on seed 20261008: λ 0.38, θ 0.12, k_max 10, 764 encounters);
exactly when the cheap tier stops being cheap. Via negativa: nothing added, one key and
one threshold corrected before ~code existed to patch.

## The lens

Taleb asks what breaks, and the answer was: the certificate's silent failure mode, not its
cost — a dropped encounter compounds (13), so a 33% silent miss is ruin-adjacent, not an
efficiency loss. The lens may have made me under-weight the honest limit of this probe:
60 minutes bought the domain boundary and the budget law, not the replacement structure
for fat swarms at scale (a 2D (θ, r) hash with drift skins, cadence ~ ρ/v_rel — the
slack-skin pattern — is the natural next question, unmeasured here). Also, the probe
inherits this crate's truth and generator wholesale: if that harness hides a bias, my
numbers share it (the memo lesson); the θ result is protected only by being derived from
a geometric necessity, not from the harness alone.
