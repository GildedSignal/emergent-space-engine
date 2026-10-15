# Predictions (written before the decisive flights)

The rebuild: `EntrySlot::Live/Demoted` (env `ES_LAZY_ENTRY`, default off = shipped verbatim).
A kick-settled Cycle binding (`kick.len > 0` at apply) keeps key+clockwise+unit only; its
catalogue slot is never taken (tube.key = u32::MAX, which `Catalogue::release` already
no-ops). Every read re-mints the entry by the pure `Orbit::compile(key)` (a "promotion").
Passages and plunges never demote; births, handoffs and flushes stay Live until their
first kick.

Cases I have NOT tuned on, and what I expect there (all seed 1 unless said, cut at
20,000 game-s, past the belt's first kick wave at ~13,000–14,500 game-s; the canonical
instrument: `frame_to` limited to the cut tick, `settle(cut)`, then `digest`):

1. **Digest identity, control vs seam, 10^4 coast**: bit-identical. The record's basis
   (760f: 120,083/120,083 cycles regenerate bit-identically from the key) plus b9ae's
   flight. If it breaks, the most likely site is `same()` in encounter.rs (held scans
   keyed by `Arc::ptr_eq` re-mint to fresh addresses): my prediction is memo misses with
   identical answers.
2. **Digest identity, 10^5 coast and 10^4 burn (L8)**: bit-identical. The burn creates a
   Passage (never demoted) and the player's chain; the player's own bindings demote like
   any other body's.
3. **Held-out seed 7, 10^4 coast, 20,000 game-s**: bit-identical (unseen seed).
4. **Counters**: demotions ≈ kicks in the window (order 10^2 at 10^4, 10^5 at 10^5 —
   the wave); promotions per demotion in the 5–25 range (each kick's resolve reads the
   standing entry several times: period, impacts, apex, decode).
5. **Standing memory at 10^5**: `bytes_per_body` (dashboard) falls from ~1.6 kB to
   ~1.0 kB; `catalogue_live` falls from ~bodies to O(10) (passages, births, flushes);
   the knots share of the census (body.rs) reads 0 for demoted bodies. RSS end-of-flight
   falls by roughly 25–35% at 10^5 on this box (Linux, shared; absolute values will not
   match the Mac record).
6. **Wall**: the seam arm runs 1.3–2× slower at 10^5 (no retention: every read pays one
   compile at ~4–9 µs on this box); at 10^4 the delta is lost in build noise.
7. **A passage through the star's doll (the 10^4 burn reaches it at ~15.8 s of wall at
   rtf 100; at rtf 1000 the cut at 20,000 game-s is ~20 s wall, so the player is in the
   star's doll for the last ~4,600 game-s)**: no refusal, digest identical.

Kill criterion (pre-registered): any digest mismatch between control and seam on any
arm kills the rebuild as-flown (b9ae's claim would then NOT stand on my independent
rebuild), and the mismatch site is the deliverable.
