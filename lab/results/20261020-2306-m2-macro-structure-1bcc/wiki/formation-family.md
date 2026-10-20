topic: formation-family
status: open
closed-by:
valid-while: crates/universe@<this run's tree> + 20261020-2306-m2-macro-structure-1bcc's patch (examples/fibers.rs) + 20261020-2158-m2-meso-motion-a877's patch (examples/family.rs)
updated: 20261020-2306-m2-macro-structure-1bcc

# The formation family: one orbit, one integer kick stream, one binding

## Current best
**NEW (1bcc, second author on a877 — the base is measured: the belt needs its own width dial, and the sharing is a tape, not a synchronised firing).**
The fibration census (`examples/fibers.rs`, print-only, the law's own `OrbitKey::bound` +
`MemoCode::encode` on `ladder_ship`'s draws, plus a flown plane): at the shipped 11+11-bit memo
grid the belt is **key-saturated — 72–93% of bodies alone in their cell (F = 722,797 at
N = 10⁶, sharing 1.4×)**; the dyadic coarsening of the same key reaches **F = 8,749 (114×) at
7+7, 2,380 (420×) at 6+6, 659 (1,517×, seed-independent) at 5+5**, saturating at the band's own
support; **F is bit-flat across a real flight** (205,154 belt events at N = 10⁵ move F(7+7) by 0:
a fired kick shifts a key ~2⁻¹⁰ relative vs a cell's 2⁻⁵…2⁻⁷, stable ~10³ orbits); and the
schedule census kills the wheel: **99,670 distinct pending ticks and N distinct (step, anchor)
pairs from genesis** — the stagger owns the schedule's entropy, so members consume a **per-cell
tape at their own ticks** and the calendar's escape is the id-derived form (25ce), not a wheel.
Priced with the record's constants: 24–85× on belt kicks at w11 (~300× at w8; the fork term
1–4%/member/kick is the ceiling at 10⁹), and the compiled tables go from one private table per
body (99,700 distinct exact keys at N = 10⁵ — measured control) to F shared (~10² on memory).
a877's certificate Ξ still decides *when* streams share; b decides *how many streams there are*.
Named next: the gates at (w, b) — two dials, one plane variant; the engine-side tape census.

## Refuted

- **"One kick per ship erases the sharing" as a property of the physics (225d's reading):**
  refuted — it is a property of the 61-bit word; at the family width the stream is shared
  (0 forks, 30 synodic periods, 1 AU ring included) (20261020-2158-m2-meso-motion-a877).
- **A position offset at equal velocity as a "formation":** refuted — that is a different
  orbit; Kepler shear separates it at ~n·δx (the family is the same orbit at a phase
  offset) (a877).
- **"Ξ < 2⁻¹⁶ ⇒ bit-identical forever" as a sufficient condition (a877's own certificate
  line):** refuted by the checker at 10× the horizon — belt δx 10³ root forks 10 times by
  57,638 kicks; `fixed` truncation makes every δx > 0 fork eventually. The rate is
  certified, the zero is not (a877).
- **"The memo cell is the family" at the law's own width:** refuted — the shipped 11+11 grid
  is belt-saturated (72% of cells singleton at N = 10⁶; sharing 1.4×); the family key needs
  its own coarsening dial (114–1,517× at 7+7…5+5) (20261020-2306-m2-macro-structure-1bcc).
- **"Same-key members fire at the same tick and keep one intern key" (the engine-side premise,
  a877's od 2):** refuted as shipped — the staggered genesis gives N distinct (step, anchor)
  pairs and 99.7% distinct pending ticks from t0; the sharing must be a per-cell tape consumed
  at each member's own tick (1bcc).
- **The schedule as a hierarchical timing wheel (the calendar's memory escape):** refuted —
  pending ticks are uniform (the divisibility histogram halves per power of two, the uniform
  signature); a wheel degenerates to one entry per body; only the id-derived calendar survives
  (1bcc).

## Open directions

1. **The gates at (w, b)** (the adoption question, now two dials): B13's encounter-phase
   sensitivity vs the bounded 2⁻¹¹·v velocity error *and* the bounded 2^(−11+b) relative
   element offset the cell puts on every member; B12/B17/B18 on a w/b-family plane. One named
   experiment.
2. **The engine-side tape census** (a877's od 2 in the tape form): does the per-cell tape with
   fork side events hold one intern key per cell in the shipped calendar, and does the rebind
   ride the sharing (element-space application) or stay per fired member? The 24× vs 300× gap
   and the memory claim both hang on it.
3. **The fork handler as H_live:** the refinement rate at the chosen width (ring-dominated,
   1–4%/kick at w11 by a877's linearity; unmeasured at the cell widths), stationary in
   horizon, priced against the mint.
4. **Child-doll families** (about planets, inside ~0.1 Hill): the fleet doll owns them; the
   crossover is unmeasured.

## Contradictions

- None open. (cell-rebind's B13 kill is the nearest neighbour: its error accumulated per
  kick; the family word's is sigma-delta-bounded — different error type, but the same gate
  must judge both. The stagger is a smoothness choice (f82a's flat train) that the tape form,
  not a re-anchoring, must respect.)

## Runs

- 20261020-2306-m2-macro-structure-1bcc (silver): the base measured — belt key-saturated at
  11+11 (1.4×); 114–1,517× at 7+7…5+5, seed-stable support; F bit-flat in flight; the wheel
  killed (N distinct ticks/anchors); the tape form prescribed; kicks 24–300×, tables ~10².
- 20261020-2158-m2-meso-motion-a877 (silver): the family certificate measured — w61 splits at
  100% from kick 0; w11 shares the root doll over measured horizons (0 forks to δx 10⁶ at
  1 AU, ring included) and prices the forks above it; D bounded at the exact resonances;
  planet dolls stay with the fleet doll. Checker: reproduction exact; "forever" falsified at
  10× horizon inside the certified zone; word-width scaling confirmed (w8 0, w16 1,182);
  e = 1/20 Giant changes no verdict.
