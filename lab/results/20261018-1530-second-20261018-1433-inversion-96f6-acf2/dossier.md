# Dossier — 20261018-1530-second-…-inversion-96f6-acf2 (second author on inversion-96f6)

**Claim.** The pin behind the crowd's "pending the observer fix" is now measured directly —
Drop-counted distinct `Arc<Scan>`s, not inferred from hwm — and the three walls re-rank with two
corrections: the multiplier is the **mint count** (0.0526 mints/game-s, K-flat and constant over
3,900 game-s; alive == mints in every flight — the latch freeze drops nothing; deque entries run
1.9–2.0× distinct), the pin is an **unbounded linear time wall** whose law is exact —
bytes_touched(t) = 0.0526·game_s·(K+38)·224 B (identity 0.997–0.999 over 7 flights), so 8 GB at
13,700 game-s at 5×10⁴ but at **687 game-s (≈7 wall-seconds at rtf 100) at the fix's own 10⁶
target**, and at ~1 game-s at 10⁹ — and the fix's compare-form re-flown natively is **0.50–0.53
ns/member** (12 ms at K ≈ 2.3×10⁷), 40× under b083's 19.2 ns/member REPLICA, so it is NOT
co-located with the pin: **the pin stands alone between the capture walk (~6×10⁴) and everything
else, and the fix's requirement is answer-or-expire held scans** — a clause neither b083's nor
5f36's letter carries.

