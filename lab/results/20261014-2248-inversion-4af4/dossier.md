# Dossier — the wave train: what stands between the belt's waves

**Claim.** The ladder's flights stop at the belt's first kick wave, and the record's memory term
("2.6 → 5.1 KB a body at the first kick, exponent 1.0 in kicked bodies") silently assumes the
step happens once; flying the plane through five waves (150,002 game-s, 25 min of play at rtf
100) shows the assumption holds — memory is a step, not a staircase (rss 1,357 → 1,366 MB over
waves 2-5, +0.7%; catalogue constant; one retired binding per body; zero lag; 3 frames over
12 ms in 90,062) — so at 3×10⁵ the plane is flat in *play time*, the binding constraint for
long flights is the CPU cadence, not retention, and the wave train itself shears (width 2.25k →
5.75k game-s, peak 35.8k → 20.2k kicks/sample by wave 5): the birth wave is the worst the
engine ever sees. One protocol trap found on the way: cutting a flight on presented time is
wall-unstable (±1 tick → ±5 kicks → a different digest); the canonical cut
(`frame_to(limit)` + `settle(limit)`, as `universe.rs` documents) removes it.

**Bottleneck.** The board's first: real bodies in the flyable engine (28 → 10⁶ claimed, the
furthest gap). The N ladder's own "next breaks" list prices memory after the first kick but no
flight had ever reached a second wave (20 s flights end before wave 1; the 200 s flights end at
~20 k game-s, mid-gap). If retention grew per wave, memory would grow with play — the project's
named failure mode — at exactly the claimed scale; it does not, and the certificate extends to
play-length flights (expected gain: deletes the "is it stable in play?" question for the memory
term; leaves the cadence law and the compact store as the only levers to 10⁷+).

**Evidence** (all from `examples/wavetrain.rs`, the plane bit for bit — `plane_extra`, seed 1,
coast, rtf 100, 12 ms budget, 60 fps frames, player at Home; commands and raw logs in `out/`):

Arm A — N = 3×10⁵ (300,028 bodies), cut 150,002 game-s, five waves, 90,062 frames, wall 137 s:

| wave | window (game-s) | kicks | width (game-s) | peak kicks/250 gs | rss after (MB) | catalogue | lag | frames >12 ms |
|---|---|---|---|---|---|---|---|---|
| 1 | 13,500-15,750 | 304,341 | 2,250 | 35,807 | 1,357 | 300,076 | 0.000 | 0 |
| 2 | 40,750-43,500 | 300,066 | 2,750 | 34,811 | 1,364 | 300,076 | 0.000 | 1 |
| 3 | 68,250-72,250 | 296,680 | 4,000 | 33,882 | 1,366 | 300,076 | 0.000 | 1 |
| 4 | 96,250-101,250 | 289,630 | 5,002 | 25,403 | 1,366 | 300,076 | 0.000 | 0 |
| 5 | 124,250-130,000 | 282,069 | 5,750 | 20,189 | 1,366 | 300,076 | 0.000 | 0 |

- Memory: 672 MB after the build (2,233 B/body rss) → 1,357 MB after wave 1 (4,515 B/body;
  the climb is linear *through* the wave, ~78 MB per 250 game-s = one binding per kicked body)
  → **+7/+2/0/0 MB at waves 2-5**; hwm = rss at the end (1,366; never exceeded); the engine's
  own accounting ends at 1,378 B/body. Zero refusals, 16 handoffs, dead stable at 30 from
  15 k game-s on, encounters linear (~750 per 15 k game-s, 7,251 total).
