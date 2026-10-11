# Dossier — 20261011-1234-second-20261011-1102-scout-4c5b-dde0 (lens: second author)

Second-author run on 4c5b. Everything below regenerates from this folder: `python3 inspiral.py`
(the run's own script + the checker's one-line `circ_L` fix; 42 s, writes `inspiral-out.json`),
`python3 second.py all` (7 s: kill grid, step convergence, W2 scaling), `python3 second.py
m1000c` (50 s) and `python3 second.py m1000e` (32 s) (measured re-keys from 1000M). numpy only,
every process < 100 MB.

## Claim

The checker's named gold path is done, and the (corrected) claim holds: **Peters' flux balance
drifting the exact Schwarzschild tube's (E, L) is adoptable inside B11's frozen domain
(p 20–1000M, e ≤ 0.6, ν ≤ 0.25) at the 1% behaviour bar — the pre-registered kill line
(wall ≥ 5× the separatrix at ν ≥ 0.01) is crossed nowhere inside it** (worst corner 4.8 at
e₀ = 0.6, p = 20M: born at its own 1% wall, a 23-orbit life — no margin) **and first crossed at
e₀ ≈ 0.65 (ν = 0.25) / e₀ ≈ 0.85 (ν = 0.01), the corner the frozen gate already excludes**,
while the EMRI corner (ν = 10⁻³) stays adiabatic even at e₀ = 0.9 (no 1% wall at all). The
design constants as measured: handoff = the exact separatrix, receiving a\* ∈ [6, 9]M with
e\* ≤ 0.09 for p ≳ 100M births (e\* is soft: 0 ↔ 0.09 under step tightening; up to ~0.2 at the
p = 20M edge where 23 orbits cannot circularize); the generator is a calendar event, not a cost
— **measured 642 (eccentric e₀ = 0.3) / 759 (circular) re-keys from 1000M at the 1% bar,
1.2–1.3×10⁻³ per orbit** (the telescoped 551/690 column and the "0.005/orbit" claim, 4× high,
are withdrawn); and **no projection rule**: the two-flux drift is self-consistent — spurious
e = 0.0 from 100M (final L +0.79% at ISCO), so the original P9 "wiring inconsistency" was the
`circ_L` artifact and the author's pre-registered prediction had held.

## Bottleneck

