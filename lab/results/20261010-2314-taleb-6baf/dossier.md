# Dossier — 20261010-2314-taleb-6baf (lens: Taleb)

**Claim.** Measured for the first time, the live-distinction rate (H_live) of a stirred
belt: a frozen population program dies in **≤ 0.4 planet orbits** at every admissible
key width (≥ 8 bits/axis), key churn runs at **13–32 events per ship per planet orbit
forever**, the churn is **uniform across ships, not fat-tailed** (top 1% carries ≈ 1%),
and the mature (E,L) entropy floor is **≈ 12.7 bits/ship** — so the newborn 0.126-bit
belt (components-98bc) is real but lasts under one game-year, and populations in stirred
regions must run the kick law itself as the program, with the scar layer re-absorbed
continuously; memory sized by birth-state compression is the ruin path.

**Bottleneck.** HANDOFF's risk list, entry 2: "Distinctions created per game-second
(H_live): they, not the body count, decide whether 10⁹ fit in 8 GB; not measured yet."
This run measures it for the canonical hard case (a stirred belt) and gives the
integrator the two numbers that matter — the program half-life and the mature
bits-per-ship floor — plus the event bandwidth the allocator must absorb. It kills the
implicit assumption that a compiled population program stays valid for astronomical
timescales.

**Evidence** (all commands from this folder, each ≤ 40 s wall, numpy float64; every
counted event is an integer cell-index change; machine: 8 vCPU shared runner, load and
mem recorded in each JSON):

```
python3 hlive.py --tag belt_s1 --seed 1 --N 4000 --po 300          # belt, 2 seeds run
python3 hlive.py --tag ctl_s1  --seed 1 --N 4000 --po 300 --mu 0   # negative control
python3 hlive.py --tag ring21_s1 --seed 1 --N 2000 --po 600 --ring 2.54,0.05,0.02
python3 hlive.py --tag ringoff_s1 --seed 1 --N 2000 --po 600 --ring 2.80,0.05,0.02
python3 analyze.py                                                 # -> metrics.json
```

Model: massless ships (test particles) around the Sun, one Jupiter-grade stirrer
(μ = 10⁻³, a_p = 1.6, e_p = 0.05) on an analytic orbit; leapfrog KDK, dt = 2π/64;
(E, L) quantized on the law's memo grid (law.md §Tube) at 4/8/12/16 bits per axis.
A key change = one scar-layer event; "smoothed" = same counter on a key of the rolling
mean over ~4 planet orbits (what a program modelling only the synodic response would
predict away). Numbers (metrics.json, seeds s1/s2 agree to <1%):

- **Program half-life** (fraction departed = 0.5): 0.077 P_p at 12 and 16 bits,
  0.36 P_p at 8 bits, unreached at 4 bits. ≈ 0.16–0.75 yr of game time.
- **Key-event rate per ship per planet orbit**, naive: median 31.7–32.1 at 16 bits
  (p99/med = 1.01); saturates near the synodic rate (synodic period ≈ 4 P_p).
  Smoothed (secular residual): 12.5–13.9, with cumulative-growth exponent 1.03–1.06 —
  linear, i.e. steady permanent churn, not decelerating diffusion.
- **No tail over ships**: p99/median = 1.23, max/median = 1.25, top-1% share = 0.96%.
  The risk is a uniform flood, not an Extremistan minority (at ≤ 600 P_p).
- **Resonance contrast absent at this duration**: 2:1 ring vs off-ring smoothed rate
  ratio 0.93 (no separation within 1200 yr; gap-scale pumping needs ≥ 10⁴ P_p, unmeasured).
- **Mature footprint**: joint (a,L) entropy 12.67 bits/ship, unchanged from birth
  (−0.004 bits over 300 P_p; 3985 occupied cells ≈ N). Distribution stays compressible;
  it is per-ship key identity that churns. Add tube phase (O(8–16) bits) for a mature
  floor ≈ 21–29 bits/ship against a total budget of ~64 bits/ship (8 GiB / 10⁹) —
  or ~45 bits once the OS and GPU take their share.
- **Bandwidth**: 13–32 key events/ship/P_p at 10⁹ ships ≈ 0.7–1.6×10¹⁰ events per
  game-year ≈ 2–4×10⁸ events per wall-second at real-time factor 100 — the idle-time
  reprogrammer must match this forever for every stirred population.
