# Dossier — 20261006-1436-scout-eab7 (scout lens)

**Claim.** A pair cache with element-space slack — physics-engine broadphase fattening applied to
the Binet certificate — makes encounter-window setup cost track geometric churn instead of kick
epochs: measured **8.0× fewer setups and 6.8× less wall time** on the training belt at secular
kick strength, with a bit-identical encounter set (misses 0, extras 0), and validity checks
(~10 flops per pair per kick) replacing 92%-of-cost numeric window setups.

**Bottleneck.** Board focus item 3 (encounters without work per element change) + the integrator's
6 October note that "the slack skin (12.6×) stays the lever; nothing to build". Setup is paid per
(pair × element change): 2.5–24 µs per candidate pair per element change (r8 v2), 92% of per-kick
evals (components-4643), while real encounters are 10²–10³× rarer (r8 v2: 1.7M pairs vs 427
encounters per 20 orbits). Expected gain: order of magnitude (bounded by churn, not epochs);
deletes the per-kick window setup for dormant pairs *without* the wake-re-pay that killed
deferral (components-4643's kill: deferral wakes re-pay, ceiling 1.1–1.2×).

**The mechanism (prior art, ranked by fit).**
1. **Broadphase fattening / skin width + pair caches** (physics engines; UNVERIFIED at source
   today): expand the certificate's validity region so small input changes don't invalidate it;
   reinsert only on exit. This run's `valid()` + `widen_sec` is that mechanism transplanted from
   position space to Binet element space.
2. **Satellite conjunction screening** (catalog update → tiered filters, per-pair rescreening
   intervals; UNVERIFIED specifics): the same structure at 10⁴–10⁵ objects with collisions as the
   stake; their rescreening interval is exactly a slack sized by expected element drift.
3. **Kinetic data structures** (Basch–Guibas–Hershberger 1999; verified to exist): certificates
   with failure events; the law's sparse order ("jump to the earliest broken certificate",
   law.md) is already KDS-shaped — the skin supplies the missing piece, a *cheap certificate
   failure test* (element drift > slack) instead of assuming every kick breaks every window.
   KDS's churn criterion is the honest measure of this mechanism's cost, used below.
4. Incremental view maintenance / differential dataflow (UNVERIFIED): pull-based dirty flags vs
   push recompute — the killed deferral was push; the skin is pull.

**Evidence.** Driver: `skin/` (standalone crate on `crates/encounters`, untouched). Arms share
belt, kick sequence, candidates, and exact per-pair checks; only setup policy differs. Baseline
recomputes `sections()` for every candidate pair every kick epoch; skin caches them, checks
validity (~20 flops: both bodies' Binet points vs setup snapshot within slack·ε_u, period and
periapsis drift within half the widening), re-setups only on drift, widens cached windows and
check arcs by widen·ρ at setup.

Training (seed 4242, σ_e 0.1, ρ 0.01, n 400, 8 epochs, κ 1e-5, slack 0.5, widen 2.0;
72,660 candidate pairs, 3,879 encounters):

| arm | setups | setup evals | checks | run evals | wall | misses |
|---|---|---|---|---|---|---|
| baseline | 581,280 | 184.5M | 35,114 | 1.59M | 64.0 s | — |
| skin | 72,660 | 23.1M | 64,127 | 3.02M | 9.4 s | 0 (extras 0) |

