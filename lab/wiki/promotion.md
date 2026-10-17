topic: promotion
status: open
closed-by:
valid-while:
updated: 20261017-0005-second-20261016-2327-library-cbc5-8792

# The compact↔live promotion: what the boundary costs, in bytes and in µs

## Current best
**The standalone mint+demote is now measured on the flown store — 3.7–5.3 µs p50 (mint =
the compile: 3.7–4.7 on seam/retain/100/1000, 5.2–5.6 on the re-mint-storm arm dwell-17
burn 10⁵ — the author's 3.7–4.9 range excluded that worst arm; demote = the Arc drop,
0.04–0.08), across coast and burn, four dwell classes (seam/17/100/1000/∞ game-s) and two
N — so the ledger's CPU half holds with ≥4.4× margin against the 23.1 µs 4-core budget at
10⁹ rtf 100 (composed ÷8+delete = 0.78–0.85 cores; ÷8 alone = 2.0–2.2, so cadence alone
meets the mint budget), and its 44 µs
bind/refit pricing is corrected: the settle hands the promotion an exact key, so the
promotion never refits — b29a's 21 µs `from_state` is the kick's own settle bill, already
inside the kick Ĉ (b063). The memory half is coast-scoped: the dwell dial
(`ES_RETAIN_DWELL`, this run) collapses coast's standing resident 100,819→288–329 at
+1% re-mints, N-independent — but on burn it fails at 10⁹: the read stream (b = 11.48
reads/body/20k gs, N-linear → 5.74×10⁷ reads/s wall at 10⁹ rtf 100) owns burn memory
and CPU — every dwell ≤ 80 game-s sits left of a measured miss cliff (75% at 5, 73% at
17, 72% at 40 and 60, 71% at 80, 14% at 100 — checker flights; the cliff is a band
between 80 and 100, and the re-reads cluster in bursts of tens of gs), so no dwell meets
both 6 GB and ~4 cores
(≥ ~220 re-mint cores at any cliff-left dwell on CPU alone; ~95 GB standing at dwell 100,
N-linear at three N); the burn knee is the
reads, not the demotion count (0619's archive) and not the dial
(20261017-0005-second-…-8792, second author; 24 flights, one frozen binary = 0619's patch
plus print-only timing/dwell/mid90 additions; every arm prints its scene's ctl digest bit
for bit; 1d52's and 0619's anchor counters regenerate exactly: 131,053/763,888/100,788,
130,187). The re-ranking stands, sharpened: diet = 10⁶ lever; ÷8 = the mint-budget lever;
delete = the event-stream lever; burn-10⁹ memory = the read stream's question (new home).**
Prior best retained: the ledger's arithmetic and its P6 correction (below).

## Refuted
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
- **"Dwell is the memory dial at 10⁹"** as stated: coast-true, burn-false — on burn the
  read stream's N-linear rate sets both the standing resident (λ_reads×dwell) and the
  re-mint bill, and the miss cliff (73%→14% between dwell 17 and 100) puts the
  memory-feasible dwell and the re-mint-feasible dwell on opposite sides
  (20261017-0005-…-8792).

## Open directions
1. **The read stream is the burn knee** (this run's transfer of 0619's direction 2): at
   10⁹ rtf 100 it is 5.74×10⁷ reads/s wall (11.5 reads/body/20k gs) — ~6 cores of pure
   hit-path ε (lock+clone) even before misses. What are the resolver's re-reads of
   kicked bodies FOR, and which representation deletes them? (0619 named this; the dial's
   failure mode is now the measured reason.)
2. Cliff position, seed stability and N-linearity are flown (checkers: cliff between 80
and 100 gs with miss 72–75% flat from dwell 5 through 80; seed 2 within 6% and seed 3 at
14.0% on the cliff's right side, digest-identical to its own ctl; reads linear at 2×10⁵
to 0.13%). The coast dial saturates at ~N beyond ~2000 gs (dwell 10000: standing
115,276 ≈ N, re-mints exactly 1.00× retain's — checker2). Remaining: a formation scene
(the burst scale the cliff hangs on) and the sub-frame dwell class (the ledger's
"~1 game-s" certificate-clear), still interpolated, not flown.
3. ES_SECULAR's promotion-skip coverage (1a46) prices the event stream only — its effect
   on the read stream is unmeasured.
4. The stagger's recurrence gate (≥3 intervals, the unprinted second spell,
   9e75-checker2) before idle-time compute-ahead is considered at all.

## Contradictions
Resolved by this run: 0619's burn knee ("WS = demotions, an archive") vs the ledger's
λ×dwell identity — both were measuring different things (0619's retained_now counts the
never-expired archive at dwell=∞; the terminal/wave-passage peak pins ~N at dwell ≥ 100).
Checker correction: the standing resident is NOT λ_reads×dwell at finite dwell either —
it is burst-structured (167 at dwell ≤ 17, a ~6.7k plateau from 40 to 100, 8.2k at 1000
vs 82.9k λ×dwell); the "memory-feasible dwell ≤ 7.5 gs" bound was that model's artifact,
and the no-dwell verdict rests on the measured miss cliff (CPU cliff-left, memory
cliff-right). Standing watch:
the ledger's P6 cell (diet at shipped rate binds memory for dwell ∈ (2,808, 28,141] gs)
is coast-only until the read stream is priced.

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
