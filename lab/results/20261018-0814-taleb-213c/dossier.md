# Dossier — 20261018-0814-taleb-213c

## Claim

The clock storm is a **player-reachable, permanent per-frame ruin on the flyable mass**: one
unbound live body at μ = 2⁻¹⁰ — minted by an ordinary player burn, or born unbound anywhere,
even 900 orbits out heading for the leave edge — collapses the clock monotonically, mints β
without bound, and costs ≥ 5×10³ events per frame **forever** (measured 0.32 s/frame for one
body on this box, unbounded toward ~4×10¹ s at the 1-tick floor), because the leave edge at
2⁴⁰ is unreachable once the clock has frozen: the body crawls ~v·interval ≈ 18 root units
per event against a remaining ~10¹¹.

## Bottleneck

Not a speed bottleneck — a **ruin state** (PRINCIPLES 13, 25; the lens's "ruin before
optimization"). The board's furthest gap (bodies in the flyable engine → 10⁹) is gated by it:
the moment any live body goes unbound — one player verb, one deep-encounter ejection, one
piece of fleet debris past escape — the frame's event budget is permanently dead, at any mass
(2⁻¹⁰ and 1.01×10⁻² collapse at the same rate; 2⁻²⁰ only ~10× slower). What it deletes: the
possibility of shipping the ladder without handing unbound bodies to the tube layer.

## Evidence

Shipped code only, public API only: `crates/universe/examples/ruin_mint.rs` (in
`work/patch.diff`), the `restricted` CRTBP scene built as `scenario.rs` builds it (star + one
planet, sep 5 AU, radius 47,400, `Config::default()`, 1 thread), driven with `add_body_state`,
`start`, `advance`, `input`. Logs: `run-all.log`, `run-edge-outward.log`. Reproduce:
`lab/results/20261018-0814-taleb-213c/regen.sh` (≈ 7 min). All wall numbers are cloud
(8 vCPU shared); orders of magnitude only.

- **P — the player mint at the flyable mass (μ = 2⁻¹⁰).** Player ship born bound (circular
  5 AU, 90° from the planet; clock constants derived bound, as for any real body), one
  prograde burn through the public decision API (`input`, level 8, 588 events), released.
  The burn overshot my 1.3×v_esc poll target: v = 1.021×10⁻³ = 16.3×v_esc (disclosed; the
  modest end is arm S). Then: interval **2.8×10¹¹ → 121 ticks, monotone** (ladder rungs
  ≤2²⁰/2¹⁶/2¹²/2⁹/2⁷ crossed at 1,361 / 8,295 / 107,184 / 573,669 / 1,428,149 events),
  |v| minted 9.5×10⁻⁴ → **5.34×10⁻²** (one-signed after the seeding dip, ×53), r pinned at
  1.962×10¹¹ root units (387 sep — the body moves ~18 root units per event), alive, zero
  refusals at cap (100 s).
- **Frame cost, measured once, not selected:** at the ≤128-tick rung, one 338,375-tick frame
  (the ladder belt's frame, calendar page) carries **5,261 events for this one body** at
  **61.3 µs/event = 0.32 s/frame**. The belt's whole 11,700-body population: 1.64 dues/frame
  (calendar page) — **one storm body = 3,200× the belt's event load**. The load grows as
  2·FRAME/interval toward ~6.8×10⁵ events/frame (≈41 s/frame here) at the 1-tick floor that
  6de0 measured.
- **S — the modest mint (μ = 2⁻¹⁰, born unbound at 1.41×v_esc).** Same collapse without any
  burn: interval 2.7×10¹¹ → 188 at 1.39×10⁶ events, |v| → 5.02×10⁻², r pinned at 4.9×10¹⁰
  (97 sep). The storm does not need a big mint or bound-born constants.
- **B — reproduction at μ = 1.01×10⁻² (6de0's mass).** Same IC as S: interval → 65, |v| →
  **0.277**, crossing β = 0.195 at the ≤128 rung — 6de0's β = 0.199 signature, on their
  mechanism, through my independent instrument. Frame window: 5,274 events, 56.3 µs/event.
- **Mass does not protect:** collapse-rung positions at ≤2¹⁶ — B (10⁻²): 36,657; S (10⁻³):
  26,013; C (2⁻²⁰): 299,271. Flat across three decades of μ at the top, ~10× slower only at
  10⁻⁶ — **the storm is not μ-gated in rate between the flyable mass and 10× it**, and even
  10⁻⁶ collapses (C: 48,218 and falling at 404k events). 6de0's "latent at any mass" is
  confirmed by direct mint, and strengthened: mass buys almost nothing.
- **The leave edge is unreachable, measured twice.** Outward control E: a body **born at
  0.9·2⁴⁰ heading out at 10⁻³ c** — 10% from the fence, no planet anywhere near — storms
  before it can cross: interval 1.9×10¹³ → 267 at 4×10⁵ events, |v| minted to 1.39×10⁻²,
  r = 9.22×10¹¹ < 2⁴⁰ = 1.0995×10¹² at cap, **alive**, ≥4.8×10¹⁰ events to exit (and that
  estimate worsens as interval → 1: → ~1.3×10¹³). P: ~1.4×10¹¹ to exit. The check exists
  (`boundary_clock`, `step.rs:733`, r > 2^leave_log2 → Lost) but the clock's own collapse —
  `kick_clock`'s step through `ext.ticks(...).max(1)` (`ext.rs:100`), which ignores
  `MIN_STEP = 128` (`step.rs:49`, applied only on the non-clock path) — freezes the body
  before the fence. (An inward fast body at that radius instead dies of a `Space(Range)`
  refusal at a Boundary — the large-r/fast regime is broken a second way; one arm, noted.)
- **Control D (bound, 6.5 AU):** 5×10⁵ events, interval 1.5–9×10¹¹ never below 2²⁰, |v|
  1.740–1.749×10⁻⁵ (±0.3%), alive, zero refusals. The instrument separates the classes.

## Predictions

`predictions.md` was frozen before any decisive arm ran (the smoke arm D only). Held: P1
(ratchet at the flyable mass, ×53 mint), P2 (freeze to ≤128 within 3×10⁶ — P at 1.43×10⁶),
P6 (control healthy). Missed on the letter, held on substance: P3 (r stayed under 2³⁵ —
both arms sat at 2³⁶·⁵–2³⁷·⁶; the substance, edge unreached at ≥10⁹ events, held by ~100×)
and P4's count (≥3×10⁵ events/frame predicted at the floor; measured 5,261 at the ≤128 rung,
growing as 2·FRAME/interval toward 6.8×10⁵ — the ≥0.1 s/frame half held at 0.32 s).
**Falsified: P5** — B does not mint 10× faster than S (measured flat); the ∝1/μ scaling is
wrong (measured ≈ μ⁻⁰·³⁵ from the 10⁻³→10⁻⁶ pair). The miss is the finding: the collapse is
driven by the time map's A/y branch (mass-independent), not by the planet's pull.

## What would make it wrong

A demotion/promotion tier that retires live unbound bodies before the collapse bites (the
board's promotion topic) would make this a bounded stall, not a permanent ruin — no such
retirement exists on the clock path today (nothing in `kick_clock`/`boundary_clock` hands an
H_D > 0 body to the tube layer; `plan_interval`'s own comment says a pure tube "costs
nothing until observed"). My arms are single-body scenes; a populated scene could surface a
different collection path (an encounter rebinding the ejected body) — unlikely at 100+ sep
where these bodies sit, but unmeasured. The µs/event is cloud, single-thread; on the M1 the
0.32 s/frame becomes maybe 0.03–0.1 s — still ≥2× the whole frame budget for one body,
growing without bound.

## Cost of adopting / fit with PRINCIPLES

Adoption is not mine to design (the fix is a representation change on the integrator's
side); the price this run pays for: any body with H_D > 0 must leave the clock — compiled
ejection Passage to the leave edge, or demotion — because a clock-run unbound body costs
≥5×10³ events/frame forever and the fence cannot collect it. Fit: "divergence is not a joke
and it compounds" (OC#34, register 13); "never let one experiment take the machine" (lab
rules) — here one *body* takes the frame; the fix deletes compute (a tube is free until
observed), which is principle 1.

## The lens

Taleb found the ruin but must name its upside honestly: this is also the cheapest possible
kill — no population, no horizon, no statistics needed; a single-body scene reproduces and
prices it in seconds. What the lens may have missed: the natural mint rate on the shipped
plane (how often real encounters mint H_D > 0 without the player) — unmeasured here; and it
says nothing about how the fix should look.
