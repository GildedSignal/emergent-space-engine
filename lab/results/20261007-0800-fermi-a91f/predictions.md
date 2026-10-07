# Predictions (written before the decisive runs)

Question: is H_live (live distinguishing bits per body) bounded in steady play, and what sets the 8 GB / 10⁹ budget?

Model (before any run): the law's kick deltas are uniform on fixed-width integer grids (shipmem's
`Pop::kick`: Δt ±2^16, ΔE ±2^10, ΔL ±2^10, Δω ±2^10). After K kicks, a body's deviation from its
program is a sum of K iid uniforms per column, so its **state** entropy grows as
H(K) ≈ 4·(11 + ½·log₂ K) bits, while the **draw account** (what a naive store or a logged history
pays) grows as 44·K bits. The store keeps current states, not histories, so the floor is the state
entropy, bounded by the law's fixed grid (~157 bits fully random).

Held-out cases (not tuned on; the code only measures):

- P1 (state floor): bits/ship after every ship is kicked K = 1, 16, 256, 1024 times (seed 7):
  ~44–52 at K=1, ~52–58 at K=16, ~56–64 at K=256, ~60–70 at K=1024. Log growth, slope ≈ 2 bits
  per doubling of K per ship (4 columns × ½ bit per doubling).
- P2 (draw account): at K = 256 the draw account exceeds the state floor by more than 100×.
- P3 (shipped store): the shelf, kicked at x = 0.25 per epoch with a compact after each epoch,
  stays within 2× the state floor + 2 bytes per live ship through K̄ ≈ 8 expected kicks per ship;
  no per-epoch compounding (slope in log K̄, not K̄). Round trip bit-exact.
- P4 (compute): hot update + amortized compact cost < 5 µs per kick, so reabsorbing the board's
  6×10⁴ kicks/game-second costs < 30% of one core.
- P5 (budget): a population whose every member has been kicked once (~50 bits/ship) is 6.25 GB at
  10⁹ bodies — it does not fit beside the engine in 8 GB; the affordable ever-kicked fraction at
  50 bits/scar is f ≲ 0.5–0.7 given ~3–4 GB for bodies.

Kill criterion for the whole model: if the measured state floor at K = 1024 exceeds 2× the P1
band (> ~140 bits/ship), H_live is not log-bounded and the 8 GB budget dies on a play-time
horizon; that would make memory, not cadence, the first wall.
