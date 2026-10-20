# Dossier — 20261020-1815-second-20261020-1621-fermi-5f76-a7c0 (second author on 5f76)

**Claim.** The checker's named gold experiment is done: the two per-player-item array-builds
are **named** — `encounter.rs:188` `candidates.push` in `PlayerNeighbourhood::capture` (the
capped ladder, 128-B elements, top 448×128 = 57,344 B) and `radial.rs` `Radial::candidates`'s
`ids: Vec<u32>` grown past its `clone`d capacity (the short ladder, 2,944..11,776 B), **both
inside the player's neighbourhood scan, not the pull** — the census converts into a measured
deletion: **two `with_capacity` lines at exact bounds the code already computes cut the
player term 193.4 → 112.5 KB/item (−41.8%) and realloc bytes −88%** (suite-neutral,
26/26 tests), and the ship marginal's K-rise **stalls at the top of the flyable range**
(2.99 → 3.88 → **3.91 KB/kick** at 10⁵/3×10⁵/6×10⁵), pinning the 10⁹ byte row's top at
**55% of 60 GB/s measured**, not extrapolated — still closing.

**Bottleneck.** budget-1e9 od 6(a) verbatim ("a backtrace instrument to name the TWO
array-builds... pull_ships vs the neighbourhood scan vs a re-pull") **closed**, and od 6(b)
(the one-line `with_capacity`, "now aimed at BOTH arrays") **priced as a measured deletion**.
No new 10×: the decision rows stand with their constants hardened and their mechanism named
(the deletable target the census lacked). Gold case: the checker's own "one experiment that
would make it gold" — the backtrace that names the two arrays, the measured deletion, and
the saturation arm — executed, with the 10⁶ arm's cheapest decisive part (6×10⁵; a 10⁶
flight is a ~2.35 GB process at the shipped ~2.35 KB/body build, over this box's 2 GB
ceiling — 6×10⁵ peaks at 1.92 GB, the nearest feasible decade).

**Instrument.** 5f76's `alloc_scope` verbatim + two disclosed additions in the example only:
`ES_BT=1` (backtrace census of player-scope ≥2 KiB calls: first 120 per size bucket + every
400th, deduped by the first four `emergent_universe` frames; guard against re-entry) and a
`peak_rss` (VmHWM) print on every arm. Patch = `work/patch.diff`. The deletion =
`work/withcap.diff` (two files, allocation-pattern only): encounter.rs `candidates`
pre-sized to the near-list length when the radial index answered (`ids.len()` — every
candidate comes from that list; `Vec::new()` kept when it did not, the read-everybody arm,
so the change never over-allocates there), radial.rs `ids` pre-sized to
`idx.unbounded.len() + hit` (`hit` is already computed two lines above as the bins' sum —
the bound is exact before dedup). Flight args verbatim to 5f76's arms.

**Evidence** (this box, load ~0.2–0.7, flights 12–48 s wall, RSS 62 MB–1.92 GB; regen =
`regen.sh` ~5.5 min warm incl. the engine's test suite; x86 → M1 orders only):

Control C1 (instrument only, K=10⁴, seed 1) reproduces 5f76's A1 on this box: player
**193.4 KB/item**, realloc share 80%, >2KiB census 70%, ship 3.7 KB/item / 1.45 KB/kick,
base 2.04 KB/game-s.

| arm | patch | K | seed | player KB/item | realloc share | player reallocs | ≥2KiB calls | ship KB/kick |
|---|---|---|---|---|---|---|---|---|
| C1 | instrument | 10⁴ | 1 | **193.4** | 80% | 332,314 | 45,875 | 1.45 |
| D1 | +with_capacity | 10⁴ | 1 | **112.5** | **16%** | 260,819 | 11,738 | 1.44 |
| S1 | instrument | 6×10⁵ | 2 | **194.2** | 79% | — | — | **3.91** |

- **The sites (BT arm, sampled census).** Capped ladder: `capture` ← `encounters_for_player`
  ← `resolve_body`, sizes 3,584..57,344 B (490 samples, 13.4 MB) — the candidates
  `Vec<(usize, Binding, Scalar)>`. Short ladder: `Radial::candidates` ← `capture`'s closure,
  sizes 2,944..11,776 B (193 samples) — the `ids: Vec<u32>` extend growth. Minor: `PlainBodies::retire`
  via `pull_ships` (3,328 B, 25 samples). Rung arithmetic closes: two starts/item at rungs
  1–3 (both arrays), one at 4–5 (candidates only); element 128 B ⇒ the 57,344-B top is
  448 elements exactly.
- **The measured deletion (D1 − C1).** Player term −41.8%; realloc **bytes** −88%
  (853.6 → 99.2 MB); player realloc **calls** −71,495 (−21.5% — the checker's
  "~0.3–1.2 M/flight" overestimated; the ladder rungs deleted are the ≥2 KiB ones:
  34.1 k calls, buckets 2048/4096/16384 collapsing 11,558→137, 11,506→85, 5,721→15).
  What remains per item: two exact allocs (means 46,556 B = 363.7×128 and 9,794 B ≈
  2,449×4) — the near-list length varies per item (mean 364, cap 448), so the bound is
  tight, not the old ladder's worst case. Ship and base untouched (1.44/1.45 KB/kick,
  2.04/2.05 KB/game-s). The 10⁹ player-term reading falls 18.8 → 10.9 KB/game-s
  (0.097 items/game-s × 112.5 KB) — negligible either way; no decision row moves.
