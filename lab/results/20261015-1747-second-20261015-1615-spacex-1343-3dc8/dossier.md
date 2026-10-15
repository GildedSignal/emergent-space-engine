# Dossier — 20261015-1747-second-20261015-1615-spacex-1343-3dc8 (second author on spacex-1343)

## Claim

The checker's named gold experiment is done and the claim it gated now holds on the flown
record: **the demote-passages variant of the lazy-entry seam is digest-identical on every
scene** — the standard ladder (10³ coast, 10⁴ coast, 10⁴ burn; cut 20,000 game-s) and the
mixed-peri comet stream (500 comets at peri 1.2 AU, 500 star-grazing at peri 0.006 AU =
1.3 R_star; cut 1,200 game-s), 18 flights, three arms each (`ctl` / `seam` / `variant`),
**zero digest mismatches** — so the never-demote rule is *not* load-bearing for correctness:
passages re-mint bit-identically from `key + outer_radius + sense/unit` (113 B measured) on
the engine's own paths. The bill and the win are both measured: on the comet stream the
variant pays 5.9 promotions per passage demotion at 421–583 µs p50 (92.9 s of compile in the
mixed arm's 132 s wall, 3.4× ctl) and wins 16–19× rss (445→27 MB comet, 542→30 MB
star-grazing, 979→51 MB mixed) — and the ctl arms show the never-demote rule's real cost is
not the 9.7–22.5 MB of standing arcs but **held structures (scans, retired history
segments) pinning every kick-settled unbound body's full compiled arc** (445–979 MB here), which the variant deletes with the arcs.

## Bottleneck

