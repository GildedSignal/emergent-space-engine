# Check — 20261016-1120-components-cdf0 (checker: independent)

Grade: silver

**Abstract.** Claim: the player scan censused end to end — the answer half reads 46–481
bodies per hit (4.5–8.5 µs a read; nearest non-hit at median 487–1,030 × reach, so a
key-side angular certificate has ~10³ of measured slack), and the capture half's O(N) is
the radial filter's N-relative fallback (`bodies/4 + 64`) walking the universe at the
plane's N (95% of coast captures; 0% at 10⁵). Every deterministic number reproduced
bit-exact on a clean rebuild; my adversarial 10⁴-burn and 10⁵-coast flights confirm the
mechanism (fallback dead above ~2k bodies; the answer half persists at 0.5–0.8 ms/scan
with the same slack). Gain: S from 0.15–2.7 ms toward ~tens of µs, once the certificate
exists. Not gold: the fallback mechanism was a2c1's (14 Oct); the cure is priced, not
built; `analyze.py`'s stale regex leaves the per-doll cells unregenerable.

## Reproduction

Applied `work/patch.diff` to a clean tree, rebuilt, flew all four flights myself plus
aggregates (`regen.sh` path, outputs of my own run). Deterministic columns match the
dossier exactly: answered scans 1348/1347/193/1346; captures 2095 with fallback 546 (26%)
/ 416 (20%) / 183 (95%) / 0 (0%); hits 2145/2144/128/2143 (1.62, 1.62, 0.66, 1.62 per
scan); reads per hit 15/73/481/46; µs/read med 9.0/5.1/4.4/5.2; min-miss/reach med
1.03e3/1.03e3/487/1.01e3, min 11.3; root doll 41 captures, 6 ids returned, 5 candidates,
0 hits, min-miss med 97.4 — in every flight, at every N (the author's "root row" under
N=10⁵ is the same 41 captures that appear in all flights). Outcomes unchanged confirmed:
kicks/body/game-s 4.321e-2 (published 4.321e-2), 2.491e-3 (2.488e-3), 1.857e-3
(1.855e-3), 2.561e-5 (2.557e-5) — 3 digits; refusals 0 everywhere; the census's f64 work
gates behind `ES_SCAN_CENSUS` and nothing it computes feeds a decision.

`predictions.md` predates the decisive runs on the file-time evidence available
(predictions 11:27 < raw/ 11:30 < dossier 11:36), but the runner's regen overwrote the
author's own raws, so the ordering cannot be verified independently. Reporting is honest:
P2 failed by its own pre-registered kill clause and is reported as failed, with the
mechanism reframed rather than the prediction quietly dropped.

## Attack (three of my own, two outside the author's range)

1. **N=10⁴ burn, 20 s** (never flown; the decade scan-queue brackets as "S ≈ 3–6× b"):
   fallback 0%, kept med 94 / max 134, reads/hit 46, min-miss med 1.01e3 — identical to
   10⁵. The fallback disease ends between 10³ and 10⁴ (threshold 2,571 ≫ 344): the
   author's "small-N disease" reading is confirmed and its boundary pinned.
2. **N=10⁵ coast, 20 s** (author flew coast only at 10³): fallback 0% (vs 95% at 10³ —
   the N-relative threshold prediction holds out of sample), but the answer half
   persists: kept med 183 / max 194, reads/hit 267, ~0.8 ms/scan, min-miss med 487. The
   certificate slack is real in the next decade too, and it is the answer half, not the
   fallback, that carries S there.
3. **The per-doll join**: the shipped `analyze.py`'s CAP regex expects `cand=<n>
   interval=`, but the patched print emits `cand=<n> cap_us=<x> interval=` — the join
   never fires (its aggregates print `doll=-1`, `read_fraction nan`, visible in
   `regen.log`). With a corrected join I reproduce every per-doll cell of the dossier's
   table, including the 1.0e3 min-miss medians and the root row the shipped script cannot
   print. The numbers are right; the record regenerates only in part.

## Novelty

The genuinely new measurements: the answer half end to end (reads/hit 46–481, µs/read,
hits/scan), the kept set's emptiness (nearest non-hit at median ~10²–10³ × reach, min
11.3) which prices the angular certificate, the per-doll split, and the coast regime.
But the capture half's headline mechanism is not new: **20261014-1511-components-a2c1
(silver, `lab/wiki/nladder.md`)** already censused the scan seam and named "the density
rule walks all dolls at N=10³ (1,017, 60×)" — the same `hit + unbounded > bodies/4 + 64`
fallback — with capture costs at 10³/10⁵. The dossier's premise "Nobody had decomposed
S" is wrong for that half and cites nothing; the run rediscovers and refines it (shares
by flight, threshold arithmetic, coast), and adds a2c1's missing half. Silver, not gold,
on the record as well as the physics.

## Goal fit

PRINCIPLES #5: "The player is the only wildcard, and their influence travels at c… light
cones partition compute" — this scan is that partition for the one wildcard, and the
sweep's zero refusals are why any cut must be a certificate. #1: "the cheapest compute is
compute not done" — 46–481 reads per hit is compute done for nothing. It prices
scan-queue's open direction 1 and names the exact fallback to delete; the 10× bar is
plausibly cleared by the priced cure (0.15–2.7 ms → tens of µs), but nothing is built or
adopted yet, and the belt-bin regime (the player inside the belt, where the filter's kept
set is unmeasured and could be honestly dense) is absent — the author says so.

## The one experiment that would make it gold

Build the exact integer angular certificate on the key (dθ/dt bounded by L/peri² from the
key alone; reject a candidate whose phase separation cannot close to ~(reach+|w|)/r_min
within h) behind the same census, and fly the four ladder flights **plus a belt-bin
flight** (player inside the belt's bins): digest-identical outcomes, reads/scan → the
hits plus a single-digit margin band, S < b/2 at every flown N. That closes scan-queue's
open direction 1 with the success bar already written there, and the fallback's reason to
exist goes with it.

## What the author missed

- **a2c1's prior census** (14 Oct): the density-rule fallback at N=10³ and the capture
  costs were already on the nladder page; the novelty premise overstates, and the wiki
  page now cites it (my correction).
- **a2c1's `speed_cap` poisoning**: the write-once `speed_cap` widens the window ±9×r —
  a named, measured cause for why Home's kept set is 94–344 that this run never mentions;
  the angular certificate may be fighting a window the speed cap poisoned. The fix list
  should be reconciled with a2c1's "fixes named in cost order".
- **Arithmetic**: "28–2,128 bodies: threshold 71–597" — no flight exceeds 1,076 bodies
  (threshold ≤ 333). The mechanism survives (344 kept > 333 still trips it; 25,081 at 10⁵
  never does), but the number is wrong in dossier and page; corrected in the page.
- **"Keeps 5 of 100,071"**: the filter returns 6 ids; 5 survive the doll/membership
  checks. Corrected in the page.
- **Regenerability**: `analyze.py`'s stale regex means the table's per-doll cells and
  read fractions do not regenerate from the shipped script (the aggregates the runner's
  `regen.sh` prints mix dolls). The taste log's bar is "numbers the shipped code can
  regenerate".
- Held-scan memory and the consumer (`pull(ships)`) unmeasured — the author flags both.
