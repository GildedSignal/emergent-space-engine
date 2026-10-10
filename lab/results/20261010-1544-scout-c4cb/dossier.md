# Dossier — 20261010-1544-scout-c4cb (scout lens)

**Machine:** GitHub Actions linux, 8 vCPU, 15 GB (loadavg 0.9–4.0 during runs,
shared with sibling jobs; all processes < 1 GB). Wall: ~70 min (two shard
reruns after a harness timeout; the physics ran twice, bit-identical).

## Claim

A doll's gravity crosses the light cone as a **quantized multipole news
channel whose rate is set by the mass distribution's amplitude-weighted
bandwidth, not the body count**: one frozen stream — 8 live reals (dipole 3,
quadrupole 5), 32 bits, 8 samples per innermost-planet period = **256 B per
system per P_ref** — served 16× more bodies with *smaller* error (H1), a
fast heavy intruder of 3% of the orbiting mass never forced a faster
channel because its quadrupole amplitude m·a² is ~400× below the planets'
(H5), and distance grading exists (ℓ=2 at 12 cell radii, dipole-only
marginal at 24, H2) — but the reader's position error walks at t^1.8 under
a linear readout (H4), so the channel needs the law's second-order ramp
and re-anchoring, not a one-price-forever certificate.

## Bottleneck

The board's listed risk "**the light cone keeps growing**" and Julien's
"gravity must travel at c" (law.md, "gravity is news"): at 10⁹ bodies,
per-pair retarded evaluation is O(N) per consumer. The news channel makes
far-field gravity cost per consumer **independent of interior body count**
(measured 16×, expected O(10³–10⁶) inside a real doll by the same
mechanism [INFERENCE]) and turns "light cones partition compute" (P23)
into a byte budget: ~10²–10³ B per doll per interior heavy-orbit. What it
deletes: the far-field kick evaluation over member bodies (the direct sum
at the observer: 600 steps × 1028 bodies per orbit → 8 reals per step),
and the fear that causal gravity grows the work with the visible universe.

## Evidence

Frozen pass rule (before any held-out run): final observer position error
≤ 10⁻³·D AND |ΔE_final| ≤ max(1%·|work_true|, 10⁻⁶·|E₀|), scene non-vacuous.
Scene: star M=100, 4 planets (m=8, a∈[0.30,0.60]L), light disk (m=2,
a∈[0.20,0.50]L), all exact Kepler generators (truth has zero integration
error); observer on its own orbit at D=12L (e=0.1) unless stated; news =
quantized q_lm(t) about the star-origin, linear readout, per-ℓ fixed-point
scale from kinematic bounds only. P_ref = innermost planet's period = 0.103.

| run | verdict | pos_err | dE_final | work_true | field_rms |
|---|---|---|---|---|---|
| calib ℓ=0 (negative control) | FAIL ✓ | 4.3e-2 | −1.2e-3 | +9.3e-3 | 2.5e-3 |
| calib ℓ=1, all rates | FAIL ✓ | 8.1e-4 | +5.5e-4 | +9.3e-3 | 1.8e-4 |
| calib (ℓ,8,32) positive control | PASS ✓ | 2.4e-4 | −3.8e-5 | +9.3e-3 | 5.9e-5 |
| calib bits=8 | FAIL | 2.7e-1 | — | — | 3.0e-3 |
| H1 nb=64 → nb=1024 | PASS, PASS | 3.5e-4 → **1.5e-4** | −6.2e-5 → −2.3e-5 | +9.9e-3 | 5.9e-5 |
| H2 D=24L (2,8,32) | PASS | 1.4e-4 | +6.0e-7 | +3.3e-3 | 3.3e-5 |
| H2 D=24L (1,8,32) | PASS (marginal) | 8.0e-4 | −1.8e-6 | +3.3e-3 | 6.4e-5 |
| H3 new seed, nb=1024 | PASS | 3.6e-5 | +2.5e-6 | +1.3e-2 | 5.4e-5 |
| H4 4× window | **FAIL** | **1.9e-3** | −4.1e-5 (0.5% of work) | −8.4e-3 | 5.8e-5 |
| H5 intruder, rate 8 | PASS | 5.0e-5 | +2.9e-5 | −1.8e-2 | 6.6e-5 |
| H5 intruder, rate 32 | PASS | 2.8e-5 | −5.9e-7 | −1.8e-2 | 1.1e-5 |

