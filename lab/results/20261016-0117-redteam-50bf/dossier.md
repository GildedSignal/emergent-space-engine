# 20261016-0117-redteam-50bf — the multiply-add cycle update breaks on the separatrix family

## Claim

The design's kick-update clause ("a kick updates the cycle by a multiply-add",
representation.md §3) is certified only on the bulk: measured error ≈ κ·ε² with
κ ≤ 2 for p ≥ 20, e ≤ 0.9 (encounter-class kicks ε = 10⁻² err ≤ 2×10⁻⁴; the
belt's tide size 2⁻²³ is ≥ 7 orders below every bar) — but κ diverges as
δ^−2.5..−3.5 toward the Schwarzschild separatrix (δ = p−(6+2e)), so a
0.1%-of-L kick at δ = 0.2 errs 18.5% on the advance and 1.1% on the period,
and the design's own named use case (Peters inspiral as kicks) is mispredicted
by 25% in merger time from four kicks (p₀ = 12, e₀ = 0.6), with stale
derivatives the cycle goes nonphysical mid-inspiral (proper-time increment
negative). No rung, gate or shipped test builds the multiply-add path at all.

## Bottleneck

The board's kick wall ("75–160 µs against a ~50 ns floor; the cheapest exact
kick on the shipped representation"): the multiply-add is that 50 ns candidate.
This run does not delete it — it bounds its certified domain and hands the
compiler a derivable recompile trigger (κ·ε² ≥ bar), which at belt scale fires
never (κ ≤ 2, δ ~ 10⁹ M) and near the separatrix fires exactly where the
shipped compile already concentrates its cost (the e ≥ 0.9 band,
closed-form-kernel page). Gain: the difference between adopting the
multiply-add blind (wrong on the GR showcase orbits) and adopting it with a
trigger (exact everywhere the bar demands).

## Evidence (float64, Linux/x86, `regen.sh` ≈ 2.5 min; every number below is in its output)

Instrument: exact Schwarzschild equatorial cycle increments C(E, L) =
(Δφ, Δt, Δτ) by quadrature (turning-point substitution), Darwin (p,e) ↔ (E,L)
exact via the two turning points; kicks ε_E = fraction of binding energy
(1−E), ε_L = fraction of L. Controls (all green, `falsifier.py validate`):
circular orbits exact to 2×10⁻¹⁴; κ_E → 15/8 = 1.875 (Kepler, t/τ channels
measure 1.873/1.875 at p = 1000, 1.856/1.871 at p = 100 — the 1PN correction
shrinks as expected); κ_L on the advance tracks the 1PN form 18/(2L²+6) to 3%
at p = 1000; quadrature stability 1×10⁻¹¹; the multiply-add floor from
derivative roundoff is ~10⁻⁴·ε (classified by the ε-sweep: the t channel
scales ×100 per ε-decade exactly — 1.83e−8, 1.87e−6, 1.87e−4, 1.81e−2 at
p = 1000 — so ε²-signal and floor are cleanly separated).

Sweep (`falsifier.py sweep`, 285 usable (p, e, ε, direction) rows,
sweep.json):
- **Bulk holds**: worst error at ε = 10⁻² over p ≥ 20, e ≤ 0.9 is 1.94×10⁻⁴
  (advance, p = 20, e = 0.9, L-kick) — κ ≤ 2. At the belt's fired impulse
  (2⁻²³ of speed, 3294/f82a) the error is κ·ε² ≲ 10⁻¹³: the premise holds
  with ≥ 7 orders of margin everywhere the belt lives.
- **Separatrix law**: at ε = 10⁻², fitting err ~ δ^−α over δ ∈ [0.2, 13.4]
  gives α = 3.47 (advance, E-kicks), 2.45–2.48 (advance, L/EL), 3.23/1.87
  (period, L/EL), 3.35/1.75 (τ, L/EL). The advance is the worst channel near
  the boundary (err_φ/err_t up to 31 at δ ≤ 0.5) — not the period.
- **Bar crossings**: the 10% precession bar breaks at (δ = 0.45, ε_L = 10⁻²,
  error 120%) and (δ = 1.4, ε_E = 10⁻², 1.7×10⁻³ rising); the 0.1% period bar
  at (δ = 0.45, ε_L = 10⁻², 57%). At ε_L = 10⁻³: (δ = 0.2) advance 18.5%,
  period 1.1%, τ 0.6% — every bar broken by a kick one hundredth of the
  showcase encounter size.

Chain (`falsifier.py chain`, Peters secular kicks per cycle, ν = 0.25, M = 1;
recompile arm = the shipped plane's path, exact C per kick):
- p₀ = 20, e₀ = 0.3 (25 true cycles to the separatrix): multiply-add with
  derivatives never refreshed runs off the physical sheet — the τ increment
  goes negative, 5000 "cycles" without merger, phase total 200× the truth.
  Refresh-every-8: cycle count 26/25, but merger time +0.1%, phase +3.5%
  (7.1 rad — more than an orbit), and with kicks sized identically in all arms
  (shared-kick arm, pure representation error) merger time −3.0%, τ −3.2% —
  30× the 0.1% bar.
- p₀ = 12, e₀ = 0.6 (4 true cycles): every multiply-add arm errs −25% in
  merger time, −28% in τ, from four kicks (refresh never even engages); the
  error concentrates in the final cycles, exactly as κ(δ) predicts.
- The three channels are wrong together: err_τ/err_t spans 0.5–1.9 (τ is not
  spared; "a clock reads its tube's length" inherits the walk).

Predictions (`predictions.md`, written before the decisive run): P1 (bulk
κ ≤ 5 at encounter sizes) **held**; P2's divergence α ∈ [1,3] **held** at the
top of the range (3.47 on the advance, E-kicks), but P2's held-out sub-case
(advance stays below period near the separatrix) **failed** — the advance is
the worst channel; P3's "refresh-64 holds to <0.1%" **failed** (1.1% at
p₀=20, −18% at p₀=12 before any refresh engages); P4 (τ ≤ t) **failed**
(τ/t up to 1.9); P5 (κ monotone in e) **failed** for the t channel (κ_t falls
10.7→2.0×10⁻⁴ across e at p = 10; the structure is set by δ and p, not e).
The kill criterion that fired: "the premise is domain-limited, not wrong" —
with the domain boundary measured, not assumed.

## What would make it wrong

The instrument is float and standalone (the multiply-add path exists nowhere
in shipped code — that is the finding, not a shortcut): its cycle quadrature
and κ coefficients are validated against Kepler and 1PN closed forms (above),
and the ε²-scaling is clean where signal sits above floor. It would be wrong
if the shipped integer law's kicks near the separatrix were somehow smaller
than encounter class — but the design's own inspiral case has ε per cycle
O(0.1) at the end, and m-meso-motion's adopted close-encounter event is a
large kick by construction. Cost of adopting the trigger: one rule in the
compiler (recompile when ½|C_LL|ΔL² + ½|C_EE|ΔE² crosses the channel bar; both
coefficients have closed forms validated here — 15/8 and 18/(2L²+6), or read
them from the compile's own derivatives), zero extra recompiles at belt scale,
recompiles concentrated where compile cost already peaks. Fit with PRINCIPLES:
13 "Errors never compound" — the multiply-add's error is one-signed and walks
(the stale chain's τ goes negative); 2 "error type over error size" — the
failure is a systematic bias, not rounding; 21 "rough first, refine when a
certificate could break" — κ·ε² is that certificate, now measured.

## The ranked attacks (the lens's deliverable; #1 executed here)

1. **The multiply-add cycle update (this run)** — breaks on the separatrix
   family and the named inspiral case; **no rung builds or guards it** (r1 has
   no kicks; r2 stores increments, never updates them; r3 judges handoffs and
   assists, not in-cycle updates; B13/B14 judge the plane's rebind-per-kick
   path). The Floquet tide certificate (3851/0d8c) sits downstream of it.
2. ν-blindness of the two-body doll — adjudicated (97b0): the premise holds in
   its certified domain p̄ ≥ 65M; B11's oracle was the defect. Caught by the
   r3-family oracle work — guarded now.
3. Binet band-centre first-order error on near-circular orbits — measured
   (fe85): m = 32 or a per-orbit u_k refit is the minimum; r1's sampler draws
   the family rarely — the re-freeze open direction covers it.
4. "Dense order bit-identical to sparse" — refuted at column level (8398,
   taleb-292a, b9c8: the w lottery); r5 was never frozen — **no rung**.
5. "Crosses once" / flat light time in the view — refuted (6eae, ace6, 5977);
   r6 was never frozen — **no rung**.
6. "Undisturbed orbits cost ≈ 0" — the flown plane fires 1.000 (3294): no
   undisturbed regime exists at the shipped grid; deferral certificates dead
   (e5a2, 67f2); guarded only by cost measurements, no behaviour rung.

A premise that survives is worth reporting too: the bulk belt (attack #1's
positive half) and the two-body doll inside its domain (#2) both survived
their strongest measured attacks.

## The lens

Red-teams overweight exotic cases: I ranked by player visibility — the
separatrix family is not exotic here (near-BH eccentric orbits are the GR
showcase the goal names; inspiral is the design's own listed perturbation),
but the bulk-survival half is the result most likely to be adopted, and I put
it first in the claim. What this lens may have missed: the integer law's own
quantization could mask or amplify the float failure (the carried error budget
is one floor unit per event — a one-signed κ·ε² walk above the quantum is
exactly what the carry cannot hide); and I did not test kicks at random
phases of the cycle (the design's kick windows are periapsis/conjunction
anchored; my kicks are invariant-space, which is phase-free and therefore
favourable to the multiply-add — the phase-anchored variant can only be worse).
