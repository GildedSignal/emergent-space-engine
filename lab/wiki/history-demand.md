topic: history-demand
status: open
closed-by:
valid-while:
updated: 20261020-0143-spacex-c8d5

# The history store's demand: who reads retained bindings, and how deep

## Current best

**NEW (c8d5, spacex — open direction 1 flown: the one-leg keep is flight-proven complete and
free, the delete is small at one-wave depth, and the shipped view itself loses 2 emitters at
every mid-flight gather through probes past its own keep — the completeness bottleneck is the
search, not the retention).** Six arms on the shipped ladder scene (N=10⁴, rtf 6000, gather
every 2 and every 60 frames, coast and burn; `ES_KEEP_LEGS=1` pins `keep = 1·ld + 2²⁶`, unpinned
= the shipped expression; a `binding_at` census counts calls/Nones/deepest tick, engine share
split by gather-time snapshots): worst seen is **10,048 of 10,050 in all six arms** — the same
two emitters missing in stock and one-leg alike (losses 112/105 coast, 3/3 sparse, 74/75 burn),
gather nones ~50 in both coast arms at 4,470–6,539 gs back ≈ 4× a belt leg (past even the
shipped 2·ld + 2²⁶, so the dial cannot lose what stock already loses), burn nones are run noise
(12→262 author, 183→0 regen) with losses unchanged (the None path is noisy, not lossy),
gather cost ±5% (384→403 ms p50 at 10⁴; ~40 µs/emitter is the full gather, not the law
[checker: ~20 µs is per readout, two a emitter]), and the delete at one-wave depth is **zero
inside run noise** [checker: the −8%/−7 MB did not reproduce — the regen coast flips to +9%
(stock 2.16 vs one-leg 2.35 body⁻¹; stock alone spans 2.16–2.41 across runs), and the N=3×10⁴
and 184k-gs coast arms read 0% with the RSS sign flipping]. The halving is real at the ratchet's
depth [checker: flown — `every=300` reaches 279k gs burn in ~40 s, so "unreachable in 60 s" was
wrong: stock 34.80 vs one-leg 13.86 segments/body, RSS 780→428 MB, dashboard bytes −53% — but
one-leg pays None probes ×40 (72,236 vs 1,795) and ~18% slower frames (truncated where stock
finished): free at bench cadence, not at ratchet burn depth].
Two instrument findings: the **digest is wall-coupled at rtf 6000** (same binary, same
args: `f94f69c387b0` then `20a606853bd4` in-session; `regen.sh`'s `stock_coast_again`
reproduces; checker: stock@16,455 gs and one-leg@16,455 gs share digest `f94f69c387b0`
across arms and runs — the dial is engine-neutral at a fixed tick): the presented tick
follows the 12 ms wall budget, so digest identity is **not**
a certificate on this bench; engine census nones 0 coast at N=10⁴, 2 in burn both arms, site
unattributed [checker: at N=3×10⁴ coast the engine itself nones 10–12 — the 0 does not extend
with N]), and c7a6's "no gather ever loses an emitter" was an end-of-flight-gather
artifact — **mid-flight gathers on the shipped keep lose 2 emitters persistently at 16k gs, and
the count grows with depth (4 at 184k gs coast, 4–5 at 240–280k gs burn — keep-independent
there too; identity still unattributed)** (the
mechanism, read in code: in `view.rs::crossing` one `None` from a warm-guess probe drops the
emitter for that whole gather). Next one experiment: attribute the 2 ids, then clamp `eval →
None` to the oldest retained binding instead of dropping the emitter (20261020-0143-spacex-c8d5;
`regen.sh` ~6 min; predictions P1/P3/P5 held, P2 failed on depth, P4's kill-side control failed
to kill because stock itself fails).

