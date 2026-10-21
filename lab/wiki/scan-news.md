topic: scan-news
status: open
closed-by:
<<<<<<< main
valid-while: crates/universe@08f5a3eb + 1551's patch (body.rs binding_until, encounter.rs news cache, step.rs dial, examples/scannews2.rs)
updated: 20261021-1551-second-20261021-1443-system-9b03-89f3
=======
valid-while: crates/universe@00696555 + 20261021-1551's patch (scanpre example, stat module, per-row/reg epochs; no law change)
updated: 20261021-1551-spacex-eb24
>>>>>>> 20261021-1551-spacex-eb24

# The player's scan: the one comb still walked as if everything changed

## Current best
<<<<<<< main
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
=======

**NEW (eb24, spacex — od 1 executed; od 3 executed and refuted as a certificate).** The walk's price
per arm (instrument `scanpre`, clock bias 36.2 ns/call): 3e3 coast fallback — loop 90% of ~280 µs/capture
(build 43%); 3e4 coast fences — **radial 73%**, loop 26%; 1e5 burn rtf100 — radial 52%/loop 48%; 1e5
burn rtf2000 — loop 1.155 ms (fallback near = 100,076, the wave-era bail). Overpayment in time:
memo-discarded walk **37%** of walk time at rtf100, **60%** (2.43 s of 4.0 s) at rtf2000. **Od 3 is
dead as any mutation-counting certificate** — three exact forms, 0 hits each, digest-identical
(c1e220b4… across off/v1/v2/v3): global epoch (dead by construction: every capture follows the
player's own `apply`, which puts the row — universe.rs:761→772; checker-verified); per-row+reg
epochs — miss_me **861/861** (same call site); `me` by value + epochs — miss_near 723, miss_reg 138
(checker: 721/140): history-retiring rebinds preserve `binding_at(j,t)` through the retired segment,
so **the reuse law is value-equality through history, not absence of mutation — the exact pre-walk
certificate costs the walk it skips.** The news-fed window (membership at kick/birth events) is the
only lever and must eat the whole walk, radial query included. **Prior standing (9b03):** news_frac
1.2–11.4%; player binding changes 49–51% of scans; memo 47% same-tick burn; radial fence
belt-N-fragile (checker: flight-dependent too — 3e3 burn fences, 0 fallback).

## Refuted

- **NEW — "the exact pre-check deletes 47–50% of captures' walks" (od 3, as a cheap guard):**
  refuted as wired — three exact forms (global epoch; per-row epochs over near + per-doll
  registration epochs; value-compared `me` + per-row epochs) all 0 hits on the shipped plane,
  digest-identical to off; the domain is value-equality through history (rebinds preserve
  `binding_at(j,t)`), which only the walk itself checks (20261021-1551-spacex-eb24).
- **"The news-fed ceiling is only the build term" (od 1's implicit risk): refuted by attribution —**
  the fence arm's walk is 73% radial query; only the fallback arm is build-dominated (43%)
  (20261021-1551-spacex-eb24).

## Open directions

1. **The news-fed window, now priced:** maintain the candidate set at kick/birth events (9b03's
   composition), evaluate the predicate per scan. Its target is the whole walk per arm (eb24's
   table), of which 37–60% is currently pure repeat (memo-discarded). The radial query must go
   with it (73% of the fence arm's walk).
2. **The wave-era fallback capture** (129/3427 at rtf 2000, near = 100,076 = the whole doll):
   the one regime where the walk is milliseconds; a capture-side bail or streaming form (scan-
   locality od 2/od 3) is worth more than everything else combined at rtf > 1000.
3. ~~Attribute the walk's internal cost~~ **Executed (eb24): radial/loop/build/lookup split per
   arm, bias-calibrated at 36.2 ns a timed call.**
4. ~~Wire the pre-check~~ **Executed and refuted (eb24) — see Refuted.** What survives of the
   idea: the reuse is already exact post-walk (the memo, 37–38% hit rate); making it pre-walk
   needs the value domain, which is the walk.

## Contradictions

None open. 9b03's caution (the pre-check needs a nothing-resolved-since dirty bit) is resolved
by measurement: no dirty bit at this call site can be clean — the player's own apply precedes
every capture, and the near rows' rebinds are history-invisible to the values the scan reads.
>>>>>>> 20261021-1551-spacex-eb24

## Runs
- 20261021-1443-system-9b03 (system): the scan walk measured for news on three arms — news_frac 0.012–0.114, memo 47% same-tick on burn, radial fence belt-N-fragile; the scan row is information-coupled to the kick dial.
- 20261021-1551-second-20261021-1443-system-9b03-89f3 (second): news-fed window wired, 8/8 digest-neutral; walk falls with the kick dial 205× (floor = churn); radial is capture's µs owner at shipped C, sig ≈ read. Checker: exact at N=100k and D=512 (walk flat at the floor 64→512) and on a 30 s burn (471k scans, walk 5.30 → 0.00, memo 49.9%); fallback arm −37% µs.
- 20261021-1551-spacex-eb24 (spacex): od 1 executed (walk priced per arm, radial 73% on the fence arm) and od 3 refuted (0 hits × 3 certificates, miss mechanisms named; overpayment 37–60% of walk time).
