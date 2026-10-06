# Dossier — 20261006-1249-library-8f99 (library lens)

**Claim:** The slack skin's width must be sized per pair: the re-setup floor sits at the pair's total drift amplitude, which is 0.11·a for a non-resonant body but 2.2·a at (and near) a 5:2 resonance — a 55× split — so resonant-band pairs need escalation out of the skin tier, not a wider skin; below the floor, setups fall only as w^(−1.1…−1.7).

**Bottleneck:** encounters — the slack skin (the lever the 6 Oct gold left standing: 12.6×) and the top scaling risk (candidate work must track real encounters). Gain sought: stop paying a global width (wastes ≥10× on the bounded majority or re-setups the resonant band every conjunction); deletes the idea that width alone buys more setups reduction. This sizes q-skin's one free parameter.

**Evidence** (`python3 slack_probe.py`, 5 s, ~100 MB; full curves in `probe-out.json`):
- Restricted 3-body (μ = 0.03 at a₂ = 5), truth DOP853 rtol 1e-12 (convergence check vs 1e-10: max |Δx| = 1.9e-7); cheap model = the plane's: osculating Kepler refit at setup, kept until prediction error crosses width w. 60 orbits, 1024 samples/orbit.
- `nr` a = 1: floor at w = 0.108 = **0.11·a** (0 setups at w ≥ A_free); setups/orbit: 1.72 at w = 3.6e-3 → 0.017 at 0.074; exponent ≈ −1.4 to −1.7 over the resolved range (steepest at small w).
- `res` a = 2.714 (5:2): e pumped 0.05 → 0.197; floor at w = 5.92 = **2.2·a**; still 4–5 setups at w = 4.1 (1.5·a); exponent ≈ −1.1.
- `det` a = 2.65 (2.4% off resonance): behaves like `res` (floor 5.78, e → 0.190) — the resonant band is at least 2.4% wide in a at this μ, so the "unusual" is a finite population, not exact commensurabilities.
- The library source (verbatim, cached): `bash fetch_readwise.sh readwise.json` (770 books, 4,580 highlights); quotes in `author-final.md`, found via `highlights.tsv`.

**Predictions** (`predictions.md`, written before the run): (1) held — nr bounded with a hard zero-setup floor at its drift amplitude; (2) half-held — res stays non-zero up to 55× A_nr (predicted ≥100×) and its slope is NOT steeper than nr's (predicted steeper): failed on both counts as stated; (3) held — the global width is ≥10× (measured 55×) too wide for the majority. Held-out failure reported: the exponent in nr is steeper than the predicted [0.3, 1] band.

**What would make it wrong:** μ = 0.03 is a fat perturber chosen for signal in 60 orbits — real amplitudes will be smaller; if the plane's inter-kick drift is dominated by kick quantization rather than tide, the floor moves but the split (bounded vs resonant band) stands. One geometry per case, 2D, float toy, orders of magnitude only (cloud, x86). Adoption cost: a per-pair drift counter in the skin tier (re-estimated at each re-setup: the width is drift-rate × budget) plus an escalation predicate (measured drift amplitude > meaningful skin ⇒ leave the tier); the escalation target already exists (the rotating binary doll / phase-neighbour certificates). Fit: "Priority is slack, not proximity" (principle 5) and "the simulation tells us what's next not us" (22) — the width becomes measured state, not a constant; "a body resolves only the influences that are significant at its own scale" (33).

**The lens:** Julien's library is decision literature (Taleb, Musk, Munger, Ferriss), not collision-detection engineering; the deepest practitioner field for encounter discovery (satellite conjunction screening) is absent from it. Lessons 2–5 are prescriptions the lab has not measured; only lesson 1 carries a number. H0161 already paraphrased Musk/Taleb for the allocator — this run's addition is the verbatim corpus and the skin-sizing law.

Machine state: 8 vCPU Linux x86 shared runner, 1.7 GB used / ~14 GB available at run time, load from co-runners unknown; probe single-threaded, 5 s.
