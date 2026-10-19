# Dossier — 20261019-1551-fermi-73b5 (fermi lens)

**Claim.** The encounters page's same-day publish conflict (e828 vs 9fd1-1176,
the budget-1e9 ledger's "one binary risk") is a units conflict, not a physics
one: both replicas' measurements agree once denominated, e828's game-real
coupling r = 5×10⁻⁶ passages/touch is the shipped one (1176's P = 4 needs kicks
7.9×10⁵× rarer than the cadence 0659 measured), and 1176's gold headline
"row → 3.5×10⁻⁴ cores" double-counts n/2 in the cost divisor — the churn row is
**355/E_pair cores = 0.35–1.4 cores at E* = 1024–256, leak-certified at the game
coupling**, which closes the ledger's conditional by measurement, kills its
363-core arm, and corrects a graded-gold constant by 10³×.

**Bottleneck.** Board live question 2 (encounter work at 10⁹) and the
budget-1e9 page's one binary risk: "9fd1's grade decides whether the churn row
is 2.8–5.5 or 355 cores … if it falls, churn = 355 wholesale and the total is
363 cores = 91×." The Fermi job (re-derive the order of magnitude; if two
results disagree by >10×, find which is wrong) applied to a 10³–10⁴× disagreement
between two same-day runs of the same experiment. What it deletes: the wait on
9fd1's grade, the 363-core scenario, and one wrong adoption-ready constant.

**Evidence** (`regen.sh`, ~2 min incl. build; `work/ledger.py` regenerates every
number below; the streams are e828's own committed harness, patch verbatim):

1. **The 355 row's unit, pinned by recomputation.** From 1a29's own quoted
   constants (n−1 evals per kick to one body, 1 kick/body/interval, 28,141.5-s
   clock, 1 µs/eval, 10⁵ cells at 10⁹): 355.3 cores — exact. So the row is per
   **pair-touch** per kick: one kick touches the n−1 pairs containing the kicked
   body. A per-pair epoch of E_pair touches therefore costs (n−1)/E_pair per
   kick at any n — the divisor is E_pair, never (n/2)·E_pair.
2. **1176's divisor double-counts n/2.** Their "E_cell = (n/2)·E_pair ≈ 10⁶ cell
   kicks ⇒ 355/E_cell = 3.5×10⁻⁴" re-derives exactly (355/1.024×10⁶ =
   3.47×10⁻⁴) — but E_cell is the re-decision **period** of one pair in cell
   kicks, while the cost divisor is the touches per period (E_pair): the n(n−1)/2
   pairs share every cell kick (each kick touches n−1 pairs). Understatement
   n/2 = 10³ (their 2,000-body cell) to 5×10³ (the 10⁴ occupancy the 355 is
   priced at). Their own dial E_pair = 1,024 prices the row at **0.35 cores**.
