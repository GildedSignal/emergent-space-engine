# Dossier — the formation falsifier: the burn knee is the belt's geometry, not burn's

## Claim (one sentence)

The twice-checked "no bounded cap serves burn" law is a property of the belt's uniform
spread, not of burning: the same flight with the belt concentrated into co-orbital
formations — identical kicks (132,278), identical demotions (130,187), identical digest
certificate — holds the promotion floor at **1.014×demotions at cap 4,096** where the belt
needs cap 131,072 and degrades to 7.23×, so a bounded burn cap revives for exactly the
fleet/battle workloads the game wants (and that the pairwise encounter tier dies on:
concentration ruins one component and saves the other).

## Bottleneck

The board's memory/live-bodies seam at 10⁹ (`lab/wiki/nladder.md`, today's consensus:
the burn knee is demotions ≈ N ⇒ ~1.4 TB at 10⁹ ⇒ "price the re-mints or delete the
reads"). This run measures the named open falsifier (b0ed's checker, page open
direction 4): *a co-orbital-concentrated scene whose burn re-reads are temporally local
would collapse the knee below demotions and revive a bounded burn cap.* Expected gain:
for concentrated populations the standing store is cap×~1.4 kB (a few MB) instead of
~1.4 TB at 10⁹ — it deletes the "no cap ships burn" branch of the adoption decision for
fleets, leaving the candidate-set fix scoped to diffuse belts.

## Evidence

Instrument: f55d's patch verbatim (lazy-entry seam + `ES_RETAIN`/`ES_RETAIN_MAX` FIFO
ring + counters), fetched from its published branch and applied bit-for-bit (belt ctl
digest `5caeb1b6…` at 10⁴ and `d3542eea…` at 10⁵ both equal f55d's), plus this run's
scene knob `ES_LADDER_FORM=<clumps>` (`scenario.rs::ladder_ship_form`, env-gated, belt
path untouched): the ladder's belt becomes `clumps` co-orbital formations — tight clumps
(±0.5° in angle and phase, ±0.1% in semi-major axis, e Rayleigh σ 0.005), base orbits
spread over [2.2, 3.0) AU; locals, seed, counts, flight (burn, cut 20,000 game-s, rtf
1000, seed 1) all identical. Flight battery: `fly.sh {10k,100k,k10}`, table: `table.py`
(raw `flights/*.txt`, `flights/table.txt`).

| scene (10⁵, burn 20k) | demotions | cap 4,096 | cap 16,384 | cap 65,536 | cap 131,072 |
|---|---|---|---|---|---|
| belt (uniform) | 130,187 | — | **7.226×** | 6.953× | 1.000× (the knee) |
| K=100 formations | 130,187 | **1.014×** | 1.003× | 1.001× | — |
| K=10 formations | 130,187 | **1.012×** | 1.004× | 1.001× | — |


Machine state: Linux x86 shared runner, 8 vCPU, 15 GB, load 1.2-1.5 during the flights,
~1 GB used, no swap pressure (timings are orders of magnitude only, per the lab rules).
- Belt arms reproduce the record exactly (f55d: 7.23 at 16,384, 6.95 at 65,536, hits
  1,528,451 at the knee; 0619 at 10⁴: 1.244 here vs their 1.24; 3.00 at 4,096).
- **The control is the result**: kicks 132,278, opens 100,471, boundaries 31,128,
  handoffs 1, lost 28, refused 0, contacts 0 — *identical* across belt, K=100, K=10;
  demotions identical (130,187). Nothing about the event stream or the demotion bill
  changed; only the re-reads' reuse distance did. The belt's extra promotions at cap
  16,384 are 810,531; the formation's at cap 4,096 are 1,874.
- The functional knee (zero extra promotions — f55d's checker2's honest reading, in
  (0.65×N, 1.2×N] for the belt) collapses to ≤ 4,096 = N/24, with no measurable
  difference between K=10 and K=100 (1.012 vs 1.014 at 4,096): the reuse distance is the
  kick window's own population, not N and not the formation size.
- Wall and memory improve too: the capped formation flights run 13.4-14.4 s vs the
  belt's 23.3-23.5 s, rss 373-454 MB vs 462-536 MB, promote compile 0.56 s vs 4.74 s
  (the arms compared: form/4,096 vs belt/16,384); fills drop from 1.66 M to 617 k.
- Identity: every seam arm prints its scene ctl's digest bit for bit (both scenes, all
  caps, both K); `table.py`'s identity check: zero mismatches.

