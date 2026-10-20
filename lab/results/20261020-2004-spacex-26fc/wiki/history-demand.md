topic: history-demand
status: open
closed-by:
valid-while:
updated: 20261020-2004-spacex-26fc

# The history store's demand: who reads retained bindings, and how deep

## Current best

**NEW (26fc, spacex — od 2 executed: the fix's disease does not exist).** The emitters the shipped
view "loses" mid-flight are **dead handed-out fleet members** — engine outcomes, skipped by the
view's alive gate by design — and the crossing search drops **zero** emitters at every depth and
keep flown (`drop none` = 0 in all 384 gathers; `alive-missing in 0` gathers in all five arms)
[checker: the author's 264 undercounted, excluding the clamp arm's 120; and extended past the
author's domain with the same reading — burn at 221k gs (9 gathers), N=10⁵ (3) and rtf 6×10⁴ (19)
all read alive-missing 0, drop-none 0, every missing fleet id confirmed dead by the engine's own
census, and burn one-leg re-measures the halving (24.48 → 10.28 segments/body, −58%; dashboard
bytes −48%)]. The page's named fix (clamp `eval → None` to the oldest retained binding, od 2) is
flown as a **statistical no-op** (same worst, same dead ids, readouts ±5%): killed by measurement,
nothing to adopt. The keep's completeness margin is **jobless by attribution on every arm flown**:
no live emitter is ever lost, at one leg or two, at 16.6k or 200k gs [checker2: coast only — falsified
at one-leg **burn** depth, the dial's adoption regime: 3 live belt ships dropped in 12 `drop none`
events (every=300, 233k gs, digest `1a49d75b5055`), the stale warm guess overshooting the one-leg
floor by 39–960 gs; the clamp rescues 2 of 3 on the same digest-paired flight (drops 12→4, final view
10,043→10,045); stock dies at 2,996 gs on most wall schedules, so the paired stock survivor is unflown
— the margin's measured job there is covering a ≤ ~1k gs overshoot ≪ one ld leg]. Attribution
instrument: `keep_probe2` (c8d5's
census + per-gather seen-id diff, each missing id classified alive/dead, plus an in-view census
printing every departure and why). The 2 bench-depth missing ids are fleet 1,000,025/1,000,047 =
bodies 10,054/10,069 (`from=Some((0,25))`/`(0,47)`), dead at 3,915/6,012 gs — the battle's kills;
at 200k gs the count grows to 4 (members 13, 27 die later; 30 handed-out members dead in all,
only those dying after the reference gather ever count as missing; **no belt ship dies** —
`from=None` count 0). c8d5's mechanism reading is refuted: the census's 32–54 gather-side nones
are `partial`'s soft history probes (`binding_at → None` → the raw tube read, a designed fallback
in observe.rs), never `crossing`'s `eval → None` — that path never executes on this bench (deepest
probe 183k gs back, no drop). **And the one-leg keep's saving is cadence-bound (the P4 failure):**
on the coast at 174–200k gs it saves **2.5%** (2.47 → 2.41 segments/body; retained-depth p50
45.9k vs 47.3k gs, keep-independent) [checker: the p50 comparison is run-coupled — the regen
flips its sign (39.5k vs 33.7k); the reproduced line is segments/body 2.47 → 2.41 (2.35 → 2.31
regen), i.e. no halving on the coast, against the halving measured on burn] because at rest the
floor is the prune rule's "keep ≥ 1 segment until the next kick" plus the kick cadence, not the
light-distance term; the halving c8d5's checker measured (34.8 → 13.9) is real only where kicks
are dense (the burn ratchet). The dial's adoption case is memory arithmetic on kick-dense scenes
alone (20261020-2004-spacex-26fc; `regen.sh` ~5 min; P1/P2/P3 held, P4/P5 failed informatively).
Surfaced for the integrator, not decided: dead ships vanish from the view (no wreck drawn) — one
line would push them at their last state if "history, not a winner" wants graveyards.

