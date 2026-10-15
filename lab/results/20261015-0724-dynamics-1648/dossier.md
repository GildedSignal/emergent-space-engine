# Dossier — run 20261015-0724-dynamics-1648 (dynamics lens)

## Claim

The skip gate is innocent in a cold dense gas — it fires only on the grazing shell (0.1%
of detected contacts at fleet closing speeds, 2.7% at a third of reach per chronon, half
the transport only once |w| ≫ reach), the equipartition attractor and relaxation rate are
unchanged within noise, ghosted pairs never re-encounter at fleet speeds — and the page's
proposed fix rule ("resolve at τ\* = −d·w/|w|²; the v1 reflection needs no root") is
**provably and measurably a no-op**: at the closest-approach normal the reflection is the
identity for every pair, so a real fix must pay the contact root |d| = reach.

## Bottleneck

Not a board wall: this is the `contact-speed` law-correctness question, open directions 1
and 2 (written hours before this run). What it deletes: any impulse to build the fix for
slow-fleet dynamics (the dropped channel carries 10⁻⁴–10⁻² of transport there), and the
page's no-root fix design (dead as worded). What it prices: the exact regime where the
skip bites (|w| comparable to reach), the fence the integrator needs before wiring fleet
contacts. Gain: a wrong fix deleted before it was built; the danger fenced with measured
rates instead of a scene reading.

## Evidence

All numbers from `regen.sh` (7.4 min single-threaded; `cargo run --release -p
emergent-lattice --example skipgas`, then `python3 analyze.py work/results.jsonl`).
Scenes: Q = 2²⁰, box 2¹⁸ quanta, r = 1024 (reach 2048), N = 200 (h1: 300, seed 13),
masses 1 (hot, v_th) and 64 (cold, v_th/16), T_A/T_B = 4 at birth. Arms: `shipped`
(CPU Chronon, `Law::RelativisticV1`) vs three f64 twins of the same rule — `skip` (exact
mirror, exchange at bin end when approaching, receding pairs ghost), `contact`
(skip-class pairs resolved at the true contact root |d| = reach), `cross` (skip-class
pairs exchanged at the bin-end separation), `tau` (8144's rule as worded: reflect at the
closest-approach normal). The skip's distortion is `contact` − `skip` (float vs float);
`shipped` vs `skip` re-tests f50d's quantization innocence in this scene class.

**Instrument controls (both sides).** c1 (v_th = 8, no contact can skip): the four twins
are bit-identical (900 contacts, equal end temperatures) — the float instrument is exact
where the rule has one path. c2 (v_th = 4000): shipped 90,263 contacts vs twins
89,870–90,021 (0.4%); skip fraction 49.7% vs 51.1–51.9%; the τ\* ≤ 1 classifier agrees
with observed revisions 88,391/90,263; energy ledger exact; and the skip drops 48% of
total momentum transport — the gross distortion a working instrument must see. Shipped
digest rerun determinism: single process, LCG genesis, no wall-clock input.

**In-situ rate law (the closed form holds in a gas, not just driven pairs).** Per-ρ skip
rates, shipped engine, d2 (v_th = 700; d1/h1/c2 within ±0.05 of the same table):
ρ≈0.15 → 0.79, ρ≈0.4 → 0.59, ρ≈0.6 → 0.40, ρ≈0.85 → 0.14, ρ > 1 → 0, against 8144's
max(0, 1−ρ) = 0.85/0.60/0.40/0.15/0 (the residual gap is Jensen curvature over the bin,
not a bias). The twins reproduce the same table.

**The skip's fleet-scale price (the decisive scenes).**

| scene | v_th (quanta/chronon) | skip fraction | dropped transport / total | t_half skip/contact | re-encounters after skip vs exchange |
|---|---|---|---|---|---|
| d1 | 150 (fleet-like) | 0.1% | 0.01% | 1.19 | 34 vs 29,792 |
| d2 | 700 (0.34 reach) | 2.7% | 1.1% | 1.00 | 2,498 vs 86,362 |
| h1 (held-out, seed 13, N=300) | 400 | 0.9–1.0% | 0.21% | 1.13 | 1,575 vs 145,449 |
| c2 (control) | 4000 (≫ reach) | 50–52% | 48% | (noise) | 38.5k vs 33.7k |

Every arm of every scene reaches equipartition (end class temperatures within finite-N
fluctuation, ~14% per class); arm-to-arm t_half spread inside a scene (e.g. d1: 7,000 /
9,500 / 8,000 / 7,000 / 11,500 across shipped/skip/contact/cross/tau at 500-bin sampling)
shows the relaxation differences are chaos noise, not a systematic channel: the dropped
channel is 10⁻⁴–10⁻² of transport at |w| ≤ reach/3, and relaxation follows transport.
Fano of contacts per active bin: 0.05 (d1) to 0.85 (c2) — no avalanche signature; a skip
never triggers a cascade at fleet speeds (34 re-encounters total in d1 against 30k after
exchanges). Shipped energy ledger exact in all five scenes (`ledger_ok = true`: ΣE(end) −
ΣE(genesis) = Σresidual, bit for bit).