Memory per live body at 10⁹ (the board's first and fourth live questions). 1343 priced the
passage tail and proved re-mint purity at the law level; e0f9 flew the seam but excluded
passages by rule. What was missing — named by the checker — was the seam flight: does the
engine's observable state stay identical when passages demote, and what does the re-mint
cost in flight? Both are now measured, with the corrected star-grazing worst case (w=20,
25.3 kB/arc in the census) in the arithmetic.

## Evidence

All numbers from `regen.sh` (build + `matrix.sh`; `flights/*.txt`, `matrix.log`);
Linux x86 8-vCPU box — orders of magnitude only, per the lab rules. The variant is
`ES_LAZY_PASSAGES=1` on the seam (e0f9's patch verbatim plus: `EntrySlot::Demoted` carries
`outer: Option<Scalar>`, re-mint is the pure `Passage::compile(key, outer)`, `is_cycle()`
reads the record, the demote site also matches `Trajectory::Passage`; ~40 lines).

**Identity (P1, decisive): all six scenes, bit-identical digests, three arms each.**

| scene (cut) | digest (shared by ctl/seam/variant) |
|---|---|
| 1000 coast (20k) | `df0e87cdf72c2b10…a45030c` |
| 10000 coast (20k) | `5e8c9e249f9213ec…5fbab6f` (= e0f9's published ctl) |
| 10000 burn (20k) | `5caeb1b668bbc1d8…64c451` (= e0f9's published ctl) |
| 500 comet, peri 1.2 AU (1.2k) | `3944a7a47190c1ef…ac8f8aa` |
| 500 stargraze, peri 0.006 AU (1.2k) | `98ab8b89294e94f9…a58e485` |
| 1000 mixed (1.2k) | `61c3a24a6f5d7bd8…d8de06` |

`VERDICT: ALL IDENTITY` (regen.log). The seam arms reproduce e0f9's counters exactly
(10⁴ burn: demotions 40,187, promotions 624,994 — e0f9's own numbers), so the merged patch
does not perturb the shipped plane (P2 held; the standard scenes' 349 passage demotions are
the plane's flyby passages, top of the predicted O(10²)).

**The bill (P3 held): per scene, variant vs ctl.**

| scene | passage demotions | passage promotions | ×dem | p50 µs | p99 µs | compile s | wall ctl→var | rss ctl→var |
|---|---|---|---|---|---|---|---|---|
| comet (w 10–14) | 15,363 | 91,456 | 5.96 | 421 | 480 | 38.9 | 17.8→57.4 s | 445→27 MB |
| stargraze (w 16–20) | 15,363 | 91,456 | 5.96 | 583 | 665 | 54.0 | 21.2→75.5 s | 542→30 MB |
| mixed | 30,721 | 182,619 | 5.94 | 576 | 633 | 92.9 | 39.0→132.0 s | 979→51 MB |
| 10³/10⁴ coast (flybys) | 349 | 34,946 | 100 | 311 | 407 | 11.2–11.3 | 4.4–4.8× (seam alone 2.0–2.3×) | 14→13, 62→47 MB |
| 10⁴ burn (flybys) | 1,957 | 44,890 | 22.9 | 313 | 450 | 14.1 | 5.2→23.4 s | 73→54 MB |

The multiplier is the read rate of a demoted binding: an unbound body is always a scan
candidate and is re-read ~6× per demotion on the comet stream; the plane's own flyby
passages (in-doll, near the player's scan) are re-read 23–100× per demotion. p50 sits on
1343's bench curve (421 µs at w≤14, 583 µs at w≤20). The crate suite passes on the merged
tree (20 test binaries, 0 failed, 2 ignored).

**The win (P4, P5 held): what never-demote actually costs.** The ctl censuses hold
518 passages × 18,780 B = 9.73 MB (comet), × 25,329 B = 13.1 MB (stargraze — the corrected
worst case on the run's own curve), 22.5 MB (mixed) standing; the variant's censuses hold
about half that (boundary rebindings — half the stream's rebind events — are not
kick-settled, so the seam's rule leaves them live). But rss is 46–97× the arcs in ctl:
**held structures (scans, retired history segments) pin every kick-settled body's Live arc**, so an unbound population's memory is
~pinned Live bindings × arc size, not arcs. The variant pins 113-B records instead: rss 27–51 MB.
The record: `OrbitKey + outer Scalar + sense + unit` = **113 B** (slot 128 B) against
18.8–25.3 kB standing — 166–224×, the corrected range (1343's 157× was the 1.2-AU class).

## Predictions

`predictions.md` was written before the matrix (P1–P5). **P1 held** (the kill test did not
fire: all 18 flights identical). **P2 held** — e0f9's digests and counters reproduce exactly;
the flyby-passage count (349) sat at the top of the predicted order. **P3 held** — 5.94–5.96×
(in 4–8), p50 421/583 µs (in 300–500/500–900), p99 1.14× p50 (within 1.3); the standard
scenes' 23–100× multiplier is a finding beyond the registered clause, not a miss of it.
**P4 held** — variant rss ≤ 0.012–0.05× ctl (≤ half, easily), ctl arcs 18.78/25.33 kB per
passage on the curve; one refinement: the variant's live passages at the cut are boundary
rebindings, so its standing arcs halve rather than vanish. **P5 held** — 113 B measured.

## What would make it wrong

The identity certificate covers six scenes at one cut each, one seed, and the census is a
sample of the standing set, not exhaustive; a passage whose demote record disagreed with its
live arc would surface as a digest mismatch at the next kick or read on that body, so the
18 identical digests bound the failure tightly, but multi-seed and multi-cut identity is the
checker's to add. The bill was measured on a stream whose kick density is high (27 kicks per
comet per 1,200 game-s); a leisurelier stream pays proportionally less wall and keeps the
memory win. The 100× read multiplier on the plane's own flyby passages means a scene with
many *observed* passages (the player watching a flyby) would re-mint dearer than the comet
stream per demotion — unmeasured. Timing is Linux/x86: orders of magnitude only.

## Cost of adopting

The seam's owner extends the demote match to `Trajectory::Passage` with the record carrying
`outer_radius` (~40 lines, in `work/patch.diff`), replaces `body.rs`'s `Passage(_) => 4096`
with 1343's measured accessor, and decides the wall-vs-memory trade per population: unbound
streams should demote (16–19× rss against 3.4× wall at this kick density), and the seam's
future cap work (`ES_RETAIN_HOT`) prices the re-mint with `lazy_passage_counters` now split
out. No law arithmetic changes; the patch is the seam, the comet plumbing, the census and
the accounting.

## Fit with PRINCIPLES

- P6 "Store the generator, not the generated": the compiled passage is exactly regenerable
  from 113 B — flown, not just proven, now.
- P1/17 "the best part is no part": the Live-arc pinning (445–979 MB) goes with the arcs.
- P12 smoothness: the bill is measured as a distribution (p50/p99 per promotion), and the
  variant's worst frame is the re-mint spike — the allocator question the seam already owns.
- P10 "map how things break, think in extremes": the star-grazing class (peri 1.3 R_star,
  w=20) is the falsifying edge, and it holds.

## The lens

The second-author lens did what the checker named and nothing beyond it: no multi-seed
sweep, no cap interaction (`ES_RETAIN_HOT` × passage promotions), no attempt to demote
boundary rebindings (half the standing arcs remain — the rule extends cleanly but not
exhaustively, and that boundary is the seam's own demote-after-kick rule, not the passage
mechanism). The 23–100× multiplier on observed flyby passages is the number a deployer should
re-measure on the player's own view path.