- **Neutrality.** Kicks 108,241 (C1) vs 108,397 (D1), events +0.06%, items within 0.22% —
  inside the declared flight-jitter band (wall-clocked 12-ms budgets; 5f76 measured 0.3–0.4%
  re-flight spread; the fleet item count is schedule-elastic and swings 199→342→139 across
  seed-1 flights with the engine untouched). Where exactness is checkable it is exact:
  **26/26 engine tests pass with the deletion applied** (lib + integration, including the
  encounter digest controls and the planted-sloppy-reuse canary). Allocation timing enters
  no state (integer-exact law).
- **Saturation (S1, K=6×10⁵, seed 2).** Ship marginal **3.91 KB/kick** (289,649 kicks,
  1,133,482 KB ship traffic): the series 1.53 (10⁴) → 2.18 (3×10⁴) → 2.99 (10⁵) → 3.88
  (3×10⁵, checker) → 3.91 (6×10⁵) — the K^0.3 rise **stalls** (+0.8% across the last
  doubling). The 10⁹ byte row: 4–8.4×10⁶ kicks/wall-s × ~3.9 KB = 15.6–32.8 GB/s =
  **26–55% of 60 GB/s** — the top measured at the top of the flyable range, killing the
  old extrapolation to 7.1 KB/kick (=100%); still closing, no pooling subsystem mandated.
  Player constant at the fifth decade: 194.2 KB/item (K-flat law holds; realloc 79%).
  Mixture dilution continues (11.35 → 4.78 KB/kick item-scope). Peak RSS 1.92 GB.

**Predictions.** predictions.md written before C1/D1/S1 (the BT naming arm disclosed as
exploratory, like 5f76's A1 anchor). No kill bar fired. P1 half-held (the ≥25% bar passed at
−41.8%, but the point landed 2 KB below my 115–135 interval, and the realloc-**calls** letter
missed: −21.5% against a predicted >80% — the bytes −88% and share 16% < 40% letters held;
the small-call floor's reallocs are not ladder rungs). P2 half-held (counts within 0.06–0.22%
jitter, not bit-equal across wall-clocked flights — my letter over-reached; the suite is the
exact check and passes 26/26). P3 not re-based by design. P4 half-held the good way (3.91
below my 4.1–5.0 band: the rise stalls rather than continues; the ≥7.1 kill bar stayed unfired).
P5 half-held (player ✓ 194.2; the RSS letter 1.8 GB missed at 1.92 — inside the box's 2 GB
rule, process not killed).

**What would make it wrong.** The backtrace samples (first 120/bucket + every 400th) could
miss a phase-only site; the census's ≥2 KiB traffic is 74% deleted by exactly the two named
sites' fix, which is strong closure, but a rare regime (burn) may build other ladders — the
burn arm was 5f76's checker's, not re-flown here. The 6×10⁵ saturation point is one draw
short of the named 10⁶ (the box's ceiling); if the marginal resumed rising past 6×10⁵ the
band top would move, though it must more than double in one decade to threaten 100%.
rtf-2000 cadence is budget-fed; all comparisons within-instrument, same rtf. One box; the
 deletion's wall-time saving was not measured (traffic was the question; the scans are
already off the critical path by design). D1's exact-alloc means (46.6/9.8 KB) replace
ladder *traffic* — the live-set is unchanged (the scan still holds its candidates); this is
a bandwidth/allocator-call deletion, not a memory-floor one.

**Cost of adopting.** Two lines on the two named sites (the bounds are already computed:
the near list and `hit`); no API change, no behavior change, suite-green. But the honest
adoption note is the page's own: cc9d's read-set fix may subsume the whole player term —
adopt this only if the read set lands without it (it is a priced option now, not a
mandate). Fit with PRINCIPLES: "the best part is no part" (71.5 k realloc calls and 57% of
the ≥2 KiB bytes deleted by pre-sizing, zero new machinery); "Measure before claiming"
(the census's count became a name and a measured deletion before any adoption talk).

**The lens.** The second-author lens risked anchor-closeness: I kept 5f76's instrument and
args verbatim (reproduction first) and could have over-trusted the census's "two arrays"
reading — the backtrace confirmed it, but the surprise was inside it: both arrays belong to
the **scan**, so the deletion lands on the encounter seam (cc9d's read-set territory), not
on the pull the page had guessed twice. What this run still cannot see: whether the burn
regime builds the same two ladders or others (one flag away, not flown); and the wall-time
value of the deletion (unmeasured by design — traffic was the named question).