**Bottleneck.** The board's #1 (bodies: 28 vs 10⁹). This closes the record's gap exactly as the
checker named: the ~30-distinct hwm fit is superseded by the direct count (40–51 at 600 frames),
the ×held multiplier is dead, and the pin's price at the fix's target scale is now a measured
sentence — at 10⁶ ships the store-grounded fix busts 8 GB in ~11 wall-seconds of play unless it
expires or answers held scans; deleting the candidates Vec alone (the letter's clause) does not
stop the mint, because the mint's trigger is the player's own clock (census: t 521/573, len 52,
body/interval/me/content **0** — binding content never differs; the crowd is static tubes under
ES_SECULAR).

**Evidence** (96f6's scanprobe verbatim + this run's print-only additions: the pinstat registry —
a `Drop` impl on `Scan` decrementing alive/bytes, `mint(len, cap)` at the one allocation site —
the trigger census in `same_inputs`, `ES_PIN` per-frame rows, `ES_WALL`, and the native
phase-compare bench; composed arm `ES_SECULAR+ES_CHAIN+ES_LOCAL_STAGGER`, coast seed 1 rtf 100,
12-ms budget; `regen.sh` regenerates all of it in ~3 min; `analyze.py` prints every table):

Table 1 — the K-trend, pin columns (600 frames; digests equal 96f6's record at every K):

| K | mints | reuses | held_max | alive_end | touched MB | alloc MB | hwm MB | B/mint | (K+38)·224 | digest |
|---|---|---|---|---|---|---|---|---|---|---|
| 10,028 | 51 | 36 | 97 | 51 (=mints) | 114.7 | 187.2 | 159 | 2.25e6 | 2.25e6 | 1b5461b0 ✓ |
| 20,028 | 50 | 37 | 97 | 50 | 224.4 | 367.0 | 302 | 4.49e6 | 4.49e6 | ac9d2e1a ✓ |
| 30,028 | 48 | 39 | 97 | 48 | 323.0 | 352.3 | 441 | 6.73e6 | 6.73e6 | c7f47c26 ✓ |
| 50,028 | 40 | 33 | 81 | 40 | 448.3 | 587.2 | 637 | 1.12e7 | 1.12e7 | 58bcbb0c ✓ |

Bytes per mint = (K+38)·224 B touched exactly (the true tuple is 224 B, not 96f6's printed 216 —
a one-line correction to `scanstat::candidate_bytes`, which sums field sizes without the tuple's
alignment); ×1.09–1.63 by capacity (the Vec's doubling headroom — allocation, not resident);
VmHWM = touched + 44–190 MB rest at every flight (159/302/441/637 MB).

Table 2 — the time wall at fixed K (alive == mints in every flight: zero drops over 3,900 game-s;
held_max ≈ 1.9–2.0× alive — entries are not objects, the 5-October lesson now counted both sides):

| flight | frames | game_s | mints | held_max | touched MB | hwm MB | mints/game-s |
|---|---|---|---|---|---|---|---|
| 50k long | 1,200 | 1,578.7 | 83 | 161 | 930.3 | 1,121 | 0.0526 |
| 30k long | 1,200 | 1,899.2 | 100 | 194 | 672.8 | 793 | 0.0527 |
| 10k long | 2,400 | 3,898.5 | 201 | 387 | 451.7 | 503 | 0.0516 |

The checker's hwm inferences all land: ~6 MB/arrival-touched at 50k (measured 930.3/153 ≈ 6.1),
637→1,121 MB over the second window (measured 448.3→930.3 touched + rest), "~13,000 game-s to
8 GB" (measured law: 13,718). Their "~30 distinct" was the fit's error: the direct count is
40–51 at 600 frames.

Table 3 — the walls re-ranked, every constant now measured on this scene:
1. **Capture walk** (unchanged): 190–205 ns/body ⇒ 12 ms at K ≈ 6×10⁴.
2. **The pin** (corrected): 0.0526 mints/game-s × (K+38)·224 B ⇒ 8 GB at K·t ≈ 7.2×10⁸
   game-s·bodies: 68,000 game-s at 10⁴, 13,700 at 5×10⁴, 687 at 10⁶, ~1 at 10⁹. SCAN_BACKLOG
   (2048 entries ≈ 1,050 mints) binds before 8 GB only under K ≲ 1.7×10⁴ (2.4 GB at 10⁴) — and
   then converts the pin into forced O(K) answers (~19–44 ms at 10⁴) inside the budget: both
   branches ruin, and neither is expiry.
3. **Compare-form** (corrected, native): 0.50–0.53 ns/member at 10⁴–10⁶ ⇒ 12 ms at
   K ≈ 2.3×10⁷ — b083's 19.2 ns/member was numpy per-element overhead (~40×), so the
   "co-located at ~6–7×10⁵" ranking is dead; nothing binds between the pin and 2.3×10⁷.

Trigger census (aggregate, 573 mints): **t = 521, len = 52, body = interval = me = content = 0.**
The capture's trigger is the player's own event clock (84–92%) and head-count flips (membership
changes: births/leavers), never binding content — the question 96f6's lens admitted leaving
uncounted, now named.

**Predictions** (`predictions.md`, written before the flights): P1 held (mints/captures 0.53–0.59
in the 0.5–0.7 band; alive == mints at every K; the exact (K+38)·224 law — including the 224-vs-216
correction); P2 held (slope 0.589 MB/game-s at 50k, inside 0.5–0.8; 8 GB at 13,718 game-s — my
band said 8–12×10³, the measured law lands just above its top, 3% over: the honest miss);
P3 held (0.5 ns ≤ 1, 40× under the REPLICA, wall 3 vanishes); P4 held bit-exactly (all four
digests, kicks/events/game_s/census identical to 96f6's record).

**What would make it wrong.** Coast, seed 1, one scene shape (as 96f6): the mint rate 0.0526 is
the coast player's item cadence — a burn or doll handoff raises the t-mints and every time-wall
number scales with it (the K-law is untouched). The 50k rows are deadline-coupled through game_s
(mints 40 vs ~48 at full rate — the disclosed slide, now quantified by the rate law). The bench
is the sorted-store sequential scan the fix would ship; a random-access store or per-member sin
would raise it (still ≪ the walk it replaces), and the store's maintenance cost on crowd churn
(insert/remove per binding change) is unmeasured — the fix's real remaining unknown. Adoption
cost: none — this prices the fix's required shape (answer-or-expire; the TTL or bounded-mint
window is the design clause to add). Fit: PRINCIPLES 13 ("errors never compound" — the pin is
memory compounding per arrival with no decay path under the freeze) and P1 ("the cheapest compute
is compute not done" — 573/573 mints died unanswered in-window: the capture walk was paid, the
candidates pinned, and the answer deferred to the digest, for nothing the player saw).

**The lens.** Second author: the checker's named experiment done in full — the pin measured
directly (distinct Arcs, bytes both ways, three K, three window lengths), the walls re-ranked on
measured constants, and the compare-form re-flown natively. What this lens may have missed: the
burn-scene mint rate (the one dial that moves every time-wall number), the store's maintenance
cost under churn, and whether an expiry clause changes the digest record (an answered-late scan
logs the same encounters — the freeze's deferral is digest-invariant by construction, but an
*expired* scan logs nothing, which is a law change to fly before adoption).
