topic: nladder
status: open
closed-by:
valid-while:
updated: 20261019-1551-inversion-f80a

# The N ladder: 28 live bodies toward 10⁹

## Current best

**NEW (f80a, inversion — the adoption's own fence inverted: e181's checker's named step flown, and
the fence deletes only HALF the ratchet — with `prune()` restored and the arm flown past every prior
horizon, TTL=16 staircases to 1,457 MB at 419k game-s on the history channel alone, so channel 2's
fix is co-equal, not deferred).** Binary: e181's patch verbatim + the frame-loop `prune()` call
RESTORED (its checker's correction (a): the patch had replaced it with the fence in BOTH arms, so
"off = shipped bit for bit" is true again on this tree) + 527a's `history_census` fields in the
probe. Scene: shipped `nladder` 3×10⁴ seed 1, L8 burn, 12 ms, guard 1,600 MB, **rtf 1000**
(game-timed memory laws; the retention *rate* is cadence-coupled — the named falsifier — the
*law* is not: 527a's rtf-100 20.7 bindings/body at 332k against this run's 28.8 at 419k)
[checker f80a: the coupling is NOT cadence — fresh rtf-100 arms on this tree (fence ON **and**
OFF, same scene) land on the rtf-1000 census to 0.6% at matched game-s (75,670 vs 75,213 at 60k;
first-wave saturation at both cadences), so the ~1.7× gap against 527a is a cross-tree/instrument
difference, not cadence; 527a's rtf-100 shipped-arm RSS/held digits (581 MB/236 at 60k) DO
reproduce on this tree (579/237) — the laws are cadence-independent, the census field differs].
OFF (TTL unset ≡ shipped, 174k gs): **gt1 saturates at the FIRST kick wave — 351 → 30,064 of
30,028 bodies between gs 11k and 16k — then +1 binding/body/wave to 241,552 = 8.03/body (hist_max
2,017), RSS 537→900 MB, kicks 8.397e-5 the record's own digit.** ON (TTL=16, 419k gs, the longest
fence arm in the record by 10×): counter identity exact (3,427 = 1,102 + 2,325 + 0 held; held ≤ 1
at every probe — channel 1 fully deleted), RSS flat 171–212 MB through 95k (e181's regime
reproduced), **then the ratchet returns: +3.32 MB/1k (130–200k), +4.19 MB/1k (200–419k) → 1,457 MB,
866,168 bindings = 28.8/body, hist_max 7,921, no saturation, guard ~440k gs.** The channels are
independent to the binding: hist_total IDENTICAL between arms at matched probes (66,752/66,752,
97,052/97,052, 155,142/155,144). **The fence buys ~15% horizon at 3×10⁴** (OFF projection ~380k,
ON ~440k); e181's "flat" was real inside 42k, and everything past ~130k is channel 2's. Corrections:
527a's "onset ~95–130k" is slope-dominance, not retention start (first wave, 13–16k; the keep key
set at kick time outruns `now` from wave 1, prune never visits, 30,065 bodies hold their whole
kicked history); e181's prune-deletion is now measured both ways. Falsifier named: a checker's
rtf-100 fence arm past 130k with census ~1/body inverts this to a cadence artifact
(20261019-1551-inversion-f80a, inversion; predictions pre-registered P1–P5, all held; two flights
~4 min wall, regen ~11 min).**

[checker2 f80a: gold, confirmed — both end states reproduce bit-exact in a clean tree at c9195bfa
(OFF 241,552/30,065/2,017; ON 866,168/7,921/1,457 MB, identity exact in both arms); two digits
above are slips: the saturation is 30,065 of **30,076** bodies (99.96%; "30,064 of 30,028" is an
impossible pair), and "IDENTICAL" overstates — max |Δhist_total| over the 174 matched probes is
134 (~0.1%, the same band as run-to-run drift; exactly equal only at the final matched probe, and
the windows.txt OFF 95–130k cell 155,142 is the ON log's value — the shipped OFF log reads 155,110
at gs 129,007, my rerun 155,143, run-elastic). Two fresh arms: K=10⁵ fence ON — first-wave
saturation (gt1 100,064), identity exact (2,992 = 1,043 + 1,949), RSS 511 MB at 59k on channel 2
alone (the law extends a decade up in N); TTL=64 — census exactly tracks TTL=16 (74,733 = 74,733
at 59k), channel 1 still at zero: independence is fence-width-insensitive. Mechanism verified in
code: key_prune's keep key droppable_until + 2·light_distance + 2²⁶ (universe.rs:1252), visited
only when ≤ now.]

[Checker f80a, gold: reproduced end to end (patch applies clean at c9195bfa, regen matches
windows.txt to schedule-elastic digits; independence re-verified at all 144 matched probes, max
|Δhist_total| = 134). Four fresh adversarial arms, all holding, two outside the author's grid:
rtf-100 fence arm flown to 200k gs — the named falsifier is DEAD (309,024 bindings = 10.3/body at
200k vs the rtf-1000 arm's 306,046; RSS 546 MB staircasing; kill criterion needed <1.1/body);
rtf-100 OFF arm ≡ fence arm ≡ rtf-1000 arms (independence extends to the player's cadence);
K=10⁵ rtf-1000 fence arm — first-wave saturation at 100,063 of 100,028 bodies, held ≤ 1, identity
exact, guard-stopped at ~200k gs on channel 2 alone (the composed horizon at 10⁵, measured not
projected; hist_total non-monotone per-probe there: prune wins back ~20k between waves, net
ratchet). The "~15% horizon" digit is projection-sensitive — OFF's guard lands 322–556k on the
measured late slopes (held-scan growth +1.5 scans/1k × 1.94 MB accelerates OFF), ON at 453k; the
robust sentence is: neither arm is flat, both guard at O(0.3–0.5×10⁶) at 3×10⁴, and the fence's
arm is channel-2-bound. e181-verbatim is verified semantically (e181's folder is on its own
branch, not on disk).]

**NEW (527a, taleb — the page's same-day conflict resolved by measurement: 1b3f's per-reader
`oldest` does NOT touch 4447's interstellar burn ratchet — the two entries are two independent
channels — and the ratchet's mid-flight channel is the scan deque, whose SCAN_BACKLOG fence is
sized on a stale premise and licenses the ruin it was built to bound; a second, later-onset
history channel measured for the first time).** Same binary for both arms (1b3f's patch
verbatim + a disclosed probe addition: `held=`/`hwm_mb=` in the probe line, the
`LADDER_RSS_MB` guard), nladder K=3×10⁴ seed 1 rtf 100 12 ms burn, ON = `ES_READER_OLDEST=1`,
OFF = unset: **ON ≡ OFF to the digit through both channels** — the 60k-gs arm (RSS 581 vs 579
MB, held 236 both, census 45,480 both, kicks 8.436e-5 both) and the guard arm (both hit
LADDER_RSS_MB=1600 at gs 332,277 — 4447's own 332,604 — held 588 both, census 620,831 / gt1
30,043 both); `gap_s` (now − oldest) stays ≤ 1.7 s at 3×10⁴ [checker 527a: the 10⁵ arm's own
`prune:` line reads 82.4 s max over the flight — the 4.1–4.2 s the probes sample misses the
peak; still ≪ the 3,000 s certificate bound]: the `oldest` door 4a71
certificate'd shut never opens naturally here, so the rule's channel is absent and cannot bind
(1b3f's checker's "at one star the oldest term never binds" extends to one-star-interstellar).
**Channel 1 (mid-flight): the held scans themselves.** Each scan retains its captured
candidates (`Scan.candidates: Vec<(usize, Binding, Scalar)>`), and interstellar the cheap tests
pass everyone in the root doll: measured 1.94 MB/scan at 3×10⁴ and 7.36 MB/scan at 10⁵
(K=10⁵ guard at gs 38,033, RSS/held 9.47 MB, slopes 67–90 MB/1k gs) — 60–95 B per doll body
per scan, K-linear [checker 527a: the K-linear law stands on the pre-onset arms (60k gs:
~1.96 MB/scan, gt1 252; 10⁵: 7.36, gt1 200) — past ~95k gs channel 2 confounds RSS, so the
guard-arm subtraction is not a clean per-scan measurement].
**The fence licenses the ruin**: `SCAN_BACKLOG=2048` is sized on "about
10 KB each" (universe.rs) ⇒ 20 MB, but measured it licenses 2048 × 2.72 = 5.6 GB at 3×10⁴ and
2048 × 9.47 = 19.4 GB at 10⁵ on the 8 GB machine, and it never engages first (guard fires at
held 588 / 195 ≪ 2048): the fix's unit is pinned BYTES at capture (4447's named fix; the
constant is now measured), not scan count [checker 527a: the stale premise, the byte-cap fix
and "a count cap cannot fence bytes" are already this record's — 51b7 measured 11.3 MB/scan
marginal on this same burn scene at 10⁵ and projected the cap can never engage; b8e2 refuted
the fence at formation scale; b77d-1fcf named the capture-byte fix — this run adds the
belt-scene constant and the measured never-engages-before-ruin]. **Channel 2 (late, new): history retention behind
the receding observer.** From ~95–130k gs the census ratchets — gt1 saturates at 30,043 of
30,076 bodies, then +~30k bindings per ~28k-gs kick wave to 620,831 = 20.7/body at the guard,
hist_max 5,845 — absent in coast (30,471 flat, held ≤ 1, RSS flat 148 from 15k gs). Code path:
`key_prune`'s visit key `droppable_until + 2·light_distance + 2²⁶` — the observer recedes at
~c so the key outruns the present (onset when 2·ld exceeds the wave gap) [mechanism inferred;
the growth and the coast control are measured]. Neither fix touches channel 2; it belongs to
the view/retention design and breaches later (gs ≳ 130k) than channel 1 at every rung flown.
Conflict resolution: keep both prior entries — they are both right, about different doors; the
adoption order is byte-capped scans (channel 1) > per-reader oldest (the far-doll door, still
needed at two stars) > channel 2's view-side answer (20261019-1452-taleb-527a, taleb;
predictions pre-registered, P2–P3 held and P1 held on slope/gap but its "census stays flat"
clause failed — that failure is channel 2; 6 flights ≤ 80 s each, regen ~4 min).

**NEW (4447, inversion — the burn-mode memory ratchet is UNBOUNDED and K-growing in play time:
the two same-day readings that split on it are reconciled, and both half-right).** The record's
live tension: d839's checker read a ratchet (150→571 MB, 13–16 MB/1k gs at 3×10⁴) "then flat"
at 40.5–45.5k gs; dcf1 read "the burn-mode byte wall is gone on current main by ~3 orders"
(VmHWM slope 0.026 MB/game-s, K-flat, "8 GB ~300,000 game-s out"). This run flies the burn past
every prior horizon (my patched nladder: Linux /proc footprint + env-gated LADDER_PROBE every
500 gs / LADDER_CAP_S / LADDER_RSS_MB guard at 1,600 MB; off = the shipped loop; seed 1, rtf 100,
12 ms, quiet box, sequential flights): **K=10⁴ burn to 560,764 game-s (93 wall-min, the record's
longest burn flight by 12×): RSS 41→1,601 MB monotone, guard-stopped while still climbing
3.4 MB/1k gs**; K=3×10⁴ burn (d839's checker's exact arm): **guard at 332,604 gs, late slope
4.57**. Window slopes: 1.1 / **5.7** / **0.8 (the 40–60k local plateau d839's flight ended
inside)** / 1.7 / 2.3 / 2.9 / **3.2** at 10⁴ — and 4.4 / **16.3** (= d839's 13–16 exactly) /
1.1 / 2.9 / 3.0 / **4.6** at 3×10⁴: **the mid-flight slope is ~K-proportional (5.7→16.3 for
**NEW (e181, library — the fence's expiry half is flown and the deletion is nearly free: the
dropped scans are ~35× emptier than the answered ones).** The record priced the burn-mode
ratchet (4447) and flew the oldest's scope (1b3f), but the answer-or-expire fence's expiry
half had never been flown or priced. This run flies it (env-gated `ES_SCAN_TTL_S`, off =
shipped bit for bit; Linux /proc probe; flag-off control at 10⁴ coast = the record's digits
bpb 2,463 / cat 10,076): at the ratchet's own worst arm (10⁵, L8 burn, rtf 100, 12 ms,
guard 1,600 MB), the shipped arm guard-stops at 29,563 game-s, RSS staircase 259→1,595 MB,
answers frozen at 2,521 from ~16k gs (the latch freeze), while the TTL=16 arm flies 41,898
game-s (42% further) FLAT at 613–702 MB (slope 4e-3 MB/1k gs past 19k gs), held ≤ 1 at
every probe, counter identity exact (2,723 mints = 2,496 answers + 227 expired + 0 held);
TTL=8 flat at 642 MB. **The deletion price, the fence's open question: ≤ 10 encounters
lost net against the shipped arm's 3,986 (≤ 0.3%) — ≤ 0.044 lost encounters per dropped
scan against 1.58 per answered scan: the fence drops exactly the dead interstellar tail**
(Musk's 10% add-back bar, met with 30× margin). Per-scan pinned bytes confirmed at 12.7 MB
(1,611 MB/127 held), so `SCAN_BACKLOG`'s count cap (2048 = 26 GB at 10⁵) is dimensionally
wrong — the fence must count pinned bytes and be sized by arithmetic at 10⁶
(TTL·λ·(K+38)·224 B). The TTL arm is a law change (expired scans never log; digests
differ by construction): adoption owes the digest re-freeze; unflown at 10⁶ (build 2.34 GB
> this box's cap — arithmetic only there) (20261019-1452-library-e181, library; shipped
`nladder` + /proc probe + the disclosed env-gated fence, 6 flights ≤ 90 s, regen ~4 min;
predictions pre-registered: P1/P2/P4/P5 held, P3 half-held — the identity exact, the
in-frame held spikes 157 outside my 26 ± 12 band).**

[Checker e181, silver: reproduced end to end at base 8b51786 (A exact: guard frame 17,739 /
29,563 gs, answers latched 2,521, encounters 3,986; B: flat 613–702 MB to 41,898 gs, identity
exact, encounters 3,978 → 8 lost; C 642 MB). Three adversarial arms hold, one outside the
author's grid: TTL=1 (extreme) stays flat 642 MB, held_max 17, 3,841 encounters at 23.9k gs
vs TTL=8's 3,884 (−1.1%) — the dead-tail price survives even when the fence eats young scans;
TTL=16 on 10⁴ coast is digit-identical to off (193/193, encounters 119); TTL=0 ≡ unset.
Corrections to this paragraph: (a) the patch ALSO deletes the frame-loop `prune()` call in
BOTH arms — undisclosed, so "off = shipped bit for bit" is false until those 3 lines are
restored (outcome-neutral: prune is forget-only, and arm A's RSS tracks held at ~9–12.7 MB
with no baseline creep, so the ratchet attribution stands); (b) the arm-B/C expired splits are
schedule-elastic digits, not regenerable points (author 227/263; checker reruns 260/294, same
identity and same ≤ 0.3% price; B's own encounter count varies 3,976/3,978 across identical
runs — the law change coupled to schedule); (c) bpb 2,463 is a band (2,458–2,464 across five
coast runs), and the staircase ends 1,611 MB at the guard, not 1,595; 1,611/127 conflates the
~300 MB held-0 baseline with scan bytes — the 16→29k gs slope is ~9 MB/held scan. Silver, not
gold, for (a): one prune-restored rerun of arms A/B, with the dossier's "off = shipped" line
corrected, is the missing step.]

3× the bodies), the late slope rises, and neither arm saturates.** The mechanism, both arms:
held_scans grows monotonically and never latches (741 / 589 at the guard; SCAN_BACKLOG 2048
never engaged) while RSS/held compounds 0.9→2.2 MB — the growth lives outside the dashboard's
accounting (bpb 18.8 kB/body × bodies = 189 MB of 1,601; catalogue constant 10,076/30,076;
build per-body constant 2,463/2,372 B) — the scan channel's retention, with the player
INTERSTELLAR since gs ≈ 1.6k (doll 0 at frame 948) and the ratchet running 560k gs past
departure: **the mint channel does not need the belt near; dcf1's "~300 locals cap the
candidates" held only inside the system — their flight ENDED at the SOI switch (frame 948),
the phase boundary where this ratchet begins.** Budget arithmetic on the final-slope (a lower
bound: slopes rise): 4 GiB at ~1.39M game-s ≈ 3.9 wall-h (10⁴) and ~880k gs ≈ 2.4 wall-h
(3×10⁴); **one wall-hour of held L8 = 989 MB at 10⁴, ~1.6–2.2 GB at 3×10⁴** — the approved
plan's frozen 4-GiB/one-hour budget survives one hour only ≈2.5× at 3×10⁴, and at 10⁵ the
mid-flight K-scaling puts the breach at ~70k game-s ≈ 12 wall-min [INFERENCE, two-point
scaling]. Controls: coast at the same horizon (797k game-s, 1,594 probes) flat at 61 MB,
0.02 MB/1k gs, held 0 throughout — the instrument's negative control; frames mild (66–69 over
of 200–336k, worst 42.5 ms): at these K the ratchet's cost is memory, not smoothness. The
record's own named fix (b77d-1fcf/b8e2/acf2: count pinned BYTES at capture + answer-or-expire
at a game-s cadence) is not on main and this flight prices its absence; dcf1's "gone by ~3
orders" is dead outside the pre-departure window, and d839's checker's "then flat" was
truncation (20261019-0435-inversion-4447, inversion; three flights ≤ 140 s wall, regen ~7 min;
predictions pre-registered: P1 ratchet held at 3.0 ≥ 2, P3 control held, P5 held — no
scene-exhaustion; P2 half-held: the channel is held's, but RSS/held is not constant — the
per-retained-scan bytes compound; P4 mild/qualitative).**

