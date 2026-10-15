# Dossier — 20261015-0724-components-e0f9 (components lens)

**Claim.** The lazy-Entry seam is rebuilt from the record's design description, committed as a
patch, and re-flown: demote-after-kick is outcome-free — the digest is bit-identical to the
shipped control on five arms including the held-out seed and three wave periods, and the 10⁵
digest lands exactly on the scout's published anchor `2109a2e0…` with demotions = 273,200,
the record's own count — so the standing compiled-orbit store (floor 0 B: the key rides in the
record) is deleted at run time: standing bytes/body 1,603 → 930 (−42%), rss 534 → 387 MB
(−28%) at 10⁵, for ~0 seam bookkeeping (the whole wall delta is the no-retention re-mints).

## Bottleneck

The board's first gap (bodies in the flyable engine, 10⁶ → 10⁹) binds on standing memory per
body: the plateau after the first kick wave is 4.85–5.06 kB/body (b30b, 4af4, 7dc6). The
scout (760f) priced the promotion (one 4.6 µs compile, bit-identical 120,083/120,033) and the
second author (b9ae) flew the seam — but the checker found the patch was never committed
("the seam and instrument source exist nowhere… rebuild the seam, commit the diff, re-fly —
that one build is gold"). This run is that build. The lens's component: the **standing
compiled-orbit store** — requirement owner PRINCIPLES 6 ("Store the generator, not the
generated"; the compiled cycle is a cache of the exact `OrbitKey`) and 3 ("Compute only
surprises"; nothing derived is stored); its floor is **0 B** (the record must carry the key,
sense and unit — ~64 B inline in `EntrySlot::Demoted` — but no knots, no slot, no `Arc`);
the shipped standing cost is 672 B/body of knots (13.7% of the plateau, 760f) plus a
catalogue slot and an `Arc` per binding. Idiot index of the cache share: unbounded (floor 0).

## The build (work/patch.diff, 15 files, ~200 changed lines)

- `EntrySlot { Live(Arc<Entry>) | Demoted { key, clockwise, unit } }` replaces
  `Binding.entry: Arc<Entry>`; all constructors build `Live` (shipped verbatim).
- At apply, a kick-settled Cycle binding (`kick.len > 0`, `new_entry` present) demotes when
  `ES_LAZY_ENTRY=1` (off = shipped): it takes no catalogue slot (`tube.key = u32::MAX`, an id
  `Catalogue::release` already ignores, so retire/prune stay no-ops), drops the `Arc`, and
  keeps key+clockwise+unit. Passages and plunges never demote; births, handoffs and flushes
  stay Live until their first kick.
- Every read re-mints the entry by the pure `Orbit::compile(key)` (a "promotion": counted,
  timed); `same()` in encounter.rs compares addresses only between two Live slots (a demoted
  side is a memo miss, same answers — the digest carries this).
- The digest reads the key from the slot without minting (values identical by construction).
- Instrument: `examples/lazy_flight.rs` — the canonical cut (`frame_to` limited to the cut
  tick, `settle(cut)`, digest) plus counters, dashboard bytes/body, `catalogue_live`, RSS/HWM.

## Evidence (all from this box: 8 vCPU x86, load 3.4, mem 15 GB; Linux, so wall is
order-of-magnitude only; digests and counters are deterministic)

Five arms, control (`ES_LAZY_ENTRY` unset) vs seam, same binary:

| arm (N, flight, cut game-s, seed) | digest (both arms) | ctl bytes/body, cat_live, rss | lazy bytes/body, cat_live, rss | demotions, promotions (ratio), compile p50/p99 µs | wall ctl → lazy |
|---|---|---|---|---|---|
| 10⁴ coast 20,000 s1 | `5e8c9e24…` identical | 1,632 / 10,076 / 60 MB | 951 / 31 / 46 MB | 41,053 / 804,941 (19.6) 3.69 / 62 | 4.7 → 9.4 s |
| 10⁴ burn 20,000 s1 | `5caeb1b6…` identical | 1,678 / 10,076 / 70 MB | 997 / 32 / 59 MB | 40,187 / 624,994 (15.6) 3.85 / 67 | 5.2 → 9.7 s |
| 10⁵ coast 20,000 s1 | `a287f479…` identical | 1,603 / 100,076 / 533 MB | 930 / 31 / 379 MB | 131,053 / 894,941 (6.8) 3.72 / 59 | 13.3 → 18.7 s |
| **10⁵ coast 48,000 s1** | **`2109a2e0…` identical = the scout's published anchor** | 1,603 / 100,076 / 534 MB | 930 / 28 / 387 MB (−28%) | **273,200** / 2,709,722 (9.9) 3.78 / 13.7 | 24.3 → 38.1 s |
| 10⁴ coast 20,000 s7 (held-out) | `bc8b489a…` identical | 1,626 / 10,073 / 59 MB | 947 / 23 / 45 MB | 39,459 / 754,881 (19.1) 3.67 / 51 | 4.6 → 9.1 s |

