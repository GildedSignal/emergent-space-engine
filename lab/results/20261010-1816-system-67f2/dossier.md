# Dossier — one renewal quantum? The impulse side is killed; the split rule stands

Run: 20261010-1816-system-67f2, lens: the whole system. Host: GitHub Actions Linux,
8 vCPU, load 3.0, ~13.8 GB available; pure-Python replica, trivial memory (< 50 MB).

## Claim

The plane's three renewal mechanisms (rebind-on-every-kick, the cycle memo's re-anchor
threshold, the encounter certificates' slack skin) are **not** one mechanism at the physics
layer: deferring the kick's *application* into an exact accumulator — the tempting unification
under principle 6 ("influences below one quantum accumulate") — is **killed**: it converts
bounded magnitude error into secular *timing* error (energy growth exponent 1.0, the forbidden
error type). What survives, now measured, is a **split rule**: the exact state is updated at
every kick (timing may never slip), and only *derived structures* (the compiled cycle, the
candidate pairs) may be renewed at magnitude thresholds — which is exactly where the jet's
re-anchor (0.05 compiles/kick) and the slack skin (12.6×) already live. Two mechanisms are one;
the third must never be.

## Bottleneck

"Fewer kicks per orbit" / "no work per orbit in the steady state" (board focus 1 and 3). The
temptation this run kills: making bindings cheaper by not applying small kicks. Expected gain
had it held: renewals per orbit → |secular drift|/q instead of 64. What it deletes instead:
any future impulse-deferral patch on the kick path, and the ambiguity about where the renewal
quantum belongs.

## Evidence

Float replica of the plane's kick layer (`deferral.py`; floats explore, they decide nothing
canonical): restricted circular three-body (Sun μ=1, Jupiter μ=10⁻³ at 5.2), Wisdom–Holman
split with **exact** Kepler drift (E error 0 after 1000 periods), kick = the perturber's
difference acceleration at the interval midpoint, 64 kicks/orbit — the plane's own cadence and
structure (crates/universe/src/step.rs). Truth: immediate at 1024 kicks/orbit. 1000 orbits,
marks every 5.

Scene A, a=2, e=0.05 (off resonance):

| config | renewals/orbit | max\|ΔE\| | exponent |
|---|---|---|---|
| immediate (the plane) | 64 | 8.2e-7 | 0.07 |
| deferred q=8.6e-6 | 36.4 | **1.3e-3** | **1.01** |
| deferred q=3.5e-5 | 10.9 | 8.8e-3 | 0.98 |
| deferred q=1.4e-4 | 2.9 | 6.5e-3 | 1.01 |
| deferred q=5.5e-4 | 0.04 | 6.4e-3 | 1.07 |
| discard q=3.5e-5 (control) | 64 | 1.6e-3 | 0.06 |
| immediate@16 | 16 | 7.0e-6 | 0.15 |
| immediate@8 | 8 | 2.6e-5 | 0.07 |

Convergence probes (no bug): deferred q=1e-9 and 1e-7 give exactly immediate's 8.23e-7,
exponent 0.07; discard q=1e-7 → 5.8e-6 (exp 0.21), q=1e-6 → 1.1e-4 (exp 0.56, the walk).
So: **impulse deferral walks linearly at every q that saves renewals; dropping the residue
while applying on time stays bounded.** Coarsening cadence (immediate@8) beats deferral at
equal renewal count by ~50× in error. Mechanism: the accumulator crosses just after the tide's
force peaks, so each deferred impulse lands systematically late; a late impulse changes E by
ΔE ≈ a·Δv·δt with consistent sign — secular. Magnitude error dithers; timing error drifts.

Scene B, the hard case (2:1 resonance, a=5.2·2^(−2/3), e=0.02, truth 512/orbit): even the
mildest deferral (25.6 renewals/orbit) pumps e to 2.19× immediate's; larger q gives 1.8–7.2×
and the resonant angle's winding changes sign and magnitude (−86.9 → +58.8). The resonance
selector that law.md already mandates for averaging is load-bearing for any future deferral.

Reproduce (each ≤ 60 s on this host):

```
cd lab/results/20261010-1816-system-67f2
python3 deferral.py deferral.json          # both scenes, ~11 s
python3 - <<'EOF'                          # convergence probes, ~6 s
import deferral as d
marks = list(range(1, 1001, 5))
ren, tout = d.run(2.0, 0.05, 1000, 1024, "immediate", None, sample=marks)
for mode, qv in [("deferred",1e-9),("deferred",1e-7),("discard",1e-9),("discard",1e-6)]:
    ren, out = d.run(2.0, 0.05, 1000, 64, mode, qv, sample=marks)
    dE=[abs(a-b) for a,b in zip(out["E"],tout["E"])]
    print(mode, qv, ren/1000, max(dE), d.growth_exponent(tout["t"], dE))
EOF
```

## Predictions (predictions.md, written before the run)

Held: #4 (resonance distorts the pump, 2.2–7.2×; selector load-bearing). **Failed: #1–#3** —
renewal collapse came only with linear E growth (the pre-registered kill criterion fired:
"does NOT hold energy bounded … the one-mechanism claim dies for bindings"). A surprise
against my own expectation: the discard control stayed bounded (0.06) where I predicted a
walk (≥ 0.4); the walk appears only at smaller q (0.56 at 1e-6). The split is not defer vs
discard but **timing vs magnitude**.

## What would make it wrong, cost, fit

Wrong if: the integer law's own variables (E, L kicks rather than velocity impulses) can be
deferred without secular timing error — i.e. if averaging theory (H0190) already is that
deferred form in the correct variables. That is exactly how law.md treats stable orbits
(orbit-averaged kicks, r4's resonance guard), so the surviving statement is consistent with,
and now motivationally grounded in, the adopted design. Cost of adopting the split rule: zero
code; it *removes* a tempting patch class and tells the integrator the renewal quantum has one
home — the certificate side (jet re-anchor, slack skin), never the impulse side. Fit:
principle 2 ("error type over error size" — this run is a pure error-type result), principle 9
("a failed experiment kills that configuration, never the method"), principle 6 (the
accumulator belongs on influences that *accumulate* — mass moments, sub-floor perturbations —
not on impulses whose phase carries energy), and engine.md's error model ("secular drift:
forbidden" — measured, not assumed).

## The lens

The whole-system lens found its unification and it died on the table — which is the lens
working: the elegant "one quantum everywhere" hid the hard special case (impulse phase), and
naming it sharpened the architecture instead of patching it. What this lens may have missed:
the replica is Newtonian, 2-body drift, one perturber, e ≤ 0.05, no GR; a GR-native kick
(clocks, tides in Fermi frame) could couple timing and magnitude differently, though nothing
in the mechanism (phase of application vs force peak) is Newtonian. Also untested: deferral in
element space with the kick's *secular* part separated first — but that is H0190's averaging,
already adopted with its resonance guard, not a new mechanism.
