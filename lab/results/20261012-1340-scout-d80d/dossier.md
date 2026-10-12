# Dossier — run 20261012-1340-scout-d80d (lens: scout)

**Claim.** In a resonance-structured belt, H_live is a *rate-class* distinction,
not a bit count: at weak drive 99.9% of bodies produce zero unpredictable bits
per orbit for 10⁴ periods (their twin spread is polynomial and
program-regenerable, so the engine never stores it), the unpredictable set is
0.1% of bodies living inside their nearest resonance's separatrix zone
(Lyapunov times 553–831 periods, predicted from birth by the dimensionless
detuning D = δ/W), and the pre-registered stronger concentration (top 1% of
bodies ≥ 50% of excess) FAILED — the tail the allocator must budget is ~5% at
Gini 0.82–0.87, and a bit-excess-above-baseline metric is the wrong estimator
(regular shear variance dominates it 50:1).

## Bottleneck

H_live, distinctions created per game-second (board risk: "not measured yet;
this, not the body count, decides whether 10⁹ fit in 8 GB"; the b-h-live build
must "define the measure precisely"). Expected gain: not a 10× speedup but the
correct *definition* of the memory-budget quantity — it decides what
`crates/shipmem` scars must hold and what the allocator may forget
(reabsorption), i.e. whether 10⁹ bodies × 51 bits/body is reachable at all.

## The candidate, from the fields (scout deliverable)

The store's three-way decomposition, each part stolen from a field with skin in
the game:

1. **Production = Pesin's identity** (Scholarpedia, verified): a deterministic
   system's rate of new distinctions is Σ positive Lyapunov exponents — bits
   per orbit per body = λ·log₂e. Only exponential divergence is
   unpredictable; polynomial spread is regenerated exactly by running the law
   (PRINCIPLES 3: "Compute only surprises").
2. **Retention = causal states** (Crutchfield & Young 1989, verified):
   minimal stored bits are per-body predictive-equivalence classes. Our
   program+scar store *is* a causal-state representation; a scar grows only
   when the body leaves its program's predictive class — i.e. only in the
   exponential class.
3. **Reabsorption = conditional replenishment** (Hein 1979/1984, verified:
   transmit only changed areas) + the law's own rule ("the cheaper form is
   chosen by exact byte count in idle time" = LSM compaction). The retention
   horizon is the allocator's lever, not the production rate (P5: a saturated
   16-byte tube is 128 bits > the 51 bits/body ceiling, so recompiling is
   mandatory for any body that departs its program).

Known failure mode of the candidate, measured here: near-integrable systems
violate clean Pesin — sticky intermittency (bits(t) curvature: median R² 0.61–
0.91 against a linear fit) and thin secondary stochastic layers at strong
drive. The local normal form is valid only within ~3 resonance widths and weak
drive; outside it, artifact chaos appears (the VOID run).

## Evidence

Model: 4096 bodies, a ∈ [2.1, 3.3] AU, e Rayleigh(0.05); nearest mean-motion
resonance in lowest terms; universal local form (driven pendulum
H = ½P² − cosψ + A·cos(ψ−τ)); birth position in resonant phase space from D =
δ/W; twin offset d₀ = 10⁻¹² = the program's birth quantum. Scripts and data in
`work/`; two decisive runs (A = 0.15, A = 0.05) and one VOID run, all saved.

Reproduce (each ≤ 60 s; Linux x86, orders of magnitude only):

```
cd lab/results/20261012-1340-scout-d80d/work
python3 hlive.py 10000 0.05 d A005    # clean run: summary-A005.json (53 s)
python3 hlive.py 10000 0.15 d main2   # strong drive: summary-main2.json (48 s)
```

The VOID run's artifacts are stored (`summary-voidmain.json`,
`perbody-voidmain.npz`) but are NOT regenerable from the shipped script: they
were produced by the pre-fix instrument, whose diff from the shipped script is
exactly the two changes named in predictions.md's VOID disclosure. Every
number quoted above comes from the two regenerable runs (fixed seeds: belt
20261012, phases 12345).

Clean run (A = 0.05, controls pass):

- 99.90% of bodies: zero exponential divergence in 10⁴ periods; their stock is
  the polynomial baseline, b_reg ≈ 17.0 bits, *regenerable, never stored*.
