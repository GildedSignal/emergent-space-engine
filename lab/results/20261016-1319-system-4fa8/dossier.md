# The comb is the anchor: one interval law retires the locals' storm at no steady-state price

## Claim

The locals' standing comb (nladder's frame-binding term: max 334 events/frame, p99 136) is
manufactured by the engine's second interval law — `step::aligned` re-anchors every planet-doll
interval to the absolute power-of-two grid, while the clock law chains from the previous event —
and unifying on the chained shape plus the existing one-step birth spread (`ES_CHAIN=1
ES_LOCAL_STAGGER=1`, a law change that gives up pair-shared boundaries exactly as ES_LOCAL_PHASE
does) collapses the storm to the N=0 floor class (max 334→52, p99 136→24 over 5,400 game-s,
N-flat 600–10⁴, no re-formation) with **zero incremental event rate** (3.17 vs 3.16 events/game-s
past 1,900 s) and **−11% total engine CPU** (1,560→1,385 ms over the same 3,300 frames) — a
strictly better trade than ES_LOCAL_PHASE's permanent +19–41% events for the same collapse.

## Bottleneck

Bodies in the flyable engine (the furthest gap, 10⁶ vs 10⁹): the checker-corrected letter says the
12-ms frame at 10⁶ is locals-driven (the comb, ~334 events ≈ 9.8 ms M1), with memory binding at
1.3–1.6×10⁶ only after it. This deletes the comb **class** (not one population's patch): the
per-body phase grid of ES_LOCAL_PHASE (and its stub minting at step changes) is replaced by one
interval law — the clock law's own shape — plus the birth spread the belt stagger already is on
the clock side. Expected gain at the letter: the frame's locals term drops ~6× (as ES_LOCAL_PHASE
showed) and, unlike it, the average does not pay permanently.

## Evidence (this Linux box, budget-free coast, rtf 100, seed 1, threads 1; ms are box-relative)

`nladder <N> coast <s> 100 1000000`, arms by env (off = shipped, bit-identical):

| Flight | Arm | max ev/frame | p99 | events | kicks | boundaries | slices |
|---|---|---|---|---|---|---|---|
| N=1000, 1,900 gs | off | 240 | 146 | 11,111 | 3,624 | 3,499 | 3,951 |
| N=1000, 1,900 gs | chain | 228 | 142 | 11,071 | 3,622 | 3,495 | 3,917 |
| N=1000, 1,900 gs | stagger | 210 | 139 | 11,642 | 3,801 | 3,657 | 4,147 |
| N=1000, 1,900 gs | **chain+stagger** | **52** | **27** | 15,596 | 3,717 | 3,542 | 8,300 |
| N=1000, 5,400 gs | off | **334** | 136 | 22,219 | 9,217 | 9,014 | 3,951 |
| N=1000, 5,400 gs | **chain+stagger** | **52** | **24** | 26,670 | 9,270 | 9,063 | 8,300 |
| N=0, 1,900 gs | off | 51 | 36 | 6,011 | — | — | 3,951 |
| N=0, 1,900 gs | chain+stagger | 44 | 13 | 5,827 | — | — | 3,746 |
| N=600, 1,900 gs | off → chain+stagger | 240→50 | 146→30 | — | — | — | — |
| N=10⁴, 1,900 gs | off → chain+stagger | 240→50 | 146→27 | — | — | — | — |

- The OFF max over 5,400 game-s is exactly the record's 334 (4c22's number, reproduced
  independently on main-as-shipped by this instrument).
- **The +20% event total is a constant early excess, not a rate:** past 1,900 game-s the
  incremental rates are equal (OFF 3.17 vs 3.16 /game-s); the excess (+4.4k events) is entirely
  fleet-battle slice wakeups (slices 3,951→8,300, all minted while the battle frame lives, ≤ 1,900
  game-s here) — physics counts are conserved (kicks +0.6%, boundaries +0.5% over 5,400 s).
- **Total engine CPU fell:** summed per-frame engine ms over the identical 3,300 frames: OFF
  1,560.3 ms, chain+stagger 1,384.5 ms (−11%); engine p99 5.45→2.04 ms, p50 0.026→0.254 ms.
- Envelope (max events per 500-frame slice, 5,400 game-s): off `212 240 207 251 229 195 334`
  (standing, non-decaying); chain+stagger `52 27 26 12 13 13 12` (floor after the first 500 —
  no grid left to re-anchor to).
- CHAIN alone is **inert** for one-tick births (228 vs 240, same class): the anchor only matters
  after an off-grid event; it is a coincidence *re-manufacturer*, not the source.
- STAGGER alone is re-absorbed (210/139, comb re-formed) — reproducing 4c22's ES_LOCAL_STAGGER.

Digests (`ladder_digest`, 4 schedules each — unlimited, 25 ev/frame, 4 threads, 3 ms wall):

