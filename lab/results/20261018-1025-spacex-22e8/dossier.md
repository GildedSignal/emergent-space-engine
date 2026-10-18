# Dossier — 20261018-1025-spacex-22e8 (spacex lens)

- **Claim:** The live body's memory is priced term by term on shipped code and the compiled
  orbit is a cache with **zero engine readers** in the belt's whole quiet life (0/9,700
  decoded over 2,000 game-s at 10⁴; N-flat 0/99,700 at 10⁵), so the ladder's memory wall
  (1.2–1.65×10⁶ bodies) is two deletable caches — the birth-time compiled orbit (991 B/B,
  67% of the deep birth bytes) and the kick's retired segment (2,625 B/B, unshared, = the
  ladder's whole 2.6→5.1 kB doubling) — at a measured recompile price of 4.7 µs that the
  engine's own read rate makes free until the wave (the kick already pays a compile).
- **Bottleneck:** board #1/#4 — memory per live body in the flyable engine (~2,460 B at
  birth, ~5,100 after the first kick, 4 GiB at ~1.7×10⁶ bodies; the wall every comb arm
  saturates at, nladder's page). Expected gain: ~1.7× the flyable N from the birth cache
  alone (1,469→478 B/B deep on belt bodies), more from the retired segment; deletes the
  "compile at birth for bodies nobody reads" from the build path's 28–31 µs/B.

## Evidence (Linux/x86, load ~1–3, single thread, seed 1; `out/*.log`, `regen.sh`)

