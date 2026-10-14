# Dossier — 20261014-2130-second-20261014-2012-system-a669-eb2d (lens: second author on a669)

## Claim

The checker's named experiment is done — the flip-gated rebind is wired on the shipped engine
(per-population-shaped `ES_KEY_BITS=shape,scale` dial, `Arc`-reuse on key equality, compile
skipped, default bit-identical) — and it **refutes the composed claim**: the live `OrbitKey`'s
periapsis walks ~2⁻¹³ relative per rebind on the belt (~600× the replica's 2.1×10⁻⁷), so the
flip run saturates at ~4 at a quantum the map no longer survives (encounters 934→0, 1,342 kick
refusals), and at the largest map-safe dial the run is 1.33 with the Jacobi walk 30–500× worse —
the ~10²× deletion of the compile stream is not buyable with a coarser key; the per-kick compile
mint itself is confirmed (measured 1.00 compiles/kick, reuse 0 on exact keys).

## Bottleneck

The board's "the kick: 75–160 µs against a ~50 ns floor" via a669's breaks 1/2/4 "one dial".
The experiment deletes the premise's arithmetic, not the bottleneck: the compile term is real
(every kick mints one), but the dial that would amortize it is closed by measured gates.

## Evidence

All numbers regenerate with `./regen.sh` (~9 min: pristine baseline phase, patch, neutrality,
dial sweep, Jacobi arms). Files cited are in `work/`.

**The wiring** (`work/patch.diff`, 89 insertions: `crates/space/src/binding.rs`,
`crates/universe/src/{bind,step,universe}.rs`; instrument `key_dial.rs`):
`Rebinding::from_keyed`/`ending_at_keyed` fit exactly, quantize the key by the dial, and reuse
`prev`'s compiled trajectory when the quantized key is unchanged (bound orbits only; a passage
depends on its edge); `bind_in` `Arc`-reuses the entry when key, sense and unit are unchanged;
`Work::rebind` passes the body's own entry; `Entry` remembers its compiled key; counters
`emergent_space::binding::keyed_counts()` (fresh compiles, reuses). Default (`ES_KEY_BITS`
unset): exact keys, gate on exact equality — a pure memo.

