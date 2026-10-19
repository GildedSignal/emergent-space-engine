# Dossier — 20261019-1452-taleb-527a (taleb)

**Claim.** 1b3f's per-reader `oldest` rule does not touch 4447's interstellar burn-mode memory
ratchet — measured identical to the digit through both of the ratchet's channels — and the
ratchet's mid-flight channel is the scan deque itself, whose `SCAN_BACKLOG=2048` fence is sized
on a stale "about 10 KB each" premise that is K-linear wrong (measured 60–95 B × doll
population per scan), so the fence licenses 5.6 GB at K=3×10⁴ and 19.4 GB at 10⁵ and never
engages before the memory budget dies; the wiki's two conflicting same-day entries are two
real, independent channels, and neither's fix cures the other's.

**Bottleneck.** The board's memory-at-10⁹ line and the allocator's ruin list: 4447 measured the
unbounded burn-mode ratchet (guard at 332,604 gs) and priced the absence of the named fix
(count pinned bytes at capture + answer-or-expire); 1b3f flew a different fix (per-reader
`oldest`) sound against an *artificial* far pin. Whether one fix closes both doors decides what
gets built next. Answer: neither subsumes the other; the scan channel needs a byte-cap unit,
and a second, later-onset history channel (measured here for the first time) needs the view's
attention. This is the "close the ruin before shaving nanoseconds" step (PRINCIPLES #25: "not
making mistakes matters more than doing things efficiently, don't multiply by zero").

**Evidence** (all flights: shipped `nladder` scene, seed 1, rtf 100, 12 ms budget, probe every
500/2,000 gs, guard `LADDER_RSS_MB=1600`; binary = 1b3f's patch verbatim + this run's disclosed
probe additions; `work/table.txt` holds the one-line-per-arm summary, logs in `work/logs/`):

| arm | gs end | RSS end | held max | RSS/held | census total (gt1) | kicks/b/gs |
|---|---|---|---|---|---|---|
| OFF burn 3×10⁴, 60k gs | 59,698 | 579 MB | 245 | 2.45 MB | 45,480 (252) | 8.436e-5 |
| **ON** (`ES_READER_OLDEST=1`) same | 59,698 | 581 MB | 237 | 2.46 MB | **45,480 (252)** | 8.436e-5 |
| OFF burn 3×10⁴ to guard | 332,277 | 1,600 MB | 588 | 2.72 MB | 620,831 (30,043) | 8.498e-5 |
| **ON** to guard | **332,277** | 1,601 MB | 588 | 2.72 MB | **620,831 (30,043)** | 8.498e-5 |
| coast control 3×10⁴, 60k gs | 58,048 | 149 MB flat from 15k | 1 | — | 30,471 flat | 8.505e-5 |
| OFF burn 10⁵ | 38,033 | 1,686 MB | 195 | 9.47 MB | 106,656 | 4.198e-5 |

1. **ON ≡ OFF, to the digit, through both channels.** Same guard game-second (332,277),
   same held 588, same census 620,831 / gt1 30,043, same kicks and events rates (8.498e-5 /
   1.680e-4), 60k-gs arm identical too (census 45,480 both). `gap_s = now − oldest_item` stays
   ≤ 1.7 s (4.2 s at 10⁵) in every arm: the `oldest` door 4a71 certificate'd closed never opens
   naturally — the ratchet is not the far-doll channel, and scoping `oldest` per reader cannot
   touch it (the rule changes only prune's drop threshold, and with `oldest ≈ now` the
   threshold is the shipped one; 1b3f's own checker predicted "at one star the oldest term
   never binds" — here it never binds at one star *while interstellar*, which is the case that
   matters for the ratchet).
2. **The mid-flight channel is the scan deque.** Held scans grow monotonically under burn
   (0→236 by 60k gs, 0→588 at the guard) while the coast control holds ≤1 and stays flat. Each
   held scan retains its captured candidates — `Scan.candidates: Vec<(usize, Binding, Scalar)>`
   (encounter.rs) — and interstellar (root doll) the cheap tests pass everyone: measured
   1.94 MB/scan at 3×10⁴ (guard arm, base subtracted) and 7.36 MB/scan at 10⁵, i.e. 60–95 B per
   doll body per scan, one candidate triple each. K-linear.
3. **The fence licenses the ruin.** `universe.rs` sizes `SCAN_BACKLOG = 2048` on "about 10 KB
   each" (⇒ 20 MB). Measured: 2048 × 2.72 MB = **5.6 GB at 3×10⁴**, 2048 × 9.47 MB =
   **19.4 GB at 10⁵** — on the 8 GB target machine the cap would license death while "bounding"
   memory. It never engages first: the guard fires at held 588 (3×10⁴) and 195 (10⁵), far below
   2048. The unit is wrong, not the number: cap **pinned bytes at capture** (4447's named fix;
   the measured constant is ~95 B × doll population), or expire scans at a game-second cadence.
4. **A second, later-onset channel: history retention behind the receding observer.** From
   ~95–130k gs the census ratchets: `gt1` saturates at 30,043 of 30,076 bodies (99.9%), then
   total grows ~+30k bindings per ~28k-gs kick wave, 620,831 = 20.7 bindings/body at the guard,
   `hist_max` 5,845 — unbounded in play time, absent in coast (30,471 flat). Code path:
   `key_prune`'s visit key `droppable_until + 2·light_distance + 2²⁶` — the observer recedes at
   ~c, so `2·light_distance` grows ~2× play time and the key outruns the present (onset when
   `2·ld` exceeds the wave gap; the drop threshold is not the binder — the body is simply never
   visited again) [mechanism inference from the code path + onset arithmetic; the growth and
   its absence in coast are measured]. Neither 1b3f's rule nor the byte-capped backlog touches
   this channel; it belongs to the view/retention design question (what a receding player can
   still read), i.e. the wiki's view/memory pages, and it breaches later (gs ≳ 130k) than the
   scan channel at every rung flown.
5. **Reproduction anchors:** guard game-second 332,277 vs 4447's 332,604 (same arm, unloaded
   box); mid-flight window slopes 12.4–26.8 MB/1k gs vs 4447's 16.3; held-count trajectory
   K-independent in shape; 10⁵ guard at 38k gs vs 4447's checker "[INFERENCE] ~70k, ~25%
   optimistic" — faster, consistent.