Smoke at 10³ coast (`df0e87cd…` identical) and the full outputs: `flights/`. Regenerate
everything: `regen.sh` (~5 min). The 10⁵/48k arm is three wave periods deep; kicks, opens,
boundaries, handoffs, lost, refused, contacts are equal in every pair, and the demotion count
(273,200) equals b9ae's published count exactly, on an instrument rebuilt from the wiki's
design description — two independent builds, one event set.

The wall decomposition: at 10⁵/48k the promotions' compiles total 12.47 s of the 38.07 s
seam wall; 38.07 − 12.47 = 25.6 s ≈ the control's 24.3 s — **the demotion machinery itself
is free; the entire bill is the no-retention re-mints** (9.9 per demotion here, p50 3.78 µs
on this box; p99 13.7 µs at 48k, max 220 µs — the e-tail of the compile, as the record
prices).

## Predictions (predictions.md, written before the flights)

All seven held: identity on every arm including the held-out seed (1–3, 7); demotions ≈ the
kicks (4; 273,200 vs 274,878 kicks); bytes/body ~1.6 kB → ~1.0 kB, catalogue_live → O(10),
RSS −28–29% at 10⁵ (5; measured 930 and 31/28, inside the predicted bands); wall ×1.4–2.0
(6; ×1.41–2.00); the burn's passage never demoted, zero refusals (7). Prediction 4's
promotions-per-demotion band (5–25) held at 10⁴/10⁵ (6.8–19.6) and was exceeded only in the
10³ smoke (32.4), which is outside the band's domain (the locals' short periods dominate
there).

## What would make it wrong

- The digest instrument is the canonical cut, but at rtf 1000 with unlimited budget; a
  budget-limited or 4-thread flight could in principle expose a seam-order dependence the
  digest does not see (40c0's schedule-independence result makes this unlikely; the crate's
  schedule tests pass on the patched tree).
- Passages/plunges never demote, so a Passage-heavy scene (deep flybys, the root-doll band)
  keeps its compiled arcs standing — the memory deletion there is unmeasured (1 passage in
  the burn arm; it stayed live, digest identical).
- The composition to 10⁹ assumes the settled belt kick rate (3.55×10⁻⁵/body/game-s) and this
  box's compile p50; the M1 re-measures.
- `Orbit::compile`'s purity is the load-bearing premise, already certified by the scout
  (120,083/120,083) and now again by five digests; a refused key would surface as a digest
  break or a refusal count, and none appeared (refused 0 everywhere).

## Cost of adopting, and fit

~200 lines, one enum and accessor; default-off is shipped verbatim (the crate suite passes on
the patched tree). Adoption needs the retention rule the record names ("promote once per
demotion, keep until the next kick"): as flown (no retention) the promotion bill at 10⁹,
rtf 100 is ~130 cores at the settled rate (9.9 × 3.78 µs × 3.55×10⁻⁵ × 10⁹ × 100); with
retention it folds into the kick's own compile (the shipped engine already recompiles once
per kick; the seam then costs ≤1 extra compile per kick and deletes the standing store).
That bill is owned by the ladder's break #1 (the cadence law), not by this seam. PRINCIPLES:
"Store the generator, not the generated" — this makes the shipped code obey it on the
standing path; "Exact means deterministic and reproducible" — bit-identical through three
wave periods.

## The lens

The components lens measures one component against its floor; the blind spot is the
neighbour: this deletion moves the compile from bind-time (once, amortised) to read-time
(as-flown, 9.9×) — the neighbour's bill is measured here (the wall decomposition above), and
the fix (retention) is named but not built; a run that adopts the seam without retention
would trade a memory wall for a CPU wall at 10⁹.
