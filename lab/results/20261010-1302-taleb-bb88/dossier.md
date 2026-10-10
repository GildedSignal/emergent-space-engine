# Dossier — run 20261010-1302-taleb-bb88 (lens: Taleb)

## Claim

The gold's phase-neighbour certificate number ("every real encounter lies within partner
rank 4 along the orbit", `20261006-0346-taleb-09b5`) is a circular-orbit property: on an
eccentric orbit the encounter density and the partner rank breathe with the local Kepler
speed, both scaling as √((1+e)/(1−e)) at aphelion (measured exact on counts at every e);
a fixed rank-4 window drops roughly a third to a half of real contacts at e = 0.9 and a
k sized for aphelion overpays (1+e)/(1−e) ≈ 19× at perihelion. The fix is one line of
representation: key neighbours by apsis-passage time (a v(M)-modulated mean-anomaly
window, w = R_enc·n_orb/v(M)), which makes the window uniform and keeps cost ∝ real
contacts; the certificate's trigger must include the bunching factor √((1+e)/(1−e)).

## Bottleneck

Board's top scaling risk (5 October): candidate work must track real encounters. The
co-orbital (phase-neighbour) certificate is the adopted answer to concentrated workloads
and is in this week's build queue (HANDOFF "Headed next" #5). This run bounds its domain
before it is wired: eccentric fleets (any transfer/Hohmann leg, e ≥ 0.6) are legal,
common, and exactly where the fixed rank breaks. No 10× cost move; a premise fix in an
adopted design before the one-way door, in the spirit of "shows that a premise is wrong".

## Evidence

All numbers from `probe.py` (numpy + scipy cKDTree, this folder); full data in
`probe_out.json`, table in `summary.txt`. Truth: fleets of n = 3000 coplanar bodies on
one orbit (a ≈ 1 AU, spreads 10⁻⁶ in a, e, ϖ, mean anomalies uniform), all pairs ever
within R_enc over T found by KD-tree per sampled epoch; partner rank = circular rank in
mean-anomaly order. Reproduce: `python3 probe.py probe_out.json` (≈ 175 s, < 200 MB).
Machine: 8 vCPU Linux, load 0.94, 9 GB free (state recorded in run log).

**Family A (tight fleet, standing-contact regime, R_enc = 3e-3 AU, T = 2P, 3 seeds):**

| e | enc/body measured | enc/body = 2.87·√((1+e)/(1−e)) | max rank | p999 rank |
|---|---|---|---|---|
| 0.0 | 2.87 | 2.87 | 7 | 6.0 |
| 0.3 | 3.92 | 3.91 | 8 | 7.0 |
| 0.6 | 5.73 | 5.74 | 9–11 | 8.0 |
| 0.77 | 7.90 | 7.96 | 11–13 | 10.0 |
| 0.9 | 12.48 | 12.51 | 15–16 | 13.0 |
| 0.95 (held out) | 17.91 | 17.87 | 19–21 | 17–18 |

The count scaling is exact to <1% at every e — it is geometry: partners within R_enc at
aphelion number 2·R_enc·(local linear density), and a fleet uniform in mean anomaly has
arc density ∝ 1/v(M). Mechanism check: the circular per-body count 2.87 = 2R_enc/(arc
spacing) and the e = 0.9 count 12.48 = 2R_enc/(v_apo spacing), i.e. contacts live at the
aphelion clump. A rank-4 window at e = 0.9 keeps partners within 4 of ~6.25 mean-reach
per side: it drops on the order of a third of real contacts (the gold killed the window
tier at 4–6% dropped).

**Held-out (predicted in predictions.md before the run):** H1 R_enc doubled at e = 0.9 →
enc/body exactly ×2 (24.9), max rank 23–26 (predicted ×2 on the mean; the max scales
softer, see below); H2 n doubled circular → enc/body exactly ×2 (5.72), max rank 10–11;
H3 e = 0.95 → max rank 19–21 (predicted 18–20). Negative control: e = 0.9, R_enc = 0.02
→ max rank 59–63, enc/body 83.5 (the instrument detects the failure mode).