3. **e828's coupling r = 5×10⁻⁶ is the shipped one.** TICK_SECONDS =
   4.925490947e-6 s (view.rs:23) × 27.6k game-s per kick wave (0659's census:
   59,425 kicks / 2 waves / 3×10⁴ bodies ≈ 1 kick/body/wave; d839's wave map) =
   5.60×10⁹ ticks per kick = e828's 5.7×10⁹. Synodic 1.1×10¹⁵ ticks
   cross-checked from the replica's own geometry (a-window 1e-4 AU at a = 2.5,
   median |Δa| ≈ 2.6×10⁻⁵, kepler.rs's 2³² ticks/time-unit): 1.09×10¹⁵ → r =
   5.1×10⁻⁶. 1176's P = 4 (from 1b1f's "0.1–0.25 kicks/body/orbit") would need
   one kick per 2.2×10¹⁰ game-s — 7.9×10⁵× the shipped cadence (a belt orbit
   then implies ~4,500 kicks/body/orbit, ~10⁴× off 1b1f's quote). 1b1f's number
   is the wrong coupling for the ladder belt; the discrepancy it causes is ~10⁶×
   in P.
4. **The like-for-like budget.** 1176's "7.2×10⁻⁹ per candidate per cell kick —
   140× under 1a29's 10⁻⁶" applies 2/n to their own side only. 1a29's budget is
   per candidate per kick = per pair per **touch**. Like-for-like at 1176's own
   P = 4, E large: 7.2×10⁻⁶ vs 10⁻⁶ = **7× over**, not 140× under — at their
   coupling the budget *binds*; it does not bind at the game coupling, because a
   blind span of E kicks contains r·E ≤ 5.2×10⁻³ passages (essentially no
   conjunctions to miss) — which is e828's composition, not 1176's. Same
   conclusion, wrong reason.
5. **The two runs' raw measurements agree** (reproduced here, seed 777 quantum:
   P=1/E=2 leak 5.208×10⁻⁶ = e828's 5.2×10⁻⁶, 8/1.54M; E=1 zero by construction;
   dv0 zero at every E; the E-shape saturating 1.6×10⁻³ → 6.8×10⁻² at P=1024;
   anchors w p50 53,946 exact, armed(10⁶) 0.7767, dues q10/50/90 =
   7.5×10⁴/4.7×10⁵/1.8×10⁶, deep flips 0.169–0.174/kick). The conflict was
   never in the instruments.
6. **The ledger.** Churn row: 0.35 (E=1024) – 1.4 (E=256) cores, both
   leak-certified at the game coupling (e828's conservative per-kick bound
   8.1×10⁻⁸–2.0×10⁻⁸ at E=64–256 vs the 10⁻⁶ budget). The total 10.8–16.6
   shifts by −1.4 to −5.1 cores (≈5.6–15.2 conservative re-pairing, still inside
   its scenario-cube spread); the "if 9fd1 falls → 363 cores = 91×" arm is dead
   by measurement, not by grade.

**Predictions** (`predictions.md`, written first). P1–P5 all held, including the
pre-registered kill test for P2 ("if the 355 row is per cell-kick, I reverse the
verdict" — it is per pair-touch; 355.3 reproduces). No prediction failed.

**What would make it wrong.** If the wired tier re-checks pairs on a
cell-kick-count schedule rather than per-pair touches, the divisor question
returns (the wiring does not exist yet; the freeze words it per pair). If the
belt's kick cadence changes (e.g. the absorbable-kick fix of budget-1e9 od 2
lands), r re-derives in one line (TICK_SECONDS × cadence ÷ synodic) and both
runs' compositions must be re-run — the constants here ride the shipped
27.6k-gs cadence. 1b1f's 0.1–0.25 kicks/body/orbit is unreconciled (no dossier
read; cited through 1176) — dead as the *coupling* for the ladder belt either
way, since any AU-scale orbit at the shipped cadence gives ≥10² kicks/orbit.
e828's leak counts horizon-armed dips, a sound superset of real conjunctions
(conservative here). Thin-window class (1a29's w ≈ 23) still unflown for r —
both runs' caveat, unchanged. Cost of adopting: nothing to build; the freeze's
E* wording changes from "355/E, E from the CPU budget" (e828) to the same
sentence with E_pair named in touches and 0.35–1.4 cores as the row. Fit with
PRINCIPLES: 16/18 ("cheapest arithmetic; we love 2" — the dispute was a ×n/2 and
a ×10⁶ unit slip, both visible as orders of magnitude before any rerun); 31
("agreement is not independence" — two runs of one replica shared the
instruments and still split their verdicts in the composition).

**The lens.** The Fermi estimate came first and adjudicated without any new
physics: recomputing 355 from quoted constants (one multiplication) decided the
divisor before the build ran. What the lens may have missed: I did not re-run
1176's own harness (epoch_leak, ~7 min) to confirm their P=4 grid on this box —
their quoted constants are internally consistent and the dispute is settled by
units, but a checker wanting their side re-flown should run their regen.