**Predictions.** `predictions.md` was written before the flights. P1 held (ON ≈ OFF, both
ratchet, gap bounded; the falsification branch — ON flat with OFF's gap growing — did not
fire). P2 held (kicks/events identical to the printed digits). P3 held (slope order, coast
flat). P4 was not needed (ON never differed). The kill criterion (OFF fails to ratchet) did not
fire.

**Commands** (each ≤ 90 s; full `regen.sh` ≈ 4 min including build):
```
cargo build --release -p emergent-universe --example nladder
BIN=$CARGO_TARGET_DIR/release/examples/nladder
ES_PROBE_EVERY_GS=500 ES_WALL_CAP_S=300 LADDER_RSS_MB=1600 $BIN 30000 burn 600 100 12          # OFF 60k
ES_READER_OLDEST=1 ES_PROBE_EVERY_GS=500 ES_WALL_CAP_S=300 LADDER_RSS_MB=1600 $BIN 30000 burn 600 100 12  # ON 60k
ES_PROBE_EVERY_GS=2000 ES_WALL_CAP_S=600 LADDER_RSS_MB=1600 $BIN 30000 burn 7200 100 12        # OFF guard
ES_READER_OLDEST=1 …same…                                                                       # ON guard
ES_PROBE_EVERY_GS=2000 ES_WALL_CAP_S=600 LADDER_RSS_MB=1600 $BIN 30000 coast 600 100 12        # control
ES_PROBE_EVERY_GS=2000 ES_WALL_CAP_S=600 LADDER_RSS_MB=1600 $BIN 100000 burn 600 100 12        # 10⁵
python3 lab/results/20261019-1452-taleb-527a/work/analyze.py <logs…>
```
Note the harness's wall speed: this unloaded box runs the 60k-gs flight in ~19 s (the 12 ms
budget is a cap, not a target), so the arms are cheap here; loaded-box runs are slower but
memory retention is load-independent (held counts are load-elastic, RSS slopes are not).

**What would make it wrong.** A code path that scopes or shrinks `Scan.candidates` at capture
differently than read (then per-scan bytes would not track doll population — the 10⁵ arm
refutes that); a flown far doll (E9, two stars) where `oldest` opens — there the two fixes
interact and ON could differ from OFF (unflown, exactly as 1b3f's checker said); the channel-2
mechanism attribution (visit-key arithmetic) is inference — the growth itself is measured.

**Cost of adopting.** The scan-channel fix is local (count bytes at capture; the constant is
measured), 1b3f's rule stays what it is (the far-doll fix, still needed at scale), and channel
2 becomes a named input to the view design. Nothing here weakens any gate.

**Fit with PRINCIPLES.** "basically we don't want errors that can compound" (#13 — the scan
deque compounds per item at ~95 B × N); "the best part is no part" (#17 — the candidates the
interstellar scan holds are work not done, retained because the frame had no idle time);
"not making mistakes matters more than doing things efficiently, don't multiply by zero"
(#25); "a fix signals the wrong representation" (#19 — the fence counts scans, the ruin counts
bytes).

**The lens.** Taleb's via negativa found the fence that licenses the ruin it was built to
bound (sized on a constant from another regime — iatrogenics by unit choice), and the
convexity question (one flight, both doors measured) resolved the record's same-day conflict.
Missed by this lens: nothing here measures the *smoothness* cost of the byte-capped fix (the
allocator page's frame channel), and the 60-minute window left the channel-2 mechanism as a
one-arm inference, not a bisect.
