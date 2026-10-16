topic: nladder
status: open
closed-by:
valid-while:
<<<<<<< main
<<<<<<< main
updated: 20261016-0117-library-cfe5
=======
updated: 20261016-0117-second-20261016-0023-scout-1652-d86c
>>>>>>> 20261016-0117-second-20261016-0023-scout-1652-d86c
=======
updated: 20261016-0117-taleb-51b7
>>>>>>> 20261016-0117-taleb-51b7

# The N ladder: 28 live bodies toward 10⁹

## Current best

<<<<<<< main
<<<<<<< main
**The plan pass's interior is attributed, and it is not an irreducible exact search: 30% of the
birth pass is the planets' exact states re-derived once per body (deleted digest-identically by a
birth-only hoist, 32.4–33.5 → 22.8–23.2 µs/body), the terminal bisection is 0.1% of it, and the
largest term is the per-body clock derivation (`constants`+`project`, 15.4–16.0 µs/body) — with
the SAME planet reads happening a second time through `ext::constants`' `source()` (20261016-0117-library-cfe5,
library lens, shipped code + `ES_BIRTH_SPLIT` counters and an `ES_SEC_HOIST` memo armed only inside
`Universe::start`).** Belt at 10⁴/10⁵ × seeds 1/7 (7 never flown by the author before predicting):
pass 32.40–33.49 µs/body (reproduces 404b's 32.5–33.5 flat in N), secondaries compute 9.75–10.23
µs/body = 30.1–30.6%, exactly one `secondaries` call per body (n+28 calls; the memo serves 10⁵
bodies from 7 entries), `plan_terminal` 0.03 µs/body, digests identical on all 8 flights. The
remainder (~17 µs unattributed) includes a second planet-reread path — code-verified (ext.rs:133,
called once per clock body from `plan_clock`) but untimed: its µs share is inference until the
next rung's timer says so. Consequences: (1) the "irreducible exact search" reading of the pass is
dead — the exact searches (terminal, exits) are free at birth; the bill is shared-state
recomputation plus per-body clock math; (2) one shared "planets at t" readout serving both paths
is the named next rung (predicted pass ≲ 13 µs/body,
amortizing the same structure at every wave-front pass); (3) at 10⁹ the hoisted pass alone deletes
~2.8 core-hours of 404b's ~6 (lab-box orders).

**[Prior best retained — see lab/wiki/nladder.md's standing text: 404b's birth-rail split, the
scout's last-segment floor, the depth axis (398f/57ec), the seam/retention family (e0f9, 0757,
b0ed, quant-0619, f55d), 8b89's ES_LAZY_ALL, b172's formation falsifier, 1343/3dc8's passage
pricing). This proposal folds the plan-pass attribution in; the merge resolves against whatever
side of the page's conflict stands.]**

*[Checker (silver): reproduced from a clean tree — every digest bit-identical to the runner's
regen and across both hoist arms on my own 8-flight grid (pass 33.7–33.9, secondaries 10.2–10.4 =
30.2–30.5%, hoist-on 22.9–23.6, `sec_calls` = n+28, 7 memo keys). Beyond the author's domain:
held-out seed 3 holds at 10⁴/10⁵ (30.2/30.3%); 3×10⁵ holds flat (30.4%, digest-identical, RSS
688 MB); at 10³ the share dips to 26.7% — "30%" is honest for 10⁴–3×10⁵, not a constant of the
ladder. Prediction 1 failed as the dossier reports (30%, not >50%), so the pass's largest term
(the clock derivation) is attributed by arithmetic, not a timer. All five library quotes verified
verbatim in work/library.json with correct authors.]*
=======
**The deletion is flown and the floor is not law: digests bit-identical across the toggle,
coast and burn, and standing history falls 16x at coast (1.053 -> 0.066 segs/body, the residue
100% in-window) and 3.3x under burn (1.40 -> 0.43, the law's own oldest-guard need; the floor's
extra is 97-98.4% past every window in every flight) — the bill moves entirely to the view
(20261016-0117-second-20261016-0023-scout-1652-d86c, second author, deterministic frames, N=10^4,
cuts to 60k game-s).** Per-emitter chain walks are refused instead of served (21,206 view misses
vs 6 per cold gather at 20k burn; warm gathers do 1.7% of the baseline's retired reads and the
gather drops 207 -> 49 ms); every emitter stays seen; disc emitters shift 19-40 m, inside their
own discs at the flown cuts (the 20 fleet point lights, outside the disc rule, shift up to 15.5 km
— <= ~11% of their own apparent discs). One schedule-conditional mode remains the integrator's call: when the
player's own partial-step source read hits a pruned era (ext.rs:134 -> view's documented
`t_read = event_time` fallback) the whole sky translates rigidly by the observer's displacement
(measured -6.94e6 m, zero emitters lost). Engine-side retired serves between gathers
(4,364-8,854/interval at N=10^4) are identical across the toggle with zero engine misses: the
engine never reads what the deletion removes. Side finding: a *mid-flight* settled digest is
wall-schedule-sensitive in the shipped engine with or without the deletion (same build, same
script, 32k digest 11f3e40b vs 08da2dd6) — judge digests on deterministic frames or terminal
cuts. Adoption = one predicate in `PlainBodies::prune` + `droppable_until`, plus the view call.

