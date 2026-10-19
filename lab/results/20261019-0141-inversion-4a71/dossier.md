# dossier — 20261019-0141-inversion-4a71 (inversion lens)

**Claim.** `Universe::prune`'s global `oldest` term is closed at one star only by the horizon
rule's own geometry — `now − oldest` equals the widest pending light gap (2,302.5 s measured,
flat in play time) — and the memory ratchet it guards against is real and priced: any pending
item whose light gap exceeds the local keeps staircases memory at +1 retained generation per
body per 27.6k gs (~2 KB per retained binding) while also eating the frame; at the goal's first
interstellar doll (4 ly) one pending item is ~9.2 MB/body by the measured law.

**Bottleneck.** Board item 1 (bodies toward 10⁹) and 4 (memory at 10⁹): the memory wall's
"constant, not a ratchet" (d839, the page's standing current best) holds **only while every doll
sits inside one light diameter**; the retention horizon couples every body's memory floor to the
single oldest pending item in the universe. Expected gain: deletes the false safety and names
the one-line scope decision (global min → per-body oldest) before the E9 far-system wiring
lands on top of it.

**Evidence** (shipped `nladder`, K = 3×10⁴, seed 1, budget 12 ms; probe = print-only — `/proc`
footprint for the macOS call, per-2,000-gs census of retired bindings and `now − oldest` — plus
one disclosed env-gated pin `ES_PIN_OLDEST=D` in `prune` (`oldest ← min(oldest, now − D)`),
off = shipped bit for bit; rtf 800 for the long arms, 100 for the corner/burn arms; deterministic
counts, timings indicative only. Reproduce: `regen.sh`, ~4 min. Logs in `logs/`, folded by
`analyze.py`.)

| arm (coast unless said) | pin D (ticks / gs) | max now−oldest (s) | peak retained (per body) | hist_max | bpb end | RSS end | frames >12 ms | held max |
|---|---|---|---|---|---|---|---|---|
| ctrl 77,399 gs | — | **2,302.5** | 31,983 (**1.02**) | 69 | 1,417 | 155 MB | 6 | 153 |
| ctrl, 5 ms corner | — | **0.0** | 649 (0.02) | 24 | 1,211 | 80 MB | 4 | 1 |
| ctrl burn (SOI switch, held 286) | — | **0.1** | 1,408 (0.05) | 775 | 1,211 | 98 MB | 0 | 286 |
| **negative**: D = 2²⁶ (331 gs < the natural gap) | 6.7e7 | 2,302.5 | 30,981 (1.03) | 69 | 1,420 | 154 MB | 3 | — |
| pin 72,567 gs | 6e9 / 29,553 | 29,552.9 | 87,920 (**2.93**) | 1,447 | 1,738 | **279 MB** | **383** | 204 |
| pin 66,457 gs | 1.2e10 / 59,106 | 59,105.9 | 151,338 (**5.04**) | 2,878 | 2,222 | **384 MB** | **683** | 178 |

- **The certificate (controls):** `now − oldest` never grows with play time — max 2,302.5 s
  over 77k gs (≈ the belt's light diameter; the probe's per-tick gap reads 0.0 except in the
  wave bursts), 0.0 s at the 5 ms corner, 0.1 s under burn through the held-286 backlog.
  Structural reason, verified in code: presented time is the horizon (`now ≤ every unresolved
  deadline − 1`, `advance`), and every pending item's deadline is `event + its light distance`
  (`deadline_of`), so `now − oldest ≤ max pending light gap` **always**. The control's census
  reproduces d839's digits (steady 1.02 retired/body, bpb 1,417 after kick₃, RSS 155 MB).
- **The falsifier (pins), the ratchet resurrected:** retained generations ≈ 1 + window/27.6k gs
  per body (2.93 at window = 1.07 periods; 5.04 at 2.14 — the excess over 1+⌊W/P⌋ is the
  mid-step kick structure and birth, disclosed); RSS staircase 155 → 279 → 384 MB = **+1.9–2.2 KB
  per retained binding**; unbounded while pinned (the series climbs at every wave: 41k → 95k →
  113k → 130k → 151k retained at D = 1.2e10), and the pin eats the frame too: over-budget frames
  6 → 383/683, game time −6%/−14% (pinned bodies come due every frame; `prune` walks them and
  drops nothing). The negative control (D below the natural gap) is byte-identical to control —
  the knob is inert unless the pin is real.
- **Instruments:** dashboard bpb under-counts the ratchet ~12× (+321 B/bpb against +124 MB at
  3×10⁴): RSS and the census are the instruments (d839's checker's caution, now quantified).
  `hist_max` 69–775 even in control: the locals accumulate generations; bounded in total.

**Predictions.** `predictions.md`, written before the flights: P1 (bounded gap, ≤ ~2,500 s,
never growing; held backlog does not pin) **held** on all three controls; P2 (staircase
≈ 1 + ⌊D/5.6e9⌋, ~2.2–2.4 KB/generation, no return while pinned) **held** with one disclosed
miss (measured generations run ~+1 above the floor formula: the mid-step kick structure); P3
(the 4-ly arithmetic) stands as [INFERENCE] on the measured constants. Neither kill criterion
fired.

**What would make it wrong.** The pin is simulated: no far doll exists on the plane (`range`
refuses past ~6 AU), so "a real far item pins `oldest` for its whole light transit" rests on (a)
the measured horizon-rule mechanism (shipped code, both halves measured) and (b) the assumption
that E9's far systems schedule items into `ship_ticks`/the few-walk the way system bodies do. If
far dolls hold their ships out of `ship_ticks` (the `waiting`/`child_ticks` split), the global
min never sees them and the door stays shut — the certificate would then be "oldest reads only
near dolls", checkable the day far-system wiring exists. The per-generation byte constant and
the wave law are measured on this box, this scene.

**Cost of adopting.** The fix is the oldest term's scope, not the margin: per-body oldest (only
items that can read body i — its own items and its encounter partners — hold its history),
which the radial index and encounter tiers already know; the global min is over-conservative by
the ratio of widest to local light gap (~1 at one star, ~10⁵ at 4 ly). No adoption before a
far-doll arm exists; nothing to wire today. Fit with PRINCIPLES: "Nothing past c … it allows to
cheaply partition compute, even gravity is light speed" (OCC#10) — the same light cone that
partitions compute must partition *retention*; and "a failed expectation is not automatically a
failed method" — d839's constant is right inside its domain, which this run measures the edge of.

**The lens.** Inversion asks how the standing result fails: I took the page's own newest
headline ("a constant, not a ratchet") and its named-unflown falsifier, and flew the falsifier.
What the lens may have missed: everything the pin is NOT — the far-doll wiring, the E9 fleet
battle channels (`slice` items), and whether `waiting`/`child_ticks` already exclude far ships
from the global min (the one cheap code check a checker can do against `requeue`/`rekey`).