- Retention mechanism, measured: the history census (4,106 fixed belt bodies) reads exactly
  **one** retired binding per body at every 5,000-game-s sample — even mid-wave-1 (2,784/4,106
  already kicked hold h=1, none hold h≥2) — so `prune` drops the older retired segment
  essentially inside the wave, as the code read predicted (keep-window ≈ 2.8 k game-s ≪ wave
  spacing). The catalogue's free list returns every rebound slot: 300,076 live entries at every
  sample, all five waves (a669's 1.00 compiles/kick mints and frees; nothing stands).
- The drain: `settle` at the cut finds 0 events outstanding at every arm — no backlog survives
  a wave; presented-time lag is 0.000 at every sample including wave peaks (the ladder measured
  0.446 s lag at 5×10⁵; at 3×10⁵ the 12 ms budget absorbs each wave whole). Held scans appear
  only inside wave 1 (0 → 191 → 0, flushed as the wave passes).
- The wave train shears: each body's interval is its own (~26-29 k game-s), so the cohort's
  width grows ~875 game-s per wave and the peak decays; extrapolated, the wave dissolves into
  the steady stream after ~20 waves (~550 k game-s): the birth wave is the engine's worst
  frame-load event of a whole session, and staggering the birth grid (bf21's suggestion) buys
  the most exactly where it matters most.

Determinism (Arms A/B, identical flights): frames, rss, encounters, opens, boundaries,
handoffs, refused, lost, b_per_body all identical; kicks differ by 5 (1,743,573 vs 1,743,568)
and the digest differs — because the cut lands on *presented* time, which is wall-quantized: A
ended at game_s 150,002, B at 150,001, and B is exactly A minus the 5 kicks due in the last
tick. At N=3,000 (no budget pressure) both cut protocols agree bit-for-bit. The engine's own
canonical protocol (`frame_to(…, limit)`, then `settle(limit)`: "a digest taken after
`settle(limit)` is the same whatever the frames were", universe.rs:1067) removes the wobble —
the control arms A2/B2 below are the corrected test. This matches 38bf's checker note
("decision-bearing digests at the cut are wall-unstable; compare counters, not those digests")
and generalizes it: *any* digest at a presented-time cut is wall-unstable under budget
pressure; wave rungs must freeze cuts at absolute ticks.

Control arms:

- **A2/B2 (identical flights, canonical absolute-tick cut): every counter identical to the digit
  and one digest** — `58de94ab…`, kicks 1,743,559 = 1,743,559, events, encounters 7,251,
  opens, boundaries, handoffs, refused, lost, rss 1,366 = 1,366, b_per_body 1,378, frames
  90,062 = 90,062. The engine is deterministic; the wobble was the cut protocol. At N=3,000
  both protocols agree (`47fd4a85…`), so the presented-time cut is unstable exactly where the
  budget bites.
- **Arm C (N = 2×10⁵, cut 250,000 game-s, ten wave windows, 150,063 frames, wall 171 s):**
  rss 450 MB build → 906 after wave 1 → 914 at the end (per-wave deltas ≤ +3 MB, then 0);
  catalogue 200,076 constant; lag 0.000 everywhere; **zero frames over 12 ms in the whole
  flight** (worst 11.96 ms); peak kicks/sample 32,380 → 7,955 from wave 1 to wave 10 (the
  cohort shears; by waves 7-10 the train is dissolving into the steady stream); held scans
  0 → 135 → 0 (wave 1 only); dead stable at 30; b_per_body 1,404. Prediction 7 (scale-free
  per-body steady state) held: 4,545 B/body rss at 3×10⁵ vs 4,570 at 2×10⁵; catalogue ≈ N at
  both; h2 ≤ 3 of 4,106 sampled bodies, transiently, at a wave (at 3×10⁵ h2 = 0 at every
  census).

Held-out record (prediction 8): encounters linear in play time (7,251 at 3×10⁵ by 150 k game-s;
12,170 at 2×10⁵ by 250 k) and `enc_log` is capped at 4,096 entries (universe.rs:1179) — bounded,
not a growth term; dead bodies 30 at both N, stable from 15 k game-s on.
held stronger than predicted (h2 = 0 *always*, not just between waves). 6 (bit-identical rerun)
**failed as stated** and was diagnosed: the failure is the cut protocol (above), not engine
nondeterminism; the fixed-tick control (A2/B2) is the corrected test. 7 (N-scaling, arm C) and
8 (encounters/dead recorded) below.

**What would make it wrong.** One seed (the ladder's), coast only (a burn at 3×10⁵ re-measures
the player-pull break, 625b's territory), the player at Home (in-band is d7e3/625b's measured
ruin), N = 3×10⁵ (this box's 2 GB/process rule; 10⁶ = 5.1 GB is M1 territory), five waves
measured (the shear trend past wave 5 is extrapolated; arm C extends to ~10). The rss metric
is Linux VmRSS against the ladder's macOS phys_footprint (~9% lower at equal B/body).

**Cost of adopting.** None: no code change is proposed for the engine. Two small protocol
notes — wave rungs cut at absolute ticks; long-flight certificates exist now (one command per
rung, ~140 s per 150 k game-s on this box). The memory lever for 10⁷ remains the compact store
(break 4), unchanged by this run.

**Fit with PRINCIPLES.** "Compute only surprises. Cost follows change" (§3): between waves the
engine holds nothing new — the step is the kick's price, not time's. "Errors never compound"
(§13): retention measured not to compound across waves. The test-ladder rule the record wrote
itself ("a rung must fly past *every* wave, not just the first", bf21) is now a measured fact.

**The lens (inversion).** I assumed the merge's claim ("only what is held per body grows")
inverted — that what is held grows with play — and tried to kill it five times over; the kill
failed at every instrument, which is the certificate. What the lens may have made me miss: the
N-axis (birth cost 2.4 KB/body — the compact store's territory, untested here), the player-axis
(in-band, burn: other runs' measured ruin), and the CPU axis at scale (the cadence law at 10⁷-10⁹
is a Fermi line, not a flight).