- H4 growth exponent of the position-error trajectory: **1.799**
  (near-quadratic: a systematic phase walk from the linear readout, not
  noise; the energy error stays bounded — the adiabatic invariant holds).
- ℓ=1 fails at D=12 at every rate (structural quadrupole miss, dE flat in
  rate): quadrupole is the load-bearing channel near-in; ℓ≥3 adds nothing
  at 12–24L (ferr plateau set by quantization+interp, not truncation).
- H5 diagnosis: intruder quadrupole = m·a² = 0.0043 vs planets' Σm·a² = 1.72;
  amplitude ∝ a² anti-correlates with frequency Ω ∝ a^(−3/2). The
  channel's bandwidth is the **amplitude-weighted** spectrum — fast light
  structure is invisible, exactly the ant/lion rule (P33) arriving as
  physics, for free, from the a² law.
- Determinism: H1/H2/H3/H4 ran twice in independent processes; printed
  metrics identical to all digits shown.
- Byte price: 8 reals × 32 bits × 8 samples / P_ref = 2048 bits = 256 B
  per system per innermost-planet period ≈ 19.9 kbit/time-unit. The
  ℓ=1 (wobble) channel would ride the doll's existing centre-tube in the
  engine (law.md, "the origin falls"), leaving ~5 reals of true news
  [INFERENCE].

**Commands** (each single config ≈ 15–90 s; grids stated):
- Sanity of the expansion (1 s): the smoke check in the transcript —
  ℓ≤6 unquantized vs direct sum at r=12.2L: rel err 3.1e-12; at r=0.59L
  (inside the cell): 4.7e-3 — multipoles are a far-field channel only.
- Calibration grid (22 configs, 322 s): `python3 news.py calib`
- One config: `python3 news.py single 1 256 12 0.1 8.37 2 8 32`
- Held-out: `python3 run_part.py A` (276 s), `B` (—), `C` (118 s),
  `D` (94 s), then `python3 merge.py` → `metrics.json`.

## Predictions

`predictions.md` was written after calibration, before all H-runs.
- **Held (4/8):** H1 both (same config passes at 64 and 1024 light
  bodies; error *shrinks* with nb as predicted); H2 (2,8,32) passes at
  24L; H3 independent seed passes; H5 rate-32 passes.
- **Missed (4/8), each diagnosed:** (1) H2 ℓ=1 at 24L predicted FAIL,
  passed marginally (8.0e-4 = 80% of threshold; seed/phase-dependent —
  grading to dipole-only at 2× distance is real but not safe); (2) H4
  predicted exponent ≤ 1, measured 1.799 — the linear readout walks; (3)
  H5 rate-8 predicted FAIL, passed — my scene sizing ignored the m·a² law
  the experiment then exposed; (4) the H4 window also failed the frozen
  position rule outright. Misses 1–3 say the channel is *cheaper* than my
  guesses; miss 2/4 says its readout is *more* expensive. Both directions
  matter for adoption.

## What would make it wrong

- Interiors were Kepler generators; a stirred or chaotic interior raises
  the amplitude-weighted bandwidth — untested. (H5's mechanism — a²
  suppression of fast inner structure — suggests it stays cheap, but a
  mutually-interacting binary of comparable masses at small a would raise
  the quadrupole amplitude at 2Ω_binary; that case is open.)
