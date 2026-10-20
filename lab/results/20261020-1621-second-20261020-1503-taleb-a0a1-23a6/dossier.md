# Dossier: the dropped bound carried — exact, ~100× on the warm answer walk, and it still does not reopen the channel

## Claim

The checker's named gold experiment is flown whole: the dropped bound (ce694696's per-body
remembered-position map, 72b71c56's deletion), re-anchored on the shipped `same` (the memo is
valid exactly when the scan-reuse machinery would say the read is unchanged) and carried in
front of the predicate, is **exact** — digest-identical to the shipped finder at 1e5 and 3e5 at
a canonical cut — and it **collapses the answer walk ~100× where the memo is warm** (4.17 →
0.041 µs/body mean on belt-wide answers at 1e5, skip 97.55%; 0.125 µs/body warm at 3e5), which
takes the drain-all settle from 18.4 s to 1.1 s at 1e5 (1.6 → 0.2 s at 3e5) and [INFERENCE]
puts a warm belt-wide answer at 1e9 near 41 s — under the 69.75 s era budget, against ~72 min
unbounded. But two of a0a1's sentences die by measurement: the bound does **not** attack both
walks (the capture walk stands at 0.247–0.292 µs/body, still the O(N) term on the frame's
critical path), and it does **not** reopen the channel (the guard still locks on the first
≥ 6 ms cold answer; belt-wide scans are still never answered in-window at 1e5/3e5) — it changes
the lock's consequences: the backlog cap's forced answers become cheap and no new worst-frame
class appears.

## Bottleneck

Board focus 1 × 2 (bodies 28 → 10⁹; encounter work at 10⁹). The answer walk was the channel's
unpayable term (4.2–4.4 µs/body × doll). The bound deletes ~97–99.9% of its reads at a
~30–50 ns/candidate check, with zero outcome change (digest identity). What it deletes at 1e9:
the ~72 min uninterruptible answer becomes a ~41 s schedulable one [INFERENCE]; what it does
not delete: the capture walk (~290 s per player item at 1e9) and the lock's cold lump (the
first answer after memo invalidation still pays the full read law on the bodies it must read).

## Evidence (flights ≤ 60 s wall each, build ~10 s; commands in regen.sh, ~10 min total)

