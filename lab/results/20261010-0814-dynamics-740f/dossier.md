# Dossier — 20261010-0814-dynamics-740f

**Lens:** dynamics and attractors. **Date:** 10 October 2026. **Wall time:** ~55 min.

## Claim

The population scar layer (H_live) is not a walk to ruin but a logarithmic crawl:
on the shipped `crates/shipmem` store, a belt's scars cost **½·log₂ k bits per action
column and 1.5·log₂ k bits for the phase column** (k = kick events absorbed) —
**≈ 3 bits per doubling of k** — so the birth program's discount erodes slowly, and
the 10⁹-body memory risk flagged in HANDOFF ("H_live, not measured") is empty for
belts at play horizons: ≤ 2.2 GB at 10⁵ s-scale 100× play for a belt of mass
fraction 10⁻⁴, and 0.2 GB at a realistic 10⁻⁹.

## Bottleneck

HANDOFF's risk list: "Distinctions created per game-second (H_live): they, not the
body count, decide whether 10⁹ fit in 8 GB; **not measured yet**." This run measures
it and retires the fear part: no new component is needed (no re-anchoring machinery,
no ruin), and one representation trap is found (below).

## Evidence

Instrument: `scarwalk/` (this folder) drives the **shipped** store — `Program::seal_from`,
`Enc::new(true)` block codec, Elias–Fano ordinals — on exact integer deviation columns
(a, e·cosϖ, e·sinϖ, periapsis-phase drift; grids q_a = q_e = 2⁻²⁴, q_φ = 2π/2³²),
N = 16,384 bodies, kicked by four generators. Physics: exact Kepler element
transforms (roundtrip error < 1e-12, tested; control δa = 2δvₜ/n matches to 0.05%)
+ textbook shearing-sheet impulse encounters (μ=10⁻⁴ belt: rate 319.6/orbit/body,
rms δa 3.1×10⁻⁷/encounter). Store `eval` round-trips every 97th body exactly
(asserted in-run).

Bytes per body vs k (P0 = birth-program anchor; P1 = mean re-anchor):

| generator | k=1 | k=4096 | slope (bits/doubling, last 3 doublings) |
|---|---|---|---|
| G1 collective (control) | 0.63 B | 0.68 B | ~0 |
| G2 gaussian individual | 9.93 B | 15.22 B | **2.81** (theory 3.0) |
| G3 encounter replay (hot belt) | 6.88 B | 10.2 B @k=102 | ~2.9 |
| G4 cauchy tail | 11.1 B | 19.6 B | **5.08** (theory 4 + patches) |
| G2 at N=4096 | — | 15.5 B (per-col 3.62 vs 3.53) | N-independent ✓ |

- Per-column at k=4096 (G2): **a 3.53 B, ex 3.53, ey 3.53, phase 6.04** — the phase
  column carries 36–40% of H_live and grows 3× faster (measured σ_φ exponent 1.44 →
  1.5 asymptotic; exact small-k variances match ΣΣmin(i,j) to 3 digits).
- Each column costs log₂(σ/quantum) + 2.05 bits within ~1 bit (Gaussian), i.e. the
  store pays the **state entropy, not the history entropy** (history would be ∝ k).
- Collective modes are absorbed **natively**: G1 ≈ EF overhead only, and explicit
  mean re-anchoring (P1) is bit-identical to P0 on every generator — the codec's
  delta transform already cancels the common mode. No re-anchor machinery needed.
- Heavy tails stay bounded: the block codec's patched exceptions add ~1.7
  bits/doubling over Gaussian (G4), no block-width poisoning.
- **Representation trap (found by breaking it):** storing the phase deviation as a
  wrapped u64 (mod one period) makes every small deviation pay ~full width + patch
  exceptions — 11.5 vs 9.93 B/body at k=1 — because negative drifts wrap to ≈2π.
  The population layer must keep the phase deviation unwrapped (the engine's 64-bit
  periapsis clock already does); wrapping saves nothing later either (the cycle
  count re-absorbs the bits).
