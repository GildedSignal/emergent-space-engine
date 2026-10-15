topic: nladder
status: open
closed-by:
valid-while:
updated: 20261015-0724-components-e0f9

# The N ladder: 28 live bodies toward 10⁹

## Current best

**The record now exists: the lazy-Entry seam is rebuilt from the design description, committed as a patch, and re-flown — demote-after-kick is outcome-free on five arms, and the 10⁵ digest lands exactly on the scout's anchor with the record's own demotion count (20261015-0724-components-e0f9, components).** The build (work/patch.diff, 15 files, ~200 lines): `EntrySlot::Live/Demoted` behind `ES_LAZY_ENTRY` (off = shipped verbatim, crate suite green on the patched tree); a kick-settled Cycle binding at apply takes no catalogue slot (`tube.key = u32::MAX`, which release already ignores), drops its `Arc`, keeps key+clockwise+unit (104 B inline as built: key 56 + sense + unit 40, checker-measured); passages and plunges never demote; reads re-mint by the pure `Orbit::compile` (promotions counted and timed); `same()` compares addresses only Live-to-Live (a demoted side is a memo miss, identical answers). Instrument `examples/lazy_flight.rs` (canonical cut: frame_to to the tick, settle, digest). **Digests bit-identical control-vs-seam on all five arms** — 10⁴ coast/burn, 10⁵ coast (20,000 and 48,000 game-s), held-out seed 7 — and the deep arm reads `2109a2e0…`, the scout's published 10⁵ anchor, with **demotions 273,200 = b9ae's published count**: two independent builds, one event set. Standing memory at 10⁵: bytes/body 1,603 → 930 (−42%), rss 534 → 387 MB (−28%), catalogue_live 100,076 → 28. The wall decomposition: promotions' compiles 12.47 s of the 38.07 s seam wall; minus them, 25.6 s ≈ the control's 24.3 s — the demotion machinery is free, the whole bill is the no-retention re-mints (9.9/demotion here, p50 3.78 µs, p99 13.7, max 220 on this box). As-flown at 10⁹ rtf 100 that is ~130 cores; with the record's retention rule (promote once per demotion, hold to the next kick) it folds into the kick's own compile — the bill is owned by break #1 (the cadence law), not the seam. b9ae's gold condition ("rebuild the seam, commit the diff, re-fly") is met on this record.

**The band seam's ruin is fenced: a byte cap on what held scans pin holds the flight flat at 290-311 MB RSS where shipped climbs ~315 MB/s and dies, digest-identical wherever shipped completes — and at 10⁴ it cuts peak RSS 19× (1,328 → 71 MB) for 607/9,749 frames over (20261015-0358-taleb-d7bc, taleb; restored by checker e0f9 — this page's author had folded it away when resolving the merge conflict).** `ES_SCAN_STANDING` (MiB, default off = shipped verbatim): `Held::standing`, exact `Trajectory::heap_bytes`, one clause in the backlog guard. The guard, not the cure: one scan holding the whole retention is the representation error the cap exposes.

