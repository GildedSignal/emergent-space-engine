# Dossier — 20261010-0541-second-20261010-0448-redteam-f771-9999 (lens: second author)

## Claim

The gold experiment is done: the re-frozen, widened r1 (r1w) runs end-to-end
from the shipped scripts and the original claim holds at rung level —
**binet-m16 is killed by the widened envelope on two criteria (period 0.9766,
precession 0.9883) while binet-m32 passes every frozen r1 criterion**, with the
per-e period-band decision now measured (per-seed 0.1% is unreachable in the
512-crossing budget for e above e*(r_p) ≈ 0.95@7M → 0.99@30M, so the honest
banding keeps 0.1% as the fraction criterion and records the m⁻² bias as
calibratable) — plus three implementation invariants the re-freeze must carry
(dyadic absorb-edge collision, amplitude-scaled event landing, in-band
extremum-to-extremum events), each of which broke the shipped probe's own code
at the widened domain.

## Bottleneck

Bottleneck 0 (the representation), continuing the shipped run. Gain: replaces
the DISPUTED r1 with a passable, honestly-banded re-freeze ([r1w-rings.md](r1w-rings.md),
draft) and kills binet-m16 outright; prevents qualifying the law on an envelope
that hides two failure axes. No speed gain.

## Evidence

Machine: Linux 6.8.0-111-generic, 8 vCPU, load 1.1–1.9, single process, 38 MB
resident. Commands (each < 60 s; from this folder):

```
python3 binet_probe.py    # 2.8 s: shipped record regenerates bit-for-bit (repro-output.txt)
python3 r1w_run.py        # 44 s: the decisive run -> r1w-output.txt, metrics.json
python3 controls.py       # < 1 s: quadrature/repeat/law controls (controls.txt)
sha256sum metrics.json && python3 r1w_run.py >/dev/null && sha256sum metrics.json   # identical
```

- **Record regeneration:** `binet_probe.py` output matches the shipped
  `probe-output.txt` line for line (host line only). My event machinery ties
  to the shipped candidate bit-for-bit: banded (7,0.99) m16 gives prec 4.45e-4
  / period 1.93e-2 / 246 crossings (the shipped row), the (8,0.95) 40-cycle
  repeat deviation is 1.17e-11 (the shipped P5 number), and my vectorized
  oracle ties to the shipped scalar oracle with Δφ diff exactly 0 (its period
  differs 1.3e-8 by the shipped code's final-step trapezoid offset, reproduced
  and explained; five orders below every band at stake).
- **binet-m16 KILLED, two criteria** (256 seeds, Random(20261010), p log-U
  [10,1000], e log-U [0.01,0.99], gate p ≥ 6.5+2e, 0 rejects): period fraction
  0.9766 < 0.99 (6 fails; worst 3.35e-3 at r_p=15.7, e=0.0106) and precession
  fraction 0.9883 < 0.99 (3 fails; worst 1.54e-2, all on the low-e axis) —
  stronger than the checker's kill (period only, 0.967 at 128 seeds): the
  checker's second hole breaks m16 precession too.
- **Low-e strong-field grid (the second hole, explicit):** m16 fails 6/6 points
  (1.28–3.72e-3); m32 passes 6/6, worst 9.94e-4 marginal at (10.9, 0.01); m64
  passes with ≥ 9× margin.
- **binet-m32 passes every r1 criterion:** prec 1.0 (worst 1.62e-3), prog 1.0,
  period 1.0 (worst 5.97e-4), defl 1.0 over 64 light seeds (worst 6.69e-5;
  swept to r=10⁸ + each side's own exact tail; oracle checks 4/b and the
  Darwin excess in the output), capture 0/10 wrong (massive + photon, both m),
  isco correct, shape 1.0, repeat 1.0 (frozen reading, max first-cycle dev
  6.84e-16), crossings median 18 (worst 312). binet-m64 also passes but costs
  worst-case 624 crossings/cycle — per-seed above the 512 budget — so m32 is
  the unique m meeting physics and cost.
- **m⁻² law:** period slopes −1.97 to −2.02 (ratios 3.89–4.07) on all fixed
  cases; precession slopes −1.96 to −2.16; the low-e axis converges faster
  (−2.7 to −3.7). The bias lives in the band ODE, exactly as the checker
  measured.
- **Per-e boundary at m32:** e* = 0.95 (r_p 7–8), 0.97 (10), 0.98 (15), 0.99
  (≥30). Per-seed 0.1% at (7, 0.99) needs m ≈ 70 ⇒ ~1100 crossings/cycle:
  outside the budget by 2×. Expected 0.1%-band failures under the sampler
  ≈ 0.5 of 256 (Fermi over the e* table) against 2.56 allowed — m32's pass is
  robust, not draw-luck (this draw had e_max = 0.9344, zero per-seed fails,
  which is the expected outcome, not luck).