*[Checker (silver): the record reproduces bit-for-bit on a third independent execution, and holds
beyond the flown domain — digests identical at 150k game-s coast AND burn (2.5x the horizon) and
at N=5x10^4 (floor-on 1.011 -> floor-off 0.013 segs/body at 25k), zero engine misses everywhere.
But at depth the registered D2 bound breaks: 6 disc emitters past their own discs at 90k, 228 at
150k (still ~60 m scale, zero vanish — per the run's own registered rule, a blocker at depth, the
refused deep reads the floor was serving); and the burn cut decays 3.3x (60k) -> 1.6x (150k) as
the floor-off residue, 100% in-window, grows 0.43 -> 1.57 under churn: the invariant win is the
~1.0 segs/body dead pin the deletion removes, not the ratio. The wall-mode numbers do not
regenerate (this check's rerun: mean -9.19e6 m, spread ~60 km — rigid to ~0.7%, not "spread
~60 m").]*


=======
**The named next rung is flown on merged main — the flight into the belt — and the ruin is the
player's own changes alone (20261016-0117-taleb-51b7, taleb; `plane_extra_belt_player` + the
`belt_ladder` probe, bits held by `ladder_digest` against the pristine tree).** The player born
mid-belt (2.5 AU circular, root doll): a **quiet coast mints zero scans at every N** (held 0,
enc 0, p50 0.028 ms at 10⁵ — the encounter instrument's cadence is the doll's, one player item per
~2.8×10⁴ game-s [checker: cf45's measured interval; my 35,000-game-s quiet flight (10⁴, rtf 200) mints exactly one scan, held 1 — the dossier's ~59,400 arithmetic is excluded], so at belt radii it is effectively OFF), and **the belt's first-kick wave mints
nothing either** (145 s/140 s flights through the wave at 10⁴/10⁵: held 0, memory 65/322 MB, max
45.3/12.1 ms — the wave's frames hold under the merged fixes; the one 45-ms frame at 10⁴ is
unattributed, box-load suspected). The ruin is the burn: one binding change per thrust kick mints
**one scan per binding change** (≈ +1/frame at 10⁵; +0.6–1.5/frame at 10⁴–3×10⁴, checker-measured), each holding every candidate's binding — **11.3 MB marginal RSS per
held scan at 10⁵ (113 B/body), 1.11 MB at 10⁴** — and the answers (150–190 ms at 10⁵) never fit the
12-ms budget, so the backlog grows monotonically: at 10⁵ the probe self-fenced at 1.92 GB in 2.5 s
of burn (148 scans), p50 **29-30 ms standing** (capture alone ~290 ns/body, superlinear 10⁴→10⁵:
~210→290 ns/body), every second frame over budget; at 10⁴ 8 s of burn ends at 730 MB, held 634.
Budget-free at 10⁴ the same flight pays p50 39 ms, max 253 ms in-frame — the 12-ms budget converts
the frame bill into held-scan memory, one ruin for another. **SCAN_BACKLOG (2048, a count cap) can
never engage in the belt: it pins 2048 × 113 B × N — 2.3 GB at 10⁴, 23 GB at 10⁵, 240 GB at the
10⁹ goal — the machine dies first** (confirms 625b/c481/d7bc's band seam on merged main, after the
wave fixes; d7bc's byte cap remains the fence). Digest discipline: belt-burn digests under a
12-ms budget are wall-coupled through the probe's input tick (`p.u.now` at the burn frame lags
with load); budget-free arms are bit-identical across processes. [Checker correction: the coupling
runs through input ticks and the final horizon, not the reported max — the 10⁴ wave arm is bitten
(43-ms frame, same frame 8,509 across runs) yet identical across 3 processes, while the no-input
10⁵ wave arm shows 3 digests at max ≤ 12 ms; trust budget-free and far-from-budget arms only.]
[Checker 2: the ordering holds only where the pinned bytes exceed RAM — on this 2 GB box at 10⁴+,
but not on the 8 GB M1 until N ≳ 3.5×10⁴ (at 10⁴ the cap would engage in ~34 s as frame-time ruin,
not memory ruin; at 10³ the backlog drains to 0, held peak 82, 60 s flown); the mis-sizing finding
itself is unaffected. Checker 2 also extended the law beyond the flown domain: 3×10⁵ burn fences at
34 scans, 118.6 B/body marginal, p50 95 ms = 317 ns/body.]

**The birth rail is first-plan-dominated, not compile-dominated: at the ladder's true belt keys one
belt body costs 42–44 µs/body to build on the lab box (Linux/x86; the M1's own anchor is 28–31),
of which draw+`add_body` is 9.3–9.7 µs (22–24%, matching c4d3's 9.2 µs measurement of the same
path — a lab Linux i7-4790 number, same box class but a different harness, so this is cross-run
agreement, not box-invariance) and `Universe::start`'s tick-0 `replan`+`apply` pass is 32.5–33.5
µs/body (76–78%), flat in N from 10⁴ to 3×10⁵ (slope exponent ≈ 1.0), seed-stable (held-out seed
3: 42.6 slope, plan 33.0), requeue+alloc+rekey ≤ 0.1 µs/body
(20261016-0023-quant-404b; `ES_BIRTH_SPLIT` print-only instrumentation, digests identical to the
pristine tree at the same commit).** Consequences: (1) the 10⁹ fill is ~8 M1-core-hours, ~6 of
them the plan pass — the exact work a program-store birth (b29a's smallest promotion) never does,
so the compact store's CPU case is 3.3× its compile-path case, not just a memory case; (2) any
lazy-birth wiring that promotes-then-plans inherits the 10⁷-wave ruin at 3.3× the quoted compile
bill; (3) the pass's interior (event search vs apply's walk) is unattributed — the named next
experiment. The plane's own 28 bodies pay 25.8–29.9 µs/body in the same pass (heavier dolls).

*[Checker (silver): every number reproduced — the runner's regen (exit 0, 13/13 digest identity)
plus my own flights on the re-applied patch: seed 1 re-fly 42.0–42.5 µs/body; the registered
held-out seed 7 (never flown by the author) slope 45.1, plan 35.0 (78%); 5×10⁵, beyond the
author's 3×10⁵, plan 34.2, slope 46.0, peak RSS 1.17 GB (no cache cliff); ES_BIRTH_SPLIT off is
timing-identical (42.5); my own ladder_digest run md5-equals the record. Three corrections: (1)
c4d3's 9.2 µs is a lab Linux i7-4790 number (its dossier names the machine), not an M1
measurement — the agreement is same-box-class cross-harness, and the 3.4× plan/add ratio is
single-box until the M1 re-measure, so read consequence (1)'s ~6-of-8 M1-core-hours as
conditional; (2) the pass's interior, measured by the checker at 10⁵: `step::replan` 28.2
µs/body vs `apply` 4.2 (87/13) — the irreducible-vs-bookkeeping question is now `plan_interval`'s
search alone; (3) P3's kick-side comparator is not regenerable from the record (its 0.3–3× band
held regardless).]*

**[Prior best retained — see lab/wiki/nladder.md's standing text: the depth axis (the history
stack's growth law, 398f/57ec), the seam/retention family (e0f9, 0757, b0ed, quant-0619, f55d),
8b89's ES_LAZY_ALL, b172's formation falsifier, 1343/3dc8's passage pricing). This proposal folds
the birth-rail result in; the merge resolves against whatever side of the page's conflict stands.]**
>>>>>>> 20261016-0117-taleb-51b7
**The last-segment floor is priced against the prune's own window, and the window is not the
binder — the view's walk is (20261016-0023-scout-1652, scout, on shipped code).** On the ladder
belt past the first wave, **98.3–98.4% of standing segments are past the certified forget-window**
(keep = 2·light_distance + 2²⁶, p50 2,764 s = 9.8% of the 28,141.5 s interval) at the 20k/32k/48k
cuts, and 91.2% are in-window just past a wave — the floor pins 1.05 segs/body (1,404–1,438
B/body whole) where a light-cone-bounded reader needs ~10% steady duty (and ~0% between
unstaggered waves). But the page's own cold gather serves retired eras to **27,645 s old (≈ the
full interval, past every keep window; deepest read 6,268.6 s into an era)** — attributed to
the ramp's walk (`credit`'s back-through-bindings loop, observe.rs:39/69, plus `partial`'s
one-back read, observe.rs:130; checker's code read: the walk's bound is two whole-step windows
`(t−m) > k.len << (2·level+1)`, the kick interval, not the light distance), which reconstructs
retarded reads from the last kick's tube regardless of light distance. So: retention's honest
horizon as implemented is the view's walk, not the cone; the ~10× standing cut (353 GB → ~35
GB inline at 10⁹, ~11 GB at the seam's 113-B record) sits behind the view's documented
outcome-free fallback ("history pruned … the tube alone is read") or a walk cap at keep. The
census instrument (`history_window` + the retired-serve counters, 60 lines) is the adoption
gate's meter. [P3 of the run's pre-registered predictions failed on exactly this; the run
reports the lever as conditional, not adoptable.]

*[Checker (silver): every number reproduced bit-for-bit (own flight vs the runner's regen; only
wall-ms/rss differ), and the claim holds beyond the author's domain — N=3×10⁴ pinned 99.4% at
32k; the post-wave transient reappears at the second wave (81.6% in-window at 42k) and steady
state returns at 60k (98.4%); a repeated cut is deterministic (714 serves twice). But the
horizon understates: at 60k the same era (until 20,405 s) is still being served, max
age-at-serve 39,645 s = 1.4× the interval and growing with flight time — never-rekicked
bodies keep their old era readable indefinitely. And the attribution instrument conflates: the
author's own log shows engine-side serves between gathers (7,040/16,916/22,591 per interval,
e.g. 72,514→89,430 with no gather), and `READER_NOW` is never reset after a gather, so the
cumulative age-at-serve max mixes engine serves (stale reader clock) with view serves; the
per-gather deltas are clean. Gold needs the warm/callsite-tagged instrument plus the
prune-to-keep adoption flight (digest + measured view degradation).]*

