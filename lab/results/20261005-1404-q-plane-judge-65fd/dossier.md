# Dossier: the plane judged by the frozen gates (run 20261005-1404-q-plane-judge-65fd)

**Claim.** The shipped plane (`crates/universe`), answering the circular restricted three-body
problem through its public API, fails the frozen gates B12, B13 and B17 at every kick cadence the
CLI can name (2^3 to 2^7 kicks per radial period), and B14 cannot finish on this machine for any
law including `echo`: the plane's encounters near the planet kill ships the reference keeps
(`Lost`: a surface) and the surviving ships' Jacobi constant drifts linearly (growth exponent
about 1.0-1.5 against the limit 0.2), so the changeover and the kick layer do not yet hold
"errors never compound" (principle 13).

**Bottleneck.** Board item 2's live path ("analytic generators in the dominant field, with
multipole residuals as kicks") and the changeover question ("reversible and integer"). This is the
first time the engine itself, not a replica, has faced B12-B14/B17; it measures whether the
shipped law is adoptable as the events layer the gates certify. Expected gain: not a speedup but a
verdict — it kills the assumption that the plane at 8-128 kicks/orbit is within one step of
passing, and points at where the error type is wrong (the encounter, not the cadence).

**Build (the patch, reviewed by the integrator).** `behave --law plane [--plane-step N]`:
`xtask/src/behave/plane.rs` (new) answers `Law::restricted` by building `Universe::new(star
surface, Config{step_log2})`, `add_body(Kind::Planet, OrbitSpec{doll:0, periapsis: sep/(1−μ),
e_q48:0, angle:0, phase:0})`, `add_doll("planet", …, Mass::of(μ/(1−μ)), planet radius)`,
`add_body_state(Kind::Ship, 0, heliocentric x,v)` (exact: `x_h = x_b − x_star(0)`, lengths and
times ×1/(1−μ), velocities unchanged — β is unit-free), `start()`, then per sample `settle(tick)`
and `observe::root_state`, back to barycentric through `scene.star(t)`. Two deviations from the
lens's recipe, both required by B17's scenes and both inert for B12-B14: the planet's mass is
`Mass::of(from_f64(μ/(1−μ)))` (exact for the f64; `Mass::ratio(1,999)` is only μ = 1e-3, B17's μ
are 3e-5/3e-4/3e-3), and the star's surface is `STAR_RADIUS·min(1, sep/AU)` (at sep = 100 the
shipped 471000 would swallow the system and decide outcomes the judge never asked for; at the
Jupiter scene it is exactly the shipped value). A ship the plane loses is answered `None`
(extrapolating its last tube would invent an answer). `--plane-step` parsed in `select.rs`;
one-line usage updates in `mod.rs`/`main.rs`. The gates and `crates/universe` are untouched.

**Faithfulness (gold's first criterion).** Three tests in `plane.rs` (all pass,
`cargo test --release -p xtask far_ship the_start`): the t = 0 state round-trips exactly through
the whole conversion (< 1e-12); a far ship at 4.1 sep tracks the judge's own float64 reference to
5.0e-4·sep at 2^7; that error falls by more than 8× when the cadence doubles twice, i.e. it is the
kicks' H², not a conversion bug (a frame or unit bug errs at ~μ·sep per synodic period and grows
linearly). The gates still bite through the same `restricted` path: `planted-kick` fails B12
(median exponent 0.766, worst err 3.9e-4) and B13 (53/64); `planted-notide` fails B14 (167/255
classes); `planted-apsides` fails B14 (0/53 apsides); `planted-average` fails B17 (pump 0.107-0.963,
amplitude 0.015); `echo` passes B12 (worst err 3.8e-15), B13 (64/64) and B17 (pump 1.000001).

**Evidence: the table** (verdict · gate detail · kicks per ship orbit · phase wall time; this
cloud box, 2 vCPU shared — orders of magnitude only; full lines in `table.log`, per-run files in
`rows/`, reproduce with `bash table.sh` after `cargo build --release -p xtask`):

| gate | 2^7 | 2^5 | 2^4 | 2^3 |
|---|---|---|---|---|
| **B12** handoffs | FAIL · median exponent 1.026, worst err ∞ · ~128-183/orbit · 26.6 s | FAIL · median ∞ · 26.4 s | FAIL · median 1.528 · 6.3 s | FAIL · median 1.178 · 20.9 s |
| **B13** assists | FAIL · 51/64 within 1%, worst ∞ · 3.7 s | FAIL · 35/64 · 1.3 s | FAIL · 36/64 · 0.9 s | FAIL · 25/64 · 0.8 s |
| **B14** Hill | FAIL timeout 60.1 s (machine; `echo` also 60.1 s) | FAIL timeout 60.1 s | FAIL timeout 60.1 s | FAIL timeout 60.1 s |
| **B17** resonance | FAIL · pump [1.34, 17.0], amplitude 0.002, regime 6/28, controls 0/3, 8 unanswered · 24.6/orbit (tick floor) · 37.0 s | FAIL · pump [1.34, 17.0], 7 unanswered · 37 s | FAIL · pump [1.34, 9.8], 9 unanswered · 28 s | FAIL · pump [0.79, 8.8], controls 0/5, 2 unanswered · 12.3/orbit · 20.3 s |

