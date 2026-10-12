# dossier.md — 20261006-1135-scout-7a46 (scout lens)

## Claim

The conic representation's singular set — radial (L = 0), plunge/no-turning-point,
and near-radial states, exactly where the engine refuses (`NoBoundOrbit`) and
Julien's ship froze in flight — is served exactly, and at event cost independent
of depth, by the square-root generator the 2D plane already hints at: Levi-Civita
`z = u²`, `dt = |u|² dτ`, `u'' = (E/2) u`, one closed formula for bound,
parabolic, hyperbolic, radial and r → 0; the stepping fallback needs 18–93× more
events at matched error by q = 0.003 r_H and produces garbage (rel. err ~190) or
never terminates on the singular set.

## Bottleneck

The motion law v2's open completeness hole (HANDOFF: "plunge and radial orbits
have no tube (`NoBoundOrbit`)"; `crates/space/examples/certified_bank.rs:27–29`
lists "radial paths (L = 0), plunge and horizon times, outgoing escapes with no
turning point" as "not supplied by the law"). The refusals fire in
`binding.rs:196–248` (`vt.is_zero()`, `disc.is_positive()`, root-search
exhaustion), `kicks.rs:157–176`, `orbit.rs:59–60` (e ≥ 1), `lib.rs:188+`. This
is the live freeze a player hits. Expected gain: unbounded on that set (> 62,500×
measured, i.e. no α in the sweep matched), 18–93× at matched error across two
decades of encounter depth; and it deletes the need for any stepping fallback
there. It also answers the opus-motion memo's open "whether a bit-reversible
drift exists cheaply" for the unbound branch: the drift becomes an integer phase
accumulator (R1's numerically-controlled-oscillator pattern), exact under
repeated addition and subtraction.

## Evidence (float falsifier; `python3 falsifier.py`, 6–7 s, < 50 MB, this folder)

Scene: the planet's doll. μ_p at origin, parent M = 1 on a circle R = 1, n = 1,
r_H = 0.03, entry 0.98·r_in, r_in = 0.4 r_H. **C** = exact LC drift + K tide
kicks only (Strang; the kick is v2's own `w = Δs·f'(U)` shape). **A-rt** =
velocity Verlet, monopole + tide, dt = min(cap, α·r), α = 0.2 locked on one
calibration case (q = 0.1 r_H, v∞ = 0.7 v_H). **A-fix** = constant dt (the
OM_FIXED_STEP ablation). Truth: DOP853 rtol 1e-12 (with-tide), exact
symmetry+quadrature for the no-tide radial cases (DOP853 itself **cannot
integrate through r = 0** — "required step size is less than spacing between
numbers" — while LC passes it as a straight line; the regularization claim made
literal). Cost unit = events (kicks vs steps).

| case | C no-tide | C K=8 | C K=16 | A-rt (α=0.2) | A-fix | cost A/C at matched err |
|---|---|---|---|---|---|---|
| q0.3 v0.3 | 5.0e-13 | 6.7e-4 | 6.2e-4 | 2.1e-4 | 2.3e-5 | 18× |
| q0.1 v0.3 | 2.1e-12 | 1.6e-3 | 3.8e-4 | 9.5e-5 | 3.5e-4 | 26× |
| q0.03 v0.3 | 9.4e-13 | 2.0e-3 | 4.8e-4 | 1.8e-4 | 1.3e-2 | 28× |
| q0.01 v0.3 | 2.9e-12 | 2.0e-3 | 5.1e-4 | 9.0e-4 | 3.5e-1 | 29× |
| q0.003 v0.3 | 7.4e-12 | 2.0e-3 | 5.1e-4 | **1.5e-2** | **4.3** | **93×** |
| q0.3→q0.003, v0.7 | same pattern | | | 2.1e-4→1.5e-2 | 2.2e-5→4.2 | 18×→93× |
| thru (bound radial, E<0, L=0, through r=0) | **1.2e-15** | 1.1e-3 | 2.8e-4 | **1.9e+2** | 1.7e+1 | > 62,500× |
| par (E = 0 exactly, L=0) | **3.5e-16** | 2.0e-3 | 5.1e-4 | **1.9e+2** | 6.2 | > 62,500× |
| hit (v∞ = 0.3 v_H, to r = 1e-4 r_H) | 6.2e-10 | 1.6e-2 | 4.0e-3 | **2.6e+9, step cap** | 1.9e+8 | (A never terminates) |
| near-radial (q ≈ 3e-6 = 0.1 r_surf) | 6.6e-10 | 2.0e-3 | 5.1e-4 | **2.4e+1, step cap** | 1.2e+1 | 350× |

- C's two-body part is exact to 3.5e-16…7.4e-12 at **every** depth including
  L = 0, E = 0 and through r = 0; its only error is the tide kicks, second
  order (6.5e-3 → 1.6e-3 → 3.8e-4 at K = 4/8/16 on the calibration case).
- C's cost is K events per encounter **independent of depth** (8–16); A-rt's
  error at fixed rule grows 70× from q = 0.3 → 0.003; A-fix grows five orders.
- Truth quality: with-tide DOP853 at rtol 1e-12 vs 1e-14 agrees to 9.2e-9
  (thru), 8.4e-9 (par), 3.9e-10 (near-radial) — below C's errors there.
- Known convention, disclosed: at exactly L = 0 the continuation through r = 0
  is a choice; the regularized flow is the elastic bounce (classical LC). Both
  conventions coincide for L ≠ 0; physically these states end at a surface or
  horizon anyway.
- Machine: shared Linux runner, 8 vCPU i7-4790, 15 GB, idle-ish; runtime 6–7 s;
  orders of magnitude only (lab rule).

## Predictions (predictions.md, written before the grid; one calibration case)

Held: (1) no-tide control ≤ 1e-12 everywhere ✓ (3.5e-16…7.4e-12); (3) A-rt's
error at fixed α grows ≥ 10× ✓ (70×); (4) cost-to-match ≥ 10× ✓ (18–93×, and
>62,500× / non-termination on the singular set); (5) C passes r = 0 at ~1e-15
with zero force evals, A-rt passes with err ~190 ✓, engine freeze is a refusal
cited from code ✓. Boundary: (2) C's K=8 error grew 3.04× from q = 0.3 → 0.003
against my "~3×" (K = 16 is flat, 0.85×); (6) measured cost-to-match exponent
−0.36 vs my amended window [−1, −0.4] — marginally outside, and my original −1
guess was wrong exactly as the addendum suspected. My pre-run belief that A-rt
would stall (original prediction 5) was wrong in an informative way: it does not
merely slow down, it goes unstable (err ~190) or wanders past the step cap.

## What would make it wrong

- **Strong field.** The oscillator is Newtonian. For Schwarzschild/Kerr the
  analogue must be a phase drift over Darwin's ψ (already the crate's radial
  variable) — same pattern, different integrand; not shown here.
- **Integer law.** Kick linearity in u', exactness of the phase accumulator and
  table cos/sin are float-verified only; the JANUS-style bit-reversible integer
  form is designed, not measured.
- **Non-smooth tides in τ.** Long captures with resonant tides (B13's deep
  regime) may need K to grow with duration; untested.
- **Multiple secondaries.** "One dominant mass per doll" is v2's existing
  selector; not exercised here.

## Cost of adoption, and fit with PRINCIPLES

Adoption is local and additive: an unbound/radial drift branch in the secondary's
doll (`crates/space`), reusing v2's kick machinery and R1's integer phase +
cos/sin tables; nothing is deleted on the bound branch. It directly unblocks
Astra's open items "plunge and radial orbits have no tube" and the in-flight
freeze. Quotes: "if you find yourself fixing things that's oftentimes a signal
that it is the wrong representation" (#19 — the refusals are such a signal);
"compute only surprises" (#3 — zero events between tide kicks); "errors never
compound" (#13 — drift exact at any depth; error only in second-order kicks);
"physics loves e while we love 2" (#16 — the LC map is a square root, the
oscillator a rotation; the phase accumulator is exact integer addition).

## The lens

Scout's prior art: the mechanism is classical (Levi-Civita/Bohlin; the repo's
own opus-math memo line 63 states E is exactly this oscillator's angle, and
Julien's pre-pivot conversation, `docs/reference/original-conversation.md`
8129–8145, already called LC "exactly your make-geodesics-trivial instinct" and
the 2D gift). Living practice: universal-variable Kepler solvers (Wisdom 2015,
"A Fast and Accurate Universal Kepler Solver without Stumpff series",
arXiv:1508.04099 — verified as a listing, contents UNVERIFIED). UNVERIFIED from
memory: Preto–Tremaine/Mikkola–Tanikawa details (cited in the memos), ARCHAIN,
KS. What the lens may have missed: the novelty is narrow — the math is 1911; the
run's value is the measured demonstration that the opus-math memo's rejection of
LC-as-drift ("fictitious time must be mapped back by Kepler's equation anyway,
which R1 already gives") holds only on the **bound** branch, and that its other
reason ("the planet's doll is already the regularized frame") regularizes the
origin, not the conic's discriminant — the certified bank's own unsupplied list
is precisely the residue. I searched lightly (two queries); the strong-field
GR extension and the integer implementation are the two open follow-ups, the
first of which belongs with the ψ machinery its owner (Astra) already holds.