Same scene and arms as a0a1 (burn, rtf 1300, 12 ms budget, unstaggered — the kick comb owns the
worst frames, disclosed). The instrument is a0a1's verbatim (CAP/ANS lines), plus `skip_bnd`
(the carried bound's skips) and the bound itself behind `ES_CARRY_BOUND`.

**Digest identity (P1), at a canonical cut** (`settle` + digest; cut mode schedules the burn at
one fixed tick): 1e5 cut 30k gs — OFF `8eecf1fa…` **twice, byte-identical** (1438/1437 frames:
pacing differs, digest does not), ON `8eecf1fa…` identical (1443 frames), across 41 belt-wide
answers × 99,715 candidates with mean 97.55% skips ≈ 4.1e6 bound decisions; 3e5 cut 19.5k gs —
OFF `1f6101a9…` == ON `1f6101a9…` (pre-ALL era there, windows to 32,680 cand); 3e3 cut 16k gs —
identical (`8d314997…`, the calibration pair). **The verify control** (`ES_BOUND_VERIFY`: every
skipped body read exactly and asserted not-hit, 3e3, 45 s): zero panics. The identity was first
confounded by a harness leak — see Predictions.

 Two instrument artifacts, named so the checker reads the lines right: the first `compute` of a
 flight pays a one-off memo allocation (~7 ms at 1e5, ~21 ms at 3e5 — the `cand=39` answers with
 read share 1–2% and µs/body in the hundreds), and each draw re-rolls the wall numbers inside
 the same bands (regen's W3: CAP ALL 0.298 µs/body, worst frame 2,779.7 ms, RSS 5,915 MB — same
 classes as the dossier's 0.292 / 2,566.9 / 5,916).

**The answer walk's collapse:** at 1e5 the settle answers every held scan: 41 belt-wide
(cand = 99,715) answers, ONE cold (3.86 µs/body, 380 ms, skip 10.9% — the first full-doll read
is not skippable, exactly as pre-registered), 40 warm at **0.041 µs/body mean** (worst 0.052,
best 0.030; skip 97.55%) against the OFF law's 4.17–4.5 — **~100×**. At 3e5 (pre-ALL windows):
OFF 4.52–4.71 µs/body; ON cold 1.89–2.29 (partial memo from earlier window reads), warm 0.125
(skip 99.6% on a re-answered 10,593-cand window) — **~37×**. Settle: 18.4/18.8 s → 1.1 s (1e5),
1.6 → 0.2 s (3e5).

**The channel does not reopen (P5's kill bar, first branch, fired at both rungs):** W2 (1e5 ON,
45 s unfenced): held_max 2,048 (the cap; OFF 1,326), max answered cand 3,546 (OFF 1,804) — the
belt-wide scans are still never answered in-window; the cap's forced answers now ride the memo
(top 8.0 ms / 3,546 cand = 2.25 µs/body, skip 50.6%) and the worst frame stays the comb's class
(803.6 ms vs OFF 880.9; 3e5: 2,566.9 ms, the 52,066-event comb, vs a0a1's a1 2,647). RSS 1,978
vs 1,957 MB at 1e5. **W3 (3e5 ON, unfenced) peaked 5,916 MB — over the 2 GB runner cap,
disclosed** (a0a1's a1 was 5,101 MB fenced): the queue holds ~126 distinct belt-wide scans of
~40 MB each waiting for the front; the bound does not fix held-scan memory either.

**The capture walk stands (P4):** CAP `radial=ALL` 126 walks, 0.267 µs/body OFF / 0.247 ON at
1e5, 0.292 ON at 3e5 — a0a1's 0.24–0.31 band, unchanged: the bound is answer-side only
(ce694696's memo lives in `compute`), so a0a1's "attacks the measured dominant term on both
walks" is half-refuted — the capture walk (the O(N) term on the player's item) is now the
channel's standing problem, and b57f's tier remains its named exit.

## Predictions

predictions.md was written after the 3e3 calibration pair (identity held there) and before every
1e5/3e5 flight. **P1 failed first, then held for a reason worth a rung of its own**: the first
D-pair's digests differed, and the diagnosis exonerated the bound — my cut harness had
replicated wall mode's `input(p.u.now, …)` at frame 60, so the burn's tick was the presented
time at frame 60, which is wall-pacing-dependent; an OFF repeat reproduced the difference
(both draws appeared, and one ON digest matched one OFF draw exactly). Fixed by scheduling the
burn at one fixed tick (`p.u.schedule`), after which OFF×2 is byte-identical and the pairs are
identical at every rung. Lesson: a wall-mode input at `now` ties any digest to pacing; the
shipped "independent of schedule" guarantee holds once decisions are at fixed ticks — which is
what `schedule` is for. P2 held (0.041 ≤ 0.5 µs/body, ~100× ≥ 8×), P3 held (one cold 380 ms
lump at 3.86 µs/body), P4 held (0.247–0.292 µs/body), **P5's kill bar fired** (zero belt-wide
answers in-window, held_max at the cap — reported as the finding, not hidden), P6 held (worst
frame 803.6 ms, the comb; no new lump class beyond the cold one, which at the cut lands in
settle, not in a frame).

## What would make it wrong

The identity is measured at cuts that cover the belt-wide object fully at 1e5 and 3e3 but only
pre-ALL windows at 3e5 (a later 3e5 cut exceeds the memory cap on the OFF arm: the ALL scans it
would hold cost ~40 MB each); a 3e5 belt-wide identity remains open. The warm constant assumes
the memo stays warm: every kick or rebind invalidates that body's print (a re-read at ~4.3 µs),
so the warm cost is really `skip × check + miss × read`, and the miss rate is the kick rate —
at the belt's ~5e-5 kicks/body/gs the first-boundaries era will re-read most of the doll once
per ~27.9k gs [INFERENCE]. The 1e9 numbers are linear extrapolations of measured per-body
constants (9ed1's checker's convention). Cost of adopting: the per-body memo (a Binding + tick
+ 2 floats ≈ 100 B/body ≈ 100 MB at 1e9, or the compact print of ce694696's original), one
float test per candidate, and the `same` anchor — the patch is env-gated, `ES_CARRY_BOUND`
off = shipped bits. Fit with PRINCIPLES: 1 ("the cheapest compute is compute not done" — the
read is not done), 2/34 (exactness kept: the oracle's predicate still decides every kept pair;
the bound only proves some pairs cannot reach it), 12 (the lump becomes schedulable, though the
lock still needs the tier or a maintenance signal), 19 (the lock that survives is the wrong
representation's signature, not a scheduling problem).

## The lens (second author)

What this lens may have missed: the memo's invalidation rate was read off the kick stream, not
measured directly (a per-answer miss-rate counter would price the 1e9 warm cost properly); the
guard's recovery-by-decay was not re-measured under the bound (the settle path answered
everything, so the in-frame decay path never mattered); and the memory arm at 3e5 ran over the
cap rather than being pre-fenced — disclosed above, same class as a0a1's own a1.
