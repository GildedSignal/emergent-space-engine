# Predictions — run 20261011-0924-inversion-262d

Written before any run of the probe. Derived on paper only (synodic-phase
randomization); no measurement has tuned anything below.

**The claim under attack (gold 20261006-0346-taleb-09b5, adopted; two build
lanes on it this week):** under a co-orbital concentration, "every real
encounter lies within partner rank 4 along the orbit, so a phase-neighbour
certificate at O(n·k) replaces the quadratic tier."

**The hidden assumption I believe kills it:** rank is a *snapshot* statistic,
but a quiet concentration is a *shearing* system. Any period spread Δn makes
phases drift; a pair's first conjunction happens at t\* ≈ |φ₀|/|Δn| with φ₀ the
setup phase gap, so the setup-rank of a future encounter partner is ~uniform
over the concentration once |Δn|·T exceeds a few inter-body gaps. The design's
own steady state (law.md: "a kick re-sets only its body's candidate pairs, with
no work per orbit in the steady state") means the certificate must hold from
setup until the next element change — an unbounded quiet horizon.

**Dimensionless number:** Ξ = |Δn|median · T_validity / (k · g), g = mean
inter-body phase gap of the concentration. Rank-k holds only while Ξ ≲ 1.

## Held-out cases (all: one dominant mass, exact Kepler, planar, no kicks — the quiet steady state; N = 600 unless said; encounters = close approach < b)

- **A — station ring** (uniform phases; σ_a/a = 3·10⁻³, e₀ = 0.05, σ_e = 3·10⁻³,
  σ_ϖ = 3·10⁻³, T = 128 P₀, b = 10⁻⁴ a₀):
  - P-A1: ≥ 2000 encounters; the static rank-4 phase certificate evaluated once
    at setup catches **< 5%**.
  - P-A2: median setup-rank of encounter partners **> 100** (≈ uniform over N/2).
  - P-A3: rank *at the encounter instant* ≤ 4 for **≥ 95%** — the claim is true
    in this (useless-for-a-certificate) reading, which reconciles the gold's
    literal number with the failure.
  - P-A4: re-evaluating the certificate every P₀ (per orbit) catches **10–45%**:
    better, still a majority missed.
  - P-A5: a static rank-4 certificate in mean motion n (not phase) catches
    **< 40%** — no single static coordinate works.
- **B — loose fleet** (clustered phases, σ_M = 0.05 rad; σ_a/a = 3·10⁻⁴,
  σ_e = 10⁻³, σ_ϖ = 10⁻³, e₀ = 0.1, T = 128 P₀, b = 10⁻⁴ a₀):
  - P-B1: ≥ 5000 encounters; static rank-4 catch **< 5%**; median setup-rank **> 50**.
- **C1 — lockstep formation control (the gold's home regime; must pass or my
  harness is broken):** σ_a/a = 10⁻⁶, σ_e = σ_ϖ = 10⁻⁴, σ_M = 0.05, T = 16 P₀:
  - P-C1: ≥ 200 encounters; static rank-4 catches **≥ 90%**.
- **C2 — brute-force truth control:** N = 60 from A's distribution, T = 8 P₀,
  dense sampling 65 536 points per pair: the event-based finder agrees with the
  brute force on every encounter below 3·10⁻⁴ a₀ (disagreements only within ±2%
  of threshold, plus any near-misses without a conjunction crossing, which I
  count and report — they only *strengthen* the miss claim).
- **D — scaling of the catch:** caught fraction ≈ k·g / (|Δn|median·T) while
  ≪ 1 (i.e. ~1/Ξ), not a constant of the scene.

## Kill criteria for MY premise (controls both ways)

- If C1 shows ≥ 10% misses, my harness is suspect → VOID.
- If A or B show ≥ 50% caught by the static rank-4 certificate, my
  synodic-randomization premise is wrong, the gold stands at the steady state,
  and this dossier reports that.
- If C2 disagrees materially (any encounter < 3·10⁻⁴ missed by the event
  finder beyond near-threshold), the truth is broken → VOID.

## What I expect the fix to be (not a prediction; to be argued from the measurement)

The static snapshot is the wrong representation: the certificate must be the
*kinetic* circular ordering by longitude — bodies exchange order exactly at
conjunctions, so a kinetic sorted structure (Basch–Guibas–Hershberger 1997)
pays one swap per conjunction and misses nothing, with cost = the real
conjunction rate. The gold's phase-neighbour insight survives; its static form
does not.