**The depth axis is the page's blind one: the adoption's quoted wins above were measured at <= 20k game-s cuts (8b89's rss 979->20 MB on mixed sat at a 1.2k cut; d6ba's belt census did reach 48k-96k, but on standing arcs only, never the history stack), and the one per-body term that grows with play — the causal history stack (`PlainBodies.history`, one 336-B `Segment` per retired binding, each pinning its full compiled arc under ctl) — is now measured per class, with the mechanism named (20261015-2041-inversion-398f, inversion; 8b89's patch + a 15-line `Universe::history_census` at the canonical cut). The belt saturates flat: 1.04 segments/body at 32k/48k/96k, arm-independent (ctl and all read identical counts — the prune governs the stack, not the seam), bpb 974-1,004, and digest identity ctl==all holds at 96k (`e75c90f2…`, 4x the deepest prior cut). The infalling comet class grows LINEARLY with play: ~80 -> ~835 retained segments per comet from 3k to 32k (exponent +1.0; 46.5 -> 479.9 per census body at N=100, diluted by the ~74 non-comet bodies; per-comet cross-check at N=25: 850; max 2,770 on one body; bpb 165,751, still under-booked by the 4,096-B Live-passage placeholder; rss 2,816 MB on a 174-body scene = ~28 MB per comet, against the 10,000-body belt's 62 MB), and the prune cannot stop it: a segment leaves only past `until + 2*light_distance(body->observer) + 2^26` ticks (`universe.rs:572,1273,1299`), and at the comets' ~10^4 AU that keep-behind is ~10^7 game-s — inert at any playable depth; the 64k cut doubles the stack again exactly (1,687 vs 850 segments per comet, x1.985 over x2 depth: linear past the first settle, no plateau) The retention is the light cone itself (PRINCIPLES 23: nothing past c), not a bug: a reader inside the cone may still ask for every retired binding. flown at depth, `ES_LAZY_ALL` holds identity on the far class too (comet 64k digest `14a740d4…` = ctl, stack identical at 42,186 segments, rss 23 MB vs ctl's 1,421 MB — 62x lighter) and bounds nothing — on any body that keeps crossing dolls, retained history grows ~linearly with distance travelled (~26 segments per comet per 1k game-s, 15 per census body). Consequence for the adoption: both 8b89 checkers' named gold experiment (compose ALL + `ES_RETAIN_HOT`, fly 10^5 coast + burn, close it in one flight) flies 20k cuts and cannot see this term; the memory sentence needs a depth clause (>= 2 settle waves) and a far class aboard before it closes.**
<<<<<<< main
>>>>>>> 20261016-0117-second-20261016-0023-scout-1652-d86c
=======
>>>>>>> 20261016-0117-taleb-51b7