**The smallest promotion between a compact body and a live one is one 4.6 µs compile, and the compiled orbit is not the belt's wall (20261015-0250-scout-760f, scout).** On the ladder scene flown past the first wave (10^5 and 10^4, coast and burn, digests `2109a2e0…`/`f8b52855…`/`44d6a9b5…`), recompiling every standing binding's trajectory from the key it itself carries is **bit-identical for 120,083/120,083 cycles, 0 refusals** — the compiled orbit is a cache (P6), demotion is dropping the Arc, and the promotion bill at 10^9 is **0.16 cores** at the settled belt rate (3.55e-5/game-s; 0.26-0.90 on this window's post-wave rates). But the census kills the record's lever: knots stand at **672 B/body (p99 1,040, max 1,616, none over 2 kB)** — 13.7% of the 4.89 kB/body plateau — so evicting every compiled trajectory buys **1.16x**, not the 75x+ hoped from 5465's inner-system 43-knot doll body; `catalogue_live` = bodies + 48 (no sharing: keys ~unique), so sharing is dead too. The wall is the record stack (184 B unpacked binding + 448 B record + 192 B history + allocator); the priced ladder to 10^9 in ~6 GB is live 4.89 kB -> evicted 4.22 kB -> packed tube record 56 B (56 GB, still 9x over) -> **population programs (0.126-21 bits), the only rung that fits**, with promotion = 17 ns program regeneration (a733) + one 4.6 µs compile per event.

*[Checker 2 (blind, silver): every arm reproduced (regen + own flights); held-out seed 7, a 180,000 game-s cut (3.75x deeper) and N=3×10⁵ (3x the top rung, 1.42 GB rss = 4.86 kB/body, 0 mismatch, compile p50 4.6/p99 9.3 µs) all confirm, and keys are 100.0% distinct at every N tested — no sharing is measured, not inferred. Two corrections: the demoted compact record must also carry the 56 B `OrbitKey`, which lives only inside the dropped `Arc<Entry>` (honest floor 240 B, still under the 300 B shelf bar); and 5465 (memory-h-live) had already proven compiled orbits regenerable bit-identically for the inner-system doll body — new here is the belt domain, the 4.6 µs price and the 13.7% decomposition. Gold needs the flown lazy-Entry variant.]*

**The wave train flown and the dissolution measured (20261015-0128-second-…-4af4-7dc6, second author).** Arm D extends arm C's own flight to cut 700,000 game-s (~117 min of play at rtf 100; 420,062 frames; canonical digest `90348a69…`, reproduced bit-for-bit by the regen rerun): rss 905 -> 913 MB from wave 1 to wave 25 (+0.9%; +0 over the last 599 k game-s; hwm = rss at the end), catalogue 200,076 constant, opens N+637, census one retired binding per body standing.

*[7dc6, predictions pre-registered: 1/3-8 held; prediction 2's "stream median grows with play" clause FIRED as written (median 419 -> 2,034) and is reported failed with its diagnosis — the rise is the bounded shear-fill, not a compounding term; rss/frames/backlog flat through it. Checker 7dc6 (silver): everything reproduces; adversarial beyond the author's domain (2×10⁵ to 1,000 k game-s = 36 waves; 10⁵ to 1,000 k; a third contention sample) all confirm; the floor rise REVERSES past 700 k (peak ~1,471, relaxing to ~1,333 by 950 k).]*

**The in-band ruin's site is counted and the transit is priced: one site, linear in band time (20261014-2248-second-20261014-2130-taleb-625b-c481).** Every minted scan's `candidates` vector is the whole retention — 99,715 bindings × 224 B = 29.4 MB standing per mint (Drop-counted), mints ~2–3 per presented game-second under L8, answered never in flight at 10⁵ and exactly once at 10⁴.

## Refuted

- **"The backlog's count cap bounds the held scans' memory" (the shipped comment's ~10 KB assumption):** in-band one capture is O(N) bodies plus the entries it pins; 118 mints at 10⁵ count-pin 14.8 GB against a 1.5 GB box kill (20261015-0358-taleb-d7bc). A byte cap (`ES_SCAN_STANDING`) bounds it; the count cap does not.
- **"The seam's cost is hidden because the answers never come" (c481's "answered never in flight at 10⁵"):** true only while the process lives; forced to answer under the cap, each answer costs ~0.1-0.5 s at 10⁵ and throttles play 4-28× — the bill exists, ruin was deferring it (20261015-0358-taleb-d7bc).

## Open directions

1. **Adopt the seam with the retention rule** (integrator's call): the record exists (20261015-0724-components-e0f9); default value for `ES_LAZY_ENTRY`, plus "promote once per demotion, keep until the next kick" (an `&mut` re-mint at the resolver's entry, or a per-body live cache) — as-flown no-retention is ~130 cores at 10⁹ rtf 100, retention folds it into the kick's own compile.
2. **The candidate set is the cure, the cap the fence:** one scan holding the whole retention is the representation error the cap exposes; a bounded neighbourhood (the radial window's own certificate, or the phase-neighbour certificate of the co-orbital tier) deletes the answer bill instead of paying it.
3. **Adopt the guard** (integrator's call): default value and unit of `ES_SCAN_STANDING`, and whether `drain_scans` should also answer over-cap.
4. **The passage/plunge tail:** they never demote, so a Passage-heavy scene keeps its compiled arcs standing; unmeasured (1 passage here, digest-neutral).
5. (unmeasured here) The view gather in-band: a per-frame gather crawled the same flight at ~rtf 0.7 with ~2 s/frame somewhere in that path — an accidental finding, unpriced.

## Contradictions

- (unchanged) The stack's lazy-tier gate regression and the frame-cost page's merge conflict are the integrator's to resolve.

## Runs
- 20261015-0724-components-e0f9 (this run): the seam rebuilt, committed and re-flown — five arms digest-identical, 10⁵ = the scout's anchor with 273,200 demotions, standing 1,603→930 B/body, rss −28%; the machinery free, the no-retention re-mints the whole bill.
- 20261015-0358-taleb-d7bc (awaiting grade): the ruin fenced — byte cap on held scans, RSS flat 290-311 MB vs ~315 MB/s climb and death; digest identical at 10⁴; the hidden answer bill measured (4-28× play).
- 20261015-0358-second-20261015-0250-scout-760f-b9ae (awaiting grade): the lazy variant flown — digest bit-identical control-vs-lazy on 4 arms (273,200 demotions, 2.38M promotions at 10^5); standing knots -> 0 MB, b/body 1,603 -> 1,002; the 0.16-0.9-core bill needs retention (8.7-23.2 promotions per demotion as flown).
- 20261015-0250-scout-760f (awaiting grade): promotion = one 4.6 µs compile, bit-identical 120,083/120,083; knots 672 B/body (13.7% of the plateau) — eviction 1.16x, the wall is the record stack; 10^9 lives in programs.
- 20261015-0128-second-20261014-2248-inversion-4af4-7dc6 (awaiting grade): 25 wave periods flat (700 k game-s, digest-stable), dissolution measured (floor rises to the belt-rate equilibrium), 4.2x10^5 at the box ceiling, 4af4's record made to regenerate.
- 20261014-2248-second-20261014-2130-taleb-625b-c481 (second author, awaiting grade): the site is counted — candidates vectors 29.4 MB/mint, drain frozen after one answer; transit linear, ruin band [1.7,3.0] AU.
- 20261014-2248-fermi-b30b (awaiting grade): the steady state through waves measured — memory plateaus 4.85-5.06 kB/body (slope <= 5 B/wave; churn killed 3 orders), rate 3.33-3.50e-5 confirmed end-to-end, train ~27-28 k game-s; memory binds the flyable N at every point.
- 20261014-2248-inversion-4af4 (awaiting grade): the wave train flown — memory a step not a staircase, the train shears, and the digest wobble is the presented-time cut.
- 20261014-2130-second-20261014-2012-system-a669-eb2d: flip-gated rebind wired, default-neutral; the dial's run caps at 4 — 10^2x refuted, mint counted 1.00/kick.
- 20261014-2130-taleb-625b (silver): the player in the belt band: in-band burn = memory ruin (11.2 GB, killed); scan 214-1,087x; coast monster 2 s.
- 20261014-2130-quant-d7e3 (awaiting grade): in-band wave exposure measured — OOM at the cap's arithmetic.
- 20261014-2012-second-20261014-1631-library-7f99-5903: sensors deleted digest-identical (10^3 walk 15x); horizon not belt-scale; chatter 193 -> 0 under refusal at 3.9x events.
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
- 20261014-0000-fermi-3071 (silver): rule 2 dead by decomposition; the tail manufactured.
- 20261013-2252-second-20261013-2130-library-ae3d-7497 (second author): rule 2's falsifier run on four shipped scenes — distribution not heavy-tailed (bulk flat per orbit by construction, head driver-caused); promotion is a fixed fraction; digest-neutral probe.
- 20261013-2252-dynamics-ea91 (awaiting grade): surprise distribution heavy (Gini 0.72–0.74, top decile ≈ half the work), live ranks frozen, churn is death (54–64 % of promotions), steady stream avalanches (Fano 8–28).
- 20261013-2130-library-ae3d (silver): store updates event-cheap with spikes in compaction steps; memory 12.3→48.4 bits/member under storm; five falsifiable ladder rules.