- Patched **OFF = pristine main bit for bit** (built at b07f5a0b before the patch; `N=1000 coast`
  6895ce06… = 6895ce06…, kicks 3,767 = 3,767; all 11 cases one digest on every schedule).
- Every arm keeps **one digest across all 4 schedules** on coast, through-the-wave and
  belt-crossing cases (the tie rule holds under the chained law); arm digests differ from OFF, as
  a law change must (chain 27d28007…, stagger de3c14c1…, chain+stagger a5e2bcde… on N=1000 coast).

Commands (each ≤ 60 s; from the repo root, binary at `$CARGO_TARGET_DIR/release/examples/`):

```
cargo build --release -p emergent-universe --example nladder --example ladder_digest
nladder 1000 coast 20 100 1000000                        # off arm, table row 1
ES_CHAIN=1 nladder 1000 coast 20 100 1000000             # chain arm
ES_LOCAL_STAGGER=1 nladder 1000 coast 20 100 1000000     # stagger arm
ES_CHAIN=1 ES_LOCAL_STAGGER=1 nladder 1000 coast 20 100 1000000
ES_CHAIN=1 ES_LOCAL_STAGGER=1 ES_DUMP=d.csv nladder 1000 coast 55 100 1000000   # long + envelope
nladder 0 coast 20 100 1000000 ; nladder 600 coast 20 100 1000000 ; nladder 10000 coast 20 100 1000000
ladder_digest                       # off: all 11 cases, 4 schedules agree, = pristine
ES_CHAIN=1 ES_LOCAL_STAGGER=1 ladder_digest "N=1000 coast"
```

`regen.sh` runs all of it and prints the table (≈ 8 min including the full digest pass).

## Predictions

All written before any flight ([predictions.md](predictions.md)). Held: P1 (OFF reproduces the
record: 334/136 at 5,400 s, N=0 floor 51), P2 (stagger re-absorbed), P3 (chain inert at coast —
though its digest is **not** identical: fleet-handout bodies are born off-grid at `l.tick`, so
four fewer kicks land by the cut; the stats-level claim held, the "may be identical" hedge did
not), P4's collapse (52 ≤ 90, p99 24 ≤ 40, N-flat) and P5 (no re-formation). **P4's event-total
halves both broke and held:** the total is +20%, not the predicted +5% — but it is a bounded
early slice excess with zero steady-state rate and −11% total CPU, which the prediction's intent
(no permanent stream price, beating ES_LOCAL_PHASE's +19–41%) is confirmed on; the letter of the
+5% was wrong. P6 (held-out N=10⁴ ≤ 90): held at 50.

## What would make it wrong

1. **The legality gates are unflown.** Both the chained law and ES_LOCAL_PHASE give up law.md's
   "every pair of bodies shares boundaries" (block time steps). B13/B14-class gates under shifted
   boundaries must fly before adoption — the same debt 4c22 left, not a new one. Determinism
   across schedules did hold everywhere flown.
2. **A long-lived fleet battle keeps paying the slice excess.** Here the battle dissolves by
   ~1,900 game-s, so the +4.4k slices are one-time; a battle that never dissolves wakes once per
   worked frame, and at 10⁶ with dense streams that is every frame — the price becomes a rate.
   Unmeasured (no such scene in the ladder).
3. Coast-only, seed 1, threads 1: the burn arm (4c22's checker: 27% residue, d0 carries 40
   events) and other seeds are unflown here.
4. The workspace test suite was not run; the OFF arm's bit-identity to pristine main (digest
   control) is the evidence that default behavior is untouched.

## Cost of adoption, and fit

Cost: the `aligned` snap becomes `step` (one branch), plus a birth-spread term already shaped
like the belt stagger; the pair-shared-boundary sentence in law.md is rewritten; B13/B14-class
gates flown before merge. Fit: principle 12 — "minimize spike compute and average compute usage
so that you get a bigger simulation that runs smoothly" (p99 5.45→2.04 ms, max 334→52, total CPU
−11%); principle 19 — "a fix signals the wrong representation": ES_LOCAL_PHASE was a fix on top
of the anchor; the anchor was the wrong representation; principle 22 — "the simulation tells us
what's next not us": the spread lands where the fleet already pays a wakeup, not on a metronome.

## The lens

The whole-system read: two mechanisms that were secretly one and a half — the clock law chains,
the block law re-anchors, and every frame cure shipped so far (the belt stagger, the proposed
per-body phase) patches the population that the re-anchor victimises. What this lens may have
missed: the hard special case is the long-lived battle (point 2 above), where spreading events
onto more frames multiplies a *shared* entity's wakeups — the unification is only free while
battles dissolve; and the comb's collapse was verified on frame statistics, not on the behaviour
gates, so the physics debt is carried, not paid.
