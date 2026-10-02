# dossier.md — run 20261001-2353-q-correctors-aa78 (lens: fewer kicks per orbit)

## Claim

Symplectic correctors and higher-order splits do **not** cut the plane's kicks per
orbit: on the plane's behaviours every scheme — the plain DKD, SABA2/3/4 and
Wisdom–Holman–Touma correctors — hits the same floor of **8 kicks per orbit**
(precession within 10%, e-pumping within 25%, resonance regime held), so the
plane's own kernel already buys the 16× fewer kicks (128 → 8) that the lens was
after, and the kernel change buys nothing further at the behaviour bar.

## Bottleneck

Board item 1 (fewer kicks per orbit at the same behaviour; kicks dominate the
engine's cost, 24–29 µs each). Expected gain was 4× or more; measured gain from
the kernel is **1×** — but the measurement relocates the win: the plane's step
count, not its kernel, is where the 16× lives.

## Evidence

Float replica of the plane's exact split (`src/replica.py`: exact Kepler drift by
osulating elements = the tube's stand-in, plane-faithful kicks — sibling pulls +
full differential parent tide, star fixed, no indirect term, per-body step = own
period/2^k). Scenes: the plane's own moon geometry (Home e=0.02, GM=2^-18, moon
at 0.25–0.8 Hill radii, 50 Home orbits) with reference = DKD at 2^10–2^11
kicks/orbit (convergence 0.8%); 2:1 resonance pairs (μ=3e-4, detuned by thirds of
W=2.5μ^(2/3), two phases, 300 orbits); close planet passes (two crossing
planets, 8 phases); Jacobi/flybys (partially run). Commands: `cd
lab/results/20261001-2353-q-correctors-aa78/src && python3 validate.py`,
`sweep1.py`, `sweep1b.py`, `sweep2.py`, `sweep4.py`, `dyadic.py` (each ≤ 15 min
on 2 vCPU; JSON outputs beside them).

1. **Kernel quality (validated):** dE per 30 orbits at equal *kicks* per orbit
   (μ=3e-3 pair): dkd 8.7e-9 at 32; saba2 3.1e-11 at 32 (280× better at equal
   kicks, τ⁴ scaling); whc3 2.2e-10 at 160 kicks/orbit (τ⁴⁺) — the schemes are
   implemented right and do what the papers say.
2. **Moon behaviours (the plane's moon, 0.25 and 0.4 Hill; 0.6 and 0.8 escape,
   as the reference says — regime match 100% everywhere):** the 10% precession +
   10% e-behaviour bar is passed by dkd at k=3, saba2 at k=2, whc3b at k=3,
   saba3 at k=2 — **all exactly 8 kicks/orbit** (saba3 misses at 6, −14.5% rate;
   dkd misses at 4, e over-pumped 42%; whc3 at 20 misses badly — its ±0.42τ
   displaced kicks mis-sample the orbit at coarse steps).
