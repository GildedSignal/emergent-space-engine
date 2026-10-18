# Run 20261018-0543-taleb-6de0 — the μ = 1e-2 runaway tail is an event storm of the root clock, not captures

## Claim

The plane's μ = 1e-2 runaway tail (chaos-shadowing's open direction 3) is **a genuine event
storm of the root clock on slingshot ejections — not captures and not the planet doll's
octave**: a real encounter ejects the body, the clock's far-field kick keeps paying a
one-signed Δv per kick (6.5e-7, every kick, no sign change) that mints β = 0.2 (2.1×10⁷
times the orbital kinetic energy; physically impossible at this mass ratio), the drift
interval then collapses as **dt = A/y with A constant to 1.4% and y = v²/2**, the event
rate grows as v², and the clock freezes: the last 25,600 kicks advance simulated time
7.5×10⁻⁹ planet periods. 10 of 144 co-orbital ICs lock this way within 16 P, holding 52%
of all ensemble events, each unbounded (the 16 P horizon is unreachable at any budget).
μ = 1e-2 is not flyable as built, and the arithmetic is μ-independent — the mass gates
only the arrival rate (0 storms at μ = 1e-3 in 64 P, the same instrument).

## Bottleneck

The board's smoothness/allocator question behind the wiki's direction 3 ("decides
whether μ = 1e-2 is flyable at all"). Answered: this is ruin, not a tail — the allocator
cannot schedule around a frozen tick, so no scheduling work at μ = 1e-2 pays until the
law changes. Gain: deletes the "capture cascade / octave" hypothesis line and points the
fix at one object (the clock's y and its far-field kick weight), not at encounter tiers
or doll octaves.

## Evidence

All from the shipped plane through its public API (`crates/universe`), scene and units
exactly the behave adapter's (`xtask/src/behave/plane.rs`); the only edits are an
env-gated per-kick telemetry tap (`crates/universe/src/trace.rs`, off unless
`KICK_TRACE` is set) and the driver `crates/universe/src/bin/tail.rs`; caps are the
public `Universe::advance(target, Budget::events(n))` loop, which preserves canonical
bits. Ensemble: 144 ICs, circular heliocentric orbits at a = sep + du·Hill (du ∈
[−1.5, 1.5], 12 values) × φ ∈ [60°, 180°] (12 values); scene sep = 5.27e8, planet radius
4.84e4; `step_log2` = 7 (the default). Linux/x86 cloud box, 8 vCPU: orders of magnitude
only.

Commands (from the repo root, `cargo build --release -p emergent-universe --bin tail` first; full regen: `lab/results/20261018-0543-taleb-6de0/regen.sh`, ~9 min):

- `sh lab/results/20261018-0543-taleb-6de0/screen.sh 0.01 16 100000 work/screen-m2-16` (~30 s):
  144 ICs, 16 P, event cap 100k → **10/144 capped (52.3% of all 1.98M events), 9 dead,
  median uncapped IC 7,329 events (230 kicks/P — the wiki's 231 reproduced)**. Capped
  ICs' cost curve (grinder du=−0.68, φ=81.8°): events/P walks 424 (1.5 P) → 676 (8.5 P)
  → 964 (9.5 P) → 400,000 (10.2 P, the lock). Per-event cost 53 µs uncapped → 121 µs
  in the grind (×2.3).
- `sh screen.sh 0.001 64 100000 work/screen-m3` (~3 min): **the control at μ = 1e-3 with
  16× the horizon: 0 capped, top IC 0.9% of events, median 276 kicks/P (the wiki's 267),
  10 dead** — the fat tail is μ-gated, the instrument matches shipped-code history.
- Deep traces (`KICK_TRACE=... tail 0.01 DU PHI 16 1500000`, ~3 min each, 3 ICs; plus 5
  capped ICs at 160k, ~1 min; and one at 600k with y traced):
  **every capped IC ends ejected at 9.2–19.0 sep from the star (8.5–18.2 sep from the
  planet), never inside 42 R_p at any traced kick, doll 0 throughout, handoffs = 0** —
  not captures. The storm tail (IC du=+1.5, φ=169.1°, v > 0.15, 4,700 samples):
  `dt·y = 2.60–2.64` (constant to 1.4%; the shipped constants give Δs/b = 3.69,
  same form, my c estimate is the 30% error), **y = v²/2 to 0.2%**, **dv/kick =
  6.52e-7 with zero sign changes**, v 0.150 → 0.199 over the tail, interval 232 → 132
  ticks (the 1.5M-event run reaches interval 22; another IC 10), and the last 25,600
  kicks advance the clock 579,431 ticks = **7.5e-9 P**. The ejection energy is minted:
  β = 0.199 against a system whose circular speed is 4.35e-5 and whose planet-surface
  escape speed is 6.4e-4 — 2.1×10⁷ times the orbital kinetic energy; no three-body
  slingshot at μ = 1e-2 does that, and the judge's own truth side (80fe: 32 disk
  crossings, no ejections) never shows it.
- `python3 lab/results/20261018-0543-taleb-6de0/analyze.py` prints every number above
  from the saved runs.

Mechanism (measured, closed by shipped constants, `crates/universe/src/ext.rs`): the
clock's two branches both fail on a positive-H_D body. (1) The kick weight
w = Δs·f′(U_P + c) far from the planet sits on the 1/y² branch with y → c, so it pays a
≈ constant one-signed Δv per kick at any distance (the frozen clock freezes the planet
too, so the direction never rotates — on a bound orbit kicks average over the orbit; on
an ejection they ratchet). (2) The drift step dt = Δs·f′(H_D + p_t + c) with H_D = v²/2
now ≫ c sits on the 1/(b·y) branch: dt = (Δs/b)/y, so the event rate grows as v² while
the ratchet grows v — positive feedback, finite-time freeze, then an eternal grind at
≥ 1 tick/kick (`Ext::ticks` clamps at 1; `MIN_STEP` never applies to `kick_clock`'s own
step). The guard in ext.rs clamps y only from below (c/8); nothing clamps it from above,
and the constants (Δs, c, b) are derived once at birth and never again.

## Predictions

`predictions.md` was written before any ensemble run. Outcome: **P1 refuted** (the
grinders are ejected bodies at 8.5–19 sep, not captures — the wiki's own leading
hypothesis, "captures → ever-shorter radial periods", dies with it); **P2's storm clause
confirmed exactly** (intervals collapse 4.1e6 → 10–22 ticks with no short period behind
them — the traced orbit is bound with a ≈ 5.8 sep, radial period ≈ 14 P); **P3 half-held**
(the tail is fat and μ-gated, but the storm spreads over 10 ICs: top-decile = 52% of
events, not top-1 ≥ 25% — my number was wrong, the fatness was right); **P4 held and
worsened** (convexity yes: 424 → 400,000 events/P; then not a rate jump but a frozen
clock — cost per horizon is infinite, not linear); **P5a refuted** (the 9 deaths are not
concentrated at small |du| — they spread across the whole grid), **P5b held** (μ = 1e-3:
no storm in 64 P), **P5c held trivially** (locked bodies never escape; nothing escapes a
frozen tick).

## What would make it wrong, cost of adoption, fit

Wrong if: a capped IC's trace shows a bounded planetocentric orbit (capture) or a
physical v (≤ 1e-3) with intervals still collapsing; or if the screens' caps are an
artifact of budget chunking (they are not: chunking preserves canonical bits, and the
uncapped ICs' medians reproduce the wiki's 231/267 kicks/P on both masses). The 30%
gap between measured A = 2.62 and my Δs/b = 3.69 is my reconstruction of c from the
code docs (floor vs sum of sources), not a fit — the checker can read the exact constants
from `ext::constants` at runtime; the form dt = A/y is what matters and is constant to
1.4%.

Adoption cost: none for the engine (no code change proposed); the finding kills the
capture/octave line of inquiry and redirects direction 3 to the clock itself. The fix
shape (for the board, not this run): clamp or re-derive the clock's constants when the
body's H_D leaves the doll's domain (unbound = a different doll or a compiled ejection
tube, "you don't advance a ship tick by tick you just map where it wants to go"), and
floor the clock's own step by MIN_STEP as a certificate, not a patch. PRINCIPLES: "A fix
signals the wrong representation" (19) — the ratchet is the wrong representation showing
itself; "Errors never compound" (13) — this is compounding energy, the exact forbidden
class; "Nothing past c" is not violated, but "a game that cannot lose by construction"
(29) is: one encounter ruins the frame.

## The lens

Taleb: I looked for the ruin and found it, but my prior (captures, fat tails of real
satellites) was wrong twice — the tail is ten bodies, not one (mediocristan spread over
an Extremistan mechanism), and the mechanism is iatrogenic (the law's own clock minting
energy), not physical. What this lens may have missed: the trigger encounters are real
and their rate at other μ (the latent-defect arrival rate at μ = 1e-3 over 512 P, where
the wiki's runs did finish) is measured only as "zero here in 64 P"; and I did not run
the judge's truth on the capped ICs to exhibit the ejection-free reference myself — the
impossibility argument is arithmetic (escape speeds), not an integrated truth.
