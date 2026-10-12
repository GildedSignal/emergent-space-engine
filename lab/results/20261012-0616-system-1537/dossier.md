# Dossier — run 20261012-0616-system-1537 (lens: the whole system)

## Claim

The plane's engine still contains a **hidden tick**: every `advance` (every frame, and every pass of
`settle`'s loop) runs `rekey`, which recomputes the deadline of **every entity** (a sqrt on the cached
root position plus an indexed-heap set) whether or not anything is due — measured **215 µs/frame at
1,000 quiet bodies, 37.4 ms/frame at 64,000, with zero events** (superlinear: 174× cost for 64× bodies,
from the heap sifts and cache misses; the Calendar's own doc says re-predictions "dominated the
calendar's cost at a million bodies") — and the naive deletion (key the calendar by the canonical tick,
compute deadlines only for the frame's due set) collapses this to **0.1–0.5 µs/frame flat from 1k to
256k bodies (~80,000× at 64k)** but **breaks schedule-independence** (digests diverge across schedules
and from the unpatched baseline), proving the rekey pass is load-bearing beyond its documented role:
it is also the *repair* for stale calendar slots left by `pull`'s direct `resolve_body` calls and for
the fleet's commit-cap ordering. The tick is real and must die; the one-line deletion is not the way.

## Bottleneck

Principle 14 ("No work for no reason, so no ticks") and principle 12 (smoothness: the p99 and the
worst frame). Extrapolated, the rekey pass alone is ≥ 1 s/frame at 10⁶ quiet bodies and ~1000 s/frame
at 10⁹ — the belt (b-belt-wire) and B18's 2²³-body rungs cannot ship behind it. **B10 cannot catch
it**: B10 gates the *total-cost exponent* (≤ 1.1) on frozen scenes, and a per-frame O(N) term is
linear — it passes the gate while killing the goal. The requirement nobody owns: *frame cost at fixed
(low) event rate must not grow with N*. The expected gain of the correct fix is the deletion of the
per-frame pass (measured 80,000× on the quiet frame; at scale it is the difference between flying and
not).

## Evidence

Commands (each ≤ 60 s; Linux x86, 8 vCPU, load ~1, 15 GB, single-threaded engine; orders of magnitude
only, the M1 re-measures). Binary: `cargo build --release -p emergent-universe --example tick_audit`
(target dir `/home/glmlab/lab-target-1`), then:

```
tick_audit quiet 1000 30    # also 4000, 16000, 64000 (unpatched and patched)
tick_audit digest           # three schedules, one canonical cut 9e10, threads 1/4, budgeted/starved
```

**Unpatched (the tick):** quiet frames (no events, all next items ~1e11 ticks away):

| n | per frame | worst frame | ns/body/frame |
|---|---|---|---|
| 1,000 | 215 µs | 218 µs | 215 |
| 4,000 | 971 µs | 1,115 µs | 243 |
| 16,000 | 7,088 µs | 8,683 µs | 443 |
| 64,000 | 37,436 µs | 39,024 µs | 585 |

**Patched (tick-keyed calendar, per-frame rekey deleted):** 0.12 / 0.10 / 0.11 / 0.47 / 0.12 µs per
frame at n = 1k / 4k / 16k / 64k / 256k (rss 494 MB at 256k, inside budget). Raw lines in
`run-log.txt`.

**The correctness gate (pre-registered):** unpatched, three schedules (A: settle, threads 1; B:
threads 4, wall-budgeted frames; C: starved 3-events budget, overflow path) all print
`645d0367d54b951b…` — schedule independence holds in the shipped code. Patched (first cut): A, B, C
print three *different* digests, none equal to the baseline (`digest-after.txt`). Adding the missing
`requeue` at the end of `resolve_body` (the `pull` path resolved bodies without refreshing their
calendar slots — the per-frame rekey was masking this) changed the digests again but did **not**
restore agreement (`digest-after2.txt`: three new distinct values). Schedule A is pure sequential
settle (no waves, no budget), so the remaining leak is not the wave path; the prime suspect is the
fleet's commit cap, whose old semantic ("run the battle only as far as the light-delayed deadline of
the next entity in line", the min deadline over *all* entities) is only approximated by the
min-*tick* entity's deadline in my patch — a different commit interleaving of the battle relative to
other bodies' reads, and the fleet hands out member ids in commit order.

## Predictions

`predictions.md` was written before the patch ran. Outcome: **(1) held and exceeded** (≥ 300×
predicted at 64k; measured ~80,000×; ns/body/frame fell to ~0.01, predicted ≤ 2). **(2) failed**:
digests are not `645d0367…` and diverge across schedules — the pre-registered kill of the patch with
the diagnosis standing. (4) half-confirmed: the wave path is not the (only) leak, since the sequential
schedule also diverges.

## What would make it wrong

- The quiet-frame extrapolation assumes sparse scenes persist at scale; a universe whose event rate
  is ~N per frame would amortize the rekey into the event cost. The goal's own premise ("space is so
  empty that there's no way that it can't be cheap") and the belt's measured ~0 events/frame say
  otherwise, but the honest number to hold is the *shape* (per-frame O(N) at zero events), not the
  constant.
- The leak localization (fleet cap vs something else) is inference from A-vs-B-vs-C plus code reading,
  not yet a direct experiment; my `restricted` (fleet-free) discriminator panicked on `NoBoundOrbit`
  — a scene-parameter error, not evidence.

## Cost of adopting, fit with PRINCIPLES

The correct fix is one step beyond this run: (i) requeue at every resolution site (done here for
`resolve_body`), (ii) keep the fleet cap's min-over-all-deadlines semantic (the due heap already holds
the due-side min; future entities' deadlines are bounded below by their ticks), (iii) re-face the
digest across schedules — the failing digests *are* the test. No law change: the deadline is
documented as "a scheduling heuristic only", and keying the queue by the canonical `(t, id)` is what
docs/law.md "Ties" already specifies ("the queue's key is (time, smallest body id, kind), so every
schedule, budget and thread count pops the same sequence" — the shipped code does not do this; it keys
by deadline). Fits principle 1 (delete before optimizing), 14 (no ticks), 12 (the worst frame), and
engine.md rule 2 ("No work without a requirement"); the failure mode found fits the lens's own hunt
("a component that exists only to repair another": the rekey pass repairs `pull`'s stale slots).

## The lens

What this lens may have missed: I audited the *engine's* frame path, not the view (b-readout-cost
owns it; the view is per-emitter by design and pixel-capped later) and not `prune` (also O(N) with a
sqrt per body, but every 64 frames — the same family, one more deletion for the same builder). The
elegant unification (one canonical key everywhere) hid the hard special case the lens told me to
name: the fleet, whose commit interleaving is order-sensitive through id issuance, is exactly the
case that broke it.
