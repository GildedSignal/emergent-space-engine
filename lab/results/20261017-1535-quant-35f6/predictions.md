# Predictions (written before any flight; census and A/B arms both unrun)

Arms: `nladder <N> coast <s> <rtf>` release+prof on this Linux box, seed fixed by the
scenario (plane_extra seed 1). Census = `ES_SEC_CENSUS=1` (recompute always, compare);
memo = `ES_SEC_MEMO=1` (serve hits). Held-out cases for the census: N=30000 rtf 600
(5eb2's arm) and N=10000 rtf 100 — neither run's exact arm set.

1. **Census (j,t) repetition at N=10000 rtf 600:** 55–75% of `state_of` calls repeat an
   exact key (6671 measured 64.5% overall), **0 value conflicts** (no hit whose recomputed
   value differs). At N=30000 rtf 600: 55–70% (5eb2's (doll,tick) sharing was 2.66× ⇒
   ~62% at multiplicity ≥ 2). At rtf 100 I expect the same or higher (6671's checker saw
   the stream concentrate further at low rtf: 24–28× key sharing at N=1e5).
2. **Memo wall prize on the secondaries stage:** SEC ns/call falls 1.5–2.5× (the belt
   comb's ~74% distinct ticks ex-birth caps the deletion; the doll/birth half repeats
   exactly). Not 64%: the belt kick path is the stream's majority at these N.
3. **Memo wall prize on the kick:** the kick clock item (P_KICK_CLOCK, ~46 µs/call at
   5eb2's arm) moves by ≤ 10% — SEC is ~13% of the kick and only part of SEC deletes.
   The FIT stage is a control: unchanged within shared-box noise (±10%).
4. **Digest:** `Universe::digest()` at flight end identical memo-off vs memo-on at every
   arm flown. If not, the lever dies as not bit-safe in that regime (kill criterion).
5. **Frame level:** engine p50 at N=1e4 rtf 600 is small; the prize shows in p99/worst
   frames only if events cluster; I expect ≤ 5% p99 change — the stream prize is
   per-event, not per-frame, at these N (5eb2's "adopt as stream lever" reading).
6. **READOUT (partial) stage** (untimed by either run at this nesting): 3–5 µs/call,
   1.0–1.7 calls per kick; the memo removes only its secondaries share.

What would make me wrong: conflicts > 0 in the census (stale generation → the memo is
not bit-safe as wired); SEC falling < 1.3× (the sharing is thinner at (j,t) than either
census claimed — instrument difference); or the kick moving > 15% (5eb2's stage shares
mis-attributed the secondaries cost).
