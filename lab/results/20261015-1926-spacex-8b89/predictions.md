# Predictions — 20261015-1926-spacex-8b89 (written before the decisive matrix)

The variant under test: `ES_LAZY_ALL=1` (with `ES_LAZY_ENTRY=1`) — the seam's demote-set
class list dies; **every** keyed entry demotes, at birth and at every settle (kick or not),
not only kick-settled cycles and flagged passages. The record is unchanged: key (+ `outer`
for passages) + sense + unit. Bases: e0f9's seam, 3dc8's demote-passages (both digest-proven
on their classes). Not tuned on: births, no-kick rebinds, the dive class, the pre-wave cut.

- **P1 (the kill test): digest identity.** `all` = `ctl` = `seam`/`variant` on every scene:
  10³ coast, 10⁴ coast, 10⁴ burn (cut 20,000 game-s), mixed-peri comet (cut 1,200), dive
  (cut 1,200). Expected: identity everywhere — the record's fields are exactly what
  `Orbit::compile`/`Passage::compile` are pure in, and no new read path exists. A mismatch
  names the read that needs more than the generator (PRINCIPLES 6 fails for that class).
- **P2 (the deletion): standing arcs → the centres.** Census on `all`: standing compiled
  bytes ≈ 0 on every scene (only the ~3-15 doll-centre/structural Live cycles remain;
  10³ coast smoke: 3 cycles, 1,720 B standing). On mixed I expect ctl ≈ 22.5 MB standing
  (3dc8's number), variant ≈ half, all ≈ < 0.2 MB; rss mixed 979 (ctl) → ~51 (variant)
  → **≤ ~35 MB** (`all`), because held scans/retired segments now pin records, never arcs.
  At 10⁴ coast pre-wave (cut 10,000, before the belt's first kick wave at ~13,051): ctl
  census cycles ≈ N (the belt's birth arcs, ~670 B each); `all` ≈ 3 cycles standing;
  bytes_per_body ctl ~2.6 kB → `all` ~1.0–1.2 kB.
- **P3 (the bill): the promotion stream is the read stream, unchanged in kind.** On the
  standard scenes `all` pays more than `seam` (births demote; a scan read of a never-kicked
  body now mints): at 10⁴ burn I expect promotions ~1–3 M (vs seam's 625k), p50 compile
  ~4 µs (cycle) / ~300–600 µs (passage); wall ≤ 6× ctl (3dc8's variant was 4.5× with no
  retention cache; the cache is not in this build). On mixed, `all` ≈ variant's bill
  (182,619 promotions) ± 30% — same reads, records instead of arcs.
- **P4 (the dive prices the tail, and no Plunge is minted by a state birth).** Dives at
  peri 0.001 AU (inside the star) bind as **passages** (smoke: w up to 23, ~27 kB/arc —
  1343's curve), not Plunge trajectories; zero `plunges` in every census. The dive bodies
  die at the surface: `dead` grows with the cut (19/200 at 1.2k); at cut 6,000 I expect
  dead ≥ 100 and the standing dive arcs correspondingly gone — **the inside-the-star class
  is self-deleting at impact; the un-kickable Plunge trajectory class stays unmeasured by
  any state-birth scene** (no scene mints it), so the never-demote rule survives for it on
  an untested class, not on a flown cost.
- **P5 (what the deletion buys at scale, read off the census):** `catalogue_live` ≈ the
  structural centres on `all` at every N (10³ smoke: 3), against ~N on ctl — the catalogue
  churn channel (cae7/e4cc's one-entry-per-ship leak) is gone at birth, not after the first
  kick.

Kill criteria: any digest mismatch kills `ES_LAZY_ALL` as flown (P1); a promotions/demotions
ratio > 100× on any standard scene, or wall > 10× ctl, kills the "bill is the read stream"
reading (P3) and the variant needs retention before adoption.