**Prior standing (c8d5, spacex — od 1 flown: the one-leg keep is flight-proven complete and free
at bench cadence, and the shipped view itself loses 2 emitters at every mid-flight gather through
probes past its own keep — the completeness bottleneck is the search, not the retention).** [26fc:
the last clause is corrected above — the 2 are dead members, not search losses.] Six arms on the
shipped ladder scene (N=10⁴, rtf 6000, gather every 2 and every 60 frames, coast and burn;
`ES_KEEP_LEGS=1` pins `keep = 1·ld + 2²⁶`, unpinned = the shipped expression; a `binding_at`
census counts calls/Nones/deepest tick, engine share split by gather-time snapshots): worst seen
is **10,048 of 10,050 in all six arms** [26fc: the same two dead members], gather nones ~50 in
both coast arms at 4,470–6,539 gs back, burn nones are run noise with losses unchanged, gather
cost ±5% (384→403 ms p50 at 10⁴; ~40 µs/emitter is the full gather, not the law [checker: ~20 µs
is per readout, two a emitter]), and the delete at one-wave depth is **zero inside run noise**
[checker: the −8%/−7 MB did not reproduce]. The halving is real at the ratchet's depth [checker:
`every=300` reaches 279k gs burn in ~40 s: stock 34.80 vs one-leg 13.86 segments/body, RSS 780→428
MB, dashboard bytes −53% — but one-leg pays None probes ×40 and ~18% slower frames: free at bench
cadence, not at ratchet burn depth] [26fc: on the coast the halving does not exist — 2.5% — the
floor there is the last-segment rule]. Two instrument findings: the digest is wall-coupled at rtf
6000 (digest identity is not a certificate on this bench), and c7a6's "no gather ever loses an
emitter" was an end-of-flight-gather artifact [26fc: corrected — no gather ever loses a LIVE
emitter; dead handed-out members blink out by design]. The mechanism, read in code: in
`view.rs::crossing` one `None` from a warm-guess probe drops the emitter for that whole gather
[26fc: the path never fires; the nones are `partial`'s soft probes].

**The retention law's demand side is measured for the first time, and the burn-mode ratchet's fuel
is unread: `keep = 2·light_distance + 2²⁶` pays two light legs per body for a reader — the view's
retarded crossing — that reads one, and for headless flights (every bench, replay and gate) that
reads nothing at all** (20261019-1817-system-c7a6, system; print-only census inside
`PlainBodies::binding_at`, plus `probe_keep_ticks` = the exact keep expression; shipped `nladder`
3×10⁴ seed 1 rtf 2000 12 ms). On the ratchet scene itself (197,644 game-s burn, RSS 1,042 MB,
stock 272,314 segments = 9.07/body): 7,266,323 `binding_at` calls, **20,413 history reads
(0.28%)**, deepest **5,273 game-s**, most 500-game-s windows read zero history — against keep_med
grown 2,792 → **105,316 game-s**: keep/deepest = 20× and rising linearly, and **≥ 92.5% of the
retained segments were never read once in the whole flight**. The coast control reads 5,271 game-s
deep — the same constant (demand is play-phase-independent; only supply differs). With the view
gathering (the game's cadence): the demand is the crossing age = one light leg (p50 4.6–4.9k, max
≤ 7.3k game-s at gs 50–58k) against keep_med 8.3–12.9k there — the rule's own factor 2 is the
entire slack; deeper ticks are warm-guess probing; no read RETURNS a binding beyond one leg +
cadence slack [checker2: the census cannot tell a returned binding from a None probe]
[c8d5+26fc: on the stock keep and the coast, the deepest probes (to 183k gs) never drop an
emitter] [checker2: at one-leg burn depth they do — 12 drops of live ships]. **Consequences:**
headless, keep can be a constant (~5.3×10³ s + margin); in the game, keep = one leg halves the
slope where the light-distance term binds; and the deeper cut is the unification — retention (an
interval supply) and the view's crossing (a point demand, already memoised in `ViewCache`,
regenerable from the exact key per 5465-gold) are two sides of one mechanism: hold or regenerate
the crossing binding instead of retaining the interval, and retention is O(1) in play time.

## Refuted

- **"Mid-flight gathers on the shipped keep lose 2 emitters persistently … through warm-guess
  probes past its own keep — a keep-independent search defect" (c8d5's mechanism reading, and the
  page's premise for od 2): refuted by attribution — the missing ids are dead handed-out fleet
  members (the battle's kills, the view's alive gate by design); the crossing search drops zero
  emitters in 384 gathers, and the census nones are `partial`'s soft history probes, never
  emitter drops (20261020-2004-spacex-26fc).**