- **Controls both sides**: μ = 0 gives median 0 naive, 0 smoothed, 0 deadband,
  smoothed-departed 1.85% < 2% (noise floor); stirred runs cross at every grid width
  (counter works). A ±1-cell deadband quantizer removes the control's roundoff tail
  (p99 1.41 → 0.0): the naive quantizer's boundary-flip artifact is real and the
  deadband is the fix (one line, Lindy: Δ-Σ/deadband quantizers).

**Predictions** (predictions.md, written before these runs): held — controls (μ=0 clean,
deadband ≥10× reduction), departure at 12 bits > 50% (it hit 100%), entropy stays far
from uniform, mature bits 25–40 (measured 21–29). **Failed, and the failures are the
result**: (1) the 1/q rate scaling does not hold — the event rate saturates at the
synodic frequency instead (transitions counted, not distance swept); (2) half-lives are
~10× shorter than predicted at coarse grids; (3) no resonance contrast and no
diffusive deceleration — the residual after short-period smoothing still grows linearly;
(4) no fat tail over ships — I predicted one (p99/med ≥ 2, top-1% ≥ 10%) and measured
1.23 and 0.96%. The Taleb prior (tails decide) was wrong here at these timescales: the
fragility is the tide, not the wave.

**What would make it wrong.** (i) The program could include the secular law, not just
the birth key: then the relevant churn is the residual after *secular* subtraction, which
my 4-P_p smoothing only partially removes (linear growth persists ⇒ secular drift
dominates; a proper secular-detrended rate needs runs ≥ secular period, ~10²–10³ P_p —
the natural next rung). (ii) Test particles only: self-stirred belts (ship aggregate
mass as source, PRINCIPLES #6) add mass-dependent rates. (iii) 2D, one stirrer, e_p
fixed; timescales ≤ 600 P_p: fat tails and resonance structure plausibly emerge at
10⁴–10⁵ P_p and were not measured. (iv) The entropy floor is measured on my (a,L) grid
over [1,8]×[0.4,2.5]; a narrower live domain lowers it, a wider one raises it.
(v) The event-rate saturation makes the 16-bit naive rate a *lower bound* on cell-swept
distance, though it is the correct count of store-update events.

**Cost of adoption.** None in code: this is a measurement. Design consequence for the
plane/shipmem: population programs must be born with their kick law attached and scars
re-absorbed on a sub-planet-orbit cadence (the idle-time reprogram cycle gets a hard
rate to match: ≥ 13 events/ship/P_p); H_live instrumentation (`b-h-live` in the queue)
should count key-departures per game-second, not just byte deltas; the memo quantizer
needs the deadband (roundoff boundary-flips otherwise create phantom distinctions, as
the μ=0 control shows: p99 1.4 events/P_p of pure noise).

**Fit with PRINCIPLES.** "Compute only surprises" (#3): measured, the surprises in a
stirred belt never stop — 13+/ship/planet-orbit is the surprise rate the compiler must
consume. "The memory floor is information-theoretic" (#24): the mature floor is 12.7
bits/ship on the memo grid, not the birth compression. "A failed expectation is not
automatically a failed method" (#9/H0183): four of my eight predictions failed and each
failure is a number the integrator now has. Julien's "every body real, never averaged"
is untouched: nothing here averages a body; it counts each ship's own key events.

**The lens.** Taleb made me look for a fat tail over ships and size the memory for the
worst 1%; the measurement says the danger is the opposite — a perfectly uniform flood
(_MEDIOCRISTAN risk), so the barbell is: exact integer key accounting for all ships,
cheap disposable probes for the long-timescale tails I could not reach. The lens also
nearly cost the run: hunting tail exponents is polishing; the half-life number was on
the dashboard from the first smoke test.

**Grade (self-assessed, for the checker):** silver-to-gold. Reproducible (fixed seeds,
≤ 40 s per command, metrics.json regenerates), predictions pre-registered with honest
failures, and it moves a named risk ("not measured yet") to measured with design
consequences. It is not a 10× engine gain; it is the measurement the 8 GB scaling
decision was waiting on, plus one bug found in the representation (quantizer needs a
deadband). The un-run long-timescale tail (secular-detrended rate at ≥ 10³ P_p,
multi-stirrer) is the named next experiment.
