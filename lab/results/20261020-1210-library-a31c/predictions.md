# predictions.md (written before verify_quotes.py / compose.py ran)

Topic: nladder (board #1: bodies 28→10⁶ live vs 10⁹; the page's named open targets:
payload interleave adoption, boundary-comb deletion). Method: composition on
page-cited constants + shipped-code facts + fresh Readwise export. No flight.

## P1 — quote verbatimness (the held-out property)
Each of the 5 lesson quotes below, pasted by hand into verify_quotes.py BEFORE
running it, is a byte-identical substring of at least one highlight in a fresh
Readwise export (4,590 highlights expected). Any failure is named and that lesson
is downgraded to UNVERIFIED and its quote dropped.
  L1 Ries: "by working in larger batches and passing work between departments"
  L2 Hoffmann: "The goal is simply to produce an even coffee bed, and do no more."
  L3 Kahneman: "it is also the ability to find relevant material in memory and to deploy attention when needed"
  L4 FS Power Laws: "Quadrupling our training mileage from 16 to 64 miles is unlikely to double our endurance again"
  L5 Darwin via FS: "to make a memorandum of it without fail and at once"

## P2 — composition (compose.py, page-cited constants only)
Constants: per-item sequential cost 45.9 µs (kick) / 8.6 µs (boundary) [8365,
checker-confirmed 45.6/8.57]; era = 27.9k game-s [8365]; play rtf 400; kick-item
floor ~50 ns (scoreboard: kick 75–160 µs vs 42–55 ns floor).
  P2a: boundary era at 1e9 = 1e9 × 8.6 µs ≈ 2.39 h; kick era = 1e9 × 45.9 µs ≈ 12.75 h
       (page: ~2.4 h / ~12.8 h — agree within rounding).
  P2b: era wall budget at rtf 400 = 27,900/400 ≈ 69.75 s → the kick comb alone is
       ≈ 658× over budget; deleting the boundary comb removes ≈ half the stream's
       events (page: 49.7% burn / 50.7% coast) but buys 0× on the binding term.
  P2c: at the ~50 ns floor the kick comb = 1e9 × 50 ns = 50 s/era ≈ 0.72× budget
       (fits) → the entire remaining 10⁹ era wall is the kick item's µs, nothing else.

## P3 — shipped-code facts (grep-verified in regen.sh)
  P3a: crates/universe/src/step.rs:717 inserts `What::Boundary` at `t + full / 2`
       and :718 the next kick at `t + full` (the comb).
  P3b: kick_clock (step.rs:663–676) already runs the crash checks (star, planets,
       own doll surface) at EVERY kick; it does NOT check the leave edge.
  P3c: boundary_clock (step.rs:725–739) = surface check + leave check + anchor
       stamp; its crash half duplicates the kick's own checks half a period away.
  P3d: the frame digest hashes `rec.anchor` (crates/universe/src/universe.rs:1327)
       → a boundary deletion without moving the anchor changes digests by
       construction; digest identity is an unpassable criterion for this arm.

## P4 — unflown consequence (stated as prediction, not measured here)
At 1e5 the era walls alternate 5.6/1.6 s coast (8365); after a boundary-comb
deletion the boundary eras lose ≈ 105k × 8.6 µs ≈ 0.9 s of items, the kick eras
are untouched — the alternation halves (kick-only), it does not equalize. The
interleave (28k) remains the wall-equalizer; the two arms are complementary,
not alternatives.

## P5 — corpus
Fresh export: 770 books, 4,590 highlights (counts regenerate).

## Kill bars
Any P1 failure → that lesson loses its quote (reported, never silently kept).
P2 disagreeing with the page's 12.8 h / 2.4 h beyond rounding → the page's
constants are wrong; report and stop claiming the composition.
P3 lines absent or moved → re-locate before claiming; if the structure changed,
this run's deletions are void.
