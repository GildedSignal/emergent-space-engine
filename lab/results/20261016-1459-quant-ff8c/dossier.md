# Dossier — 20261016-1459-quant-ff8c (Quant): apply's position walk, deleted twice, exactly

## Claim

`apply`'s `root_state_raw` position walk (kick-jet's named-but-unbuilt −13 % lever) is deleted
by `ES_POS_CARRY` (~55 lines): the stage falls **−84…−87 %** (0.797–0.992 s → 0.126–0.127 s on a
belt flight of 10⁵ bodies to 20,000 game-s; 4,951–6,164 → 783–790 ns/call), the deletion is
**exact** — `ES_POS_VERIFY` re-walked all **130,434** carried rebinds with **0 mismatches, 0
walk errors**, and digests are identical on that flight, on all 8 `frame_digest` flights × 4
schedules and all 13 `ladder_digest` cases × 4 schedules.

## Bottleneck

The kick at 75–160 µs against a ~50 ns floor (the scoreboard's ~10^3.3 gap). 5ade
(20261016-1120) decomposed the wave kick and priced this walk at −13 % of the event cycle,
unbuilt. This run builds it and finds **two** duplicates, not one:

1. **The carry.** A rebound body's walk re-reads `b.cartesian(b.event_time)` — the state
   `rebind` just bound. `bind.rs` promises the readout at the binding event is the bound state
   *bit for bit*; `rebind` now hands `scalars(exact)` to `apply`, which scales it to root units
   (`root_pos_from`, the walk's own-half arithmetic, operation for operation) and walks only the
   doll chain above.
2. **The skip.** An unrebound body's walk recomputes a value the position cache already holds:
   the walk runs at `b.event_time`, and if nothing rebound the body, the cache was written from
   the same binding at the same tick (`pos_tick`). On the belt this is the whole boundary class —
   skips 30,481 ≈ boundaries 31,291.

Counter structure on the belt flight (the instrument the reasoning predicts): **hits 130,434 ≈
fired kicks 131,537 (every rebind carried), skips 30,481 ≈ boundaries, walks 100,075 = one per
birth** (O(births), not O(events) — the surviving stage is the birth bill, 1.26 µs each).


**Provenance note (the shared tree).** A sibling run's `run.sh` restored the shared checkout
mid-flight (15:18), wiping this run's working-tree edits; the evidence above was already
produced and saved. The edits were re-applied from the recorded patch, rebuilt from scratch and
re-flown (`work/belt_{off,verify,on}_re.txt`, a fresh compile): the same digest `a287f479…`,
the same counters (130,434 / 30,481 / 100,075, mismatch 0) and ROOT 0.778 → 0.115 s. The
sibling's own edit (`xtask/src/universe/kick_bench.rs`) is left untouched and excluded from
`work/patch.diff` (pathspec `crates/universe`).
The cycle share: ROOT was 15.2 % of (ROOT + kick items) on the OFF arm (0.797 / 5.241 s);
deleting 84 % of it ≈ **−12.7 % of the event cycle** — 5ade's −13 % pricing, now measured on
the built change. At the 10⁹ rail the per-event walk is gone whole (kicks carry, boundaries
skip); what remains is O(births). The stage's kick-item wall wobbles ±25–30 % between runs on
this shared box — paired A/B only; the stage table, counters and digests are stable.

## Evidence

All numbers regenerate (commands below; Linux x86 shared box, orders of magnitude only):

- `pos_carry` OFF/ON/VERIFY ×2, N=10⁵, cut 20,000 game-s (through the first wave):
  - digests `a287f479…` identical, all 5 runs × 3 arms;
  - ROOT 0.992/0.797 s (OFF) → 0.126/0.127 s (ON); ns/call 6,164/4,951 → 790/783;
  - VERIFY arm: mismatch 0, walk_err 0, hits 130,434 (digest identical);
  - paired event cycle: 5.241 → 4.746 s (−9.4 %; the second pair −30 % but its OFF arm is the
    noisy one — the honest range is the ROOT share arithmetic, −12.7 %).
- `ladder_digest` (13 cases × 4 schedules, planet-doll locals and belt crossings included):
  every case's digest identical OFF vs ON (e.g. wave case `df0e87cd…`, crossing `ef19d3de…`).
- `frame_digest` (8 flights × 4 schedules): every digest identical OFF vs ON.

## Predictions

Written before the decisive runs (`predictions.md`). Held: bit identity (0 mismatches — the
bind.rs promise is true on every rebind of the flight), digest identity everywhere, the hit
structure (hits ≈ kicks, skips ≈ boundaries, walks ≈ births). Held with a correction: I
predicted the fired kick would fall ~2–5 µs; the walk stage is outside the kick-item timer, so
the gain reads on the event cycle (−12.7 % by ROOT share), and the paired wall deltas (−9 %) sit
inside the box's ±25–30 % wobble. The walk-error counter stayed 0 (prediction 2's side branch
never fired).

## What would make it wrong

The carry rests on one law property: a binding's readout at its own event tick is the bound
state, bit for bit. VERIFY tested it on 130,434 rebinds of one belt population (and the digest
matrices cover the locals' dolls); a regime where the fit's remainder does not reconstruct (the
strong-field tail, e ≥ 0.99) is untested — a mismatch there would show as POS_MISMATCH > 0 with
digests possibly still identical (the cache is scheduler-only), so the gate must stay paired
with VERIFY when adopted. The skip rests on `pos_tick[i] == b.event_time` implying an unchanged
binding: bindings append forward in time, so a fixed tick's `binding_at` is stable — if a path
ever rewrote a binding in place at the same event tick without `rebind`, the skip would go
stale; none exists today (searched: `rec.b` is written by `rebind`, `bind_exact` at creation,
and kick/impact fields that the readout never reads).

Cost of adopting: `pos_tick` is 8 bytes per body (a `Tick::MIN` sentinel could fold it into the
existing cache); the carry adds 32 bytes to `Update` (stack) and one `Option` store per rebind.
Off (no env var): the old path, verbatim.

Fit with PRINCIPLES: "The cheapest compute is compute not done. Delete before optimizing" (1);
"Nothing is evolved that can be derived when looked at" (3) — the position is derived from the
binding, not walked; exact means deterministic — 0 mismatches, digests identical (2). It is
bookkeeping, not law: no behaviour, no representation change (19's "the right representation
already feels right" — this is deleting a redundant read of it).

## The lens

Quant's blind spot is shaving nanoseconds off a path the cadence split will delete: the
kick-cadence page says the belt's fired impulse is 2⁻²³ of the body's speed, and a cadence law
that fires 10⁶× fewer kicks deletes this walk with it. The run's defensible core is the exact
identity instrument (VERIFY) and the two-duplicate decomposition — both transfer to whatever
cadence survives. What the lens also hid: the wall instrument on a shared box (±25–30 %) — the
stage table and counters, not µs, are the reproducible numbers.
