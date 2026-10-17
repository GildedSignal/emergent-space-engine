# Dossier — 20261017-2142-library-e29c (library lens)

## Claim

The certificate's angle bars are frozen from the shipped consumers — the map's pixel, the
contact's miss quantum, the aggregate's dipole noise — and the freeze **deletes the re-kick
from the flight law** (0 firings at every flyable N; 0.28% of the deleted stream at 10⁹),
**deletes the mass bar** (never binds, ≥10 orders of slack), and **forces the contact
consumer out of the angle channel** (its bar sits 11× below the law's own acting angle
grid): the one-global-bar reading is dead, and the compose rung's one free constant per
population is `q_view(N)`, derivable, not tunable.

## Bottleneck

The board's #1 gap (bodies: 10⁶ flyable vs 10⁹), whose cure chain is frozen shut behind
this constant: bar → re-kick cadence (dc8f/f5bd's k*) → compose rung (RES delete) → compact
store wiring → the 1.2–1.65×10⁶ memory wall. Expected gain: not a CPU ratio but a component
deletion (the sparse secular re-kick leaves the shipped law) and the unblocking of the
ladder's next rung; at 10⁹ the fence is bounded at 0.28% of the deleted belt stream, so the
belt row's remaining bind is named (the resonance-exclusion width, 38.5% kept), not the fence.

## Evidence (all commands ≤ 1 s)

`python3 bars.py` (this folder; every input a shipped constant or a published measurement):

| Bar | Value | Consumer | Source |
|---|---|---|---|
| q_grid | 8.38×10⁻⁸° | the law's acting angle grid | tube's 32-bit periapsis angle, docs/law.md:12 |
| q_contact | **7.51×10⁻⁹°** | a conjuncting pair | 49 m miss (encounters page) at r_mid 1247.5 ls |
| q_view(10⁵) | 1.44×10⁻¹° | the map's belt dot | spacing 6.25 ls / 2 px dot |
| q_view(10⁶) | 4.54×10⁻²° | " | spacing 1.98 ls |
| q_view(10⁹) | **1.44×10⁻³°** | " | spacing 0.0625 ls |
| q_mass | **never binds** | the aggregate | dipole noise ≤ 7.9×10⁻¹¹ of host field at M_belt/M_host = 10⁻³ |

- q_view = (half the mean inter-neighbour separation)/r_mid: a belt body is a 2×2 px rect
  with no name (`kind===4`, `bodyPaint`, page.html:141; names drawn for kind ≤ 2 only;
  `fitLog` counts kind ≤ 3 only) — a lone belt dot carries no reference finer than its
  neighbours, so the pixel at neighbour resolution is the floor "the player differentiates"
  (PRINCIPLES: "the floor is what the player can differentiate"). Band [2,3) AU:
  scenario.rs:333, nladder.rs:2. AU_LS = 499.004784: page.html:58. Scaling: N^−1/2
  (the bar self-tightens as the belt fills — the right direction for 10⁹).
- The fence (f5bd's measured drift law: the belt population's own max 2.2×10⁻³° at
  7.41×10⁶ game-s, ~t²): T*(q_view) = 5.99×10⁷ / 3.37×10⁷ / 5.99×10⁶ gs at 10⁵/10⁶/10⁹ —
  **never fires before the 8×10⁶-gs horizon at any N ≤ 10⁶**; at 10⁹, k* = 213 carried
  kicks (cadence 3.55×10⁻⁵ ev/B/gs), re-kick = 0.6/213 = **0.28%** of the deleted stream.
  The t² extrapolation past 7.41×10⁶ gs is conservative: the max's measured late law bends
  to t^0.9–1.6, so the true T* at 10⁵/10⁶ is later still.
- q_contact sits **11.2× below q_grid**: no acting angle word in the law can even represent
  the difference; contacts of carried bodies must be certified by the margin representation
  (cf2a direction 1: birth-constant min-distances, Diophantine first-hit), never by angle.
- The locals (313 individuals, the comb's population) keep the r9-class 10⁻²° bar (10c4's
  guess, not re-derived here — see The lens); their fence fires at 2.6×10⁴ gs (f5bd's own
  number at that bar): 313 bodies × 0.6 kicks every 43 min at rtf 100 — noise in the ledger.

## Predictions

All five pre-registered predictions held (`predictions.md`, written before `bars.py` ran):
P1 0.144°/0.045°/1.44×10⁻³° against the predicted 0.1–0.2°/0.03–0.07°/(0.7–3)×10⁻³°; P2
7.51×10⁻⁹° inside (5–9)×10⁻⁹° and strictly below q_grid; P3 worst-case dipole noise
7.9×10⁻¹¹ (≥10 orders under 1); P4 zero firings ≤10⁶ and k* = 213 ∈ [150, 300]; P5 quotes
5/5 byte-identical (`python3 verify_quotes.py`, full-text check, exits 0).

## The five lessons (each changed a decision; all verbatim in `quotes.json`)

1. **Paul Graham, Black Swan Farming** — "listen only to your instruments": a difference
   with no instrument that reads it does not exist for the player. → The belt's bar is the
   map's pixel at neighbour resolution (1.44×10⁻³° at 10⁹), not a physics number.
   Test: `bars.py` row q_view; the client's own kind split is the instrument's spec.
2. **Taleb, The Bed of Procrustes** — "the more precision, the more dead you are": the
   consumers' bars span six orders (7.5×10⁻⁹° to 10⁻³°); a global bar at the tightest
   consumer's level taxes every body for precision nothing reads. → The one-global-bar
   reading dies; per consumer per population.
3. **Taleb, The Logic of Risk Taking (Buffett)** — "establishing a high filter, then
   picking opportunities that pass such threshold": the certificate is a frozen pass/fail
   filter, not a measured-error negotiation. → Each bar names its consumer and its kill;
   the compose rung carries q_view(N) as its one derived constant per population.
4. **Herbert, Dune** — "Too few individuals, and a people reverts to a mob": the mob/individual
   split is a count property, and the client already encodes it (kind ≤ 3 named circles that
   set the fit vs kind 4 rects). → The mass bar is deleted (dipole noise ≤ 7.9×10⁻¹¹ of the
   host's field); 10c4's "two bars q_live/q_mass" refines to q_live + q_view, and no q_mass.
5. **Musk (Isaacson)** — "if you do not end up adding back at least 10% of them, you didn't
   delete enough": dc8f pre-committed the re-kick as the delete's add-back; the add-back's
   rate is now measured at the frozen bar — 0% where we can fly, 0.28% at 10⁹. → The delete
   passes Musk's own test with ≥ 20× margin; the re-kick leaves the flight law and enters
   the 10⁹ wiring with k = k*(q_view).

## What would make it wrong

The drift constants are the ladder scene's 477 deleted bodies (belt sample 274) — a 10⁹
belt with a different secular drive could drift faster [inference]; the fix is one arm of
f5bd's harness at 10⁶. The view bar assumes the player never needs a belt body's phase
below neighbour resolution (a fleet rally point on a specific asteroid would need a named
body — but named bodies are kind ≤ 3, the individuals' population, already excluded). The
49-m miss quantum is the encounters page's coarse-end constant; if delivery tightens, q_contact
only falls further below q_grid, strengthening the margin-representation conclusion.

**Adoption cost:** none in code — the compose rung drops a component (the re-kick arm) and
gains a derived constant; the encounters queue gains an arithmetic forcing of its direction 1.

**Fit with PRINCIPLES:** "the floor is what the player can differentiate like frame rate in
early cinema" (0. representation, 29 September); "Compute only surprises" (§3: a sub-pixel
drift is not a surprise); "The view is an instrument" (§28); "A fix signals the wrong
representation" (§19: contacts below the acting grid are a representation question).

## The lens

The library lens quotes practitioners and composes published constants; it flew nothing.
Missed by construction: the locals' pixel bar (the fitted view's scale depends on the
scene's `near` body — derivable from one flight's frame dump, not attempted); any
interaction of the fence with the burn (f5bd's constants are coast-scoped); and whether
the checker's independent recomputation of the N^−1/2 neighbour law (a uniform-density
assumption on the belt band — the real belt is Rayleigh-e with a 0.4 cap, so local
clumping coarsens q_view by O(1), not orders).
