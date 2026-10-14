# Dossier — 20261014-1719-second-20261014-1631-taleb-6138-4487 (second author on taleb-6138)

**Claim.** The checker's named gold experiment, done: the run's own named fix — hold the player's
scan when the ship backlog it would read exceeds a threshold, so the pull never runs on a saturated
queue — is implemented in the engine's idiom (`work/patch.diff`, one crate file and the two flight
instruments), it **deletes the wave's freeze at every N tested (worst frame 315→37.7 ms at 10⁵,
1,213→90.3 ms at 2×10⁵ seed 1 and 1,244→81.4 ms seed 2, the M1 record's 1,280→123.8 ms at 3×10⁵,
which landed inside this box's 2 GB cap at 1,705 MB peak), and it is bit-exact wherever the cut is
canonical**: `frame_digest`'s 8 scripted flights × 4 schedules give one digest pristine = fixed =
every-pull-forced, and the belt flights agree to the digit at the post-wave cut (digest, kicks,
events, encounters) — the freeze bought no bits.

**Bottleneck.** The furthest-gap line's F1 (bodies: 10⁵–3×10⁵ certified, 10⁹ wanted): the wave
turned the certification into 1.2 s single frames; the fix moves the wave's resolution into the
frame-budgeted drain in the pull's own key order, so the certification window extends from "20 s
coasting" to "past the first wave under burn" at bounded frames. What it deletes: the unbudgeted
item itself. Gain: ~13× on the worst frame at 2×10⁵, ~10× at 3×10⁵, events/frame max 24,467→333;
adoption is one patch, no new state machines (a 64-item slice, a drain pass, a waiting scan).

**Evidence** (shipped main `9fcae60f` + `work/patch.diff`; Linux 8 vCPU shared, load 1–3, 11–14 GB
free; every command ≤ 60 s wall except the flights, 30–55 s each; `regen.sh` regenerates all of it
in ~12 min; `table.py` prints the tables below from `raw/`):