[Checker 4447: regen end-to-end plus three fresh arms, all outside the author's grid, all
support the claim. Probe-off (shipped loop, cap only): 1,001 MB at ~365k gs, held_max 593 —
the probe instrument is not the cause. K=3×10³ (a rung below the grid): the ratchet reproduces
(windows 0.4/1.7/0.7/1.3/2.0/2.6, still rising at 288k gs), and the held trajectory is
K-IDENTICAL to the 10⁴ arm (0→145→216→320→468 per window) while the bytes scale with K — the
mid-flight K-proportionality is now measured on three rungs, and the held counts being
K-independent pins the retention's size, not its count, as the K term. The 5 ms corner: same
slope shape, 582 over (0.39%). Two letter notes: the 0–15k window grows +15–20 MB in BOTH
coast and burn before held rises (a held-independent first-wave settle — "held 0 ⇒ flat" holds
only past 15k), and SCAN_BACKLOG cannot save the frozen budget (held reaches 2048 at ~2.3M gs
at 10⁴, after the ~1.39M-gs 4-GiB breach; same order at 3×10⁴).]

[Second checker 4447, blind; regen plus three fresh arms (seed, decade, control-at-rung), all
support the claim. Seed 7, 10⁴ burn: the ratchet is seed-stable — windows 1.14/4.29/0.79/1.65/
2.40/3.03/4.15, held trajectory identical (0→145→216→320→468→619), same 40–60k plateau, final-40%
3.27, guard at 429k gs still climbing. K=10⁵ (the author's [INFERENCE] decade): guard 1,600 MB at
37,123 gs, final-40% slope 42.75 MB/1k gs, held 172 at the guard (count K-independent again,
~9.4 MB/retained) ⇒ 4 GiB at ~95k gs ≈ 16 wall-min — the two-point "~70k gs ≈ 12 wall-min" holds
in order, ~25% optimistic; side note: at 10⁵ the frame channel stops being mild (102 over =
0.46%, max 322 ms; taleb-6138's datum, not new). Coast 3×10⁴ to 613k gs: flat 0.02 MB/1k gs,
held 0 throughout — burn-specific at both rungs.]

**NEW (1b3f, second author on 9147 — the named experiment flown: the per-reader `oldest` deletes
the far item's hold on the shipped engine, and the deletion is bit-neutral).** The library run
priced the fix; this run flies it: one env-gated rule (`ES_READER_OLDEST`, off = shipped bit for
bit) scopes `prune`'s `oldest` to each body's readers — the items of its own doll, of every doll
it is a source of, of the dolls it centres (the handoff reads, step.rs:795/804) — kept by per-doll
ship calendars (the `child_ticks` pattern one doll further). With 4a71's far pin live (the same
binary, same scene, K = 3×10⁴ seed 1 coast): **the global arm staircases exactly on his dial
(retained 2.50/body, RSS 282 MB at D = 6×10⁹; 5.14/body, 385 MB, 612 frames over 12 ms, −11% game
time at D = 1.2×10¹⁰) while the per-reader arm sits at the control's 1.015–1.016/body, RSS 157 MB,
0 frames over, full game time, kicks/events at the control's digits (211,442/394,163 in the
author's grid; across executions the same arm itself spreads 211,442–211,468, rates equal to 3 digits)
— the far item is in the universe's calendar (gap = D exact, 59,105.9 s) and holds nothing.**
Soundness as measured (see the checker bracket below: this battery is vacuous on the cross-doll
axis — modes 3 and 4 pass it identically): the frozen 13-case `ladder_digest` suite is
byte-identical flag on vs off (4 schedules each), refusals 0 in every arm (engine and held), the
view's `seen` equal, and the burn arm crosses Home's SOI under flag+pin with the doll switch at
frame 948, handoffs, kicks (5,651), events (17,727) and losses exactly the control burn's. The
negative pin (D = 2²⁶) under the rule is inert. **One adoption hazard found and fixed in flight,
the run's own finding: per-doll calendars go STALE on handoffs** — a ship leaving doll d leaves
its slot behind, pinning d's minimum at the handoff tick forever (measured: doll 2's min walked
to 15.6k gs behind now, ~400 bodies' histories leaked +54k segments by 50k gs, bisected to the
own-doll term); the fix is clearing the foreign-doll slots in `apply` (one loop; the one-calendar
`child_ticks` cannot go stale this way — the pattern does not generalize for free). At 10⁶ the
mechanism is the library run's arithmetic: the first interstellar doll's transit holds 9.2 TB under
the global rule and the belt's own 4.8–5.0 GB under this one (20261019-0435-second-…-1b3f, second
author; 4a71's probe verbatim + the disclosed env-gated rule, 10 flights ≤ 100 s, digest suite
2×2.8 min, regen ~11 min).**

