# Dossier — 20261016-1120-components-cdf0 (components lens)

## Claim

The player-scan candidate set is measured end to end on shipped flights: the answer half
reads **46–481 bodies per hit found** (4.5–8.5 µs a read), the kept set is empty by a
**median ~10³ × reach**, and the capture half's cost at the plane's own N is a fallback
that walks and clone-tests **every body of the universe** (~120–180 ns a body, 95% of
coast scans) — a second, key-side angular certificate has three orders of measured slack
to cut with, and the root-doll apsidal filter is already at its floor (5 of 100,071 kept).

## Bottleneck

The player's neighbourhood scan (`PlayerNeighbourhood`, `encounter.rs` + `radial.rs`) is
the seam scan-queue measured latching (S = s·N) and nladder's next-break 3. Nobody had
decomposed S: which doll it lives in, what the filter keeps, what a read costs, and how
empty the kept set really is. Expected gain of the named cure: the answer half 46–481× →
~1–3 reads (a hit plus the margin band) at ~15 ns a key test; the capture fallback
(universe walk) deletes with it. This is scan-queue's open direction 1 (success S < b/2)
priced by measurement.

## Requirement (the PRINCIPLES line that owns the component)

#5: "The player is the only wildcard, and their influence travels at c… light cones
partition compute" — the scan is the light-cone partition for the one wildcard; it must
miss nothing (the sweep's zero refusals), so any cut must be a certificate. #1: the
cheapest compute is compute not done — 46–481 reads per hit is compute done for nothing.

## Floor

Per scan: read the ~1.6 true hits (measured) plus the handful inside the honest margin
band, plus an O(log) index lookup. The measured certificate slack — nearest non-hit
candidate at median 487–1,030 × reach (min 11.3, the frames round a real conjunction) —
says the margin band is single-digit bodies. Floor ≈ 2–5 reads/scan ≈ 15–40 µs; shipped
answer ≈ 0.4–2.7 ms at the plane's N (cand 94–344 × 4.5–8.5 µs): **idiot index ~10² per
scan** (46–481 reads per hit), plus the capture fallback's O(N_universe) walk on the
frame path at the plane's N (~0.12–0.19 ms a capture at N=1,028).

## Evidence (commands in `regen.sh`, each flight ≤ 35 s wall, Linux/x86 shared: orders only)

Print-only census (`ES_SCAN_CENSUS=1`, `work/patch.diff`): per capture — doll, universe
size, `near` (the radial filter's kept ids; −1 = the fallback), candidates, capture µs;
per answered scan — reads, hits, µs/read, smallest approach distance of any candidate in
reach units. Flights: the ladder's own (`nladder {0,1000,100000} burn 20`, `nladder 1000
coast 20`), seed 1. Outcomes unchanged (kicks/b/game-s match the published ladder to 3
digits; refusals 0 everywhere).

| flight, doll | captures | fallback share | capture µs (fb mean/max) | reads/scan med–max | µs/read | hits/scan | reads per hit | min-miss/reach (med) |
|---|---|---|---|---|---|---|---|---|
| N=0 burn, Home | 2,095 | 26% | 15 / 33 | 19–45 | 8.5 | 1.6 | 15 | 1.0e3 |
| N=10³ burn, Home | 2,095 | 20% | 63 / 208 | 94–344 | 5.6 | 1.6 | 73 | 1.0e3 |
| N=10³ coast, Home | 193 | 95% | 122 / 185 | 333–344 | 4.5 | 0.7 | 481 | 4.9e2 |
| N=10⁵ burn, Home | 2,095 | 0% | 21 / 73 | 94–134 | 5.8 | 1.6 | 46 | 1.0e3 |
| N=10⁵ burn, root (belt) | 41 | 0% | 11 / 20 | 5 | 5.4 | 0 | — (0 hits) | 97 |

The mechanism, read off `radial.rs:254`: the fallback fires when `hit + unbounded >
bodies/4 + 64` — an **N-relative** threshold. So Home's compact doll falls back to
walking every body of the universe exactly at the plane's flown N (28–2,128 bodies:
threshold 71–597 against a doll that keeps 94–344), while at 10⁵ the same doll never
falls back (threshold 25,081). Scan-queue's S = s·N is this: at the plane's N both
halves are ∝ N — the capture walks N_universe (0.12–0.19 ms at 10³) and the answer reads
~the whole doll (0.15–2.7 ms) to find ~1.6 companions a scan.

The root doll is the opposite: the apsidal filter keeps **5 of 100,071** (the belt is
1 AU off radially) — in these 20 s flights the finder is at its floor there; the belt
seam nladder's break 3 names (one item 14.6 ms near the belt) needs a flight into the
belt's bins, not these flights.

## Predictions

`predictions.md`, written before the runs. **P1 held** (Home doll: read fraction
0.09–0.64 of the universe = most of the doll; hits ≈ 1/scan; nearest miss > 10² reach).
**P2 failed by its own kill clause** — the root-doll filter keeps 5×10⁻⁵ of the doll, so
the seam is not the root-doll finder in these flights; the cost lives in Home's doll
(reported as failed, and the mechanism — the N-relative fallback — is the finding).
**P3 held** in Home's doll (median min-miss 487–1,030 × reach). **P4 half-held**: a read
costs 4.5–13.7 µs (I guessed 1–4); the capture's cheap half is 0.12–0.19 µs/body of
universe in fallback (I said ≤ 0.2).

## What would make it wrong, adoption cost, fit

Wrong if: the belt flights (player inside the belt's bins) keep a dense set — then no
certificate cuts there and the reads are honest work; or the hit companion's margin band
is wider than the min-miss tail suggests under fleet battles (the 11.3-reach min-miss
frames show the band is real but narrow). Adoption: a second certificate on the key
before any readout — angular: a conjunction needs the orbital-phase separation to close
to ~(reach + |w|)/r_min within the interval, and dθ/dt is bounded per body by L/peri²
from the key alone (Kepler; the tube is exact) — ~10–20 ns a candidate, no clone, no
readout; it must be integer/exact like the apsidal filter (the f64 census only measures
the slack, it decides nothing). It also deletes the fallback's reason to exist (a
phase-cut compact doll is cuttable), though the fallback walk itself could be deleted
today by clamping candidates' doll before `binding_at` — a one-line order swap I did not
make (law-adjacent: `binding_at` is what makes a body live for the scan). Fit: PRINCIPLES
#5 (the light cone partitions the wildcard's compute), #1 (compute not done), #23
(nothing past c — the window h is the cone's width). Cost: one certificate in `radial.rs`
+ capture's candidate loop, no law change, the predicate stays the exact `hit`.

## The lens (what it may have missed)

I measured the finder, not the consumer: the same candidates feed `pull(ships)` and the
held scans' memory (115 B/body held per scan — the fallback's clones are ~344 × ~1.3 KB
≈ 0.45 MB a held scan at the plane's N, the ×3.7 memory of nladder's break 3); a run
that prices the cut should re-measure held memory, not just S. And one flight class is
absent: the player inside the belt (the 10⁵/10⁶ bins), where the filter's kept set is
unmeasured. Timings are Linux/x86 shared-load: orders of magnitude only.
