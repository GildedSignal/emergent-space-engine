# Check — 20261019-2017-redteam-8c3e

Grade: lead

**Abstract (for the integrator).** Reproduced exactly (66/66 grid rows, all
headline numbers: 32/66 violating cells, 4.46e6/5.02e6 budget multiples,
78/78 unrepresentable crossings) — but the refutation is the kick-jet line's
gold record, uncited in the dossier: df81 (C·drift² unbounded), 4978
(separatrix 10³–10⁹× floor, plunge fabricated as bound), 6164/ee08 (far-field
outside a corner, r_apo 2000; freeze-ready guards: 9a04's tri-predicate,
ee08's root-distance certificate). Two of its own numbers fail: margin
"≥140×" is 1.11× at e=0.5/κ=0.25; "Δφ passes at 8-bit gap" fails to κ=0.05.
My probes break the licensed domain at both ends: e=0.02–0.05 violate at
κ=0.5; e=0.98 grows 3.0×/9.1× at κ=16/32, 1408× at e=0.999/κ=8. New: the
matched-(q,w) budget grid, the √q crossing band, the r12 draft. Adopting the
amendment as written imports a wrong license.

## 1. Reproduction

`regen.sh` (runner, exit 0) and my own clean-tree rerun in /tmp agree: the
66 per-cell rows, the licensed-domain block and the crossings block are
line-identical; smoke rel=1.00e-06; 32/66; worst 4.460e6 (Δt) / 5.023e6 (Δφ)
at e=0.1/κ=0.005; 78 crossings, all `taylor_finite`, all +E/−L; q² median
0.003730 (n=438). Instrument validated independently: quadrature vs DOP853
reproduces (e=0.5/κ=0.005 rel 1.4e-9 in the runner's log; e=0.9/κ=0.05
re-executed by me, digit-identical: 9.08e-11/1.18e-11/8.47e-12); smoke against
the exact circular closed form 1.002e-06; n=4096→65536 quadrature convergence
at the apoapsis-channel cells is 1.5e-10–1.8e-9 — two orders below the ~1.1e-6
relative remainders at issue, so the apoapsis finding is not a quadrature
artifact. `patch.diff` is empty as claimed; no repo file touched.

## 2. Predictions

`predictions.md` predates the final script (mtime 50 min vs 23 min) and is a
real pre-registration with a frozen kill criterion. Held: P2's crossing-band
half (√q: 2⁻¹⁶→κ≤0.05–0.1, 2⁻²⁰→≤0.01–0.02, 2⁻²⁴→≤0.005), P5 (crossings,
finite Taylor garbage). Failed and honestly reported: P1 magnitude, P3 (Δφ
worse, not better), P6 partial. Two overstatements: P2's *boundary* half is
untestable on this grid (κ* pinned at the 0.005 floor for every (q,w) in the
author's own summary), and the dossier's "the parents at κ ≤ 0.002 … for
e ≤ 0.3" is wrong — all 18 dropped rows (every e) sit below the resolver.

## 3. Adversarial cases (mine; three outside the tested range)

1. **Higher e (outside e ≤ 0.98):** e=0.995/κ=8 → 25.7 budget multiples;
   e=0.999/κ=8 → **1408×**; e=0.999/κ=2 → 404×. The far field is not
   "non-monotone, fails only at κ=8" — the apoapsis channel grows without
   bound in e.
2. **Next κ decade (outside κ ≤ 8):** e=0.98 fails 3.0× at κ=16 and 9.1× at
   κ=32. The violation grows past the grid edge; "passes for 0.1 ≤ κ ≤ 4,
   fails at κ = 8 (1.16×)" understates a monotone far-field failure.
3. **Lower e (outside e ≥ 0.1):** e=0.02 and e=0.05 **violate at κ=0.5**
   (2.84×, 2.30×) — inside the dossier's licensed domain "e ≤ 0.9, κ ≥ 0.5
   for e ≤ 0.3"; both pass only at κ ≥ 1. Instrument validated there
   (quad-vs-ODE 3.1e-8 at e=0.02/κ=0.5; smooth κ-monotone structure). The
   near-circular regime — the game's undisturbed-orbit archetype, not an
   exotic case — needs κ ≳ 1, so the claim sentence's licensed domain is
   falsified by the author's own budget semantics. (My e=0.001 rows show
   spurious crossings from the author's own disclosed float64 floor at
   e ≲ 1e-3; not counted.)
4. Boundary refinement between grid points: e=0.5 fails to κ≈0.23, e=0.9 to
   κ≈0.14 — the grid's band edges are right where resolved.

## 4. Numbers that fail against the author's own results.json

- **"margin ≥ 140× (worst passing remainder 0.007 at e=0.9, κ=8)":** the worst
  passing cell in the stated licensed domain is **e=0.5/κ=0.25 = 0.897 budget
  multiples → margin 1.11×**; e=0.9/κ=8 reads **0.0493 (20×)**, not 0.007.
  The 140× traces to e=0.7/κ=8 (6.4e-3 → 156×) — a selection slip on their
  own table. The error flatters the amendment ("licensed with ≥140× margin"
  appears in the claim, the adoption cost and the proposed page).
- **"Δφ passes everywhere at 8 bits of gap (q2⁻²⁴, w16)":** at that combo Δφ
  still violates up to κ=0.05 (3.53× at e=0.1; **9.6×10³×** at e=0.1/κ=0.005);
  Δt at the same combo also fails to κ=0.05. And **no 12-bit-gap cell exists
  in the run** — "Δt needs ≳ 12 bits finer storage" is an untested
  extrapolation whose direction contradicts the run's own budget arithmetic
  (budget_mult ∝ q²·2^w: *finer* storage makes the one-floor test harder).

## 5. Novelty (the decisive point)

The dossier claims "the accuracy half was never measured". The kick-jet page's
own Runs list holds the opposite, all in the record and much of it gold:
- df81 (gold, 6 Oct): "multiply-add error C·drift² unbounded; inspirals need
  Peters' generator; re-anchor rule proposed" — the same q² remainder scaling
  and the same inspiral argument.
- 4978 (gold, 6 Oct): "jet invalid near the Schwarzschild separatrix;
  10³–10⁹× the floor; **plunge fabricated as bound**" — same doll, same
  magnitude decade, and the same type error as "the player sees a ship orbit
  where it must fall in".
- 2040/9a04 (silver/gold, 8 Oct): "multiply-add fails by type at the
  separatrix"; "E-axis failure (15/8)(δE/(1−E))² … tri-predicate complete,
  freeze-ready" — the exact scaling behind the apoapsis channel, plus a
  freeze-ready guard.
- 6164/ee08 (silver/gold, 11 Oct): "the multiply-add is false **outside a
  corner**: 190× the floor at p 100, e 0.9; every kick recompiles at
  r_apo 2000"; "Kerr confirms at every spin … both-ends root-distance
  certificate" — the high-e far-field channel and a second freeze-ready
  certificate.

So the separatrix magnitude, the crossing type-failure, the high-e far-field
channel, the guard and even the "state the licensed domain" surgery were all
measured and adopted into the record before this run (kick-jet open 4 /
binet-cells open 4 — fe85's standing item — asks for a *rung*, not a first
measurement). What is genuinely new here: the budget-multiple restatement at
matched (q,w) on a 2-D (e, κ) grid, the √q crossing-band scaling, and the r12
draft criterion — increments, not a 10× bottleneck move, and the parts that
carry the amendment's weight (the domain's coordinates and margins) are the
parts that are wrong. Per the rubric ("already known or tried — cite the H
entry … a repetition is not gold, however well done") this is a lead.

## 6. The page

`wiki/representation-premises.md` carried all four errors ("first
measurement", "≥140×", "passes everywhere at 8 bits", the unbounded licensed
domain). Corrected in place: novelty now cites df81/4978/9a04/ee08; margins
read "down to 1.1×"; the domain is bounded to e ∈ [0.1, 0.9] with my low-e and
high-κ extensions noted; the gap lever is replaced by the guard (9a04/ee08
shape) and the "≥12-bit" clause flagged as unsupported; a Checker note added.

## 7. What the author missed

- The kick-jet Runs list — the one place the lab keeps exactly this history;
  the dossier cites kick-cadence's 99%-refit number from the same neighborhood
  but none of the four multiply-add kills.
- The low-e arm: near-circular orbits are the populous case, and they break
  the stated license at κ=0.5; a red-team that sweeps 0.1 ≤ e ≤ 0.98 has
  bracketed the boring middle and missed both edges that matter.
- Their own summary table: κ* = 0.005 for every (q, w) simultaneously refutes
  P2's boundary claim they report as held, and the per-(q,w) band table
  contradicts the "gap" lever they built on it.
- e=0.98's growth past κ=8 was one grid column away and the trend (0.65 → 1.16
  from κ=4→8) was visible in their own printout.

## 8. What survives (keep, don't redo)

The reproduction is solid and the instrument is sound; the r12 draft is the
first rung text for fe85's standing item and should be kept as a draft — but
its freeze should start from 9a04's tri-predicate/ee08's certificate rather
than re-deriving the guard, and its grid must add the e < 0.1 and κ > 8 arms
(this check's numbers may be reused: e=0.02/0.05@κ=0.5 fail; e=0.98@κ=16/32
fail; e=0.999@κ=8 fails 1408×).