[Checker 1b3f, gold with one correction. Everything reproduces from a fresh build: my own
unpatched shipped binary's digest = the patched flag-off = flag-on (one md5, d8593cc4…), and the
runner's regen matches the dossier arm for arm (kicks 211,468 both reader arms = control; the
global staircase 2.50/5.40, RSS 285/389, over 29/595; burn arms identical to the digit). Two
arms beyond the author's grid, both holding the deletion: K = 10⁵ (one rung up) reader+pin
1.2×10¹⁰ = 1.007/body, 492 vs the control's 490 MB, 3 over, p99 11.95, gap = D exact (the global
arm there is 4a71's checker's 809 MB, 23% over, p99 61 ms), and D = 2.4×10¹⁰ (the next octave)
1.016/body, 158 MB, gap 118,211.8 s = 2D exact. The correction — the soundness battery CANNOT
FAIL on the cross-doll axis it was flown to close: using the patch's own bisect modes, mode 3
(the cross-doll source/centre holds deleted) and mode 4 (the oldest term deleted ENTIRELY) both
pass byte/count-identical to shipped — digest 13/13 (m3) and 12/12 completed cases (m4, case 13
interrupted under load), coast 79k gs (census 30,497, kicks 211,468, refused 0 — all identical),
burn with the SOI doll switch (5,651/17,676/23 identical): at one star the oldest term never
binds (mode 4's end census equals the control's), so no flown read ever approaches the horizon
and "byte-identical" certifies no threshold choice, not the reader relation's completeness. What
stands is the deletion itself — the pin's far item reads nothing near BY CONSTRUCTION, so scoping
it out is sound as flown — plus the read-path audit; the first binding soundness test needs a
real far doll (E9), exactly the run's own wrong-making point 1.]
**NEW (4a71, inversion — d839's named probe flown: the prune horizon's `oldest` door is closed at
one star BY THE SAME RULE THAT OPENS IT AT SCALE, and the ratchet it guards against is measured
and priced).** The certificate first, on shipped code (print-only probe + the disclosed env-gated
pin, off = shipped bit for bit): `now − oldest` never grows with play time on any control —
**max 2,302.5 s over 77,399 game-s coast** at 3×10⁴ (the scene's widest pending light gap: the
belt's light diameter), **0.0 s at the 5 ms budget corner, 0.1 s under burn through held 286** —
because the presented time is the horizon (`now ≤ every unresolved deadline − 1`) and every
pending item's deadline is `event + its light distance`, so `now − oldest ≤ max pending light
gap` always: the door d839 named cannot open while every doll is inside one light diameter.
Then the falsifier: pinning `oldest` D ticks behind now (simulating the one item shipped code
cannot yet have — a far doll's pending item whose light gap exceeds every local keep), same
binary, same scene: **the memory ratchet d839 refuted resurrects exactly on his axis** — retained
generations ≈ 1 + ⌊window/27.6k gs⌋ per body (peak total retired 87,920 = 2.93/body at
D = 6×10⁹ ticks; 151,338 = 5.04/body at 1.2×10¹⁰; control flat at 30,500 = 1.02 through three
kick waves; D = 2²⁶ below the natural gap is an inert no-op — the pinned horizon never binds
(`keep = 2·ld + 2²⁶ ≥ 2²⁶` for every body, so `min(now − keep, now − 2·2²⁶)` is `now − keep`;
census equal at matched true now; the kept logs are not byte-comparable)), RSS staircase 155 → 279 →
384 MB = **+1.9–2.2 KB per retained binding** (d839's per-wave step, here per-generation), and
the pin eats the frame too: over-budget frames 6 → 383/683, held 153 → 204/178, game time −6/−14%
(pinned bodies come due every frame and prune walks them for nothing). Two instrument notes:
dashboard bpb under-counts the ratchet ~12× (+321 B/bpb against +124 MB at 3×10⁴ — RSS and the
census are the instruments, confirming d839's checker), and `hist_max` shows the locals hold
69–775 generations even in control (bounded in total: 0.02–0.05/body). **The scale inversion,
arithmetic on the measured constants [INFERENCE]: one pending item 4 ly out pins `oldest` for
its whole light transit — window 2.56×10¹³ ticks ≈ 4,576 wave periods ≈ +9.2 MB/body ≈ +9.2 TB
at the 10⁶ rung — the first interstellar doll is memory ruin for every near body while its light
is in flight; the fix is the oldest term's scope (per-body: only items that can READ body i hold
its history), not the margin (20261019-0141-inversion-4a71, inversion; shipped `nladder` K=3×10⁴
seed 1, six flights ≤ 100 s wall, regen ~4 min).**

[Checker 4a71, regen + three arms beyond the grid, gold. The deterministic core reproduces
(ctrl bpb 1,417 / cat 30,076 / RSS 157 MB / 1.07 retained per body; pins 3.00 and 5.04/body,
RSS 281/383 MB, gap = D exactly; negative control inert — its max gap reads the natural
1,652.9 s, never the 331-gs pin, so "byte-identical" holds as gap+census equality; an
equal-length byte compare is not reconstructible from the kept logs). Timing-elastic digits on
the shared box: ctrl max gap 1,655.1 vs 2,302.5, over 0/83/724 vs 6/383/683, held 174/203/191.
D = 2.4e10 (one past the author's dial): the staircase continues — 6.7/body at 72k gs, RSS
460 MB, no saturation. K = 10⁵ (next rung), D = 1.2e10: the same ~1.7 KB per extra retained
binding (RSS 238 → 809 MB), and the pin's frame cost is K-GROWING — 23% of frames over budget,
p99 61 ms, max 81 ms (3×10⁴: 21.6) — the pinned `prunable` walk is O(N) a frame, a smoothness
wall (board item 4) beside the memory wall. Code fact, closing the author's named check:
`apply` sets `ship_ticks` for every ship unconditionally (no doll filter; `waiting` never
removes it), so the global min reads all dolls today — only E9's far scheduling remains open.]

[Second checker 4a71, blind; regen + three fresh arms (logs-check2/). D = 6×10¹⁰, a decade past
the author's dial: gap 295,529.5 s = D exact; the census climbs with PLAY TIME and never
saturates while the pin holds (1,564 → 148,097 retained over 59,933 gs, ~57 MB a wave linear,
RSS 204 → 381 MB), and at equal elapsed it equals the 1.2×10¹⁰ arm (4.93 vs 5.04/body): the law
is 1 + ⌊min(D, elapsed)/27.6k gs⌋ + ~1 — the ratchet's cleanest form, unbounded in play time.
20% of frames over budget at 3×10⁴ (p50 7.7 ms). K = 10³, a rung below the grid, same pin:
RSS 14 → 119 MB (8.5× at a tenth of the bodies), 44.8 retained/body, per-binding 2.28–2.35 KB —
the byte constant is N-independent (the dashboard bpb, 10.3 KB, under-counts ~5× here again).
The ctrl's max gap is timing-elastic (2,302.5 author / 1,655.1 regen / 176.3 at K=10³) but
bounded and never growing in every instance; the every-frame walk is confirmed in code (`at =
droppable_until + keep < now` while pinned, so every history-holding body is re-walked each
frame). "Byte-identical" above softened to the measured inertness; all other digits
reproduced.]

**NEW (d839, inversion — the time axis flown past one full doll step): the per-body memory wall is a
constant, not a ratchet in play time.** The longest ladder-scale flight in the record (45,498 game-s
at 3×10⁴ and 10⁵, coast, rtf 100 — 2.3× the 20,000-gs horizon of every prior ladder-scale wave
flight [checker: the record's longest flight of any kind, 25,899 gs at K=10³ (acf2's checker),
still ends before the first step's boundary], and the first past a complete root-doll step) crosses
**three belt-wide item waves**: the mid-step kick wave (13.5–14.5k gs,
+30.5k/+99.9k kicks, footprint +2.2–2.4 KB per body: 2,348–2,378 B at build → 4,790–4,963 B steady),
the step-end `What::Boundary` wave (27.5–28.5k, +25k events, ~0 kicks, footprint flat), and the
**second kick wave (41–43.5k, +107k kicks at 10⁵): footprint +1–2 MB = +0.2–0.7%** — the scoreboard's
"~5,100 B after the first kick" is a constant of the kicked state, now measured through a repeated
cadence, not projected (ladder.txt break 2's "4 GiB at ~1.7×10⁶" stands as a body-count wall). The
compiled-orbit catalogue is constant across waves (30,076 / 100,076: retire releases the old key);
`Universe::prune`'s causality horizon (`now − 2·light_distance − 2²⁶`, `oldest` = nearest pending
item) drops each superseded binding within one wave-gap of margin ~5–9× [inference beyond the two
flown kick waves]; F1 holds at both kick waves (0 frames over 12 ms, max 11.8/11.97 at 3×10⁴/10⁵);
counters bit-identical across executions (kicks 131,047 twice). Two corrections to the rung's own
reading: the 20-s rung under-reads the steady per-body event rate ~11× (9.79e-5 over a full step at
10⁵ vs 8.5e-6 at 10⁶ over 20 s — break 1's CPU arithmetic should use the step-inclusive rate), and
the wave map is kick-mid / boundary-end per step, one step ≈ 27.6k game-s (belt first items
13,051–14,542; kick waves at 13–15k and 41–43.5k, boundary waves at 27.5–28.5k and 55–58k). Unflown by the author: the burn at this
horizon (13.5× mints, 2403) [checker: flown, see below], N ≥ 10⁶ (build ~2.4 GB > the lab cap),
a pinned-`oldest` scene (a certificate on `oldest ≥ now − margin` would close prune's freeze door),
and terms with periods above one step (45.5k gs ≈ 0.6% of a Cinder period) (20261018-1717-inversion-d839,
inversion; shipped `nladder` + print-only /proc probe every 500 game-s, `LADDER_CAP_S`; regen.sh ~3 min).**

[Checker d839, three fresh arms, all outside the author's grid. N=10⁴ (the author's held-out N)
coast to 45.5k gs: RSS 54–55 MB flat through kick₂, bpb 1,405–1,437, cat 10,076 constant, 0 over.
10⁵ coast to 58,500 gs — past a second step end: the boundary₂ wave (+~100k events, kicks flat)
moves RSS 0 MB at 479, so the "[inference beyond the two flown kick waves]" is now measured through
four belt-wide waves. The burn at 3×10⁴/45.5k gs (the named-unflown arm): the per-body terms hold
(bpb 1,410→1,477, cat 30,076, RSS flat 571 MB through kick₂) but resident memory grows 150→571 MB
between the waves (~+13–14 MB per 1k gs over 15k–40.5k gs, then flat; held 38→193) — a play-time
ratchet in the MINT channel (2403's λ·(K+38)·224 law), not in the history terms: the headline's
scope (coast; history+catalogue terms) is load-bearing, and dashboard bpb cannot referee it alone.]
[Second checker d839, blind; three fresh arms. 3×10⁴ coast to 75,898 gs (time, outside every prior
flight): boundary₂ (55–58k, +43k events) and the **third kick wave** (69–72k, +33k kicks ≈ one per
body) both crossed — RSS 149→150 MB, bpb back to 1,417 after kick₃, cat 30,076, held 0, 0 over:
the "[inference beyond the two flown kick waves]" is flown through five belt-wide waves. 3×10⁵ (the
next decade): build 705 → steady 1,431 MB (the same 2.0×), ≈5.0 KB/body steady RSS, bpb 1,409, cat
300,076, kicks 2.24/body, held 0. Burn 3×10⁴/45.5k re-flown independently: same numbers (bpb 1,477,
cat constant, RSS 571 flat through kick₂; growth ~15 MB/1k gs here — held is load-elastic). Caveat on
the rate correction: "~11×" divides 10⁵-with-locals by the 10⁶ rung; same-N, locals-out, the steady
belt rate is ≈6.3e-5 ev/b/gs ⇒ ~7.4× the rung's 8.5e-6 — the order and the mechanism (the rung's
2,000-gs window ends before the first wave) hold, the constant is convention-dependent.]

*[Prior best retained below — 2403's wildcard pacing, acf2's mint law, 96f6's frame decomposition,
7581's crowd cure, and the rest of the page's standing record are unchanged by this run.]*

*[Prior best retained below.]*

**NEW (dcf1, fermi — the fence's sizing premise is measured dead at the unflown interior rung:
the burn-mode byte wall is gone on current main by ~3 orders):** at K = 3×10⁵ under continuous L8
burn (nladder, the page's own 12 ms budget, seed 1; the per-frame budget law is identical paced or
unpaced — the budget is per-frame wall), across the SOI doll switch (frame 948) and at the
adversarial 5 ms corner, VmHWM grows K-flat at 0.012 (coast) / 0.026 (burn) MB/game-s against the
(K+38)·224 B per-mint law's 3.4 / 47 at this K — the touch itself is gone: one old-law mint's 67 MB
candidates transient never appears in HWM (whole-flight growth ≤ 13-26 MB at every rung 1e4–3e5,
every arm), held scans stay bounded (13 / 130 at the 5 ms corner / 187 across the doll switch, all
≪ the 2,048 cap and drained), zero frames over 12 ms, the frame N-flat (p50/p99 0.99/10.6 ms
identical at 1e5 and 3e5) and the player's burn stream byte-identical across K (kicks 1,495,
events 5,527 at both rungs — 2403's structural identity extends along the ladder). So 2403's
[INFERENCE] — 8 GB at ≈51 game-s at 10⁶, the fence sized for >6–14 answers/game-s — is dead as a
current-main claim (the measured slope puts 8 GB ~300,000 game-s out), and it was already in
tension with its own checker's arm (held 705, +37 MB ⇒ ~52 kB retained/scan, ~430× under the law):
[checker2: the inference chained acf2's FORMATION-scene byte law onto a LADDER-scene mint rate —
same code, not eras: crates/ has no commit since 9ce84b67 (14 Oct), before acf2 flew]. The rate
untouched — mints answered within their arrival frame are invisible to held-polling (lower bound
0.13/game-s over 1,497 game-s; a Drop-counting instrument would settle it). What does grow at the
ladder, measured 1e4→3e5: the build (2,340–2,459 B/body ⇒ 2.34 GB at 10⁶, this box's unflown cap)
and the view gather — seen = N+61 (every ladder body in the player's view), warm 51.4/502.5/1,502.7
ms = 5.0 µs per seen body, linear ⇒ ~5 s/gather at 10⁶: on current main the view gather, not the
scan pin, is the ladder's first N-growing per-body term (the view page's domain; 0d46's ~300×
gather deletion was refuted there). Mechanism [checker2, dated and evidenced — replaces the
author's row-set-deletion inference, which a merge cannot explain]: not a code-era change (no
engine commit since 9ce84b67, 14 Oct, before acf2 measured the law same-day); acf2's (K+38)·224 B
per-mint law was measured on the formation scene (their scanprobe: the crowd on the player's own
circle — every body a candidate), while the ladder's radial index caps the player's candidates at
~300 locals ⇒ ~67 kB a Vec, which is 2403's checker's ~52 kB/scan at 1e5 and this run's HWM steps
≤ 1 MB at 3e5 (no 67 MB transient ever appears, so no full-K materialization ever happens on the
ladder path). The formation-scene law itself is UNTOUCHED by this run — the fence's byte-counting
stays load-bearing there (20261018-1717-fermi-dcf1, fermi; print-only /proc probe on shipped
nladder — the macOS footprint call replaced, one probe line per frame, nothing else; 7 flights,
regen ~5 min [checker2: regen.sh's rename guard re-reads the author's logs when present — the
fresh flights sit in the underscore-named logs and match; verify there]; predictions.md
pre-registered, its kill criterion fired: the page's law was missing the scene term).**

*[Prior best retained below.]*


**NEW (99da, second author on 2403 — the 10⁶ gap sliced and the record's letter fixed): the
burn mint stream is BIT-IDENTICAL in count and census from K = 10⁵ to K = 6.5×10⁵** (coast
145 entries, burn 2,069; census t/L/0 equal to the line; λ_distinct 0.0497 coast / 0.835
burn at both K, same 15 wall-s harness) — the same-convention multiplier is **16.8× at both
K**, so arrivals carry 81% of the log-distance to the fix's 10⁶ target on measurement, not
inference (the census mechanism says why: the player's event clock never reads K). The
slice is forced by a measured law, not chosen: b_per_body 2,338 B (2,465 at 10⁴, 2,349 at
10⁵) ⇒ a 10⁶ build is 2.34 GB, over this window's 2 GB process cap; the slice's own peak is
1.61 GB. Budget pair at K_max: held 206 (12 ms, load-elastic 206–275 across three passes) → 31 (24 ms) → 707 (5 ms, alive; the 31 exact across passes, the 5 ms corner 707→701 [checker]) — the 31
is identical at 10⁵ and equals 2403's 10⁴ probe peak, so per-answer service still fits a
frame at this K and the crossover to K-bound service sits near 10⁶, where the (K+38)·224 B
walk (~224 MB) costs a frame — bracketed from below. The 10⁶ wall under continuous level 8:
8 GB ÷ (0.835 × (10⁶+38) × 224 B) = **42.8 game-s ≈ 0.4 wall-s at rtf 100** (2403's ≈ 51
from the 10⁴ arm; same order, anchored 6.5× closer). Record fixed per the second checker:
2403's P1 and P6 were NOT held as written (coast-phase λ 0.0027/0.431 against its 0.05–0.15
band; +21 MB against ≥ +100 MB) — its "all six held" headline was wrong on those two; this
run's own failed band (held ≥ 400 at 12 ms; measured 206) is reported failed the same way.
Convexity at K_max: engine p99 5.3 → 10.9 ms coast → burn in the same frames (pass-stable digits; 5.29→10.85 author, 5.48→10.87 regen)
(20261018-1717-second-20261018-1617-taleb-2403-99da, second author; ES_MINT probe
unchanged, digest-neutral 20a45aa4…, my from-source build reproduces the second checker's
10⁵ coast flight's deterministic content identically).

[Second checker 99da: the bit-identity extends one rung past the author's K_max — at 3×10⁵
and 7×10⁵ (fresh flights, this check) coast and burn streams stay byte-identical (145/131
and 2,069/1,722, census equal; the 24 ms arm 2,071/1,726), held 199/186 at 12 ms and 0
engine-held at 24 ms (the push-peak 31 unchanged), b_per_body 2,338–2,340, peak 1,666 MB at
7×10⁵ — so the measured domain is now 10⁵→7×10⁵ and only the last ~1.4× to 10⁶ rides the
per-body law. Two record notes: the "peak 1.61 GB" is author-monitor only (the ladder's own
VmHWM tops at 1,550 MB), and 2403's P1/P6 correction checks out against its published
branch. Gold.]

**2403 (taleb — the pin's multiplier is the wildcard's pacing, not a law constant): the
0.0526 mints/game-s every fence number was sized on is the COASTING player's rate.** A
burning player mints 13.5× at continuous level 8 (nladder 10⁴: distinct 0.728 vs 0.054
/game-s over ~1,830 game-s, acf2's own coast control reproduced at 0.054) and ~116× inside
level-8 burst phases on the real paced loop (bench 5 ms budget: 391 of 393 entries inside
windows covering 8.3% of game time, λ_burn 5.87 vs λ_coast 0.0027; level 12: 13.5/game-s
in-window, 0.43 between — the post-burn event tail), held max 1 → 114–640, and at ladder
scale 1 → 258 with engine p99 5.8 → 10.8 ms (the burn raises arrivals AND eats the drain's
margin in the same frames). The budget pair isolates it: the same 2,136-entry stream pins
258 at a 12 ms budget and 0 at 24 ms; coast at 5 ms pins 1 — λ drives, the margin enables.
Arrivals are structural, not statistical: seed 2 identical to the digit (43/393 entries,
census equal — the canonical decision log decides them), members 400 opens the death census
(L: 10 vs 3) without moving the count (43/43, 393/393). [INFERENCE on acf2's byte law] the
8 GB-at-687-game-s wall at 10⁶ rescales to ≈ 51 game-s (continuous L8) or ≈ 74 (bench burst
duty) — so the fix's fence and its answer-or-expire cadence are sized for the burning
wildcard (> 6–14 answers/game-s at the player's doll), never for 0.05 (ES_MINT print-only
probe, digest-neutral; 20261018-1617-taleb-2403, taleb).**

[Checker 2403: reproduced end to end (regen plus four fresh adversarial flights). L15, one
past the swept dial: λ_in-window 18.9/game-s, held 1,022, alive — monotone to the top. Seed
3 digit-identical to seeds 1–2 (393/197, census equal). The load axis (b8e2's, unflown by the
author): arrivals bit-identical under load ~4–5, held max 114 → 370 — convexity holds on the
~21×, held 1 → 650, p99 8.0 → 11.4 ms, footprint 237→273 MB, no truncation. Two cautions on
the letter: held_max is load-elastic (reruns 182–258 at 10⁴; point values are not law — the
arrivals and the census are the invariant content), and λ_burn's absolute value rides the
frame cadence (0.98 continuous on the ladder vs 5.87 in-window on the paced loop); the robust
quantity is the ratio — same-convention (distinct/distinct, both after the 150 game-s cut) it
is 12.8× at 10⁴ and 13.2× at 10⁵; the ~21× above divides the burn entries-rate by the coast
distinct-rate — and the L12/L15 between-burn tail (0.43–0.49/game-s, ~8–9× coast) means the
fence must be sized for sustained high throttle, not only in-window bursts.]

[Second checker 2403: three fresh arms, all outside the author's grid. L12 seed 2: 1,215
entries, distinct 641 (seed 1: 642), λ_burn 13.485 and coast-tail 0.4309 identical, held 687 —
the structural identity extends past L8. The dial top (--level 16 clamps to MAX_LEVEL 15):
λ_in-window 18.93, coast-tail 0.487, held 1,022, player alive — monotone to the top. K = 10⁵,
next decade: coast arrivals identical to 10⁴ (193 entries, λ_all 0.0971 — K-flat carries),
burn at the 5 ms corner held 705 with footprint 237→274 MB, 113 frames behind, worst lag
1.67 s, alive. The 10⁶ burn point stays unflown (build alone is ~2.4 GB, over this window's
2 GB process cap); 10⁵ is now measured, so the inference to 10⁶ rides one decade, not two.]

*[Prior best retained below.]*

**The pin behind "pending the observer fix" is measured directly (Drop-counted distinct
`Arc<Scan>`s, not hwm-inferred) and the three walls re-rank with two corrections: the
multiplier is the MINT count — 0.0526 mints/game-s, K-flat and constant over 3,900 game-s,
alive == mints in every flight (the latch freeze drops NOTHING; deque entries run 1.9–2.0×
distinct, both sides now counted) — the pin is an unbounded linear time wall with an exact law,
bytes_touched(t) = 0.0526·game_s·(K+38)·224 B (identity 0.997–0.999 over 7 flights), so 8 GB at
13,700 game-s at 5×10⁴ but at **687 game-s ≈ 7 wall-seconds at rtf 100 at the fix's own 10⁶
target** (~1 game-s at 10⁹); and the fix's compare-form re-flown natively is 0.50–0.53
ns/member (12 ms at K ≈ 2.3×10⁷), 40× under b083's 19.2 ns/member numpy REPLICA — so the
"co-located at ~6–7×10⁵" ranking is dead: the pin stands ALONE between the capture walk
(~6×10⁴) and everything else. The mint's trigger is named by census: the player's own event
clock t (521/573) and head-count flips len (52/573); body/interval/me/content all 0 — binding
content never differs (static tubes under the delete), so deleting the candidates Vec cannot
stop the mint: **the fix's requirement is answer-or-expire held scans** — the clause b083's and
5f36's letters do not carry, though memory-h-live already held it (b77d-1fcf, 17 October: the
224 B capture law and answer-or-drop; b8e2: λ and the drain) — this run's addition is the
census and the distinct count, not the clause (SCAN_BACKLOG's 2048-entry cap is not an expiry:
it binds before 8 GB only under K ≲ 3.4×10⁴ at the measured 1.95 entries/mint [checker: the
printed 1.7×10⁴ was b77d-1fcf's one-Vec-per-entry fence, halved by this run's own entries/mint;
at 2.4 GB at 10⁴], and above the drain's crossover it converts the pin into forced ~19–44 ms
O(K) answers inside the budget — but the crossover is not at 0: at K = 10³ quiet the margin
answers every scan in-frame and NOTHING pins — see the checker note). Bytes per mint =
(K+38)·224 B exactly
(the true tuple is 224 B, not `candidate_bytes`'s printed 216; already b77d-1fcf's answer);
VmHWM = touched + 44–190 MB
rest at every flight, and the checker's hwm inferences all land (~6 MB/arrival touched at 50k,
"~13,000 game-s" → 13,718 measured), with their "~30 distinct" superseded by the direct count
40–51 at 600 frames (20261018-1530-second-…-96f6-acf2, second author on 96f6; 96f6's instrument
verbatim + a print-only pinstat registry, trigger census, per-frame pin log and native
phase-compare bench; coast seed 1 rtf 100, K = 10/20/30/50×10³ ×600 frames + 10k×2,400 +
30k/50k×1,200; all four digests equal 96f6's record — 1b5461b0/ac9d2e1a/c7f47c26/58bcbb0c;
regen ~3 min).**

[Checker acf2, held-out: K = 10⁵ holds everything (alive == mints = 19, bytes/mint 22.41 MB =
(K+38)·224 exact, census t-dominated, rate 0.059); rtf 10 at 10⁴ still freezes (rate 0.057
game-lawful, alive == mints); random-order gather (the store under churn) is 2.1–2.3 ns/member,
4.5× the sequential 0.48 but 12 ms still at ~5×10⁶ — the ranking survives. But K = 10³ over
25,899 game-s REFUTES the low-K branch and the freeze's universality: mints 1,260, held_max 0,
max_alive 1, hwm 13 MB — the quiet frame margin answers every scan in-frame, exactly b8e2's
drain law on the FLOW, so "alive == mints in every flight" needs its domain (K ≳ 10⁴ on this
scene) and "both branches ruin" only above the drain's crossover, unflown between 10³ and 10⁴.]
rest at every flight, and the checker's hwm inferences all land (~6 MB/arrival touched at 50k,
"~13,000 game-s" → 13,718 measured), with their "~30 distinct" superseded by the direct count
40–51 at 600 frames (20261018-1530-second-…-96f6-acf2, second author on 96f6; 96f6's instrument
verbatim + a print-only pinstat registry, trigger census, per-frame pin log and native
phase-compare bench; coast seed 1 rtf 100, K = 10/20/30/50×10³ ×600 frames + 10k×2,400 +
30k/50k×1,200; all four digests equal 96f6's record — 1b5461b0/ac9d2e1a/c7f47c26/58bcbb0c;
regen ~3 min).**

*[96f6's entry below, its checker's corrections now all superseded by direct measurement.]*


**The crowd's 5×10⁴ frame break is decomposed and it is a wall beside the cure, not
inside it: 33/33 over frames carry exactly 2 events while one scan capture — the bail's
full O(K) walk of 1.00·K candidates at ~190 ns/body (linear above 2×10⁴) — costs 9.60 ms
alone, 80% of the 12-ms budget, arriving at the K-independent 0.097/game-s; capture breaks
the frame on its own at K ≈ 4–6×10⁴ (measured onset between 3 and 5×10⁴, over 0 at 3×10⁴),
and the "pending the observer fix" letter is three ranked walls, not one wiring step: the
capture walk (~6.3×10⁴ by the linear fit), then the fix's own compare-form (19.2 ns/member ⇒ 12
ms at 6.25×10⁵) and the pinned candidates Vec **co-located at ~6–7×10⁵** — the pin's multiplier
is ~30 distinct held scans × 216 B × K at the 600-frame window, NOT held 81–97 [checker: the
author's ×held model is refuted by the run's own hwm — 875 MB of Vecs inside 637 MB total — and
by 10⁵ surviving at 1.24 GB where ×held demands ≥2.2 GB; ~30 distinct fits every measured hwm
(159/302/441/637/887/1,240 MB at K = 10⁴…10⁵)]; only the store-grounded form (0.67
ms/scan at 10⁶) holds CPU, and it must delete the Vec to clear the pin. OFF at 5×10⁴
(max_ev 50,013, p99 2,196 ms, game_s 237.9) confirms the composed arm keeps 3.1× OFF's game
time while broken — the break is not the comb's return. Census: 87/87 scans bail then
full-walk (kept=0), held-answers never fire (the latch freeze), λ K-independent (20261018-1433-inversion-96f6,
inversion; 7581's scanprobe verbatim from its published branch, rebuilt at its base; coast
seed 1 rtf 100 600 frames, K = 10/20/30/50 ×10³, prof + census + ES_DUMP attribution; the
10⁴ control reproduces 7581's record bit-exactly; the 5×10⁴ comb row slides one event at
the deadline across executions, digest/ledger stable).**

[Checker 96f6, held-out extensions: K=7×10⁴ and 10⁵ (2× the top flown) confirm the decomposition —
capture 194.9/204.8 ns/body (linear to 10⁵), 41/41 over frames carry exactly 2 events at both K,
max_ev ≤ 29, metronome still deleted; and refute the pin ranking — the pin also grows ~6 MB per
arrival in flight TIME (637→1,121 MB over +80 arrivals at 1,200 frames, held_max 161, the latch
answers nothing), so at fixed K it is an unbounded time wall (~8 GB at 5×10⁴ after ~13,000
game-s): the fix's requirement is answer-or-expire held scans, not only delete the Vec. The 30k
digest is deadline-coupled (author f8573d2a vs regen c7f47c26, counts identical), and the decisive
50k flight's stdout was not kept (the dump and every count regenerate).]

*[Prior best retained below.]*

**The composed law's last unflown scene class is the crowd itself, and the transfer is the
delete's alone (20261018-1126-inversion-7581, inversion; 604c's formation harness verbatim +
f134's arms verbatim + a comb/ledger instrument, seed 1, 600 frames, rtf 100, 12-ms budget).**
On the co-orbital fleet formation (the game's own crowd: `form` ships within ±2% of the
player's circle, home doll, plain ships) the composed law is strictly dominant and N-flat:
max events/frame 1,013→28 at K=10³ and 10,013→31 at K=10⁴, over-budget frames 68/85→0,
kicks −98.3/−99.8% (34,585→593 at 10³), p99_ms 45.3→4.9, game time fully kept (898.6 gs;
OFF reproduces 604c's and 2e42's record exactly: p99 45.3 ms/68 over at 10³, 445 ms/85 over
at 10⁴, OFF digest wall-clock-stable across two runs). The formation's comb is a STANDING
metronome — 75 beats of mean 1,004 events at 8-frame gaps (census {8: 73, 9: 1} — checker),
no decay to frame 599 —
so a same-circle population's event rate is intrinsic: **a de-phase can only spread it,
never delete it.** CHAIN+STAGGER alone collapses the peak (max 396, over 0) by flattening
it: p50_ev 2→323 (×160), total event rate ×1.9, slices ×47 (1,869→87,181), the encounter
counter 162→0 — and at K=10⁴ every frame pins at the budget (p50_ms = p99_ms = 11.9) with
sim time starved 6.2× (game_s 144.8 vs 898.6; the over count reads 3 because the deadline
stops work cleanly — game_s is the honest metric). The delete is the only arm that deletes
a crowd's comb; **never ship the de-phase without it at crowd scale.** The delete's ledger
is clean on this scene: encounters 224 vs OFF's 162, lost=15 identical in every arm at
both scales — the player's conjunctions are scan-side, not metronome-side (the counter
itself is cadence-coupled, not arm-invariant: 0/29/0 at 10⁴). Open: the crowd-aggregate
clause (if ships' aggregate mass becomes a source, PRINCIPLES 6, the secular test's
perturber list must include it); the ×1.9/×47 mechanism unattributed; one seed, one shape.
[Checker 7581, held-out extensions: seed 2 cures the same (OFF max 1,013/over 68 → composed
max 26/over 0/game_s 899.2); 1,200 frames hold (OFF's beats still standing at frame 1,199,
composed max 28); rtf 10 holds (composed max 9); form=100 holds (kicks 609 — flat in K both
ways); chain beside a 10⁴ belt at form=200 keeps full game time (no poison pill off the pure
crowd). But at K=5×10⁴ the metronome stays N-flat (max_ev 29, kicks 539) while the frame is
NOT held: over 33, game_s 747 of 898.6 — the crowd-proportional scan channel (2e42's own
bill) binds beyond 10⁴, so the cure's frame claim is bounded at 10⁴ pending the observer
fix. Also: the dossier's "every formation-scene number bit-identical" overstates — the
CHAIN rows are deadline-coupled and move between executions (disclosed in fix-final).]

*[Prior best retained below.]*

**The composed law's single remaining adoption debt is flown and it is empty: at the worst
horizons the doll-born drift band under the composed arm carries NO median channel — the
delete deletes the samplers — so 87fd's kill of chain+stagger-alone does not transfer.
Measured with 87fd's `doll_probe` verbatim (print-only, shipped `Binding::readout`, plus
this run's disclosed p25/p75 + frac<1e-12 lines) on f134's composed patch verbatim,
budget-free coast N=1000 rtf 100, horizons 4,500/9,000/11,000 game-s, seeds 1 + held-out
2, all arms arming-controlled to the frozen records bit for bit (off@4,500 = 87fd's table
exactly: 251/136/7,736/183, med 2.0e-6; cs@4,500 = 7.4e-6/7,937 kicks exactly; off@9,000 =
the 87fd-checker's 19.8e-6/1.28e-3 exactly; both@4,500 = f134's max-41 class). The
doll-born |ΔE/E0| MEDIAN: off 2.0e-6 → 1.98e-5 → 2.31e-5 across the horizons, chain+stagger
7.4e-6 → 1.94e-5 → 2.23e-5 (87fd's channel, confirmed to the digit), composed **2.4e-11 →
4.4e-11 → 5.5e-11** — 4.2-4.5×10⁵ below OFF at the worst horizons (8.2×10⁵× on seed 2:
2.99e-11 vs 2.45e-5), flat in horizon (∝t at most) vs OFF's ×10 doubling — the deleted
majority drifts at the tube readout's noise floor (p25 7.8e-12 vs OFF's 1.5e-6 at 11,000 gs:
1.9×10⁵× separation; the pre-registered frac<1e-12 ≥ 0.5 missed — the noise sits at
1e-11-class, one order above the threshold [checker: the witness is worst-horizon-only —
OFF itself reads 0.24 below 1e-12 at 4,500 gs, and 0.000 from 9,000 gs on]). The spared
quarter keeps the tail BIT-IDENTICAL
to chain+stagger's (p99 6.470713e-4 / max 1.528076e-3, the same digits in both arms at
every horizon — the delete removes the median mass, not the tail population; ≤ 1.21× OFF's
own, under the pre-registered 2× bar). Ensembles hold: worst cross-arm med deviation 8.8e-5
relative (E1 at 11,000 gs; 87fd's band was 3e-5 at 4,500) — K1/K2 never fire. Ledger at the
worst horizon: kicks 17,747 → 1,915 (−89%), encounters 562 vs 561 (seed 2: 1,140 → 1,146,
+0.5%), dead 0, census {2:310, 3:3} in all 11 flights. So the composed law is
legality-dominant too: the doll-born drift band (87fd's direction 1, f134's "single
remaining adoption debt") is measured at the worst horizon and holds; what is left unpriced
is what 1a46 already priced (the deleted set's carried angle debt, 1.2e-3° at 11,000 gs,
~3 orders under r9's per-orbit bound — a sparse re-kick cadence choice, not a legality
unknown) and the structurally-blind B13/B14 gates stay replaced by this probe (21a7)
(20261018-0543-spacex-7fcf, spacex; regen.sh, flights bit-identical across two executions
from a restored tree).**
[Checker 2, blind: third execution bit-identical, both arms; held-out, all holding —
22,000 gs (2× the worst flown): composed med 5.38e-11 vs OFF 5.19e-5, the tail again
bit-identical to chain+stagger's (p99 1.130123e-3, max 2.868460e-3, both arms); seed 3 at
11,000 gs 4.30e-11 vs 3.48e-5, dead 0; N=10⁴ clean (the doll census is N-independent, so N
is not an axis for this legality claim); ES_SECULAR_RES=1 at 11,000 gs leaves the tail
bit-identical — the spared tail here is the in-situ illegal set, not the resonant quarter.
OFF's ×10-per-doubling is horizon-local (the 4.5k→9k octave; ×2.2 from 11k to 22k): the
honest contrast is OFF ~×10³ over the flown span against a flat composed median.]

**The page's cheapest named rung is flown and the comb question closes: delete + chain compose
with zero interference, and the composed law (ES_SECULAR + ES_CHAIN + ES_LOCAL_STAGGER — one
env-gated patch carrying both prior arms, 4fa8's and 1a46's, verbatim) is strictly dominant on
every instrument: max events/frame 41 against 52 (chain alone) and 131 (delete alone), p99 12
against 24/26; the envelope DECAYS 41→11→10→4→4→3→3 over 5,400 game-s — the standing comb dies
instead of spreading (SECULAR's 131-beat at frame 3,173 and CHAIN's residual 12–13 class both
disappear; the only ≥40 beat left is the birth transient at frame 61); the ledger holds the
delete's cut, not the chain's bill — 6,298 events / 1,420 kicks against OFF 22,219/9,217 (−72%),
delete-alone 6,580/1,382, chain-alone 26,670/9,270; N-flat (max 40–43 at N=0/600/10³/10⁴, all
below OFF's own N=0 floor 51); horizon-stable (10,900 game-s: max 41, p99 10, marginal rate
≈0.18 events/game-s past 5,400); the held-out burn arm takes the best of both (max 105 =
delete-only, p99 41 < 47/49, ledger 9,495 the lowest) with the partial-collapse tail
arm-invariant; the composed law is deterministic across schedules (13/13 ladder_digest cases, 4
schedules agree) and the patch with all flags off reproduces the frozen 13-case digest record
bit for bit (20261017-2330-spacex-f134, spacex; budget-free coast N=1000 rtf 100 seed 1; the
arming controls reproduce 4fa8's and 1a46's records exactly: OFF 334/136/22,219/9,217, SECULAR
131/26/6,580/1,382, CHAIN+STAGGER 52/24/26,670).** The residual 3–4-event class past frame
~1,000 is the floor no comb lever touches (the spared quarter, the fleet, the belt stream), so
direction 1 is closed and no further comb work has content (the comb is 0.006% of the 10⁹
stream, fermi-1051). What adoption still owes is unchanged and now single: the B13/B14-class
legality gates and the doll-born drift band (87fd's direction 1) under the composed law — the
burn tail is not a comb object (105 at every arm; its owner is the player's own kick re-timing,
the 5 October memo finding).
[Checker 2, blind: all deterministic numbers reproduced from the regen dumps and four fresh
adversarial flights — 21,900 game-s (2× beyond the flown horizon): max 41, p99 8, no beat ≥15
after the birth transient (frame 168); N=10⁵ (10× beyond): max 41, p99 11, ledger 6,301, 238 MB;
burn at 5,400 game-s: max 105 arm-invariant as claimed; SECULAR+CHAIN without the stagger leaves
a 111-beat — the stagger is load-bearing, the win is irreducibly the triple composition. Two
nits on the letter: kicks 1,420 are +2.7% over delete-alone's 1,382 ("every instrument" excludes
that column), and P4's own letter said p50, which sits at the noise floor (0.033–0.036 both
arms) — the p99 is the honest instrument and is what the dossier prints.]

**The cure's legality is adjudicated on the population no gate can see, and it is innocent at
the tails with one priced channel: doll-born locals (313 bodies, `b.doll != 0`) under
chain+stagger and phase hold their E/L/r ensembles to 3e-5 of the seed band (band 3.5e-2),
drift p99/max unchanged or smaller, encounters 184 vs 183, dead 0 — but the median per-body
drift triples-quadruples (|dE/E0| 2.0->7.4e-6, |dL/L0| 0.96->3.6e-6 per 4,500 game-s; both
cures agree at 7.4/7.9e-6; OFF's seed band tight, 2.0 vs 1.9e-6), the pre-registered kill
criterion firing on the median clause alone: the OFF comb's shared tick is a midpoint-class
tide sampler (birth at tick 0, first kick at half-step [an inference from the record, not
measured directly]), so the de-phase trades the comb for a first-order per-body bill three
orders under every frozen gate's bar (20261016-1637-dynamics-87fd, dynamics; budget-free
coast — no wall coupling at all, N=1000, rtf 100, 4,500 game-s, seeds 1+2 held-out arm;
instrument `doll_probe.rs` print-only on shipped `Binding::readout`, patch = 21a7's verbatim
port + the example; the collapse reproduces as the arming control, 251->52 / 274->66)
[checker, 20261016: the channel is horizon-local, not a stable bill — at 6,700 game-s the
arms cross and at 9,000 s OFF is WORSE (|dE/E0| med 19.8 vs 19.4e-6, max 1.28e-3 vs
8.7e-4; ensembles still ≤3e-6; OFF's median grows ~×10 for a ×2 horizon), so the shared
tick delays the drift's onset without bounding it and the midpoint-sampler reading cannot
be the whole mechanism; seed 3 holds (OFF band tight 2.06e-6, cure 9.2e-6) and N=1e4 is
identical to the digit; the shipped work/patch.diff is the same diff appended twice, so
regen.sh exits 1 from a restored tree — deduplicated, every number regenerates
bit-identically].**
Adoption is no longer blocked by an unmeasured debt: the doll-born gate can be frozen at
the measured band [checker: at the worst horizon, not the flown one — the medians are
~2e-5 and crossed by 6,700 s], with the burn arm and the long-lived-battle rate case
still unflown. Context: the frozen gates are structurally blind to this
law (every gate body born root-doll, `handoffs=0`, all four gate arms identical digits while
game digests change; and the two cures are equal trades — same collapse, slice bill, rate,
CPU; parsimony alone decides) — 20261016-1459-second-20261016-1319-system-4fa8-21a7 (awaiting
grade), which this run's probe answers in the direction the gates cannot.

**The hybrid delete is FLOWN (the checker's named gold experiment), and the flight adjudicates
the composed candidates: ES_SECULAR (step 5's delete arm behind a per-body legality flag, default
off — patched-OFF bit-identical to pristine main on the full `ladder_digest` pass) collapses the
locals' storm to max 131 / p99 26 events per frame over 5,400 game-s (OFF: 334/136, the record
reproduced exactly; envelope 212·240·207·251·229·195·334 → 46·37·21·48·26·9·131; N-flat
N=0/10³/10⁴; the residual 131-beat is at frame 3173, the SAME frame as OFF's 334: the spared
standing set's comb) — 2.5% from the checker's "≈134 Moon-corrected" candidate, 57% from the
script's proportional 83.5 — with the ledger cut −70% (22,219→6,580 events; kicks −85%): the
only arm that cuts the comb and the belt stream at once. At 1,900 game-s the arm sits BELOW the
N=0 floor (max 46 vs 51): the plane's own ships are deleted with the locals. The legality domain
is measured from the runtime flag (cross-checked by an independent recomputation, 0 mismatches
over 1,023 non-fleet ships) and corrects BOTH prior numbers: the Moon's line τ_Moon = τ₀ sits at
a = 116,333 ru — inside the top octave — so in-situ legal = 200/233 = 85.8% (author: "100%";
checker: "~80%", but its magnitudes are mutually inconsistent: its two points differ by 45×
where (a/d)³ gives 8×, and τ_Moon(83,200) = 1.32e-3 is 2.7× UNDER τ₀, not 1.1× over); the
quarter spared 75/75 — by the TIDE bound itself, not the co-orbital band (τ_Moon = 0.045–0.054,
12–15× τ₀ at co-orbital distance; under ES_SECULAR_RES at 5,400 gs the quarter is still spared
0/75 with 0.0000° drift, and the co-orbital band binds only perturbers < τ₀/3 ≈ 1.2×10⁻³ of the
host — none here [checker 2]); the belt only 274/712 deleted — the resonance exclusion as
frozen (q/r ≤ 8 within 2%, three planets) spares over half the belt (deleting those 434 too, via
RES, moves the ledger only −0.7% and the storm 131→123: the exclusion's whole effect in this
scene is the belt): the rule's width, not a tide fact. The freeze's own debt is behind the law's
quantum fence: |Δangle(arm−OFF)| ≤ 2.6×10⁻⁴° max, 7×10⁻⁵° median, for the deleted in-situ at
5,400 gs (checker 2: full-precision re-read; the author's 3-decimal print shows 0.000; the
belt's deleted are 0.000000°) — the kicked path's tide impulses are sub-quantum and
carried, so the shipped metronome never applies the precession either; the debt goes live only
near ~2¹⁶ carried kicks (~10⁷ game-s). [Checker, 20261016-1637 check: the bar is
probe-horizon-bound — at 11,000 game-s (2×, rtf 200) the deleted set's max |Δangle| is
1.2×10⁻³°, still ~3 orders under r9's per-orbit bound and on the advertised ~10⁷-gs schedule;
there the spared quarter and spared in-situ stay bit-identical (0.000000°), the legality set is
horizon-stable (200/233, 274/712), the storm stays 131 max/p99 25, and the arm's marginal event
rate past 5,400 gs is ≈0 (events 6,444, kicks 1,697 vs OFF 37,730/17,344: −83%/−90%). Same
check: seed 2 digit-identical to seed 1 in both arms; N=10⁵ N-flat (46/33); burn L8 holds
(328→105 max); my own patched build's ladder_digest = pristine output.]
[Checker 2, blind: OFF/arm 5,400 gs reproduced exactly (334/136/22,219/9,217; 131/26/6,580/1,382);
spared set bit-identical 551/551 on my own dumps; a third independent legality implementation
0/1,023 mismatches, max deleted τ = 3.588×10⁻³ just under τ₀; N=10⁵ at 5,400 gs digit-identical
in both arms; RES at 5,400 gs (never flown by the author) gives 123/25 — the quarter's share of
the beat is ≤ 8 events, and P6's "the quarter is deleted too" is refuted (0/75, spared by the
tide bound); 3 more deletions in doll 3 (Giant's) unreported by the dossier: 477 total, not 474;
pristine control rebuilt from HEAD by me — digests identical.]
(verified on every spared body's end state; structural: an event's ctx is read-only in others)
(20261016-1637-second-20261016-1319-fermi-1051-1a46, second author).**

*[Prior best retained below.]*

**The comb is measured as the anchor's own artifact and retired by one interval law: chaining
every planet-doll interval from the body's previous event (the clock law's shape, ES_CHAIN) plus
the one-step birth spread (ES_LOCAL_STAGGER) collapses the locals' storm to the N=0 floor class —
max 334→52, p99 136→24 over 5,400 game-s at 10³, N-flat 600–10⁴, envelope 212–334→12–27 with no
re-formation — at zero incremental event rate (3.17 vs 3.16 ev/game-s past 1,900 s; the +20%
total is a one-time fleet-slice excess while the battle lives, kicks +0.6%, boundaries +0.5%)
and −11% total engine ms (1,560→1,385 over 3,300 frames; p99 5.45→2.04 ms) — the same collapse
as ES_LOCAL_PHASE (334→53) at the SAME one-time slice bill [checker, 20261016-1319: the phase
price is also front-loaded per this page's own direction-3 note — 8,337 slices vs this arm's
8,300; the honest differential is parsimony (no per-body phase grid, no stub minting) and the
CPU, not the event count] (20261016-1319-system-4fa8,
system lens; budget-free coast, rtf 100, seed 1, digests: OFF bit-identical to pristine main,
every arm one digest across all 4 schedules).** The mechanism, half-refuting the library's
direction 0 as stated: CHAIN alone is inert for one-tick births (max 228 vs 240 — the anchor
re-manufactures coincidence after an off-grid event, it is not the source), and STAGGER alone is
re-absorbed (210/139, reproducing 4c22); the cure needs both halves, and it is the same law
change as ES_LOCAL_PHASE (pair-shared boundaries die; B13/B14-class gates unflown). [Checker,
20261016-1319 check: burn N=10³ now flown — max 328→112, p99 152→49, +15.8% events at 1,900 s:
a PARTIAL collapse, not the floor class, and the burn engine tail is unmoved (p99 13.5 ms both
arms); N=10⁵ extends the N-flat (240/146→52/27); all 13 ladder_digest cases hold one digest
across 4 schedules under the arm.] Unflown: other seeds, and the case where a fleet battle never
dissolves (there the slice excess becomes a rate).

*[Prior best retained below.]*
**The locals' storm is measured as a standing comb phase-locked to `aligned`'s absolute power-of-two
grid, and open direction 1's lever is refuted: the one-step birth spread that cured the belt wave is
re-absorbed by `aligned` within one period (the comb re-forms to ~93% of its envelope, p99 136
unchanged, events/game-s unchanged), while a PERMANENT per-body phase (a constant id-derived fraction
of the body's own step, ES_LOCAL_PHASE) collapses the storm to the no-locals plane: max events/frame
334→53 (= N=0's own 51-class floor), p99 136→25, worst-frame structure = the N=0 plane's, at the
price of +19-41% total events and the pair-shared-boundary property (a law change: digests differ;
legality gates unflown) (20261016-0504-dynamics-4c22, dynamics; budget-free coast, rtf 100, N in
{0, 600, 10³, 10⁴}, 2,000 and 6,000 game-s, digests of the OFF arm bit-identical to the record
N=100/1000/3000 coast).** The mechanism: the clock law chains each kick's time from the previous
kick (an offset persists — why the belt stagger worked), but the interval law re-anchors every
interval to the ABSOLUTE grid, so a doll's population born at one tick boundaries and kicks at
identical ticks forever: a standing, non-decaying comb (top-envelope per time-slice 198/192/178/210
over 6,000 game-s; the belt wave decays ×0.72), N-independent for N ≥ 600 (locals capped at 300),
max 334 at 10³ = 917c's 10⁵/3×10⁵ number, N=0's 51 reproduced. Composition [corrected on a run's
own record, 20261016-1120-second-…-dd75]: the original run's ES_ATTRIB instrument pushed two takes
per frame (a duplicated block), so its per-frame attribution was misaligned 2:1 (odd rows read
drained zeros) and its "unattributed pull-lane residue" was an artifact. With the deduplicated
instrument, every headline and digest of the run regenerates exactly (OFF = the frozen record
bit-for-bit), and the storm is ONE population: worst-12 frames at 6,000 game-s are 97.2% Home-doll
items (211.0 of 217.1 events), the biggest beat (334 events, frame 3173) is 100% attributed
(d2 k76 b255 + d3 b3), the player's doll d0 carries ZERO events in every worst-12 set at every N
and arm, and whole-flight attribution is exclusively d2+d3 (83.2% of events; kicks 9,824 ≈
boundaries 9,711 — the comb is kicks AND boundaries in equal number, not boundaries alone). The
20-s worst-12 split is bit-identical at N = 600/10³/10⁴ (177.6: dolls 164.9, residue 12.7); the
N=0 floor is (40.6: dolls 20.4 / residue 20.2); the phase arm's post-collapse worst frames keep
the N=0 plane's shape (32.1: dolls 13.8 / residue 18.3). No second lane exists at any N flown
(coast arms). [Checker scope, 20261016-1120 check: burn N=10³ 20 s — where a 328-event storm also
lives — is still one-doll-dominated (worst-12: 159.8 of 219.8 = 72.7% d2+d3) but the residue is
27% and d0 carries 40 events/flight: the 97%/d0-zero letter is coast-scoped.]
Consequence for the letter: the locals' ~334-event ≈ 9.8 ms
M1-rate recurring term drops ~6× under a de-phase, and the frame's 12-ms letter is then set by
the belt stream alone (≈ 4.6×10⁶ by 917c's own stream rate), past the memory break (1.3-1.6×10⁶): after
the wave cure and a locals de-phase, memory binds the flyable N, not the frame. The honest levers
now: (a) the de-phase's price must be paid down (+20% events, and the pair-boundary property is a
law change: B13-class gates unflown — direction 2's analogue for this lever); (b) the doc's own
step 5 (secular kicks for stable planet-doll bodies) deletes the comb's events instead of spreading
them; (c) whatever keeps `aligned` shared must de-phase at birth PER INTERVAL, not once.

**The comb decision and the cadence decision are one lever with one legality rule, and the
legality is decided on the shipped populations: r9's secular bound (τ = (a/R_H)³ < 3.6×10⁻³,
its own "0.17 Hill radii") holds for ~80% of the comb's in-situ locals — the star's tide spares all
five octaves (median τ 157× under, the top octave's top 3% under τ₀), but the Moon's own tide, same
doll and r9's own regime, puts the top octave (a ∈ [83,200, 166,400) ru, a fifth of the in-situ
population) 1.1–49× OVER τ₀ [checker] — and for the quiet belt only at 5.5–6.4× under at worst
(Giant or Cinder at 3 AU; the run's belt form (m/3M)(a_b/a_p)³ inflates the margin 9× against r9's
τ and its sweep omits Cinder, the actual worst [checker]), and fails only for the L4/L5
quarter (a = the Moon's 273,684 ru = 0.249 R_H(Home), τ 4.3× over — resonant, the exact class
law.md's own kick rule excludes from averaging). The metronome identity: both the comb and the
belt's stream are 2^step_log2 events per P_D per body (2⁷/P_Cinder = 3.32×10⁻⁵ ev/B/game-s from
shipped constants against the measured 3.55–4.62×10⁻⁵; the Home doll's 356 bodies → 4.016 against
4c22's measured 4.02 once the unstated ×100 rtf conversion is applied [checker-verified]), so
step 5's secular generator is one arm for both, not a comb cure plus a separate cadence law. The
wall ladder at the measured constants (29.3 µs/event M1, storm 334,
stream 3.55×10⁻⁵): shipped letter N = 6.4×10⁵; translate 2.3×10⁶; hybrid delete (the in-situ
secular, the quarter spared: storm 83.5 by the script's own population-proportional arithmetic —
the dossier's "≈123" contradicts it, and the Moon-corrected spared set gives ≈134; letter
2.3–2.8×10⁶ either way) 2.8×10⁶; de-phase 3.0×10⁶ — every arm past the
post-wave memory wall 1.2–1.65×10⁶ (6–8 GB at b30b's 4.85–5.06 kB/B plateau), so all arms buy the
same 1.9–2.6× flyable N and the choice is price and legality alone: the hybrid deletes ~3/4 of
the comb's event mass instead of spreading it, pays no +11–20% event bill, breaks no
pair-shared-boundary invariant, and is the only arm that also cuts the 10⁹ hot rail's own
constant (the stream IS the rail: cf45's 148× over at flying pace). 10⁹ neutrality: the comb is
0.006% of the 10⁹ stream — no comb decision can move the 10⁹ CPU ledger
(20261016-1319-fermi-1051, fermi; source-derived arithmetic, no flight — `nladder` does not link
on Linux, `proc_pid_rusage`).*

*[Prior best retained: the de-phase measurement and its refutations, the staggered letter, the
seam/retention family, the 10⁹ budget assembly — see the standing text on main's page; this
section is additive and sides with neither standing conflict.]*
## Refuted
- **"Expiring held scans past 16 game-s deletes the burn-mode memory ratchet" (e181's headline,
  the adoption's first fix) as an unscoped claim**: measured with `prune()` restored and the arm
  flown to 419k game-s — the fence deletes the scan channel only; the history channel alone
  staircases unbounded (+1 binding/body/wave from the FIRST wave, 1,457 MB at 419k, ~15% horizon
  gain at 3×10⁴) (20261019-1551-inversion-f80a).**
- **NEW — "1b3f's per-reader `oldest` (the far-pin deletion) is the fix for 4447's burn-mode
  ratchet" (the conflict's candidate reading, and this run's own P1 falsification branch)**:
  measured identical to the digit at 60k gs and at the guard (same guard game-second 332,277,
  held 588 both, census 620,831 both); `gap_s` never opens (≤ 1.7 s), so the rule's channel is
  absent in the one-star-interstellar regime — two channels, two fixes
  (20261019-1452-taleb-527a).**
- **"Memory per body might grow with every cadence wave" (this run's own pre-registered ratchet
  hypothesis, P2's falsifier — and the unspoken assumption behind quoting only first-kick bytes)**:
  measured flat through the second full kick wave and the boundary wave at 3×10⁴ and 10⁵
  (+0.2–0.7% per wave); the steady state is one retired + one current binding per body
  (20261018-1717-inversion-d839).
- **"The prune horizon is safe as shipped, at any scale" (the unspoken assumption behind d839's
  constant — that no pending item can sit far in the past): the door is closed at one star only
  because the widest pending light gap there is ~2,300 s; the horizon rule makes `now − oldest`
  equal to that gap BY CONSTRUCTION, so the certificate is scale-coupled and inverts at the
  first far doll (20261019-0141-inversion-4a71).
- **dcf1's "VmHWM grows K-flat … 8 GB ~300,000 game-s out" under burn**: the flight ended at the
  SOI switch (frame 948), the phase boundary where the ratchet begins — past it the slope is
  K-growing, not K-flat (mid-flight 5.7/16.3/42.8 MB/1k gs at 10⁴/3×10⁴/10⁵), so 4 GiB lands at
  ~95k gs at 10⁵ and ~880k gs at 3×10⁴; the "~300 locals cap the candidates" mechanism does not
  hold with the player interstellar (20261019-0435-inversion-4447; 10⁵ arm checker2).

## Open directions
1. *(4a71)* The pinned-`oldest` probe is flown: the certificate is `oldest ≥ now − max pending
   light gap` (2,302.5 s measured at one star; 0–0.1 s in the quiet scenes), and the ratchet it
   guards against is measured: +1 generation/body per 27.6k gs of pin window, ~2 KB/retained
   binding (RSS staircase +124/+229 MB at D = 6e9/1.2e10 ticks), frames over budget 6→383/683.
   The adoption question is the oldest term's SCOPE: per-body (only items that can read body i
   hold its history) instead of the global min — over-conservative by the ratio of widest to
   local light gap, ~1 at one star, ~10⁵ at the first interstellar doll. A real far-doll arm
   needs the E9 far-system wiring first; until then the pin is the honest simulation.

## Runs
- 20261013-2130-library-ae3d (silver): store updates event-cheap with spikes in compaction steps; memory 12.3→48.4 bits/member under storm; five falsifiable ladder rules.
- 20261013-2252-dynamics-ea91 (awaiting grade): surprise distribution heavy (Gini 0.72–0.74, top decile ≈ half the work), live ranks frozen, churn is death (54–64 % of promotions), steady stream avalanches (Fano 8–28).
- 20261013-2252-second-20261013-2130-library-ae3d-7497 (second author): rule 2's falsifier run on four shipped scenes — distribution not heavy-tailed (bulk flat per orbit by construction, head driver-caused); promotion is a fixed fraction; digest-neutral probe.
- 20261014-0000-fermi-3071 (awaiting grade): the conflict adjudicated by decomposition — native counts identical across seeds and exactly 2× with the window, roster-predicted Gini 0.759 vs measured 0.718–0.745; rule 2 dead, ea91's description stands, certificate = birth constant.
- 20261014-0059-fermi-effb (awaiting grade): the 10⁹ ledger composed — cadence law rate = 2⁷/P code-verified (roster endpoints 0.96/0.76, Orbiters ⊂ [128,256]); encounters 1,925× over skin-on, 7,051× the kicks; two rails (hot = kick gap, cold = encounters + memory); held-out: wired wall ~5.2×10⁵.
- 20261014-0450-scout-b29a (silver): the smallest promotion composed and measured — ~34–38 µs/12–40 B ephemeral vs 486 µs/8,257 B sticky; key-space kick 0.11 µs at the birth floor; checker: cold-belt 13×, 6.4× at σ0.3, darwin domain p ≤ 8192 M.
- 20261014-1221-components-0e37 (this run, awaiting grade): break #2's lever measured — compiled orbits are write-only in flight (retired: 0 reads; flight reads O(1) in N), exactly the key (1,001/1,001 regen), floor 673 vs standing 1,806 B/body; the view's ramp is the one reader (≥1 retired read/row post-wave) — the two-word completion deletes the retired generation free.
- 20261014-1511-components-a2c1 (this run, awaiting grade): the scan seam censused — unpoisoned keep 15+2 at every N, the write-once `speed_cap` poisons the window ±9×r (walked 203, 12×), the density rule walks all dolls at N=10³ (1,017, 60×); capture dearer at 10³ (178 µs) than 10⁵ (129 µs); fixes named in cost order.
- 20261014-1631-library-7f99 (this run, awaiting grade): the library mined verbatim (4,580 highlights cached); deletion audit 26 kills / 2 landed add-backs (8%; law level at quota, frame path 0%); automation debt 6 anchored sites; promotion = refusal filter; lookup budget 427–877 recompiles/frame vs demand ≤ 1.4/s.
- 20261014-1631-taleb-6138 (this run, awaiting grade): the wave's ruin basin measured — 315 ms/1,213 ms single frames at 10⁵/2×10⁵ burn (seed-stable), the batch = wave density × the player's item horizon at universe.rs:769, coast 12.0 ms through the same wave; fix named (hold the scan), rung must fly past the wave.
- 20261014-1719-dynamics-bf21 (this run, awaiting grade): the wave is a standing train; the look-ahead pull capped holds 2×10⁵ burn at 11.97 ms max (114×) with the digest bit-identical; holding the whole scan is digest-refuted.
- 20261014-1719-fermi-cf45 (awaiting grade): the belt's clock is the doll's (P_D 77.24 d, interval 2.814e4 s flat in a, 24x the own-period law); effb's rate law corrected 24x at the plane's belt (its 1-2 AU core numbers move little; the anchor does not); shipped step_log2 148x over at flying pace; dial anchor P_D.
- 20261014-1719-second-20261014-1631-taleb-6138-4487 (awaiting grade): the checker's named gold
- 20261014-1631-taleb-6138 (silver): the wave's ruin basin measured — 315/1,213 ms single frames at
- 20261014-1631-library-7f99 (gold): the deletion program's method — 26 kills, the 10% add-back
- 20261014-1511-components-a2c1 (silver): break 3's scan half decomposed — the cap's monotone walk
- 20261014-1221-components-0e37 (silver): break 2's lever — the compiled orbit is write-only memory,
- 20261014-0450-scout-b29a (silver): the smallest promotion is no promotion.
- 20261014-0059-fermi-effb (silver): the 10⁹ ledger composed; the cadence law code-verified.
- 20261014-0000-fermi-3071 (silver): rule 2 dead by decomposition; the tail manufactured.
- 20261014-0000-fermi-3071 (silver): the conflict adjudicated by decomposition — native counts identical across seeds and exactly 2× with the window, roster-predicted Gini 0.759 vs measured 0.718–0.745; rule 2 dead, ea91's description stands, certificate = birth constant.
- 20261014-0059-fermi-effb (silver): the 10⁹ ledger composed — cadence law rate = 2⁷/P code-verified (roster endpoints 0.96/0.76, Orbiters ⊂ [128,256]); encounters 1,925× over skin-on, 7,051× the kicks; two rails (hot = kick gap, cold = encounters + memory); held-out: wired wall ~5.2×10⁵.
- 20261014-1221-components-0e37 (silver): break #2's lever measured — compiled orbits are write-only in flight (retired: 0 reads; flight reads O(1) in N), exactly the key (1,001/1,001 regen), floor 673 vs standing 1,806 B/body; the view's ramp is the one reader (≥1 retired read/row post-wave) — the two-word completion deletes the retired generation free.
- 20261014-1511-components-a2c1 (silver): the scan seam censused — unpoisoned keep 15+2 at every N, the write-once `speed_cap` poisons the window ±9×r (walked 203, 12×), the density rule walks all dolls at N=10³ (1,017, 60×); capture dearer at 10³ (178 µs) than at 10⁵ (129 µs); fixes named in cost order.
- 20261014-1631-library-7f99 (gold): the library mined verbatim (4,580 highlights cached); deletion audit 26 kills / 2 landed add-backs (8%; law level at quota, frame path 0%); automation debt 6 anchored sites; promotion = refusal filter; lookup budget 427–877 recompiles/frame vs demand ≤ 1.4/s.
- 20261014-1631-taleb-6138 (silver): the wave's ruin basin measured — 315 ms/1,213 ms single frames at 10⁵/2×10⁵ burn (seed-stable), the batch = wave density × the player's item horizon at universe.rs:769, coast 12.0 ms through the same wave; fix named (hold the scan), rung must fly past the wave.
- 20261014-1719-second-20261014-1631-taleb-6138-4487 (awaiting grade): the wave's freeze deleted — pull held at 64, a budgeted drain, Waiting scans; 315→37.7 ms at 10⁵, 1,213→90.3 at 2×10⁵, 1,280→123.8 at 3×10⁵; bit-exact at every canonical cut past the drain; the mid-drain cut and the belt digest's wall-schedule instability named.
- 20261014-2012-components-38bf (awaiting grade): the input seam bounded — 0.17–0.23 ms a decision mid-wave under the cap, monsters 1,487→12.5 ms, digest bit-identical, +1 to +2 encounters per 657 no-op decisions (checker: 0.15–0.16 ms even uncapped; silver).
- 20261014-2012-second-20261014-1631-library-7f99-5903: sensors deleted digest-identical (10^3 walk 15x); horizon not belt-scale; chatter 193 -> 0 under refusal at 3.9x events.
- 20261014-2012-system-a669 (silver): key quantum vs per-kick dL — breaks 1/2/4 one dial; flip-gated rebind.
- 20261014-2130-quant-d7e3 (this run, awaiting grade): in-band wave exposure measured — OOM at
- 20261014-2130-second-20261014-2012-system-a669-eb2d: flip-gated rebind wired, default-neutral; the dial's run caps at 4 — 10^2x refuted, mint counted 1.00/kick.
- 20261014-2130-taleb-625b (silver): the player in the belt band: in-band burn = memory ruin (11.2 GB, killed); scan 214-1,087x; coast monster 2 s.
- 20261014-2248-fermi-b30b (awaiting grade): the steady state through waves measured — memory plateaus 4.85-5.06 kB/body (slope <= 5 B/wave; churn killed 3 orders), rate 3.33-3.50e-5 confirmed end-to-end, train ~27-28 k game-s; memory binds the flyable N at every point.
- 20261014-2248-inversion-4af4 (this run, awaiting grade): the wave train flown — memory a step not a staircase, the train shears, and the digest wobble is the presented-time cut.
- 20261014-2248-second-20261014-2130-taleb-625b-c481 (second author, awaiting grade): the site is counted — candidates vectors 29.4 MB/mint, drain frozen after one answer; transit linear, ruin band [1.7,3.0] AU.
- 20261015-0128-second-20261014-2248-inversion-4af4-7dc6 (this run, awaiting grade): the checker's named in-box experiments done — 25 wave periods flat (700 k game-s, digest-stable), dissolution measured (floor rises to the belt-rate equilibrium), 4.2x10^5 at the box ceiling, 4af4's record made to regenerate.
- 20261015-0250-scout-760f (awaiting grade): promotion = one 4.6 µs compile, bit-identical 120,083/120,083; knots 672 B/body (13.7% of the plateau) — eviction 1.16x, the wall is the record stack; 10^9 lives in programs.
- 20261015-0358-second-20261015-0250-scout-760f-b9ae (this run, awaiting grade): the lazy variant flown — digest bit-identical control-vs-lazy on 4 arms (273,200 demotions, 2.38M promotions at 10^5); standing knots -> 0 MB, b/body 1,603 -> 1,002; the 0.16-0.9-core bill needs retention (8.7-23.2 promotions per demotion as flown).
- 20261015-0358-taleb-d7bc (awaiting grade): the ruin fenced — byte cap on held scans, RSS flat 290-311 MB vs ~315 MB/s climb and death; digest identical at 10⁴; the hidden answer bill measured (4-28× play).
- 20261015-0724-components-e0f9 (this run): the seam rebuilt, committed and re-flown — five arms digest-identical, 10⁵ = the scout's anchor with 273,200 demotions, standing 1,603→930 B/body, rss −28%; the machinery free, the no-retention re-mints the whole bill.
- 20261015-0358-second-20261015-0250-scout-760f-b9ae (awaiting grade): the lazy variant flown — digest bit-identical control-vs-lazy on 4 arms (273,200 demotions, 2.38M promotions at 10^5); standing knots -> 0 MB, b/body 1,603 -> 1,002; the 0.16-0.9-core bill needs retention (8.7-23.2 promotions per demotion as flown).
- 20261015-0128-second-20261014-2248-inversion-4af4-7dc6 (awaiting grade): 25 wave periods flat (700 k game-s, digest-stable), dissolution measured (floor rises to the belt-rate equilibrium), 4.2x10^5 at the box ceiling, 4af4's record made to regenerate.
- 20261014-2248-inversion-4af4 (awaiting grade): the wave train flown — memory a step not a staircase, the train shears, and the digest wobble is the presented-time cut.
- 20261014-2130-quant-d7e3 (awaiting grade): in-band wave exposure measured — OOM at the cap's arithmetic.
- 20261014-2012-components-38bf (awaiting grade): the input seam bounded — 0.17-0.23 ms a decision mid-wave under the cap, monsters 1,487→12.5 ms, digest bit-identical.
- 20261014-1719-second-20261014-1631-taleb-6138-4487 (awaiting grade): the wave's freeze deleted — pull held at 64, a budgeted drain, Waiting scans; 315→37.7 ms at 10^5, 1,213→90.3 at 2×10^5, bit-exact at every canonical cut past the drain.
- 20261014-1719-fermi-cf45 (awaiting grade): the belt's clock is the doll's (P_D 77.24 d, interval 2.814e4 s flat in a, 24x the own-period law); shipped step_log2 148x over at flying pace; dial anchor P_D.
- 20261014-1719-dynamics-bf21 (awaiting grade): the wave is a standing train; the look-ahead pull capped holds 2×10^5 burn at 11.97 ms max (114×) with the digest bit-identical.
- 20261014-1631-taleb-6138 (silver): the wave's ruin basin measured — 315 ms/1,213 ms single frames at 10^5/2×10^5 burn; fix named (hold the scan).
- 20261014-1631-library-7f99 (awaiting grade): the library mined verbatim; deletion audit 26 kills / 2 landed add-backs; promotion = refusal filter.
- 20261014-1511-components-a2c1 (silver): the scan seam censused — unpoisoned keep 15+2 at every N; fixes named in cost order.
- 20261014-1221-components-0e37 (silver): compiled orbits are write-only in flight; the view's ramp is the one reader; floor 673 vs standing 1,806 B/body.
- 20261014-0450-scout-b29a (silver): the smallest promotion composed and measured — ~34–38 µs/12–40 B ephemeral vs 486 µs/8,257 B sticky; key-space kick 0.11 µs at the birth floor.
- 20261014-0059-fermi-effb (silver): the 10⁹ ledger composed; the cadence law rate = 2⁷/P code-verified.
- 20261015-1338-quant-1d52 (this run, awaiting grade): the retention rule built and priced — promotions = demotions exactly (85-90% hits, wall +6.5-12.5% over shipped, digests identical, the record's anchors reproduced); global retention erases the memory win (retained set = every kicked body), the redundancy is N-independent (the locals) — adopt bounded, not global.
- 20261015-1450-second-20261015-1338-quant-1d52-0757 (second author, awaiting grade): the bounded cache built and flown — digests identical on 23 flights, retained <= cap by construction, 962 B/body kept (rss 393-414 vs global 548-554 at 10^5), promotions at the kick floor at sufficient cap (exactly 1.00x and 0 evicts on burn at 65,536), ~0.15 cores re-mint at 10^9; the cap curve is the law's read pattern (coast ~4k, burn ~40k).
- 20261015-1450-taleb-b0ed (this run, awaiting grade): the bounded cache built and priced — digest-identical, ratio flat in N at matched cuts (≤1.026 at 4,096 to 2×10⁵), the deep-cut +74-78% bill is history depth (2×N read-once fills), not N; adopt S=16,384.
- 20261014-1719-fermi-cf45 (awaiting grade): the belt's clock is the doll's (P_D 77.24 d, interval 2.814e4 s flat in a, 24x the own-period law); effb's rate law corrected 24x at the plane's belt; shipped step_log2 148x over at flying pace; dial anchor P_D.
- 20261014-1511-components-a2c1 (silver): the scan seam censused — unpoisoned keep 15+2 at every N, the write-once `speed_cap` poisons the window ±9×r (walked 203, 12×), the density rule walks all dolls at N=10³ (1,017, 60×); capture dearer at 10³ (178 µs) than 10⁵ (129 µs); fixes named in cost order.
- 20261014-1631-taleb-6138 (silver): the wave's ruin basin measured — 315/1,213 ms single frames at 10⁵/2×10⁵ burn; fix named (hold the scan).
- 20261015-0358-second-20261015-0250-scout-760f-b9ae (this run, awaiting grade): the lazy variant flown — digest bit-identical control-vs-lazy on 4 arms (273,200 demotions, 2.38M promotions at 10⁵); standing knots -> 0 MB, b/body 1,603 -> 1,002; the 0.16-0.9-core bill needs retention (8.7-23.2 promotions per demotion as flown).
- 20261015-0358-second-20261015-0250-scout-760f-b9ae (awaiting grade): the lazy variant flown — digest bit-identical control-vs-lazy on 4 arms (273,200 demotions, 2.38M promotions at 10⁵); standing knots -> 0 MB, b/body 1,603 -> 1,002; the 0.16-0.9-core bill needs retention (8.7-23.2 promotions per demotion as flown).
- 20261014-2012-components-38bf (awaiting grade): the input seam bounded — 0.17–0.23 ms a decision mid-wave under the cap, monsters 1,487→12.5 ms, digest bit-identical.
- 20261014-1719-second-20261014-1631-taleb-6138-4487 (awaiting grade): the wave's freeze deleted — pull held at 64, a budgeted drain, Waiting scans; 315→37.7 ms at 10⁵, 1,213→90.3 at 2×10⁵, bit-exact at every canonical cut past the drain.
- 20261014-1719-dynamics-bf21 (awaiting grade): the wave is a standing train; the look-ahead pull capped holds 2×10⁵ burn at 11.97 ms max (114×) with the digest bit-identical.
- 20261014-1631-taleb-6138 (silver): the wave's ruin basin measured — 315/1,213 ms single frames at 10⁵/2×10⁵ burn; fix named (hold the scan).
- 20261015-1450-second-20261015-1338-quant-1d52-0757 (second author, awaiting grade): the bounded cache built and flown — digests identical on 23 flights, retained <= cap by construction, 962 B/body kept (rss 393-414 vs global 548-554 at 10⁵), promotions at the kick floor at sufficient cap (exactly 1.00x and 0 evicts on burn at 65,536), ~0.15 cores re-mint at 10⁹; the cap curve is the law's read pattern (coast ~4k, burn ~40k).
- 20261015-1615-quant-0619 (this run, awaiting grade): the burn knee is the demotion count, not a working set — WS = demotions = N + 30,187 integer-exact at four N, seed and cut; price law exact 7/7 (promos − dem = hits_sat − hits_cap); fixed cap degrades with N (1.24→7.23→8.50×); ring pins +27,911 zombies over global; no bounded cap ships burn at 10⁹ (knee ≈ 1.4 TB) — price the re-mints or delete the reads.
- 20261015-1615-second-20261015-1450-taleb-b0ed-f55d (second author, awaiting grade): the burn knee measured — 1.31xN exactly at 10^5 and 2x10^5, mints = apply not the resolver, hits = the scan (26->71% with N), kick-anchored admission refuted; identity 26/26; regen fixed.
- 20261015-1615-spacex-1343 (silver): the passage tail priced — 96 B/panel, 10.74 panels/octave past the 2^10 join, universal in w; re-mint bit-identical, so never-demote is for plunges alone (checker: the cap is on outer, not w — star-grazing mints w=20, 25.7 kB alive; unflown on the seam).
- 20261015-1747-inversion-b172 (this run, awaiting grade): the formation falsifier measured — concentration collapses the burn knee from ~1.31×N to ≤ N/24 (1.014×dem at cap 4,096 vs the belt's 7.23×), same kicks/demotions/digests; the no-cap law is the belt's geometry, not burn's.
- 20261015-1747-second-20261015-1615-spacex-1343-3dc8 (this run, awaiting grade): the checker's named gold experiment flown — demote-passages digest-identical on 18 flights (standard ladder + mixed-peri comet stream), record 113 B vs 18.8–25.3 kB, bill 5.9×dem at 421–583 µs p50, rss 445–979→27–51 MB (Live-arc pinning deleted).
- 20261015-1926-spacex-8b89 (this run): the class list dies — ES_LAZY_ALL demotes every keyed entry (births, no-kick settles), 7 scenes digest-identical, standing arcs → the centres (680 B/body at the belt's birth state), rss 979→20 MB on mixed; no state birth mints a Plunge.
- 20261014-1719-dynamics-bf21 (silver): the wave is a standing train; the look-ahead pull capped holds 2×10⁵ burn at 11.97 ms max (114×) with the digest bit-identical; holding the whole scan is digest-refuted.
- 20261014-1719-fermi-cf45 (silver): the belt's clock is the doll's (P_D 77.24 d, interval 2.814e4 s flat in a, 24x the own-period law); effb's rate law corrected 24x at the plane's belt; shipped step_log2 148x over at flying pace; dial anchor P_D.
- 20261014-1719-second-20261014-1631-taleb-6138-4487 (silver): the wave's freeze deleted — pull held at 64, a budgeted drain, Waiting scans; 315→37.7 ms at 10⁵, 1,213→90.3 at 2×10⁵, 1,280→123.8 at 3×10⁵; bit-exact at every canonical cut past the drain.
- 20261014-2012-components-38bf (silver): the input seam bounded — 0.17–0.23 ms a decision mid-wave under the cap, monsters 1,487→12.5 ms, digest bit-identical, +1 to +2 encounters per 657 no-op decisions.
- 20261014-2248-second-20261014-2130-taleb-625b-c481 (awaiting grade): the site is counted — candidates vectors 29.4 MB/mint, drain frozen after one answer; transit linear, ruin band [1.7,3.0] AU.
- 20261015-0250-scout-760f (silver): promotion = one 4.6 µs compile, bit-identical 120,083/120,083; knots 672 B/body (13.7% of the plateau) — eviction 1.16x, the wall is the record stack; 10^9 lives in programs.
- 20261015-0724-components-e0f9 (silver): the seam rebuilt, committed and re-flown — five arms digest-identical, 10⁵ = the scout's anchor with 273,200 demotions, standing 1,603→930 B/body, rss −28%; the machinery free, the no-retention re-mints the whole bill.
- 20261015-1338-quant-1d52 (silver): the retention rule built and priced — promotions = demotions exactly (85-90% hits, wall +6.5-12.5% over shipped, digests identical, the record's anchors reproduced); global retention erases the memory win, the redundancy is N-independent — adopt bounded, not global.
- 20261015-1450-second-20261015-1338-quant-1d52-0757 (gold): the bounded cache built and flown — digests identical on 23 flights, retained <= cap by construction, 962 B/body kept, promotions at the kick floor at sufficient cap, ~0.15 cores re-mint at 10⁹; the cap curve is the law's read pattern.
- 20261015-1450-taleb-b0ed (silver): the bounded cache built and priced — digest-identical, ratio flat in N at matched cuts, the deep-cut bill is history depth, not N.
- 20261015-1615-quant-0619 (gold): the burn knee is the demotion count, not a working set — WS = demotions integer-exact at four N; price law exact; fixed cap degrades with N; ring pins zombies over global; no bounded cap ships burn at 10⁹ — price the re-mints or delete the reads.
- 20261015-1615-second-20261015-1450-taleb-b0ed-f55d (silver): the burn knee measured — 1.31xN exactly at 10^5 and 2x10^5, mints = apply not the resolver, hits = the scan, kick-anchored admission refuted; identity 26/26.
- 20261015-1747-inversion-b172 (awaiting grade): the formation falsifier measured — concentration collapses the burn knee from ~1.31×N to ≤ N/24 at cuts under one wave period, same kicks/demotions/digests; the no-cap law is the belt's geometry, not burn's.
- 20261015-1747-second-20261015-1615-spacex-1343-3dc8 (awaiting grade): the checker's named gold experiment flown — demote-passages digest-identical on 18 flights, record 113 B vs 18.8–25.3 kB, bill 5.9×dem, rss 445–979→27–51 MB.
- 20261015-1926-taleb-d6ba (this run, awaiting grade): the seam residue censused on the belt — a wave pulse (711 B/body just after a settle, 8.6 at depth), not a standing class; plunges mint zero; dead hold ~1 arc/death; the record stack is the depth term.
- 20261015-2041-inversion-398f (this run, awaiting grade): the history stack's growth law measured per class — the belt flat (1.04 seg/body at every cut, arm-independent), the infalling comet class linear (+0.99 exponent, 46.5->480 by 32k, rss 2.8 GB on 174 bodies); keep-behind = 2*light_distance makes the term causal; single-cut adoption flights are blind to it.
- 20261015-1926-taleb-d6ba (silver): the seam residue censused on the belt — a wave pulse (711 B/body just after a settle, 8.6 at depth), not a standing class; plunges mint zero; dead hold ~1 arc/death; the record stack is the depth term.
- 20261015-2041-second-20261015-1926-taleb-d6ba-57ec (this run, awaiting grade): the comet class is standing — the same 100 passages at 32k and 48k, one arc per live comet (the belt drains at 0.2 kicks/ks; comets stand at 28); ctl is 2.1 GB linear ruin at 32k; the belt floor is 87 kB total, N-constant; record stack 1.0–1.3 TB at 10⁹.
- 20261016-0023-quant-404b (this run): the birth rail split — plan pass 32.5–33.5 µs/body (76–78%
- 20261016-0023-scout-1652 (this run, awaiting grade): the last-segment floor priced against the prune's own keep window — 98.3–98.4% of the belt's standing segments are past it at steady cuts (91.2% in-window just past a wave; keep p50 2,764 s = 9.8% of the interval), but the view's gather serves eras to 27,645 s (≈ the full interval, past every keep): retention's horizon today is the view's partial-step walk, not the light cone; ~10× standing cut (353 GB → ~35 GB inline at 10⁹) sits behind the view's documented outcome-free fallback.
- 20261013-2252-dynamics-ea91 (awaiting grade): surprise distribution heavy (Gini 0.72–0.74), live ranks frozen, churn is death (54–64 % of promotions), steady stream avalanches (Fano 8–28).
- 20261014-0450-scout-b29a (silver): the smallest promotion composed and measured.
- 20261014-1221-components-0e37 (silver): compiled orbits are write-only memory; the view's ramp is the one reader.
- 20261014-1511-components-a2c1 (silver): the scan seam censused; fixes named in cost order.
- 20261014-1631-library-7f99 (gold): the library mined verbatim; deletion audit 26 kills / 2 landed add-backs.
- 20261014-1631-taleb-6138 (silver): the wave's ruin basin measured; fix named (hold the scan).
- 20261014-1719-dynamics-bf21 (silver): the wave is a standing train; the look-ahead pull capped holds 2×10⁵ burn with the digest bit-identical.
- 20261014-2248-fermi-b30b (awaiting grade): the steady state through waves measured; memory binds the flyable N at every point.
- 20261014-2248-second-20261014-2130-taleb-625b-c481 (awaiting grade): the site is counted — candidates vectors 29.4 MB/mint, drain frozen after one answer.
- 20261015-0128-second-20261014-2248-inversion-4af4-7dc6 (awaiting grade): 25 wave periods flat (700 k game-s, digest-stable), dissolution measured, 4af4's record made to regenerate.
- 20261015-0250-scout-760f (silver): promotion = one 4.6 µs compile, bit-identical 120,083/120,083; 10^9 lives in programs.
- 20261015-0358-taleb-d7bc (awaiting grade): the ruin fenced — byte cap on held scans; the hidden answer bill measured.
- 20261015-0358-second-20261015-0250-scout-760f-b9ae (awaiting grade): the lazy variant flown — digest bit-identical on 4 arms; standing knots -> 0 MB.
- 20261015-0724-components-e0f9 (silver): the seam rebuilt, committed and re-flown — five arms digest-identical, rss −28%.
- 20261015-1338-quant-1d52 (silver): the retention rule built and priced — promotions = demotions exactly; adopt bounded, not global.
- 20261015-1450-second-20261015-1338-quant-1d52-0757 (gold): the bounded cache built and flown — the cap curve is the law's read pattern.
- 20261015-1450-taleb-b0ed (silver): the bounded cache built and priced — the deep-cut bill is history depth, not N.
- 20261015-1615-quant-0619 (gold): the burn knee is the demotion count, not a working set — no bounded cap ships burn at 10⁹.
- 20261015-1615-second-20261015-1450-taleb-b0ed-f55d (silver): the burn knee measured — 1.31xN exactly; mints = apply not the resolver; kick-anchored admission refuted.
- 20261015-1615-spacex-1343 (silver): the passage tail priced — 96 B/panel, 10.74 panels/octave; re-mint bit-identical.
- 20261015-1747-inversion-b172 (silver): the formation falsifier measured — concentration collapses the burn knee from ~1.31×N to ≤ N/24 at cuts under one wave period; the no-cap law is the belt's geometry, not burn's.
- 20261015-1747-second-20261015-1615-spacex-1343-3dc8 (awaiting grade): demote-passages digest-identical on 18 flights; record 113 B vs 18.8–25.3 kB.
- 20261015-1926-spacex-8b89 (this run): the class list dies — ES_LAZY_ALL demotes every keyed entry; standing arcs → the centres.
- 20261015-1926-taleb-d6ba (silver): the seam residue censused — a wave pulse, not a standing class; plunges mint zero.
- 20261015-2041-inversion-398f (awaiting grade): the history stack's growth law measured per class — the belt flat, the infalling comet class linear.
- 20261015-2041-second-20261015-1926-taleb-d6ba-57ec (awaiting grade): the comet class is standing — the same 100 passages at 32k and 48k; ctl is 2.1 GB linear ruin at 32k.
- 20261016-0023-second-20261015-1747-inversion-b172-f56e (this run): b172's gold step closed — the depth arms landed (29.26 at 48k, 26.07 at 32k, horizon one wave recurrence), the bill scene-invariant at depth (270,979), and the matched-fills control kills the angular reading (fills 616,250 invariant in w and K; 1.013 at full diffusion).
- 20261016-0117-library-cfe5 (this run): the plan pass attributed — secondaries 30% of birth
- 20261016-0117-second-20261016-0023-scout-1652-d86c (silver): the floor deletion flown — digests identical coast and burn (checker: also at 150k and 5x10^4), 16x coast / 3.3x burn standing cut at 60k (decaying to 1.6x at 150k, the in-window residue), view-only cost (refused walks, disc shifts <= 40 m at the flown cuts but past-disc at >= 90k; fleet lights <= 15.5 km; one observer-fallback mode), engine reads untouched.
- 20261016-0117-taleb-51b7 (this run, awaiting grade): the flight into the belt flown on merged main — the quiet belt and the wave mint zero scans (the instrument is cadence-off at belt radii); the burn mints one scan per binding change, 11.3 MB marginal each at 10⁵, p50 29 ms standing, fenced at 1.92 GB in 2.5 s; SCAN_BACKLOG's count cap can never engage (240 GB at 10⁹).
- 20261016-0213-fermi-1a1c (this run, awaiting grade): the assembled 10⁹ budget on merged main —
- 20261016-0213-second-20261016-0117-taleb-51b7-e28f (this run, awaiting grade): the cure's first rung flown — candidates shared behind an Arc, mint per candidate-set change (1 snapshot per burn, 971 consecutive changes), the 1.92-GB fence deleted (720 frames at 307 MB), answers bit-identical (5 robust A/B digest equals + 10/10 record ladder_digest rows, 14/14 regen), the 10⁵ answer bill measured 0.39 s/scan.
- 20261016-0213-system-d31c (this run, awaiting grade): one shared planets-at-t readout for both birth read paths — pass 33→22.7 µs/body, digest-identical everywhere; the element read ≤0.4 µs, the ≲13 prediction dead: the pass is arithmetic.
- 20261016-0346-quant-3ec8 (this run, awaiting grade): plan_clock's three own-state reads served by one readout - birth pass -18-22%, rail -14.5%, digests identical; thrusting-kick readout named next.
- 20261016-0346-scout-7da3 (this run, silver [checker]): staggered wave flown four periods budget-free, window-level cure permanent (held at 10⁴ by the checker); the run's letter break 1.7–2.2×10⁶ REFUTED at rtf 100 (crest 342/366, N-flat, a 660-s beat) — corrected break ≈ 6×10⁵, composed 10⁹ ≈ 0.7× at the key arm; wave period 14,167 game-s, decay ×0.72.
- 20261016-0346-second-20261016-0213-system-d31c-79ca (second author): the pass's shared recomputes deleted — one state read (3 calls → 1/body) + per-doll constants (5.3 → 0.03 µs); pass 34 → 11 µs/body (≈3×), digest-identical; the readout lever alone 1.4×, under checker 2's bar.
- 20261016-0346-spacex-917c (this run, awaiting grade): staggered wave flown budget-free at
- 20261016-0504-components-4534 (this run): the locals' storm is the block-step grid, not the begin — BEGIN refuted bit-exactly, the grid-translate flattens 335 -> 141 (2.0-2.4x, both seeds, N-flat), event totals move +6/+73% (undiagnosed), gates unflown.
- 20261016-0504-dynamics-4c22 (silver [checker]): the locals' storm is a standing comb phase-locked to aligned's absolute grid; the belt's one-step cure is absorbed; a permanent per-body phase collapses it 334→53 at +11-20% events (a law change); the run's attribution instrument was 2:1 misaligned (checker-corrected: the storm is ~93% doll-2 boundaries, no pull lane).
- 20261016-0504-second-20261016-0346-spacex-917c-c840 (second author): the checker's gold step flown — B13 armed 0/64 vs off 60/64, all 13 armed digests change; the stagger configuration killed, the cure goes to the birth program.
- 20261016-0504-system-e070 (this run, awaiting grade): the locals isolated on main — 3%
- 20261016-0504-components-4534 (this run): the locals' storm is the block-step grid, not the begin — BEGIN refuted bit-exactly, the grid-translate flattens 335 -> 141 (2.0-2.4x, both seeds, N-flat), event totals move +6/+73% (undiagnosed), gates unflown. [restored by checker 20261016-1120: dropped from this page's conflict resolution; Runs is append-only]
- 20261016-0504-second-20261016-0346-spacex-917c-c840 (second author): the checker's gold step flown — B13 armed 0/64 vs off 60/64, all 13 armed digests change; the stagger configuration killed, the cure goes to the birth program. [restored by checker 20261016-1120: dropped from this page's conflict resolution]
- 20261016-0504-system-e070 (this run, awaiting grade): the main-tree storm is the belt's wave, and the locals are secondary on main at seed 1 (isolation control moves the worst bucket 922→894); at seed 3 the locals bind it. [restored by checker 20261016-1120: dropped from this page's conflict resolution]
- 20261016-1120-second-20261016-0504-dynamics-4c22-dd75 (second author): the corrected attribution instrument on the run's own record — every headline and digest regenerates exactly; the storm is 97% one doll's kicks+boundaries (biggest beat 100% attributed), d0 zero everywhere, no second lane.
- 20261016-1207-library-846b (awaiting grade): the library mined verbatim (4,580 highlights, 7 quotes verified): the comb cures ordered — question the anchor, delete the events (B14-gated), spread last; chained intervals over ES_LOCAL_PHASE; serve the view from the program; size caps by demotions; automation last.
- 20261016-1319-fermi-1051 (silver): one lever, not two — the comb and the stream are
- 20261016-1319-system-4fa8 (silver [checker]): the comb is the anchor's artifact — ES_CHAIN+birth
- 20261016-1319-system-4fa8 (awaiting grade): the comb is the anchor's artifact — ES_CHAIN+birth spread retires it (334→52, p99 136→24, zero steady-state rate, −11% CPU); chaining alone inert; ES_LOCAL_PHASE beaten.
- 20261016-1637-dynamics-87fd (this run, awaiting grade): the cure judged on doll-born locals —
- 20261016-1637-second-20261016-1319-fermi-1051-1a46 (second author): the hybrid delete flown — storm 334→131 (134-candidate wins, 83.5 refuted), legality measured 85.8% in-situ (both prior numbers corrected), ledger −70%, freeze behind the quantum fence.
- 20261014-2012-components-38bf (this run, awaiting grade): the input seam bounded — 0.17–0.23 ms a decision mid-wave under the cap, monsters 1,487→12.5 ms, digest bit-identical, +1 to +2 encounters per 657 no-op decisions (checker: 0.15–0.16 ms even uncapped; silver).
- 20261014-2130-quant-d7e3 (this run, awaiting grade): in-band wave exposure measured — OOM at the cap's arithmetic.
- 20261016-0023-second-20261015-1747-inversion-b172-f56e (this run): b172's gold step closed — the depth arms landed (29.26 at 48k, 26.07 at 32k, horizon one wave recurrence), the bill scene-invariant at depth (270,979), and the matched-fills control kills the angular reading (fills 616,250 invariant in w and K; 1.013 at full diffusion). [restored by checker 20261017: dropped from this run's conflict resolution; Runs is append-only]
- 20261016-1459-second-20261016-1319-system-4fa8-21a7 (awaiting grade): the gates blind to the comb law (every gate body root-doll); ES_LOCAL_PHASE = chain+stagger on every instrument; parsimony decides.
- 20261017-2330-spacex-f134 (spacex, awaiting grade): delete + chain composed — strictly dominant (max 41 vs 52/131, p99 12, ledger −72% with no slice bill, envelope decays 41→3, N-flat, horizon-stable, 13/13 schedule-determinism); patch-off bit-identical to the frozen record; the comb question closes.
- 20261018-0543-spacex-7fcf (spacex, awaiting grade): the composed law's doll-born drift
- 20261018-1126-inversion-7581 (inversion, awaiting grade): the composed law on the crowd
- 20261018-1433-inversion-96f6 (inversion, awaiting grade): the crowd's 5×10⁴ break decomposed — 33/33 over frames carry 2 events; the bail's full O(K) capture walk (190 ns/body, λ K-independent) owns the frame at 4–6×10⁴; the observer fix must land store-grounded and delete the candidates Vec (pin 8 GB at ~3.5×10⁵ first).
- 20261018-1530-second-20261018-1433-inversion-96f6-acf2 (second author, awaiting grade): the pin measured directly — 0.0526 mints/game-s K-flat, alive == mints (the freeze drops nothing), 8 GB at 687 game-s at the fix's 10⁶ target; compare-form native 0.5 ns/member (40× under the REPLICA); trigger = the player's clock; the fix must answer-or-expire.
- 20261018-1617-taleb-2403 (taleb, awaiting grade): the mint rate is the wildcard's pacing — burn 13.5× coast (nladder 10⁴, held 1→258; 0 at a 24 ms budget with identical arrivals), burst phase ~116×, seed-identical (canonical log); the fence is sized for the burn, not 0.05.
- 20261018-1717-fermi-dcf1 (fermi, awaiting grade): the burn byte wall is dead at 3e5 (HWM K-flat 0.026 MB/game-s vs the law's 47; held <=187; 0 over 12 ms; frame and player stream N-flat); the view gather (5.0 us/seen-body, seen=N+61) is the ladder's first N-growing term.
- 20261018-1717-inversion-d839 (inversion, awaiting grade): memory through cadence waves is flat —
- 20261018-1717-second-20261018-1617-taleb-2403-99da (second author, awaiting grade): the 10⁶ gap sliced — arrivals bit-identical 10⁵→6.5×10⁵ (145/2,069, census equal), multiplier 16.8× at both, 10⁶ wall ≈ 43 game-s; 2403's P1/P6 corrected to not-held.
- 20261019-0141-inversion-4a71 (inversion, awaiting grade): prune's global `oldest` measured — closed at one star (gap = the widest pending light gap, 2,302.5 s, flat in play time, 0–0.1 s at the 5 ms corner and burn), and the ratchet it guards is real: a pin deeper than the gap staircases memory (+1 generation/body per 27.6k gs, ~2 KB/retained binding, +124/+229 MB) and eats the frame (over 6→383/683); at 4 ly one pending item is ~9.2 MB/body.
- 20261019-0435-inversion-4447 (inversion, awaiting grade): the burn-mode memory ratchet unbounded past every prior horizon — 10⁴ to 561k game-s (RSS 41→1,601 MB, still 3.4 MB/1k gs), 3×10⁴ guard-stopped at 333k; d839's "flat" was truncation, dcf1's "wall gone" ended at the SOI switch; slope ~K-proportional mid-flight; one wall-hour of L8 = 1–2.2 GB.
- 20261019-0435-second-20261019-0325-library-9147-1b3f (second author, awaiting grade): the per-reader `oldest` flown — far pin live, near bodies at control (1.016 vs 5.14/body, 157 vs 385 MB, 0 vs 612 over, counts at control within same-arm spread), digest suite byte-identical, burn/SOI clean; per-doll calendars stale on handoffs (found, fixed).
- 20261019-1452-library-e181 (library, awaiting grade): the expiry fence flown — TTL 16 game-s deletes the burn ratchet (guard 1,600 MB at 29.6k gs → flat 702 MB through 41.9k gs), ≤ 0.3% encounters lost; the fence must count bytes, not scans.
- 20261019-1452-taleb-527a (taleb, awaiting grade): the conflict resolved — reader-oldest ≠ the burn ratchet's cure (identical to the digit, gap shut); channel 1 = the scan deque (fence 10KB-stale, licenses 5.6-19.4 GB, never engages first); channel 2 = late history retention behind the receding observer (new).
- 20261019-1551-inversion-f80a (gold, two checkers): the fence inverted — channel 1 deleted, the ratchet survives on channel 2 to 1,457 MB at 419k gs; onset is the first wave