- One system, one observer, no nested hierarchy run: the O(depth)-streams-
  per-body claim is inference, not measurement.
- Retardation/aberration not modelled (a constant light-delay does not
  change information rates [INFERENCE]); per-pair correctness is
  b-news-gravity's falsifier (Carlip 2000), untouched here.
- My thresholds were frozen by me before held-out runs but chosen by me;
  a checker should attack them (e.g. does ℓ=1-at-24L survive other seeds).

## Cost of adoption, fit with PRINCIPLES

Adoption: a per-doll news emitter (sample at the doll's own bandwidth,
fixed-point with the doll's shared exponent — bounds from the doll table,
tighter than my kinematic bound, which was 6.5× loose and is why 16 bits
failed), a distance-graded channel table (ℓ=2 near, ℓ=1 far, ℓ=0 static),
and the reader is the existing tide kick widened to quantized channels
with the law's **second-order ramp** between samples (law.md line 33) —
H4 is the measured reason that ramp is not optional. Near field
(encounters, two-tier certificates) unchanged.

- P3 "Compute only surprises. Cost follows change and entropy": emission
  rate = the interior's own variation rate; nothing is sent for a static
  doll beyond its monopole, once.
- P6 "Store the generator, not the generated. Aggregates matter": 16× the
  bodies, identical bytes (H1).
- P7 "Multipoles are the mechanism, for gravity and for causality regions
  alike": measured as a causal *channel*, not just a moment.
- P23 "it allows to cheaply partition compute, even gravity is light
  speed": the partition unit is the quantized news stream.
- P33 "a raindrop is an event for an ant and nothing for a lion": H5's
  m·a² law is this principle as physics.
- P13 "Errors never compound": H4 shows where it *would* compound
  (position phase, t^1.8) and that the invariant (energy) does not — the
  adoption carries the second-order ramp and re-anchoring to honour it.

## Prior art (scout deliverable), ranked by fit

1. **Spectral (multipole) news on the light cone** — the mechanism
   measured here. Physics source: far-zone multipole expansion and Bondi
   news/memory (Blanchet 2023, arXiv:2303.07732 — abstract verified; the
   memory integral meaning the absorber retains O(channels) state, not
   O(history), is textbook GR [UNVERIFIED in this run]). Algorithmic
   source: **plane-wave time-domain FMM** (Ergin, Shanker, Michielssen
   1998–2004; multilevel PWTD for transient wave scattering — titles/
   authors verified, mechanism details UNVERIFIED): retarded, band-limited
   translation of group radiation, the proof that causal group-to-group
   delivery is not O(N²) for wave equations. Maps: doll = group; emission
   = quantized q_lm(t); near field direct (my r<L check). Failure modes:
   linear-wave machinery (GR weak-field superposition is the regime; the
   strong field stays inside the doll tree); float machinery needing our
   integer quantization.
2. PWTD plane-wave basis variant — same channel, anisotropic delivery;
   more machinery than spherical harmonics; no fit gain at our ℓmax≤2.
3. **Send-on-delta / conflation** (networked control, HFT feeds) — not a
   field representation but the *emission schedule*: send a channel only
   when it moves by one quantum. Complements 1; untested here.
4. Instantaneous FMM/tree codes (Dehnen's Cartesian expansions, hybrid
   cosmological FMM) — rejected: no causality, no channel, hides the
   light cone.
5. Null-hypersurface (characteristic) grid evolution — rejected: O(surface)
   grids, float cathedrals, wrong scale for a game.

## The lens

The scout lens trusts other fields' framings: PWTD is linear-wave and I
did not test the nonlinear or nested cases; the "best solution anywhere"
here turned out to be the physics' own (multipoles-as-channel), with the
literature as evidence of feasibility rather than as a component to
copy. Thresholds, scene design and the linear readout are all mine and
unaudited; the H5 scene-sizing error shows how easily my priors about
"what stresses the channel" are wrong in both directions.
