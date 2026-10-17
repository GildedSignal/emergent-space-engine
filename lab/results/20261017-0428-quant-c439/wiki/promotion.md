topic: promotion
status: open
closed-by:
valid-while:
updated: 20261017-0428-quant-c439

# The compact↔live promotion: what the boundary costs, in bytes and in µs

## Current best
**The read stream is censused on shipped code and the 10⁹ premise is corrected: the engine's
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
  the near set pinned, what is left of the cliff is the cadence's
  (20261017-0005-…-8792; c439).

## Open directions
1. **The read stream question is closed on main and handed back:** the observer half is a
   ~70-body pin (build it: keep the scan's near set live across dwell); the N-linear half
   is the kick cadence's mint bill (kick-cadence's page, ladder break 1) — no store
   representation deletes it. What 0619 named ("what are the resolver's re-reads FOR") is
   answered: they are the kicks' own reads of sources, self and record (2.9–4.3 an event).
2. Cliff position, seed stability and N-linearity are flown (checkers: cliff between 80
and 100 gs with miss 72–75% flat from dwell 5 through 80; seed 2 within 6% and seed 3 at
14.0% on the cliff's right side, digest-identical to its own ctl; reads linear at 2×10⁵
to 0.13%). The coast dial saturates at ~N beyond ~2000 gs (dwell 10000: standing
115,276 ≈ N, re-mints exactly 1.00× retain's — checker2). Remaining: a formation scene
(the burst scale the cliff hangs on — c439's near set is the ladder's spread belt; a
co-orbital formation swells it) and the sub-frame dwell class.
3. ES_SECULAR's promotion-skip coverage (1a46) prices the event stream only — its effect
   on the read stream is unmeasured.
4. The stagger's recurrence gate (≥3 intervals, the unprinted second spell,
   9e75-checker2) before idle-time compute-ahead is considered at all.

## Contradictions
Resolved by 8792: 0619's burn knee vs the ledger's λ×dwell identity (different
instruments; the standing resident is burst-structured, not λ×dwell). Reconciled by c439:
8792's b = 11.48 reads/body/20k gs is the mint-path reads riding ~3.9 kicks/body, not
observer re-reads — their N-linearity and the census's O(1) observers measure the same
flight's two halves. Standing watch: the ledger's P6 cell (diet at shipped rate binds
memory for dwell ∈ (2,808, 28,141] gs) is coast-only.

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
  identical 1e4↔1e5, 70 reads a scan), N-linear reads ride the kicks (4.3 an event); the
  10⁹ read-stream premise corrected, the cliff's hot set named (~70 bodies).