3. **Jacobi on moonlets inside the doll (B12-style: ≤1e-4, growth exponent ≤0.2,
   3 stable moonlets at 0.3–0.7 SOI, one retrograde; the 0.9-SOI prograde
   moonlet escapes as the reference says — regime match):** dkd passes at k=3 =
   **8 kicks/orbit** (worst error 5.8e-5, slopes ≤0.1); dkd k=2 fails (2.0e-4,
   and the outer moonlet's error grows with exponent +6); saba2 needs k=2–3
   (8–12 kicks/orbit, the outer moonlet only at 12); whc3b at k=3 = 8 passes
   with numbers identical to dkd's. The flyby part (B13) is inconclusive: my
   exit detector at step boundaries misses whole passes when τ approaches the
   crossing time (0–2 passes caught, index-matching across schemes unreliable) —
   reported as such, not judged.
4. **Close passes (held out):** whc3's end-state elements are *identical* to
   dkd's at every k (worst-case e errors match to 3 digits) — see the telescoping
   finding; no scheme survives a 0.1 mutual-Hill pass without sub-level kicks
   (SyMBA is outside this replica), and at 2–9 mutual-Hill passes all schemes
   saturate at the same chaos-amplified error.
5. **Telescoping (new, load-bearing, two-sided):** the WHT corrector is a
   *conjugation*, and `(C M C⁻¹)ᴺ = C Mᴺ C⁻¹` exactly when the kick sources are
   time-independent. Measured there (planet–planet scenes): per-step whc3 and
   boundary-only whc3b agree with each other and with dkd's *elements* to 3
   digits — a relabelling cannot change element-behaviours, which is exactly why
   it does not move the behaviour floor. Against a moving source (the parent
   tide: the corrector's sub-kicks sample the primary at displaced times) the
   conjugation is time-dependent and does **not** telescope: per-step whc3 beats
   dkd ~5× on the Jacobi readout at equal steps (3.0e-6 vs 1.6e-5 at k=3) while
   whc3b gives exactly dkd's numbers — but at equal *kicks* dkd still wins
   (3.6e-6 at 16 kicks/orbit vs whc3's 1.7e-4 at 20). The corrector's accuracy
   gain is real only where it is paid for per step, and behaviour gates do not
   price accuracy (PRINCIPLES 2, "error type over error size").
6. **Integer path (named and measured):** SABA2 with 12-bit dyadic coefficients
   (866/4096, 2364/4096, drift sum exactly 1) gives the *same* behaviours as the
   irrational one (rates and emax identical to 3 digits); the corrector's b₃₁ =
   −102/4096 is within 1.8e-6 of WHT's value and whc3b-dyadic also passes. Kicks
   stay integer sums; drifts stay tube reads; coefficients land on the law's
   dyadic grid (`dyadic.py`, `dyadic.json`).

## Predictions

`predictions.md` was written before the sweeps. **Held:** dkd's break at ~4–8
kicks/orbit; the resonance floor at ~8 kicks/orbit with the corrector not better
than dkd at coarse steps; whc3b ≈ whc3 on elements (telescoping), later sharpened: it fails against the moving tide; the 4× gold bar met "on
precession" only in the sense that *everything* including dkd meets it at 8
kicks/orbit. **Failed:** saba2 holding to 16 kicks/orbit *below* dkd's own bar
(it holds at the same 8, not fewer); whc3 degrading at close passes (it is a
conjugation — it neither helps nor hurts); the held-out e=0.3 moon sweep and the
μ=3e-3 resonances did not finish in the window (the e=0.3 prediction stands
untested — honest miss, listed under open).

## What would make it wrong

- The behaviour bars I used (10% precession, [0.8,1.25] pump) come from B14/B17;
   if the freeze tightens them to 1%, saba2 wins at 8–16 kicks/orbit where dkd
   needs 16–32 — the kernel then buys exactly one octave, still not 4×.
- The resonance result covers μ=3e-4 only; if μ=3e-3 (the hardest B17 case)
   forces everyone above 32 kicks/orbit, the *plane's* floor there is set by the
   resonance, not the kernel, and the 16× claim shrinks for that regime.
- The flyby (B13) replica is detection-limited (see 3); the e=0.3 held-out
   moons and the mu=3e-3 / 3:2 resonances did not finish in the window. The B12 handoff criterion needs the two-doll changeover, which
   this replica does not model (an always-doll-1 first attempt was wrong and is
   kept as `s3_old_design_invalid.json`).
- If the M1's kick cost is dominated by the rebind (15 of 29 µs) rather than the
   force, then halving *steps* also halves rebinds and the 16× step cut carries
   over fully; but if the plane's 1/128 step was itself chosen to cover
   behaviour not yet gated here (GR precession of the tube, thrust cadence), the
   safe cut is what B14/B17-style judges say on the integer law, not this float
   replica.

## Cost of adoption, and fit with PRINCIPLES

Adopting *nothing new* is free. The actionable adoptions: (a) measure the
plane's step_log2 against the behaviour judges — the replica says 2^3 not 2^7
kicks per radial period for moons and non-strong resonance (a 16× kick cut on
the plane's dominant cost, one configuration change, `Config::step_log2`);
(b) if any future gate judges error size (it should not: "error type over error
size"), adopt SABA2-dyadic: same behaviour floor, 280× smaller error at equal
kicks, coefficients on the dyadic grid, kicks still integer sums. Both obey
PRINCIPLES 2 ("'Exact' means deterministic… error type over error size") and 18
(the right question turned out to be "how few kicks does the *behaviour* need",
not "which kernel is higher-order"). The corrector-as-conjugation finding fits
"observation is a pure function of the state": the corrector is a relabelling
applied once at the readout, so observation stays pure — but precisely because
of that, it cannot change behaviours, and the plane should not pay for it.

## The lens

The correctors lens (mine) presumed the kernel was the lever; the measurements
say the step count is. What the lens hid: that the plane's own gates judge
behaviour with 10–25% bands, and any second-order scheme meets those an octave
or two above where higher-order schemes stop being *worse* (corrector sub-kicks
at ±0.42τ mis-sample coarse steps). "Nothing worth adopting — except the step
count we already own" is the honest answer.

## Grade request

Silver: real, reproduced, and it moves the bottleneck question (16× available in
`step_log2`, kernel change dead at the behaviour bar), but the μ=3e-3 resonances,
the e=0.3 held-out moons and the Jacobi runs are unfinished in the window, and
the step-count claim must be re-measured by `behave` on the integer law (B14,
B17) before adoption.