**The retention law's demand side is measured for the first time, and the burn-mode ratchet's fuel
is unread: `keep = 2·light_distance + 2²⁶` pays two light legs per body for a reader — the view's
retarded crossing — that reads one, and for headless flights (every bench, replay and gate) that
reads nothing at all** (20261019-1817-system-c7a6, system; print-only census inside
`PlainBodies::binding_at`, every call counted and site-tagged, plus `probe_keep_ticks` = the exact
keep expression; shipped `nladder` 3×10⁴ seed 1 rtf 2000 12 ms, f80a's arm class). On the ratchet
scene itself (197,644 game-s burn, RSS 1,042 MB, stock 272,314 segments = 9.07/body — the wave
saturation reproduces, first wave gs 13.8–14.8k; f80a's 8.03/body at 174k is its own rtf-1000
digit, cadence-coupled — this run reads 7.01 at 174k): 7,266,323 `binding_at` calls, **20,413
history reads (0.28%)**, deepest **5,273
game-s**, most 500-game-s windows read zero history — against keep_med grown 2,792 → **105,316
game-s**: keep/deepest = 20× and rising linearly, and **≥ 92.5% of the retained segments were
never read once in the whole flight**. The coast control reads 5,271 game-s deep — the same
constant (demand is play-phase-independent; only supply differs). With the view gathering (the
game's cadence): the demand is the crossing age = one light leg (p50 4.6–4.9k, max ≤ 7.3k game-s
at gs 50–58k) against keep_med 8.3–12.9k there — the rule's own factor 2 is the entire slack;
deeper ticks are warm-guess probing (a stale `ViewCache` guess evals past the crossing, gets None
on pruned history, brackets down — demand-shaped, not law-shaped; at one gather per frame the
slack is one frame) — and probe ATTEMPTS do read past two legs without returning a binding
(arm B: 93.4k gs against a 45.6k leg; the checker's coast+view arm: 17.8k against a 3.15k
lawful leg, every gather still delivering all 30,046 emitters): no read RETURNS a binding
beyond one leg + cadence slack
  [checker2: the census cannot tell a returned binding from a None probe, so "returns" is inferred, not counted; what is measured is that no gather ever loses an emitter — all 30,046 at 3×10⁴ and 100,048 at 10⁵ (my coast+view arm) delivered every gather, at 10⁵ with census keep_over_demand 0.3×, i.e. keep already below the deepest attempt]
  [c8d5: that completeness held only for the bench's tail gathers — mid-flight gathers on the same
  shipped keep lose 2 of 10,050 emitters at every gather past ~frame 76 (N=10⁴, rtf 6000), the
  probes 4× a belt leg deep: past both keeps, hence keep-independent; see the block above]
adds no retention. **Consequences:** headless, keep can be a constant (~5.3×10³ s + margin) and
channel 2 of the ratchet is deleted with no observable change (prune is forget-only; b911's
stronger freezes were already digest-neutral); in the game, keep = one leg halves the slope; and
the deeper cut is the unification — **retention (an interval supply, O(c·t) per body) and the
view's crossing (a point demand, one tick per body per frame, already memoised in `ViewCache`,
regenerable from the exact key per 5465-gold)** are two sides of one mechanism: hold or
regenerate the crossing binding instead of retaining the interval, and retention is O(1) in play
time — the f80a/e181/527a fence line becomes unnecessary for channel 2. The one hard case the 2×
plausibly guards: gravity-as-news (law.md, designed, not built) reading a source at t − ld(i,j),
whose antipodal worst case reaches ld(i)+ld(j) — when that reader exists its margin belongs keyed
to the pair distance, not paid by every body forever; today's engine has no two-leg reader (the
census counts every `binding_at` call in the process).

## Refuted
- **"The retained interval is the view's necessary supply"** — the view reads the crossing tick
  (one leg), not the interval: each gather touches ≤ 6 of a body's ~9 retained segments' worth of
  reads at one tick region, and ≥ 92.5% of the whole stock is never read in a full flight
  (20261019-1817-system-c7a6).
- **"No gather ever loses an emitter" (c7a6's checker, tail gathers)** — mid-flight gathers on
  the shipped two-leg keep lose emitters persistently (2 of 10,050 at 16k gs; 4 at 184k gs
  coast; 4–5 at 240–280k gs burn [checker] — the count grows with depth), every gather past
  ~frame 76, through warm-guess probes past both keeps; keep-independent (the same count is
  lost at one leg and at two; identity unattributed) (20261020-0143-spacex-c8d5).

## Open directions
1. **Adopt the demand-measured keep** — flight-proven complete at every depth flown (c8d5;
   checker to 279k gs burn, N=3×10⁴) and free at bench cadence. What remains is the
   ratchet-depth cost [checker: at 279k gs burn the halving is real (34.8→13.9 segments/body,
   RSS −45%) but one-leg pays None probes ×40 and ~18% slower frames] and the integrator's
   call: the one-wave-depth saving is ~0 [checker: −8% was run noise], the halving is c7a6's
   argument now measured — with that cost attached.
2. **The search fix that finishes it:** in `view.rs::crossing`, one `None` from `eval` drops the
   emitter for the whole gather — clamp to the oldest retained binding instead (the probe was
   below the crossing anyway) and the 2 stock-lost emitters come back; then the keep's margin has
   no completeness job left at all (c8d5, next experiment; attribute the 2 ids first — if they
   are fleet members pushed without a crossing search, the mechanism is misread).
3. The crossing-memo representation (c7a6's deeper cut): unchanged, unflown.
4. Derive the 5,273 s headless demand constant (credit's level walk-back against the 2²⁶ margin
   × 16) so the headless keep is derived, not empirical. Note from c8d5: `credit`'s walk-back can
   reach level-0 kick windows (~1.3e7 gs on the belt) at long play — a per-reader scope, not a
   per-body margin.

## Contradictions
- One open, resolved by domain: c7a6's checker measured every gather complete (tail gathers,
  warm cache, end of flight); c8d5 measures 2 emitters lost at every mid-flight gather (per-frame
  cadence, rtf 6000). Same engine, different instrument points — the difference is the cadence
  and the cache's staleness, not a disagreement about the law.

## Runs
- 20261019-1817-system-c7a6 (system): the history store's demand measured — 0.28% history reads,
- 20261020-0143-spacex-c8d5 (spacex): the one-leg keep flown — complete and free at bench
