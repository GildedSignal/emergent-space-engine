# Predictions — 20261019-1551-fermi-73b5 (written before any run of mine)

Question: the encounters page's publish conflict — e828 ("churn row = 355/E cores,
E* = 64–256 CPU-chosen, leak-unbound") vs 9fd1-1176 ("row → 3.5×10⁻⁴ cores, leak
140× under budget at every E"). Both ran e87d's integer replica of the shipped tier
with an epoch dial; their verdicts differ by ~10³–10⁴×. I re-derive the order of
magnitude independently (Fermi lens) and reproduce e828's anchors from their own
committed patch.

## P1 (the coupling constant). e828's r = 5×10⁻⁶ passages per touch is the game-real
one; 1176's P = 2–10 (from 1b1f's "0.1–0.25 kicks/body/orbit") is not.
Derivation from shipped code and measured cadences: TICK_SECONDS = 4.925490947e-6 s
(view.rs:23) → 2.03×10⁵ ticks/game-s; the belt's kick cadence ≈ one kick per body per
doll step ≈ 27.4–27.6k game-s (0659's clock census 59,425/2 waves at 3×10⁴ bodies;
d839's wave map) → kick interval ≈ 5.6×10⁹ ticks = e828's 5.7×10⁹. Candidate-pair
synodics ~1.1×10¹⁵ ticks (near pairs, |Δn| small) → r ≈ 5×10⁻⁶. For 1b1f's P ≈ 4 to
hold, kicks would have to be ~10⁶× rarer (belt orbit ~10⁻² AU at the same cadence) —
impossible on the shipped plane. Prediction: the numbers reproduce; r is anchored.

## P2 (the cost divisor). 1176's "E_cell = (n/2)·E_pair ⇒ row = 355/E_cell"
double-counts n/2. The 355-core row (1a29) is n−1 evals per kick TO ONE BODY =
per pair-touch per kick; under a per-pair epoch of E_pair touches the per-kick cost
is (n−1)/E_pair (each cell kick touches n−1 pairs; a specific pair is re-decided
every E_pair touches = every (n/2)·E_pair cell kicks, but there are n(n−1)/2 pairs
sharing those kicks). Correct row at their own dial (E_pair = 1024): 355/1024 ≈
0.35 cores, not 3.5×10⁻⁴ — a factor n/2 = 10³ (their cell) to 5×10³ (the 10⁴
occupancy the 355 is priced at).

## P3 (the like-for-like budget). 1176's "7.2×10⁻⁹ per candidate per cell kick —
140× under 1a29's 10⁻⁶" converts only their own side by 2/n. 1a29's 10⁻⁶ is per
candidate per KICK = per pair per TOUCH (their flight: 0.055 flips/kick over the
n−1 scanned pairs at 10⁴). Like-for-like at 1176's own P = 4, E large: 7.2×10⁻⁶ per
pair per touch vs 10⁻⁶ = ~7× OVER, not 140× under. The leak budget DOES bind at
P = 4 — it does not bind at the game-real coupling (r ≪ 1 passages per blind span),
which is e828's composition, not 1176's.

## P4 (the two runs' raw measurements agree). At P = 1 the two replicas' leaks agree
in order: e828 5.2×10⁻⁶ per interval (seed 777, 8 events/1.54M), 1176 3.0×10⁻⁶/touch
saturating, miss_frac 1−1/E at the quantum. The conflict is composition units, not
physics. Prediction: e828's regen reproduces (armed(10⁶) = 0.7742, w p50 53,946,
deep flips 0.169–0.174/kick; P=1 column 0/5.2×10⁻⁶/0 by seed).

## P5 (the ledger). The budget-1e9 conditional closes at the good end, by
measurement not by 9fd1's grade: churn row 0.35–1.4 cores at E* = 1024–256
(leak-certified at the game coupling), ledger total shifts by ≤ 5 cores (10.8–16.6
→ ~8.4–13), and the 363-core arm (9fd1 falls → wholesale) is dead: both runs'
measurements support the epoch rule; only 1176's two conversions were wrong.

## Kill criteria for my own run
- If e828's regen does NOT reproduce their anchors, my P4 fails and the
  adjudication rests on citations alone (report as such).
- If the 355 row turns out denominated per cell-kick (not per pair-touch), P2's
  factor vanishes and 1176's divisor is right — I would then reverse the verdict.
  Test: recompute 1a29's 355 from their own quoted numbers (n−1 evals/kick,
  1 kick/body/interval, 28,141.5-s clock, 1 µs/eval, 10⁵ cells at 10⁹).