Commands (each ≤ 60 s where possible; the 10⁵ flights are 13-24 s):

```
bash lab/results/20261015-1747-inversion-b172/fly.sh 100k   # ~4 min, 13 flights
bash lab/results/20261015-1747-inversion-b172/fly.sh 10k    # ~40 s, 8 flights
bash lab/results/20261015-1747-inversion-b172/fly.sh k10    # ~80 s, 5 flights
python3 lab/results/20261015-1747-inversion-b172/table.py   # the table + identity
```

## Predictions

`predictions.md` was written before the decisive flights. **P1: the falsifier LIVES,
stronger than registered** — I predicted "lives, weakly" with the knee bounded below by
the +30k offset; in fact cap 4,096 (below even the offset) holds 1.014, so the offset
mass is evictable under concentration, not pinned (it was only pinned in the belt's read
order). **P2 held exactly** (belt digests = f55d's; all seam arms = their ctl). **P3's
registered razor reading failed, its mechanism reading held**: the no-eviction razor
still sits at demotions in both scenes (evictions > 0 at every cap flown, as in the
belt), but the functional knee collapsed at both K with no K-scaling — the reuse
distance is set by the kick window, not the formation. Reported as a miss on the razor,
a hold on the mechanism. **P4 held**: 0 refusals, lost 28 as the belt, wall ≤ 24 s.

## What would make it wrong

- A checker re-flying with a *different* concentration (e.g. formations at one radius
  only, or a single mega-fleet of 10⁵) could find the collapse weaker; the mechanism
  claim ("reuse distance = the window's population") predicts it still holds at any
  concentration, and predicts a *diffuse-but-clumped-at-one-radius* belt sits between
  1.01 and 7.2.
- The scene is still one seed, one cut (20k game-s), one thrust program (the L8 burn);
  deep play (48k ≈ 2 wave periods, 0619's 2.71×N mint bill) was not re-flown here — the
  belt's knee grows with play depth, and the formation's must be shown not to (the
  registered expectation: it does not, because extra promotions track evicted *re-reads*,
  which stay window-local at any depth).
- `ladder_ship_form` re-draws the belt's lanes for its jitter (lanes 1/2/3 reused with
  new formulas), so formation orbits are not a permutation of belt orbits; the ctl
  comparison is within-scene by construction, and the event-stream control (identical
  kicks/opens/demotions) is what carries the claim across scene change.

## Cost of adopting, and fit

Adoption is a *decision change*, not code: the seam's bounded rule (0757's `ES_RETAIN_HOT`
ring, in f55d's patch) may ship for concentrated populations at a small fixed cap, and
the "price the re-mints or delete the reads" branch applies to diffuse belts only. No
engine change; the falsifier scene knob is experiment-only (env-gated, belt verbatim).
PRINCIPLES: "A failed expectation is not automatically a failed method: diagnose which
one broke" — here the failed expectation is the record's scene generality, and the
diagnosis is the belt's geometry; and "behaviours matter, not continuum fidelity" — the
behaviour (promotion floor) is the metric, bit-identity the certificate.

## The lens (what inversion may have missed)

Inverting the freshest consensus asked "what scene breaks it"; I did not invert *my own*
favourite outcome — the mechanism sentence ("reuse distance = the kick window's
population") is inferred from two K values plus the record's mint_who histogram, not
directly measured (no per-body reuse-distance trace). A second blind spot: the formation
scene is also *cheaper* in fills (617 k vs 1.66 M), so a defender of the old law could
say the cap survives because there is less to read; the counter is the per-fill
economics (extra promotions 1,874 vs 810,531 at the compared arms), but the fills
asymmetry should be named and, ideally, closed by a diffuse-but-sparse belt with matched
fill counts (unmeasured).

## Grade sought: gold

It reproduces the record bit-for-bit (belt arms = f55d/0619's numbers), the held-out
predictions were registered before the flights and the one miss is reported, and it
moves a board decision by more than an order of magnitude (the 10⁹ standing store for
fleet-shaped populations: ~1.4 TB ⇒ a few MB at a fixed cap). One named experiment away
from nothing — but if the grader weighs the un-flown deep-play arm, silver is honest.
