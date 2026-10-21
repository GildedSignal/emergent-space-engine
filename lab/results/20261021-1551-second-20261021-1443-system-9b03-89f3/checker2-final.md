Grade: gold**Grade: gold** — written to `check2.md` / `checker2-final.md`, with one evidence-backed refinement folded into the run's `wiki/scan-news.md` (Contradictions: the radial-fence failure is coast-specific — at 3k *burn* it passes, 0% fallback, my flight).

**What I did as the blind second checker:**

1. **Reproduction, clean tree.** Applied `work/patch.diff` at the base commit myself; every deterministic number regenerates bit-for-bit: all digests, walk counters (65.55 → 1.20/0.46/0.32 burn; 163.19 → 3.67 coast; 2536.71 → 86.14/53.12 fallback), and memo counts equal shipped↔newsfed on every arm (362/362, 365/365, 22/22) — that equality is itself evidence the kept candidates are the rebuild's.

2. **Exactness audited in code, not just flown.** `binding_until` is the exact segment-end companion of `binding_at` (identical case analysis, `body.rs:157–178`); the signature (event_time, alive, recomputed until) catches rebind (`step.rs:374–383` retires and stamps `event_time = t`), prune and death; the only in-place binding mutations are `.kick`/`.impact`, which no scan reader reads (`same()`, `compute()`, `readout`/`cartesian`).

3. **Thirteen adversarial arms of my own, 13/13 digest-neutral:** outside the author's range (N=100k burn D=512 — walk flat at the 0.32 churn floor; 30 s horizon — 471,055 scans, walk 5.30 → 0.00, memo 49.9%), fresh seeds (7, 13), non-dyadic D (3, 12 — monotone fall), and fallback-under-burn (regime refinement: fence failure is coast-specific). My independent fallback-arm timing confirms the page's −37% µs win: 156.4 → 96.4 µs (−38%).

4. **Predictions** were pre-registered (file times precede the matrix logs); P1–P3 held, P4 refuted and reported as the run's finding — the honest form. **Novelty:** executes the topic page's named open direction and answers 1fd7's standing ledger line; no HISTORY entry predates it. Tree left clean, nothing committed.
`same()`, `compute()`, `readout`/`cartesian` read entry/tube/turn/residual/units/clock_exp only). Cached clones share the immutable entry Arc, so `same()`'s `ptr_eq` holds.
3. **Predictions pre-registered and honest.** predictions.md (28 m old) precedes the matrix logs (12–13 m); P1–P3 held, P4 refuted and reported as the run's finding — "a failed expectation is not automatically a failed method" (H0183) done right.
4. **Novelty.** Executes the topic page's named od ("wire the pre-check… digest-neutral by construction") and answers 1fd7's standing ledger line ("walks 111–311×, cadence-invariant", kick-cadence.md:19): the walk's information rides the kick dial — 205× measured — while its shipped µs do not, because the row has two terms and the radial membership query owns the fenced arms' µs. No HISTORY entry predates it. The µs refutation is a premise correction the 10⁹ ledger needs.
5. **Goal fit.** PRINCIPLES #3: "Compute only surprises… Nothing is evolved that can be derived when looked at" — the walk re-derived unchanged bindings; now deleted in work units, exactly. The negative µs result respects #27 (the goal, never a proxy): work units were becoming a proxy for frame µs, and the run prices them separately.

**What the author missed.**
- The radial fence's failure is coast-specific, not small-N-only: at 3k *burn* it passes (0% fallback, digest-neutral, my flight) — the player's motion rebuilds the window; sharpen's od 4's domain question (I folded this into the page's Contradictions).
- At the 30 s horizon the burn window collapses (near/scan 72.7 → 6.3, the player flying out of the belt): the 0.3–0.6/scan churn floor is a 6 s-window number; at steady state the news walk is ~0.003/scan. The growing-window corner (flying *into* the belt) remains unflown, as the author concedes.
- The slot cache holds a full Binding (~192 B) per ever-candidate body; the author notes the ~5 MB cost at 30 k but not its scaling at the 10⁹ row the ledger prices (fallback arms cache rejects for *every* body: 2,506 kept slots at 3k).
- The signature's three dyn-dispatched trait calls per id are an artifact of the read-side form; the author names the write-side dirty word as the fix but does not price it even at wiring level.

Both checkers' numbers stand: gold.