Kicks per orbit measured from `PLANE_TRACE`: B12 about 24400 per ship per 200 periods (nominal
2^7·200 = 25600; passages inside the doll shorten some tubes); B17 pinned by `MIN_STEP = 128`
ticks — steps 7/5/4 all give 24.6 kicks per ship orbit and step 3 gives 12.3, so B17's four rows
are not four cadences (the only differences across 7/5/4 come from captured ships, whose doll
clock makes their steps differ).

**Failure modes** (from the traces, `rows/*repro.err`):
- *Ships die.* 7 of 64 B13 flybys and 5 of 15 B12 ships end in `Resolved::Lost` (a surface —
  `leave_log2` is unreachable at 5.3e8), mid-run or at the flyby's exit sample. The trace shows
  `lost=1, refused=0`: these are crashes, not binding refusals. The reference flies the same seeds
  past the planet at ≥ 1.2 planet radii.
- *The drift is linear.* Every surviving B12 ship rises above the 1e-12 floor with median growth
  exponent 1.0-1.5 at every cadence (the limit is 0.2): the Jacobi error compounds, it does not
  oscillate — the error *type* the gate exists to catch (r10's float replica scored 0.43; the
  shipped integer changeover is worse here).
- *Deep slow encounters are under-resolved.* A B13 flyby with periapsis 1.2 planet radii and
  v∞ = 1.7e-5 has an interaction time (r_p/v_p ≈ 3e8 ticks) far below even the deepest SyMBA
  level's step (h0/64 ≈ 9e9 ticks at 2^7): single kicks of Δv ~ 7e-5 against v∞ = 1.7e-5 — the
  encounter is resolved by kicks each larger than the whole excess speed. This is the same
  structure r10 killed ("no float changeover at the plane's budget reaches 0.2").
- *B17's miniature breaks the resonance outright*: the plane pumps e up to 17× the reference's,
  libration amplitude ratio 0.002, regime matched for fewer than a third of the cases, and the
  non-resonant controls fail at every cadence — far from resonance, where nothing resonant
  happens. This is not a cadence question (24.6 vs 12.3 kicks/orbit barely moves it); something
  in the plane's restricted-problem dynamics at μ = 3e-5..3e-3 pumps eccentricity that the
  reference does not. Suspects the integrator can test first: the origin-fall term's scaling with
  the doll's mantissa at non-power-of-two mass ratios (B12-B14's q = 1/999 vs B17's), and the
  level-0 kick's sampling of the planet's pull when the ship's tube period is commensurate with
  the planet's (kicks at fixed mean anomaly, conjunction at a fixed anomaly too).

**B14** is machine-VOID on this box, honestly: its phase (the judge's own 768 reference moon runs
plus the law) exceeds the 60 s limit for `echo` and for every plane cadence (`planted-notide`,
whose law is cheap, finished at 52.8 s on a quieter box — the plane's moons cost 10^4-10^6 kicks
each and push it over). The probe `moon_probe_b14_physics_not_the_gate` (ignored test, output in
`moon-probe.out`) measures the same physics on the gate's first 12 circular births with one
reference run each: classes 10/12 agree at 2^7 and at 2^3, with one and two moons respectively
LOST by the plane that the reference keeps; apsidal rates read "none" for the reference too
(circular births have no apse — the gate's rated moons come from the eccentric draw). So the
class physics is mostly right and the losses are there too; the apsides remain unmeasured.

**Predictions** (`predictions.md`, written before any gate ran through the plane): the adapter
predictions held (exact round-trip; 5e-4·sep far-ship error falling like H²). The verdict
predictions were wrong in the direction that matters: I predicted B12/B13 PASS at high cadence
with B17 a coin toss and only B14's apsides failing at 2^3. Instead the plane fails all three
gates at every cadence, mostly through ships dying and a linear Jacobi drift that no cadence
cures — the 25% risk I named for B12 (a ship lost below the surface) is the *dominant* mode for
B13 and B12, and B17's failure is total (controls included), which I did not predict. A failed
expectation is not a failed method (H0183): the method here is the judge, and it worked.

**What would make it wrong.** The adapter is the one place an artifact could hide; it is pinned by
the three unit tests (exact boundary, far-ship fidelity, H² cadence attribution) and by `echo`
passing the same gates. A checker should re-run `table.sh` on a machine where B14's phase fits
(the M1) to close the one VOID row, and re-derive the "lost" ships' death cause inside
`crates/universe` (the trace names the sample; `PLANE_TRACE=1 cargo run --release -p xtask --
behave --law plane --gates B13 --plane-step 7` reproduces in 4 s).

**Cost of adopting.** None: nothing here is adoptable as a law change; the adapter itself
(~120 lines + tests, no gate or engine edit) is the deliverable and is one step from merge if the
integrator wants the plane permanently judgeable.

**Fit with PRINCIPLES.** "Errors never compound" (13): measured compounding, exponent ~1.
"Compute only surprises" (3) / "fewer kicks per orbit" (board focus): the table says the lever is
not the cadence — no cadence between 8 and 128 passes — so the next token should go to the
encounter's representation (the board's "changeover near a secondary, reversible and integer"),
not to more kicks. "A test that cannot fail is a control": the planted laws failed every gate the
plane failed, so these verdicts mean something.

**The lens.** A directed build through a frozen judge: it made me measure the engine as shipped
and kept me from tuning anything, but it also meant I spent the window on measurement, not
repair — the two B17 suspects above are derived, not tested, and the B14 apsides row stays empty.
