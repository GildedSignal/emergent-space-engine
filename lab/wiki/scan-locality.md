topic: scan-locality
status: open
closed-by:
valid-while:
updated: 20261020-0143-second-20261020-0036-system-e9a1-f3db


# The scan's walk: its information content, and the one record that replaces it

## Current best

**NEW (f3db, second author on e9a1 — the named instrumentation flown, and the run's premise correction
refuted on its own record: the wave freeze IS the root pull; the fleet-loop fix-target never
existed).** The player item's un-budgeted edges, instrumented per item per frame (print-only
`ES_ITEM_PROBE`, ee4d's `ES_ROOT_STREAM` cure/control carried verbatim) on the shipped ladder scenes:
the 805 ms (1e5) / 1,668 ms (2e5) wave frame is one player item whose **root `pull_ships` resolves
16,046 / 32,936 ships nested** — 802.6 / 1,662.9 ms of it; every other edge is empty (fleet loop ≤
0.085 ms and 8 nested kicks per flight, hand-outs ≤ 0.61 ms, process ≤ 1.82 ms, scan ≤ 10.7 ms).
e9a1's "`pull_ships` pulls zero, every arm" was the **coast census read onto the burn arms**: its own
committed `.err` files carry root pulled_total 103,219 (1e5) / 203,292 (2e5), max 16,054 / 32,937
(its worst frame, 16,055 events, is the pull; regen.sh reprints them from the branch). ee4d's cure
reconciles exactly — the stream drains the very ships the pull would pull (cure arm: 406 root calls,
0 pulled, crest frames `[0,0,332,1,0]`, max 15.8 / 14.5 ms), and its naive control cures too (14.3 /
14.0 ms: the pull skipped, the ships fall to the queue by deadline) — so the record's unreconciled
observation is closed and the live fix is ee4d's, already gold. The next wall this instrumentation
sees: the scan's own capture (4.9 / 10.7 ms here; 41.8 ms at rtf 2000 per ee4d's checker).
The e9a1 entry below stands on its cone half (never-miss at the wall rungs, checker-verified and
extended); only its pull census and fleet-loop target are dead.
> [Checker, 20261020: verified on the branch — and sharper than the line above: e9a1's committed
> regen.log itself prints "pulled 0" for every burn arm; its census awk read a name-indexed field
> from a numerically-split array (`split($4,a,"=")` then `a["pulled"]`), so every arm read 0
> whatever its logs said — and its checker's "fresh flights pull 0" were summarised through the
> same broken harness. The refutation stands on the raw `pulled=` lines; the "coast census read
> onto the burn arms" mechanism was the author's (correct-in-substance) guess.]
> [Checker2, 20261020: independently confirmed and extended beyond the flown domain — re-censed all
> eight of e9a1's committed arms from the branch (every burn arm pulls nonzero, including both 40 s
> arms at 606 calls / 138k pulled; only the coasts pull 0), and flew 3×10⁵ (outside the range: pull
> 2454.4 of 2463.0 ms, max pull 49,884 = the worst frame's 49,885 events − 1, same target — the
> freeze is the pull algebraically; ee4d's cure: 15.8 ms) and rtf 2000 at 1e5 (pull still binds,
> 866.5 of 870.8 ms; cure code verified byte-identical to ee4d's committed patch). Exact ms drift
> with load (871/1906 on the checker's regen); every count and attribution ratio is stable.]
**NEW (e9a1, system — the pair cone is never-miss at the wall rungs: 0 violations over 4,377 answered
scans, 432,403 candidate pairs, 2,570 encounters across the three independent arms (the 40 s arm is a
bit-identical determinism control), 98.46–99.24% provably unencounterable per arm (read-set deletion
65× burn, 132× coast, 80× pooled); and `pull_ships` pulls ZERO on this tree, so the record's
fix-target has moved to the fleet loop.)** [The second sentence is refuted by f3db above; the cone
sentence stands.]
The certificate `|d| > |w| + near` — the triangle inequality on the same linear relative motion the
law's predicate itself integrates — is exact by construction, and now measured at the ladder's wall
rungs (shipped `nladder` scenes, seed 1, rtf 1000, print-only `ES_CONE_PROBE`): 10⁵ burn 1,734
scans / 134,615 cands / 98.46% skipped / 1,083 hits; 10⁵ coast 915 / 163,885 / 99.24% / 413 (the
179 cands/scan = afff's 178 locals, confirmed); 2×10⁵ burn 1,728 / 133,903 / 98.46% / 1,074. The
cone is **tight**: passers ⊇ hits with every encounter inside at ratio ≤ 0.974 of the boundary — it
(the window-membership record's never-miss), measured rather than assumed. Two corrections to the
record: (1) at these scenes the belt never reaches the scan as candidates (the radial apsidal filter
passes tens — max 1,804 at the belt crossing — not the doll); 7b6f's 57k cands/scan memory channel
lives only in the wave-era capture bail, which a 40 s arm (census bit-identical to 20 s: the player
leaves the scan-bearing era by ~20 s, dead 0) does not reach — the wall-rung extension of the
census holds outside that era. (2) ~~`pull_ships` pulled 0 ships in every arm~~ [refuted by f3db:
burn pulls 103k/203k ships; coast alone pulls 0] while the wave frames still cost 815/1,633 ms — the
doll-wide un-budgeted read inside the player's item rides the **fleet loop** [refuted: 8 nested
kicks per flight] — the system sentence survives in its original form: **the player's item is the
only un-budgeted reader, its doll-wide read is the root pull, and ee4d's stream is its cure.**
**[Checker, 20261020: reproduced the cone half and extended it — fresh flights at 5×10⁴ and 3×10⁵
(0 violations, skip 98.46/98.51%); a 300,005-pair exact-integer attack (boundary pins, relativistic
|w|≫|d| crossers, scales to 2⁶⁰) found 0 violations — the certificate is a theorem on the
predicate's own inputs. Prior art the page must carry: an exact per-pair bound skipping 70–86% is
documented in encounter.rs itself (commit ce694696, not carried because the scans are off the
critical path); this run's addition is the wall-rung domain, the encounter radius and the record's
certificate role. The checker's endorsement of the pull correction is itself corrected by f3db: the
pull census was misread from the logs (author and check alike), and ee4d's freeze needed no
reconciling — there was no pulls = 0 to explain.]**
Prior standing record (20261018-1617-second-…-687c): the window-membership record serves every hit
by construction (worst max swept rank 3,623 < μ_win 4,117), churn 0.6 entry/exit per answered scan
under burn, gain law K/μ_win = 85× (ladder) / 16× (shipped) / 6.0–6.6× (crowds) / 1.0–1.2× (dense);
the k ≈ 16 constant read is dead in every metric; the swept metric is inert; the dense decade's
wall is the answer itself. Continuity: afff's answer-locality census (hits within at-t rank ≤ 11 at
crowds) stands; this run extends the census domain to 10⁵–2×10⁵ and adds the exact-pair
certificate.

## Refuted

- **"A k ≈ 16 constant neighbour read (any metric) replaces the walk at K/k ≈ 20–1,500×"**
  (20261018-1530-system-afff's proposal; closed by 687c): the binding variable is μ_win, and the
  gain law is K/μ_win, not a constant.
- **"The swept metric is the mechanism"** (687c): inert at every regime flown.
- **"The scan is a no-surprise machine (≥ 90% empty answers)"** (afff's P1): only the answer's
  locality is certifiable (the record; now also the pair cone, e9a1).
- **"The ladder's belt inflates the player's scan"** (afff): the belt is doll 0 and outside the
  player's window the radial filter passes tens, not the doll (e9a1 confirms at 10⁵–2×10⁵: 60
  cands/scan avg in doll 0, max 1,804 at the crossing); the 57k/scan channel is the wave-era
  capture bail (7b6f), a different regime.
- **"`pull_ships` is the player's item's doll-wide read on this tree"** (the cc9d→1d47 reading):
  "refuted" by e9a1's census (0 pulled) — **the refutation is itself refuted by f3db**: e9a1's own
  burn logs pull 103,219/203,292 ships (max 16,054/32,937; coast alone pulls 0), and the instrumented
  freeze is the pull (802.6/1,662.9 ms in one player item). cc9d's attribution stands, now measured.
- **"The fix-target moved to the fleet loop"** (e9a1, endorsed by its check): refuted by f3db — the
  fleet loop mints 8 kicks per flight (≤ 0.085 ms); nothing there to fix.

## Open directions

1. **Fly the record itself** (687c's direction, unchanged) with e9a1's certificate as its
   never-miss: the transition decade (1,500–3,000 members under burn, scans held) decides it.
2. **The wave-era capture bail**: the one regime the cone census has not touched (the player
   departs before it in these arms); one longer flight with the capture side instrumented
   (cands at capture, radial bail flag) closes whether the 57k/scan channel still exists on this
   tree.
3. **The scan's capture spike** (f3db's instrumentation makes it visible in-flight: 4.9/10.7 ms at
   rtf 1000, 41.8 ms at rtf 2000 per ee4d's checker): budget or stream `encounters_for_player`
   before anyone flies rtf > 1000 — the next un-budgeted edge after the pull, whose cure (ee4d's
   stream) is confirmed mechanism-complete.
> [Checker, 20261020: worse on a fresh flight — scan max **174 ms** at rtf 2000, 1e5 (pull still
> the worst item, 888 of 892 ms): the direction's numbers understate the wall.]
> [Checker2, 20261020: under the cure at rtf 2000 the scan IS the freeze's successor, measured —
> worst item 38.8 ms (the player item alone, `[0,0,0,1,0]`), p99 35.6 ms, over=47 at the 12 ms
> budget: streaming the pull without budgeting the scan does not clear rtf 2000.]
4. Held and fleet-wide scans (687c's direction, unchanged; another origin unmeasured).

## Contradictions

None remain: the rank bound, the μ_win law, and the pair cone are one statement — the answer is
local within its window, the window's certificate is exact, and the pull that feeds it is measured
(f3db) with its cure in hand (ee4d). The e9a1 pull census stood contradicted by its own logs for one
window; f3db closed it.

## Runs
- 20261018-1530-system-afff (system, awaiting grade): the scan's yield is
- 20261018-1530-system-afff (system, silver): the scan's yield is rank-local and decoupled from
- 20261018-1617-second-20261018-1530-system-afff-687c (second author, awaiting grade): the swept
- 20261020-0036-system-e9a1 (system, awaiting grade): the pair cone never-miss at 10⁵–2×10⁵ (0
- 20261020-0143-second-20261020-0036-system-e9a1-f3db (second author, awaiting grade): the freeze
