# Root-clock event keys (the motion law v2, step 4)

## Claim

The queue's canonical key is now each event's exact image on the root clock — its doll tick plus the
doll chain's integer simultaneity shear `sinh(η)·x̂_axis` (frozen per entity when its own item
resolves) — so a relativistic doll orders its events correctly and "one tick is the same physical time
in every doll" is deleted; measured, the plane's own Moon's key moves by −25 ticks, a 0.5 c doll's
1,000 members' keys spread ±8,314 ticks, and every gate holds (B8's whole suite green, B13's detail
line bit-identical, B17 unchanged).

## Bottleneck

HANDOFF's risk "simultaneity across dolls" and the queue item "root-clock event keys" (the memo §5
step 4). It unblocks relativistic dolls at all: without it, a doll at 0.5 c orders events that are up
to thousands of ticks apart in root time as simultaneous, and the canonical cut and the tie rule
(law.md: "events at the same root-clock time") are wrong for every fast doll. No order-of-magnitude
compute gain is claimed; what it deletes is a wrong convention, and it costs ~one centre readout plus
one `Frame::of` per child-doll entity per event (root-doll entities: zero — the map is the identity
and is skipped).

## Evidence

Machine: the lab's Linux box (8 vCPU, shared; `machine_state` lines in the work logs), release
builds, no other load run by me. Every command ≤ 60 s except the suite and B17, noted.

**The mechanism** (`work/patch.diff`, 5 files + the test):

- `lorentz.rs`: `Frame::shear_time` — the boost's own coefficient (`bb = −sinh η·2^N`) applied to the
  event's position rotated onto the motion: the inverse boost's `t` row with the diagonal (the
  centre's time dilation) anchored away, so a centre's own events keep their ticks and a centre at
  rest changes nothing. The same shears as the handoff's, exactly invertible in integers.
- `ctx.rs`: `Ctx::root_offset` — the chain walk, all edges accumulated at 2^-64 tick and rounded
  once; position carried up Galilean (the boost's spatial part is O(β²); no depth-2 doll exists).
- `universe.rs`: the key `(t_root, id, kind)`, frozen in `root_key[e]` at `requeue` **and refreshed
  in `apply`** (a pull resolves bodies outside `resolve_entity`; a stale frozen key there spun the
  plane's ship lane forever — found by probe, fixed, both runs in the logs' history). The canonical
  cut (`advance`'s `target`) is now a root-clock time. The player's decisions, the fleet gate and the
  hand-out gate stay on the player's doll clock, as before.
- `fleet.rs`: the frame's members keep the frame's clock — the battle is one entity, keyed by its
  origin's event through the doll chain.

**P6** (`cargo test --release -p emergent-universe --test rootkeys`, 0.9 s): a planet crossing the
system at 0.5 c (a state-made passage tube — `retune` now lets a body made from an exact state be a
doll's centre), 1,000 members spread over the doll. Every member's next event's key equals the shear
image recomputed independently in floats from the member's position and the planet's velocity: worst
miss 0.500 of a tick (the map's rounding), key offsets −8,314..+6,002 ticks, and each member's whole
history is the identical record under 1, 4 and 8 threads and both orders of making the members
(`work/p6-out.txt`). The order test: two members on one circle of the doll, ahead and behind the
motion, their plans on the same doll ticks (16,384); at a cut between their root keys the behind
one's item has resolved and the ahead one's has not. **Control** (in the run log): with the key
forced to the identity (the old convention) both tests fail — member 1 off by −110.5 ticks, the pair
tied at 16,384.

**The real plane** (`work/rootkey-plane.txt`, ~8 s): after 5×10^6 ticks, the Moon's key offset −25
ticks, Skimmer 1 +1, an orbiter and the player 0 (rounded) — the plane builder's 15–1,400-tick
finding enters the canonical order at its measured size, and nothing else moves.

**Gates, both ways** (`work/gates-before.txt`, `work/gates-after.txt`, ~100 s each):

- B13 before: `FAIL assists: 60/64 judged flybys within 1e-2 …, worst ΔE 2.12e-2 ΔL 2.12e-2; 0 of 64
  excluded; 9 draws replaced…` — after: the **identical line** (worst and draws included). Expected:
  its ships live in the root doll, whose image is the identity.
- B17 before: `FAIL timeout: 60.1 s over the 60 s limit` — after: `FAIL timeout: 60.0 s`. This box
  cannot run B17 inside the gate's minute (the M1 passes it, H0215); before/after agree.
- B8 (`cargo test --release -p emergent-universe`, 268 s before, 247 s after, `work/b8-*.txt`): all
  56 tests green both ways — every digest comparison (budgets, threads 1–8, both battle orders,
  replays, throttle) still gives one digest per cut with the new keys in.

## Predictions

`predictions.md` was written before the gate runs. All five held: B13's detail line identical, B17
the same timeout, the suite green with digests changed-but-self-consistent (centres' tubes frozen
across every test horizon — the planets' first kick is ~10^10 ticks out; the largest horizon,
5×10^14, is a one-planet scene with no forces), wall time within ±10 % (−8 %), and the control fails
as stated.

## What would make it wrong; the cost of adopting; the fit

- **Wrong if** the frozen key's inputs were not schedule-invariant. A body's own binding is fixed
  between its items; the one mutable input is the doll centre's tube, which changes only at the
  centre's kicks (~10^10 ticks apart in the plane; never inside any test). When one lands between two
  schedules' key computations, the key can wobble by `x·Δw` ≈ 10^-4 tick — visible only if it
  straddles a rounding boundary. The same applies to a same-doll source whose item sits inside the
  δ-gap of a reader (the Moon is the only such source; its cadence, 3×10^9 ticks, is far beyond the
  26-tick gap at every test scale). Both close properly with step 5's causal reads: reading a source
  at the tick whose root image equals the reader's makes the pull discipline exact by construction.
  Until then the law reads a doll's sources at the reader's doll tick (Galilean inside the doll,
  bounded by the doll's shear spread) — the memo leaves exactly this for R5's cursor.
- **Cost:** ~150 lines; per child-doll entity per event one extra centre readout and one `Frame::of`
  (a square root); root-doll entities (the planets, every B12/B13/B17 ship, most of the plane) add
  nothing — measured as the suite's time, not modelled.
- **Fit:** law.md already said it — "Events at the same root-clock time… the queue's key is (time,
  smallest body id, kind)" and "Handoffs are Lorentz… Open: a boost also maps event times". This
  closes that Open the way PRINCIPLES 7 asks ("Spacetime, not space plus time") without adding a
  stored field: the image is derived, exact in integers ("Exact means deterministic and
  reproducible", principle 2), and floats appear only in the test's oracle.

## The lens

A directed build trusts the memo's scoping, and the memo scoped this to the key. The deeper question
the work exposed — which tick a reader reads a same-doll source at when their shears differ — is
step 5's, and I left the read rule alone rather than half-close it; a reader from inside a moving
doll still reads its doll's sources at its own doll tick (an error bounded by the doll's shear
spread, zero for the root doll). I also did not touch the digest's contents (the key is derived, not
state), and the Fermi frame's own motion relative to its doll (its phase 2) is untouched: the frame
is keyed by its origin's doll event only. Two smaller things the lens may have biased me to keep:
the Galilean position carry-up the chain (no depth-2 doll exists to test it) and the relaxed `retune`
(a passage can now be a doll's centre — a capability, adopted for the test, that the integrator may
want to look at separately).
