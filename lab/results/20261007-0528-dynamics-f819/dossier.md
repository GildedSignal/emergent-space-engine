# Dossier: the dynamics red-team of B12's proposed arrow statistic (channel coverage, null, gray zones)

## Claim

The arrow-of-time statistic proposed to replace B12's exponent (`q-b12-design-9242`, whose checker
died on a 429 and was never graded) survives the phase-channel attack my lens predicted would kill
it — the CR3BP's rotating primaries give the Jacobi functional O(1) gain along the orbit, so phase
errors trip either the arrow (sub-wrap drifts: clock 1e-4 reads z = +9.96) or the 1e-4 cap
(wrapped walks: phase-walk reads z = +2.49 with 150 R_H of position error) — and its N(0,1) null
is honestly measured (permutation sd 0.93–1.03, p95 ≤ 1.67), but a **memoryless bounded offset
switched on mid-horizon reads z = −1.26 on the plain path and +6.40 on the fma path: a
machine-dependent verdict on a bounded law**, the only verdict flip found, and the one gray zone
the freeze must resolve before B12 is re-frozen.

## Bottleneck

HANDOFF "Headed next" #2: "B12 rebuilt and frozen … red-teamed first". This run is that red-team's
dynamics half, on the one B12 candidate that exists in code. Not a 10× speed gain: a
gate-correctness probe; the cost of skipping it is freezing an instrument with an unmeasured null
and an unrecorded verdict instability. PRINCIPLES 13 ("errors never compound") and 34 (oracles are
guards, not shepherds) are the invariants at stake.

## Evidence

All numbers from a copy of the candidate crate (crates and gates untouched), on this Linux box,
8 vCPU, each command ≤ 46 s, peak RSS 2.9 MB.

```
cd lab/results/20261007-0528-dynamics-f819/work/b12arrow
cargo build --release                                   # CARGO_TARGET_DIR honored
$CARGO_TARGET_DIR/release/b12arrow --channels > ../redteam-plain.txt   # 46 s: table + channel
$CARGO_TARGET_DIR/release/b12arrow --fma        > ../redteam-fma.txt   # 35 s
$CARGO_TARGET_DIR/release/b12arrow --permute    > ../permute-plain.txt # 28 s: the null
$CARGO_TARGET_DIR/release/b12arrow --fma --detail=step                  # per-ship rows
```

**1. Reproduction (before any edit of mine).** The candidate's full table regenerates exactly on
this machine: echo −2.68, scaled +1.50, planted-bounded +0.90 (worst 1.27e-5), planted-compound
+27.65, planted-drift +36.90, planted-kick +42.03, leak 3e-9 +44.29, periodic −14.40 — every
verdict as in its dossier.

**2. The phase-channel attack (my central prediction) — killed by the scene, honestly.** Plants:
`clock r` (the exact conserving reference read at t(1+r)) and `phase-walk` (the time offset
random-walks ±0.01 P per SOI entry — the exact dual of planted-compound, which walks C_J and is
caught at +27.65). Results (plain / fma):

| law | z_pool plain | z_pool fma | worst_err | along-track vs echo, med Q1→Q4 (R_H) | verdict |
|---|---|---|---|---|---|
| clock 1e-4 | +9.96 | +4.56 | 2.3e-1 | 0.21 → 30.8 (max 108) | FAIL (arrow plain, cap both) |
| clock 1e-3 | +4.04 | −1.69 | 1.7e-1 | 2.1 → 31.7 | FAIL (cap) |
| phase-walk | +2.49 | +9.31 | 3.4e-1 | 0.60 → 32.4 (max 150) | FAIL (cap) |

The arrow **alone** is blind to fully-mixed phase walks (z = +2.49 plain while the ship decorrelates
by 150 R_H); what fails these laws is the 1e-4 **magnitude cap**: C_J, evaluated against the
primaries at the sample time, oscillates with O(1) gain along the orbit (2Ω(x·v_y − y·v_x) and
2μ/r₂ react to the synodic phase), so a phase offset reaches C_J amplitude ~0.2–0.3 here. Slow
drifts that do not wrap within the horizon read as leaks and ARE caught by the arrow (clock 1e-4,
z = +9.96). Consequence for the freeze: the phase channel (the tube's Δt/Δφ quantization is a real
instance) is certified **by error size, not error type**, and only for scenes with this O(1) gain;
the gate should say so, and the certified horizon is what bounds the invisible walk below ~5e-5 rad.

