# Dossier — 20261021-0607-system-cbe6 (lens: the whole system)

## Claim

The belt's own cadence floor is measured on the shipped plane's instrument for the first
time — 16 kicks per planet period (~5 per belt orbit, ~8 per synodic conjunction) against
B12's frozen 1e-4 Jacobi bar, draw-stable, with the cliff beyond it super-quadratic
conjunction aliasing — so the certificate is per-class and set by conjunction sampling,
while the plane's one doll-wide Δs (tied to the fastest secondary) delivers the same bodies
~9,000 kicks per belt orbit (board, measured): the desynchronised grid's headroom on the
belt is ~10³, one hundred times the ledger's split8, and it is one constant per class, not
an algorithm — the clocks, the fired gate and the intervals are already per body.

## Bottleneck

The board's top macro row: "kicks per body (~10³ at stake) … the star's doll kicks every
body on one grid, ~9,000 kicks per belt orbit; the gates hold at 8-16 per the body's own
orbit … desynchronised grids; which bodies must stay fine and what fraction they are."
Expected gain: the belt's stream row falls by the headroom ratio (~10²·⁵-10³ against the
board's own 9,000/orbit anchor; split8's 8× is 2 orders short of the class's own
certificate). What it deletes: the same dial also relaxes the live set (τ = 43.6 game-s,
promotion fraction 1.0, both measured at shipped cadence — the dwell scales with h), the
calendar's live sizing (L = λ·τ·N), and the comb crest mass (the freeze's N·C law), because
all four rows are the one grid's rate.

## Evidence (all from `regen.sh`, ≤ 60 s per arm, Linux x86, shipped code + the run's patch)

Instrument: the shipped `jacobi` example's own scene and rng (star + Jupiter 2⁻¹⁰ at
5.27×10⁸ root units), copied verbatim to `examples/beltcad.rs` (work/patch.diff) with one
added axis — the radius class — a `SEED` dial, an osculating-e tracker, and read refusals
counted instead of panicking. Horizon 100 planet periods, 6 ships, ramped readout.

**Strong class (1.5–3 Hill, 7076's judged class; positive control):** worst Jacobi
5.1e-6 (step 6) and 1.8e-5 (step 5) — 7076's numbers to the digit; at step 4 (16/orbit) the
cliff arrives as deaths: 2/6 ships lost (read refusals 274/340), survivors' worst 1.1e-4;
step 3 worst 3.2e-4. The instrument bites (P1 held).

**Belt class (interior circles 2–3 AU = 6.8–8.5 Hill, the plane's own belt draw,
scenario.rs):** step 7 worst 1.4e-7 (36× below the strong class one octave finer, P2 held);
the ladder is n⁻² (×4.1–5.6/octave) through step 4; **step 4 (16/planet-period ≈ 5.3 per
belt orbit ≈ 8 per conjunction) = 9.4e-6–1.2e-5, PASS** on both draws (second draw
0.99–1.3e-5); **step 3 (8/planet-period ≈ 2.7/orbit ≈ 4 per conjunction) = 1.8e-4, FAIL**
the 1e-4 bar on both draws (three ships ≥ 1.1e-4 on draw 2); step 2 = 4.7e-4–1.1e-2; step 1
= 1.3e1, orbit destroyed (Δe 6.0). The cliff from step 3 is super-quadratic (×15, ×38,
×1900 per octave). The secular e-pump is step-independent to the digit per ship at every
passing octave (9.0e-4…7.8e-3 over the horizon) — real dynamics, corrupted only from step 2
(a built-in control: the certificate that moves with the step is the sampling error, not the
pump). Zero doll captures, zero losses, zero refusals at every passing octave (P5 held).

Commands: `regen.sh` (all arms); single arm:
`cargo run --release -p emergent-universe --example beltcad -- 4 100 6 belt`.

## Predictions

`predictions.md`, written before the run. P1 held (7076 reproduced to the digit; the
control's cliff is stronger than 7076's reading — deaths at 16/orbit on 2/6 draws of the
example's 6-ship scene; 7076's B17-PASS-at-step-4 was the gate's own 36-ship scene — both
readings reported). P2 held (36×). P3 held (n⁻² to the floor). **P4 half-failed: the floor
is step 4 (~5/orbit), not ≤ step 2 — the belt is ~6× deeper than the strong class in kicks
per own orbit, not ≥ 8×; the binding unit is the conjunction (8 holds, 4 fails), not the
orbit.** P5 held.

## What would make it wrong

The probe is the restricted three-body scene (one Jupiter), not the plane (Cinder, Home,
the Moon add tides ~50× weaker at belt distance — they cannot demand a finer cadence than
the conjunctions they ride, but the measured floor could shift on a resonant draw: a belt
body near a mean-motion commensurability with the Giant is uncertifiable at any cadence per
the page's standing resonance rule, and my two draws sample none). The 1e-4 bar is B12's,
the ladder's n⁻² is the same law ad35 measured in float. The ~10³ headroom composes my
floor with the board's 9,000/orbit anchor — both measured, on different scenes; the plane's
chained clock and quantized dv sit on top of the class certificate (the fired gate is inert
at any coarser Δs per 3294, so only the behaviour gates bind).

## Cost of adopting, and fit

Not an adoption (a measurement the adoption needs): the desynchronised grid (board's open
question; 7f97's split; Opus's in-flight `wt/cadence` job sizes per-body certificates) now
has the belt class's floor on shipped code: the split's belt constant is ~2⁻⁴ of the
planet-period grid with a measured cliff, and the 10⁹ ledger's split8 is 2 orders short of
what the class certificate allows. PRINCIPLES 33: "a body resolves only the influences that
are significant at its own scale" — one doll-wide Δs bills the passage class's price to
every raindrop. PRINCIPLES 14: the shared grid is the tick, reborn as combs.

## The lens

The whole-system reading: one mechanism — the doll's single Δs grid — sets four scoreboard
rows at once (stream CPU, live set, calendar sizing, comb spikes), and four wiki topics
(kick-cadence, allocator-ratchet, calendar, live-residency) each fight a symptom of it. The
machinery is already per-body (`full` recomputed each kick from the body's own state; the
fired gate per body); what anchors every body to the doll is one constant per doll
(`ext::constants`), so desynchronising is a per-class Δs change, not an algorithm. What
this lens may have missed: the unification is argued from the pages' own measured numbers,
not re-measured as one experiment; and the elegant "one dial" reading can hide the hard
case — the resonant/encounter bodies that must stay fine are exactly the ones whose
certificates (B13's 256/orbit) set the grid everyone else overpays, so the deletion lives
or dies on the class census (which bodies are fine-class), still unmeasured on the plane.
