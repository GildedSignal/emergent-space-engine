# Dossier — 20261018-1717-inversion-d839 (inversion)

**Claim.** The ladder's per-body memory wall is a constant, not a ratchet in play time: flown past a
full root-doll step for the first time (45,498 game-s, 2.3× the horizon of every prior wave flight),
the second full belt kick wave and the step-end boundary wave move footprint by +0.2–0.7% while
re-kicking every body, the compiled-orbit catalogue does not leak, and F1 holds at both waves.

**Bottleneck.** The board's top item (bodies 28 → 10⁹), memory term. ladder.txt's break 2 projects
"2.6 → 5.1 KB a body; 4 GiB at ~1.7×10⁶" from flights that end at 20,000 game-s — before the belt's
first kick wave even completes for the step, and two waves short of a repeated cadence. The inversion
question: does the per-body state keep growing with every cadence wave (memory ∝ play time, ruin at
wave count) or saturate? Answer: **saturates, measured** — the wall stands where the scoreboard says,
and one failure mode ("memory that grows with play", the lens's list) is retired for the per-body
history term on the flown domain.

**Evidence** (seed 1, coast, rtf 100, 12-ms budget, 1 thread; Linux/x86, load 0.3–0.7, 13.9 GB free —
`raw/state.txt`; instrument = shipped `nladder` + print-only patch: /proc footprint, `LADDER_CAP_S`,
a probe line every 300 frames = 500 game-s; engine state untouched, patch touches the example only):

| flight | game-s | waves crossed | RSS build→end | kicks | over 12 ms | max ms |
|---|---|---|---|---|---|---|
| N=0 (28 bodies) | 35,898 | — | →10 MB | — | 0 | 11.5 |
| 3×10⁴ | 35,898 | kick₁ 13.5–14.5k, boundary₁ 27.5–28.5k | 74→148 MB | 86,602 | 0 | 11.8 |
| 3×10⁴ | 45,498 | + kick₂ 41.5–43k | 74→**149** MB | 131,047 | 0 | 11.8 |
| 10⁵ | 35,898 | kick₁, boundary₁ | 238→477 MB | 156,602 | 0 | 11.96 |
| 10⁵ | 45,498 | + kick₂ 41–43.5k (+107k kicks) | 237→**479** MB | 271,047 | 0 | 11.97 |

- **The step's wave map** (`belt_first 30000`: belt first items 13,051–14,542, p50 14,071; locals
  21–5,289): the root doll steps the whole belt together — mid-step `What::Kick` wave, step-end
  `What::Boundary` wave ("the kick at the middle of a step and the boundary at its end", fleet.rs),
  next kick at ~2× the first. Wave₁: +30.5k (3×10⁴) / +99.9k (10⁵) kicks, RSS +66/+239 MB
  (+2.2–2.4 KB per body: 2,348–2,378 B at build → 4,790–4,963 B steady). Boundary₁: +25k events,
  ~0 kicks, RSS flat. **Kick₂: RSS +1 MB (+0.7%) at 3×10⁴, +1–2 MB (+0.2–0.4%) at 10⁵** while
  every body is kicked again. Dashboard bytes/body 1,379–1,417 throughout (it dips between waves).
- **Catalogue constant** (30,076 / 100,076 from gs 2,000 to the end): retire releases the old key,
  each kick compiles a fresh one — no per-wave leak (P3 held).
- **Mechanism, from the code, now flight-confirmed:** `Universe::prune`'s horizon is
  `(now − 2·light_distance − 2²⁶).min(oldest − 2²⁶)` with `oldest` the nearest pending item, so a
  binding retired at wave N is droppable ≫ one wave-gap before wave N+1; `BodyStore::prune` keeps
  exactly one retired segment. Steady state = 1 retired + 1 current per body. [INFERENCE beyond the
  flown two waves: the wave gap (13.7k gs) exceeds the keep window (~1.5–3k gs) by ~5–9×, so waves 3+
  ride the same path; strictly, two kick waves are flown.]
- **Determinism:** kicks 131,047 and every counter bit-identical across two executions of the 45.6-s
  arm (`raw/n30000_coast_456s{,_rerun}.log`).
- **By-products:** (a) the 20-s rung's per-body event rate (8.5e-6 ev/b/gs at 10⁶) under-reads the
  steady cadence ~11×: over a full step it is 9.79e-5 at 10⁵ (4.45 events/body per 45.5k gs = 2 kicks
  + 2 boundaries + the locals' share) — break 1's CPU arithmetic should use the step-inclusive rate;
  (b) coast holds nothing over 45.5k gs at 3×10⁴ (held_max 1) and 59 at 10⁵ with flat RSS — no mint
  pin on this scene (extends acf2's quiet-K finding to 45.5k gs).

**Predictions** (`predictions.md`, written before the decisive flights): P2 (saturation, the
decisive one), P3 (catalogue), P4 (wave-2 frames ≈ wave-1) and P5 (no coast pin) **held**. P1 held
on existence and timing of a second belt-wide wave but was **wrong in kind**: the 26.1–29.1k
concentration is the step-end boundary wave, not the second kick wave (which lands at 41–43.5k) —
the step's kick-mid/boundary-end structure was not in my model of the cadence.

**What would make it wrong.** A third wave that grows (unflown; the prune-window argument says no);
the burn flight at this horizon (unflown — the burning player mints 13.5× and changes the scan
channel, 2403; memory-through-waves under burn is the named next arm); N ≥ 10⁶ (the 10⁶ build alone
is ~2.4 GB, over this window's process cap — same wall 2403's checker hit); and any scene whose
`oldest` pins in the past (a body with a stale pending item would freeze prune's horizon — none on
this scene; a certificate on `oldest ≥ now − margin` would close that door).

**Cost of adopting: none** — this retires a fear rather than adding a mechanism. Fit with
PRINCIPLES: "A failed experiment kills that configuration, never the method" — here the
configuration (memory ∝ waves) is killed by measurement; and "Measure before claiming" — the 4 GiB
at 1.7×10⁶ projection is now flown, not projected (at one step of horizon; the M1 re-measure stands).

**The lens.** Inversion asked what makes the top bottleneck fail regardless of constants: the
time axis was the unflown one (every prior flight ended inside the first doll step). What this lens
may have missed: the horizon is still one step long in absolute terms (45.5k gs ≈ 0.6% of one
88-day Cinder period), so slowly-accumulating terms with periods above a step (secular drift
channels, the record's long-cadence entries) remain unexercised.

**Commands** (each ≤ 60 s here; full regen ≤ 15 min via `regen.sh`):
`LADDER_CAP_S=280 cargo run --release -p emergent-universe --example nladder -- 100000 coast 456 100`
and `cargo run --release -p emergent-universe --example belt_first -- 30000`.