**3. Anti-persistence does not hide compounding** (held): planted-compound with AR(1) increments
(φ = −0.9, stationary variance matched; effective leak 19× weaker) still FAILs: z = +8.25 plain,
+10.02 fma. The rank test is scale-free; no hiding by negative increment correlation.

**4. The null, measured.** Permutation of the gap labels within each ship's pairs (400 shuffles,
conditional on the |r| multiset), pooled exactly as the gate pools: sd 0.93 (echo), 0.95 (scaled),
1.03 (bounded), 0.93 (periodic); p95 ≤ 1.67; max ≤ 3.04. The claimed N(0,1) is honest and the 4×
pair-dependence allowance is conservative. But `periodic 1e-7`'s z = −14.40 is ~15 measured sd out:
real |r|-decreasing-with-gap structure from a genuinely bounded error. **The gate's one-sidedness is
load-bearing** (a two-sided 5σ gate would false-fail bounded periodic errors — quantization beating
against synodic frequencies is exactly this shape in a real law).

**5. The verdict flip.** `step 95P`: a permanent 3e-9 Jacobi offset switched on at t = 95 P —
memoryless, bounded, must pass. Plain: PASS (z = −1.26). Fma: **FAIL (z = +6.40)**. Per-ship on the
failing path: z from −4.91 to +7.58, `leak` coefficient −3e-9 to −1.4e-8 — the same order as a real
leak's, because the switch at 95 P sits near the matching's half-horizon boundary (early endpoints
in [95,100] P carry no offset), so step-landing correlates with gap through the pair population,
and chaos re-deals the pairs between rounding paths. The discriminator that does separate them is
per-ship consistency: the true `leak 3e-9` plant reads `leak = +3.00e-9` on 15/15 ships (ties 0),
while the step reads scattered negatives (-3e-9 to -1.4e-8) — reporting the per-ship leak
coefficient alongside z gives the integrator the read, at zero new cost (the field is already
computed). This is the only control whose verdict depends
on the machine, and it is a *bounded* law: the error class "time-localized signature change" is the
statistic's live gray zone. Margins on chaotic plants swing hard between paths in general (clock
1e-4: 9.96 → 4.56; phase-walk: 2.49 → 9.31); only strong-effect verdicts are path-stable.

**6. Record note.** The crate's header says "the pooled gate statistic is the median per-ship z";
the code pools with Kendall variances (z_pool, matching the dossier). The doc comment, not the
code, is wrong — worth fixing at freeze so the frozen text says what ships.

## Predictions

`predictions.md` was written before the plants ran (P4, P5 held; P1–P3 failed — the kill criterion
fired and the gameability premise is reported dead). The miss is informative: I argued C_J is
constant along the orbit, so phase error lives in its kernel; in fact the functional's
time-dependence (rotating primaries) breaks exactly that degeneracy, with O(1) gain. The substructure
my prediction did not contain: the arrow/cap crossover (sub-wrap drift → arrow; wrapped drift → cap).

## What would make it wrong, cost, fit

Wrong if: the C_J-vs-phase gain is scene-dependent and a future B12 scene (near-circular,
co-rotating populations) has weak gain — then the phase channel reopens (my original attack lands);
or the step-95P flip is an artifact of this exact offset/horizon ratio — a sweep of switch times
would bound it (the one experiment this run leaves). Cost of adopting the findings: zero code —
record the measured null, keep the gate one-sided with the reason attached, add a time-localized
bounded control to the freeze suite, and state the phase channel's cap-delegation in the gate text.
Fit: PRINCIPLES 13 as error *type*; 10 ("measure before claiming") — the null is now measured, not
assumed; 2 ("behaviours matter, not error size") — the phase channel is currently certified by size,
which the freeze should name as a known limit rather than discover later.

## The lens

The dynamics lens looked for attractors and conserved quantities in the error process, and its
conserved-quantity instinct is exactly what mis-led it: treating C_J as the certificate hid that a
functional's *time-dependence*, not its level sets, decides channel coverage. What the lens did
catch that the design lens had not: the null is a dynamical claim (exchangeability of returns) that
must be measured, not derived — and bounded errors with time-structure (periodic, switched) violate
it in both directions. Missed by this run: no sweep of switch times; no per-ship map of the
C_J-vs-phase gain (the weakest ship is where the channel reopens); multi-planet scenes (no Jacobi
constant) remain outside B12 entirely.
