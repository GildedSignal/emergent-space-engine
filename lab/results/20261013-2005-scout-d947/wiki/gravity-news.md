topic: gravity-news
status: open
closed-by:
valid-while:
updated: 20261013-2005-scout-d947

# Gravity at c: news, the cursor, the version ring

## Current best

**The version payload is decided: it must carry the source's total acceleration
(x, v, a) and nothing more — jerk never enters the field, only the staleness of the
a-slot (20261013-2005-scout-d947).** The literature anchor, read at source: the
retarded field of an arbitrarily thrusting source (Kinnersley's photon rocket) depends
only on retarded position, velocity and acceleration — Carlip 1999 (arXiv:gr-qc/9909087
§2, eq. 2.4–2.5: the field points to the retarded data *quadratically extrapolated*)
— so (x,v,a) is the complete broadcast; 7ab4's ½aT² is exactly the thrust part the
aberration cancellation cannot absorb (the cancellation uses the gravitational EOM).
The float falsifier (Carlip's §3 scalar retarded force as oracle field, consumer at
β_c 0.003–0.3, versions every T): payload (x,v,a) under a constant burn sits at the
machine floor (0 / 8×10⁻²⁰) at every window and every β — the burn channel is deleted,
not attenuated; under jerk the residual is the a-slot's own staleness, scar ∝ j·T³
(exponent 3.15–3.98), 1.8×10⁻⁸ per rebind at kick cadence T = P/32 and β_c = 0.3
(~50× under a 10⁻⁶ budget; the residual crosses 10⁻⁶ at T ≈ P/9.6 — the measured P/8
point already reads 2.2×10⁻⁶; the dossier's P/6.5 is ~1.5× optimistic — checker); a
jerk slot is dead weight **on constant-jerk programs** (the (x,v,a,j) arm is bit-exact
on cubic programs — the control that also caught the run's own first-build bug), but
the verdict is burn-curvature-scoped, not exact: on quartic (time-varying-jerk)
programs the frozen-jerk slot buys 28–143× and a violently curving burn puts (x,v,a)
at 1.6×10⁻⁶ while (x,v,a,j) holds 5.7×10⁻⁸ (checker's quartic, β 0.3, P/32). The
as-if-now readout (the no-retardation tube
convention) scars ∝ a·T per rebind and its total per orbit is cadence-invariant
(7.7×10⁻⁴ flat, β 0.3) — 7ab4's "rekeying faster buys nothing" is the total; payload +
retarded readout beats it 3.4×10³× at the same cadence. Free fall stays exact for every
payload (0.0): the tube travels.

**The rebind half of "gravity is news" is right and now has an error model; the thrust
half is wrong as specified, and no gate, rung or oracle can see either.** For a freely
falling source, news ≡ instantaneous gravity (the tube travels, not the position; the
aberration cancels by construction): binaries bound with dt-quadratic drift (a237), the
flyby scene matches to 5×10⁻⁸ (a237), the wired plane is bit-identical wherever no rebind
falls inside a light window — which is every named gate scene (e300). The first
measurement past free fall (7ab4): every **rebind** of a source leaves each consumer a
permanent orbital scar (accrued entirely inside the light window; sign set by kick
geometry) |ΔE| ≈ 0.7·(β_c²/2)·|δv| (β_c = the consumer's orbital
speed about the source; exponent 1.963 over β_c 0.003–0.3) — 5.5×10⁻¹⁰ per rebind at a
Jupiter moon (why the gates are blind), **1.4×10⁻² at r = 20M** (a strong-field consumer
takes percent-level steps at its doll origin's kick cadence; whether the lag channel
then dominates the direct tide is unmeasured — the checker's arithmetic puts the tide
above it in magnitude at 20M/100M, though bounded where the scar is one-way). Under a
**sustained
burn** the free-fall tube readout lags the design's own 1PN near-zone oracle family by a
**cadence-invariant ½·a·T²** (measured at T/8 and T/32 epochs), so the consumer permanently
absorbs β_c²/2 of the source's total burn Δv (ΔE = 2.2×10⁻² for a 2P burn at β_c = 0.3,
200× B12's budget; measured factor 0.7–0.8 of β²/2·a·D in the swept range, saturating near
β_c 0.5 — checker 2): **the version payload must carry the source's total acceleration
(quadratic tubes)** — a237's probe payload already recorded (t, x, v, a) and read
quadratically, but its `a` is gravitational only and the plane's 16 B compiled-cycle tube
drops the slot: every built instantiation is thrust-blind, and rekeying faster buys
nothing (7ab4) — scout-d947 confirms the total-scar invariance and prices the fix
(payload+readout, not cadence). Mechanism cost is solved: the per-(body, source)
cursor selects the delivered version exactly (0 mismatches over 7.2M kicks, 1 + arrivals
integer tests per kick; frozen single-version ghosts are structurally unstable, so the
chain carries per-rebinding versions — 05b0), ≈6× an instantaneous kick in float, one
cached comparison wired (e300). Proposed freeze-ready criterion (`r-news`: twins
bit-identical until the cone; scar ≤ 2·β_c²·|δv|/v_c per rebind, bounded under alternating
kicks; free-fall versions must fail ½aT² at β_c ≥ 0.1, acceleration-carrying versions
must pass) — now with numbers for the pass side (floor at constant thrust; jerk residual
1.8×10⁻⁸ at P/32, β 0.3; T* ≈ P/6.5) and a cheap new negative control: jerk-carrying
versions must show no further gain at flight cadences — for a rung that does not
exist (r5/r6 never frozen; B16 is light-only).

## Refuted

- "Naive retardation (pull toward where the source was) is good enough": spirals binaries
  out (Laplace), unbound in 4–12 orbits at β 0.1–0.3, ~170 at 3.3×10⁻³; 1PN-sized spurious
  precession (a237).
- "A frozen single-version ghost suffices": structurally unstable, explodes in 3–7 orbits
  at any cadence (05b0).
- "The tube readout between rekeys represents a thrusting source": lags by ½aT²,
  cadence-invariant; consumer absorbs β_c²/2 of the burn's total Δv (7ab4); its total
  scar per orbit is flat in rekey cadence — confirmed and quantified (scout-d947).
- "The named gates exercise news": byte-identical before and after wiring — no gate scene
  rebinds inside a light window (e300).
- "A jerk slot is needed for hard ramps": refuted **for constant-jerk ramps only** — the
  (x,v,a,j) payload is bit-exact where (x,v,a) already holds the window, and the jerk
  residual crosses 10⁻⁶ only past T ≈ P/9.6 at β 0.3 (scout-d947 — toy domain: planar,
  scalar force, β ≤ 0.3, one thrust family). **Not refuted for curving burns**: at jerk
  ×16 the P/32 residual is 7.7×10⁻⁷ (at the budget's edge), and on quartic programs
  (x,v,a) alone reaches 1.6×10⁻⁶ while (x,v,a,j) holds 5.7×10⁻⁸ — checker's adversarial,
  same toy.

## Open directions

1. **Carry the source's total acceleration on the version** (a237's float payload already
   had the `a` slot, gravitational only; the wired 16 B tube drops it — restore and extend
   to thrust; quadratic readout ≈2 multiply-adds) and freeze `r-news` with the criterion
   above and scout-d947's numbers — the missing instrument for law.md's causality
   primitive (7ab4, scout-d947). The slot is the same one the burn carry and the view's
   field term request (2964: one adoption, three bottlenecks).
2. **Expressibility before instrumenting the plane:** the plane cannot resolve arrival at
   stellar scale (kick steps 25–500 ticks vs light delays 4–32) nor express mutual β above
   the star's escape speed — the causal half needs scenes it can bite (e300 E3; 7ab4's
   probe is standalone float; scout-d947's toy likewise).
3. ~~A causal oracle: the retarded 2PN oracle computation would fix the required payload
   (acceleration vs jerk)~~ **answered at the field level by the literature (Kinnersley/
   Carlip: acceleration, never jerk) and in float (scout-d947); what remains of the
   oracle question is the strong-field consumer (r = 20M, where the O(v²) extrapolation
   corrections and the direct tide grow) and the burn-profile family (constant-jerk
   programs only were swept; curving burns are where the jerk slot pays — checker) —
   unmeasured.
4. **The fleet doll under thrust** (adjacent, unmeasured): the dense order's Fermi frame is
   defined along a geodesic; a burning fleet centre is not on one (7ab4 names it;
   b-fermi-phase2 owns the build).

## Contradictions

None open. The record's near-agreements are compositional: news ≡ inst *for free fall*
(a237, e300) and news ≢ inst *at every rebind inside a light window* (7ab4) are the same
mechanism seen from both ends; the scar is the causal half itself, and the 1e-6-class
agreement numbers of earlier runs are the β_c of their scenes (5×10⁻⁸–10⁻⁷ at flyby β),
not a bound on the mechanism. 7ab4's rebind-scar coefficient form (0.7·β²/2·|δv|) does
not transfer to the toy's window-sampling channel (toy C = 0.004–0.038, spread 10×,
tidal-dominated) — different channel, same exponent family in T; kept as a domain note,
not a conflict.

## Runs
- 20261005-1404-q-gravity-at-c-a237 (silver): news vs inst vs ret on binaries, a star system, flybys, a struck source; Laplace refuted; free-fall news ≡ inst to 10⁻⁷; probe payload (t, x, v, a), quadratic read, gravitational `a` only — thrust-blind as built.
- 20261005-1540-q-gravity-cursor-05b0 (silver): the version cursor exact (7.2M kicks, 0
- 20261006-1738-b-news-gravity-e300 (silver): news wired into the plane's kicks; gates
- 20261006-1931-second-20261006-1738-b-news-gravity-e300-e1ac (missing): second check, no
- 20261013-0236-redteam-7ab4 (this run, awaiting grade): the rebind scar law (0.7·β²/2·δv, exponent 1.963) and the thrust-blind tube: ½aT² cadence-invariant, consumer absorbs β²/2 of the burn's Δv; payload must carry total a.
- 20261013-2005-scout-d947 (this run, awaiting grade): payload decided from Kinnersley/Carlip and measured — (x,v,a) exact at constant thrust (floor), jerk residual ∝ j·T³ (1.8×10⁻⁸ at P/32, β 0.3; T* ≈ P/6.5), jerk slot exactly dead, as-if-now readout's total scar cadence-invariant (3.4×10³× gap).
