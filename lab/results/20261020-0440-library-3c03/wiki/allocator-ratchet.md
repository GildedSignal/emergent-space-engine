topic: allocator-ratchet
status: open
closed-by:
valid-while:
updated: 20261020-0440-library-3c03

# The allocator's rollback feedback: a one-way ratchet on the forecast margin


**NEW (3c03, library — da23's survivor instrumented; site corrected by the checker, see
below).** The surviving fire's published `fin_hi` is never a finality decision on the
gated 8704 battle class: it is inherited publication minted onto a fresh id with no
alone-ness check, right when rollbacks leave live truths below the mint tick — **but the
mint is the ROLLBACK RESTORE (`make_region` at alloc.rs:1480 over `union_parts`), not
`regroup`: 7 of 8 pooled fires (author 3/4, checker 4/4) show `why=[""]` with one donor
part, each immediately preceded by `RB lid=<donor> s0=<mint tick>` restoring exactly that
donor at exactly the fired region's `verified` — the restore is the one mint site the
instrument does not label, so the author read these as merge-mints; one fire
(`why=["merge@864"]`, three donors) is a genuine regroup mint.** Proof: the `merge` note
is unconditional for fresh regroup ids and cannot drain (newest entry, fire follows within
lines); a single-member regroup reuses its id; `make_region(Some(fin))` has exactly two
callers (regroup instrumented, restore not). da23's (a) radius and (b) staleness stay
excluded on the gated 8704 class: **0 DECIDED lines on the gated arms** — but NOT "every
arm": the shipped arm decides (91 in the author's own `s19.a0`, self-truth only; quiet
514), and at galaxy 12288/36 gate 1 the alone path decides again (8/draw, two of them
single-member groups publishing past foreign truths starting 512 at t=656 — 3c03's
predicted ids-empty hole (d) is live at the next scale, so truth-ids is inert only at
8704). Arms (one build, paired interleaved, s19 protocol): gate v2 **3 fires/10** author
window, 2/3 checker; +truth-ids equal to gate v2 at 8704 (0/10 author window, 1/3 checker
under load — clean was NED, not END; the inversion is measured);
+`merge_gate` (defer a regroup whose slack-grown union hull touches any live truth
starting below the mint's publication tick) **0/13 fires and no fix**: 42 DEFERs/draw
flat (13/13 draws; the dossier's "42–168" regenerates as 42), merges 11→0, regions
23→23, present 1792→538 (the no-conflict floor), final lead pinned 0 — and since the
fatal mints were restores, the gate never touched the mechanism it was credited with
killing: the 0 fires is the starvation, doubly confounded. **The fix direction: cap
inherited publication at the touchable truths' floor and make the mint inherit its
members' live truths at BOTH mint sites (restore and regroup), never defer the merge.**
Churn class (gas, min_region 1): present 1024 identical on arms 0/1/3 (weak control —
single region; 01e7's selfchurn protocol still da23's open P4). Tests 14/0 with all
switches in (20261020-0440-library-3c03, library; ES_FIRE_WHY instrument over da23's
patch, arms 0/1 byte-identical; regen ~4 min; 4,590 highlights fetched fresh, 5/5 quotes
byte-identical; predictions P1/P2/P4 refuted on the letter, P3 moot, P5 held weakly).
Checker: lead — the headline (regroup mint) is contradicted by the author's own kept
logs; the corrected pin is the checker's, from those same logs.

**NEW (da23, taleb — direction 1's first measured candidate: the stride gate built and
flown).** `Config::stride_gate` (off by default, one build both arms) gates finality in
`alone_at`/`final_through` three ways: reach boxes grown by one stride's light travel
(v·(stride_max+1)·window, the same hull bound e517's HAZ projects), no skip at `fin ≥ t`
(a restored/merged giant carries final parts above its `verified` — c749's violated region;
it now projects its live stride hull and current rmax), and every certified truth with
`start < t` coalesced as an ids-empty pseudo-member (finality had never read the truths
table). **On the battle fire protocol (galaxy 8704/24, margin 0.5, 8 seeds, one hot window):
fires 7/8 shipped → 1/10 gated** (the survivor is the s19 class, D=32, a certified truth
from 944 against fin_hi 976); clean gate draws keep the equality law (every RB m ≤ 0),
finish (regions →1), present 1280-1536 vs 1792-2128 shipped-clean (~15-40% cost), final
lead 64-96 (>0, no publication livelock). Gate v1 (first two parts only) fired 1/8 — its
fire exposed the giant-skip hole, killed as a configuration (#9), not the method. The
churn class (gas min_region 1) was NOT flown: starvation there is untested (e517's cost
note stands). The survivor names the next experiment: pin whether truth-hull radius,
finalize-round base staleness, or a merge path raising fin_hi without a decision (da23).
  [Checker da23: reproduced in kind, not in magnitude — the fire counts and the 15-40% cost
  are hot-window numbers. Regen (quieter): shipped 1/8, gate 1/11; per-seed present differs
  ≤ ~14%, often ~0. Paired same-seed same-window blocks: regen s11 shipped FIRE D=48 / gate
  clean; checker s25 shipped FIRE D=80 / gate clean. The survivor is deterministic — PRE
  D=(32,44,944) → FIRE id=52 s0=944 fin_hi=976, state-identical in the author's window and
  the regen. P4 churn flown by the checker: no starvation (present equal, 0 fires). Adverse:
  under 8-way crush every gate draw at final lead 0 and 1/14 near-stalled (present 72 vs 529
  shipped same seed+window, finality pinned F=32) — the disarm channel the gate needs is
  load-coupled on the battle class too.]
**NEW (c749, dynamics — od 5's named next step done: the fire's internal state on the
game's own fleet battle, e517's instrument verbatim on bf83's harness).** Six fires
pooled over two executions whose incidence moved with the wall clock (execution 1: 3/8
at galaxy 8704/24 fleets margin 0.5, 0/6 at 4352/12, 0/2 at margin 2.0, replicates of
fired seeds clean; execution 2: 2/8 at 8704, 1/6 at 4352 — a seed of bf83's 4/62 class)
— **every fire state-decided at certify: PRE's D equals the assert's own violation
exactly (6/6, violations 16–96 chronons = 1–6 windows, s0 exact), and the last pre-fire
HAZ armed pair names the fatal clash (exact 4/6; same lineage, identical margins 1/6 —
a split moved the busy id; publish-blind 1/6: regen g8704_s23's fatal pair 53↔36 at
s0 704 never appears armed at its own margins (lineage 36 armed only earlier, A = 112–256
at s0 256, resolved) — e517's
soundness note made a measured fact: the A ≤ 0 publish-side certificate misses fires;
D at certify is the complete decider, so the fix must gate certifies, not
publications).** The violated region is in every case a merged giant descendant of the
armed pair (bbox 302–2553 units wide, not fleet-scale), carrying the closure's max
fin_hi over an old stride's start — the identity to watch is PRE's box. Containment
holds under the battle's real merge/split topology: `out=` empty and mo = 0 on all 267
RB lines, fires included. m > 0 ⟺ fire (6/6 fatal, 261/261 non-fatal at m ≤ 0). **But
two halves of e517's churn record do not transfer: 94/261 non-fatal restores land
strictly inside the boundary (record execution m ∈ [−432, −48], median −224 —
"publication rides the boundary" is the churn scene's property, not the law's), and at
the shipped default margin 2.0 the battle stays armed at over half its publishes yet
rolls back zero times — the planner absorbs every meeting (the fire is a margin ≤ 0.5
exposure, bf83's reading confirmed from inside the state).** Shared-instrument caveat:
PRE/HAZ are e517's code; this run's independence is the different scene family, the
moved incidence, and the m < 0 finding contradicting the shared instrument's earlier
record (20261018-0932-dynamics-c749).**
**(Checker c749: law reproduced with an independent parser on two further executions —
11 fresh fires, every one D = violation exact with s0 exact, `out=` shut on 419 RBs
total, non-fatal m ≤ 0 with no exception; fires are the shipped assert itself
(alloc.rs:1499, exit 101). The stated ranges are observations, not bounds: violations
to 192 (12 windows) and fire bboxes to 3,384 units measured on regen. Publish-blind
confirmed operationally: 2–13 fully quiet publishes (A ≤ 0 at every pair) before each
blind fire, one (margin 0.25) whose fatal pair appears in no armed line at all.
Adversarial: min_region 8 holds containment (161 RBs, out= shut); galaxy 12288/36
fleets 0/4 fires — incidence is not monotone in scale.)**
**NEW (e517, second author on fd35 — the positive side reproduced, direction 7 closed
both ways):** the finality assert's FIRING is a pure state property at certify time.
On 01e7's selfchurn harness (finpol) with fd35's print-only instrument plus one field
(`out=`: affected ids outside the clash lineages' descendants), 18 protocol draws
(seeds 11–19 × 2 replicates, frames vmax 2, rate 600) gave **9 fires, and every one
was decided exactly by PRE's D**: the fatal clash's `D = 16 = fin_hi − s0` preceded
every FIRE (9/9, in 7/9 on the immediately preceding line), while all 2,286
non-fatal realized clashes sat at D = 0 (m = 0) — zero exceptions on realized
clashes. (Checker: PRE `D > 0` without fire is NOT excluded in general — it is the
armed state; at window 32 it is common, 114–116 `D = 32` lines per draw with 0
fires. The law is: fire ⇒ D = violation on the fatal pair; realized non-fatal ⇒
m = 0.)
**Armed precedes fire** (fd35's P5, the named experiment): every firing draw shows
HAZ `A > 0` from publish 8–12 (presented t = 0.41, scene start) — an armed lead of
the whole scene start (~32 chronons, 51–449 publishes). Violations on this family
are exactly one window (48−32 scene start; s13 twice at 96−80, bc0f's late reclash
phase); the checker's vmax-8 late-reclash fire measured viol = 48 = 3 windows at
s0 = 1376 (D = viol still exact) — the invariant is D = viol, not one window.
**The sibling-closure hole never opens**: `out=` non-empty on 0 of 2,295 RB
events (mo = 0), fires included — rollback's union-find `affected` coincided with
PRE's descendants closure on every realized clash, which is why D never misses
(containment); its exactness is the measured equality, with the derivation still
open (direction 7).
**Armed ≠ incidence**: all 9 survivor draws were armed too (95–99% of their
publishes; fired draws 85–99%) without firing — armed is the possibility state;
whether a clash realizes on an armed pair stays the wall-clock race. Cost note for
the fix: on this family a hold-while-armed rule refuses publication for essentially
the entire scene start on every draw — progress needs the disarm channel (truth
aging/pruning, the h_nosab episode's resolver), not refusal alone.
Regeneration fixed: fd35's regen
`h 0` sabotage trap (now `sab x` → None: the armed episode regenerates, 15 armed
publishes to A = 128, rb = 0) and its relative-path analyze bug; equality-law churn
arms rerun under the e517 patch unchanged (579/541 rollbacks — schedule-moved, all
D = 0, never armed). Certificate soundness note: the D ≤ 0 half decides the assert
on its own (it mirrors certify's own scan; exact when out = empty — measured
everywhere); the A ≤ 0 publish-side half misses only strides dispatched between
publishes, which D still covers at their certify.
Checker extension (same invariants, wider domain): the batch driver fired 4/9
(viol 16 = D exact, armed from publish ~20 with ~240-publish leads, `out=` shut)
and the crossing family, window 8/32 and seeds 21/23 held the equality law with
2,632 further RB events, `out=` never opening.

**NEW (bf83, inversion — direction 5's first half answered on shipped code, unsabotaged):**
the game's own scene shapes are separable by fire: the FLEET battle (lattice `worlds::galaxy`,
12 power-law fleets, `Law::Relativistic`) fires the finality assert on main at protocol
(1 fire / 14 draws, seeds 11-16 × 2, rate 2400, 4.5 s ≈ present 3.5k-10.8k; `min_region 32`
shipped, `speed_margin 0.5`, sabotage off; seed-11-skewed with a replicate split — the
wall-clock race), while the belt's shapes stay clean: a churny 3×3 bounce clump grid 0/12
(9-27 rollbacks, final lead to 1,504 at `min_region 1`), cold Pass crossing trains 0/6
(10-12 rollbacks — crossings conflict without contacts — no fire at this horizon; bc0f's
crossing crash lives in other windows), and one dense slow gas
blob 0/6 at 135-171 rollbacks with final lead 0. **The two-ingredient law: fire needs light
slack (publish-ahead) AND an unplanned meeting; churn alone is inert** — the page's crash
family is gas-shaped, but gas without slack cannot fire at all, so the fix's test scene
should be converging fleets, not gas. At the shipped default margin 2.0 nothing fires (0/6
battle; gas conflicts fully absorbed), and margin 0.0 — the shipped finality tests' value —
degrades sharply at `min_region 1` (present 8,355→~3.1-4.7k, rollbacks 0→~256, regions to
~2.3k on the author's draw) but never stalls in three checker replicates — the chronon-3
stall was one draw, not a law. Harness:
`crates/allocator/examples/exposure.rs` (the run's only code change; one process per draw;
fire = exit 101 + the assert message). Checker-measured since (gold check): 3 further fires
in 12 fresh battle draws, all seed 11 (0 on ~40 draws of seeds 12-24; pooled 4/62 at margin
0.5), one at a 4x horizon (20 s, present ~15k); fires are load-coupled (0/8 in a quiet
loop, 0/53 in the runner's regen); rate 600 is the keeping-up rate (present pinned at
2,698, lead ~240, 0/12 — the axis is dead). Checker2 (independent): fires are not
seed-11-specific — s19 fired 1/6 at 4352, and the first N rung above the author's range
(galaxy 8704, 24 fleets, span 12, margin 0.5) fired 2/4, both with the exact assert
(fin_hi 1232 vs s0 1216): incidence rises with the battle's scale, the direction the 10⁹
game cares about; gas margin-0.0 never stalled in 3 further replicates (present 3.9-4.7k,
rb 247-254, regions 512→1), and rate-600 gas under load gives final lead 0 (present
1.2-1.7k), so the keeping-up lead is machine-load-coupled. Still unmeasured: the fire's internal state
(no fin_hi/PRE instrument; e517's instrument on the fleet scene is the named next step).

**The state side (fd35, direction 7 answered, now with its positive half):** the
race is measurable as a state property on shipped code, and on every draw flown it
sits exactly on its boundary. A print-only instrument (HAZ at every publish: max
published `fin_hi`, deepest live truth start `S`, per-pair armed margin A over
in-flight stride reach hulls × live truths; PRE before every certify with the
measured box: the D the upcoming clash would restore; RB/FIRE inside rollback: the
exact assert inputs) shows: **the equality law — all 8,213 realized clashes across
45 arm-processes restore at exactly `fin_hi == s0`** (min D = max D = 0, every RB
margin 0): finality's coalescing and the certificate's separation pin the same
contact tick, so publication rides the boundary as an attractor, never past it and
never behind it. **The armed episode** (dispersal probe, sabotage truly off: 17
armed publishes to A = 192, several episodes, every one resolved by disarm at
rb = 0 — checker's rescue, now the regen line) — the race has two resolution
channels, conflict (fires iff armed > 0 at contact) and pruning. **The negative
certificate:** armed ≤ 0 at every publish AND D ≤ 0 at every certify ⇒ the finality
assert is unreachable for that draw (fires = 0 on all 45 arm-processes + the
checker's 7 adversarial arms; equality law held on every fresh draw including
window-32, seed-33/101, sab-6 and 8-s arms; min_region 32 control: 4 rollbacks vs
~1,300, never armed; replicate: rollback counts move with the wall clock while the
equality law holds in both). The engine-side fix's test can therefore be "armed ≤ 0
maintained" instead of window Monte Carlo.

**The finality-assert conflict is resolved and now at protocol strength: the crash is an
engine-side publish/rollback boundary defect, every overlap class reaches it, and no
driver or scene dodge closes it — the engine-side fix is the only door.** Frames mode
crashes on a scene with **no bulk approach at all** — one dense slow gas cluster
(selfchurn, internal spread 2 units/chronon, `min_region 1`) — at the keeping-up rate,
with panics at **chronon 32–96**: the first ~0.2 s of a loaded scene
(20261017-1018-taleb-01e7; re-run 3/9, bc0f). Both limbs of the driver rule are dead at
the page's protocol (≥ 3 seeds × ≥ 2 replicates): on-grid chunked targets crash
(chunk 128: 2/3 in both windows; checker: 96 and 512 too), and **single-call batch
crashes 7/12 (11/17 pooled with the checker), identically on-grid (3/6) and off-grid
(4/6), always at scene start 32→48** — the crash is decided in the first ~48 chronons
(survivors finish the whole 1800-horizon in 0.4 s), so horizon class cannot matter
(bc0f). Panic values per seed are stable across replicates; reachability is a
wall-clock race with **seed-skewed propensity** (s11 4/4, s15 3/4, s21 0/4; one
same-seed replicate pair splits; e517's sweep: s11/13/15/16 2-of-2, s14 1-of-2,
s12/17/18/19 0-of-2). **Two crash phases exist**: scene start under churn
(chronon 32–96) and **late quiet-phase reclash** in the dispersed/crossed classes
(chronon 1120–2720, panic gaps 16–144 = 1–9 windows) — this window crashed vmax-16
3/6 (4/22 pooled), vmax-8 2/6 (4/18 pooled), crossing 1/4 (the first crossing crash,
1/16 pooled) and vmax-8-at-480 1/3, so "quiet classes are safe / rare, not never" is
dead as a window-independent statement: **incidence is fat-tailed across windows; only
the zero-churn wave (0/15 pooled) and `min_region 32` (rb exactly 0, 9/9 pooled) are
strictly clean** — the knob deletes the conflicts, not the defect (bc0f). rb is not a
separator: n480-at-vmax-2 survivors sit at rb 123–180, far above the n240 crash band
57–95, and survive 5/6; a crashing draw never prints its rb (the row prints at
completion), so rb cannot be a draw-level predictor by construction (bc0f). Escalation
is exactly **E = 2^rb on every survivor, 37/37 across all arms, up to 2^180** (bc0f) —
the page's unbounded ratchet. Window 32 survived rb 83–109 (9/9 pooled across three
windows): the coarser stride/grid widens the race margin — a lead, not a verdict
(20261017-1018-taleb-01e7, checker, bc0f). The engine-side fix (refuse an advance
whose rollback would cross a published tick, or hold publication; 9b46's open
direction 1) is the confirmed requirement
(frames reachability first shown by 20261017-0839-dynamics-b966, 14/35 across five
windows, checker-confirmed).

**Prior standing (9b46, 3da3, 217f, e704 — unchanged).** The wave response is
Extremistan: at one frozen scene and N = 27,936 the seed flips the end-state *class*
(s7 → 1 region, s1 → ~2,400, s2 → ~2,500–4,700, s3 → 1,389) while nothing else is
seed-fixed (the latch E = 64–512, region counts, walls spread 1.65×/2.4× across
replicates); no quantity follows its attributed knob (E is drawn, not an N-law; the cap
verdict inverts across draws); the no-conflict regime is the cost floor (the quiet
control stalls < 0.6 timeline chronons/s at 28k); publication cadence is a path knob;
outcome digests are bit-identical across arms, caps, margins and replicates wherever
arms finish — the certificate moves scheduling, never results. Batch interior-tick
targets (off the window grid) are a separate, deterministic crash channel (7/11 on
5d87's box; on-grid 96–512 never crashed there — true for *their* sparse scenes, refuted
as a complete rule by the churn class above).

## Refuted

- **"Publication rides the boundary as an attractor — every realized non-fatal clash
  restores at exactly fin_hi == s0" (fd35/e517) as a law of the shipped allocator**:
  true on the churn family; on the fleet battle 94/261 non-fatal restores land strictly
  inside the boundary (m ∈ [−432, −48], median −224), so the boundary is the *limit*,
  not the typical restore point — the fix's test cannot assume it
  (20261018-0932-dynamics-c749).
- **"The negative certificate's publish-side half (armed A ≤ 0 at every publish) helps
  rule out fires" beyond the strides-between-publishes caveat**: measured blind — a
  galaxy-battle fire (regen g8704_s23, fatal pair 53↔36 at s0 704) appears in no armed
  HAZ line at its own margins (lineage 36 armed only in an earlier, differently-shaped
  episode, resolved); only the certify-side D saw it (20261018-0932-dynamics-c749).
- **"The crash is a window-grid defect of chunked batch drivers, not a live-path
  hazard"** (20261017-0839-second-…-5d87, as a complete claim): frames panics on one
  self-churning cluster at scene start (3/9 twice), on-grid chunk targets crash on the
  same scene (2/3 twice; checker: chunks 96, 512), and single-call batch crashes 7/12
  at protocol (bc0f) — grid alignment protects neither, and neither does one call per
  process (20261017-1018-taleb-01e7, bc0f). What survives of it: the batch
  interior-tick channel is real and grid-shaped, and the zero-churn class (wave) is
  safe in every driver.
- **"Crash dose grows with internal velocity spread"** (01e7's own pre-registered P6,
  inverted by measurement): slow dense gas (spread 2) crashes at scene start; fast gas
  (spread 8–16) mostly disperses first. The dose axis is sustained overlap, not spread
  magnitude — but the dispersed phase is *not* safe: it crashes late and
  window-dependently (vmax-16 3/6, vmax-8 2/6 in bc0f's window; 4/22 and 4/18 pooled),
  and 01e7's "rare, not never" is dead as a window-independent statement (bc0f).
- **"rb separates crashing from safe arms"** (01e7, as a draw- or band-level rule):
  n480-at-vmax-2 survives 5/6 at rb 123–180, above the n240 crash band 57–95; crashers
  never print an rb at all (bc0f; the checker's n480 0/3 first showed it).
- "Maybe frames mode's continuous publication is structurally protected by the ahead
  cap / the grid" (5d87; b966's alternative): refuted — panics with gaps 16–64 against
  a 150-chronon ahead lead; survival tracks rollback pressure (b966, checker2, 01e7).
- "The latch level grows with the conflict wave / scene size" (e704): E is a per-run
  draw, flat in N (9b46); in every churn-class survivor E = 2^rb exactly (01e7, bc0f).
- "The latch cap costs 2.3–3.6× wasted ops and a DNF-tailed wall" as a controller
  property (3da3): inverted draw-for-draw (9b46).
- "The one-region end state is the collapse's cost" (e704/3da3): churn magnitude is a
  draw; the collapsed state is never the slow one (9b46).
- "The rollback response is a controller": half — AIMD restores, escalation only
  doubles (217f). "Rollbacks cascade": self-quenching at the derived bound (217f).
- "The 10-line decay mirror restores the equilibrium": livelocks at scale (e704).
- "Per-region escalation fixes the wrong locality": ES_LOCAL wedges more (e704).
- "The margin drives the collapse": capped margins still coalesce; the end state flips
  with the seed (3da3, 9b46).

## Open directions

1. **The engine-side publish/rollback boundary — confirmed necessary at protocol
   strength; the survivor's unchecked mint is the ROLLBACK RESTORE first (7/8 fires),
   the regroup mint second (1/8; 3c03, checker-corrected): the fix must CAP inherited
   publication at the touchable truths' floor and make the mint inherit its members'
   live truths, at BOTH mint sites, never defer the merge — regroup-only deferral
   deleted every merge on the battle class (present 538) without touching the fatal
   mints** (upgraded by 01e7, bc0f; e517 supplies its test): refuse an advance
   whose rollback would cross a published tick, or hold publication until the wave
   quenches (specified by 9b46; reachability quadruple-confirmed: b966 + 01e7 at
   scene start, bc0f through on-grid chunks, single-call batch on and off grid, and
   the late quiet-phase reclash of dispersed/crossed classes). e517's cost note: on
   the churn family the hold rule refuses the whole scene start on every draw —
   pair it with the disarm channel (truth pruning) or it starves publication.
   Until it lands, `min_region` is the named exposure knob (it deletes splits, a
   capability, not the defect).
2. Window/stride granularity as the race margin (01e7's lead): window 32 survived
   rb 79–114 at 9/9 pooled draws across three windows where window 16 crashed at
   rb ≥ 57; the margin `fin_hi − s0` scales with the grid. More draws per arm before
   it is a verdict.
3. Open the quiet stall: the no-conflict many-region regime is the family's cost
   floor (< 0.6 chronons/s at 28k, 1.7 at 14k); merge/avoid churn vs per-unit floor
   (9b46, untested).
4. Seed/load protocol for every allocator verdict (exercised by bc0f, honoured by
   e517): ≥ 3 seeds and ≥ 2 replicates, sweep the load axis (rate × n) before
   calling anything reachable or safe; incidence lives in bands and is
   window-fat-tailed — invisible at endpoints and in single windows (9b46, b966,
   01e7, bc0f: vmax-16 0/6 in the checker's window, 3/6 in bc0f's; e517: 9/18 on
   the same family at higher load).
5. The real conflict rate of the flown universe (encounters, burns, the belt) — **first
   half answered (bf83): the battle class fires unsabotaged on shipped code (1/14 at margin
   0.5, 0/6 at the default 2.0); the belt's clump and crossing shapes stay clean at
   protocol; churn without slack cannot fire.** [c749, 20261018: the second half is done
   for the fleet class — the fire's internal state measured on `worlds::galaxy` battles,
   6/6 fires state-decided (D = violation, out= shut), the violated region the armed
   pair's merged giant descendant; the boundary attractor and the publish-side armed
   certificate do not transfer (see Current best and Refuted). The fix must gate
   certifies, not publications.] Still open: the incidence tail (windows, rate 600
   long-horizon, more seeds), the plane's own flown battle once wired, and whether the
   publish-blind fire class is always a between-publish dispatch.
6. Margin from the law, not from history (relativistic scenes): the c-cap makes the
   conflict window one stride; no-conflict throughput ceiling unmeasured at every size
   ≥ 128 cells (e704 checkers).
7. **Timing analysis of the race — CLOSED both ways (bc0f's note; fd35 state side;
   e517 positive side).** Incidence stays a wall-clock draw (armed survivors: 9/9
   survivor draws armed without firing), but the assert's firing is state-decided at
   certify: PRE D > 0 ⟺ fire, exact on 9 fires (D = 16 = violation) and 2,286
   non-fatal clashes (D = 0), closures coinciding (`out=` never opened, 0/2,295).
   The fix's test is the state certificate (armed ≤ 0 ∧ D ≤ 0), not Monte Carlo.
   What is left for a next run: the *geometry* derivation of why `alone_at` and
   `certify` pin the same contact tick (fd35's lens note) — the soundness argument
   the fix will be written against.

## Contradictions

- None open: the b966/5d87 records are reconciled as two scene classes of one exposure
  (sustained-overlap churn vs planned/no churn; 01e7), with bc0f adding that the
  dispersed/crossed classes reach the same assert late and window-dependently. 3da3's
  "unbounded latch is not a reachable ruin" against its checker's 28,160 draw: both
  basin draws (9b46). The tax battery's one-region-at-~10-chronons/s collapse vs
  9b46's wave family: different batteries, opposite cost owners; the churn and the
  many-regime floor are the battery-independent suspects. fd35's 0/45 arm-processes
  against 01e7/bc0f's 7/12 was a scene-class gap, now bridged: e517 fired the same
  assert on the selfchurn harness with fd35's instrument and the equality law held
  there too — one boundary, both sides measured.

## Runs
- 20261016-2138-dynamics-217f (this run, awaiting grade): the rollback ratchet measured —
- 20261016-2138-dynamics-217f (silver, checked): mechanism, quench and digest invariance
- 20261016-2138-dynamics-217f (silver, checked): the rollback ratchet measured — global,
- 20261017-0238-second-20261016-2138-dynamics-217f-e704 (gold, checked): the
- 20261017-0428-taleb-3da3 (awaiting grade): ES_CAP killed — the latch is convexity: caps
- 20261017-0739-taleb-9b46 (awaiting grade): Extremistan wave response — the seed flips
- 20261017-0839-dynamics-b966 (awaiting grade): the finality crash reaches the frame
- 20261017-0839-second-20261017-0739-taleb-9b46-5d87 (awaiting grade): the crash is a
- 20261017-0428-taleb-3da3 (silver): ES_CAP killed — the latch is convexity
- 20261017-0739-taleb-9b46 (silver): Extremistan wave response — the seed flips
- 20261017-0839-dynamics-b966 (silver): the finality crash reaches the frame harness
- 20261017-1018-taleb-01e7 (awaiting grade): conflict resolved — crash is engine-side,
- 20261017-1018-taleb-01e7 (silver): conflict resolved — crash is engine-side,
- 20261017-1149-second-20261017-1018-taleb-01e7-bc0f (this run, awaiting grade):
- 20261017-1447-dynamics-fd35 (this run, awaiting grade): the race as state — equality
- 20261017-1829-second-20261017-1447-dynamics-fd35-e517 (this run, awaiting grade):
- 20261018-0035-inversion-bf83 (this run, awaiting grade): the game shapes separated by fire — fleets fire unsabotaged (1/14, margin 0.5), belt shapes clean, churn without slack inert; margin 0 is its own ruin.
- 20261018-0932-dynamics-c749 (dynamics, awaiting grade): the fire's state on the game's
- 20261020-0143-taleb-da23 (taleb, awaiting grade): the stride gate built: fires 7/8 → 1/10 on the battle protocol, ~15-40% present cost, equality law held; one survivor fire names the last hole.
- 20261020-0440-library-3c03 (library, lead): survivor instrumented; author pinned regroup, checker corrected to the rollback-restore mint (7/8 fires, the uninstrumented site); regroup-only mint-block starves (present 538) without touching the fatal mints.