**Family B (the gold's own drift regime; spreads 10⁻⁴, R_enc = 1.5e-4 AU, T = 10P):**
max rank 12–15 at e = 0, 12–15 at e = 0.6, 15–17 at e = 0.9 — the drift regime is
e-robust, as predicted: synodic drift acts in mean anomaly, which is e-independent. So
the two mechanisms superpose: rank ≈ Poisson-max of 2·(standing reach √((1+e)/(1−e)) +
drift reach), drift reach = (3/2)·(δa/a)·(T_reeval/P)·n spacings.

**Two fat tails on top of the e-law** (the lens's point, and a caveat for the build):
(i) mean-anomaly spacings of a uniform fleet are Poisson — the worst clump runs 2–5× the
mean reach (circular max rank 7 at mean reach 1.4 spacings; the *mean* cost lies);
(ii) rank is ∝ n·R_enc at fixed e (H2), so "rank 4" is a scene property, not a law — at
a 10⁶-body fleet with the same R_enc/spacing the Poisson max reaches ~10 even circular.

Controls: K-doubling (240→480, 2000→4000 epochs) changes pair counts by ≤ 0.01%
(sampling adequate; proximity episodes last far longer than the step). Family B circular
reproduces the gold's order (single-digit-to-low-teens rank at its drift parameters).

## Predictions

`predictions.md` was written before the sweep. Held: P1 (circular ≈ gold, max 7),
P2 (rank grows with e; crossing 4 near e ≈ 0.6–0.77 at this density), P4 (drift-regime
rank 12–15, the gold's order), P5 (drift regime e-flat), H1–H3, negative control.
**Falsified and reported: P3** — I predicted encounters per body roughly e-independent;
in the standing regime they grow as √((1+e)/(1−e)) exactly (the clump multiplies count,
not just partner identity). The corrected statement is in the table above.

## What would make it wrong

My truth is sampled-in-time, not analytic per-pair minima; it could over- or
under-count contacts (K-doubling bounds this at 0.01%). Rank is measured in mean-anomaly
order at t = 0; if the implemented certificate re-windows continuously or keys by arc
length, its effective rank differs from my t₀ order by at most the drift reach (family A:
3·10⁻⁶ spacings — nil; family B: the quantity measured). The gold's exact fleet scene
(density, R_enc, spreads) is not in my hands, so "rank 4" may have been measured at a
density where the circular Poisson max was 4 — that is consistent with, not contrary to,
the claim: the number is a scene property that scales as measured. The fix (apsis-time
keying) is argued, not measured in code; the next run could implement it against this
harness as the falsifying test.

## Cost of adoption

Near zero: the certificate is not wired yet (this week's build). Replace fixed k with
k(M) = ⌈2·R_enc·n_orb/(v(M)·ΔM_spacing)⌉ (equivalently, sort by apsis-passage time and
use a uniform window R_enc/v_apo), gate its trigger on the bunching number
√((1+e)/(1−e)), and size the window by the Poisson clump tail, not the mean.

## Fit with PRINCIPLES

- "A fix signals the wrong representation" (#19): fixed k in mean anomaly is the wrong
  coordinate; apsis time is the one where the window is uniform.
- "Symmetry is found, not given" (#32): the symmetry is Kepler's second law — arc
  density ∝ 1/v; the certificate should borrow it instead of paying a per-body constant.
- "Fat tails … judge the worst cases, not averages" (lens): the Poisson clump and the
  aphelion pile-up are exactly the concave spots; sizing by the mean misses both.
- "Gates judge a representation; they never size it" (AGENTS): rank 4 was a measurement
  promoted to a constant; the law behind it is now measured.

## The lens

Taleb made me attack the freshly adopted gold rather than build, and the Fermi estimates
killed two louder ideas first (e-fat tails breaking the Binet cone's tracking: both cone
width and encounter cross-section grow ~e at fixed density, ratio constant — which is
q-candidate-degree's own finding; and a drift-mechanism e-break: mean-anomaly dynamics
is e-independent). What the lens may have missed: speed. Nothing here makes the engine
faster; it prevents a silent correctness break in a component about to be built. The
sampling truth is cheap but not exact per-pair; a checker with the encounters crate
could redo the truth with its own continued-fraction conjunction machinery.