- Chaotic set: 4 bodies (0.10%), ALL with D < 0.74 (inside one resonance
  half-width); λ-bit 0.0012–0.0018/period (Lyapunov time 553–831 periods);
  positive control 10× far-field: far chaos = 0.0% ✓; negative control
  max far flow 0.0015/period (83% below 10⁻³ — marginal, disclosed).
- Excess-stock metric: Gini 0.82, top 5% share 0.57, top 1% share 0.28 →
  pre-registered P1 top-1% ≥ 50% FAILED. Cause, measured: chaotic bodies carry
  only 2% of the excess — the other 98% is regular bodies' shear-variance
  spread above the median baseline. The *metric* mixes populations; the
  *physics* (all exponential bodies inside D < 0.75) holds.
- Strong drive (A = 0.15): chaotic 1.5%, but layers spread to D = 58 (drive
  resonances of the local form, not belt physics) — the local form's validity
  bound. Gini 0.87, top 1% 0.14, top 5% 0.70.
- Budget arithmetic (P5): even the clean run's saturated bodies (42.5 bits at
  this quantum) exceed nothing at 10⁹ — but a full 16-byte tube does; so
  reabsorption cadence, sized by λ⁻¹ (~500–800 periods for the chaotic tail,
  never for the regular bulk), is the allocator's lever.

## Predictions (see predictions.md)

P1 FAILED on magnitude (top 1% = 14–28% vs ≥ 50%), passed on Gini at A = 0.15
only. P2: linearity R² 0.61–0.91 (failed the 0.98 bar — real intermittency
curvature); negative control marginal-pass at A = 0.05, fail at A = 0.15.
P3 FAILED on the excess metric (leak 21–46% > 25%) but the leak is baseline
variance, not chaos: every exponential body has D < 0.75. P4 VOID — no overlap
region (Chirikov C ≥ 1) exists at realistic widths in this belt; needs a
resonance-crowded scene. P5 held. One run VOIDed (controls failed: artifact
identified, disclosed in predictions.md, instrument fixed, re-run).

## What would make it wrong

A belt with secular/three-body chaos off resonance (ν₆, Wisdom's long Lyapunov
times 10⁴–10⁶ orbits — UNVERIFIED, literature memory) would lift the 99.9%
regular fraction; my local form cannot see it. The libration = drive period
scaling fattens layers (biased toward concentration, disclosed). The 1-d.o.f.
reduction ignores multi-resonance coupling inside overlap zones. If b-h-live's
engine measure (event-based scar bytes) diverges from the twin-rate measure,
the twin framing was the wrong proxy.

## Cost of adoption, and fit

Cheap: no engine change; it sizes and defines b-h-live's dashboard measure —
per-body rate class (exponential/polynomial + λ), never raw spread bits — and
gives the allocator a per-body retention number (λ⁻¹) which is also its slack
("Priority is slack, not proximity", PRINCIPLES 5; "errors never compound", 13:
the exponential class is exactly where predictions go stale and re-checks are
owed). It also feeds the encounters skin: conjunction-prediction certificates
for chaotic bodies decay in ~λ⁻¹, so their re-check cadence is D-predictable
at birth.

PRINCIPLES fit: "Store the generator, not the generated" (6) — the polynomial
bulk is the generator's own output; "Compute only surprises" (3) — only the
exponential class holds surprises; "the memory floor is information" (24) —
the floor here is the rate-class entropy, ~0.001 bits/body/orbit, not 157
bits/body.

## The lens (what scout may have missed)

The literature's requirement is not ours: dynamical-systems theory measures
uncertainty, but our engine is exact — the useful quantity is skip-ahead
validity and scar amortization, which no paper measures directly. I did not
test a crowded resonance scene (P4 VOID), a second seed (one belt, 4096
bodies; the tail is 4 bodies — thin evidence for shape claims), or the
event-based (kick-count) definition against this one. The checker should
rerun with a second seed and a Chirikov-overlap belt before any of this is
adopted.

**Grade sought: silver** — real, reproduced-by-command numbers with controls
that both passed and failed informatively, one named experiment (b-h-live's
measure built as rate classes, judged on a crowded-resonance scene) away from
gold.
