# dossier.md — 20261013-2005-scout-d947 (scout lens)

## Claim

The gravity-news payload is decided by the literature and by measurement: the retarded
field of an arbitrarily thrusting source depends on retarded **(x, v, a) only — never
on jerk** (Kinnersley's photon rocket via Carlip 1999, read at source), so the version
must carry the source's **total acceleration**; with that slot, a constant burn leaves
the consumer at the machine floor, the residual is the jerk-staleness of the a-slot
itself (scar ∝ j·T^3, measured exponent 3.15–3.98), and **no jerk slot is needed at
game cadences** — at kick cadence (T = P/32) and the hardest consumer (β_c = 0.3) the
jerk residual is 1.8×10⁻⁸ per rebind, ~50× under a 10⁻⁶-class budget.

## Bottleneck

`gravity-news` open direction 3 (7ab4): "a causal oracle would fix the required payload
(acceleration vs jerk) — unmeasured". This is the payload half of "gravity is news"
(law.md:33), Julien's insisted-on foundation, and the same one slot the burn carry and
the view's field term ask for (frame-cost 2964: "one adoption, three bottlenecks").
Gain: deletes the burn-channel scar outright (measured here 10⁸–∞× at constant thrust;
3.4×10³× vs the as-if-now readout at kick cadence, β 0.3, jerk on) and freezes `r-news`
with numbers instead of a guess. It deletes nothing else: the cursor cost is already
solved (05b0, e300).

## Evidence (all from `regen.sh`, ~20 s, pure stdlib)

Toy = Carlip's Lorentz-invariant scalar retarded force (gr-qc/9909087 §3 eq. 3.1,
verbatim structure), source on x(t) = ½a₀t² + jt³/6, consumer circular at
β_c ∈ {0.003, 0.03, 0.3} (7ab4's range), versions every T, RK4 h = P/1024
(step control ratio 0.98), scar = per-rebind |ΔE| vs the perfect-news oracle arm.

- **The a-slot is exact for constant thrust:** payload (x,v,a) with j = 0 → scar
  **0 / 8×10⁻²⁰ (floor)** at every T, every β; payload (x,v) at the same scenes:
  1.3×10⁻¹²…1.4×10⁻⁷, T-exponent 2.19–2.99 (the ½aΔ² position remainder through the
  tidal channel — my predicted δv/T² band [1.9,2.6] was low, see Predictions).
- **The jerk residual is one order higher:** with j ≠ 0 the (x,v,a) scar is
  1.9×10⁻¹⁴…2.6×10⁻⁹, T-exponent **3.15–3.98**; (x,v) exponent minus (x,v,a)
  exponent = 0.90–0.98 (just under the full order I predicted).
- **The jerk slot is provably dead weight at game cadence:** payload (x,v,a,j) =
  **exactly 0** even with jerk (the cubic-program exactness control — this control
  caught a real bug in my first build, see Predictions).
- **Free fall:** every payload exact (0.0) — the cancellation control.
- **The shipped-style readout quantified:** an as-if-now readout (newest *arrived*
  version read as current) scars ∝ a·T per rebind (slope ≈ 1) and its **total scar per
  orbit is cadence-invariant** (7.7×10⁻⁴ flat across T = P/256…P/8 at β 0.3) — 7ab4's
  "rekeying faster buys nothing" is the total; the fix is not cadence but payload+readout:
  at T = P/32, β 0.3, jerk on: now-readout 6.2×10⁻⁵, (x,v,a) retarded 1.8×10⁻⁸
  (**3,400×**).
- **T\* window:** at β 0.3 the jerk residual crosses 10⁻⁶ only at T ≈ P/6.5; the plane's
  kick-like P/32 holds 50× margin.
- Sign control |scar(+j)|/|scar(−j)| = 0.67–0.72 (sign flips, magnitude asymmetry from
  burn-vs-orbit-phase geometry, disclosed).

Source, read at source: S. Carlip, *Aberration and the Speed of Gravity*,
arXiv:gr-qc/9909087 (§2: the Kinnersley connection "depends only on the retarded
position, velocity, and acceleration of the source", eq. 2.4–2.5 quadratic
extrapolation; §3: the scalar force used as the toy's field). This grounds 7ab4's
½aT² finding: thrust is exactly the part of a source's motion the aberration
cancellation cannot absorb, because the cancellation uses the (gravitational) EOM.

## Predictions

`predictions.md` was written before the corrected decisive run. Held: the a-slot floor
(P2, including ≥5 orders), the O2 exponent band [2.9,4.1] (P3), the free-fall control,
the sign flip (P6). Missed, all reported: P1's O1 exponent band (measured up to 2.99 —
the tidal channel dominates beyond my model), P3's jerk-linearity (0.77 effective over
a decade, not 1.0±0.1 — the amplitude sweep co-scales the source's displacement),
P4's coefficient transfer from 7ab4's 0.7·β²/2·δv form (C = 0.004–0.038, spread 10× —
the toy's channel is tidal, not δv), P5 as written (per-rebind slope ≈ 1, not ≤ 0.2;
reconciled by the total-scar invariance above). Two instrument bugs were caught by the
run's own controls before any number was used: a scalar jerk applied isotropically
(exposed by the O3-exactness control failing) and an as-if-now readout using un-arrived
versions (exposed by the cadence-invariance control). The first, buggy execution's
numbers appear nowhere.

## What would make it wrong

The toy is planar, scalar-gravity, β ≤ 0.3, windows ≤ P/8, one thrust geometry; the
coefficient forms (not the exponents, not the floor) are toy-specific — P4's miss is
the proof. The strong-field question 7ab4 left open (r = 20M consumers; whether the lag
channel beats the direct tide there, where Carlip's O(v²) ε₁, ε₂ terms also grow) is
untouched. The plane cannot yet express these scenes at stellar scale (e300 E3), so the
wired test waits on expressibility; until then the numbers bind the design, not the
engine. Cost of adoption: one payload slot + a quadratic readout (≈2 multiply-adds,
7ab4's price) — the shared slot two other bottlenecks already requested.

Fit with PRINCIPLES: #23 "Nothing past c… even gravity is light speed" — the retarded
readout is the causal half made cheap; #3 "Compute only surprises" — (x,v,a) is the
minimum broadcast that makes the consumer exact between surprises (Kinnersley's data);
#21 "Rough first, refine when a certificate could break" — carry (x,v,a), refine
cadence only if the jerk residual crosses the quantum, which at game cadences it does
not. Free fall stays free (the tube travels) — #6 "Store the generator, not the
generated".

## The lens

The scout trusts the literature's framing of the requirement; here that is a feature
(Kinnersley fixes the payload) but the same trust produced P4's miss — I assumed 7ab4's
plane-measured coefficient would describe a toy with a different dominant channel. A
builder lens would have wired the slot into `crates/space` and measured the plane's own
digest instead of a toy's; that build is the named next step, and it needs scenes the
plane cannot yet express (e300).

## Files

`falsifier.py` (sweep), `probe_floor.py` (floor probe), `analyze.py` (tables),
`results.json`, `analysis.txt`, `probe_floor.txt`, `predictions.md`, `regen.sh`.
