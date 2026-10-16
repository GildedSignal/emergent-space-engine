# Dossier: the binet cell's frequency belongs to the orbit, not the band

**Claim.** The in-cell Binet law's first-order near-circular error is deleted not by a better
band centre but by removing the centre from the dynamics: the cycle's frequency compiled from
its own two turning points (exact cubic + AGM, ~30 flops once per cycle) makes the advance
exact to 8×10⁻¹⁶ at every m (machine level, m-free), so m collapses from an accuracy dial
(m=32 for a clean pass) to a pure cost dial (m=2: 4 crossings/cycle, 19.5× fewer events) —
while the frozen band-centre law keeps a first-order e=0 family (fails the 0.1% period bar
to p≲35–60) and the page's literal refit (centre = (u_peri+u_apo)/2) trades that family for
a collapsed period (0.47 pass fraction) and an e/p advance error at the eccentric corner.

## Bottleneck

The lens's component: the cells' in-band law (representation.md §1, "Binet cells ... that is
a rotation"). The board's representation item 0/1 lineage; the wiki page
[binet-cells](../../wiki/binet-cells.md) open direction 2 ("the per-orbit u_k refit ...
deletes the first-order term by construction; needs one measured row to price") — this run
is that row. Requirement owner (PRINCIPLES #7): "Geodesics are as trivial as straight lines"
— a bound cycle is one rotation; its frequency is an invariant of the orbit, not of the
memory grid the orbit happens to sit in. Floor: the advance of a bound Schwarzschild cycle
is a closed function of its two turning points (Darwin's 4√(p/d)·K(4e/d)−2π, AGM ~30 flops),
so no exact in-cell law needs the band geometry for frequency at all; the bands' dynamical
jobs reduce to plunge/capture classification and the crossing/event structure. Idiot index
of the frozen law on the advance channel: it pays 78 crossings/cycle (m=32) and still holds
only 5.6×10⁻⁴ worst advance error; the compiled-frequency law pays 4 crossings (m=2) for
8×10⁻¹⁶ — the accuracy gap is 12 orders and the event cost ÷19.5 at strictly better behaviour.

## Evidence (float64, G=c=M=1, `work/binet_refit.py`, stdlib only; regen: `bash regen.sh`, ~100 s)

Oracle = Python ports of the shipped `xtask/src/gr_oracle.rs` (`periapsis_elliptic`) and
`gr_oracle_extended.rs` (`bound_constants`, `bound_period_quad`), validated in-run against an
independent RK4 of the exact Binet ODE u″=1/L²+3u²−u: advance agrees to 2×10⁻¹³, period to
8×10⁻¹⁵ (4 cases).

Frozen 256-seed sampler (r1's exact draw, `Random(20260930)`, p log-U[10,1000], e U[0,0.7],
p≥6.5+2e), advance error / period error, pass bars = r1's (1% / 0.1%):

| arm | prec pass | per pass | adv med | adv worst | per med | per worst | crossings med |
|---|---|---|---|---|---|---|---|
| frozen-m8 | 0.9961 | 0.9570 | 2.7e-5 | 1.3e-2 | 6.6e-5 | 1.2e-2 | 19 |
| frozen-m16 | 1.0000 | 0.9961 | 5.7e-6 | 4.8e-3 | 1.5e-5 | 4.7e-3 | 38 |
| frozen-m32 | 1.0000 | 1.0000 | 1.4e-6 | 5.6e-4 | 3.7e-6 | 5.5e-4 | 78 |
| mid-m16 ((u_peri+u_apo)/2) | 0.9961 | 0.4688 | 7.0e-6 | 1.1e-2 | 1.1e-3 | 6.8e-2 | — |
| invL-m16 (1/L²) | fails e=0 to p≳100–300 (6.1e-1 at p=6.5 → 1.0e-4 at p=300) | | | | | | |
| **agm-m2/m8/m16** | **1.0000** | 0.4570 | **1.4e-16** | **8.3e-16** | 1.1e-3 | 8.0e-2 | **4 / 18 / 38** |
- **Control vs the prior run (20261015-1450-redteam-fe85), no code shared:** period pass
  fractions match exactly (m8 0.9570, m16 0.9961 = 255/256); m8 precession 0.9961 vs their
  0.9844 (3 seeds); eccentric error second order in band width (median ÷4.7, ÷4.2 per
  m-doubling; their 1.83e-4 at m=16 vs my 5.7e-6 — same order family, different code); the
  e=0 worst-offset family fails the 0.1% bar to p≲35–60 (m16: fails {6.5,8,10,20,35}) and
  p≲30–35 (m32), matching their "p≲60 / p≲35" envelopes.
- **The literal refit (`mid`) kills the e=0 family** (worst 4.7e-16 across p=6.5…1000) but
  the eccentric corner pays ~(2e−0.92e²)/p (measured worst advance 1.1e-2, 1 seed over the
  bar — held-out p=8.5,e=0.9: **12.4%**, matching the pre-registered 0.95/p=11%) and the
  period (read through the rung's dt/dφ rule on the law's own shape) **collapses to 0.47
  pass** (worst 6.8e-2): the page's open direction 2 as worded is priced and fails.
- **The compiled-frequency law (`agm`)** — ω = 2π/Δφ_exact, Δφ_exact from the cycle's own
  turning points, themselves compiled from the conserved (E,L) by the exact cubic (closed
  form; reconstructed (p,e) match the labels, advance output 8×10⁻¹⁶ worst) — passes
  precession 256/256 at every m with **m-independent errors** (identical to 1 ulp at
  m=2/8/16): the dynamics no longer touches the bands. Held-out: p=8.5,e=0.9 (separatrix
  neighbour, margin 0.7): advance 9.3e-15 — the divergence as d→0 emerges; p=1000,e=0.69:
  2.8e-16; p=10,e=0.05: 1.8e-16. Crossings median 4 (m=2) vs frozen-m32's 78 for its clean
  pass: **19.5× fewer band-crossing events** at 12 orders better advance.
- **The period is the honest failure (pre-registered as the row's uncertainty, and the
  prediction FAILED):** I predicted median <1e-5, worst ≤3e-2; measured median 1.1e-3,
  worst 8.0e-2 (0.457 pass at the 0.1% bar; 44% at p=8.5,e=0.9). Mechanism: T_r is the
  dt/dφ = E/(Lu²(1−2u)) rule integrated over the law's own shape, and the rotation's cosine
  shape mis-weights the periapsis peak by O(e²u); the frozen law's band-kinked shape is
  second-order-accurate instead. So the compiled cycle needs its **shape word** (Darwin's
  r=p/(1+e cos χ), dφ/dχ=√(p/(p−6−2e cos χ)) — also closed form) if 0.1% periods must hold;
  that is the next one-row experiment, now precisely priced.
- Repeat/cycle identity: frozen cycles repeat to 0.0 spread (8 seeds × 3 cycles); the
  rotation arms are closed-form generators (identical by construction).
- ISCO pair on the band channel (scoped unchanged by the refit): bound case ✓, plunge case ✓.
- **Instrument limitation, disclosed:** my port of the frozen law misclassifies 2 of 6
  capture cases (L=2.00, L=3.88 — both truth-absorbed read as not-absorbed; L=3.60, 4.12,
  4.40, 6.00 correct). Mechanism shown in the log: at hyperbolic-band seams the event list
  can enter a zero-length cycle (state frozen at u=lo(40), band 40, L=3.88) — the frozen
  rung text does not specify turn/root rules inside unstable bands, and the prior run's
  capture pass is not reproduced by my port. The refit row is bound-orbit-only and
  unaffected, but r1's re-freeze must pin the hyperbolic seam rule.

## Predictions

Pre-registered in `predictions.md` before the run. P1 (control) held; P2's e=0 deletion and
invL failure held, its eccentric-corner regression was milder than predicted (1 seed vs
25%), and its period collapse was not predicted as total; P3's advance half held exactly
(8×10⁻¹⁶ < 1e-12 everywhere, kill criterion not fired) but **P3's period half failed**
(median 1.1e-3 vs <1e-5; worst 8.0e-2/44% vs ≤3e-2) — reported as held-out miss, and it is
the finding: the shape, not the frequency, is the residual channel. P4 held (crossings 4 at
m=2 vs predicted 7–14, better).

## What would make it wrong

The agm arm's advance is the same closed form the oracle uses, fed by an independent compile
(the cubic solve) — the advance metric is a wiring check, not an independent derivation;
the row's load-bearing measurements are the period family (fails where the shape fails),
the crossings and the frozen control. Domain: one static mass, equatorial, bound orbits,
r1's sampler and held-outs; light (which passed 64/64 frozen and is untouched), capture
seams (above), multi-source cells (tides, aggregates — the cells' real job) are all outside.
The frozen control's m8-precession 3-seed discrepancy with the prior run bounds how tightly
my port pins theirs.

## Cost of adoption, fit with PRINCIPLES

One sentence in representation.md §1's Binet clause (the in-band frequency is the compiled
cycle's own, from its turning points; the bands keep crossings, plunge and memory), plus a
re-freeze of r1 with m as a cost dial (2≤m≤16), a deterministic near-circular row (now
exact), the Darwin-shape question priced, and the hyperbolic seam rule specified. No engine
code depends on the current clause (the cells are design-level, not wired into the plane).
PRINCIPLES #19: "if you find yourself fixing things that's oftentimes a signal that it is
the wrong representation" — the band centre was that signal; the fix is not a better centre
but deleting the centre. #7: "Geodesics are as trivial as straight lines" — one rotation per
cycle at its own exact frequency is that triviality, measured.

## The lens

First-principles, one component: the component was the in-band frequency; the floor came out
closed-form (Darwin/AGM), and the measured gap was 12 orders of accuracy and 19.5× events.
What the lens may have missed (its named blind spot — cost moved to a neighbour): the period
channel took the load the advance dropped — measured and priced above, not hidden; the
capture-seam underdetermination is the other neighbour this run exposed but did not fix.