Same as 4c5b (HANDOFF "Headed next" #4, the unowned inspiral item): not a speedup but a
deletion plus a contract — it kills inspiral-as-kicks permanently (df81) and hands the
motion-law v2 finishers the generator's measured constants. This run's addition is the
**domain of adoptability as a measured boundary** (e_kill(ν)), which is what the integrator
needs to write into the gate.

## Evidence

**The fix and the record (A).** `circ_L`: coded √(a/(a−3)), true a/√(a−3) — proven by the
author's own control, `EL_from_ae(a, e→0)` (agrees to 1e-15 at a ∈ {8, 30, 100, 1000}) and by
the double-root residual R(u₀) = −1.1e-16 with the family L (+0.010 with the coded one).
Rerun on the fixed code: **exactly one field of `inspiral-out.json` changes —
`P9_spurious_e`: 0.8149 → 0.0** (field-by-field diff against the original JSON; every other
value bit-identical). P9 as characterized: two-flux drift from a circular birth lands at
L = 3.4916 vs family 3.4641 at the ISCO (**+0.79%**), spurious e below the harness's
resolution — the author's registered band [1e-4, 1e-2] was an over-estimate of a real but
sub-resolution effect. The projection rule is withdrawn.

**The kill criterion, applied (B)** — births at the p = 20M boundary (a₀ = 20/(1−e₀²)),
`second-all.json`:

| ν | e₀=0.5 | 0.6 | 0.65 | 0.7 | 0.75 | 0.8 | 0.9 |
|---|---|---|---|---|---|---|---|
| 0.25 wall/sep | 4.1 | 4.8 | 5.0 | 4.9 | 6.6 | 8.1 | **15.0** |
| 0.01 wall/sep | 1.1 | 1.1 | 0.9 | 0.9 | 1.1 | 1.1 | **14.7** |

The checker's exact case (ν = 0.25, e₀ = 0.9, a₀ = 110M, p = 20.9M): ratio **14.7**, kill
fires. Domain note the checker missed: B11's frozen domain is "p 20–1000, **e ≤ 0.6**, ν ≤
0.25" (law.md gate table) — the dossier had quoted it as "(ν ≤ 0.25, p ≥ 20M)", dropping the
e-cap. With the correct domain the kill does not fire inside it — but with zero margin at the
worst corner (4.8 at e₀ = 0.6), so the honest adoptability statement carries the measured
boundary e_kill(0.25) ≈ 0.65 ± 0.05 (the 0.65/0.7 inversion is endpoint wiggle, ±1M in
a_end), e_kill(0.01) ∈ (0.8, 0.9). At ν = 0.01, e ≤ 0.8 the wall coincides with the
separatrix (ratio ≈ 1) — the near-EMRI behaviour already at ν = 0.01.

**Re-keys from 1000M, measured in the shipped code (C)** (`second-m1000c.json`,
`second-m1000e.json`):

| run (ν=0.25) | orbits | re-keys 1% | rate 1% | re-keys 0.1% | rate 0.1% |
|---|---|---|---|---|---|
| circular, a₀=1000M | 627,509 | **759** | 1.21e-3 | 7,591 | 1.21e-2 |
| e₀=0.3, a₀=1000M | 478,997 | **642** | 1.34e-3 | 6,429 | 1.34e-2 |

642/478,997 reproduces the checker's numbers exactly. The eccentric run ends at
a\* = 11.57, e\* = 0.010 (the shipped-code endpoint; the checker's replication gave 6.78 —
near-separatrix sensitivity, see D) — both inside the honest handoff band [6, 12]M, near-circular.

**Soft edges characterized (D).** Step tightening (dt × 0.25, verbatim copy of the shipped
stepper with one scale): a\* moves 6.298→6.193 (e₀=0.3), 6.761→6.265 (e₀=0.6), 6.229→6.102
(ν=0.01, e₀=0.6) — ≤ 0.5M; e\* flips 0.088→0.000 in one case (the checker's 0↔0.03): the
handoff is a **band, not a 0.1M constant**: a\* ∈ [6.1, 6.8] for p = 100M births, [6, 12]M
including the from-1000M endpoint. W2's step scaling: relerr 7.99e-8 → 1.84e-8 for dt P/64 →
P/256 = **4.3× per 4×** (endpoint O(h)-dominated; the dossier's "2×" was one noisy sample).

## Predictions

[predictions.md](predictions.md), written before the runs. **Held: A1 (0.0 < 1e-3), A2 (exactly
one field differs), B1 (crosses 5 in [0.6, 0.8] at ν=0.25: measured ≈0.65), B2 (e_kill(0.01) in
[0.6, 0.9]: measured (0.8, 0.9)), B3 (no kill inside e ≤ 0.6 at 1%: max 4.8), B4 (checker's
case ≥ 11×: 14.7), C2 (642 ∈ [600, 700], rate 1.34e-3), C3 (a\* = 11.57 ∈ [6, 12], e\* ≤ 0.1),
D2 (4.3 ∈ [2, 8]).** **Misses, disclosed: C1** — circular count 759 against my [550, 750]
(1.2% over; the rate prediction < 1.5e-3 held at 1.21e-3); **D1 half** — a\* moved ≤ 0.5M (≤ 2M
predicted) but e\* moved 0.088 (> my 0.05) in the flip case.

## What would make it wrong

- The kill boundary e_kill(ν) is measured on wall(1%)/a_end with a_end wiggling ±1M at the
  separatrix (endpoint sensitivity): the boundary is ±0.05 in e₀, which does not move the
  conclusion (B11's cap sits at the boundary with no margin either way — the gate should name
  e_kill explicitly rather than lean on e ≤ 0.6).
- The from-1000M re-keys inherit the P = 2πa^{3/2} period proxy and the pend-accumulator
  discretization of the shipped code (the re-key bar itself); the true memo-key quantum, which
  the docs do not pin, sets ε̄. Same caveat as 4c5b.
- Adopting costs one flux module + one calendar event type + the separatrix predicate (already
  implicit in the tube) + the 1PN circular coefficient (1% merger-time bar breaks at a₀ ≲
  150M net); a B-gate should now freeze: merger time 1% vs the 1PN-corrected generator inside
  the **corrected** domain (p 20–1000, e ≤ 0.6, ν ≤ 0.25) at the 1% bar, and e\*(ν) at plunge.
- The EMRI corner and the Kerr case remain as 4c5b left them (untested beyond ν = 10⁻³,
  Schwarzschild only).

## PRINCIPLES fit

Unchanged from 4c5b — #3 (compute only surprises: 1.2–1.3e-3 events/orbit, measured), #6 (store
the generator), #13 (staleness resets at each re-key) — and this run adds what #20 asks:
"behaviours over many seeds… not because the laws were made for it to work": the adoptability
boundary is now a measured quantity (e_kill(ν)) taken from the run, not an assumed domain
string; the artifact-driven "projection rule" (a law made for a broken harness to work) is
deleted.

## The lens may have made me miss

The second author inherits the scout's harness wholesale (same flux module, same tube, same
accumulator): agreement with the checker is not independence where we share code — the
bit-identical diff and the exact 642 reproduction are the strong checks precisely because they
are mechanical. What neither run measures: the adiabatic approximation error itself against a
true 2.5PN osculating integration (both harnesses are the same approximation), and the Kerr
separatrix. The kill grid probes only the p = 20M edge and the e₀ axis at two ν; the interior
(p, e₀, ν) cube is interpolated on trust in F̃(e)'s monotonicity.
