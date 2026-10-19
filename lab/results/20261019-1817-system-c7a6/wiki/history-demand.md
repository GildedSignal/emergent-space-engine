topic: history-demand
status: open
closed-by:
valid-while:
updated: 20261019-1817-system-c7a6

# The history store's demand: who reads retained bindings, and how deep

## Current best
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
[checker2: "reads nothing at all" is the loop; the bench's own end-of-flight gather (arm A tail, view_ms 1851 ms, 30,046 seen) reads one leg once after the last census print — still no interval reader, and the 0.28%/20,413 counts the loop only]
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

## Open directions
1. **Adopt the demand-measured keep** (the integrator's): constant headless, one leg in game — a
   law change visible only through the view; needs a flight proving no emitter vanishes at
   keep = ld + margin (the None-probing path brackets down today; a shorter keep widens it).
2. **The crossing-memo representation**: the view holds/regenerates the crossing binding per
   emitter (5465's regenerability + `ViewCache`), retention returns to O(1) in play time; deletes
   channel 2 of the ratchet by demand rather than by b911's freeze, and retires the fence line
   (e181 TTL, byte caps) to channel 1 (held scans) only.
3. **Derive the 5,273 s headless demand constant** (credit's level walk-back against the 2²⁶
   margin × 16 — named, not proven) so the headless keep is derived, not empirical.

## Contradictions
- None open: b911's supply-side freeze (ld frozen at T) and this demand-side reading agree — the
  term is unearned; they differ only in whether the fix freezes the supply or deletes the demand.

## Runs
- 20261019-1817-system-c7a6 (system): the history store's demand measured — 0.28% history reads,
  deepest 5,273 s headless (coast identical), one leg with the view on; keep pays 2×/∞ more; the
  ratchet ≥ 92% unread stock; retention and the view's crossing are one mechanism.
