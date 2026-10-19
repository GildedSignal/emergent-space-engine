# Dossier — 20261019-2017-redteam-8c3e

**Claim.** The multiply-add cycle update (docs/representation.md L67) is refuted
on two measured families of its own doll — inside κ ≲ 0.1–0.25 M of the
Schwarzschild separatrix p_sep = 6+2e (remainder up to 4.5×10⁶ floor-budget
multiples at a 2⁻²⁰ kick, and every crossing kick is categorically
unrepresentable) and at high e far from it (e = 0.98 violates out to κ = 8) —
while it is licensed with ≥ 140× margin at e ≤ 0.9, κ ≥ 0.5; no rung guards it.

**Bottleneck.** Premise census item 3 (kicks and cycle derivatives), accuracy
half — the cost half died in 12db, the accuracy half was never measured
(binet-cells od 4 names it "unguarded by any rung"). This is the compiler's
promised cheap path (the ~50 ns multiply-add vs the 34.8 µs refit the shipped
code actually does on ~99% of kicks), and the doc's own kick list (Peters
inspiral, L67) drives every strong-field binary through the refuted band: an
inspiral traverses κ from O(1) to 0, so it crosses both the violation band and
the crossing with probability 1. Gain: the letter stops promising a mechanism
where it is wrong by 6 orders; the fix (a kick-time separatrix guard, one O(1)
test like 3570's key-range test, plus Δt/Δτ stored ≥ 12 bits finer than the
kick quantum) is priced below.

**Evidence** (exact Schwarzschild timelike geodesics, M=1, equatorial = the
game's plane; cycle map C(E,L) = (Δφ, Δt, Δτ) periapsis-to-periapsis;
budget = 2⁻ʷ·|channel|, generous relative reading; kick = q·E or q·L, both
signs; FD derivatives Richardson-extrapolated, h adaptive 1e-5→1e-11 to stay
bound near the separatrix). Commands:

    cd lab/results/20261019-2017-redteam-8c3e && python3 falsifier.py   # 7 min incl. 2 ODE spot-checks; grid alone 1.6 s

Instrument validation (all regenerate in the output):
- quadrature vs DOP853 (rtol 1e-12), e=0.9/κ=0.5: 1.2–1.6e-11; e=0.5/κ=0.005:
  0.7–1.4e-9; e=0.9/κ=0.05: 0.08–1.2e-11. Smoke vs exact closed form: 1.0e-6.
- q² law: remainder ratio between consecutive kick arms (4× in q) median
  0.003730 vs theory 1/256 = 0.003906 (n=438) — second-order clean, so the FD
  derivatives do not pollute the remainders.

Numbers at the design's own scale (q = 2⁻²⁰, w = 20):
1. **32/66 computed cells violate on Δt** (e ∈ {0.1,0.3,0.5,0.7,0.9,0.98},
   κ = p−(6+2e) ∈ {0.005…8}, the parents at κ ≤ 0.002 for e ≤ 0.3 being below
   the turning-point resolver). Worst multiples: **4.46×10⁶ (Δt)** and
   **5.02×10⁶ (Δφ)** at e=0.1, κ=0.005.
2. **Licensed domain (Δt):** all cells pass at κ ≥ 0.5 for e ≤ 0.3 and κ ≥ 0.25
   for e ∈ {0.5,0.7,0.9} — margin ≥ 140× (worst passing remainder 0.007 budget
   multiples at e=0.9, κ=8). **e=0.98 is non-monotone: it passes for
   0.1 ≤ κ ≤ 4 and fails at κ = 8 (1.16×)** — the apoapsis channel: r_a = 800 M
   there and the cycle map's E-curvature grows like r_a·(1−E)⁻²; a one-quantum
   E-kick moves that apoapsis by ~0.6 M. This channel is e-driven, not
   separatrix-driven, and it is what breaks the far field at diving-run
   eccentricities.
3. **Δφ is the worse channel, not the better one:** its violation band is one
   κ-step wider than Δt's at 5/6 e values (e.g. e=0.9: Δt fails to κ=0.1,
   Δφ to κ=0.25... Δφ e=0.1 fails to κ=0.5).
4. **Crossings are categorically unrepresentable: 78 kicks left the bound
   region; the Taylor extrapolate returns finite cycle constants in every
   case** (recorded `taylor_finite: true` in results.json). The crossing band
   scales as √q exactly: 2⁻²⁴ crosses at κ ≤ 0.005, 2⁻²⁰ at κ ≤ 0.01–0.02,
   2⁻¹⁶ at κ ≤ 0.05–0.1, always in the plunge directions (+E, −L). A body
   pushed across p = 6+2e keeps "cycling" under the letter's mechanism: the
   player sees a ship orbit where it must fall in — an error of type
   (bound/plunge misclassification), the class L60 claims cannot happen.