- **The fix** (`crates/universe/src/universe.rs`): `pull_ships` gains a cap — the player's in-root
  item resolves at most `PULL_HOLD = 64` ship items; over that, the key goes to `held_pulls` and the
  scan becomes a `Waiting` entry; `advance` drains one held item a pass behind the same
  `spent_before` gate as any other item (key order, the pull's own); a `Waiting` scan captures only
  when the ship lane is clear of its key (`answer_front`, the digest's fold, both live-checked), so
  it reads exactly the state the whole pull would have left. The children-only pull (player out of
  the root doll) is untouched. `set_pull_hold` (doc-hidden) forces the hold to 0 for the control.
- **Frames** (200 s wall flights, rtf 100, budget 12 ms, seed 1 unless said):

  | arm | pristine max ms | fixed max ms | fixed over | ev/frame max | wave region worst (fixed) |
  |---|---|---|---|---|---|
  | 10⁵ burn | 315.2 | **37.7** | 20 | — | 11.94 ms |
  | 2×10⁵ burn s1 | 1,213.1 (1,358.8 rerun) | **90.3** | 15 | **333** (was 24,467) | 11.94 ms |
  | 2×10⁵ burn s2 | 1,244.5 | **81.4** | 12 | 633 | 11.96 ms |
  | 2×10⁵ coast s1 | 12.0 | **11.97, 0 over** | 0 | — | 11.90 ms |
  | 3×10⁵ burn s1 | 1,280 (M1 record, quoted) | **123.8** | 11 | 333 | 11.95 ms |

  The wave region (frames 8,300–8,799) now runs at the budget-saturated drain (11.9 ms, ~235 events
  a frame), the coast control's exact shape; the overload appears as 1.667 s of lag, recovered after
  the wave; refusals 0, dead 0, the freeze does not ratchet (6138's P6, unchanged). The **worst
  frames are now the second seam** (1 event each, every ~50 frames, burn only): 37.7/90.3/123.8 ms
  at 1/2/3×10⁵ — it grows with N and is now F1's binding failure; the fix does not touch it (open
  direction 0, with a2c1's walk-all and cap as the named suspects).
- **Bit-exactness.** (a) `frame_digest` 20 (the shipped harness): 8 scripted flights, 4 schedules
  each, digests identical across pristine / fixed / `FORCE_HOLD=1` (every in-root pull held) — and
  each agrees across its schedules. (b) Belt flights, deterministic budget (25 events a frame; see
  the caveat below), 2×10⁵ burn s1, settled to canonical cuts: **21,000 game-s: `ae06c773…`,
  kicks 233,600, events 473,200, encounters 7,356 — identical to the digit**; 16,000 game-s: differs
  (fixed holds 11,473 fewer resolved events there — the drain's unfinished share at a mid-drain cut).
  (c) N=2,000 wall (the deferral engages, `held_max` 188): identical at cuts 12,000/16,000/21,000.
  (d) Coast 2×10⁵ wall: identical at both cuts (the fix never engages; the control is end-to-end
  clean).
- **The instrument caveat, found and controlled.** Two pristine 2×10⁵ wall-budgeted burn flights of
  shipped main (same seed, same binary) differ from each other at both cuts (`f6869cbb…` vs
  `02570fef…` at 16,000; `cac5f723…` vs `33b794aa…` at 21,000): **the wall-budgeted belt flight's
  digest is not schedule-stable on main** at this scale, so belt digests compare only under a
  deterministic budget — which is why (b) uses `NLADDER_EBUDGET=25` (added by this run's patch).
  This is a finding about the certificate's domain, not a product of the fix.

**Predictions** (`predictions.md`, written before any patched flight): F1 held (90.3 < the 100 ms
kill; the <25 ms point estimate missed — the residue is the second seam, not the wave: the wave
region itself is 11.94 ms). F2 held (333 ≤ 2,000). F3 held for the wave (lag 1.667 s ≥ 1.0,
recovered; the "frames under 12 by 190–200 s" clause trips on the second seam's 1-event frames —
the prediction's wording did not separate the seams). F4 held (8/8 flights, default and forced).
F5 held at the post-drain cut and everywhere the instrument is stable; the mid-drain cut (16,000)
differs by the drain's unfinished share — disclosed, not hidden; the death-window residual never
fired as an attributable case (the 21,000 cut's bit-identity rules out any state divergence). F6
held (473,200 == 473,200 events at 21,000; in-flight within 0.6%). F7 held (coast bit-identical,
0 over; 10⁵'s <20 ms point estimate missed — the second seam again, 37.7 ms). F8 resolved without
the kill: 3×10⁵ ran inside the cap.

**What would make it wrong.** The mid-drain cut: a digest taken while a held key remains below the
cut reflects the drain's pace, so a rung that cuts mid-wave sees different canonical states — the
rung writer must cut past the drain (or the settle drains first, which it does; the residual is the
flight's own pace at the moment of the cut). The second seam is unfixable by this change and now
binds F1 at every N: 3×10⁵'s 123.8 ms would fail a 12 ms-smoothness gate as surely as the wave did,
one event at a time. The frame_digest forced arm may be vacuous on flights whose player never sits
in the root doll with ship backlog (engagement is proven on the belt arms, not the scripted ones).
Cost of adopting: one crate patch, no new standing state (a `VecDeque` of keys, ≤ one per player
item), the common path unchanged below 64 due items — and the M1 re-measure remains the
integrator's.

**Fit with PRINCIPLES.** #12 verbatim — "the algorithm that allocates the work to prevent those
heavy tails, it's the most important one": the pull was a heavy tail hiding inside one unbudgeted
item; the fix is allocation, not a law change. #5 (priority is slack, not proximity: the drain runs
the oldest held key first). #19 (one law at every scale: the held pull is the same pull, sliced;
the scan is the same scan, waited — no regime switch, only a threshold on backlog). #13 (errors
never compound: bit-identity at the canonical cuts is the certificate, and it holds).

**The lens (second author).** What it may have missed: the honest reading of the 16,000-cut
divergence took three probes (wall A/B, N=2,000, deterministic budget) to pin as the instrument's,
and the attribution "the drain's unfinished share" is arithmetic (11,473 events), not per-item
instrumentation; and the second seam's growth (37.7→90.3→123.8) is three points, unmodelled.

## Commands (each ≤ 60 s wall; full regen ≤ 15 min: `regen.sh`)

    $P/frame_digest 20                                   # pristine; $F for fixed; FORCE_HOLD=1 $F/…
    NLADDER_MAX_S=260 NLADDER_TRACE=1 NLADDER_DIGEST=16000,21000 \
        <target>/nladder 200000 burn 200 100             # each arm; NLADDER_SEED=2; coast; 100000;
                                                         # 300000 (NLADDER_DIGEST=21000)
    NLADDER_MAX_S=400 NLADDER_EBUDGET=25 NLADDER_DIGEST=16000,21000 \
        <target>/nladder 200000 burn 200 100             # the deterministic digest comparison
    python3 table.py                                     # the tables above
