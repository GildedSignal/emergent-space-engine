Grade: gold

**Abstract.** The pending adoption's premise is half wrong, and the run proves it on the corrected
tree: with e181's patch plus its checker's named fix (the frame-loop `prune()` restored) and the
fence arm flown 10× past every prior horizon, TTL=16 deletes only the scan channel (held ≤ 1,
identity 3,427 = 1,102+2,325) while the history channel alone staircases RSS 171→1,457 MB to
419k game-s (866,168 bindings = 28.8/body, +4.19 MB/1k, no saturation), the two arms' censuses
matching to 0.1% (channels independent). I reproduced both end states bit-exact in a clean tree;
my K=10⁵ and TTL=64 arms extend the law a decade up in N and across fence widths. Gain: re-prices
the adoption order — channel 2's fix is co-equal — and delivers e181's silver→gold rerun. Cost:
zero bytes; a decision change.

**Reproduction (mine, clean tree at c9195bfa + `work/patch.diff`, build 12.8 s).** I verified the
patch is e181's verbatim except the prune restoration and the disclosed probe additions (diffed
against e181's `work/patch.diff` from its branch: the only semantic deltas are the restored
`prune()` call, `history_census()`, and the census fields in the probe line). My reruns:
- OFF: end state **exact** — gs 174,016, hist_total 241,552, gt1 30,065, hist_max 2,017, mints/
  answers 3,224/2,774 (author's log identical; RSS 901 vs 900). All 174 probes agree within the
  run-to-run elastic band (≤ ~130 bindings, 0.1% — the same band my rerun shows against the
  author's log itself: 155,143 vs 155,110 at gs ~129k).
- ON: end state **exact** — gs 419,016, RSS 1,457 MB, hist_total 866,168, hist_max 7,921, held 0,
  identity exact (3,427 = 1,087+2,340 at the last probe; 3,427 = 1,102+2,325 at the end line).
- The dossier's carried digits check against the logs: gt1 351→30,061 between gs 13k and 15k
  (first wave), slopes 2.68/3.32/4.19 MB/1k, guard projections OFF ~396k / ON ~456k linear
  (ratio 1.15 — the "~15%" is right in band, though both are projections; OFF never guarded).

**Predictions.** `predictions.md` mtime 16:01:59 precedes every flight log (16:08:38+). P3, the
decisive one, held inside its pre-registered bands (slope 3.32–4.19 in 2–4; composed horizon
~453k inside 0.3–1×10⁶); the kill criterion (ON census < 1.1/body at 240k) did not fire — 28.8
at 419k. P4 held by identity, P5 held (over 125 frames, lag 15.2 s).

**Adversarial (mine).**
1. **K=10⁵, fence ON, 59k game-s** — outside the author's tested N by 10×: first-wave saturation
   (gt1 100,064 of 100,076), fence identity exact (2,992 = 1,043+1,949), held 0, RSS 511 MB at
   59k on channel 2 alone. The law extends up a decade in N; nothing breaks.
2. **TTL=64** (unflown fence width; ~4 frames at rtf 1000): census exactly tracks the TTL=16 arm
   (74,733 vs the author's 74,733 at gs 59k), channel 1 still deleted (3,006 = 1,218+1,788).
   Channel independence is fence-width-insensitive — the fence moves bytes only, as claimed.
3. **Determinism**: the OFF rerun above.
4. **Code audit**: the claimed mechanism is in the shipped source — `key_prune` registers a body
   at `droppable_until + 2·light_distance + 2²⁶` (universe.rs:1252) and `prune` visits only keys
   ≤ now (universe.rs:1274-1284); a receding observer's light distance grows ~c·t, so the key
   outruns the present and the kicked history is never visited. As written.

**Novelty.** The page before this run held e181's fence (silver; flat to 41.9k, on a
prune-deleted tree) and 527a's channel 2 (rtf 100, 1b3f tree). None of this run's four pieces
existed: the prune-restored rerun (e181's checker named it as the gold step), the fence arm past
the onset (419k, 10× the record's longest), channel independence measured to the binding, and
the first-wave saturation correction. Not a repetition of either.

**The page.** Faithful; I corrected two slips in place (bracketed checker2 note): the saturation
is 30,065 of **30,076** bodies ("30,064 of 30,028" is an impossible pair), and "IDENTICAL between
arms" overstates — max |Δhist_total| = 134 over the 174 matched probes (~0.1%, the run-to-run
band), with the windows.txt OFF 95–130k cell (155,142) being the ON log's value, not the shipped
OFF log's (155,110; run-elastic — my rerun read 155,143). Also marked the runs line gold, twice
checked.

**Goal fit.** Board bottleneck #1's memory term: the run deletes a belief, not bytes — the
composed adoption (byte-capped scans first, channel 2 "later") is re-priced to co-equal before
the integrator freezes it. PRINCIPLES: "A failed expectation is not automatically a failed
method: diagnose which one broke (H0183)" — the fence did not fail; its claim's scope did.
"Agreement is not independence" — the author named the shared-harness risk and the one falsifier
that mattered; the first checker flew it (rtf-100 fence to 200k: 10.3/body, falsifier dead) and
I confirm independently. Two independent finders, both gold.

**What the author missed.**
- The disclosed "cadence-coupled retention rate" is mis-attributed: on this tree the census is
  cadence-independent (checker 1's fresh rtf-100 arms: 75,670 vs 75,213 at 60k); the ~1.7× gap
  against 527a is a cross-tree difference (1b3f's tree delayed retention to 95–130k — mechanism
  unresolved, a real lead the page should eventually own).
- The "~15% horizon" rests on two projections; the measured anchors (332k guard) live at another
  cadence and tree. The robust sentence — neither arm flat, both guard at O(0.3–0.5×10⁶), the
  fence's arm channel-2-bound — is what the integrator should read.
- The fence's answer price at rtf 1000 (2,325 of 3,427 scans expired unread) was not re-measured
  against e181's ≤0.3% encounter-loss bar on this tree; presumably carries over, unproven here.
- The body-count slip and "IDENTICAL" overstatement (corrected); the view-side design question
  the lens names (what a receding player may still read) stays unopened — honestly reported.