**Neutrality (P1 held).** Pristine vs patched-default, digest lines identical: ladder wave
(`df0e87cd…` N=1000, `d2632de9…` N=3000), ladder crossing, and `frame_digest 5` (8 flights × 4
schedules) — `work/pristine_*.txt` vs `work/default_*.txt`, diff empty outside wall timings.
Reuse on exact keys: **0 of 34,606** fits (memo.rs's law, now counted).

**The shipped stream.** N=3000 through the wave, cut 4,060,508,935 (`work/dial_default.txt`):
kicks 34,537, compiles 34,606 — **1.00 compiles/kick**. a669's mechanism premise is a counted
fact on shipped code.

**The dial** (`work/dial_*.txt`, `ES_KEY_BITS=shape_bits,scale_bits` on `OrbitKey`: shape
quantizes `2k−1`, scale quantizes periapsis):

| dial | reuse | compiles/kick | kicks | encounters | refused |
|---|---|---|---|---|---|
| default | 0.000 | 1.00 | 34537 | 934 | 0 |
| 48,16 / 33,16 | 0.000 | 1.04 | 33296/33300 | **0** | ~1300 |
| 24,16 | 0.136 | 0.90 | 33223 | **0** | ~1300 |
| 12,12 | 0.747 | 0.26 | 33203 | **0** | **1342** |
| 12,24 | 0.249 | 0.75 | 34537 | 928 | 0 |
| 12,28 | 0.067 | 0.93 | 34537 | 928 | 0 |
| 12,32 / 16,32 | 0.010 | 0.99 | 34537 | 928/934 | 0 |
| 16,28 | 0.078 | 0.92 | 34537 | 934 | 0 |

Monotone in the scale word, and the run it buys is walk-limited: reuse 0.747 at quantum 2⁻¹¹
(run ≈ 3.95), 0.249 at 2⁻²³ (run 1.33), 0.010 at 2⁻³¹ (run 1.01) — one per-rebind periapsis
walk of **~2⁻¹³ relative** fits all four arms. A run of 100 needs a quantum of ~2⁻⁶·⁵; at the
measured death points the map is already gone (encounters 0 at scale ≤ 16) and ~4% of fits
refuse outright (the quantized key leaves the compilable envelope: 1,342 refusals at 12,12).

**The exactness leg (B12-type, P4 failed).** `jacobi 6 100 6` (`work/jacobi_*.txt`): baseline
worst per ship 2.8e-6…5.1e-6; at `20,36` (reuse ~0 on this scene) 8.0e-5…9.7e-4 (30–500×); at
`16,32` (reuse 1.0% on the ladder) worst 4.6e-3 (~900–1600×); at `16,28` and `12,24` the
readout itself panics (`Space(Range)`). **No measured dial has material reuse and a held
conservation walk.** The largest map-safe point (12,24) is a 1.33× compile cut at −0.6%
encounters — and it breaks the deep-field readout.

**Why the replica missed it (mechanism, named).** The engine's fitted key is derived from
`decode(tube) + residual`, and the residual is a frozen Cartesian offset: at each rebind it maps
to element changes of order |residual|/r, so the key walks by representation even when the
physical kick is sub-quantum. a669's replica re-fit a continuously propagated state, so it saw
only the physical ΔL (2×10⁻⁷) and predicted 226–3.7×10⁶ quanta per kick. The residual keeps the
readout exact **at events**; it does not keep the **key** from walking between them — which is
law.md:36's recorded objection ("it re-rounds the orbit at every kick, a random walk"),
confirmed on shipped code with the gate wired.

## Predictions

`predictions.md` was written after the patch built and baselines flew, before any dial run.
P1 held (bit-identical neutrality, reuse 0). P2 held in direction, failed in magnitude — the
run caps at ~4, not ~100: the live key's walk is ~600× the replica's. P3 held where the map
survived (kicks equal, encounters −0.6% at 12,24) and failed at coarse dials (encounters → 0).
P4 failed: 30–500× at the mildest arm, panics at 13.6% reuse. P5 not cleanly held: wall times
on the shared box are noise (default 8.4 s cold-cache vs 5.4 s warm at equal work); the compile
counter, not the clock, carries the result.

## What would make it wrong, cost, fit

- The walk constant 2⁻¹³ is derived from four run-length arms, not logged per body; a
  Δlog-periapsis instrument could move it by small factors. It cannot move it 500×, which is
  what the 10²× dial needs. The boundary clock only reads (no rebind), so the walk is per kick.
- The dial here is one global env setting, not a per-population byte; per-population choice
  selects within the same measured frontier (finer for hot dolls, where flips are free anyway).
- One scene (seed 1, ladder belt, coast), one Linux box, cold belt only — the refutation's
  domain. Hot scenes flip at any grain and were never the dial's claim.
- Cost of what survives: the wiring is default-neutral and keeps a counted memo at exact keys
  (0 hits on 34.6k — free, useless today). The real cost is the conclusion: the compile stream
  must fall to a **key that does not walk** — carry the fit's drift as an integer phasor on the
  binding instead of re-fitting through a frozen residual — not to a coarser quantum.
- PRINCIPLES #13 ("basically we don't want errors that can compound"): the coarser key's walk
  compounds ~600× faster than the replica claimed; #34 — the oracles (the encounter scan, the
  Jacobi instrument) rejected the coarser representation exactly as guards should; #9 — this
  kills the configuration, never the method: breaks 1/2/4 remain one mechanism (the per-kick
  mint, now counted at 1.00/kick), but the dial is not the lever.

## The lens

Second-author lens: I ran the checker's experiment, not a fresh question. Missed by it: the
reuse gate excludes passages (edge-dependent) — under 1% of the belt stream, immaterial; the
walk constant is inferred, not directly logged; wall-clock claims are unreliable on this box,
so the CPU half of the composition rests on the counter plus b29a's 21 µs, not on a re-timed
wave. The refutation answers memo.rs's requirement (B1/B2/B9 re-judged on memo keys) in the
only form that matters: at every dial where keys memoize, the walk the memo induces already
fails the cheaper instruments downstream.

Grade suggestion: **gold as a refutation** — the named experiment ran on shipped code, the
record regenerates, and the held-out predictions that failed name the mechanism.
