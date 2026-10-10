# Dossier — the named experiment done: the kill survives the corrected clock; the record now regenerates

Run: 20261010-1920-second-…-3ea5, second author on 20261010-1816-system-67f2.
Host: GitHub Actions Linux, 8 vCPU, load 1.4, 2.0/15.9 GB used; pure Python,
~60 MB, 12 s for the whole record.

## Claim

Checker 2's named experiment is done — clock fixed (force at the body's own
time), quantize-and-carry added, both scenes rerun with Scene B at the **true**
2:1 — and the author's claim **holds on the clean record**: deferring a kick's
*application* into an exact accumulator walks energy secularly at every quantum
that saves renewals (exp 1.01–1.11; timing error, the forbidden type), while
rounding the *magnitude* to the same quantum with exact timing stays bounded
(quantcarry exp −0.01…0.44, error 28–46× lower at equal q) — so the renewal
quantum has one home, the derived-structure side, never the impulse side. What
does **not** survive the fix: the author's "discard stays bounded" surprise
(buggy 0.06 → corrected 0.73/0.63; it was the mistimed force) and the Scene B
sign-flip numbers (the scene was a 4:3, not a 2:1); what replaces them is
stronger — at the true 2:1 deferral scrambles the resonant phase (ψ windings
−5.9…+6.2 vs immediate's −0.1) and **ejects the body hyperbolic** (orbit 856,
pump 10.6).

## Bottleneck

Board focus 1 and 3 (renewals per orbit; steady-state work). This run closes
the silver→gold gap on a kill that deletes the cheapest-looking route to fewer
renewals (impulse deferral) before anyone builds it. Expected gain had it
held: renewals → |drift|/q; what it deletes instead: the whole impulse-deferral
patch class, now measured bug-free.

## Evidence

The bug, verified first from the author's own code (`deferral-orig.py`, kept
verbatim): clock/body ratio → 1.5000, lead = 119.2 Jovian revolutions per 1000
orbits. The corrected `deferral.py` (three changes, each documented in its
header; force law, WH split, exact drift, q ladder and mark cadence the
author's, unchanged) regenerates **bit-exact** (`cmp` clean, 12 s):
`python3 deferral.py deferral.json`.

Scene A, a=2, e=0.05, 1000 orbits, truth 1024/orbit (author's buggy numbers in
brackets):

| config | renew/orbit | max\|ΔE\| | exp |
|---|---|---|---|
| immediate | 64 | 3.22e-7 [8.2e-7] | 0.08 [0.07] |
| deferred q=8.6e-6 | 36.3 [36.4] | 1.33e-3 [1.3e-3] | **1.11** [1.01] |
| deferred q=3.5e-5 | 10.9 [10.9] | 8.52e-3 [8.8e-3] | **1.01** [0.98] |
| deferred q=1.4e-4 | 2.8 [2.9] | 5.62e-3 [6.5e-3] | 0.54 [1.01] |
| deferred q=5.5e-4 | 0.02 [0.04] | 6.03e-3 [6.4e-3] | **1.09** [1.07] |
| **quantcarry q=3.5e-5** | 64 | **1.86e-4** | **0.39** |
| discard q=3.5e-5 | 64 | 2.69e-3 | **0.73** [0.06 — the artifact retracts] |

At e=0.3 (new): deferred exp 0.96 vs quantcarry **−0.01** (flat) at equal q.
Scene B, the **true 2:1** (a=3.2758, e=0.02, truth 512, e_max(truth)=0.1009 =
immediate@64's, so the pump baseline is honest): deferred pump 1.87 at the
mildest q (22.4 renewals/orbit) — checker 2's 1.87 reproduced; ψ windings
scrambled (−5.9…+6.2 vs −0.1); at q=32·dvr **ejection at orbit 856** (e=1.07,
pump 10.6); checker 2's ejection sat at 8·dvr — the edge is chaotic, the
ejection is robust. Quantcarry there: pump 1.08, bounded, but ψ −4.2 — even
bounded magnitude error becomes phase error at resonance (law.md's resonance
guard, standing). Probes: deferred q→1e-9/1e-7 give immediate's exact 3.22e-7;
quantcarry 1e-7 → 9.4e-7, exp 0.24; discard walks even at 1e-7 (0.66).

## Predictions (predictions.md, written before the decisive run)

Held: #2 (quantcarry bounded, 28–46× below deferred), #3 (discard retracts,
0.73 ≥ 0.6), #5 mostly, #1 and #4 in substance. Letter misses, reported: #1
exp 0.54 (not ≥ 0.85) at q=1.4e-4 — the error saturates early at a 5.6e-3
plateau (1.7×10⁴× immediate) instead of growing; #4's mid-ladder point
(q=8·dvr) distorts phase (ψ −5.9) rather than amplitude (pump 0.905, inside
the band) — non-monotonic in q, as checker 2 found; #5's quantcarry probe is
2.9× immediate, not 3 digits. The pre-registered kill criterion for the split
rule did **not** fire: no q with ≥ 2× renewal savings has exp ≤ 0.5, and
quantcarry never reaches 0.8.

## What would make it wrong, cost, fit

Wrong if a GR-native kick couples timing and magnitude differently (the replica
is Newtonian, one perturber, e ≤ 0.3), or if averaging in the law's own
variables (H0190, adopted, with its resonance guard) is already the legal
deferred form — the split rule says exactly that: defer in element/averaged
space where phase is carried by the generator, never raw impulses. Adoption
cost: zero code; it removes a patch class. Fit: principle 2 ("error type over
error size" — timing walks, magnitude dithers, now measured with the right
instrument), principle 9 (the configuration dies, the method lives), and
engine.md's "secular drift: forbidden" — on a record free of the clock bug.

## The lens

The second-author lens inherits checker 2's probe results, so its predictions
were not fully blind — the value added is the clean, shipped, regenerating
record and the two retractions stated as retractions (discard's boundedness,
Scene B's label), not new physics. What it may have missed: the ejection's q
is chaotic (8·dvr vs 32·dvr between two correct replicas) — do not quote it as
a threshold, only as an existence proof; and quantcarry's own ψ shift at the
resonance (−4.2 windings) suggests "bounded" means bounded in energy, not in
behaviour, at resonances — the selector stays load-bearing for any renewal
mechanism, including legal ones.
