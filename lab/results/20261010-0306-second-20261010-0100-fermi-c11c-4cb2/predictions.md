# Predictions (written before the decisive runs)

The decisive experiments (this run's own `bench/`, driving only shipped public APIs; the
plane replay's digest is checked against the shipped `--kick-bench` record):

1. `second-bench plane 1 55 1.0` (and seeds 2, 3): per-distinct-kick sub-phase attribution
   on the shipped plane scene — the checker's "open the resolver".
2. `second-bench coorbital N S 100 R`: N ships on one circle of the root doll (one compiled
   cycle shared by construction), the checker's amortization measurement.

Smoke runs already seen (not held out): plane 20 s (32 kicks, digest-matched: bind 42% of
process, `Orbit::compile` 8.2%, warm memo hit 0.6 µs) and coorbital 64×20 s×100 (64 kicks,
1 exact shape, 1 quantized shape). The predictions below are about the decisive runs'
fuller cases.

## Held-out predictions

P1 (attribution, made ships). Over the clock path (the plane's made ships), the rebind
   (`bind::bind`) is 30–50% of `step::process`, and the *shareable* part (`Orbit::compile`)
   is ≤ 12%. Readout + secondaries + field + planning each stay under 15%. Sum of all
   attributed buckets covers ≥ 65% of process (the rest: bisections, inserts, allocator).

P2 (attribution, leavers). The leaver population (the 385 µs tail) is passage-dominated:
   ≥ 60% of its cost is `bind`, and `Passage::compile` alone ≥ 35%. So the shareable share
   is larger there than on made ships.

P3 (sharing premise). N ships on one circle produce ≤ 3 distinct exact `ShapeKey`s and
   ≤ 2 quantized codes at N = 64 and N = 400 over ≥ 60 s of game time at rtf 100, while
   distinct kicks grow at least ~linearly with N (each ship kicks on its own clock):
   sharing one compiled cycle per formation is real, not incidental.

P4 (the ≥ 40× bar — the verdict). With the compile fully shared (replaced by a warm memo
   hit), the per-kick cost on the made population falls by at most the compile's share:
   predicted amortized cost ≥ 15 µs vs today's ~55–65 µs — a gain ≤ 1.3×, at least 25×
   short of the 40× the claim's lever demands (and ≥ 10× above the 1.5 µs/kick the 10⁹
   low-orbit budget needs at rtf 100). **Prediction: the lever is refuted; the ranking's
   "the billion must live at belt scale" conclusion survives by a different reason — the
   per-kick cost is fit + decode + readout spread across the resolver, not one shareable
   compile.**

P5 (window effect). At the 55 s window the plane's quantized memo key recurs on distinct
   kicks at 10–30% (the checker saw 16%; the 20 s window's 0% is an artifact), while the
   exact key stays ≤ 5%. This changes no budget verdict: the engine compiles fresh either
   way, and a warm hit costs ~0.6 µs.

P6 (consistency). The plane replay's digest matches the shipped `--kick-bench` record for
   seeds 1–3 at 20 s and 55 s, and `process` medians land within ±25% of the shipped bench
   on this shared box.