Instrument: `work/patch.diff` — print-only census (`binding_at` clones split current/history
+ `decode` knot evaluations, attributed per body via the last body served; flights are
1-thread) plus a byte-anatomy walk (record / plan / knots / entry+Arc / retired history,
deep, Arc-ptr deduped). No behaviour change; digests untouched (counters only). The anatomy
uses public shipped APIs (`rec`, `bindings_of`, `history_len`, `Trajectory::Cycle(o).shape().knots()`),
cross-checked against shipped `bytes_of` (mean 1,196 B/B) and the process footprint
(2,478 B/B at build over n, ladder's class).

1. **The anatomy of a belt body at birth (deep, 10⁴ coast):** total **1,471–1,472 B** =
   record (BodyRec) 464 (32%) + plan 16 + **compiled orbit 991 (67%: knots 672 = 7.3 knots ×
   88 B + Entry 288 + Arc 16)**. Planets/local orbits are the same class (knots 552–673).
   Shipped `bytes_of` undercounts the same body at 1,196 (it omits Entry+Arc and all
   retired-binding deep bytes — see 3); the process-level 2,478 B/B carries ~1,000 B/B more
   in allocator/catalogue/names overhead outside the store.
2. **Read demand, engine phase (before the belt's first kicks at 13,051–14,534 game-s,
   `artifacts/runs/nladder`):** decodes **BELT 0/9,700** (coast 20 s), **0/9,700** (burn L8,
   12 s), **0/700** (N=10³), **0/99,700** (N=10⁵, 10 s) — every engine knot evaluation lands
   on 236–267 distinct bodies (178–204/300 locals, planets, moon, player's near set; 116,462
   decodes over 1,998 game-s at 10⁴ ≈ 58/game-s, O(1) in N). `binding_at` clones every body
   (distinct 10,071–10,076 — the scan's candidate walk, Arc bumps, no knots touched);
   history reads are 4.5% of binding reads (2,846/66,392 coast; 237 burn), 166 distinct.
   The view gather is the only all-bodies reader (10,051 decoded per cold gather, 105,710
   decodes, 418 ms) — the page's instrument, already paying ~30 µs/body.
3. **The kick's doubling is the retired segment, unshared (P4):** kicked locals (204/300 by
   2,000 game-s) hold 2.46 retired segments each: shallow 511 + **deep 2,114 B/B (shared
   0)** = **2,625 B/B** — the ladder's entire 2.6→5.1 kB/B post-kick step, to the number.
   A kicked body totals 3,989 B (2.7× an unkicked one's 1,471).
4. **The recompile price:** `Orbit::compile` from the key = **4,711–4,758 ns** (200 belt
   keys × 5 rounds; matches the shipped mint measurement 3.7–4.7 µs, cbc5/8792).

## The delete this prices (no law change)

Drop the compiled knots after the fit (keep the key: `OrbitKey` + the record's 464+16 B),
recompile at first read. Bits identical (the compile is deterministic from the key —
`recompile ok 1000/1000`, same key ⇒ same orbit). Price at the measured rates: **0 ns of
engine recompile per belt body before the wave** (its reader count is zero), one 4.7 µs
compile inside each kick the kick already pays ~30 µs for; the view gather would pay
4.7 µs/body per cold gather only for bodies it renders (it already pays ~30). Belt bodies:
1,471 → 478 B deep (−67%); the same rule on retired segments (read 4.5% of binding reads)
deletes 2,625 B/B per kick. At 10⁶ that is ~0.99 GB at birth and ~2.6 KB per kicked body —
the 1.7×10⁶ memory wall moves by ~1.7× on the birth term alone, and the compact store
(21–126 B/B) then owns the rest. PRINCIPLES 6 ("store the generator, not the generated")
and 1 ("the cheapest compute is compute not done") — this is the measured instance: the
generated knots of bodies nothing reads.

## Predictions (`predictions.md`, written before the runs)

P1 ✓ (belt decoded 0 at every N and flight); P2 ✓ (history 4.5%/0.1%/4.4% of binding
reads, <5%); P3 **half-miss**: knots alone are 45.6% of deep birth bytes, under the ≥50%
letter — the compiled orbit *including* Entry+Arc is 67%; the deep sum (1,471 B) also sits
at 59% of the process-level 2,478 B/B, outside the ±15% letter (the gap is allocator/
catalogue/names, itemised above); P4 ✓ (2,625 B/B retired, shared 0, kicked 2.7×); P5 ✓
(4.7 µs); held-out arms (burn, N=10³, N=10⁵) ✓ within the stated factors.

## What would make it wrong

The census attributes a decode to the last body `binding_at` served (1-thread flights; a
mis-attribution could hide belt reads inside multi-body call chains — the per-class sums
236–267 distinct vs 0 belt make a hidden belt reader implausible, not impossible). The
zero-reader window is the quiet phase only: at the wave (13,051 gs) every belt body's orbit
is read by its own kick — the claim is not "never read" but "read once, at the event that
pays a compile anyway". A view that must render every body every frame (today's gather)
re-reads all knots; the zoom-level minimap (OC#30) is the view page's own lever. Linux/x86
orders of magnitude; the M1 re-measures.

## Fit with PRINCIPLES

- #6 "Store the generator, not the generated" — the knots are the generated; the key is the
  generator, already stored in the same record.
- #1 "The cheapest compute is compute not done… make compute cheap" — 991 B/B × 10⁶ held
  from birth for a reader that arrives at 13,051 game-s.
- #17 "the best part is no part" — the retired segment's orbit for 95.5% of reads.
- Lens (delete-first, idiot index): memory/body vs the 21–126 B compact-store floor was
  ~10–100×; this run names which bytes are information (the record, 464+16 B) and which are
  dead cache (991 B/B birth + 2,625 B/B per kick).

## The lens (what SpaceX-eyes may have missed)

Delete-and-rebuild is cheap for a rocket; here the same cache is the view's trail and the
ramp's previous binding (4.5% of reads) — the delete must be lazy-with-recompile, not
absent, or the view's partial step loses its past (the ladder's own reason for keeping it).
The census does not measure the wave's read pattern (only the quiet phase before it); a
falsifier is a flight past 13,051 gs with the lazy arm and `ladder_digest`'s 13 cases.

## Reproduce

`sh lab/results/20261018-1025-spacex-22e8/regen.sh` (applies `work/patch.diff`, builds,
runs the four arms; < 15 min total, each arm < 30 s). Logs: `out/coast10k.log`,
`out/burn10k.log`, `out/coast1k.log`, `out/coast100k.log`.
