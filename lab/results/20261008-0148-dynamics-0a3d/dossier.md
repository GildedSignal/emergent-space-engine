# Dossier — 20261008-0148-dynamics-0a3d (lens: dynamics and attractors)

**Claim.** The belt's encounter stream cannot avalanche (the e↔rate feedback is self-regulating at
every mass ratio, and the rate saturates at λ_max ≈ 0.48 events/body/orbit when every annulus
overlaps), and it is not memoryless: half the events are per-pair trains locked to integer
multiples of the synodic period (cold-belt Fano F(10 orb) = 2.25 vs Poisson 1.00), so smoothness
budgets must carry a √F variance multiplier — but exact-period fleets are *under*-dispersed
(F(1 orb) = 0.13, p99 below Poisson), so concentration threatens candidate-tier setup cost, never
stream timing; no cascade gate is needed.

**Bottleneck.** Board #4 (smoothness/allocator: "p95/99 results… the algorithm that allocates the
work") and the top scaling risk (candidate work must track real encounters). The allocator's input
assumption — how surprise arrivals cluster — was unmeasured. This run deletes the worry it was
sized for (cascades, fleet bursts) and replaces "Poisson at the mean rate" with two measured
numbers (λ_max and the F multiplier), at zero runtime cost: the trains it exposes are exactly what
the Diophantine synodic certificate already schedules.

**Evidence** (exact, deterministic per seed: the repo's own `truth_pair`, every distance-minimum
below ρ; no candidate tier involved; all raw streams + `reproduce.sh` in `work/`).

- λ(σ_e) sweep, N=500, a∈[0.96,1.04] (W=0.08), ρ=3e-3, 400 orbits, seed 20261002:
  σ_e {1e-3, 3e-3, 1e-2, 3e-2, 8e-2, 1.5e-1} → events {10325, 16682, 43522, 82536, 94176, 95842},
  i.e. λ = 0.052→0.479/body/orbit, monotone rising, slopes 0.44→0.80→0.58→0.14→0.03 — saturation at
  σ_e·a ≈ W, no falling branch (a conjunction miss is 1-D: the conjunction itself enforces
  azimuthal alignment, so dilution ∝ρ/σ_e cancels the partner gain ∝σ_e only at saturation).
  Second seed ±2% (17006 vs 16682; 43288 vs 43522).
- Stream statistics (same belt family; Poisson control = same count resampled uniformly,
  F̄ = 1.00±0.02 and p99 band reported; `work/analysis.txt`):
  - cold σ_e=3e-3: F(1 orb)=1.18, F(5)=1.59, F(10)=**2.25** (Poisson p99 of F: 1.57), F(20)=2.15;
    49.5% of events from repeat pairs; median per-pair gap = 1.0005·T_syn for warm belts
    (2.0, 2.5, 2.97·T_syn at hotter σ_e) — trains locked to the synodic clock; co-orbital pairs
    (T_syn > horizon) are 19% of pairs but hold **28%** of events (8.8% in the warm belt).
  - warm σ_e=1e-2: F(10)=1.26 (second seed 1.03) — trains thin as predicted.
  - fleet (keys=8, 62 bodies per exact period): F(1 orb)=**0.13**, p99 44 vs Poisson 53 —
    under-dispersed; one frozen pair emitted 850 perfectly periodic events. Timing is *safer*
    than Poisson; the gold 20261006-0346 cost of concentration is setup, not arrivals.
  - inter-arrival CV ≈ 1.0 and burstiness ≈ 0 in every regime; p99 window counts within ±3% of
    the Poisson prediction at the same mean (the correlation lives in the variance, not the tail,
    at these densities).
- Cascade closure (`work/cascade.py`, λ from the measured sweep, impulse stirring with Coulomb
  log, both bodies kicked): pumping slope d ln(λ·⟨δe²⟩)/d ln E = −0.37…0.00 for mass ratios
  1e-12…1e-6 → sub-linear growth, no finite-time blowup anywhere; a m=1e-8 belt walks σ_e from
  1e-3 to 1.1e-2 in 400 orbits with λ ∝ t^0.37, then saturates. The rate can only grow to
  λ_max ≈ 0.48/body/orbit (measured ceiling, not an assumption) and takes ≥ 100s of orbits to get
  there.

**Predictions** (`predictions.md`, written before the runs): P1 falsified (no 1/σ_e falling
branch; misses are 1-D, saturation instead — the measurement corrected my model); P2 half-held
(F(10 orb)=2.25 ≫ 1.3, but F does not relax to 1 by 20 orbits and the repeat share is 49.5%, a
hair under 50%); P3 held (warm F < cold F); P4 falsified (fleets under-dispersed, not ≥5×
bursty); P5 held (self-regulating), though through per-encounter weakening, not the sign I
assumed. Controls: every Poissonized control landed at F=1.00±0.02 — instrument healthy. The
kill criterion as pre-registered (F(1 orb) < 1.2) sits at 1.18 — marginal at 1-orbit windows;
at 5–20-orbit windows the clustering is decisive.

**What would make it wrong.** (1) The closure is incoherent-only: coherent e-pumping (resonant
chains — H0203's "resonance kills averaging" — or player fleets as external sources) can break
"no avalanche"; that regime needs its own probe. (2) Fixed-orbit streams: feedback enters only
through the closure, not a self-consistent perturbed run. (3) One belt family (Rayleigh e,
uniform a, N=500, ρ=3e-3): the λ_max ∝ N·ρ/W scaling is argued, not measured across N.
(4) F at 20 orbits rests on 20 windows — wide CI; read orders, not digits (cloud run, Linux/x86,
8 vCPU, ~2 GB). Cost of adoption: none in code; the allocator design takes two constants
(λ_max, F∈{2 cold, 1 warm, <1 fleet}) and one confirmation: budget frames from mean + z√(F·mean),
and schedule trains by the synodic clock rather than treating arrivals as surprises.

**Fit with PRINCIPLES.** "Compute only surprises" (3): half the stream is not surprise at all —
it is the synodic clock, derivable when looked at; "the algorithm that allocates the work to
prevent those heavy tails, it's the most important one" (12): its input is now measured, and the
tails it feared (cascades, fleet bursts) do not exist; "the simulation tells us what's next not
us" (22): the next encounter of a repeat pair is k·T_syn away, k ∈ {1,2,3} measured.

**The lens.** A dynamics lens measured arrival statistics but not *work per event* (the cost
distribution of an encounter, which multiplies these counts), not burst duration of co-orbital
clusters at frame scale (< 1 orbit), and left the chaos/KS side untouched. Its bias to attractors
found regulation where the board feared avalanches — a negative result, but sized by exact event
counts, not by a model of a model.
