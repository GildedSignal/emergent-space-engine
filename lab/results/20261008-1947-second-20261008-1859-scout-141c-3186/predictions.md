# Predictions — 20261008-1947-second-...-3186 (frozen before the decisive analysis)

The prior run (scout-141c, silver) measured the news-channel law on a Poisson toy. The checker
named the gold experiment: both channels on the plane's **real event stream** (engine physics:
directional cancellation, correlated kicks), accumulator Q set by the receiver's certificate
floor. Record: `kicks_massive.csv` (24,525 kicks, 4 bodies, 4e13 ticks, shipped engine through
its public API; massive streams bit-identical to the full plane with ships/fleet/player — md5
checked over the shared 2e10 window). Receiver anchor from the full plane: the player's step
H = 2^22 ticks, velocity quantum 2^-74 of c, sigma-delta carry 2^-16 of that quantum
⇒ **Q_engine = 2^-74 · 2^-16 / 2^22 = 2^-112 tick^-1 ≈ 1.93e-34**.

News model (from the engine's own registers, not assumed): a kick on a massive source is an
impulse dv over its window T = kick.len; a receiver at distance d that ignores it accumulates a
retarded-force error G·m·|dv|·T/d³ by the source's next kick ⇒ event size s = Gm|dv|T/d³,
arrival t_e + d (c = 1, root unit = tick). This is 1/d³ — *steeper* than the toy's assumed
1/a² (a mass change), so every toy result should tighten, not loosen.

## Frozen predictions

- **P1 (naive channel).** Arrivals = every kick arrival of every massive source in the cone:
  grows exactly as the number of systems N(R) = ρπR² (deterministic count; exponent 2.00, no
  tolerance needed beyond bookkeeping).
- **P2 (accumulator, log law).** Per-octave-shell Σs per window is constant across octaves
  (shell source count ∝ r², per-source size ∝ r^-3) ⇒ fire increments per octave constant
  within ±15% over ≥ 5 octaves at every Q. If increments grow like a positive power of R,
  the toy's identity is missing engine physics and the claim is killed.
- **P3 (crossover, the engine's exponent).** Naive = accumulator at r_cut with
  r_cut ∝ Q^(-1/3) (cube root, from 1/d³), NOT the toy's Q^(-1/2). Slope of log r_cut vs
  log Q = -1/3 ± 0.05. A -1/2 slope means the toy's mass-change model was the right one and
  my impulse model wrong.
- **P4 (directional cancellation).** Vector accumulation (fires floor(|Σ δa_vec|/Q) per shell
  window) ≤ scalar accumulation, ratio in [0.25, 1.0]: real dv directions are quasi-periodic
  within a system but incoherent across systems. Ratio ≈ 0 would mean systematic cancellation
  the toy missed (report it).
- **P5 (correlated kicks).** The real stream's kicks sit on aligned power-of-two grids; all
  replicated systems share them (maximally correlated arrivals). Fires with real aligned times
  vs Poissonized times: within ±5% (correlation cannot inflate past the Σs/Q bound; the toy's
  bursty case said so, the real grid now tests it).
- **P6 (plane scale, the adoption question).** At Q_engine = 2^-112, every source of the
  receiver's own system fires individually (s ≫ Q at d ≲ 5 AU): r_cut(Q_engine) ≥ 10 AU —
  the per-(body, source) cursor stays inside systems (b-news-gravity's territory unchanged)
  and the accumulator engages only beyond. Kill: r_cut(Q_engine) < 1 AU would mean the
  accumulator is needed at system scale and the cursor design is wrong.

Controls on both sides: naive count is the positive control (must be exactly N(R)·rate);
a Q so fine that accumulator = naive at all R (Q → Q_engine·10^-4) is the negative.

## Addendum (2026-10-08T20:25Z, written before any run output existed — no news_engine.json yet)

P2 as frozen contains an arithmetic slip I caught re-deriving it: shell source count ∝ r² times
per-source size ∝ r⁻³ is Σ ∝ 1/r, **not** constant. Corrected expectation: accumulator
increments **halve** per octave (geometric decay, ratio 0.5 ± 0.1), so the quantum channel's
total rate **saturates** as R → ∞ (bounded by ~2× the innermost octaves) — strictly stronger
than the toy's log R (which assumed 1/a² mass-change news). The frozen P2 text stands as the
prediction of record and is expected to FAIL in this tightening direction; the run decides.
P1, P3–P6 unchanged. This is a correction of my algebra, not a peek: the script has produced
no output.