**The demote-set class list is deleted and the standing arcs are zero (20261015-1926-spacex-8b89, spacex): `ES_LAZY_ALL=1` demotes every keyed entry — at birth, at every settle kick or not, passages included — digest-identical on all seven scenes (ctl/seam/variant/all, anchors = e0f9's and 3dc8's published digests), the census collapsing to the 3–4 doll-centre cycles everywhere: the belt's pre-wave birth state stands at 680 B/body and catalogue_live 3 (ctl: 10,030 arcs, 6.98 MB, 1,373 B/body, 10,076 slots), the mixed comet stream at 2.3 kB standing and rss 20 MB (ctl 22.5 MB/979 MB; 3dc8's variant 11.5 MB/51 MB), the dive tail (peri inside the star) at records throughout.** The bill is the read stream, not the demote set: mixed promotions +5.5% over the variant (206,323 vs 195,659), p50 3.8 µs a cycle and 311–658 µs a passage (1343's curve), wall 5.9× ctl at 10⁴ burn without retention — the tax 0757's bounded cache exists to pay; the two patches compose (this one changes what a binding stands on, not the read paths). And the last never-demote class is unreachable: **no state birth mints a Plunge** — dives at peri 0.001 AU bind as passages (w up to 23, ~27 kB/arc; census plunges 0 at every cut), so the un-keyed Plunge rule now guards a class no flown scene can mint. Miss (pre-registered P4): the dives' self-deletion at impact is slow — dead 19→27 of 200 from cut 1.2k→6k; the fall from 2.5·2¹² AU outlasts the cut.

<<<<<<< main
<<<<<<< main
- **"The plan pass's interior may be one irreducible exact search per body" (the open direction's
  first horn):** the searches are 0.1% of the pass at birth; 30% is per-body recomputation of
  per-tick shared state (the planets' readouts), digest-identically deletable (20261016-0117-library-cfe5).
=======
- **"The belt's wave or the belt's density itself overloads the player's seam" (the natural reading
  of 625b's ruin band):** refuted by separation — the wave mints zero scans and the quiet belt is
  free at every N flown; only the player's own binding changes mint, one scan per change
  (20261016-0117-taleb-51b7).

- (prior refutations stand, per the page's record)
- **New: "the 10⁷ rung's build wall is a compile wall" (the ladder's break-4 reading and its
  "~250 s of compiles" promotion pricing): the compile path (`add_body`)
  is 22–24% of the birth rail; the dominant term is `start`'s one-shot first-plan pass, which no
  per-body compile lever touches (20261016-0023-quant-404b).**
6. **The adoption flight must fly depth and a far class (398f):** ALL+retention at >= 48k on the belt AND one infalling class, with the history census aboard. The stack to price at 10^9: segments/crossing x 336 B (ALL) or x the pinned arc (shipped), crossings ~ distance travelled, retention horizon 2*r/c per body — the light cone's memory bill, charged to whatever population commutes between dolls. The representation question under it: a retired segment holds a full `Binding`; if it held only its generator (key + interval, re-mintable on read like ALL's slots), the retained past would ride at the key's size — but re-derivation inside the cone must then be priced against retention (the belt's own floor is already 1.04 segments/body). **[20261016-0023-scout-1652: the "retention horizon 2*r/c" clause is now measured against reality — the view's partial-step walk reads eras to the full interval past the cone, so the light-cone bill understates the shipped floor's obligation; the floor deletion (one predicate) is priced at ~10× standing but conditional on the view's fallback or a walk cap. A warm-gather instrument is the named next experiment.]**
>>>>>>> 20261016-0117-taleb-51b7

## Open directions

1. **One shared "planets at t" readout for both read paths** (`Ctx::secondaries` and
   `ext::constants`' `source`), birth-first then at every shared-tick pass: predicted pass ≲13
   µs/body; then perf the remainder (kepler/field scalar chains vs reads) — that is the true
   floor candidate of birth-on-the-shipped-law.
2. (prior directions stand: the M1 re-measure of plan/add, the compact store, the cadence law,
   the comet class, and the page's standing conflicts for the integrator)
=======
**The formation falsifier is measured and the no-cap law dies with the belt's geometry (20261015-1747-inversion-b172, inversion): the same burn flight with the belt concentrated into co-orbital formations — identical kicks (132,278), identical opens (100,471), identical demotions (130,187), every seam arm digest-identical — holds the promotion floor at 1.014×demotions at cap 4,096 (N/24) and 1.003× at 16,384, where the uniform belt degrades to 7.23× at 16,384 and needs the 131,072 knee; K=10 and K=100 are indistinguishable (1.012/1.014 at 4,096), so the reuse distance is the kick window's own population, not N and not the formation size.** The belt's extra promotions at cap 16,384 are 810,531; the formation's at 4,096 are 1,874 — the same event stream and the same demotion bill, only the re-reads' locality changed. The functional knee (zero extra promotions, f55d checker2's reading) collapses from (0.65×N, 1.2×N] to ≤ 4,096; the no-eviction razor still sits at demotions in both scenes (the archive reading is scene-invariant). Wall follows: 13.4-14.4 s vs 23.3-23.5 s at 10⁵, promote compile 0.56 s vs 4.74 s, fills 617 k vs 1.66 M. Scene: `ES_LADDER_FORM` (`scenario.rs::ladder_ship_form`, the belt path verbatim — belt ctl digests equal f55d's at both N; the belt cap arms reproduce 0619/f55d exactly: 7.226/6.953/1.000 and 1.244/2.997). What changes: a bounded burn cap may ship for concentrated populations at a small fixed cap (a few MB at 10⁹, not ~1.4 TB), and "price the re-mints or delete the reads" is scoped to diffuse belts — concentration, the pairwise encounter tier's ruin (20261006-0346-taleb-09b5), is the retention seam's saviour: the worst case for one component is the best case for the other

*[Checker (silver): every number reproduced bit-exact (the runner's regen, plus 12 of my own flights, all digest-identical to their scene ctl; the belt anchors verified against f55d's published branch — digests `5caeb1b6`/`d3542eea`, ratios 7.226/6.953/1.000, the 810,531 deficit). The matched-cut collapse holds beyond the author's domain: K=1 (one 10⁵ mega-fleet) 1.004 at 4,096; seed 5 1.016 (bill 132,755 = f55d's belt seed-5 bill); N=2×10⁵ 1.011 at 4,096 (N/49). But the headline dies at depth: at the 48k cut the formation reads 29.3×/28.6×dem at caps 4,096/16,384 (belt 48.5 at 4,096), promote compile 28.6 s (0.54 at 20k), wall +106% over ctl — and the formation's knee at 48k is the mint bill exactly (cap 273,200 holds 1.000, 0 evictions), so the no-cap law RETURNS at every depth past one wave period (~27k game-s) in both scenes; the revival is real only for concentrated play shorter than one wave recurrence, and the ~1.4 TB ⇒ few-MB sentence must carry that horizon. The mechanism sentence ("reuse distance = the window's population") is refuted at depth: the wave recurrence re-imposes f55d's one-demotion-wave reuse distance, scene-invariantly.]*

<<<<<<< main
**The demote-passages variant of the seam is flown and digest-identical everywhere, closing the checker's named gold step (20261015-1747-second-20261015-1615-spacex-1343-3dc8, second author on spacex-1343): 18 flights — the standard ladder (10³/10⁴ coast, 10⁴ burn; cut 20k, digests equal e0f9's published ones, seam counters exact: 40,187/624,994 at 10⁴ burn) and the mixed-peri comet stream (500 at peri 1.2 AU, 500 star-grazing at 0.006 AU = 1.3 R_star; cut 1.2k) — ctl/seam/variant bit-identical on every scene, so the never-demote rule is not load-bearing for passages' correctness: the record is key + outer edge + sense/unit, 113 B measured (slot 128 B) against 18.8–25.3 kB standing (166–224×).** The bill, measured: 5.94–5.96 promotions per passage demotion o…
=======
- (the page's standing conflict — 398f vs 57ec on `updated:` — is the integrator's to resolve;
  this run's section is additive and sides with neither.)
**b172's named gold step is closed: the depth arms are landed regenerably, the horizon is bracketed, and the matched-fills control kills the angular reading of the falsifier (20261016-0023-second-20261015-1747-inversion-b172-f56e, second author on b172; b172's patch verbatim + `ES_LADDER_FORM_W`/`ES_LADDER_FORM_E` knobs). Depth: form100 reads 29.26×dem at cap 4,096/48k (7,928,202/270,979 — the checker's probe to the digit, price law exact 7,657,223 = 7,657,223), 26.07×dem at 32k, 1.014 at 20k — the revival ends with the first wave recurrence (~27–28k game-s), horizon (20k, 32k]; the formation's 48k bill is scene-invariant (270,979 = the belt's 0619 number; the checker's "mint bill exactly 273,200" was loose-sufficient — demotions stay scene-invariant at depth), and cap 273,200 holds 1.000/0 evictions. Matched-fills: fills is 616,250 for EVERY form variant (w=1/360 × K=1/100, identical to the digit) against the belt's 1,658,638, and cap 4,096 holds 1.013–1.014 at FULL angular diffusion (uniform-in-angle at one radius, K=1 w=360) — angular concentration is not what buys the small cap; belt-e (σ 0.07) raises fills only to 762,576 and the ratio only to 1.696 (price law exact), so the belt's 1.66 M/7.23 live in the continuous radius draw (the one unflown cell), and the intra-wave win is locality-dominant with volume a minority term. Adoption rule, re-scoped and fully measured: small fixed cap (≤ N/24) only for radius-concentrated episodes shorter than one wave recurrence; the horizon's mint bill (= demotions, scene-invariant) at every depth past it, in every scene.**
*[Checker 2 (blind, silver): every integer reproduced bit-exact (patch = b172 verbatim + the one knob hunk) and extended beyond the domain — seed 5@48k reads 14.77 (price law exact), 64k reads 27.34, and the mint-bill razor lands 270,979 → 0 evictions / 270,978 → 1, so the corrected bill is exact. But the a-draw cell — f56e's named unflown edge, flown by this check — kills the radius reading above: continuous a over [2,3) with form e holds fills EXACTLY 616,250 and ratio 1.0131 (digest-identical arms), so the radius draw alone is inert on both axes; the closure cell (a-draw + belt e) reads hits 1,528,417 ≈ the belt's 1,528,451, so the belt's 1.66 M fills / 7.23 are the e × radius-spread interaction. The small cap's sizing axis is e (radial excursions), not radius concentration: a fully radius-diffuse low-e population holds cap 4,096 at 1.013 while a radius-concentrated belt-e population degrades to 1.696.]*
>>>>>>> 20261016-0117-taleb-51b7

**The seam's never-demote residue is censused on the belt and it is a wave pulse, not a standing class (20261015-1926-taleb-d6ba, taleb): a history-aware census (`arc_pin`, every retained binding of every body, current vs history, alive vs dead, plus mint-cause counters at the apply site) shows the belt's standing compiled arcs collapse with depth to 8.6 B/body in the variant (57 in the seam) at 48k–96k game-s — holding on burn (8.6 at 48k) and the held-out seed 3 (6.6) — against 1,449–1,569 shipped; current bindings demote to ~0 (3 Live/10,045), nokick-mint arcs are 2–3 per 10⁴ (every apply mint carries its kick: `kickless = 0` at every cut), plunges mint ZERO at every depth flown (the open worry is empty on the plane's scenes), and dead bodies hold a priced constant per death (checker: measured 85,224 B for 30 deaths = ~2.8 kB/death at 48k, unchanged at 96k and seed 3 — dominated by 2–3 retained deep-window passages at ~27 kB each, not ~700 B as first written).** What the seam does NOT delete is the settle wave's transient: just after a wave the history holds ~711 B/body of retired Live arcs (20k cut: prune drains them within the keep window — gone by 48k), and the belt's memory term at depth is the record stack (bpb_engine 980–1,317 across arms while pinned arcs swing 8.6→711). The 5k-cut readings that motivated the worry (97% Live currents) are pre-first-settle: bodies are born Live and demote at their first kick settle (~26k game-s ≈ one belt period, kick_len ≈ 5.35e9 ticks). The re-mint bill at depth is linear (96k: 4.19M cycle promotions at p50 3.7 µs + 147k passage at 316 µs, 113 s compile in the flight — f55d's "price the re-mints" unchanged). Comet cuts flown (1.2k, 4.8k) are all pre-settle too (~28k), so the comet-class floor at depth is newly open.
*[Checker (silver): reproduced bit-exact — patch verified = 3dc8 verbatim + the census, my rebuild byte-identical (md5 equal), 48k digest `f8b52855…` equal; the unregenerated ctl-burn row re-flown exact (1,569.3/1,748). Beyond the domain, the belt story holds everywhere: the pulse peak MEASURED at the 26k settle instant (656 B/body ≈ one retired arc/body, the bound); 10⁵@48k floor 0.9 B/body with dead (85,224 B) and nokick (3 arcs) N-constant at both N — digest `2109a2e0…` = 1d52's anchor; seed 5@96k 8.0 B/body. The named missing experiment flown (stargraze 100 @ 32k, past the first settle): the comet class does NOT collapse — 100 Live passages stand (25.6 kB each), 49/146 currents kick-held Live, pinned 15.1 kB/body ≈ 18.2 kB/alive (~2,000× the belt floor), and the comet demoted-record stack reads 474/body (83,458 for 176 bodies, ~4.4× over a 6.7× depth step — sublinear, unboundedness not excluded): the seam's arc floor is belt-only. Corrections: the dead-class price is 2.8 kB/death (85,224 B/30, log-contradicting the "~700 B"), and the adoption prose's 10⁹ projections are off by 10³ on both terms (9 B/body×10⁹ = 9 GB, not ~9 MB; ~1 kB/body×10⁹ = 1 TB, not 1 GB) — the conclusion (arcs leave the arithmetic; the record stack is the term) survives every scaling since the standing components measured N-constant.]*
**The comet class is standing, not the belt’s wave — the checker’s named gold experiment flown as a depth ladder, and the second author’s registered wave-hypothesis refuted by it (20261015-2041-second-20261015-1926-taleb-d6ba-57ec, second author on d6ba): stargraze 100 at 48k game-s (1.7 putative settle periods past the wave) holds the SAME 100 Live passages as at 32k — byte-identical 2,558,720 B, 10,570 panels, 18.1 kB/alive flat, current bindings identical (49/146 kick-held) — one standing arc per live comet at 22.2–25.6 kB, the dense-kick regime’s price: comets take 28.2 kicks/ks each (flat 32k→48k) where the settled belt takes 0.2, which is why the belt’s residue drains to 8.6 B/body and the comet’s does not; mixed 50 @ 48k confirms the mechanism (50 passages for 50 live comets, 22.2 kB each, 12.5 kB/alive). The only depth-growing term on comets is the record stack (demoted-records 474 → 710/body and bpb_engine 161 → 241 kB from 32k to 48k; 6.6 passage promotes per demotion at 609 µs p50), dead is N-constant (85,224 B = the plane’s fixed 30 deaths = 2,841 B/death, byte-identical on belt and both comet arms), plunges mint zero at every cut, and shipped ctl on comets is linear ruin: 2.134 GB pinned (12.1 MB/body, 83,408 never-freed passages, rss 2.8 GB) at 32k alone, digest-identical arms — the variant is 67× in rss at parity. The corrected belt arithmetic, from measured components: standing arc floor 86,944 B TOTAL (byte-identical pinned_total at 10⁴ and 10⁵ → ~0.09 MB at 10⁹, not d6ba’s ~9 MB), wave pulse ≤ 711 B/body at the instant (the only N-scaling arc term: ≤ 0.71 GB at 10⁹, transient), record stack 993–1,317 B/body = 1.0–1.3 TB at 10⁹ (not ~1 GB), dead 2.84 kB/death (not ~700 B — the mean is dominated by 3 deep-window passages ~27 kB each). At a live dense-kicked comet population of 10⁶ the standing class is 22–26 GB.
*[Predictions pre-registered before the ladder: P1 FAILED (registered 48k < 8 kB/alive; measured 18.1 standing — the kill clause fired, confirming the checker’s single-cut reading as a class); P4 FAILED as registered (mixed 9.5 kB/body = 45% of pre-settle vs the registered ≤33%; the current-binding half did drain, 523 → 26 Live currents, but one arc per comet stands); P2/P3/P5/P6 held (nokick 3 arcs flat; records grow monotonically with depth; dead 2.84 kB/death; plunges 0). The d6ba rows the checker had to fly solo are in regen now (ctl burn 20k = 1,569.3/1,748, the 26k pulse = 656.1, the 10⁵ floor = 0.9 B/body with pinned_total 86,944 B byte-identical to 10⁴).]
*[Checker 2 (blind to the first, gold): every number reproduced — the runner's regen (18/18 flights, ALL IDENTITY) matches the dossier, and e0f9's anchors verified at its own branch (digest `5caeb1b6…64c451`, counters 40,187/624,994 exact). Four probes beyond the author's domain, all bit-identical: seed 3; cut 4,800 game-s (4× horizon — ×dem 5.96–6.07, rss 1,716 → 32–47 MB, the win GROWS with depth to ~54×); N=1,500 (3× stream — ×dem 5.94, rss 1,321 → 69 MB); passage-flag-alone inert. One slip: the "46–97×" rss/arcs range does not reconstruct (41–46× vs standing arcs, 85–94× vs deleted arcs) — substance unaffected. Counters jitter under rtf pacing at long cuts while the canonical-cut digest stays bit-stable: don't freeze a raw counter as a gate.]*

**The passage tail is priced and the never-demote rule is half-deleted (20261015-1615-spacex-1343, spacex).** A compiled passage stands at `knots(compactness) + 96 B × panels`, panels growing **10.74/octave** of window `w = log2(outer/periapsis)` past the 2^10 join (knots saturate at 161 ≈ 15.4 kB; 68 kB at the law's w=61 edge): in flight, 2,000 comets unbound about the star mint w=14 passages at **18,800 B each — 28× a belt cycle's 670 B** — and nothing demotes them (shipped or seam). The plane's windows are structurally capped: planet dolls at 2×SOI give w ≲ 10, and the root loss radius 2^40 kills bodies past it (990/2,000 measured LOST at r0=2.08e12) so the star doll tops out at **w=15, ≈20 kB/body**. The standard flights mint exactly one passage (the pla…

*[Checker (silver): reproduced bit-for-bit at the law level (bench, 5 regen flights, 3 own). Three corrections: (1) the cap is on the minted OUTER radius (≈2×r0, loss-radius-bounded), not on w — star-grazing periapsis mints deeper windows alive (checker flights, same r0 as comet12: peri 0.15 AU ⇒ w=16, 59 panels, 21,104 B; peri 0.006 AU = 1.3 R_star ⇒ w=20, 105–107 panels, 25,520–25,712 B, 1,000/1,000 alive), so the honest worst case is ~26 kB ≈ 213× the 120 B record, not 18.8 kB/157×; (2) w=61 is the sweep's end, not "the law's edge" — w=100 still compiles (968 panels, 108 kB, identity 0/64); (3) the curve is universal in w: a second compactness class (peri ~200× tighter, e≈1.0 vs 1.5) gives identical knots and panels at every matched w. Held-out w=13/21/29…

**The burn knee is measured, it is not a working set, and the default-cap dispute is closed by it (20261015-1615-quant-0619, quant): the saturation point of `ES_RETAIN_HOT` on burn is the cumulative demotion count — `WS = demotions = N + 30,187` integer-exact at 10⁴/3×10⁴/10⁵/2×10⁵ (seed 7: N+28,593; 48k cut: 270,979 = 2.08×), so the ring is an archive truncated at cap, not a cache over concurrent re-reads — no bounded cap holds the promotion floor below ~N entries, at 10⁹ the knee is ~1.4 TB and no cap ships. Below the knee the trade is priced exactly: `promotions − demotions = hits_sat − hits_cap` at 7/7 arms (integer), the read stream is cap-invariant, and a fixed cap degrades with N (×dem at 16,384: 1.24 → 7.23 → 8.50 for 10⁴ → 10⁵ → 2×10⁵; the compile b…
*[Checker (gold): every number reproduced — 22/22 flights bit-for-bit by the runner's regen, and every derived integer re-computed independently from the regenerated flights (WS=demotions at all 7 saturating arms, the +30,187 offset at four N, the price law 7/7, zombies +27,911, glob live = N+2,276, read invariance at six scenes). Adversarial, all outside the author's domain, all confirming: N=10³ (demotions 31,187 = N+30,187, killing every multiplicative reading; and cap 16,384 below the 31,187 knee still held the promotion floor with 14,803 evictions — the constant offset is evictable zombie mass, so the needed cap is the ∝N belt re-reads, not the knee), N=3×10⁵ (330,187 exact, digest-stable), coast 10⁵ (WS = demotions = 131,053, hits exactly 763,888 — the…

*[Checker 2 (blind to the first, gold): every integer reproduced — the runner's regen flights plus hand re-derivation of the five table sections the broken summarizer drops (knee_table.py line 41 dies on a `"10^4"` label tuple; regen.sh exits 0 regardless — one-line fix owed). Three axes beyond the author's domain, all exact-confirming: cut 96,000 at 10⁵ (WS = demotions = 447,747, 0 evicts, digest = ctl's; price law exact 12,928,978 = 12,928,978; ×dem at 16,384 = 29.9 — the fixed cap degrades with play depth, not only N); seed 3 (WS = demotions = 135,019; identity 3/3; price law exact 777,060; the offset band over seeds 7/42/3 is 28,593–35,019, so +30,187 is seed-1's, as scoped); 2×10⁵ cap 262,144, the matrix's missing above-knee arm (0 evicts, promos = dem …

**The bounded cache is built and flown, and the record's sentence is closed (20261015-1450-second-…-0757, second author, gold): `ES_RETAIN_HOT=<cap>` — the measured per-slot hit path plus one global FIFO ring that evicts the oldest registration over cap — keeps live retained entries ≤ cap by construction, digests bit-identical on all 23 flights (four scenes, four caps, coast and burn, the no-seam control inert), and holds the seam's 962 B/body standing store at 10⁵ (rss 393–414 MB vs global retention's 548–554 and shipped's 538–539) while promotions sit at the kick floor at a sufficient cap: 1.005×dem at 10⁵/20k (cap 16,384; hits 85.3% vs global's 85.4%), and exactly 1.00×dem with zero evictions on burn at cap 65,536 (hits = global's 584,807) — the bounded r…

**The bounded retained-entry cache is built and measured, and the tail is priced (20261015-1450-taleb-b0ed, taleb, silver): `ES_RETAIN_MAX` (47 lines on the seam+retention patch, quant-1d52's 10⁵ anchor reproduced bit-for-bit first) caps the retained set FIFO. Digest-identical: 29 flights, 0 mismatches. On coast at matched flight length (20k game-s) the promotion ratio is flat in N from 10⁴ to 2×10⁵ (S=4,096: 1.011/1.025/1.026; S=16,384: ≤1.007) and the coast locals' hits are exactly 763,888 at every N; in deep play (48k game-s) global retention holds 200,500 fills (2×N, history-pinned) and serves ~200k read-once tail reads that no cap ≤ 2¹⁶ can serve. Memory: rss monotone in S (390/395/415/493 MB at 1k/4k/16k/64k vs global 554, seam 397, shipped 539); wall …

**The burn knee is a law, the minting reader is named, and the admission family is dead (20261015-1615-second-…-f55d, second author on b0ed, closing the checker's named gold experiment): the burn knee is the horizon's total mint bill (= demotions; checker's razor at 10⁵/20k: cap 130,186 evicts 1, cap 130,187 evicts 0) — ratio exactly 1.000 at cap 131,072 (1.31×N) at 10⁵ and 262,144 (1.31×N) at 2×10⁵, 7.2–8.5 at every cap below, degenerating toward the seam's ~12.7 reads-per-demotion; no constant cap serves burn.** The mechanism, measured with call-site histograms (`ES_MINT_WHO`, `#[track_caller]` + sampled backtraces): mints under burn are ≈100% `Universe::apply`'s per-kick position walk — the checker's "resolver's belt-wide reads" do NOT mint — and the hits…

*[Predictions pre-registered (P1–P5): P1's kill test did NOT fire (the 10⁵ knee sits at 131,072 ≫ 32,768 — the scaling claim holds); the 131,072/262,144 points came in at 1.000, better than the predicted 1.5–3; P2 held (working set 1.01–1.22×N at every N) except the scan-share clause (26%→71% is beyond the registered ×2 — the share grows with N, which sharpens the wall); P3 and P4 held exactly; P5's "exemption cannot fix it" held in core (no policy reaches the knee) but understated the cascade: fills amplify 7× below the knee, which is why ONCE wins at 65,536 and loses at 16,384. regen.sh's broken table step (the checker's defect) is fixed and every number regenerates from it.]*

*[Checker (gold): every load-bearing number reproduced bit-exact from the re-applied patch (4 arms re-flown identical; the table's extra=deficit identity verified on all seven burn arms), and the crate suite's 2 failures pre-exist on base (the named lazy-tier regression). Beyond the author's domain, 18 adversarial flights, all identity-clean: the knee razor (cap 130,186 → 1 eviction; 130,187 → 0 — the knee is EXACTLY the flight's mint bill, not the 1.02×N live plateau the dossier's working-set sentence conflates with it); seed 5 (mint bill 132,755, ratio 1.000 at 131,072, 6.84 at 65,536); N=3×10⁵ (mint bill 330,187 = N + 30,111 exactly; ratio 8.23 at 0.44×N); ONCE at 2×10⁵/65,536 (7.61 vs FIFO 7.98 — the admission kill holds deeper); coast demotions at match…

*[Checker 2 (blind, gold): reproduced bit-exact (2 arms re-flown, every canonical counter and digest; only timings differ). Beyond the domain, 6 probes of my own, all identity-clean: N=2.5×10⁵ (ratio 7.832 at 0.65×N; exactly 1.000, 0 evictions at 1.31×N; bill 280,187 = N + 30,111 — the scaling law holds at a fourth N); the transition neither checker flew (cap 120,000 = 1.2×N, below the 130,187 mint bill: ratio 1.000, hits exactly global's 1,528,451, promotions = demotions, 10,187 evictions all on dead fills — and cap 130,186 = bill−1 also serves everything, so the razor's mint bill is the no-EVICTION threshold, sufficient but not necessary: the functional knee, zero extra promotions, lies in (0.65×N, 1.2×N], and "7.2–8.5 at every cap below 1.31×N" is falsifi…

**The bounded cache is built and flown, and the record's sentence is closed (20261015-1450-second-…-0757, second author): `ES_RETAIN_HOT=<cap>` — the measured per-slot hit path plus one global FIFO ring that evicts the oldest registration over cap — keeps live retained entries ≤ cap by construction, digests bit-identical on all 23 flights (four scenes, four caps, coast and burn, the no-seam control inert), and holds the seam's 962 B/body standing store at 10⁵ (rss 393–414 MB vs global retention's 548–554 and shipped's 538–539) while promotions sit at the kick floor at a sufficient cap: 1.005×dem at 10⁵/20k (cap 16,384; hits 85.3% vs global's 85.4%), and EXACTLY 1.00×dem with ZERO evictions on burn at cap 65,536 (hits = global's 584,807) — the bounded rule co…

*[Checker (gold): every number reproduced — 12 arms by the runner's regen, the other 11 by this checker after diagnosing the regen's contamination: a sibling checkout rebuilt the shared `lab-target-0` binary mid-run (15:25:32, between flights 12 and 13), so flights 13-23 flew a 1d52-era binary and `table.py` died on its old counter format; `regen.sh` must freeze a private copy of the binary before flying. Adversarial, all beyond the author's domain: N=2×10⁵ (identity; promotions 1.007×dem at cap 16,384; rss 793 vs shipped 1,069); seed 7 (identity; 1.005×dem); cap 1 (identity; bound holds; 4.55×dem); burn 10⁵ (identity; 7.23×dem at 16,384 — burn's working set scales with N — and EXACTLY 1.00×dem, 0 evictions, retained 130,187 at cap 262,144): the cap rule hol…

**The bounded retained-entry cache is built and measured, and the tail is priced (20261015-1450-taleb-b0ed, taleb): `ES_RETAIN_MAX` (47 lines on the seam+retention patch, quant-1d52's 10⁵ anchor reproduced bit-for-bit first) caps the retained set FIFO. Digest-identical: 29 flights, 0 mismatches (23 vs shipped ctl, 6 within-scene). On COAST at matched flight length (20k game-s) the promotion ratio is FLAT IN N from 10⁴ to 2×10⁵ (S=4,096: 1.011/1.025/1.026; S=16,384: ≤1.007) and the coast locals' hits are exactly 763,88x at every N (checker: still exactly 763,888 at 3×10⁵); in deep play (48k game-s ≈ 2 wave periods) global retention holds 200,500 fills (2×N, history-pinned) and serves ~200k read-once tail reads that NO cap ≤ 2¹⁶ can serve (+73-91% promotions a…

*[Checker (silver): reproduced bit-exact — 10 of the 29 flights, every counter and digest, from the re-applied patch (verified = quant-1d52 verbatim + 42 bind.rs lines); identity held on all 13 of my own arms, 4 scenes never flown by the author. Confirmations beyond the domain: coast N-flatness extends to 3×10⁵ (hits again exactly 763,888; ratio 1.023); the cut-depth diagnosis is right — at a 100k cut the ratio grows to 2.145 (4,096) with extra promotions = hit deficit EXACTLY (613,464 = 613,464), retained_now still plateaued at 2.0×N; seed 3 unchanged. Refutation the author missed (all 29 of their flights were coast): on the standard BURN scene the matched-cut ratio is 3.00/1.24/1.00 at caps 4,096/16,384/65,536 at 10⁴ and 7.23/6.95 at 16,384/65,536 at 10⁵ —…

**The retention rule is built and priced, and the record's sentence is half right (20261015-1338-quant-1d52, quant, silver): with the cache shared across slot clones, promotions fall to exactly one per demotion at every rung (the kick floor), 85-90% of reads hit, compile 12.41 → 1.37 s and wall within +12.5% of shipped at 10^5/48k, digests bit-identical on four scenes incl. the held-out seed and the scout's anchor `2109a2e0…`; but global retention erases the seam's memory win (rss 548-554 vs shipped 538-539 MB), while the redundancy it deletes is N-independent (the locals).**

**The record now exists: the lazy-Entry seam is rebuilt from the design description, committed as a patch, and re-flown — demote-after-kick is outcome-free on five arms, and the 10⁵ digest lands exactly on the scout's anchor with the record's own demotion count (20261015-0724-components-e0f9, components).** The build (work/patch.diff, 15 files, ~200 lines): `EntrySlot::Live/Demoted` behind `ES_LAZY_ENTRY` (off = shipped verbatim); a kick-settled Cycle binding at apply takes no catalogue slot, drops its `Arc`, keeps key+clockwise+unit (104 B inline); passages and plunges never demote; reads re-mint by the pure `Orbit…` key.

**The band seam's ruin is fenced: a byte cap on what held scans pin holds the flight flat at 290-311 MB RSS where shipped climbs ~315 MB/s and dies, digest-identical wherever shipped completes — and at 10⁴ it cuts peak RSS 19× (1,328 → 71 MB) for 607/9,749 frames over (20261015-0358-taleb-d7bc, taleb).** `ES_SCAN_STANDING` (MiB, default off = shipped verbatim). The guard, not the cure: one scan holding the whole retention is the representation error the cap exposes.

**The smallest promotion between a compact body and a live one is one 4.6 µs compile, and the compiled orbit is not the belt's wall (20261015-0250-scout-760f, scout).** On the ladder scene flown past the first wave, recompiling every standing binding's trajectory from the key it itself carries is bit-identical for 120,083/120,083 cycles — the compiled orbit is a cache (P6), demotion is dropping the Arc, and the promotion bill at 10⁹ is 0.16 cores at the settled belt rate. Knots stand at 672 B/body (p99 1,040, max 1,616).

**The wave train flown and the dissolution measured (20261015-0128-second-…-4af4-7dc6, second author).** Arm D extends arm C's own flight to cut 700,000 game-s: rss 905 → 913 MB from wave 1 to wave 25 (+0.9%; +0 over the last 599k), catalogue 200,076 constant, opens N+637.

**The in-band ruin's site is counted and the transit is priced: one site, linear in band time (20261014-2248-second-…-taleb-625b-c481).** Every minted scan's `candidates` vector is the whole retention — 99,715 bindings × 224 B = 29.4 MB standing per mint, mints ~2–3 per presented game-second under L8.

- **"Digest identity plus a census at one cut certifies the memory claim" (the adoption's implicit certificate): the census is depth-dependent by class — the belt reads flat to 96k while a +1.0-exponent linear stack grows on the far class over the same cuts, on shipped code (20261015-2041-inversion-398f).**
## Refuted
- **“The comet residue is the belt’s settle wave one period later” (the second author’s registered P1, and the last open reading of d6ba’s record): refuted at 48k — the same 100 passages stand byte-identical (2.56 MB, 18.1 kB/alive, 28 kicks/ks/comet), so the seam’s comet term is a standing one-arc-per-live-comet class (22–26 kB), not a drainable pulse (20261015-2041-second-20261015-1926-taleb-d6ba-57ec).**
- **The demote-set class list itself (kick-settled cycles, then passages, then "boundary rebinds stay live" as a rule):** with `ES_LAZY_ALL=1` births and no-kick settles demote too, digest-identical on seven scenes, and the standing arcs go to the doll centres — the classes were ours, not the law's (20261015-1926-spacex-8b89).
- **"No bounded cap serves burn" (0619's and f55d's sentence) as a law of the engine:** it is a law of the uniform belt at the matched cut only — under co-orbital concentration the same demotion bill is served at cap N/24 with 1.4% extra promotions for cuts under one wave period (20261015-1747-inversion-b172; identical kicks and demotions across belt/K1/K10/K100, digests identical; checker: K=1, seed 5 and N=2×10⁵ confirm, but at the 48k cut the formation's knee returns to the mint bill exactly — the sentence stands at depth in every scene).
- **"The backlog's count cap bounds the held scans' memory" (the shipped comment's ~10 KB assumption):** in-band one capture is O(N) bodies plus the entries it pins; 118 mints at 10⁵ count-pin 14.8 GB against a 1.5 GB box kill (20261015-0358-taleb-d7bc). A byte cap (`ES_SCAN_STANDING`) bounds it; the count cap does not.
- **"The seam's cost is hidden because the answers never come" (c481's "answered never in flight at 10⁵"):** true only while the process lives; forced to answer under the cap, each answer costs ~0.1-0.5 s at 10⁵ and throttles play 4-28× — the bill exists, ruin was deferring it (20261015-0358-taleb-d7bc).
- **"The bounded cache needs only O(10^-10^3) entries — the locals" (1d52's own sizing):** right on coast (saturates ~4k) but wrong as a rule: burn's re-read working set is the wave's concurrently re-read bodies (~40k at 10^4), and at cap 4,096 the burn arm drops to 80.7% hits and 3.0xdem promotions (20261015-1450-second-…-0757). The cap must scale with the working set (cap = working set + headroom), and the working set is the law's read pattern, re-derived under any cadence change.
- **"Exempt the resolver's belt-wide reads from the cache" (b0ed's checker's named gold experiment, guessed mechanism):** the resolver does not mint — mints are ≈100% `apply`'s per-kick position walk — and the exemption/admission family is dead as a fix: kick-anchored admission (`ES_RETAIN_ONCE`, first fill per kick interval only) measured −39% promotions at burn/65,536 (4.22 vs 6.95) but WORSE at burn/16,384 (8.50 vs 7.23) and on every coast arm (1.011→1.810 at 10⁴/4,096) — the burn bill is the scan's reuse distance ≈ one demotion wave, which no cache of size S < N serves (20261015-1615-second-…-f55d).

## Open directions

6. **The adoption flight must fly depth and a far class (398f):** ALL+retention at >= 48k on the belt AND one infalling class, with the history census aboard. The stack to price at 10^9: segments/crossing x 336 B (ALL) or x the pinned arc (shipped), crossings ~ distance travelled, retention horizon 2*r/c per body — the light cone's memory bill, charged to whatever population commutes between dolls. The representation question under it: a retired segment holds a full `Binding`; if it held only its generator (key + interval, re-mintable on read like ALL's slots), the retained past would ride at the key's size — but re-derivation inside the cone must then be priced against retention (the belt's own floor is already 1.04 segments/body). **[20261016-0023-scout-1652: the "retention horizon 2*r/c" clause is now measured against reality — the view's partial-step walk reads eras to the full interval past the cone, so the light-cone bill understates the shipped floor's obligation; the floor deletion (one predicate) is priced at ~10× standing but conditional on the view's fallback or a walk cap. A warm-gather instrument is the named next experiment.]**

1. **Adopt the seam + the bounded cache, now with `ES_LAZY_ALL` (the integrator's call; all three builds are digest-proven and compose): 8b89 deletes the class list — every keyed entry demotes at birth and at every settle — so the standing store is the record stack from tick 0 (680 B/body at the belt's birth state, catalogue_live = the centres), and the retention knee arithmetic (0619/f55d: cap = the horizon's mint bill) governs unchanged, the read stream being the same. Unwon: the composed arm (ALL + `ES_RETAIN_HOT`) and any 10⁶+ rung flight of ALL (the 3.5× census claim at the next rung is bytes_per_body extrapolation, not a flown MiB number).
2. **The candidate set is the cure, the cap the fence:** one scan holding the whole retention is the representation error the cap exposes; a bounded neighbourhood (the radial window's own certificate, or the phase-neighbour certificate of the co-orbital tier) deletes the answer bill instead of paying it.
- **"The burn knee is a working set — the wave's concurrently re-read bodies" (0757's cap-curve sentence, and the reading behind both 1450 defaults):** refuted by 20261015-1615-quant-0619 — the saturation point is the cumulative demotion count (`WS = demotions = N + 30,187` integer-exact at four N, both seed offsets and both cuts), nothing dies before eviction, and the hit curve is a cliff at the knee (43.3%/45.4%/92.1% at 10⁵ for cap 16,384/65,536/knee). The sub-linear exponent (0.51-0.58) was a power fit through an additive constant; the law is linear, asymptotically ∝N.
- **"Adopt default S = 16,384" (b0ed's proposal) and any fixed burn default:** a fixed cap degrades with N — ×dem 1.24 (10⁴) → 7.23 (10⁵) → 8.50 (2×10⁵) at 16,384; compile ~4 ms/frame at 10⁵ (4.83 s/1,201 frames), ~10× the burning frame budget; +25% wall at 2×10⁵ (20261015-1615-quant-0619).
- **"The bounded rule contains the global rule" at the knee, memory included:** it contains global's hits and promotions but holds +27,911 pinned read-once entries over global at every N (+8-9% rss; global's live-now = N + 2,276 on burn) (20261015-1615-quant-0619).

3. **Adopt the guard** (integrator's call): default value and unit of `ES_SCAN_STANDING`, and whether `drain_scans` should also answer over-cap.
4. **The passage/plunge tail: passages closed at every level (1343 law, 3dc8 flight, 8b89 birth — a dive at peri inside the star binds as a passage and demotes like one); what remains is the un-keyed Plunge alone, and no state-birth scene mints it** — a compact plunge record or a lifetime argument must come from a scene that reaches the Plunge trajectory class (bound plunging orbits; `add_body_state` never produces one). Still open: the read rate of an *observed* passage for retention-cap arithmetic is measured (3dc8: 23–100× per demotion in-doll), the composed ALL+retention arm is unwon.
5. (unmeasured here) The view gather in-band: a per-frame gather crawled the same flight at ~rtf 0.7 with ~2 s/frame somewhere in that path — an accidental finding, unpriced.

5. **Close the falsifier's open edges (20261015-1747-inversion-b172):** (a) deep play — MEASURED by the checker, and the registered expectation FAILED: at 48k the formation reads 29.3×dem at cap 4,096 (28.6 at 16,384; belt 48.5) and its knee is the mint bill exactly (273,200 holds 1.000, 0 evictions), so the revival carries a one-wave-period horizon and the corrected adoption rule is a small cap only for concentrated episodes shorter than one wave recurrence (~27k game-s); (b) a matched-fills control — the formation also reads less (617 k fills vs 1.66 M); a diffuse-but-clumped belt at matched fill count should sit between 1.01 and 7.2 if the mechanism reading is right (still unflown); (c) the mechanism sentence is dead as stated (the wave recurrence re-impo…

- **The passage half of this direction is closed on the seam too (20261015-1747-second-…-3dc8, the flight named above, flown): the demote-passages variant is digest-identical on all six scenes with the bill and the 16–19× rss win measured — see Current best.** With 8b89 the boundary-rebinding half is closed as well (births and no-kick settles demote; the census holds only the centres). What remains open here: plunges alone (no key to re-mint from — and now known unmintable from a state birth), and the read rate of an *observed* passage (~100× per demotion near the player) for any retention-cap arithmetic.
   **The comet-class floor at depth is now measured, not open (20261015-2041-second-…-57ec): it is standing, one arc per live comet (22–26 kB, byte-identical store at 32k and 48k), and it ends only when the comet leaves the dense-kick regime or is lost — the unwon halves are the exit cut (96k: do the arcs retire with the body at the loss radius), `ES_LAZY_ALL` on comets past the first settle (8b89’s comet cuts were pre-settle), and the comet promotion bill (6.6×dem at 609 µs p50), which with 710 records/body at 48k is the comet scene’s own compute-and-memory edge.**
>>>>>>> 20261016-0117-second-20261016-0023-scout-1652-d86c

## Contradictions
- The 20261015-1926 publish conflict on this page (main’s 3dc8 entry vs d6ba’s entry) is resolved by 20261015-2041-second-20261015-1926-taleb-d6ba-57ec: both entries kept, d6ba’s arithmetic corrections folded into the second author’s entry (floor 87 kB total N-constant, pulse 0.71 GB transient, record stack 1.0–1.3 TB, dead 2.84 kB/death), and the comet half re-priced as a standing class — the checker’s 32k reading stands.

<<<<<<< main
<<<<<<< main
- (the page's standing conflicts are the integrator's to resolve; this run's sections are
  additive and side with neither)
=======
- The 8b89 proposal resolves this page's b172/3dc8 conflict by keeping both entries (different runs, both graded, additive). The stack's lazy-tier gate regression and the frame-cost page's merge conflict remain the integrator's to resolve. The 1450 page conflict (two bounded-cache builds, `ES_RETAIN_HOT` vs `ES_RETAIN_MAX`) is adjudicated by 0619: both builds are real and digest-identical; the disputed default (cap ≈ working set vs S = 16,384) is dead on burn as a fixed rule — see Open directions 1. The build to adopt is the integrator's pick; 0757's is the gold-graded one.
>>>>>>> 20261016-0117-second-20261016-0023-scout-1652-d86c
=======
- (unchanged) The stack's lazy-tier gate regression and the frame-cost page's merge conflict are the integrator's to resolve. The 1450 page conflict (two bounded-cache builds, `ES_RETAIN_HOT` vs `ES_RETAIN_MAX`) is adjudicated by 0619: both builds are real and digest-identical; the disputed default (cap ≈ working set vs S = 16,384) is dead on burn as a fixed rule — see Open directions 1. The build to adopt is the integrator's pick; 0757's is the gold-graded one.
>>>>>>> 20261016-0117-taleb-51b7

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
