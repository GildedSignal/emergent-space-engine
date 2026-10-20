# Dossier — the pair cone is exact at the wall rungs, and the record's fix-target has moved

**Claim.** The scan's pair cone — `|d| > |w| + near` proves no encounter, the triangle inequality on the same linear relative motion the law's own predicate tests — is measured **never-miss at the ladder's wall rungs** (6,111 answered scans, 432,403 candidate pairs, 2,570 encounters, **0 violations**, 98.55% of pairs provably unencounterable, read-set deletion 80×), and on today's tree `pull_ships` pulls **zero** at every scene flown, so the doll-wide un-budgeted read inside the player's item rides the **fleet loop** (`universe.rs` 733–741), not the pull the record targeted.

**Bottleneck.** Bodies in the flyable engine (28 → 10⁹): the player's item legally materializes its whole doll (fleets, hand-outs, pulls) to feed a scan whose answer needs 5,385 of 432,403 bindings read. The same cone that bounds the scan bounds what must exist before the item; everything else stays a budget-gated queue entry. Expected gain on the read set: ~80× measured here (afff's band 16–85× extended two decades up); on the wave frame (815 ms at 10⁵, 1,633 ms at 2×10⁵, reproduced) the lever is the same item's fleet loop.

**Evidence** (shipped `nladder` scenes, seed 1, rtf 1000, 12 ms, print-only probe `ES_CONE_PROBE=1` in `Scan::compute` + `Universe::pull_ships`; off = shipped bits):

| arm | scans | candidates | cone-skippable | passers | hits | violations |
|---|---|---|---|---|---|---|
| 10⁵ burn 20 s | 1,734 | 134,615 | 98.46% | 2,075 | 1,083 | 0 |
| 10⁵ coast 20 s | 915 | 163,885 | 99.24% | 1,246 | 413 | 0 |
| 2×10⁵ burn 20 s | 1,728 | 133,903 | 98.46% | 2,064 | 1,074 | 0 |

- The passers ⊇ hits with slack ≤ 1 near; real encounters sit deep inside (max ratio `|d|/(|w|+near)` = 0.95): **the cone is tight** — it cannot be widened for free, and needs no widening.
- Candidates per scan: 78 avg (burn, all dolls), 179 avg (coast: afff's 178 locals, confirmed), max 1,804 (the belt crossing, doll 0). The radial apsidal filter, not the cone, does the coarse cut at these scenes; the cone deletes 98.5% of what it passes.
- `pull_wave` census: **root pulls 467 (10⁵) / 467 (2×10⁵) calls, 0 ships pulled, every arm**; child pulls likewise 0. The wave frame still costs max 815.3 ms (10⁵) / 1,633.0 ms (2×10⁵) — the record's own digits — and the flight's kick count (~1.4×10⁵ at ~50 µs/kick ≈ the 815 ms frame) is consistent with the fleet loop inside the player's item (`resolve_body` advances every fleet to its tick−1 and resolves every due hand-out before its own step, outside the budget). Attribution by consistency, not instrumented: named below.
- The 40 s arm's census is bit-identical to the 20 s arm's (the player leaves the scan-bearing era by ~20 s; `dead=0`, `truncated=false`): the wave-era capture bail (7b6f's 57k cands/scan memory channel) was not reached; that regime is the named gap.

**Commands** (each ≤ 60 s; full set in `regen.sh`, ~5 min): `cargo build --release -p emergent-universe --example nladder` (with `work/patch.diff` applied), then `ES_CONE_PROBE=1 $BIN 100000 burn 20 1000 12 > arm.log 2> arm.err`, and the awk summaries over `cone_scan`/`pull_wave`/`VIOLATION` lines.

**Predictions** (`predictions.md`, written before the flights): P3 held (0 violations — the exactness result). P1, P2, P4, P5 failed on their letters: the candidates per scan are ~78, not ≥5×10⁴ (the belt is radially filtered at the player's window on this tree — the wall-rung scan is not the whole doll outside the wave era); skip is 98.5%, not ≥99.9%; the margin is not ≥10³ — the cone is tight at the boundary (hits at 0.95); `pull_ships` pulls zero, so the pull/cone ratio is undefined — the doll-wide read rides the fleet loop. P6 held (coast: no root pulls, 179 cands/scan, 99.2% skippable).

**What would make it wrong.** A violation at a scene not flown: relativistic crossers (|w| near c against the f64 census is fine — the skip test itself is exact i128 via the norms' inputs; only the census's *reporting* is f64), fleet-wide scans (another origin), and the dense crowd decade (afff's 6,000 members: 1.0–1.2× — nothing to delete there, unchanged). The cone is exact by the triangle inequality on the law's own linear-motion model — a pair whose real motion deviates from linear within the interval by more than the slack would break it; the slack measured is ≥0 at hits (tight), so adoption must keep the certificate on the same interval the predicate integrates.

**Cost of adopting.** The capture-time form still cannot evaluate the cone without reading the binding (the walk) — adoption is afff's window-membership record (open direction 1) with this run's never-miss now measured at the wall rungs; plus re-attributing the player's item's fleet loop to budget-gated items (ee4d's pattern) and a digest re-freeze. Fit with PRINCIPLES: "Compute only surprises" (98.5% of the read set is provably not a surprise), "a fix signals the wrong representation" (TTL fence, SCAN_BACKLOG lag, deferral staleness and the stream cure are four patches on one unbounded read).

**The lens (whole system).** The unification I went for — one predicate bounds the scan, the pull and the held-scan memory at once — half-landed: the cone bounds the scan exactly, but the doll-wide read the record chased through `pull_ships` has moved to the fleet loop on this tree, which my probe did not instrument. What the lens missed until the numbers said so: the belt never reaches the scan as candidates at these scenes (the radial filter passes tens, not the doll) — the memory channel's 57k/scan lives only in the wave-era bail my flights do not reach. The system-level sentence survives, sharpened: *the player's item is the only un-budgeted reader left, and its read set's certificate is the pair cone.*

# regen

`regen.sh` applies `work/patch.diff`, builds, flies the four arms and prints the census table. ~5 min.
