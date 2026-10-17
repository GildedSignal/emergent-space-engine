# Dossier: the two-body doll's strong-field flank, measured

**Claim.** The premise "two comparable masses form one doll; ν enters only through the
energy map" (representation.md L37, law.md L39) survives its first quantified
next-term test, but only marginally and unguarded: the 2PN ν-in-the-potential term
moves the equal-mass plunge boundary from 6M to 5.718M (−4.71%, just under the frozen
5% kill line; my own prediction said ≥10% and was wrong), shifts periastron advance at
p = 20M by −1.66%, and **no frozen gate classifies binary plunge or stability at
ν > 0** — the 0.282M misclassification band is invisible to every gate that exists.

**Bottleneck.** Not a current compute bottleneck: this is the representation census's
premise 4 (the census run `20261016-1207-redteam-12db` left this flank as the named
open direction 3, "the missing licence for the merger scene the game sells"). Expected
gain: none in orders of magnitude; what it can delete is the wrong belief that the
1PN doll is licensed where the game's poster scene (comparable-mass black holes) lives.
HISTORY L2701 already records "no 2PN comparison" against the two-body oracle; this
run is that comparison's first number.

**Evidence** (float, 1.8 s, `work/eob2pn_flank.py`, output `work/run_final.txt`,
JSON `work/eob2pn.json`; reproduced three times bit-identically during debugging):

Doll = shipped code: `crates/space/src/events/binary.rs` puts the effective orbit on
the **exact Schwarzschild geodesic** (A = 1 − 2u, ν-blind), ν only in the 1PN energy
and clock maps (which I re-verified by hand: E_eff−1 = ε+νε²/2 inverts the exact map
correctly). Oracle = the next term the premise drops: 2PN EOB A(u) = 1 − 2u + 2νu³
(Buonanno–Damour 1999), same kinetic form (g_rr = 1/A; D̂ omitted — see wrongness).

1. **Plunge boundary (circular ISCO from E_eff² maximum along circulars):**

| ν | doll r_ISCO | 2PN r_ISCO | shift |
|---|---|---|---|
| 0.01 | 6.000 M | 5.989 M | −0.18% |
| 0.1 | 6.000 M | 5.909 M | −1.80% |
| 0.25 | 6.000 M | **5.718 M** | **−4.71%** |

   Direction: the doll **destroys too early** — every equal-mass circular binary with
   r ∈ (5.718, 6)M is stable per the oracle and plunged by the doll (band 0.282M).
   Error type, not size (principle 2): a stability-class misclassification.

2. **Periastron advance k = 2π(Ω_φ/Ω_r − 1), circular-adjacent, ratio invariant under
   the energy map:**
   - u = 1/20 (p = 20M, B11's innermost seed): k_doll 1.2267, k_2PN 1.2063:
     **−1.66%** at ν=1/4; −0.67% at ν=0.1.
   - u = 1/1000: −0.025% (ν=1/4). The error scales as νu, as it must.
   - B11's tolerance at p=20 is (1% + 2·8/20) = 81%: the gate concedes the flank by
     design and passes the seed against the 2PN truth; the measured next term (1.66%)
     sits 24× below the gate's own conservative self-estimate (8/p = 40%).

3. **Controls** (both sides): ν→10⁻⁶ reproduces Schwarzschild — u_ISCO = 1/6 to
   3×10⁻⁸, k(1/20) = 1.226657448 vs exact closed form 2π(1/√(1−6u)−1) = 1.226657530
   (residual 8×10⁻⁸ is the real linear-in-ν shift, predicted 6.6×10⁻⁸ from the ν=0.25
   slope); the planted sign-flip (−2νu³) moves the ISCO to 0.1600 (outward), opposite
   to the 2PN shift — the instrument sees sign, it is not a yes-machine.

Reproduce: `cd lab/results/20261017-0552-redteam-1bdf && ./regen.sh` (≤ 2 s; sympy
from the system). No network, no crates build.

**Predictions** (`predictions.md`, frozen before the decisive run): P2 (monotone ν,
<1% at 0.01), P3 (≥1% precession at p=20, <0.1% at p=1000), P4 (controls), P5
(epicyclic ν-shift 0.1–5% — measured 1.66%: inside) **held**. **P1 FAILED: I predicted
u_ISCO shift ≥10% at ν=1/4, measured 4.71%.** Reported as failed; the lens's blind
spot (overweighting exotic strong field) is visible in my own pre-registration.

**What would make it wrong.** The oracle is 2PN in A only: it omits the 3PN a₄u⁴ term
(same structural family, same sign direction as 2νu³) and the D̂ angular correction —
both push the same way, so 4.71% is a **conservative lower bound** on the departure,
not an upper bound; an EOBNR-calibrated or NR-anchored oracle would sit deeper (my
literature check from this box failed: the arXiv API is unreachable and ar5iv serves
the 2024-rewritten LRR; the a₄ value is quoted from memory as unverified [INFERENCE]).
If 3PN+calibration totals under 5% at ν=1/4, the premise stands with margin; the
first number that would flip this dossier to a kill is a calibrated ISCO below
5.7M for equal masses. The circular-adjacent precession does not cover e up to 0.6
(B11's seeds); the eccentric-orbit 2PN precession needs the full Hamiltonian with D̂.

**Cost of adopting the finding:** near zero. Not a code change: (a) the integrator's
one-pass amendment of representation.md should annotate "two comparable masses" with
the measured flank (r_ISCO 5.718M at ν=1/4, 2PN) and route merger-phase binaries
(p ≲ 20M, ν ≳ 0.1) away from the 1PN doll, or license them by a gate; (b) one missing
gate criterion, nameable now: **B4b — for circular binaries at ν ∈ {0.1, 0.25},
plunge/stability classification within 2% of a 2PN-or-better oracle's r_ISCO**, with
the ν-blind doll as the planted negative (it must fail at ν=0.25). Nothing else moves.

**Fit with PRINCIPLES.** Principle 2: "Behaviours matter, not continuum fidelity:
error type over error size" — a plunge misclassification is exactly the wrong type.
Principle 34: "the oracles are guards, not shepherds" — today no guard at all stands
at the binary separatrix; this adds the guard's specification, not a new shepherd.
Principle 10 (measure before claiming): the census called this flank "unlicensed";
now it is "unlicensed and measured, −4.71% at 2PN".

**The lens (premise red-team).** Ranked attacks this run considered: (1) two-body
ν-in-potential at the merger scene — measured here, survives marginally; (2) the
uncreated r5/r6 (already recorded by the census; nothing new to add); (3) Binet/kicks/
view/dense-order — refuted or censused by earlier runs, not re-run (would repeat the
page). What this lens may have missed: the census's five other premises were taken as
standing on their recorded grades, not re-probed; and my oracle is the cheapest
next-term, not the strongest truth. Red-teams overweight exotic cases — here the
exotic case (merger scene) turned out *milder* than predicted, which is itself the
calibration lesson.
