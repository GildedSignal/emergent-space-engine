# Dossier — 20261017-0739-spacex-4ea0

**Claim:** Compile-on-read is dead in both its forms on the shipped engine — the compiled
table is not a cache awaiting laziness but the engine's own working set (98–224 reads per
build, 99% engine-side, and the mint itself is the first reader of every generation) — so
the kick's 84–87% compile term can only get cheaper (the Carlson wiring), never moved or
deleted by deferral.

**Bottleneck:** the kick (75–160 µs vs a ~6 µs arithmetic floor; the board's worst idiot
index) and, through the same component, the standing 58% of a live body's memory. This run
prices kick-jet's open direction 2 (compile-on-read), the one alternative to the integrator's
named step (direction 1), which the page left unmeasured: "measure the read-side bill it
defers (the view's ramp is the reader, 0e37)".

**Evidence** (Linux/x86, orders of magnitude; `regen.sh` regenerates all of it in ~3 min,
digest-identical to pristine on all four runs):

Census instrument (`work/patch.diff`, +196 lines, print-only): every `OrbitShape` build and
`Passage::compile` counted and timed; every binding decode counted per Entry generation and
attributed to its reader by caller site; mints counted by origin (spec birth vs rebind).

`xtask universe --bench` (engine + view gather + JSON, 1,200 frames = 2,000 game-s, rtf 100):

| arm | generations (spec/rebind) | never-read | reads/rebind-gen | observe | secondaries | step | view |
|---|---|---|---|---|---|---|---|
| 48 members, seed 1 | 1,071 (32/1,039) | **0** | **77.4** | 65.9% | 19.2% | 12.0% | **1.0%** |
| 400 members, seed 1 (held-out) | 8,182 (32/8,150) | **0** | **69.8** | 66.1% | 6.4% | 24.2% | 0.24% |
| 48 members, seed 7 (held-out) | 1,329 (32/1,297) | **0** | **68.1** | 62.1% | 19.1% | 16.0% | 1.0% |

48-member arm detail: 240,114 attributed reads against 2,451 builds (2,394 orbit at 21.7 µs
mean + 57 passage at 368 µs) = **98 reads per build**; 224 reads per generation; p50 of read
generations 53, p99 3,361, max 69,172. The 32 spec-born sources absorb 66.5% of all reads
(4,992 per source generation — every event in their doll re-reads its 3 sources). The
**first reader of every rebind generation is the mint's own birth-read** (1,039/1,039):
`bind_in` decodes the fresh trajectory at the binding event to build the turn and the
residual, so the compile cannot be deferred past the kick even in principle on this
representation. Kick-bench (pure resolver, no view): 30.1 reads/rebind-gen, same structure.

Digest controls: bench digests 5b2d998b…/2713edb5…/01531ed2… and kick-bench replay 56dd012c…
all bit-identical between patched and pristine builds (the first kick-bench draft differed —
the harness hashes `{:?}` of records and my id field leaked into Debug; fixed with a manual
`Debug` that skips the instrument field, then identical).

**What the numbers decide:**
1. **Retention-deferral ("compile at first read") defers nothing:** the first read IS the
   mint, inside the same event (the residual/turn machinery needs a decode at the binding
   event). The rebind's compile share (a765: 84–87%) stays on the kick path.
2. **Eviction (b9ae's knots→0 standing) is CPU-ruin:** every read would first rebuild —
   ×98 builds (240k × 21.7 µs ≈ 5.2 s of build on a 20 s flight vs 73 ms shipped, ×71 on
   the build term). The standing table amortizes one 22 µs build over 98–224 reads
   (0.1–0.2 µs of build per read): it is the engine's working set, not a lazy cache.
3. **The page's premise "the view's ramp is the reader" is refuted on this scene:** the
   view is 1.0% of reads (2,400 = 2/frame); the scheduler's retarded-time reads (observe)
   are 66%, the per-event 3-source rebuild 19%, the step path 12%.
4. **Direction for memory:** deleting standing knots pays the read bill above; the lever
   that does not is sharing (efd4's intern, 513→2 on formations) — consistent with, and now
   motivated by, the read census. The read side itself has two engine-side deletion targets
   now sized: the per-event sources rebuild (19%, read-stream open 1) and observe's
   per-event reads (66%, cadence territory).

**Predictions** (`predictions.md`, written before any census run): P2 correct (never-read
rebinds < 10% → measured 0, all arms); P3 half (mean reads/gen > 20 ✓; "view-dominated" ✗ —
engine-dominated); P4's kill branch fired exactly (p50 53 > 20 with eviction ruin);
P5 correct (orbit builds 97.7% of count; passages 29% of build wall from 2.3% of builds);
**P1 wrong** — I predicted view ≥ 40% of reads, following the page's own guess; measured
1.0%. The miss is the result: the reader is the engine, not the view.

**What would make it wrong:** the census counts decode calls, not knot-panel walks
(space-side counter 476,696 vs attributed 240,114 — engine-internal reads through
`Trajectory::state` outside decode are the difference and only raise the read bill, so the
kill is conservative). A scene where bodies are viewed but never scheduled would re-open the
question; the bench is the player's own loop (engine + view), so none exists here. The
2.29 builds/generation ratio (2,451 builds / 1,071 generations) is un-decomposed — word
re-binding and memo builds are the likely halves; it does not touch the decision (more
builds = stronger kill).

**Cost of adopting:** none — this is a kill, not a build. The integrator's step stays
direction 1 (wire the Carlson compile, ≤2.9 µs verified, ~18× on the compile term), with
the read side's two engine deletions now sized as its companions.

**Fit with PRINCIPLES:** "a fix signals the wrong representation" (19) — laziness was a fix
for a compile that is actually load-bearing; the honest lever is the cheaper build.
"A failed experiment kills that configuration, never the method" (9). Idiot index (the
lens): one build serving 98 reads is a cache earning its keep; the part to delete is the
build's cost, not the table.

**The lens:** SpaceX-delete looks for parts not earning their mass; this census found a part
that is — the blind spot (a deleted certificate may have been catching something) here cuts
the other way: the deletion candidate was the reader's own working set. What the lens may
have missed: the belt at 10⁵–10⁶ (not flyable in this bench's 2 GB window here) may shift
the observe/secondaries split, but not the mint-is-first-reader structural kill.
