# predictions.md — run 20261010-1706-fermi-2914

Written before the decisive run. Held-out quantities I have NOT measured at the time of writing.

## Fermi estimate first (my prior, derived from repo constants)

Budget at 10^9 bodies on the M1 (universe budget ≈ 4 GiB of 8 GB, ~1e10 simple ops/s, ~60 GB/s):

- Tube store: 16 B/body × 1e9 = 16 GB > 8 GB ⇒ massive populations cannot store per-body tubes at
  all; they must be family generators (galaxy scene already does this: 0 bytes/ship). Live state =
  amendments only. Budget for ALL live distinctions: 4 GiB / 1e9 = 4.3 B/body ≈ 34 bits/body.
- Event compute: belt body at 3 AU (P ≈ 1.6e8 s), secular cadence 0.3 kicks/orbit ⇒ 1.8e-9
  kicks/body/game-second ⇒ 1.8 kicks/s at 1e9 bodies — trivial even at 32× (195/s at ~1 µs/kick).
  A low-orbit population (P ≈ 5.4e3 s) at 32/orbit ⇒ 6e-3 kicks/body/s ⇒ 6e6 kicks/game-second
  ⇒ seconds of core time per game-second at 1 µs/kick ⇒ ~600 core-s per wall-s at rtf 100: dead.
- Amendment storage: if each kick carries the law's binding remainder (Residual, 4 × i128
  components, "up to 65 bits" each) and nothing reabsorbs: 33 B/kick × 9 kicks (0.3/orbit × 30
  orbits) ≈ 300 B/body ⇒ 300 GB at 1e9: over budget by ~75×. So reabsorption (folding remainders
  into the next key, or shared scars) is load-bearing, not polish.

## Predictions (held-out; the bench decides)

1. **Kick compute is NOT the first-breaking term for belt-scale populations; amendment
   storage is.** Concretely: kicks per body per game-second on the plane's own ship population,
   times measured µs/kick, times 1e9 stays ≥ 10× under the M1's per-second op budget at belt
   cadence, while un-reabsorbed residual storage exceeds 4 GiB within ≲ 1e2 orbits at 1e9 bodies.
2. **Bits per kick (creation rate of H_live):** the quantized orbit-key delta stream carries
   O(1–10) bits/kick (memo lattice 12+12 bits; consecutive kicks of one body move by a few
   lattice cells at most, so Δ-buckets concentrate); the residual components carry more
   (tens of bits each at full i64-lattice resolution). Prediction: residual bits dominate
   key bits by ≥ 10×.
3. **Secular reabsorption is visible in the stream:** consecutive kicks of one body revisit
   memo codes (revisit rate > 0), i.e. the program state random-walks around a small set
   rather than exploring the lattice — otherwise shared-cycle compilation absorbs nothing and
   the "population programs + scars" plan has no lever. If the revisit rate is ~0, that plan
   is in trouble and the dossier must say so.
4. **The event term decides which populations can be massive:** at 1e9 bodies, populations
   inside ~low orbit can be at most ~1e5–1e6 members on kick cadence alone (estimate;
   bench gives the per-body rate to scale).

## What would make this wrong

- The plane's ship population is too small/too short-lived (members die, few kicks each) to
  estimate per-body rates: then the run reports rate per body-at-risk with wide error bars,
  and the claim drops to the belt-cadence derivation only.
- `new_entry` is not produced on every kick kind (passages, refusals): then bits/kick is a
  lower bound; say so in the dossier.
