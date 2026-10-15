# Dossier — 20261015-0250-scout-760f (scout lens)

**Claim.** The smallest promotion between a compact body and a live one is one `Orbit::compile` —
4.6 µs p50 (p99 8.6, max 56), regenerating every one of 120,083 standing bindings bit-identically
across coast and burn — so demote-after-kick is information-free and costs 0.16–0.9 cores at 10⁹;
but the compiled orbit is **not** the belt's memory wall (672 B/body mean, p99 1,040, max 1,616,
zero bodies over 2 kB): evicting every compiled trajectory on the ladder belt buys only ~14% of
the 4.89 kB/body plateau, so the wall between compact and live is the per-body record stack
(184 B unpacked binding + 448 B record + 192 B history + allocator), and 10⁹ still lives in
population programs — now with the promotion price measured.

**Bottleneck.** The board's first question (bodies in the flyable engine: 28→10⁶ against 10⁹),
specifically its named lab item: "the smallest promotion between a compact body and a live one."
Expected gain: turns memory-h-live's open direction #1 ("evictable/shared compiled shapes …
would change: 10⁹ fits with no law change") from a named lever into a measured one — and kills
its compiled-shapes half for the belt. What it lets us delete: the plan to buy the 10⁹ memory
wall with trajectory eviction (this run: 1.16×, not 75×); what it keeps: promotion itself is
cheap enough to wire (0.26 cores at the settled belt rate).

**Evidence** (Linux shared box, 8 vCPU; each command ≤ 60 s; `promote.rs` is this run's patch —
`nladder`'s flight loop + a census at the cut; scene `scenario::plane_extra`, seed 1, rtf 6000,
48,000 game-s, past the first kick wave ~14 k game-s):

```
cargo build --release -p emergent-universe --example promote
target/release/examples/promote 100000 coast 8 6000   # ~30 s
target/release/examples/promote 10000 coast 8 6000    # ~10 s
target/release/examples/promote 10000 burn 8 6000     # ~10 s
```

| arm | bodies | digest | cycles | mismatch | refused | compile µs p50/p99 | knots B/body (p99, max) | compact B | rss end |
|---|---|---|---|---|---|---|---|---|---|
| 10⁵ coast | 100,028 | `2109a2e0…` | 100,028 | **0** | 0 | 4.6 / 8.7 | 672 (1,040, 1,616) | 184 | 489 MB |
| 10⁴ coast | 10,028 | `f8b52855…` | 10,028 | **0** | 0 | 4.6 / 8.6 | 668 (1,040, 1,424) | 184 | 56 MB |
| 10⁴ burn | 10,028 | `44d6a9b5…` | 10,027+1 passage | **0** | 0 | 4.6 / 8.7 | 668 (1,040, 1,424) | 184 | 75 MB |

- **Regenerability:** `Orbit::compile(binding's own key) == the standing trajectory` (shape
  `PartialEq`, knots and crossings) for 100.000% of cycles; 0 refusals. The 10⁵ digest
  `2109a2e0…` reproduced identically across two binary rebuilds (print-only change between
  them). The one burn-arm non-cycle is a Passage (not recompiled; counted).
- **Promotion price:** 4.6 µs p50. Composition at 10⁹: settled belt kick rate 3.55×10⁻⁵
  (cf45, wiki) → 3.55×10⁴ promotions/game-s → **0.16 cores**; this scene's post-wave window
  rates (5.7×10⁻⁵ at 10⁵, 1.97×10⁻⁴ at 10⁴) give 0.26–0.90 cores.
- **What stands:** rss 489 MB / 100,028 bodies = 4.89 kB/body at the cut (the b30b plateau);
  knots are 67 MB of it (**13.7%**). `catalogue_live` = bodies + 48: one standing entry per
  body, no sharing (keys are ~unique on this belt), so sharing is as dead as eviction.
- **The ladder to 10⁹ in ~6 GB, priced:** live 4.89 kB → kill-N 1.2×10⁶ (measured, = b30b's
  8.8×10⁵ at 4 GiB class); drop entries → 4.22 kB (1.16×); the packed tube record 448–454 bits
  (42e6) → 56 GB at 10⁹ — still 9× over; the birth/phase-locked program 0.126–21 bits (98bc,
  2b8e) → fits. **Only the program rung reaches 10⁹**; promotion from program to live is
  17 ns/body regeneration (a733) + one 4.6 µs compile per event.
- **Prior art** (scout lens; mechanism, not adoption): file-backed virtual memory / the OS page
  cache — never store what a pure function of a small key regenerates, evict under pressure,
  pay page-in on touch; our page-in (compile) is 20–2,000× cheaper than a disk fault
  [UNVERIFIED at source this run]. Build-system action caches (Bazel/Buck): recompute beats
  store when outputs are pure functions of keys; thrash is the failure mode, set by read set ×
  recompute cost [UNVERIFIED]. Here the read set is the view's `seen` — 100,046 at the default
  zoom (gather 4.2–4.3 s cold at 10⁵, the known all-bodies gather), bounded in play by the zoom
  (OC#30) and already replaced by row sets on the shipped crossings (view topic).

**Predictions** (`predictions.md`, written before the runs): 1 held (0 mismatches, all arms);
2 held in direction and beat the range (4.6 vs 15–60 µs); **3 FIRED** — knots are 13.7% of the
plateau, not ≥50%: the record's "~43 knots × 88 B" doll body (5465) does not exist on the
ladder belt (max 1.6 kB, ~18 knots); 4 held at the edge (184 vs 80–160 B); 5 held (live set is
seen-bounded; cores 0.26 measured vs 1–2 predicted from the higher compile guess).

**What would make it wrong.** The certificate is bit-identity of the compile at the cut, not a
flown lazy-eviction build: a read path that depends on Entry identity (pointer equality, caches
keyed by `Arc` address), or a Passage/Plunge-heavy scene (flybys were 1 body here), could break
the flown version — the named next experiment is a `Trajectory` lazy variant wired into
`decode`, flown digest-vs-baseline. Timing is Linux/x86 (orders of magnitude only; the
integrator re-measures on the M1). The 10⁹ composition uses cf45's settled rate, not this
window's post-wave rate.

**Cost of adopting.** Small: demotion is dropping an `Arc` after a kick settles; promotion is
the compile the kick already mints (a669: 1.00 compiles/kick — the CPU bill is already paid;
demotion only stops the *standing* copy). The compact record needs the shelf (42e6's 56 B pack)
before 10⁹ is reachable at all. Fit with PRINCIPLES: P6 "Store the generator, not the
generated" — the key is the generator, the compiled orbit the generated; P1 less is more (the
14% answer deletes a planned lever); P22 the simulation decides (the census measured what
stands, not what the record assumed).

**The lens.** Scout looked outside (page caches, action caches) and priced the mechanism; what
it may miss is engine-internal: whether `decode`'s callers can tolerate a lazy Entry without a
law-level review, and whether the inner system (Home/Moon, where 5465's 43-knot bodies live)
has different standing fractions — this census is belt-dominated by construction (99.97% of
bodies). Grade suggestion: silver — real, reproduced, digest-stable, but one build (the flown
lazy variant) from gold.

**Run-to-run wall variance** (shared box): compile p50 4.6–4.8 µs, p99 8.5–9.6, cold gather 4.2–4.3 s at 10^5 across the four process runs in `out/runs.txt` and this transcript; every law counter, digest, knots byte and census count is identical wherever recomputed. The three digests are the regen certificate.
