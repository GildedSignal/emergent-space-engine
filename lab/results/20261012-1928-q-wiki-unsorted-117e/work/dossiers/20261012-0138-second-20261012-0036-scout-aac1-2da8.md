# Dossier — 20261012-0138-second-20261012-0036-scout-aac1-2da8 (second author)

## Claim

The checker's named experiment, run to 600 radial periods with an angle-based libration
classifier on a second potential and bar shape, **upholds the original claim and upgrades
it to a design number**: the static resonance flag stays dead (on P1, sustained churn is
35% at eps=0.03, 2.5x the 60-period reading of 14%), the (E,L) drift must be owned by the
kick layer (walkers' median dL reaches 53%, their E wobbles 58%), and the quiet/churned
boundary is pattern-locked **in the bar's own envelope**: sustained churn switches on
between eps_eff = eps·A(r_corotation) ≈ 0.008 (0–0.5% of a disc churns) and ≈ 0.025
(35–40% churns), with the sustained band [CR−0.6, OLR+0.1] on an extended bar and
shrinking to nothing on a bar whose envelope dies before corotation — while a 60-period
census is unreliable in **both directions** (it under-reads P1 by 2.5x and over-reads the
localized-bar disc by 9%→0%).

## Bottleneck

Same as the original run (board: "fitting 10^9 in 8 GB" / cost-at-a-billion at galaxy
scale). The blocker to adopting the galaxy doll was that its regime size was known only
from 60-period windows with a slope t-stat — an instrument the checker showed reads low on
P1 and nobody had tested anywhere else. This run replaces the instrument and measures the
regime census on two potentials, two bar envelopes, four strengths, windows 60→600.

## Evidence

Everything regenerates from shipped code in this folder (Linux x86, 8 vCPU shared, orders
of magnitude only):
- `python3 probe2.py <job>` regenerates every census JSON (11 populations, 209 orbits
  each, nfail=0 everywhere; long jobs ~10–13 min each, shorts ~1–2 min; DOP853 rtol 1e-10
  truth, same as the original).
- Disclosure: `probe2.py`'s physics/classifier code was frozen at 01:47, before any data;
  a 02:06 edit (after the first eight populations) only added the two control *job
  configs* (`p1e001-long`, `p2e10-long`) — no analysis code changed after data existed.
- `python3 analyze.py` (<1 s) reprints every number below from the stored JSONs
  (`data/analysis.txt` is the saved output).
- `data/probe-orig.json` is a byte-copy of the original run's record
  (`git show origin/claude/lab-20261012-0036-scout-aac1:lab/results/20261012-0036-scout-aac1/data/probe.json`).

**Census vs window** (angle classifier: beat-angle confinement R̄≥0.5 ⇒ trapped librator;
net drift dL>5% ⇒ walker; else quiet; windows are prefixes of one 600-period integration):

- P1 (original potential/bar), eps=0.03: walk 25.8→28.2→31.1→34.9→34.9% over W=60→600;
  median walker dL 13.7→53.0% (true migration); librators constant 5.3%, parked exactly at
  corotation (all k*=0, dL≤0.7%); quiet-orbit E stays bounded (99.2% within 3x wobble,
  median net dE *shrinks* 0.36%→0.09%). Walker bins at 600p: 5/15/26/53% in
  [0,1.8)/[1.8,2.3)/[2.3,2.8)/[2.8,4.2) — 94% at Rg≥2.3; sustained band [1.57, 3.80] =
  [CR−0.60, OLR+0.06]. The 60-period census (tstat: 14%) under-reads by 2.5x.
- P2 (centrally concentrated potential, held out) + A2 (localized bar, held out), eps=0.03
  (eps_eff=0.007): the 60-period "walkers" (9.1%, dL up to 47%) **all resolve as bounded
  L-oscillators**: 0.0% walk at 600 periods, 5.3% librators. They sit at Rg≈0.96 where the
  bar envelope peaks (A2(0.96)=0.92). The 60-period census over-reads by 9 points.
- P1 eps=0.10 (eps_eff=0.083): whole disc churns (66.5% at 600p, band censored at the
  sampled edge), librators destroyed (1.4%). Quiet-orbit E still bounded (100%).

**The design number** — sustained churn (600p) vs eps_eff = eps·A(r_CR):

| eps_eff | cell | walk600 | lib600 | sustained band |
|---|---|---|---|---|
| 0.0074 | P2 e0.03 | 0.000 | 0.053 | — |
| 0.0082 | P1 e0.01 | 0.005 | 0.033 | [1.97,1.97] |
| 0.0247 | P1 e0.03 | 0.349 | 0.053 | [1.57,3.80] |
| 0.0248 | P2 e0.10 | 0.268 | 0.062 | [0.96,2.58] |
| 0.0825 | P1 e0.10 | 0.665 | 0.014 | censored |

The switch-on is between 0.008 and 0.025, and it is the **effective** strength that
governs, not the labelled eps: P2 at eps=0.10 churns like P1 at eps=0.03 (26.8% vs 34.9%
sustained, both eps_eff≈0.025) despite a 3.3x stronger bar, and the band's radial extent
follows A(r): P1's A1 stays 0.82–0.93 from corotation to OLR and the band spans
[CR−0.6, OLR+0.1]; A2 dies as exp(−r²) and P2's sustained band is cut at [0.96, 2.58]
(A2(2.6)=0.12), never reaching its own OLR at 3.93. At eps=0.10 on P2 the walkers' median
dL keeps growing with window (0.18→0.31, W=60→600): sustained migration, same error type
as P1's.

**Corrections to the original record** (recomputed from `data/probe-orig.json`,
analyze.py Part A): (a) main walker bins 8/42/51% in [1.8,2.3)/[2.3,2.8)/[2.8,4.2), not
42% in [1.8,2.3); (b) H2's churned band is [1.8,2.8) (75% of walkers), not [1.3,2.3];
(c) the m=2 OLR of P1 at Ωp=0.5 solves Ωp−Ω=κ/2 at **R=3.744** (formula printed by
`resonance_radii`; neither the dossier's 3.57
nor the checker's 3.37); (d) eval-on-read is **384×** cheaper than stepping one period
(23038× vs a whole 60-period block; compile is 687× the block); (e) nfail=19 was exactly
the de=0 circular rows — the double root defeats the sign-change bracket; the closed form
(κ²=Φ''+3L²/r⁴) now compiles all 19 circular rows per population with nfail=0 (W5).

## Predictions

`predictions.md` written 01:41:57, before any census data (file times prove ordering; the
original run's process defect is fixed). W1, W2, W5, W6 held; W3 failed and the failure is
the mechanism (band tracks eps·A(r), not corotation alone); W4 untestable as written
(censored width), with the sub-threshold growth super-linear (x4.6 for x3 in eps).

## What would make it wrong, cost of adoption, fit

Wrong if: longer windows (6000 periods) re-absorb the P1 walkers as ultra-wide librators
(median dL 53% and growing with W makes this unlikely), or the eps_eff threshold moves
between potentials by much more than the factor-3 bracket measured here (the ladder has five cells but two potentials, whose κ/Ω ratios differ, so the threshold is
not yet separated from the resonance-density change). Adoption: the
galaxy doll's edge rule — compile everywhere, put doll edges where eps·A(r) evaluated at
the pattern-locked resonances crosses ~0.01–0.02, own (E,L) re-anchoring inside the band —
is now a measured number with controls on both sides, but it needs one more potential
between the bracket before it is frozen. Cost: none this run (floats, nothing canonical;
no integer decided anything). PRINCIPLES fit: 3 (compute only surprises — the census is the
surprise-rate measurement that sizes the re-anchor tier), 33 (a body resolves only the
influences significant at its own scale — eps·A(r) is that significance, measured), 10
(simplest falsifying test first: the transient-vs-sustained split needed only prefix cuts
of one integration).

## The lens

The second-author lens inherits the scout's limits: floats only, one bar pattern family
(m=2, rigid, smooth envelope), 2D; the census says nothing about 3D Stäckel fudges, and
the classifier thresholds (R̄=0.5, dL=5%) are instrument parameters — the librarian class
is a distinct high-R̄ tail (p90 R̄=0.38, p95=0.60 at 60p on P1), so the 5.3% count is
threshold-stable, but the walker/quiet boundary at dL=5% could be re-cut at 2% or 10%
(the P2 transients swing 6–47% at 60p and <5% at 600p, so the qualitative result is
threshold-robust). What it may have missed: whether the P2 oscillators' large bounded L
swings (tens of %) still force re-anchoring at their oscillation period even without net
drift — the census bins them quiet, but a doll reading (E,L) stored at epoch 0 would be
wrong by the swing amplitude; that is a re-anchor-cadence question, not a regime question.
