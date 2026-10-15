# Dossier — 20261015-2041-second-…-taleb-d6ba-57ec (second author on 20261015-1926-taleb-d6ba)

## Claim

The checker's named gold experiment is flown as a depth ladder and it **refutes this run's own
registered wave-hypothesis and confirms the checker's standing-class reading with its
mechanism and price: the comet class does not drain with depth — stargraze 100 at 48k game-s
(1.7 putative settle periods) holds the same 100 Live passages as at 32k, byte-identical
(2,558,720 B, 10,570 panels), 18.1 kB/alive flat — it is one standing arc per live comet
(22.2–25.6 kB), the dense-kick regime's price (comets take 28.2 kicks/ks each, flat with
depth; the settled belt 0.2, which is why the belt's residue drains to 8.6 B/body and the
comet's does not), while shipped ctl on the same scene is linear ruin (2.134 GB pinned,
12.1 MB/body, 83,408 never-freed passages at 32k; the variant 67× lighter at digest parity).
d6ba's adoption sentence is corrected on its three arithmetic defects: the belt's standing arc
floor at 10⁹ is **~87 kB total (pinned_total 86,944 B byte-identical at 10⁴ and 10⁵)**, not
"~9 MB"; the wave pulse is the only N-scaling arc term (≤ 0.71 GB at 10⁹, transient); the
record stack is **1.0–1.3 TB at 10⁹** (not "~1 GB"); the dead price is **2,841 B/death**
(the plane's fixed 30 losses, the same bytes on belt and comet scenes), not "~700 B".

## Bottleneck

Memory per live body at 10⁹ (the board's live question). d6ba closed the belt half of the
seam's residue question; its checker named the missing piece — the ≥ 30k comet census cut —
flew one point (stargraze 100 @ 32k: ~100 Live passages, 49/146 kick-held currents, ~18.2
kB/alive) and read a standing class. One cut cannot distinguish a standing class from the
settle wave mid-drain: the belt's own 20k cut read 656–711 B/body mid-pulse and fell to 8.6 by
48k, and 32k is only ~4k game-s past d6ba's "~28k first settle". This run flies the ladder
(32k/48k stargraze, mixed 50 @ 48k, shipped ctl @ 32k), folds the answer into the adoption
sentence, and re-derives the 10⁹ arithmetic from measured components.

## Evidence

All numbers from `regen.sh` (build + d6ba's frozen patch, unchanged + frozen private binary +
`matrix.sh`), flights in `flights/*.txt`; Linux x86 8-vCPU shared box — orders of magnitude
only, per the lab rules. `work/patch.diff` is d6ba's verbatim (3dc8's seam + demote-passages +
the census instrument); the belt anchors are digest-identical to d6ba's published flights
(48k coast variant `f8b52855…`, every canonical counter equal), so the record regenerates from
shipped code. The comet arms' digests are canonical at the cut; their counter columns are
pacing-bound (rtf=1000 everywhere, as d6ba).
\* mixed counts kicks over both halves' comets (73,703 kicks / 50 / 48 ks → 30.7).
**The regen gaps closed** (rows d6ba's `matrix.sh` missed; all reproduce the values its
checker had to fly solo):

| arm | cut | pinned B/body | bpb_engine |
|---|---|---|---|
| ctl burn (the missing row) | 20k | 1,569.3 | 1,748 |
| var coast (the pulse instant) | 26k | 656.1 | 1,009 |
| var coast (the floor anchor) | 48k | 8.6 (digest = d6ba's) | 1,008 |
| var coast 10⁵ (the N-floor) | 48k | 0.9 (**pinned_total 86,944 B = the 10⁴ flight's, byte-identical**) | 993 |

**The comet depth ladder** (seed 1, variant `ES_LAZY_ENTRY=1 ES_LAZY_PASSAGES=1`; stargraze:
176 census bodies = 100 comets + 76 plane, 146 alive; the 32k arm reproduces the checker's
flight on every published number — 100 Live passages, 49/146 kick-held currents, 15,089.6
B/body, 474 demoted-records/body — and its digest `32ef5b00…` equals ctl's at the same cut):

| arm | cut | Live passages (B) | pinned/alive | kicks/ks/comet | records/body | bpb_engine |
|---|---|---|---|---|---|---|
| stargraze 500 (d6ba, pre-settle) | 4.8k | 506 (12.88 MB) | 23.6 kB | 26.3 | 107 | 38,452 |
| stargraze 100 | 32k | 100 (2,558,720) | 18.19 kB | 28.4 | 474 | 161,340 |
| stargraze 100 | 48k | **100 (2,558,720 — byte-identical)** | **18.12 kB** | 28.2 | **710** | **240,578** |
| mixed 50 (1.2 AU + 0.006 AU) | 48k | 50 (1,109,824; 22.2 kB each) | 12.47 kB | 30.7* | 502 | 170,289 |
| **ctl stargraze 100 (shipped)** | 32k | **83,408 (2.134 GB)** | **14.62 MB** | 28.4 | 0 (never frees) | 163,970 |

\* mixed counts kicks over both halves' comets (73,703 kicks / 50 / 48 ks → 30.7).

**The reading.** At 48k the census holds the *same* 100 passages as at 32k — the same bytes,
the same 10,570 panels, the same current-binding split (49 kick-held Live of 146 alive) —
while everything else moved exactly as depth demands: kicks 90,806 → 135,485 (28.2–28.4
kicks/ks/comet, flat), mints = demotions 90,560 → 135,125, demoted-records 83,458 → 124,977
(474 → 710/body), bpb_engine 161 → 241 kB. Every comet holds exactly one Live passage at
every cut past birth (kick-minted-live = 100 = the comet count; the 12 extra kick-minted
cycle arcs at 32k are plane-body transients, gone by 48k; nokick-mints 3 arcs / 1,720 B, flat
— the boundary-rebind class stays empty on comets too). The class census at every comet cut:
plunges 0, dead 30 holding 85,224 B (the belt's byte-identical dead total — the 30 deaths are
the plane's fixed population, not comet losses: no comet is lost by 48k, `lost 30` at every
cut), `kickless = 0`. So the comet residue is not the belt's wave one period later: it is the
steady state of a continuously-kicked body — one pending mint per body — and it drains only
when the body leaves the dense-kick regime or dies. The belt collapses to 8.6 B/body because
its bodies sit at 0.196 kicks/ks (94,518 kicks / 10,076 bodies / 48 ks): between two belt
kicks a body's mint settles and nothing re-mints it, so at any cut only ~3 per 10⁴ hold an arc.

**The shipped-ctl comet contrast (the ruin the seam deletes):** ctl mints 90,560 kick-mints
by 32k and frees none — 83,408 Live passages stand at 2.134 GB pinned (12.1 MB/body, rss
2,816 MB), and the mint rate is flat in depth, so ctl's comet store grows linearly forever
(~2.1 GB per 100 comets per 32k game-s). The variant holds 2.66 MB at the same cut (rss 42 MB,
67×) with the identical digest.

**The corrected 10⁹ arithmetic (belt, variant, from measured components):**
- standing arc floor: 86,944 B **total** (dead 85,224 + nokick 1,720), byte-identical at 10⁴
  and 10⁵ → **~0.09 MB at 10⁹** (d6ba's "~9 MB" was 10⁵ over: it scaled a per-body reading
  that is actually an N-constant total);
- wave pulse (the only N-scaling arc term): ≤ 711 B/body at the instant (20k–26k readings),
  pruned within the keep window → **≤ 0.71 GB at 10⁹**, transient;
- record stack: bpb_engine 993–1,317 B/body across arms → **1.0–1.3 TB at 10⁹** (d6ba wrote
  "~1 GB": 10³ under) — the belt's memory term, as 760f said;
- dead: **2,841 B/death** over the plane's 30 fixed losses (d6ba's "~700 B" priced the median
  arc; the mean is dominated by 3 deep-window passages ~27 kB each), N-constant on every
  scene flown;
- comets: a **standing 22.2–25.6 kB per live dense-kicked comet** (one passage each, flat in
  depth) — 22–26 GB per 10⁶ live comets; plus the record stack at 710 records/body (48k) and
  the promotion bill (6.6 passage promotes per demotion at 609 µs p50, ~838k promotes by 48k
  on 100 comets) — the comet scene's own compute term, f55d's law holding there too.

## Predictions

Pre-registered in `predictions.md` after the 4.8k/32k anchors, before the 48k/mixed/ctl arms
flew. **P1 FAILED — and its kill clause fired**: registered "48k < ~8 kB/alive, the wave
drains"; measured 18.12 kB/alive with the byte-identical store — the standing-class kill
("96k ≥ ~12 kB") is confirmed at 48k without waiting for 96k. **P4 FAILED as registered**
(predicted mixed ≤ 1/3 of pre-settle; measured 9,498 B/body = 45% of 21,056): the
current-binding half did drain (523 Live currents at 1.2k → 26 at 48k) but one arc per comet
stands, exactly as P1's failure predicts. **P2, P3, P5, P6 held**: nokick 3 arcs / 1,720 B
flat at both cuts; demoted-records grow monotonically (474 → 710/body) while pinned stands;
dead 2,841 B/death, inside the 1–4 kB band, on both scenes; plunges mint 0 at every cut. Two
protocol notes, disclosed: the registered mixed arm was "mixed 1000 @ 48k" (its CPU cost,
~20 min solo at the measured churn, exceeded the window — the flown arm is mixed 50 @ 48k,
same class mix, per-body question unchanged); and a 96k probe flight completed at 755 s wall
but its output file was deleted by this author's own premature cleanup — it was re-flown and
is reported in `run-log.txt` only (its solo CPU cost exceeds what `regen.sh`'s 15-minute
budget carries alongside the ladder, so its numbers stay out of this dossier).

## What would make it wrong

The ladder ends at 48k (3.4 settle-periods' worth of kicks; the 96k exit probe is logged but
not load-bearing): a drain that turns on only past 48k cannot be excluded, only bounded — any
standing comet class is ≤ ~25.6 kB per live comet while the flight lives, and the mechanism
(kick density 143× the belt's, mints = demotions at every cut) has no depth-dependent term in
it. The standing-class reading extends only to bodies in dense-kick regimes; a comet past the
root loss radius, or a scene whose comets settle into sparse-kick orbits, should drain like
the belt — that exit (96k, or a bound-orbit comet scene) is the unwon half. The mixed arm
flew at N=50, not the registered 10³. The 10⁹ arithmetic extrapolates the measured
N-constant components along N only (both N flown share the plane's fixed 30-death population;
a scene whose deaths scale with N would make the dead term ∝ deaths × 2.84 kB). Plunges mint
zero on every scene flown; a plunge-minting scene still reopens that class at
`Plunge::retained_bytes()`.

## Cost of adopting, and fit with PRINCIPLES

Nothing new to adopt: the patch is d6ba's, unchanged; the belt anchors are digest-identical.
What changes is the adoption **sentence**: the seam's belt floor is ~87 kB total (N-constant)
plus a ≤ 0.7 kB/body wave transient; its comet term is a standing one-arc-per-live-comet
class (22–26 kB) for as long as the comet is kicked — priced, not drainable, and 67× under
shipped ctl which is linear ruin (2.1 GB per 100 comets per 32k game-s); the record stack
(1.0–1.3 kB/body belt, 710 records/body comet at 48k) is the depth-growing memory term on
both scenes. `ES_LAZY_ALL` (8b89, same window) supersedes the variant for adoption by
demoting at birth; this ladder prices what ALL must delete on comets (the standing class plus
the transient) and shows the delete is not free of the record stack, which no seam touches.
Fit: "Store the generator, not the generated" (the belt's generated arcs are the generator's
transient; the comet's are its steady-state invoice while kicked) and "Errors never compound"
(no monotone arc term in any variant arm flown; ctl's linear retention is the counter-example
that justifies the seam).

## The lens

The second-author lens registered the cheapest falsifier of the checker's single-cut reading
and was falsified by it — the useful direction: the mechanism (kick density, not scene) is
now measured, and it predicts where else the standing class lives (any burn, any fleet in a
dense-kick regime holds ~1 arc/body; d6ba's burn arms read 8.6 B/body only because the burn's
dense phase is a pulse). What the lens may have missed: the 96k exit is logged, not
canonized; one seed, one comet geometry per class; and the promotion bill on comets (6.6×dem
at 609 µs) is priced here only as a rate — f55d's cap arithmetic on a comet stream is unwon.