**The no-op (8144's open direction 1 as worded).** In the pair's COM frame the law's
normal N = (d·P_s, E_tot·d) is purely spatial (P_s = 0), so the reflection flips each
momentum's component along d(τ\*); at closest approach d(τ\*) ⊥ w, and in the COM frame
both momenta lie along w — the flipped component is zero for both bodies, any masses:
the reflection is the identity. Measured: the `tau` arm pays 0.30% (c2), 0.01% (d2),
0.01% (h1) of total transport on skip-class contacts against 48%/1.1%/0.2% for the
contact-root arm — the residue is the contaminated multi-pair path (1,343–1,487 bins at
c2), not the rule. A real fix needs the contact root |d| = reach, whose direction carries
depth/|w| = ρ under a square root — irrational in general; "the v1 reflection needs no
root" is false at the only rational geometry. The cheap `cross` variant (bin-end
exchange, the one-line change) pays 0.5× the contact-root impulse on grazes at slow
speeds (0.51% vs 1.09% at d2) — right order, wrong geometry, and at fleet speeds both
are negligibly small.

**Quantization (f50d extended, and its floor).** At |k| ≥ 150 quanta (d1/d2/h1) the
shipped engine tracks the float mirror in every ensemble statistic (contacts within 4%,
skip fraction equal to the third digit, end temperatures within fluctuation) — f50d's
innocence extends to cold dense two-temperature gases. At crawl speeds (c1, |k| ~ 8
quanta) shipped and twins genuinely diverge (826 vs 900 contacts, visibly faster
equilibration): per-body velocity quantization is first-order there. Domain note, not a
channel of this run's question.

## Predictions

`predictions.md` was written after the controls (c1/c2) and before d1/d2/h1 ran; the
no-op was found during control validation, then proven, then made a measured arm. Held:
the relaxation bounds (d1 t_half within noise of contact, h1 ratio 1.13 ∈ [0.85, 1.15]),
the tau no-op (< 10⁻³ of contact's dropped transport: measured ≤ 3×10⁻³ of *total*),
shipped-vs-twin agreement at |k| ≥ 150. Missed, both in the same direction: the skip
*fraction* bands were 3–10× high (d1 predicted 0.3–4%, measured 0.1%; d2 predicted
15–35%, measured 2.7%; h1 predicted 5–15%, measured 0.9%) — cause understood after the
fact: the grazing shell is the annulus b ∈ [√(reach²−|w|²), reach], an area fraction ≈
(|w|/reach)²/2, and the detected-contact b-distribution further concentrates away from
grazing; the transport-fraction predictions were the load-bearing ones and held.

## What would make it wrong

The twins are sequential-batch mirrors, not sub-bin interleavings: multi-pair bins are
approximated (contaminated path: 1–1,487 bins per scene, ≤ 1.6% of skip-class contacts,
measured and reported). If a real fleet shows skip-class contacts clustering in bins
(density ≫ these scenes' 1–2% filling), the contamination grows and the float-vs-float
isolation weakens — the shipped-vs-twin check is the canary (it held at every speed
above the quantization floor). The relaxation readout is finite-N (±14%/class
fluctuation): a channel smaller than ~10% of transport cannot be resolved by these
scenes, so "innocent" means "below 10⁻² of transport with relaxation indistinguishable",
not "zero". Cost of adoption: nothing to build — the adoption is a *decision* (do not
fix the skip for slow-fleet dynamics; if ever fixed at speed, pay the contact root or
accept cross's 2× under-impulse). Fit: "Compute only surprises" and "Behaviours matter,
not continuum fidelity: error type over error size" — the skip's error type at fleet
speed is a bounded deletion of the smallest impulses, measured; at |w| ~ reach it becomes
a law change (half the transport), and that fence is now a number, not a scene reading.

## The lens

The dynamics lens measured the attractor (equipartition), the transport channel, and the
cascade question (re-encounter rates, Fano) — and the no-op came from refusing to
implement the proposed fix without checking its geometry. What it may have missed: a
*bound-state* channel (the two-body pump of f50d, where 55–62% skip inside a bound pair
— my gases are unbound boxes, so the skip's effect on a trapped orbit's dwell is not
re-measured here); and the game-scale *rate* in a flown fleet (members share the frame
velocity, so the closing-speed distribution is set by manoeuvres, not temperature — open
direction 3 stands).
