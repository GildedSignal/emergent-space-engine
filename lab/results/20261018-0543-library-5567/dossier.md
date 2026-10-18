# Dossier — 20261018-0543-library-5567 (library lens)

## Claim

The 10⁹ encounters **fleet row (4,510 cores at F = 10⁵ fleets, 99.77% of cf2a's composed
ledger) is an artifact of carrying formations as compact belt bodies: the plane already ships
the formation's native carrier — the Fermi-frame fleet (`crates/universe/src/fleet.rs`) — and
on it the same population prices at ≤ ~1 core; the "fleet-scale finder" requirement never
exists** (cf2a's own checker named the route "a shipped alternative route this run does not
price at 10⁹"; this run prices it).

## Bottleneck

Board #2 (encounters at 10⁹, ~10³–10⁴ cores → a few). The fleet row was 99.77% of the
composed 10⁹ CPU ledger; killing it removes ~4.5×10³ of the 4.5×10³-core headline and deletes
the planned rank-certificate/phase-neighbour finder for concentrated populations (adopted in
design, not shipped — it is now needed only if tight formations are carried as belt bodies,
which they should not be).

## Evidence (all commands ≤ 60 s after one ~90 s build; this shared Linux box, 8 vCPU)

Shipped code + one env-gated CLI line (`work/patch.diff`: `--members` cap 400 → `ES_MEMBERS_CAP`);
flights `xtask universe --bench --members M --seconds 20 --rtf 100 --unpaced --no-record`
(1,200 frames ≈ 2,000 game-s; the fleet's own class in the report's `engine_cost_by_kind`,
"fleet"; logs in `work/flights/`):

| arm | fleet class | slices | µs/slice | leavers | lost | dissolved |
|---|---|---|---|---|---|---|
| seed 1, m=48 | 85.3 ms | 3,931 | 21.7 | 43 | 21 | 0 |
| seed 1, m=192 | 207.0 ms | 9,420 | 22.0 | 182 | 78 | 0 |
| seed 1, m=768 | 679.9 ms | 13,500 | 50.4 | 768 | 403 | **1** |
| seed 7, m=48 (held out) | 125.6 ms | 4,579 | 27.4 | 42 | 23 | 0 |
| seed 7, m=192 (held out) | 274.2 ms | 7,248 | 37.8 | 192 | 84 | **1** |

1. **Per-member rate, low orbit (the only shipped fleet scene, the Armada at 7,000 km about
   Home):** 85.3 ms / (48 × 2,000 game-s) = **0.89 µs per member per game-second** (an upper
   blend: it includes the 43 leaver hand-outs; the in-frame population decays from 48). P2
   (0.1–10 µs) held.
2. **Scaling while the frame holds:** ×4 members (48→192) costs ×2.43 total (exponent 0.65);
   the **per-slice cost is member-flat (21.7 → 22.0 µs)** — the EventCore (`Order::Sparse`,
   the plane's shipped order) charges events, not members, and its contact batch is binned
   (`lattice-metal`: counting sort into spatial buckets, pairs only between adjacent cells).
   P1 held (kill was ≥1.5).
3. **The domain boundary, measured:** the frame's extent rule `r_p/32` (frame.rs:80) is the
   representation's edge. Seed 1 holds at 192 and dissolves at 768 (768/768 handed out); seed 7
   dissolves by 192. Dissolution hands everyone to the doll as ships (ship class 1,345 → 19,699
   items) — the tier's ruin regime (taleb-09b5) is exactly what the frame refuses to hold.
   taleb-09b5's tight formation is inside; the L4/L5 quarter (spread ~0.25 R_H) is not.
4. **The 10⁹ composition:** epochs per period are scale-free (1,600–3,200 at any radius,
   frame.rs:37, the E3-measured `ω·E ≤ 2⁻⁸` rule), so a heliocentric formation at 2 AU
   (P = year vs the Armada's ≈5.2×10³ s) runs its member events at ×1.65×10⁻⁴ the low-orbit
   rate: 0.89 µs × 1.65×10⁻⁴ ≈ 0.15 ns/member/game-s ⇒ **~0.15 cores** of member events at
   10⁹ members, **~0.8 cores** of per-epoch batch scans (10⁵ fleets × 7.6×10⁻⁵ epoch/s × 10⁴
   members × ~10 ns), **1.8×10⁻⁴ cores** of origins (10⁵ tubes at the belt stream 3.55×10⁻⁵
   ev/B/game-s). **≤ ~1 core against 4,510: ≥ 4,500×.** P3 held. [INFERENCE: the composition
   is arithmetic on the measured scale-free epoch law; a doll-0 frame about the star is not
   flown — the wiring for it is named below.]
5. **Wiring debts, code-verified:** one fleet per universe (`add_fleet` asserts,
   universe.rs:513 — many fleets need id ranges); the player's loop runs *every* fleet to the
   player's tick (universe.rs:733–737 — needs a doll filter at F = 10⁵); a heliocentric frame
   is doll 0 with the star's mass (`Fleet::new` takes any doll; `boundary()` already checks
   the secondaries' shells). Distant battles are already capped by light-delayed deadlines
   (universe.rs:787: committed tick never passes the next entity's deadline minus distance).
6. Quotes 5/5 byte-identical against the 4,590-highlight cache (`verify_quotes.py`; fresh
   Readwise export in `work/`).
7. **Regen:** `regen.sh` (37 s end-to-end) reproduces every count (leavers, lost, dissolved;
   kicks within ±3 — the decision-tick dependence 16ec measured) with per-slice timings inside
   the shared box's load wobble (17.7–27.4 µs/slice at seed 7, m = 48); counts are the
   instrument, timings the order of magnitude.

## Predictions

`predictions.md` was written before the flights. P1 held (0.65 < 1.2 kill bar); P2 held
(0.89 µs); P3 held by composition (≤ ~1 core ≤ 10); P4's debts verified in code. The held-out
seed 7 reproduced the structure and moved the dissolution threshold down (192 vs 768) — the
domain is spread-dependent, not member-count-dependent, which is the extent rule's signature.

## What would make it wrong

A flown heliocentric (doll-0) frame whose per-member cost leaves the low-orbit class — the
tide coefficient changes (star at 2 AU vs planet at 7,000 km) though the kick arithmetic does
not; or the EventCore's per-epoch cost at m = 10⁴ per fleet exceeding ~10 µs/epoch/member-flat
(the m = 48→192 flights say it is member-flat at ~22 µs/slice, but no arm flew m > 768 held).
If either fails, the row falls back toward the low-orbit rate × period ratio, and it is still
~×6 below 4,510 cores. **Cost of adoption:** the three wiring items in (5) plus a birth rule
that carries tight formations as fleets instead of belt bodies — no new finder, no law change
(the frame is shipped and digested). **Fit:** PRINCIPLES 4 "Everything is emergent. No central
control and no categories: regimes are chosen by dimensionless numbers" — the extent rule is
the dimensionless gate between frame and belt-body regimes; and 26 "This is a solved problem
elsewhere for sure" — the solved problem was in our own tree.

## The lens (what it may have missed)

The library lens reaches for the practitioner rule and risks pricing the world by analogy; the
numbers here are one scene (low orbit), one law order, and an unflown composition step. It
also did not price frame members' *memory* at 10⁹ (6793's plateau is per live body; frame
members are lattice bodies — that census is a named next run), nor the many-fleet queue's
deadline behaviour under load.

## The five lessons (each changed a decision this run)

1. **Musk, via Isaacson — "Step one should be to question the requirements… Make them less
   wrong and dumb… And then delete, delete, delete."** Mechanism: the row priced a requirement
   (find 49-m contacts between fleet members) the plane's representation deletes. Change: the
   encounters queue's fleet rung is retired, not built. Cheapest test: this run's flights.
2. **Musk, via Isaacson — "It's not the product that leads to success… It's about building the
   machine that builds the machine."** Mechanism: a 10⁹ ledger composed from one crate prices
   the hand tool, not the machine; the machine had another route shipped. Change: composed
   ledgers must price every shipped route to the answer (the same lesson as the 5 October memo
   artifact, now for cost). Test: this recomposition.
3. **Farnam Street — "to a man with a hammer, every problem looks like a nail."** Mechanism:
   the belt body was the hammer; concentrated populations are nails it bends. Change: the
   birth rule chooses frame vs belt by the extent number. Test: the m=768/seed-7-192
   dissolution flights (the hammer's measured edge).
4. **Lenny's Newsletter — "increasing engagement with existing key features is more impactful
   than launching new features."** Mechanism: three small wirings unlock a shipped carrier;
   the designed rank certificate stays unwired. Change: wire fleets (id ranges, doll filter,
   doll-0 birth) before building any finder. Test: a many-fleet birth probe (next run).
5. **Farnam Street, Power Laws — "the behavior of the system differs from the simple addition
   of its parts. This characteristic is called emergent behavior."** Mechanism: a formation's
   10⁹ cost is not 10⁴ × a body's cost; it is one origin's stream plus epoch batches. Change:
   compose the ledger per population unit, never per body summed. Test: the ≤ ~1-core row.
