topic: allocator-ratchet
status: open
closed-by:
valid-while:
updated: 20261020-2102-second-20261020-2004-taleb-c1ad-b41f

# The allocator's rollback feedback: a one-way ratchet on the forecast margin

## Current best

**NEW (b41f, second author on c1ad — the checker's named gold experiment done: v5 rebuilt
as v6, the heterogeneous family un-stalled at v4's exact present, 0 fires).** v6 = v5 with
(1) the base term dropped to `verified` alone — `history[0]` was a restore-point term, not
a clash-s0 term, and it DEADLOCKED IGNITION: prune pins history[0] at the sync floor
(stride_max·window = 256), so inside the first sync grid every floor was 0, nothing
published, the present stalled at the observer's own cluster and the goal cap kept the
frontier below the grid forever (clumps/mixed at present 0, 1080/1080 deadline misses —
the checker's stall, mechanism found); (2) both window-keyed terms (suffix-min `sm`,
scanner-min `lscan`) replaced by ONE geometric pair scan mirroring certify's clash
predicate: region r scans a live truth keyed at w ≥ w(r.verified) only from
s ≥ boundary(w−stride_max), the pair pins both lineages at min(s, t.start) iff the truth
touches r's hull grown to the truth's DEATH horizon (boundary(w+1)+sync()−verified+
stride_max·window — a scan can happen at any start until the truth is pruned; the
earliest-scan hull missed a pair a later scan fired on: the pre-fix build's s13 fire,
victim = the truth's own writer, fin_hi 768 vs s0 640 — also a hole in v5's lscan, whose
0-fires were incidence, not closure); (3) cap_final coverage-aware: retain can drop a whole
parent's lineage (`a view holds every body once` panicked 5891/8704) — rebuild from the
deepest complete history entry ≤ cap (CAPGAP last resort, 0 occurrences). **Measured
(one binary, env arms v4/v5/v6; family rate 600 seeds 11+13): clumps 2695/2695/0/2695,
mixed 2698/2698/0/2698, streams 2698/2577-819/1024-819/2698 (shipped/v4/v5/v6 — v6 at v4's
exact values, above v4 on streams; v5's kill reproduces); battle seeds 11-21: shipped 1/6
(s21), v4 0/6, v6 0/6 present 1440-1792; crush 12-way: v6 0/12 median 529.5 vs v4 272.5
(~1.9×), 0 CAPGAP; equality law 97+44 RB all m ≤ 0, out=[].** Open before close: the
death-horizon growth recouples toward v4's global floor under a frontier-stalling laggard
(window-owned, not flown here); O(regions×truths-in-range) per finalize unmeasured at 10⁶;
the descendants-closure derivation (20261020-2102-second-20261020-2004-taleb-c1ad-b41f).**
  [Checker b41f: the liveness half reproduced bit-exactly (same commands, ~30 min later:
  family clumps 2695/2695/0/2695, mixed 2698/2698/0/2698, streams 2698/2624-819/1024-819/2698,
  quiet 2698 all; crush v6 0/12 median 532 vs v4 205, ~2.6×, 0 CAPGAP). The safety half did
  NOT: the regen window fired v6 once on battle s19 — the finality assert itself ("rollback
  of region 53 from 816 would revise its published tick 896"), RB m=80 > 0 (P1 and P4 break
  as window-free claims; shipped 3/6 there vs 1/6 in the author's window). Four immediate
  s19 re-runs clean, v4 clean ×2, fresh seed 41 clean, 2× scale 17408/48 s11/s13 clean — a
  rare interleaving, not a deterministic kill. The regen's non-fired battle margins sit at
  zero slack (44 of 57 RB exactly m=0), so "0 fires / exactly safe" is window-owned, not
  closed; suspect paths unexamined: the rollback re-cap covers only restored.last() and runs
  after the assert, and a truth born after the publisher's floor computation. Silver.]

**NEW (c1ad, taleb — f1ca's named close built and flown: v5, the per-region publish floor
with merge-capping, on both publishers).** For region r the binding s0 of any future clash
that can assert r (or a region inheriting its parts) is: starts of live truths keyed at
windows r's strides still span; for r's lineage's live truths, the truth's start or the
least stride-start of a live region still spanning that window (a stride spans ≤
stride_max windows — the bound that keeps a far laggard from recoupling everything); r's
own verified, oldest snapshot and least live-ancestor verified. `publish_floors()` caps
the frontier advance AND the gated coalesce; `cap_final()` re-caps inherited fin_parts at
every merge/rollback (`regroup` purges no member truths — the merged child inherits the
other parent's high parts with a stale-truth lineage). NOT capped by the global frontier:
capping by `front` re-couples to the laggard's verified (measured: v5 at 74% of shipped
under crush with the cap, 92% without — the cap was the residual coupling). **Measured
(one binary, env arms; battle = galaxy 8704/24, rate 2400, margin 0.5, seeds 11-25 odd;
crush = 12 concurrent battle draws): shipped fires 1/8 (s21, fin_hi 544 > s0 512), v4 0/8,
v5 0/8 and 0/12 crush; crush medians shipped 387, v4 256 (66%), v5 355 (92%); quiet battle
present v5 1280-1792 against shipped's 1280-1536 (same window); equality law shut on all
257 v5 RB lines (every m ≤ 0, out=[] always); quiet control clean in every arm.** The
author's pre-registered 3× v5/v4 crush band FAILED (1.39×: v4 only fell to 66% in this
window, not f1ca's 43-vs-529 class — window-owned); the decoupling's honest number is 92%
of shipped against v4's 66%. v5's exactness needs one assumption v4 did not: `affected` =
the descendants closure (measured shut, e517/c749 + 257 here); the stride-span bound is
config-true (an unbounded-stride config invalidates lscan). The deterministic-laggard
scene (mixed class, shipped in the patch) does not laggard on this box — the crush stays
the laggard protocol (20261020-2004-taleb-c1ad).
  [Checker c1ad: the safety half reproduced and extended — regen window shipped 1/8
  (s17), v4/v5 0/8, equality law shut on 111+42 RB; fresh seeds 41-47 shipped 1/4 (s41),
  v5 0/4; 2× scale (galaxy 17408/48, beyond the author's range) shipped 3/4 fires, v5
  0/4 at present 512. But the decoupling claim is falsified outside the battle class:
  the heterogeneous family stalls under v5 deterministically — clumps present 0 (shipped
  and v4 both 2695, s11+s13), mixed present 0 (shipped and v4 both 2698, s11×2+s13;
  1080 deadline misses), streams 1024 vs shipped 2698 — a slow region's floor pins the
  whole scene's present, so "a laggard pins only its lineage" dies at the present level;
  v5 as shipped is killed as a configuration on multi-cluster scenes (the v4 control
  isolates v5's floor, not the gate). Reproduction defect: work/patch.diff contains every
  file diff twice, so the clean-tree regen the runner ran fails at apply; the numbers
  reproduce from work/fix.diff (byte-identical to the first half).]

**NEW (f1ca, taleb — 541d's named next experiment built: the disarm channel as an
exactly-safe publish floor, v4).** Under `stride_gate`, the frontier advance publishes up
to `floor0 = min(oldest kept snapshot, oldest kept truth start)` instead of being removed
(v3) or unbounded (shipped): no rollback can restore below floor0 (every restore reads a
kept snapshot or kept truth start, both ≥ floor0; floor0 monotone), so publication there
cannot fire the assert. **On the battle protocol (8 quiet paired draws): shipped fires
3/8 (s11/s21/s23, exit 101) — a SECOND unsafe publisher besides 541d's frontier pin: the
shipped light-cone coalesce itself, every fire signed `fin_hi > s0 = front` (1072>1024,
v4 0/8, present 71-94% of shipped (median 93% on clean pairs, the author's window; the
checker's regen window gave 51-100%, median 74% — wall-clock-owned, both windows above the
pre-registered ≥0.5-every-seed / ≥0.7-median thresholds), equality law intact
(136 RB, all m ≤ 0, out= shut).**
But the channel is **min-coupled**:
under 4- and 12-way crush a region that never accepts pins frontier=0 and floor0=0 (its
truths at start 0 stay live and readable by itself; HAZ f=0 F=0 all draw vs shipped's
f=0 F=368→512 — shipped "survives" the laggard only through the coalesce, the exact
publisher that fires), and the gate starves (s11: 43 vs shipped 529; s19/s21/s23 hold
44-100%). The close's shape is now: a **per-region floor** (deepest restorable tick among
truths that can still touch this lineage, with merge-capping) or a scheduler that refuses
to let one region pin the engine's finality; the global floor is exact but
load-min-coupled (20261020-0440-taleb-f1ca). [Built and flown by c1ad above.]
  [Checker f1ca: reproduced — 0 fires on every gated draw incl. the checker's fresh seeds
  37/39/41, where shipped fired 3/8 in one window with the exact signature
  (fin_hi > s0 = front: 1136>1104, 960>912, 784>768) and v4 ran clean on all three at
  1280-1536 present; equality law 77 further RB, all m ≤ 0, out= shut; 12-way crush
  v4≡v3 (43/341/153/119) with the pin line f=0 F=0 S=0 vs shipped f=80 F=368 S=0 armed
  A=80. Adversarial beyond the author's range: 2× scale (galaxy 17408/48) v4 82% of
  shipped, 0 fires; 9 s horizon 83%, floor lag does not compound; the 2-way load boundary
  is clean (96%). The churn class (gas) stays unflown: no splits occur in a 4.5 s window
  on this machine, both arms identical.]

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

**NEW (c749, dynamics — od 5's named next step done: the fire's internal state on
the game's own fleet battle, e517's instrument verbatim on bf83's harness).** Six fires
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
**(e517, second author on fd35 — the positive side reproduced, direction 7 closed
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
m = 0.)**
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
open (direction 7). [c1ad note: v5's exactness buys exactly this measured closure —
the assumption is now load-bearing for a built fix, the derivation is the page's
highest-value open.]**
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
- **"The light-cone coalesce is a safe publisher" (the surviving half of the shipped
  design after 541d pinned the frontier advance)**: fired 3/8 in one quiet window, every
  fire signed fin_hi > s0 = front (1072>1024, 544>512, 672>512) — the coalesce publishes
  above live truth starts exactly as the frontier advance does (20261020-0440-taleb-f1ca).

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
   strength** (upgraded by 01e7, bc0f; e517 supplies its test): refuse an advance
   whose rollback would cross a published tick, or hold publication until the wave
   quenches (specified by 9b46; reachability quadruple-confirmed: b966 + 01e7 at
   scene start, bc0f through on-grid chunks, single-call batch on and off grid, and
   the late quiet-phase reclash of dispersed/crossed classes). e517's cost note: on
   the churn family the hold rule refuses the whole scene start on every draw —
   pair it with the disarm channel (truth pruning) or it starves publication.
   Until it lands, `min_region` is the named exposure knob (it deletes splits, a
   capability, not the defect).
   **[f1ca, 20261020: the disarm channel now exists — v4, five lines in `finalize()`,
   exact (publish up to the deepest restorable tick floor0), fires 3/8→0/8 at 51-100% of
   shipped present in quiet windows; NOT yet the close: under crush the global floor is
   min-coupled (a never-accepting region pins frontier=0=floor0 and the gate starves
   while shipped hides the laggard behind the unsafe coalesce). 541d's second unsafe
   publisher (the coalesce, fin_hi > s0 = front) is now measured too — both shipped
   publishers are dead.]**
   **[c1ad, 20261020: v5 built and flown — the per-region floor with merge-capping on
   both publishers, exact modulo the measured descendants closure, 0 fires on 20 draws
   (battle 0/8 twice + crush 0/12) where shipped fired 1/8, and 92% of shipped's crush
   present against v4's 66% (the starvation decoupled; the author's 3× band failed —
   v4 never starved that hard in this window). Remaining before this closes: (a) the
   descendants-closure derivation (now load-bearing for a built fix — out= shut on
   2,714+257 RBs, never derived); (b) the stride-span bound is config-true (lscan
   assumes ≤ stride_max windows per stride); (c) fresh seeds/scales and the churn
   class under v5 (this run's crush is one window); (d) the overhead at 10⁶ regions
   (O(truths + lineage edges) per finalize, unmeasured at scale).]**
   [Checker c1ad: (c) is answered and it kills v5 as shipped — fresh seeds/scales clean
   and fire-free, but clumps/mixed stall at present 0 and streams at 38% of shipped
   where v4 runs clean (see Current best); the next candidate must bound the self-pin
   (a region's own genesis truths stay scannable by its own strides) before the family
   re-flies.]
   **[b41f, 20261020: the re-fly is done and passes — v6 (geometric pair-scan floors,
   death-horizon touch, verified-only base, coverage-aware cap) matches v4's 2695/2698/2698
   on the family (above v4 on streams) with 0 fires on 44 draws incl. crush; the stall was
   two mechanisms — the history[0] ignition deadlock and the window-keyed coupling — plus a
   latent v5 cap bug (view coverage). Remaining: the stalled-laggard recoupling window, the
   10⁶-region cost, the closure derivation.]**
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
   the fix will be written against. [c1ad: and now IS written against — v5's floor is
   that argument's first customer; the derivation is open direction 1(a).]

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
- 20261020-0440-taleb-f1ca (taleb, awaiting grade): the disarm channel built (v4, publish
- 20261020-2004-taleb-c1ad (taleb, awaiting grade): v5 built and flown — per-region publish floors + merge-capping: 0 fires on 20 draws (shipped 1/8 same window), crush present 92% of shipped vs v4's 66%.
- 20261020-2102-second-20261020-2004-taleb-c1ad-b41f (second author, awaiting grade): v6 rebuilt — family at v4's present, 0 fires on 44 draws; v5's stall was ignition deadlock + window coupling.