- **Hyperbolic periapsis bands (r_p < 6 M), first measurement:** all 7 grid
  points stay bound at m32 through the hyperbolic branch (crossings up to
  490/cycle at e = 0.99 — inside the budget); period errors 1.3e-3–1.0e-2
  (worst at the gate corner r_p = 4.31, e = 0.99), precession ≤ 2.5e-4.
- **Wall beyond 0.99 (m32):** bound but period error 9.6e-3 (e=0.995),
  4.9e-2 (0.999), 7.7e-1 (0.9999) — the checker's e=0.9999 misclassification
  (their m16 run) does not reproduce at m32 in this implementation; the wall
  shows as error size, and the domain cap at 0.99 stands.

## Predictions

[predictions.md](predictions.md) written before the decisive run. Score: 7 of
10 held. P1 (m16 period kill, 0.94–0.99) ✓ 0.9766; P2 (m32 passes, fails only
e ≥ 0.97 & r_p ≤ 8 per-seed) ✓; P3 (low-e: m16 ≥ 4/6 fail, m32 worst marginal)
✓ 6/6 and 9.94e-4; P4 (m⁻² slopes in [−2.10,−1.90]) ✓; P5 (hyperbolic bands
stay bound, errors continue the law) ✓; P8 (deflection 1.0, worst < 1.5e-3) ✓
6.7e-5; P10 (e* ≈ 0.93–0.97 at 7M rising to 0.99) ✓ 0.95→0.99. Misses, held:
P6 — e=0.9999 stays bound at m32 (error 77%), the misclassification I predicted
does not occur at m32; P7 — photon capture passes, but only after I fixed my
own amplitude-scaled-landing bug (my first full run misclassified all four
near-critical photon cases; disclosed below); P9 — r1's frozen repeat text
passes as written (dev 6.8e-16 ≪ 1e-12); the unpassability I predicted was
wrong, an artifact of generalizing the shipped (8,0.95) 1.17e-11 case.

## What would make it wrong

The decisive run is a Python float64 port of the rung, not the shipped Rust
harness; the integrator's clean re-run could differ where my port needed the
three invariants (the Rust r1 may already have them — H0205's defl and capture
passes suggest it does, which would confirm the invariants rather than
contradict the result). My sampler draw (Random(20261010)) had e_max 0.9344,
so the fraction criteria never stressed the top corner directly; the grid
fills that gap, and the Fermi argument covers the fraction, but a different
draw could show 1–2 per-seed period fails at m32 (still passing 0.99). The
e* boundary is gridded at 7 discrete e values per r_p; interpolation error
~one grid step. Disclosure: two bugs were found and fixed *in my own code*
during the run (both recorded in the output trail): the dyadic absorb-edge
collision and the u-proportional landing nudge; the first full run's photon
"misclassification" and 57% deflection errors were those bugs, not physics —
the final record carries the fixes, and the shipped-tie-outs were re-verified
bit-identical after them.

## Cost of adoption

One rung file: re-freeze r1 as r1w ([r1w-rings.md](r1w-rings.md) — sampler
line, low-e grid cases, three implementation invariants, repeat anchoring;
thresholds untouched). binet-m16/m8 die at the widened envelope; binet-m32
becomes the surviving configuration. The integrator decides the per-e band
question with the measured e* table; my argued default is fraction-0.1% +
calibratable bias, domain capped at e ≤ 0.99. Nothing else in the tree moves.

## Fit with PRINCIPLES

- "A failed experiment kills that configuration, never the method" (9): the
  widened envelope kills binet-m16, not Binet cells — m32 passes everything.
- "Errors never compound" (13): the surviving error is a fixed bias per (E, L),
  retrace-verified (repeat 1.0 at 6.8e-16), scaling m⁻².
- "Measure before claiming" (10) and controls on both sides: the m16 kill has
  passing controls at m32/m64 on identical machinery; quadrature and oracle
  sensitivities are 3+ orders below every decided band.
- "navigation, knowledge and dynamics those need to be perfect" (30): the
  decided quantity is arrival-time (period) accuracy in the regime the player
  flies (eccentric transfers, slingshots); the dossier prices the residual
  bias at the top corner instead of hiding it.
- "Gates are frozen before the first run and never weakened" (repo rules):
  every threshold is r1's frozen number, applied unchanged; only the seed
  envelope widened (the fix the original run proposed and the checker
  endorsed).

## The lens

The second-author lens trusts the checker's named experiment and could have
inherited their blind spots: I initially "confirmed" a photon-capture hole that
was my own float bug — the discipline that saved it was refusing to accept a
57%-off deflection that contradicted the shipped record. What this lens may
still miss: the river/square/tiltonly configurations were not re-run (out of
the re-freeze's scope, unchanged cases); the m⁻² extrapolation to m=70 for the
budget argument is a law, not a measurement at m=70; and the visibility of a
0.5% arrival bias at e = 0.99 near 7M is argued, not played.