5. **Refining quanta does not license the family:** κ* = 0.005 for every
   matched (q, w) pair (2⁻¹⁶/16, 2⁻²⁰/20, 2⁻²⁴/24) — because remainder ∝ q²
   while budget ∝ 2⁻ʷ shrinks with it. The lever is the GAP: Δφ passes
   everywhere at 8 bits of gap (q2⁻²⁴, w16), Δt still fails at the boundary —
   Δt needs ≳ 12 bits finer storage than the kick quantum, or the guard.

**Predictions** (predictions.md, frozen before the decisive run): P1 form
held, magnitude failed (κ* at q2⁻¹⁶ measured to 8 at e=0.98 vs predicted
0.05–0.5 — the apoapsis channel was unpredicted); P2 held (√q, both the
boundary and the crossing band); P3 REFUTED (Δφ's band is wider, not 10×
narrower); P4 held at e ≤ 0.9, and the e=0.98/κ=8 cell is a genuine marginal
failure (1.16×) beyond the control's intent — disclosed as a finding; P5 held
(78 crossings, pattern quantitative); P6 partial — the static violating
fraction is large on this separatrix-weighted grid (32/66) but the grid is not
a population; the population-weighted channel stays the inspiral/eccentric
one. Instrument changes, both disclosed: smoke moved from e=1e-4 to e=0.01
(at e ≲ 1e-3 the endpoint-node R falls below float64's E²−V floor; grid cells
sit 8 orders above it), and the κ grid was extended DOWNWARD from the frozen
0.05 to 0.005 (finer; no bar weakened).

**What would make it wrong.** The probe is the doc's own doll (one mass,
Schwarzschild) and its own mechanism as written (kick → constants updated by
stored derivatives). If the designed cheap path secretly includes (a) a
separatrix/distance guard forcing refit inside κ*, or (b) phase re-anchoring
plus second derivatives, the budget violations shrink by (a) removing and (b)
one order — but the crossing stays unrepresentable under any linear update,
and neither (a) nor (b) is in the letter. If the checker finds the remainder
is FD-artifact: the q² law (item above) already rules that out. If a
different cycle definition (e.g. apoapsis-to-apoapsis, or mean-anomaly
phasing) changed C's smoothness class, the apoapsis channel (measured at
κ=8, far from any endpoint subtlety) would survive anyway.

**Cost of adoption.** One O(1) guard at kick time (distance of (E,L) to the
separatrix, exactly computable — the same shape as 3570's key-range test)
routing bodies inside κ*(q) ≈ 0.25·√(q·2²⁰) to the refit or to plunge
handling; Δt/Δτ stored ≥ 12 bits finer than the kick quantum; Δφ's guard band
one κ-step wider than Δt's. That converts L67 from a wrong universal claim
into its measured licensed domain (e ≤ 0.9 and κ ≳ 0.25–0.5 M, margins ≥ 140×)
— the same surgery the wiki already applied to the EOB license. Nothing else
in the design moves: the memo, the cycle representation and the refit are
untouched.

**Fit with PRINCIPLES.** "A failed experiment kills that configuration, never
the method" (P9): the killed configuration is the multiply-add on the
separatrix + high-e families, not the cycle memo. "basically we don't want
errors that can compound" (P13) and L60's own budget: the letter violates its
own error model on measured families, and the violation is an error of type.
The cure follows P1 (delete the promise where it is wrong) and P21 (rough
first, refine when a certificate could break — this is that moment for the
cycle update). One sentence for the amendment: strike L67's universality,
state the licensed domain and the guard.

**Rung criterion.** None exists: `grep -E 'separatrix|multiply-add|derivative|
Taylor|refit' lab/rungs/` returns nothing (verified this run). r1 judges the
in-cell walker on frozen orbits (precession, capture, ISCO), not the
kick→cycle shortcut; r3's handoff criterion is a different event. Freeze-ready
criterion drafted in `r12-cycle-update-separatrix.md` (this folder): behaviour
bar = remainder budget multiples < 1 over the (e, κ) grid at matched (q, w);
type bar = unrepresentable kicks == 0; controls on both sides (refit
negative... i.e. the exact refit must pass everywhere; far-field positive
must pass strongly); scaling bar = q² ratio in [8, 32].

**The lens (what it may have made me miss).** A red-team overweights exotic
cases; I scoped the static-population claim honestly (the grid is
separatrix-weighted, the certain channel is the inspiral), but the probe is
float and single-mass: it says nothing about the nested-doll case (kick +
handoff in the same event), about the binary doll's rotating frame (where
"separatrix" means the resonance layer too — r4's territory), or about what
the shipped code already guards (it refits on ~99% of kicks, so the shipped
plane is arguably already on the safe side of this finding — the refutation
lands on the design's promised cheap path, which is the path the 10⁹ ledger
needs). The doc's L48 contact-frame asymmetry (one body's frame, canonical
choice unstated) remains unattacked — the cheapest next falsifier.
