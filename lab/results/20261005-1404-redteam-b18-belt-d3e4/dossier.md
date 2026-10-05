# Dossier — red-team of the B18 belt row before its freeze (run 20261005-1404)

## Claim

The B18 belt row's premise holds against every loud adversary (clips at its own threshold, repeats,
neighbour copying, thread order, lattices all fail loudly; the gold's two-level table passes), but three
invariants have measured holes a frozen gate should not have: a belt that crushes 15% of the protected
tail's spread passes every run (`crush85`), a belt with a hollow inner edge passes every run (`innerclip`),
a belt whose 100k deep dippers all dive one periapsis corridor passes every run (`aligned`), and criterion
(4)'s byte allowance is the program's own declaration, so a 4 MB one-level table passes it (256× the gold).

## Bottleneck

Board focus item 5 (fitting 10⁹ in 8 GB) and the B18 belt row itself, before its freeze. The gain is not
bytes: it is the gate's power to hold Julien's standing rule ("You cannot average a population … I hate
averages because they crush data especially tail events") once the row is frozen and can no longer be
weakened. Four dispositions below; each is a few lines of judge or one line of row text, and none costs
the gold program anything (it already passes the real judge).

## Evidence

All numbers from `probe.py` (this folder), a faithful mirror of the frozen judge
(`git show wt/b18-belt:xtask/src/behave/belt.rs`, af07b33): the same SPEC, the same SplitMix64 counter
stream and `rayleigh_grid`, and exactly the judge's statistics and thresholds (χ² 128×128 on (p, t_p),
|z| ≤ 4.5; serial 18 lags + cross pairs, |z| ≤ 5; per-column two-sample KS, D ≤ 2.470·√(2/n); tails of e
and p: count z with variance 2K, reach vs the reference's 20th largest, overshoot, tail-shape KS), over
the judge's own frozen `RUNS` (3× 2²⁰, seeds 20261008–10, then 2²³, seed 20261011, stopping at the first
failing run, as the judge does).

Commands (each one run, ~2.5 min total, cloud 2 vCPU):

```
cd lab/results/20261005-1404-redteam-b18-belt-d3e4
pip install numpy
python3 probe.py none table12 winsor lattice serial   # calibration anchors
python3 probe.py crush85 crush75 crush67 crush60 crush50 innerclip aligned table20
```

