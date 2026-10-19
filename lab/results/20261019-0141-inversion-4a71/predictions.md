# predictions.md (written before the decisive flights; run 20261019-0141-inversion-4a71)

Question: does `Universe::prune`'s global `oldest` term (the min pending item over
planets/moons/player/ships, `universe.rs` `prune`) ever sit in the past on shipped scenes, and if
an item's light gap pins it there (a far doll's pending item), does the memory ratchet that d839
refuted ("a constant, not a ratchet in play time") resurrect?

Scene: shipped `nladder`, K = 3×10⁴ (d839's rung), seed 1, budget 12 ms; probe = print-only
(`/proc` footprint, per-game-second census of retired bindings, `now − oldest` gap) plus one
disclosed env-gated pin (`ES_PIN_OLDEST=D`: `oldest ← min(oldest, now − D)`, off = shipped bit
for bit). Waves on this scene: belt-wide kick waves ≈ 13.5k, 41k, 69k game-s (period ≈ 27.6k gs
= 5.6e9 ticks); keep = 2·ld + 2²⁶ ≈ 3e8 ticks ≈ 1,480 gs at the belt.

## Held-out cases and expectations

- **P1 (the certificate half), controls, not tuned on:** coast 70k gs (rtf 800), coast at the
  5 ms corner (the backlog arm: held in the hundreds), and burn through the SOI doll switch
  (frame ~948). Expected: max(now − oldest) ≤ ~2,500 s ≈ the belt's light diameter, **never
  growing with game time**, on every control — the horizon rule (presented time never passes an
  unresolved deadline) holds `oldest` within the widest pending light gap. Baseline census:
  control hist is a sawtooth, ≤ 1 generation above baseline outside a ~1,500 gs window after
  each wave.
- **P2 (the falsifier, the ratchet), pinned flights, held out:** D = 6e9 ticks (~1.1 wave
  periods) and D = 1.2e10 (~2.2): the staircase. Expected: retained generations at flight end
  ≈ 1 + ⌊D / 5.6e9⌋ per kicked body (control returns to baseline); hist_max control ≤ ~2,
  D=6e9 ≈ 3, D=1.2e10 ≈ 4; memory +2.2–2.4 KB/body ≈ +66–72 MB at 3×10⁴ per extra retained
  generation (d839's per-wave step), RSS climbing in steps that do not come back down while
  pinned.
- **P3 (the failure law at the goal's scale, arithmetic on measured constants):** one pending
  item whose light gap is D retains every body's history for D − keep; at the first
  interstellar doll (4 ly ⇒ D = 2.56e13 ticks ≈ 4,570 wave periods) that is ≈ 4,570 × 2.4 KB ≈
  11 MB/body — one far pending item multiplies the belt's standing memory ~4,500×. [INFERENCE
  from P2's measured per-generation constant; not flown.]

## Kill criteria (either fires = the letter changes)

- If any control flight shows now − oldest growing with play time (unbounded), the ratchet is
  already live without any pin — that replaces this run's whole letter (bigger finding).
- If the pinned flights show no staircase (hist bounded at the control's level), the horizon
  clamp is not the retention mechanism (the `prunable` calendar re-keying caps it instead) —
  the door is closed one level deeper than the horizon rule, and this run reports that
  mechanism.
