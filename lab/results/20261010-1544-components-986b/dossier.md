# H_live's floor: the rate at which a program-born belt accumulates distinguishing bits

## Claim

The storage component's live rate is measured for the first time: under the law's own
event structure (exact Kepler drift + hyperbolic kicks at conjunctions), a belt's
distinguishing information grows **diffusively, not linearly** —
`bits(t) = Σ_col log2(σ_col(t)·2.07/q)` with σ ∝ t^0.55 — so 10⁹ program-born bodies fit
the 4 GiB budget at a player-differentiable quantum, and the **storage quantum q, not the
encounter rate, is the memory lever** (−13 bits per decade of coarsening). Two scaling
facts I predicted wrong: per-body spread is **flat in N** at fixed belt mass (diffusion is
dominated by rare strong encounters, not the numerous weak ones — so no 1/√N dilution may
be assumed), and 10× belt mass buys only ×3.8–7 spread (self-limiting heating).

## Bottleneck

Board risk "H_live: distinctions created per game-second … not measured yet" and HANDOFF's
"decided by distinctions created per game-second". This is the storage component's floor
(PRINCIPLES #24: "The memory floor is information"). The `b-h-live` build instruments the
plane's dashboard (one small scene); this probe measures the **rate law itself** on belt
physics the plane cannot hold, and answers the 10⁹ verdict.

## Evidence

Probe: `hlive/` (self-contained Rust, no deps). Bodies drift on exact Kepler tubes
(integer periods/periapsis times, `crates/encounters`' discipline); conjunctions found
event-driven per pair (bracketed synodic scan + epicycle scan); every conjunction inside
ρ_screen applies the hyperbolic kick `δ = 2·atan(μ/(b·v²))` — proven **identical** to the
exact analytic hyperbola `2·asin(1/e)` (so the kernel is exact for isolated pairs; the
only approximations are the star's tide during an encounter and the impulse's position
treatment). Elastic contacts below 2·r_contact. Measured: empirical entropy of quantized,
centered offsets (ΔE/E, ΔL/L, Δϖ/2π, Δλ/2π) vs the birth program, plus the offset spreads
σ_col (the 10⁹-relevant differential entropy — the empirical entropy saturates at the
sample cap log₂N).

Self-tests: Kepler round trip 4e-13; conjunction finder exact (wrap 0.0);
hyperbola conserves speed to machine precision; **control μ=0 is exactly 0.0 bits at every
checkpoint** (analytic drift ⇒ the instrument's noise floor is zero).

Numbers (N=256, width 0.01, σ_e 0.05, q=1e-6, t=100 orbits, centered):

| scene | σ_E | σ_L | σ_ϖ | σ_λ | kicks/body | strong | contacts |
|---|---|---|---|---|---|---|---|
| μ=0 control | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| μ=3e-7 | 1.7e-3 | 8.4e-4 | 6.7e-3 | 1.4e-1 | 135 | 10 | 59 |
| μ=3e-6 | 6.4e-3 | 3.3e-3 | 4.5e-2 | 3.0e-1 | 112 | 70 | 73 |
| μ=3e-5 | 4.7e-2 | 2.4e-2 | 2.5e-1 | 2.9e-1 | 209 | 1494 | 357 |
| μ=3e-4 (256b, 50 orb) | 6.9e-2@6orb | — | — | — | saturated | — | — |
| N-scaling @3e-7 | 1.9e-3 / 1.7e-3 / 1.7e-3 (N=128/256/512) | | | | 64/135/284 ∝ N | 10/10/15 | |
| ρ=0.005 vs 0.02 @3e-7 | 1.57e-3 vs 1.69e-3 | | | | 30.6 vs 135 | same | |
| lane (20× concentrated) | 6.0e-4 | 3.7e-4 | **1.2e-1** | 1.2e-1 | 319/200orb | 12 | 242 |

Diffusion exponents (μ=3e-7): σ_E ∝ t^0.55, σ_L ∝ t^0.54, σ_λ ∝ t^1.6 (phase integrates
the period error; the phase column dominates scars). Mass scaling of σ_E:
×3.8 per decade at 100 orbits (×5.7 at 12.5 orbits) — self-limiting, not ×10.

**The 10⁹ verdict.** Budget 4 GiB / 10⁹ = 34.4 bits/body. Birth program 0.126 bits
(gold components-98bc). Extrapolating μ^0.7 (measured over 3 decades) and, conservatively,
**flat in N**:
- ship populations (μ_f ~ 1e-26 of the star): encounters contribute ~0; contacts at
  physical ship radius extrapolate (rate ∝ r, measured at inflated r) to ≤ 1e-3 bits per
  body over 10⁴ orbits. **Fits with ~2 orders of headroom.**
- a physical belt (μ_b ~ 1e-9): ~25±10 bits at q=1e-6 after 100 orbits, growing as
  0.55–0.8·log₂t (+7 bits per decade of horizon). Fits at q ≤ 1e-5 for any session.
- a heavy belt (μ_b ~ 1e-5, partially mixed): ~30 bits at q=1e-6 → needs q=1e-4 (~13–18
  bits) or program re-encoding as it heats. A fully thermalized belt costs its full
  differential element entropy (~32 bits measured at saturation, N=256 sample cap) — the
  allocator must detect mixing (σ_offset ≈ σ_birth) and recompile the program, not store
  per-body scars forever.
- **Idiot index:** the naive per-body 16-byte tube store = 128 bits/body = 16 GB at 10⁹
  (2× the whole machine) against ~0.13–18 bits actually needed → 7× (worst case, mixed
  heavy belt at coarse q) to ~1000× (ship belts). The scar store is within ~2× of its
  floor once q is fixed by the player-differentiable resolution.

Reproduce (each ≲ 60 s uncontended; the whole set ran in 192 s on this contended machine):

```
cd lab/results/20261010-1544-components-986b/hlive
cargo run --release -- selftest && cargo run --release -- kernel
cargo run --release -- belt 256 0    0.02 100 301   # control: 0.0 bits everywhere
cargo run --release -- belt 256 3e-7 0.02 100 301
cargo run --release -- belt 256 3e-6 0.02 100 301
cargo run --release -- belt 256 3e-5 0.02 100 301
cargo run --release -- belt 128 3e-7 0.02 100 302   # N-scaling (with 256 above, 512)
cargo run --release -- belt 512 3e-7 0.02 100 302
cargo run --release -- belt 256 3e-7 0.005 100 303  # screening cut
cargo run --release -- lane 256 1e-6 0.02 200 304 1e-3 0.02
```
Raw JSONL in `out-s-*.jsonl` (already in this folder; regenerated by the same commands).

## Predictions (predictions.md, written before the runs)

- **Held:** (1) growth is diffusive, sub-logarithmic in cost — no linear term anywhere,
  including the concentrated lane; (5) the control is at the floor (exactly 0, stronger
  than the < 0.05 bits promised); (6) the kernel is exact — stronger than claimed: the
  impulse *is* the hyperbola for isolated pairs; (7) ship belts accumulate ~nothing;
  (8) the shared drift is real (centering matters: drift_ϖ reaches −0.05 rad in the lane).
- **Failed, and the failures are the result:** (2) I predicted +6.6 bits per decade of
  mass (variance reasoning); measured +2 bits (σ ∝ μ^0.6–0.85) — self-limiting heating.
  (3) I predicted −0.5…−1 bit per doubling of N at fixed mass; measured **0** — rare
  strong encounters dominate, so the population does not dilute as 1/√N in this regime.
  (4) I predicted a Coulomb-log ~2 bits between ρ and ρ/4; measured **0.11** — same cause.

## What would make it wrong

- The probe is two-body-Kepler + pairwise scattering: no coherent resonance pumping (B17
  lanes), no secondaries, no mean-field feedback (centering absorbs only a global drift).
  A lane parked **on** a mean-motion resonance pumps e coherently and could grow σ linearly
  in t — that is the unmeasured case, and it is the single most likely place where H_live
  stops being diffusive.
- σ_λ's t^1.6 growth is integrated period error; if the engine re-anchors phases at
  program updates, that column's cost drops accordingly.
- N-flatness is measured over N ∈ [128, 512] only; the extrapolation to 10⁹ conservatively
  keeps σ flat. If weak encounters take over at large N (Coulomb regime), the rate only
  gets *smaller*.
- Floats explore here; the engine's integers quantize kicks, which truncates the weak tail
  exactly where it contributes least (measured: cutting ρ 4× costs 0.11 bits).

## Cost of adoption, and fit

Adoption is a rule, not code: `bits(t) = Σ_col log2(σ_col(t)·2.07/q)` with q set by the
player-differentiable resolution (one line in `docs/law.md`'s Populations section and the
allocator's H_live budget in `crates/shipmem`); plus two design consequences — screen
encounters tightly (the strong tail is the physics), and recompile a population's program
when σ_offset approaches σ_birth. PRINCIPLES #6: "influences below one quantum accumulate"
— measured: they accumulate diffusively and cost log₂ of the accumulated spread. #24: the
floor is information — the belt's floor is 0.126 bits at birth plus the measured spread.

## The lens

First-principles, one component: it missed the neighbours. (a) The readout: bits depend on
q, and q is owned by observation ("the floor is what the player can differentiate"), not
by storage — the two components must agree or the number is arbitrary. (b) The queue:
H_live's rate is what the slack skin should schedule against; this run measured the rate
but not the scheduling. (c) Resonant lanes are the open hole (above). And the probe's
empirical-entropy columns saturate at log₂N — the differential estimate is the honest 10⁹
number but is unvalidated above 10 bits/column by construction.
