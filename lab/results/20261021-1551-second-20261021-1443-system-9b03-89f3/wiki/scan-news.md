topic: scan-news
status: open
closed-by:
valid-while: crates/universe@08f5a3eb + 1551's patch (body.rs binding_until, encounter.rs news cache, step.rs dial, examples/scannews2.rs)
updated: 20261021-1551-second-20261021-1443-system-9b03-89f3

# The player's scan: the one comb still walked as if everything changed

## Current best
**The news-fed window is wired and exact [89f3, second author on 9b03]: a kept candidate is proved identical to a full rebuild's through `(event_time, alive, binding_until(j, t))` (every rebind retires and advances `event_time`, step.rs; a death flips `alive`; prune moves the end, rechecked) — 8/8 flights bit-for-bit digest-neutral (30k coast/burn, 3k fallback, D=1/8/64, 20 s horizon), the same-tick duplicates deleted at signature cost (48.6% of burn captures).**
**On the desync dial (`BELT_DESYNC=D`, every ship's kick cadence × D, the player's cadence held) the walk falls with the dial in work units: 30k burn 65.55 → 1.20 → 0.46 → 0.32 re-reads/scan (D=1/8/64, flat 65.55 shipped); coast 163.2 → 3.67; the floor ≈ 0.3–0.6/scan is membership churn (687c's number). The shipped walk is cadence-invariant in implementation only — 9b03's composition, now measured.**
**But capture's µs verdict is arm-split [89f3 + checker]: on the *fenced* arms (30k, 0% fallback) capture is radial-bound (65–80%: the unbounded-list clone + sort in `radial.candidates`) and the read-side signature costs ≈ the read it guards (net +3 to +29 µs/call) — but on the *fallback* arm (3k, 83–90% fallback, the regime od 4's m48 belts read) the walk dominates and the news form is a measured net µs **win**: 162.3 → 101.8 µs/call (−37%, checker-flown), because shipped pays `binding_at`+clone on ~2,250 doll-rejects a scan that a cached Doll-reject signature skips.** The scan row has two terms: walk (kick-coupled, now exact and news-fed) and radial membership (per-scan, C-coupled, the fenced arms' µs owner). A write-side dirty word beside the rec (one generation, bumped at rebind) is the measured condition for the news form to pay in µs at large fenced C.
> Prior art the page carries (checker, 20261021): the overpayment magnitude was already standing on
> `scan-locality` — 687c (churn 0.6/scan, gain K/μ_win = 85× ladder / 16× shipped) and e9a1 (read-set
> deletion 65× burn / 132× coast); 9b03 added the kick-coupling (the 1fd7 correction), the memo's exact
> domain, and the fence's small-N failure. 9b03's baseline: news_frac 0.012 burn / 0.114 coast / 0.070 3k;
> the player's binding changes on 49–51% of scans; the fence fails below 10k (90% fallback at 3k).

## Refuted
- The µs unification at shipped fenced C [89f3]: predicted the newsfed capture µs < shipped on both timed arms (P4); measured the opposite there (radial-bound, signature ≈ read). Scope: on the fallback arm P4's prediction is *true* (−37%, checker) — the refuted premise is the fenced-arm payoff, not the news form's µs payoff outright.

## Open directions
1. **The radial membership query is now the scan's µs owner** (65–80%): the unbounded-list clone + per-scan sort in `radial.candidates` — an incremental/news-fed membership is the next lever for shipped-C µs; unpriced.
2. **Write-side dirty word** (one generation per rec, bumped at rebind): cuts the kept-check to one word; the measured condition for the news walk to pay in µs at large C; wiring only.
3. **Fly the growing-window corner** (the player flying into the belt): the churn floor here is the plane's own orbits; ddeb's per-class cadence floors (16/64/256, not one global D) are wiring on top of the dial, unflown.

## Contradictions
- None open. Noted: od 4 (budget-1e9) reads the fallback on every m48 belt arm; 9b03 finds it scene-fragile with the belt's N (0% fallback at 30k coast, 90% at 3k) — both stand, the fence's domain is the open question. Checker2: the fence is also player-motion-dependent — at 3k *burn* it passes (0% fallback, digest-neutral), so the failure is coast-specific, not small-N-only.

## Runs
- 20261021-1551-second-20261021-1443-system-9b03-89f3 (second): news-fed window wired, 8/8 digest-neutral; walk falls with the kick dial 205× (floor = churn); radial is capture's µs owner at shipped C, sig ≈ read. Checker: exact at N=100k and D=512 (walk flat at the floor 64→512) and on a 30 s burn (471k scans, walk 5.30 → 0.00, memo 49.9%); fallback arm −37% µs.
- 20261021-1443-system-9b03 (system): the scan walk measured for news on three arms — news_frac 0.012–0.114, memo 47% same-tick on burn, radial fence belt-N-fragile; the scan row is information-coupled to the kick dial.
