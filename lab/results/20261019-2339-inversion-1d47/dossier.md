# Dossier — 20261019-2339-inversion-1d47 (inversion)

## Claim

The root burst (the player's item legally pulling the whole doll's due ships past the budget,
cc9d's wall) is an **over-strict read order, not a law necessity**: extending the 766-770
budgeted-stream pattern to root — one gated line at `universe.rs:770` — deletes the wave's
worst frame **58-111×** with **every shipped digest bit-identical** (14/14 on `ladder_digest`,
all four schedules still agreeing), because the queue's deadline order (`key + light_distance`,
`universe.rs:564` — "when its light reaches the player") is already the light cone that fences
what a scan can ever read stale.

## Bottleneck

The board's first: real bodies in the flyable engine (28 → 10⁹), whose measured wall at the
flown rungs is this burst (cc9d: max_ms ≈ 8.1-9.5 µs × K, ~8 s a frame projected at 10⁶).
Gain: ~10² on the worst frame at 10⁵-2×10⁵ (max 867.9 → 15.0 ms; 1,851.9 → 16.7 ms), p99 back
inside the budget (225 → 11.9 ms). What it deletes: the need for the allocator or the
built-unwired encounter tiers to fix *this* wall, and cc9d's "a law change" cost — nothing to
re-freeze, the digests hold.

## Evidence

All numbers from this run's arms (Linux lab box, load ~0.4-6, 8 vCPU; orders of magnitude).
Patch: `work/patch.diff` — the gate `ES_ROOT_SHIPS_TO_QUEUE` (universe.rs:770), a staleness
probe `ES_FIX_PROBE` (a captured candidate is *stale* when its body's next item is due before
the scan's tick), and a `#[cfg]` Linux `/proc` footprint shim for the example (the shipped
`proc_pid_rusage` is macOS-only). Unset = shipped bit for bit.

**Off ≡ shipped, verified:** `ladder_digest` with the patch off reproduces the record's
digests (`artifacts/runs/nladder/ladder_digests_before.txt` / `_wave.txt`) exactly, 14/14,
including both belt crossings — the instrument and the off-path are clean on this tree.

**The law (the decisive arm).** `ladder_digest` with the gate **on**: all 14 digests identical
to shipped (belt crossing L10 included — the player in the star's doll among the belt, through
the first kick wave), kicks and encounters per case identical (789/789, 934/934, 3945/3945…),
and the four schedules (unlimited, 25 events, 4 threads, 3 ms wall) still agree in every case.
Bookkeeping, not a law.

**The burst (nladder burn, seed 1, rtf 1000, 12 ms, probe on):**

| rung | arm | max_ms | p99_ms | over | lag_s | stale (max/scan) | refusals/dead | end rss |
|---|---|---|---|---|---|---|---|---|
| 10⁵ | off | 867.9 | 45.8 | 15 | 15.05 | 0 (0) | 0/0 | 483 MB |
| 10⁵ | on | **15.0** | 11.95 | 7 | 16.67 | 3,829 (541) | 0/0 | 354 MB |
| 2×10⁵ (held out) | off | 1,851.9 | 225.1 | 19 | 15.62 | 0 (0) | 0/0 | 947 MB |
| 2×10⁵ (held out) | on | **16.7** | 11.9 | 5 | 16.46 | 4,686 (598) | 0/0 | 542 MB |

OFF's worst frames are the record's gulp (one player item, 15-16k events: 867.88 ms/15,098 at
frame 882; cc9d's and 0c0f's bands reproduced). ON's worst frame is 228 events — the wave
drains at the budget over ~10³ frames, which is the lag: +1.4-1.6 s over the flight.

**The mechanism, measured and in code.** With the gate on, scans do capture stale bindings
(the probe's 3,829/4,686 candidates; zero with the pull), but a candidate can only be stale
when its deadline exceeds the player's item — i.e. its light distance exceeds the deferral
(≥ 1 tick ≈ 5 ms ≈ 1,500 km) — while a ship-ship conjunction needs ≤ 2¹⁰ radii (sub-km):
three orders of magnitude apart, so no encounter predicate can flip on a stale read. Planets
(the large-radius case) are never deferred: `resolve_body` pulls their lanes to the key first
(`universe.rs:720-722`). The queue's deadline order is the light cone; the pull at 770
resolves ships before their light can matter.

Reproduce: `lab/results/20261019-2339-inversion-1d47/regen.sh` (~10 min: builds, both
ladder_digest arms, all four flights; prints the digest identity and the headline table).

## Predictions

`predictions.md`, written before the decisive arms. **P1 held** (ON max ≤ 60 ms predicted;
15.0/16.7 measured; lag grew as predicted). **P3 held** (kicks per case identical; the digest
identity subsumes it). **P4 held** (refusals 0, dead 0, alive everywhere; no hang). **P5
held** (OFF stale = 0; ON stale > 0 only at the wave, max 541-598 a scan). **P2 failed
constructively**: I predicted the belt-crossing digests would change or the schedules
disagree; measured bit-identity instead. That failure is the result — the fix is cheaper than
the record believed. The held-out rung (2×10⁵) and the key-mashing/through-the-wave cases
held everything.

## What would make it wrong

A reader that needs a ship's state *before* the ship's light can reach it (none exists in the
shipped code: the scan is the only capturing reader, the view reads last state by design,
fleets and hand-outs are pulled separately at `universe.rs:733-741`). A body with a
conjunction reach comparable to a light tick (a ship with radius ≳ 1,000 km — not a ship).
The lag cost is real and lands on the player's presented time at the wave (~1.5 s per 18 s at
rtf 1000): if Julien's playability bar prefers one 1.9 s freeze over ~1,000 budgeted frames of
lag, the trade inverts — that is a judgement, not a measurement.

## Cost of adoption, fit with PRINCIPLES

One line (delete the `!in_root` distinction at 770 — the gate verbatim), no digest re-freeze
(measured bit-identity, but the integrator re-freezes on the M1 per process), no new state.
PRINCIPLES: "beyond c=1 means paradoxes" / "his direct influence is bounded and propagates at
c at most" (23, 5) — the deadline order is that bound, and the pull was paying to resolve
ships before their light can matter; "No work for no reason" (14); "i care about the p95/99
results i want the game to be smooth" (12) — p99 225 → 11.9 ms at 2×10⁵. The best part is no
part: the deleted code *is* the fix.

## The lens

Inversion found the fix by asking what the named fix would break, and the answer was
"nothing measurable — because the light cone already does the work the pull was doing
synchronously". What the lens may have missed: only 18 s flights (the backlog's steady-state
drain across a *sustained* burn is untested beyond that); single seed per rung (the wave's
onset is seed-sensitive per 0c0f's checker, but the digest identity carries no seed
dependence — it is structural); and the 10⁶ rung is unbuildable in this container (2 GB cap).
The lag-vs-freeze trade is flagged, not decided.