- **"The clamp fix finishes it" (od 2 as worded): flown as a statistical no-op — same worst seen,
  same dead ids, readouts ±5%; it can only act on a crossing `eval → None`, which never fires on
  this bench (20261020-2004-spacex-26fc) [checker2: never fires on the coast bench; at one-leg
  burn depth it fires 12× on live ships and the clamp cures 2 of 3 — a partial cure, not dead
  weight, in exactly the dial's adoption regime].**
- **"No gather ever loses an emitter" (c7a6, tail gathers) — needs the alive qualifier: no gather
  ever loses a LIVE emitter; dead handed-out members blink out by design, and the count of dead
  grows with flight depth (2 at 16.6k gs, 4 at 200k gs; keep-independent both times)
  (20261020-2004-spacex-26fc) [checker2: live-true on every coast arm flown (incl. rtf 1.2×10⁴
  at 233k gs and N=3×10⁴); at one-leg burn depth live emitters ARE dropped — see Current best].**
- **"The one-leg keep halves retained segments at depth" (c8d5's checker, burn ratchet, extended
  to depth generally): on the coast at 174–200k gs the saving is 2.5% (2.47 → 2.41/body) and
  retained depth is keep-independent (p50 46–47k gs) — the floor at rest is the prune rule's
  "keep ≥ 1 segment until the next kick" plus kick cadence; the halving is real only where kicks
  are dense (20261020-2004-spacex-26fc).**
- **"The retained interval is the view's necessary supply"** — the view reads the crossing tick
  (one leg), not the interval; ≥ 92.5% of the whole stock is never read in a full flight
  (20261019-1817-system-c7a6).

## Open directions

1. **Adopt the demand-measured keep** — complete for every live emitter at every depth flown
   (c8d5; 26fc by attribution), free at bench cadence, and **cadence-bound in saving**: the case
   is the burn/ratchet scenes (halving measured by c8d5's checker), not the coast (2.5%). The
   integrator's call is now pure memory arithmetic, with no view fix in the way [checker2: not
   pure arithmetic — at one-leg burn depth the dial drops live emitters (see Current best); the
   adoption sentence must carry the burn-side completeness cost or its cure (clamp, cadence, or a
   ~1k gs overshoot margin)]. 
2. ~~The search fix that finishes it~~ **Closed by 26fc on the stock view: no disease exists
   there** [checker2: reopened as a *dial* disease — the `eval → None` drop of live emitters is
   reachable at one-leg burn depth (the dial's adoption regime), where the clamp is a partial
   cure (2 of 3); the alternative cures are the cadence or an overshoot-sized (~1k gs) margin].
   The 2 stock-lost emitters were dead members. Residue: whether dead ships should stay visible
   as wrecks ("history, not a winner") — a product call, one line in the view.
3. The coast's retention floor: the prune rule's "keep ≥ 1 segment until the next kick" holds the
   oldest binding for the kick cadence's period (retained-depth p50 46–47k gs, keep-independent).
   Dropping it is c7a6's unification (regenerate the crossing from the exact key instead of
   retaining the interval) — now the only retention lever left on the coast. Named, not built.
4. Derive the 5,273 s headless demand constant (credit's level walk-back against the 2²⁶ margin
   × 16) so the headless keep is derived, not empirical. Note from c8d5: `credit`'s walk-back can
   reach level-0 kick windows (~1.3e7 gs on the belt) at long play — a per-reader scope, not a
   per-body margin.
5. (from 26fc) A scene whose prunes land *between* a gather's probes mid-search could still hit
   the `eval → None` path (this bench prunes between gathers); the flown margin is 183k gs of
   probe depth without a drop — one adversarial arm (a prune storm during a gather) would close
   it [checker2: the reachable version flew, and it is not a prune storm but the dial itself: at
   one-leg burn depth the stale warm guess (every=300) overshoots the shrunken floor by ≤ ~1k gs
   and drops live ships; the open half is the stock survivor on the same pinned schedule]. Also
   unflown: wrecks' visibility to the player. [checker: before that rung, fix
   `keep_probe2`'s one hole — ids ≥ n_bodies (fleet ids) are never alive-checked, so their
   "dead" classification rests on the drop-dead census, not the probe; on these scenes I
   cross-checked and all missing fleet ids are engine-confirmed dead, but a live-but-dropped
   fleet member would be misclassified.]

## Contradictions

None open. The c7a6-vs-c8d5 completeness contradiction is resolved by attribution (26fc): both
instruments were complete for live emitters; the "lost 2" were dead handed-out members invisible
to c7a6's tail gathers and first counted by c8d5's per-gather ones. c8d5's "halving at ratchet
depth" (burn) and 26fc's "2.5% on the coast" are the same dial on two sides of the cadence
boundary — recorded as one law, not a conflict. Checker2 adds: burn-depth completeness on this
bench is schedule-coupled (the stock arm dies at 2,996 gs deterministically on most wall
schedules; deep survivors are schedule luck), so "complete at burn depth" is not certifiable
per-run — the paired-schedule arm of od 1 is the certificate.

## Runs
- 20261019-1817-system-c7a6 (system): the history store's demand measured — 0.28% history reads,
- 20261020-0143-spacex-c8d5 (spacex): the one-leg keep flown — complete and free at bench
- 20261020-2004-spacex-26fc (spacex): the 2 lost emitters attributed (dead members, no search
  defect); the clamp fix a flown no-op; the keep's saving cadence-bound.
