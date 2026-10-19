# Predictions — 20261019-0015 (second author on 20261018-2312-system-9eeb)

The checker's named gold experiment, pre-registered before any on-arm gate run. The off-arm
control (`behave --law plane --gates B12,B13,B17`, ES_QMEMO unset) is the shipped law and is
expected to PASS as it stands on main; it is run for the baseline detail lines, not as a
prediction. Decisive arms: the same gates with `ES_QMEMO=1`, and the belt cell census at the
11+11 width (new instrument, `crates/universe/tests/qbelt.rs`).

P1 — **B12 (Jacobi handoff drift, the dephasing probe the checker named).** PASS under
ES_QMEMO=1: median growth exponent ≤ 0.2 (mechanism: every kick re-fits the exact (E, L) from
the readout state, so the cell's shape error is re-anchored per segment — bounded wobble, not a
compounding drift; the killed write-back form is not in play), and every ship's max |ΔC_J/C_J|
≤ 1e-4 with at least 2× margin (my estimate: ≤ 5e-5 — per-segment state error ~2π·6e-5·(τ/P),
with kicks many times per radial period, re-absorbed into new exact invariants at each rebind;
the walk in E, L has steps of that size and 200 periods of segments, so ≤ ~1e-5 median ship,
worst ship ≤ 5e-5). The risk I am watching: the worst ship's max err crosses 1e-4 (the census's
worst period error, 6.8e-4 relative, is the same order as the band; a ship whose segments ride
the worst cell could trip it). If it fails, that is the clean refutation and I report it as
such, not as noise.

P2 — **B13 (assists).** PASS: ≥ 99% of judged flybys within 1% of the reference ΔE/ΔL. The
flyby itself is a Passage (unaffected: `served` only arms `Trajectory::Cycle`), and the
heliocentric Cycle segments carry ~1e-5-level state error, three orders under the 1% band.
Confidence high; exclusion share unchanged from the off-arm (same reference, same draws).

P3 — **B17 (resonance), the tightest.** PASS with movement: e-pump ratios stay in [0.8, 1.25]
and regimes match everywhere asked. The cell's period error (med 5.8e-5) is ~7% of the smallest
detuning step (±W/3 ≈ 8e-4 at μ = 3e-5, W = 2.5·μ^(2/3)); a detuning shift of that size moves
the pump by well under the 25% band. I predict the on-arm pump ratios differ from the off-arm's
by ≤ 10% relative; the controls (nothing resonant) hold their e within 20% trivially. Risk: a
case sitting at the libration/circulation excursion boundary (~2π) flips regime — those cases
are not asked by construction, so the risk is the amplitude ratio's 0.8 floor.

P4 — **Belt cell census (the unmeasured half).** Distinct occupied cells at birth is SUBLINEAR
in belt bodies and saturating: on the weak branch `shape_bits` drops the radius entirely, so a
belt body's cell is its 11-bit gap fraction + 6-bit gap exponent only; with e Rayleigh (σ 0.07,
re-drawn above 0.4) I predict ≤ 2^11 occupied gap cells and in practice ≤ ~300 distinct cells
for N = 2,000 belt bodies (locals excluded), i.e. cells/belt-body < 0.2 and flat in N when N
doubles (cells(4,000) − cells(2,000) ≪ cells(2,000)). If instead cells ≈ N − locals (one cell
per body), the memory win caps at eviction and I say so. The belt stream itself is quiet
(belt ships re-key on encounters, not cadence), so the birth census is the standing-shape number.

P5 — **Cell width is load-bearing on the branch, not the body.** For the belt population the
strong branch (compactness > 2^WEAK_EXPONENT) is empty — every belt cell is a weak-branch cell
(radius dropped). I predict 0 strong-branch cells in the census; if any appear, the census
splits by branch and both are reported.

P6 — **Determinism under the gates.** The on-arm gate detail lines regenerate identically on a
rerun (same seed, same frozen ships): the served law is a pure function of the key, so the
plane's answers are reproducible. (Not bit-compared to the off-arm — the law changed, that is
the point.)

Written before the first ES_QMEMO=1 gate run and before the first belt census run. The off-arm
control was launched first and is the shipped law (known PASS on main); no on-arm number below
influenced these bars.