Full output: `evidence.log`. The real Rust judge was also built and run on its own controls
(`git worktree add /tmp/b18 wt/b18-belt && cargo test --release -p xtask show_the_evidence -- --ignored
--nocapture`): `echo` (the reference program) and `dyadic` (the gold's two-level table) both PASS all
four frozen runs, and its z-values match my mirror where the statistics coincide (e.g. seed 20261010:
χ² z = −0.97, serial worst 2.10 at ω lag 128 in both), up to the reference draw (mine is PCG64, the
judge's xoshiro).

**Calibration anchors (the mirror reproduces the judge's documented plants, each on the intended
criterion):**

| plant | verdict | failing criterion |
|---|---|---|
| `none` (counter stream) | PASSES all 4 runs | — |
| `table12` (the lab's original 2¹² table) | FAILS | tail e: **0 of 105** values reach the threshold (reach, overshoot, shape all fail) — the judge's own number |
| `winsor` (clip at the 10⁻⁴ quantile) | FAILS | tail p range (count survives, 123 vs 105, exactly as the plant doc says) |
| `lattice` (i·g per column) | FAILS | 2-D χ² z = −84.7 |
| `serial` (1/8 of odd bodies copy the neighbour's t_p) | FAILS | serial t_p lag 1, z = 63 |

**Held-out adversaries (the run decides):**

| plant | what it is | verdict | margins |
|---|---|---|---|
| `crush85` | every e above the 10⁻⁴ quantile averaged 15% toward the tail floor | **PASSES all 4 runs** | tail-shape KS D = 0.078 vs 0.121 at 2²³; count z ≈ 0; reach/overshoot pass |
| `crush75` | 25% crush | fails | only the 2²³ tail-shape KS, D = 0.128 vs 0.121; **all three 2²⁰ runs pass** |
| `crush67` | 33% crush | fails | 2²³ tail-shape KS, D = 0.172; all three 2²⁰ runs pass |
| `crush60` | 40% crush | fails | reach at 2²⁰ on seed 20261010 only (2 of 3 seeds pass 2²⁰); tail KS 0.291 close at 2²⁰ |
| `crush50` | 50% crush | fails | reach at 2²⁰ on seed 20261010; D = 0.320 vs 0.328 on seed 20261008 |
| `innerclip` | p clipped from **below** at its 10⁻⁴ quantile (a hollow inner edge, 10× coarser than the tail the row protects) | **PASSES all 4 runs** | per-column KS D ≤ 0.0019 vs 0.0034; every tail test untouched (they test the top) |
| `aligned` | the top-10⁻⁴ of e (the deep dippers) confined to 1/32 of the ω circle | **PASSES all 4 runs** | ω KS distortion ≤ 10⁻⁴; cross-pair z ≈ 0.1; χ² is on (p, t_p) only |
| `table20` | e through a one-level 2²⁰-cell quantile table (4 MB) | **PASSES all 4 runs** | every statistic; see F4 for the bytes |

## The findings, named by the invariant at stake

**F1 — tails survive (row clause 3; Julien: "averages … crush data especially tail events").**
The gate's tail power, measured: nothing that keeps values above the threshold and the top-20's reach is
detected below a 15% crush of the protected tail's spread. `crush85` passes every run with margin
(64% of the 2²³ shape-KS critical). Crushers ≥ 25% die only at 2²³ (tail-shape KS), and 40–50% crushers
die at 2²⁰ only on 1 of 3 seeds (reach, which depends on the belt's own base max — seed-fragile). At 10⁹
the protected tail is 100k bodies; a 15% spread crush is invisible. *Disposition:* accept and state it
(the row's honest noise floor is the 839-value tail sample), or add one cheap statistic with a mean, not a
sup: the mean of ln(e/thr) over the X tail values against the reference's, z ≤ 4.5 (sd ≈ σ/√k, ~3×
tighter than KS at k = 839; catches ~5% crush). I propose the latter; it is three lines in the judge.

**F2 — every body an exact individual (row clause 2; "no Elite style").** `innerclip` hollows the belt's
inner edge — the game-critical tail: low p is the smallest r_p, where handoffs and the changeover live —
at 10× the depth the row protects on the top side, and passes everything, because clause (3) is one-sided
and per-column KS at n = 2²⁰ cannot see a 10⁻⁴ CDF shift. *Disposition:* clause (3) becomes "the extreme
10⁻⁴ of p on both sides, and of e" (the same three order-statistic tests mirrored at the bottom end; the
judge already has the machinery).

**F3 — no structure in the state space (PRINCIPLES 4, 29: emergence, never a winner).** `aligned`
concentrates all deep dippers into one periapsis corridor — at 10⁹, 100k bodies crossing through one
region, exactly the kind of hotspot encounters and contacts feed on — and passes everything: the judge
tests 2 of the 6 column planes ((p, t_p) only) plus global product moments, and a 10⁻⁴-conditional
structure is below both. *Disposition:* clause (3) adds "and the tail's other columns stay uniform": a KS
of ω and t_p over the X tail bodies (k = 839 at 2²³; catches the 1/32 corridor at D = 0.97).

**F4 — the memory floor is information (PRINCIPLES 24; the integrator's own open question).** Criterion
(4)'s allowance is the program's own declaration, bound only by sufficiency, non-growth in n, and the
factor 2. Measured: a legitimate one-level 2²⁰-cell quantile table (tail resolved to 2⁻²⁰) passes every
statistic (`table20`, all runs) and passes (4) by declaring info = 4,194,345 B (charge equal; 4 MB at 2²⁰
and at 2²³, so grown 0 ≤ 16): 255× the gold's 16,456 B, and no bound exists — a 2²⁸-cell table at 2 GB
passes the same way. *Disposition:* only parameters count. The gold already derives its table at birth
and stores 41 B (`ProgramBelt`: "derived at birth, never stored"); freeze the rule that matches it:
`info` is the bytes restore needs beyond what the judge's own spec (41 B) regenerates — mechanically, cap
the declared info of a spec-derived program at 64 B and charge stored tables as store bytes. Table bytes
stayed reported at 10⁹.

**What survives the premise (stated, not strawmanned):** determinism is exact and order-blind (real
judge, all orderings and threads); "within its noise" and "in range" ARE decidable as the judge wrote
them (variance 2K, exact order statistics at 2⁻²⁰ each); repeats, lattices and neighbour-copying die at
z = 63–85; the reference passes its own tests; the gold's ported table passes and the lab's original 2¹²
table fails on tails exactly as Julien feared (0 of 105). The judge is the strongest on this repo; the
holes are the noise floor of n (F1), the chosen sides and planes (F2, F3), and the self-declared
denominator (F4).

## Predictions

`predictions.md` was written before any run. Held: all five anchors; `innerclip` passes; `aligned`
passes; `table20` passes (statistics half measured, bytes half by the judge's own rule); `crush50` fails.
Missed, both in the gate's favour: I predicted `crush75` passes everywhere — it fails the 2²³ tail-shape
KS by 6% (the judge's tail KS is stronger than my order-of-magnitude estimate); I predicted `crush50`
fails only at 2²³ — it also fails at 2²⁰ via reach, but on 1 of 3 seeds only (which is itself the
seed-fragility finding in F1). The honest clean-crush boundary is 15% with margin, not the 25% I
pre-registered.

## What would make it wrong, adoption cost, fit

Wrong if my mirror diverges from the judge: it cannot, on the verdicts — all five anchors reproduce the
judge's own plants on the intended criteria, and the real judge's z-values match mine where statistics
coincide. The findings could be judged acceptable noise (F1) or out-of-scene structure (F3) — that is the
integrator's call, and the dispositions are separable.

Cost: F1 ≈ 3 lines + one calibration run; F2 ≈ 10 lines (mirror three tests at the bottom); F3 ≈ 5 lines
(one KS over tail bodies); F4 = one frozen rule + a cap. None touches the gold program (it passes today's
judge and all four additions: its tails are exact quantile draws, both sides, and its store is 41 B).

Fit: PRINCIPLES 24 ("the memory floor is information theory says so" — F4 is this principle, or the
allowance is not information); the register's "I hate averages because they crush data especially tail
events" (F1 is a measured average the gate blesses); 20 ("determinism ≠ realistic trajectories — the
fidelity question is behaviours", which is why the dispositions are behaviour tests, not representation
rules); 10 ("Measure before claiming" — the power boundary is measured, not asserted). The row's own
words "A requirement from the goal (8 GB), not a size chosen for a representation" (B18) are exactly what
F4 protects.

## The lens

A red-team sees adversaries; it does not build. I did not test what the gate costs a real sculpted scene
(a belt that SHOULD have structure — resonance gaps — is out of the row's scope today, but the same F3
statistics would then need to be scene-conditional, and that boundary is worth one sentence in the row).
I judged the judge as built (af07b33); if the freeze rewords clause (3), my dispositions attach to the
new text, not the old. My tail model (exponential-order) set my priors, and the two misses were both in
the gate's favour — a red-team that only finds its own prior underestimates its target.
