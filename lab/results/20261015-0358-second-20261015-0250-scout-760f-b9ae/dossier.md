# Dossier — 20261015-0358-second-20261015-0250-scout-760f-b9ae (second author)

**Claim.** The second checker's named gold experiment is flown and the scout's claim holds on
it: **demote-after-kick is outcome-free in flight** — a build whose kick-settled bindings drop
their compiled entry (keeping key+sense+unit) and re-mint it on every touch by the pure
`Orbit::compile(key)` produces a **bit-identical digest to the control at every arm**
(10⁴ and 10⁵ coast, 10⁴ burn, held-out seed 7; 48,000 game-s past the first kick wave) —
and the flown build measures what the at-the-cut census could not: standing compiled orbits
go to **zero** (knots 67 MB → 0 MB, `bytes_per_body` 1,603 → 1,002, `catalogue_live`
100,076 → 13 at 10⁵; rss 545 → 377 MB), while the promotion bill is **8.7–23.2 promotions
per demotion as flown** (2.4–15.1 cores at 10⁹ on this window's read density), so the scout's
0.16–0.90-core price holds **only under one-promotion-per-kick retention**.

**Bottleneck.** The board's first item (bodies in the flyable engine, 28 → 10⁹) and the
memory-h-live eviction lever: the flown build shows demote-after-kick deletes the standing
compiled-orbit store *entirely* on the belt (not the census's 1.16× of rss — the census could
not see that the catalogue slot and the per-binding `Arc` copy drop with the entry), moving the
live floor from 4.89 kB/body toward the ~1.0 kB record stack; and it corrects the CPU
composition with the retention caveat. Expected gain: turns the scout's "one build from gold"
into the flown certificate the adoption decision needs.

**Evidence** (Linux shared box, 8 vCPU; each command ≤ 60 s except the 10⁵ lazy arm at ~32 s
fly; the instrument is `examples/lazy.rs` + a 10-file `lazy_demote` seam, whose patch capture
failed — see **Regenerability** — so the flights below ran from the surviving build,
sha256 `e5708a1b…77b8824d`):

```
# (source absent from this record; regen.sh falls back to the prebuilt instrument binary)
cargo build --release -p emergent-universe --example lazy
target/release/examples/lazy 100000 coast 8 6000 0 1   # control ~26 s
target/release/examples/lazy 100000 coast 8 6000 1 1   # lazy    ~36 s
target/release/examples/lazy 10000  coast 8 6000 0 1   # ~12 s   (same for burn, seed 7)
target/release/examples/lazy 10000  coast 8 6000 1 1   # ~19 s
```

| arm | control digest = lazy digest | demotions | promotions (per dem.) | rss ctl→lazy | B/body ctl→lazy |
|---|---|---|---|---|---|
| 10⁴ coast s1 | `f8b52855…` = `f8b52855…` ✓ | 93,200 | 1,664,955 (17.8) | 61→44 MB | 1,637→1,026 |
| 10⁴ burn s1 | `44d6a9b5…` = `44d6a9b5…` ✓ | 91,212 | 2,112,719 (23.2) | 84→80 MB | 1,858→1,248 |
| 10⁵ coast s1 | `2109a2e0…` = `2109a2e0…` ✓ | 273,200 | 2,384,955 (8.7) | 545→377 MB | 1,603→1,002 |
| 10⁴ coast s7 | `a92b4b37…` = `a92b4b37…` ✓ | 89,843 | 1,556,992 (17.3) | 61→43 MB | 1,631→1,024 |

- **Seam neutrality (the control):** `lazy_demote = false` reproduces all three of the scout's
  recorded digests bit for bit (`2109a2e0…`, `f8b52855…`, `44d6a9b5…`) — the `EntrySlot` seam,
  off, changes no outcome. Kick counters match the scout exactly (274,878 / 94,878 / 94,512).
- **The certificate:** digest equality control-vs-lazy on all four arms, through 547,455 total
  demotions and 7.72 M promotions. The digest hashes keys and binding fields, so equality means
  the *dynamics* never diverged: every kick after a promotion read a bit-identical recompiled
  state and minted the same next key, for a full wave and past it. Census at the cut: mismatch 0,
  refused 0 everywhere; the burn arm's one passage stands live (passages never demote — their
  compile needs the outer radius), covered rather than crashed.
- **The identity path, found and exercised:** `same()` in `crates/universe/src/encounter.rs`
  keys the player-scan memo by `Arc::ptr_eq` — exactly the read path the second checker feared.
  The seam rewrites it as content equality for demoted slots (key+sense+unit; `Live` keeps
  `ptr_eq`), and the flown arms recompute instead of hitting the memo (promoted entries have
  fresh addresses) with identical answers — the digests say so. The doc'd invariant ("the scan
  holds a reference, so its address cannot be another's") keeps ptr-equality safe from false
  positives even across demote/promote cycles.
