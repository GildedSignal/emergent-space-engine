topic: promotion
status: open
closed-by:
valid-while:
updated: 20261017-0739-second-20261017-0552-inversion-604c-2e42

# The compact↔live promotion: what the boundary costs, in bytes and in µs

## Current best
**The formation frame's tail is decomposed per frame, and the fix ranking inverts: the over-budget
frames at fleet scale in-phase are comb-owned (91.7-99.7% item pipeline: kicks, boundaries, fits),
not scan-owned — at K=1,000, 0.6-1.0% scan / 97.7-98.5% comb in the 68 over frames on both seeds
and two passes, the six p99 frames 98.0-98.7% comb, the worst frames the wave frames (`ev=1002`;
comb 43.9-65.4 ms against scan 0.24-0.33; at 3,000+10⁴ the worst is 137.26 ms = 1.47 scan /
134.23 comb, `ev=3002`; at 10⁴, p99 452.8-463.5 ms, 98.4% comb) — so the frame's first fix is the
comb's cadence (de-phase the births; kick-cadence's), and the observer's phase axis is second: the
scan channel rides idle room below 69f3's latch (72-95% of its ns inside under-budget frames
[checker: 95/95 author-regen, 88 seed 3, 72 seed 5 — the placement is seed/load-dependent; the
tail ownership is not], 3-10% of mean frame wall at K ≤ 1,000 (seed 5: 2.9), answers ~3.9-4.4
ms one at a time (seed 5: 4.41), held_max ≤ 54 of 2,048 across five seeds, ≤ 71 at any K),
freezes above
it (zero answers in flight at K ≥ 3,000 — 69f3's `S < b/2` with S ∝ K, the crowd law setting S)
and then pins 51 MB (3,000+10⁴: 71 held × 3,338 × 216 B) to 93 MB (10⁴) [checker2, one decade
beyond: 2×10⁴ pins 43 × 20,039 × 216 B ≈ 186 MB — the pin ∝ K; there the over frames stay 0.7%
scan / 95.1% comb, worst frame ev=20,002, comb 923 ms, hwm 932 MB]. 0552's P5 mechanism is
corrected: SCAN_BACKLOG (2,048) never fires in any flight (held_max ≤ 71); below the latch the
answers drain into quiet frames, above it they stop, not pile into a frame
(20261017-0739-second-20261017-0552-inversion-604c-2e42, per-frame top-level prof channels closed
against wall to 98.4-99.6%, both seeds, coast, rtf 100, regen.sh; seed-1 K=1,000 digest identical
to 0552's). What stands from 0552: both channels' own bills are crowd-proportional, so at 10⁹ the
observer fix alone buys a smooth mean on a ruined frame — the two fixes are ranked, not
alternatives.**


**The observer half's "bounded near set" is measured on the game's own crowd and it is crowd-proportional:
the radial filter bails on 100% of the plane's own coast scans (28 bodies, no formation: 87/87, the window
at coast covers every radius from zero — reach ≈ 9·r from h = 1.1e12 doll units × speed_cap 9.76e-3, and
the bail's numerator counts bin-entries, 1,947 mean against 71 registered, so `hit ≫ bodies/4 + 64` at
plane scale), a fleet formation on the player's circle adds 1.00 candidates a ship (37.7 + 1.00·K:
87.7 at 50, 1,037.9 at 1,000; capture 382 µs and one answer 4.53 ms a scan at K=1,000, 4.4 µs a
candidate), 1,000 ships put the p99 at 52.5 ms (68/600 frames over the 12-ms budget, 23% of game time
lost; beside the comb: 128 events a frame, 9× the spread-10³ class), and 200 ships beside a 10⁴ belt
switch the whole universe's scans back to full walks (78/84 bailed, 9,549 binding_at a scan, 51× the
census's 186) — the filter's on/off decided by other dolls' populations (the belt inflates `self.bodies`,
the bail's denominator), a nonlocal coupling against PRINCIPLES 15 (20261017-0552-inversion-604c,
inversion; coast, rtf 100, seed 1, print-only `radial::scanstat` census bit-stable across reruns,
`prof` stages, regen.sh; at 10⁹ a 10⁶-ship fleet ≈ 0.36 s capture + 4.4 s answer a scan ≈ ~500× over
at rtf 100, and a held scan pins candidates × 216 B).** The census's own numbers reproduce on the same
binary at form=0 (201.1 / 199.5 candidates at 10⁴ / 10⁵, zero bails): the O(1) verdict is a property of
the ladder's population (locals capped at 300, none in the player's band, the belt in another doll), not
of the filter. [20261017-0739: the tier beside a 10⁵ belt is off (0 bails, 387 candidates) — the "200
ships" crossing is population-pair-dependent, as 0552's checker measured.] Fixes to price: the bail's
numerator in bodies (dedup) and its threshold local to the window's population; a phase axis for
co-orbital crowds (taleb-09b5's rank-along-orbit invariant, the encounters gold, applied to the
observer); the comb channel is kick-cadence's.

Provenance (checker): the plane-scale fallback and the `bodies/4 + 64` mechanism are scan-queue's
priors (cdf0 20261016-1120: Home's doll trips the N-relative rule exactly at the plane's flown N,
95% of coast captures; 3999: the belt-band every-N disease) — this run's new content is the
co-orbital formation itself (the page's named unflown direction), the 1.00/ship crowd law, the
coast window covering every radius with a bin-entry numerator, so the bail never turns off under
concentration (100% still at 10⁴ in-band bodies, checker — cdf0's "small-N disease" scoping
corrected), the c439 inversion, and the frame cost. [20261017-0739 adds the per-frame channel
decomposition and the ranking.]

Prior best retained: **the read stream is censused on shipped code and the 10⁹ premise is corrected: the engine's
read demand is O(1) in N on the ladder's flights — every reader's absolute count identical
at N=1e4 and 1e5 (scan candidates 148,996 at both; totals 188,181 vs 188,227) — the player's
scan reads a bounded near set (70.0 candidates a scan at burn, 184 at coast's wider window;
the radial apsidal filter cuts the belt), and the only N-linear reads ride the kick cadence
at 2.9–4.3 reads an event (state_of 0.9–1.6 + root_state_raw 1.4–1.8 + rec 0.6–0.9;
misses 0, history hits ≤4.3%) (20261017-0428-quant-c439, `prof::reads` census behind the
prof feature, digest-identical plain vs prof `d1822b88…`, regen.sh).** So the "~6 cores of
pure hit-path ε (lock+clone)" never materializes as an observer demand: at 10⁹ rtf 100 the
observer reads are ~7.7×10³/s and the event-riding reads between ~4×10³/s and ~10⁷/s
(≤ ~1 core at the measured 67–129 ns a `binding_at`, 192 B; rec 114–167 ns, 464 B) — a
term of the kick bill (kick-cadence's, ladder break 1), not a separate knee. The ~7×10⁶/s
figure is the wave-window per-body extrapolation (checker2: events themselves are O(1) in
N over 20 s windows — 16,212/16,215/16,215 at 1e4/1e5/1e6 — and grow only ~2.4× a decade
through the wave, 65,154→155,092 events 1e4→1e5, so no per-body × 10⁹ term exists on
these flights; checker2's wave arm at 1e5: 4.70 reads an event). 8792's b = 11.48
reads/body/20k gs
reconciles as the kicks' own mint-path reads (~3.9 kicks/body in that window × ~4.3), which
an N-linear counter records when a mint counts as a read. The dwell cliff's hot set is,
as an inference (never flown together: the census runs on main, the cliff on 8792's
retention patch), the scan's near set (~70 bodies read at ~1.1 scans/gs at burn, 88 on
seed 2 — checker; 144 on seed 3 at coast and 70.2 at N=1e6, O(1) a decade up — checker2;
clustered in bursts): a pin of the near set is the proposed deletion
of the cliff's observer half, unflown, and the set's size is realisation-dependent.
Domain: the ladder's
flights (player near Home / the root doll at 1 AU, seed 1, 1 thread); a flight into the
belt at density (radial returns None, the player seam) and the page's per-frame O(N) view
gather are outside it.

Prior best retained: the standalone mint+demote measured on the flown store — 3.7–5.3 µs
p50 (mint = the compile: 3.7–4.7 on seam/retain/100/1000, 5.2–5.6 on the re-mint-storm arm
dwell-17 burn 10⁵; demote = the Arc drop, 0.04–0.08), across coast and burn, four dwell
classes and two N — the ledger's CPU half holds with ≥4.4× margin against the 23.1 µs
4-core budget at 10⁹ rtf 100 (composed ÷8+delete = 0.78–0.85 cores; ÷8 alone = 2.0–2.2, so
cadence alone meets the mint budget), and its 44 µs bind/refit pricing is corrected: the
settle hands the promotion an exact key, so the promotion never refits — b29a's 21 µs
`from_state` is the kick's own settle bill, already inside the kick Ĉ (b063). The memory
half is coast-scoped: the dwell dial (`ES_RETAIN_DWELL`) collapses coast's standing resident
100,819→288–329 at +1% re-mints, N-independent — but on burn it fails at 10⁹ as stated
below (8792; 24 flights, one frozen binary, digests bit for bit; anchors regenerate
exactly: 131,053/763,888/100,788,130,187). The re-ranking stands, sharpened: diet = 10⁶
lever; ÷8 = the mint-budget lever; delete = the event-stream lever; burn-10⁹ memory = the
kick cadence's mint bill plus bytes/body, no separate read-stream term.

## Refuted
- **"The observer half is free / pin the ~70-body near set" (this page's own open direction 1, and
  the census's c439 reading)**: on the game's own crowd the near set is crowd-proportional (1.00
  candidates a ship), the filter bails on 100% of the plane's own scans, and at K=1,000 one answer
  is 4.53 ms — the observer alone is ~500× over at rtf 100 for a 10⁶-ship fleet
  (20261017-0552-inversion-604c). [20261017-0739: the observer's own bill stands, but the frame's
  ruin is not its — the over-budget frames are 98.5% comb on both seeds; see Current best.]
- **"The radial apsidal filter cuts the belt" (c439's letter, as a property of the filter)**: at
  coast the window covers every radius from zero (reach ≈ 9·r); what cuts the belt is the doll
  partition, and the filter's own viability hangs on the belt inflating the bail's denominator —
  at plane scale it bails always (20261017-0552-inversion-604c).
- **"The burn read stream is an N-linear observer demand at 10⁹"** (8792's open direction 1
  as stated, "~6 cores of hit-path ε"): on shipped main the engine's read demand is O(1) in
  N on the ladder's flights — identical absolute counts 1e4↔1e5, 70 candidates a scan — and
  the N-linear reads are the kicks' own (4.3 an event through the wave), i.e. the mint bill
  the cadence owns (20261017-0428-quant-c439).
- **"The smallest promotion is a byte question"** (the board's framing under nladder):
  bytes only buy dwell headroom; the binding terms are dwell (memory) and mint cost
  (CPU) (20261016-2327-library-cbc5).
- **"The record diet moves 10⁹"**: it moves the 10⁶ ladder wall (its 75–615× is real
  there); at 10⁹ the diet only lifts dwell* — CPU is unchanged, and CPU is the bind
  (20261016-2327-library-cbc5).
- **"Mint+demote = 84% of kick cost (44 µs)"** — the ledger's pricing: the promotion on
  the flown store never refits (the settle's key is exact), so mint+demote = compile + Arc
  drop = 3.7–5.3 µs measured; the refit is inside the kick bill, and pricing it again
  on the promotion side double-counts (20261017-0005-…-8792).
- **"Dwell is the memory dial at 10⁹"** as stated: coast-true, burn-false — the miss cliff
  (73%→14% between dwell 17 and 100) is real but its owner is now named: the scan's ~70-body
  near set read in bursts (the observer half) plus the kick mints (the cadence half); with
  the near set pinned, what's left of the cliff is the cadence's
  (20261017-0005-…-8792; c439). [20261017-0552: the "near set pinned" clause is
  crowd-scoped — under a formation the set is K-sized, not 70.]

## Open directions
1. **The scan's representation under concentration** (this run's handback): price (a) the bail made
   local (numerator in bodies — dedup the bin-entries — and threshold against the window's own
   population, not the universe's `bodies/4`), and (b) a phase/along-orbit axis for co-orbital
   crowds (taleb-09b5's invariant on the observer's side), which is the only representation that
   makes fleet scenes cheap for the scan; measure both against this run's matrix (regen.sh). The
   old "pin the near set" is refuted above; the player-seam flight (into the belt at density,
   radial None) stays unflown. [20261017-0739 ranks it: the phase axis is the observer's own bill
   (mean share ~10% at K ≤ 1,000, the pin 51-93 MB above the latch), second to the comb's cadence
   for the frame's tail.]
2. The comb channel of the formation scene (1,000 ships at one period: 128 events a frame, p99
   52.5 ms) is kick-cadence's page, not this one; the formation matrix is the ready instrument.
   [20261017-0739: the comb owns the over-budget frames (91.7-99.7% at K = 200-10⁴, and 95.1% at
   2×10⁴ — checker2) — the cadence fix (de-phased births) is the frame's first; the interaction
   (de-phased waves moving work into the quiet frames where the answers drain) is unmeasured.
   Checker2: rtf 25 does not de-phase the wave — the worst frame still resolves all ev=1002 in
   one frame (comb 54.1 ms) and only the over count drops (68→21), so the de-phasing must come
   from the births'/cadence phase, not from the time knob.]
3. Cliff position, seed stability and N-linearity are flown (checkers: cliff between 80
and 100 gs with miss 72–75% flat from dwell 5 through 80; seed 2 within 6% and seed 3 at
14.0% on the cliff's right side, digest-identical to its own ctl; reads linear at 2×10⁵
to 0.13%). The coast dial saturates at ~N beyond ~2000 gs (dwell 10000: standing
115,276 ≈ N, re-mints exactly 1.00× retain's — checker2). Remaining: the formation scene's
dwell behaviour (the burst scale the cliff hangs on is now measured crowd-proportional, so
the cliff's observer half is a fleet term — unflown together) and the sub-frame dwell class.
4. ES_SECULAR's promotion-skip coverage (1a46) prices the event stream only — its effect
   on the read stream is unmeasured.
5. The stagger's recurrence gate (≥3 intervals, the unprinted second spell,
   9e75-checker2) before idle-time compute-ahead is considered at all.

## Contradictions
Resolved by 8792: 0619's burn knee vs the ledger's λ×dwell identity (different
instruments; the standing resident is burst-structured, not λ×dwell). Reconciled by c439:
8792's b = 11.48 reads/body/20k gs is the mint-path reads riding ~3.9 kicks/body, not
observer re-reads — their N-linearity and the census's O(1) observers measure the same
flight's two halves. Standing watch: the ledger's P6 cell (diet at shipped rate binds
memory for dwell ∈ (2,808, 28,141] gs) is coast-only. New, named: c439's "70 candidates a
scan" and this run's "crowd-proportional, bail always at plane scale" measure the same
filter on different populations — reconciled above (the cap and the belt's denominator), no
live conflict. Resolved by 20261017-0739: 0552's P5 mechanism (a 4.5-ms answer forced into
a frame by SCAN_BACKLOG) against the measurement — SCAN_BACKLOG never fires (held_max ≤ 71
of 2,048); below 69f3's latch the answers drain into quiet frames' idle room, above it they
freeze and pin. The frame's over-budget tail is comb-owned on both seeds.

## Runs
- 20261014-0450-scout-b29a (silver, prior art on nladder, uncited by the ledger):
- 20261015-0250-scout-760f (silver, prior art, uncited): promotion = one 4.6 µs
- 20261015-1926-quant-c4d3 (silver, prior art, uncited): shipped `add_body` promotion
- 20261015-1338-quant-1d52 … 0757, and 20261015-1615-quant-0619 (prior art, uncited):
- 20261016-2327-library-cbc5 (library, this run): promotion ledger — dwell is the memory
- 20261014-0450-scout-b29a (silver, prior art on nladder): the smallest promotion
- 20261015-0250-scout-760f (silver): promotion = one 4.6 µs compile, bit-identical
- 20261015-1926-quant-c4d3 (silver): shipped `add_body` promotion path 9.2 µs p50, flat
- 20261015-1338-quant-1d52 … 0757, and 20261015-1615-quant-0619: demotion/retention built
- 20261016-2327-library-cbc5 (library, silver): promotion ledger — dwell is the memory
- 20261017-0005-second-20261016-2327-library-cbc5-8792 (second author, this run): the
- 20261017-0428-quant-c439 (this run): the read census — read demand O(1) in N (counts
- 20261017-0552-inversion-604c (this run): the formation scene flown — the filter bails on
- 20261017-0739-second-20261017-0552-inversion-604c-2e42 (this run, second author): the