Setups 8.0× down (= horizon: zero re-setups after epoch 0, all 508,620 validity checks passed).
The widening overhead is 1.8× exact checks and 1.9× run evals — two orders below the setup
saving. Reproduce (each ≤ 75 s, Linux x86, orders of magnitude only):
Held-out (`predictions.md` was written first; n 400, ρ 0.01, 8 epochs, slack 0.5, widen 2.0;
"ratio" = baseline/skin setups; each line's two arms shared belt, kicks, candidates, exact checks):

| Case | Result |
|---|---|
| H1 seed 777, σ_e 0.1, κ 1e-5 | **Held.** 588,776 → 73,597 setups (8.0×), wall 64.3 s → 9.1 s (7.1×), zero re-setups, misses 0, extras 0 (3,826 encounters) |
| H2 seed 313, σ_e 0.2, κ 1e-5 | Rerun (matched σ_e): **held.** 627,496 → 78,437 setups (8.0×), setup evals 326M → 40.8M, wall 126.0 s → 18.5 s (6.8×), zero re-setups, misses 0, extras 0 (4,200 encounters; 414 evals/setup here vs 292 at σ_e 0.1 — the cache is worth more on the costlier belt) |
| C1 κ = 0 | **Held.** per_epoch_setups = [ncand, 0×7], misses 0, extras 0, ratio 8.0. |
| C2 κ 1e-3, widen 0 (negative) | **Design failed.** Validity tripped every epoch (cache_hits 0, full re-setup each epoch): stale windows were never used, so this is not the stale-use test — it degenerated to baseline (misses 0 trivially). The detector's sensitivity to stale-use is instead proven by H3's caught miss. |
| C3 κ 1e-5, slack 1e-9 (negative) | **Held.** Validity failed every epoch (cache_hits 0): setups 581,280 = baseline exactly (ratio 1), misses 0, wall 65.9 s vs 65.6 s (+0.5% for the validity checks) — a useless skin degrades to baseline and costs nothing. |

Predictions scorecard: H1, H2 (rerun), C1, C3 held exactly; H3 failed on both its numbers
(setups 7.05×ncand vs predicted ≤3×ncand; 1 miss vs predicted 0) — the churn regime is both
uneconomical and unsound at slack 0.5/widen 2.0, exactly as the pre-registered kill criteria
anticipated; C2's design failed (validity tripped before stale use). The botched first H2 run
is disclosed above and kept in `scratch/H2botched/`.

Cross-cutting: at κ 1e-5 (secular strength) the skin is sound on three seeds (4242, 777, 313;
plus κ=0) — 0 misses in 11,905 encounters, cache validity held for 1,573,278 of 1,573,278
checks (515,179 + 549,059 + 508,620 + C1's 508,620... at κ=0 counts trivially). The
widening overhead stays ~1.8× exact checks and ~1.9× run evals everywhere, two orders below
the setup saving. One named experiment from gold: size slack/widen from the law's own drift
statistics (orbit-averaged tide plus compiled precession shear — a systematic drift my
random-walk kicks understate) and prove the superset property at the churn boundary where the
slack-0.5/widen-2 pairing missed 1 of 3,771.
    cd lab/results/20261006-1436-scout-eab7/skin && cargo build --release
    cd ../scratch/train  # or any empty dir
    /home/glmlab/lab-target-1/release/skin-falsifier baseline 400 0.1 0.01 1e-5 8 4242 0 0
    /home/glmlab/lab-target-1/release/skin-falsifier skin     400 0.1 0.01 1e-5 8 4242 0.5 2.0

The held-out table and the scorecard above cover predictions.md case by case.

**What would make it wrong.**
- A single miss with widen ≥ 4× slack: the validity envelope is unsound (kill the pairing rule).
- Churn regime: kicks of order the slack (κ ≳ 1e-3 here) re-setup every epoch — the skin
  degenerates to baseline (harmless, measured in C3), but if re-setups *exceed* one per epoch
  the wake-re-pay failure of deferral returns.
- Systematic drift the random-walk kicks understate: GR differential precession rotates (V, W)
  every orbit for nearby-a neighbours — a *shear*, not a walk. The cache lifetime is then set by
  the precession shear (still just a threshold change), but the honest churn rate must be
  measured on the law's own compiled precession before adoption. This falsifier's κ = 1e-3
  case bounds the behaviour, it does not measure that shear.
- The candidate set is frozen at epoch 0 in both arms (kick-driven candidacy flux is second
  order at these κ; unmeasured here).

**Cost of adoption.** Small: a per-pair cache (sections + two element snapshots; in production,
versions against the body's own stored elements — the snapshot is already paid for) and one
threshold per doll (slack, widen in element quanta — integers decide, floats only explored
here). It is scheduling-only: like the allocator, it changes *when* setups happen, never which
exact per-pair check decides an encounter (the found sets are compared, not trusted).

**Fit with PRINCIPLES.** "Compute only surprises" (3): a dormant pair's unchanged window is not a
surprise; "no work for no reason" (14); "the simulation decides, heuristics schedule" (22) — the
skin schedules setups, the exact check decides; "a fix signals the wrong representation" (19) —
deferral's wake-re-pay was the wrong representation (time-deferred), the skin is the right one
(drift-thresholded); "Steal what works, from skin in the game" (26).

**The lens (what scout may have missed).** The literature optimises for its own requirements:
broadphase has 60 Hz deadlines and position-space fattening; conjunction screening has sparse
catalog updates and human analysts. Our regime — every body kicked once per orbit, integer
determinism, churn set by compiled precession — sits between them and was not measured by either.
The κ sweep here is a proxy; the law's own kick statistics (orbit-averaged tide, secular drift)
should replace it before the skin is built into `crates/encounters`.