- Determinism: two full runs byte-identical (only cargo chatter differs).

Game-scale extrapolation (`analyze.py`, constants measured above; 1 AU, RTF 100 —
1 h of play = 0.011 orbits):

| play | orbits | bytes/body | 10⁹ bodies |
|---|---|---|---|
| 1 h | 0.011 | 3.85 B | 3.9 GB |
| 1000 h | 11.4 | 6.57 B | 6.6 GB |
| 10⁴ h | 114 | 7.60 B | 7.6 GB |

μ and N sensitivity (at fixed belt mass, per-orbit variance ∝ μ²/N, both measured
in the MC's construction): μ=10⁻⁴/N=2²⁰ → 4.69 B at 10 h; same μ at N=10⁹ → 2.22 B;
realistic main-belt μ=10⁻⁹ at N=10⁹ → 0.25 B (self-scarring below one quantum:
scar layer nearly empty). The 8 GB line (8 B/body) is crossed only after
**2.4×10⁴ hours of 100× play** at μ=10⁻⁴, N=2²⁰ — and never at plausible μ for
large N. The full 16 B tube is unreachable (~10⁹ h).

Reproduce (each ≤ 60 s): `cd lab/results/20261010-0814-dynamics-740f/scarwalk &&
cargo run --release` (≈20 s, prints `run3.csv` content), then `python3 ../analyze.py`.

## Predictions

Written before the decisive run (`predictions.md`). Held: G1 ≈ 0 (0.63 B); the ½-log
law with slope ≈ 3 bits/doubling total (2.81 measured); G3 follows it; P1 ≈ P0 for
individual kicks (exactly equal, for a better reason than predicted); N-independence;
single-digit bytes/body at play horizons. **Refuted:** prediction 4's phase-column
saturation at log₂(period grid) bits — wrong because the exact periapsis time must
distinguish *which* period the body is in; the information past 2π reappears as the
cycle count, so the 1.5-log growth is genuine, not an artifact of not wrapping.
The slope part of prediction 4 held (1.44 measured).

## What would make it wrong

- The kick statistics are a shearing-sheet impulse Monte Carlo, not the plane's kick
  layer; the **law** (bits vs k) is generator-robust (shown across four generators),
  but the physical constants (rate, per-orbit σ) carry the model's O(1) errors and
  the uniform-encounter-phase simplification.
- Secular resonances with planets and chaotic diffusion are not modelled: real
  e-excitation at low μ can be resonance-dominated (collective, likely
  program-absorbable per region, but unproven here). The self-gravity walk is a floor.
- The grids are model choices; bits shift by Δlog₂(quantum) exactly (additive) —
  slopes unaffected.
- Single replay seed per generator; the σ-based fits are ensemble statistics over
  16,384 bodies, so the slope estimate is tight, the per-epoch byte points are not
  independent.

Cost of adoption: none — a measurement plus one rule (keep phase unwrapped in the
population layer). It **deletes** candidate machinery: periodic program re-anchoring
and H_live-driven belt repacking are not needed at any horizon the game will see.

Fit with PRINCIPLES: "Store the generator, not the generated" (6) — measured how
long the generator survives against its own generated history; "The memory floor is
information" (24) — the floor crawls at 3 bits per doubling, it does not march;
"Measure before claiming" (10) — the HANDOFF risk line said "not measured"; it is
now.

## The lens

The attractor lens predicted saturation where exactness forbids it (the refuted
prediction 4): what looks like a wrapping variable at the store level is exact
clock information at the law level. The lens also nearly over-read the first-hour
transient (9.9→11.2 B in one doubling: decaying cross-column codec wins, not the
asymptotic slope — the last-three-doubling fit is the honest one). What the lens
did catch: the state-vs-history entropy distinction is exactly "compute only
surprises" applied to memory — the store pays for what the walk *is*, never for
how it got there.