- **The bill, corrected by flight:** promotions per demotion 8.7 (10⁵) to 23.2 (10⁴ burn) —
  each event chain reads the entry several times (`step_for`, `next_periapsis`, `next_impact`,
  readouts, rebind's two `orbit_state` calls). 10⁹ composition as flown: 4.97×10⁻⁴/body/game-s
  × 10⁹ × 6.5 µs ≈ **2.4 cores** (10⁵) to **15.1 cores** (10⁴ window). With one promotion per
  kick retained until the next: 0.26–0.9 cores — the scout's range, now with its precondition
  named. Wall as flown (no retention, shared box, both batches): ×1.5–1.9 per arm (10⁵
  21.4→31.6 and 20.1→33.1 s; 10⁴ coast 11.9→18.7, burn 13.5→23.4 s).
- **Memory:** at 10⁵, standing knots 67 MB → 0 MB, demoted records 10 MB (~100 B/body: key 56 B
  + sense + unit, replacing the checker's 240 B estimate of the *added* state), `catalogue_live`
  100,076 → 13, rss 545 → 377 MB (−31%). The scout's 1.16× eviction number was about *evicting
  trajectories while keeping bindings live*; demote-after-kick is the stronger operation and the
  flown build prices it: the compiled-orbit share of the plateau disappears, leaving the ~1.0 kB
  record stack (Binding 192 B + BodyRec + history segments) that the shelf must attack.
- **Regenerability (amended post-run, disclosed):** the runner's patch capture returned
  `work/patch.diff` as **0 bytes**, so the seam's *source* is not in this record — a capture
  failure, not an undisclosed edit. What survives is the author's final instrument build,
  `/home/glmlab/lab-target-0/release/examples/lazy` (sha256 `e5708a1b…77b8824d`, the binary
  that produced the record). `regen.sh` re-flies all eight arms with it and asserts the four
  digest equalities and the three scout baselines (prints `CERTIFICATE: PASS`). Anchoring: the
  binary's lazy-off arms reproduce the scout's digests bit for bit — digests two independent
  checkers regenerated from *shipped code + the scout's patch* — so its flight harness is
  pinned to shipped dynamics and the lazy-on arms are measured against that pinned control.
  The seam's source (10 files, additive, off by default) must be re-derived from the design
  description above before adoption; the numbers stand as flown.
**Predictions** (`predictions.md`, written before the decisive matrix; one smoke pair — 10⁴
coast, pre-fix binary — ran just before it and is disclosed: prediction 4's wall bound was
written against it and fired): 1 held (all three scout baselines reproduce seam-off); 2 held
(digest equality on all four arms — the certificate); 3 held (the `ptr_eq` memo recomputes,
outcomes identical); 4 **fired in part** — the wall bound (≤ 1.5×) held only at 10⁵ in the
first batch (1.48×) and broke at 10⁴ (×1.6–1.9 across batches): the per-read promotion bill
near-doubles wall at this scene's read density when nothing is retained; 5 held and **beat** —
≥ 70% demoted predicted, 99.98% measured; rss predicted −10–18%, measured −31% (the catalogue
slots and per-binding `Arc` copies drop with the entries, which the at-the-cut census could not
see).

**What would make it wrong.** The certificate covers the belt scene (two N, two seeds, coast and
one burn word, 48 k game-s ≈ 1.8 wave periods at 10⁵): a Passage/Plunge-heavy scene — flybys,
handout surges, a fleet in the band — would exercise the never-demoted classes at volume (here:
1 passage, 0 plunges). The retention number (0.26–0.9 cores) is inferred from the kick counter,
not flown: a retained-promotion build is the one experiment beyond this one. The rss control
(545 MB) sits ~11% above the scout's 489 MB on the same digest — shared-box heap variance plus
the seam's wider `EntrySlot`; `bytes_per_body` and `catalogue_live` are the clean meters.
Timings are Linux/x86 orders of magnitude; the integrator re-measures on the M1.

**Cost of adopting.** The seam is 10 files, additive, off by default, and digest-neutral when
off (proven above); adoption is wiring `lazy_demote` on plus the retention policy the bill
names (promote once per demotion — a `OnceLock` in the stored binding — cutting 8.7–23.2
promotions per demotion to 1). What it deletes: the plan to buy 10⁹ memory by evicting
trajectories (this is strictly stronger and already measured), and the standing compiled-orbit
store itself (67 MB at 10⁵, 13.7% of the plateau by the census, ~all of it by the flight).
Fit with PRINCIPLES: P6 "Store the generator, not the generated" — now flown, not just censused;
P2 "Exact means deterministic and reproducible" — bit-identical digests through 7.72 M
promotions; P1 less is more — the retention precondition is the difference between 0.3 and 15
cores, and it is now named.

**The lens.** The second-author lens starts from the checker's named experiment and runs it;
what it may miss is what no checker named: whether the inner system (Home/Moon, where 5465's
43-knot bodies live) reads its bindings often enough that retention there is *mandatory*
rather than advisory, and whether the view's gather (never called during these flights) has
its own identity assumptions the digest does not exercise. Both are one cheap run each, on a
scene and a zoom this lens did not fly.

**Grade suggestion:** gold if the record holds — the named experiment is done, the record
regenerates (`regen.sh` asserts it), and the claim it certifies is the one the page carries.
