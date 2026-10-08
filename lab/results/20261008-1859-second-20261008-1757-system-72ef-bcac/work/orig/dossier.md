# Dossier — 20261008-1757-system-72ef (system lens)

**Claim.** Measured on the design's own store (genesis program + quantized
scars, drift exact + kicks), a perturbed belt's stored distinguishing
information does **not** accumulate per game-second: it **saturates** at
~64 bits/body (quantum 1e-6), with the per-kick rate falling 5 000× (0.75 →
1.5×10⁻⁴ bits/body/kick) over 4 500 kicks — the H_live premise in its rate
form ("distinctions created per game-second decide whether 10⁹ fit in 8 GB")
is wrong; what decides memory is a one-time saturation level, and that level,
not a drain, is what the 8 GB budget must price.

**Bottleneck.** Board risk #2, "H_live: distinctions per game-second — not
measured yet" (HANDOFF, risks to attack first; queue `b-h-live`). Expected
gain: deletes the rate-monitor framing before it is wired into
`xtask universe`'s dashboard; replaces it with a level measurement and a
recompute-vs-store trade. No 10× compute gain claimed.

**Evidence.** All commands run from `lab/results/20261008-1757-system-72ef/`,
each < 200 MB; each ≤ 60 s except the disclosed 310 s kill test:

- `python3 scars.py control` — μ=0 control: every channel at machine
  precision (p99 ≤ 6×10⁻¹³), entropy exactly 0. (This control caught two
  instrument bugs before the run: a sign flip in the true anomaly and a
  missing Kepler rate in the λ program.)
- `python3 scars.py main` — 31 s: N = 10 000 belt bodies (a ∈ 2.1–3.3 AU,
  includes the 2:1 Jupiter resonance at 3.28; Rayleigh e σ = 0.05), Jupiter
  5.2 AU, e_J = 0.048, μ_J = 9.55×10⁻⁴; KDK, Jupiter on its exact Kepler
  tube, 150 kicks per Jupiter orbit, 4 500 kicks = 30 Jupiter orbits ≈ 150
  belt orbits (356 yr; the JSON's `t_yr` column is in GM = 1 time units,
  1 yr = 2π). Outputs `scars-main.json`, raw arrays `scars-main-final.npz`.
  Scar channels: Δa/a, Δh, Δk, Δϖ (wrapped), Δλ against the program's own
  Kepler rate.

| kicks | 1 | 13 | 116 | 348 | 1042 | 3122 | 4500 | 45000 |
|---|---|---|---|---|---|---|---|---|
| H_total bits/body | 39.6 | 55.2 | 61.4 | 62.4 | 62.8 | 63.4 | 63.6 | 64.3 |
| slope vs log₂(kicks) | | | | | | | 1.75 b/oct avg | **0.19 b/oct tail** |

- **10× horizon kill test** (`python3 scars.py long`, 310 s, backgrounded —
  over the 60 s guide, disclosed; 45 000 kicks = 1 500 belt orbits):
  H_total = 64.31 bits vs 63.61 at 4 500 — +0.7 bits for 10× the time, tail
  slope 0.19 bits/octave. The saturation is real, not the knee of a climb.
  `scars-long.json` holds it.

- Saturation level vs quantum at the 45 000-kick horizon: 60.6 bits at
  q = 1e-5, 64.3 at 1e-6, 66.0 at 1e-7 — ~3.3 bits per decade of resolution;
  the level is set by the scar distribution's width (bounded wander), not by
  time or by the quantum.
- At 10⁹ bodies: 7.2 GB (q = 1e-5) to 8.2 GB (q = 1e-7) — the level, not a
  drain, is what brushes the 8 GB ceiling; against the naive per-kick store
  (32 bits × 5 channels × 4 500 kicks = 7.2×10⁵ bits/body) the scar layer is
  ~11 000× smaller at equal exactness (every body regenerates exactly).
- Resonance (held-out prediction 3, held): the 4.7% of bodies within 1% of
  the 2:1 carry the largest scars (|Δa| p99 2.4×10⁻² vs 5.6×10⁻³ elsewhere;
  |Δh| p99 0.19 vs 0.045) and still saturate below the mod-2π bound
  (log₂(2π/q) = 22.6 bits/channel).

**Predictions** (`predictions.md`, written before the run): #1 near-miss
(63.6 vs the promised ≤ 60 bits — the shape held: no linear channel,
slope decelerating 1.75 bits/octave average → 0.5 bits over the last
octave); #2 held (rate ratio 5 000×); #3 held; **#4 failed and is reported**:
a per-body linear-rate program compresses nothing (63.2 vs 63.6 bits) — the
per-body precession is quasi-periodic, not linear (inspected: Δϖ wanders
non-monotonically while e pumps 0.040 → 0.056 over the horizon), so the
saturation level is not cheaply compressible by "one rate per body".
A two-phasor program is the untested candidate.

**What would make it wrong.** (1) ~~Longer horizons~~ — tested: the 10× run
holds the level (64.3 bits, tail slope 0.19 b/oct); a 100× horizon remains
open but the trend is flat. (2) Encounter-rich play: contacts add event
records (index state, not sums) and fleets on one orbit (taleb gold) may
saturate higher than a Rayleigh belt.
(3) One μ, one belt shape, 1 500 belt orbits; the plane's B18b belt at 2²³
bodies and the engine's own kick cadence may sit elsewhere. (4) The
recompute side is unmeasured: canonical memory is zero-rate, but placing a
body without a scar costs replayed kicks — the trade is priced in CPU slack,
not bits.

**Cost of adopting.** None in code: this reframes `b-h-live` before it is
built — instrument the **level** and its quantum scaling (3.3 bits/decade,
measured), not a bits/second rate; report the scar table against the 8 GB
ceiling per workload class. Fit with PRINCIPLES: "Store the generator, not
the generated" (#6) — the belt's generator is 0.126 bits/body (components-98bc)
and its time evolution adds a bounded, saturating correction, because
"influences below one quantum accumulate" into the same stored sums;
"Microstates are canonical... observation never changes outcomes" (HANDOFF)
— the scar layer is cache, not truth.

**The lens (simplification, unification, deletion).** The scar layer, replay
checkpoints and the H_live budget are one structure: a cache of a
deterministic function of (genesis, player log). Canonical memory has entropy
rate exactly zero — the player is the only wildcard (#5) — so nothing
"created per game-second" is canonical; the measurement shows even the cache
saturates (10× horizon run: +0.7 bits). The next experiment is named, not
run: a two-phasor program on the saved raw arrays, and an encounter-rich
scene for the event-record channel.

**What this lens may have missed.** Elegant unifications hide hard special
cases: a dense fleet's phase-neighbour certificates and contact event records
are index state that grows with *events*, not with element wander — my scene
has no encounters by construction (belt–Jupiter closest approach 1.65 AU), so
the one channel that could genuinely drain memory per second is unmeasured
here.
