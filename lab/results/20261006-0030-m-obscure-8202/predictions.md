# Predictions — 20261006-0030-m-obscure-8202 (m-obscure lens)

Written **before** the decisive runs. Cases below were not tuned on. Kill criteria are
frozen here; the checker may run the scripts on reshuffled seeds.

## Probe A — every boring stream is a linear recurrence (Prony / Berlekamp–Massey / Bareiss)

Scene: emitter and observer on two incommensurate Kepler orbits (light-cone gather,
c = 10 scene units, 64 frames per emitter period, 8192 frames, root found by bisection
to 1e-13). Stream = apparent angle of the emitter (unwrapped) and the emission
eccentric anomaly E.

- **A1 (order).** Least-squares recurrence order k ≤ 24 predicts the stream to
  relative error < 1e-6 for e_emit ∈ {0.05, 0.3, 0.7}, e_obs ∈ {0.1, 0.3}.
  **Kill:** k > 40 needed at e ≤ 0.7.
- **A2 (integer drift, the law's grid).** With coefficients and samples quantized to
  Q24 fixed point, prediction error stays < 1e-6 (relative to the 2π range) for
  ≥ 256 frames after identification — bounded error, not compounding (roots on the
  unit circle ⇒ marginal stability).
  **Kill:** drift crosses 1e-6 in < 16 frames (then re-anchoring costs more than the
  Newton it replaces).
- **A3 (cost vs Newton).** With the predicted root as the starter, ≥ 80% of frames
  need 0 further Newton iterations for the view's tolerance (residual < 1e-9 of the
  frame interval); the gather's iteration count falls ≥ 2× vs cold last-frame Newton.
  **Kill:** median iterations with prediction > 1 (no win).
- **A4 (held out: kick).** A Δv of 1e-4 relative at frame 3000 (e = 0.3 case) is
  flagged by the prediction residual (|s − ŝ| > 3× running robust sigma) within
  ≤ 2 frames, and a sliding-window re-identification (k + 8 samples) restores
  < 1e-6 prediction within k + 16 frames.
  **Kill:** the kick is not flagged within 2 frames, or re-identification needs
  > 4k frames (then post-kick amortization beats nothing).
- **A5 (held out: order vs eccentricity).** The needed order k grows roughly
  linearly in e (Fourier content ~ n·e): I predict k(0.7) / k(0.05) ∈ [1.5, 8].
  A superlinear blow-up (ratio > 20) kills the high-e usefulness.

## Probe B — the frame budget's p99 as an integer (max,+) window certificate

Scene: 50,000 frames, 8 workers of capacity 1 integer unit/frame, deadline slack
D = 2 frames, arrivals = 60% deterministic base + heavy-tailed bursts
(Pareto tail index α = 2.5, mean utilization ≈ 75%). Certificate
W* = max over windows [u,v] of (Σ arrivals − 8·|window|), integer, one pass.
Policies: single EDF queue; 8 round-robin shards; 8 shards + emergency stealing.

- **B1 (soundness).** Single-queue EDF misses deadlines only in frames where the
  deadline-window certificate (Σ work with deadline ≤ v − 8·width, max over windows)
  is > 0. Any miss with certificate 0 means my implementation is wrong ⇒ VOID, and
  I report it as such.
- **B2 (exactness).** Work-conserving single-queue backlog equals the Lindley
  recursion and its maximum equals W* exactly (integer identity).
- **B3 (coordination value).** Round-robin shards inflate p99 lateness ≥ 2× vs the
  single queue; stealing recovers ≥ half the gap. If shards ≈ single queue,
  coordination is worthless here and the certificate's adoption value is only B1/B2.
- **B4 (held out: fatter tail).** At α = 1.5, utilization 70%: p99/median lateness
  ratio ≥ 10 (the tail decides; means would lie). If the ratio is < 3, the heavy-tail
  framing of smoothness is overstated for this workload.
- **B5 (cost).** W* over 10⁵ frames computes in < 1 s single-threaded (it is two
  prefix-sum passes). Slower than 5 s kills "cheap certificate".

## What would make the whole direction wrong

- Probe A: apparent streams near conjunction have topology changes (root jumps) that
  no fixed-order recurrence tracks; drift compounds in fixed point; order scales with
  harmonics × resolution so the win over Newton vanishes.
- Probe B: the certificate is vacuous (> 10× loose) on realistic mixes, or the
  arrival model (iid bursts) misses the engine's real correlation structure
  (bursts share causes — a battle is one event, not many) so tightly that no
  conclusion transfers.
