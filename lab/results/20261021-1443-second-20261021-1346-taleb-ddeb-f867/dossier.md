# Dossier — 20261021-1443-second-20261021-1346-taleb-ddeb-f867

**Claim.** The checker's named experiment, run: on cbe6's own instrument, **every fine class of
the plane's belt floors at 16 kicks per Giant-period** (≈ 5.3 per belt orbit ≈ 8 per synodic
conjunction) — the 3:1 resonance zone *including its centre* (worst scaled Jacobi 0.9–3.2×10⁻⁵
against B12's frozen 10⁻⁴ bar), the interior Hill bridge down to 4.1 Hill, and the e-tail to
e = 0.4 — so the census's 78–700× headroom interval **pins to 838×** (713× at one octave finer),
and ddeb's "not ~10³" correction retracts: it was the borrowed 256/own-orbit encounter floor,
not the belt, that made the rescue look small.

**Bottleneck.** Board macro row 1 (kicks per body, ~10³ at stake): the desynchronised grid's
belt headroom. ddeb (silver) priced the composed rate at 115 events/body/belt-orbit (78×) with
the zone floor borrowed from B13; the checker named the missing experiment ("pins the 78–700×
interval to a number and makes the refutation unconditional — or retracts it"). This run flies
it: the interval pins to **10.73 events/body/belt-orbit → 838×**, and the retraction is the
outcome. What it deletes: the fine-class split itself — the belt is *one* cadence class at one
constant (16/GP) for 99.7% of its bodies; the per-class Δs constants the desync design was
waiting on are now measured and there is only one.

**Evidence.** All from `crates/universe/examples/zonecad.rs` (new, this run's patch): cbe6's
`beltcad` verbatim — same scene (star + Jupiter 2⁻¹⁰ at 5.27×10⁸, surface 49,000), same sampler,
same scaled-Jacobi metric, same SEED dial — with the belt drawn from the shipped birth law
(`ladder_ship`'s belt arm verbatim) and kept by ddeb's census predicates. The control reproduces
cbe6 to the digit (`beltc`: 9.4×10⁻⁶–1.2×10⁻⁵ at step 4, Δe identical), and the printed per-ship
kick step H re-confirms step_log2 = 4 ↔ 16 kicks/planet-period. 12–16 ships per arm, horizon
100 planet periods + 400-period walk check (cbe6-checker's precedent), seeds 1/2/3.

| census class (population) | ddeb's floor | measured floor | worst J at it (100 P / 400 P) |
|---|---|---|---|
| clean, gap ≥ 6.3 Hill (41.1%) | 16/GP (cbe6) | **16/GP** ✓ | 1.0–1.9 / 1.1–2.5 ×10⁻⁵ |
| zone 3:1, q = 2 (9.4%) | 256/own-orbit | **16/GP** | 0.9–2.2 / 1.5–2.4 |
| zone 3:1 centre (inner tenth) | (same) | **16/GP** | 1.1–2.5 / 1.2–3.2 |
| bridge 5–6.3 Hill (B64 bulk) | 64/GP | **16/GP** | 1.2–2.6 / 1.3–2.2 |
| bridge 4.1–5 Hill | 64/GP | **16/GP** | 1.2–2.9 / 1.9–2.7 |
| e-tail, e > 0.23 (0.26%) | 256/own-orbit | **16/GP** | 2.0–8.1 / 2.4–5.5 |
| strong tide < 4.1 Hill (0.26%) | 64/GP | unmeasured, kept 64 | cbe6's 1.5–3 Hill control died at 4 |
| first-order (67be: none, D1 = 0) | ∞ | not retested | 0.148 AU margin stands |

- The ladder is n⁻² through the floor (zone: 3.7×10⁻⁸ → 1.6×10⁻⁷ → 7×10⁻⁷ → 3×10⁻⁶ → 1.6×10⁻⁵,
  ×4.3/octave) and breaks super-quadratically at step 3 (worst 1.1×10⁻⁴–1.9×10⁻³, all arms).
  Zero deaths, zero read refusals, zero doll captures at every step ≥ 3. The Δe pump is
  step-independent per ship to the digit at passing steps (zone ship 7: 1.8×10⁻² at every
  cadence; corrupted only at step 3) — cbe6's built-in control, holding in the zone: the
  resonant pump is real dynamics, not error.
- **Composition** (`beltcensus.rs`, ddeb's + three floor args; defaults reproduce ddeb bit for
  bit: 115.41/78×): at floors 16/16/16 the composed rate is **10.73–10.74 events/body/belt-orbit
  (both combs) → headroom 838×** on seeds 1/2/3; the plane's own 2,700 bodies give 837–841×;
  zone one octave finer (32) gives 713×. The 17.8% "tail" now pays its population share — the
  bill is flat across classes.
- **Geometry check** (conservative direction): the scene's planet is circular at 5.2 AU; my
  bridge arms' conjunction distances (1.78–2.25 AU) cover the census's bridge class (5.4–6.3
  Hill against the plane's e = 0.05 Giant ⇒ 1.92–2.24 AU) and extend 0.14 AU deeper.

Commands (`regen.sh`, ~6 min; single arms ≤ 60 s each on 8-vCPU Linux):

```
cargo run --release -p emergent-universe --example zonecad -- 4 100 16 zone31 1    # the zone floor
cargo run --release -p emergent-universe --example zonecad -- 4 400 16 zone31 1    # the walk check
cargo run --release -p emergent-universe --example zonecad -- 4 100 12 zone31c 1   # the centre
cargo run --release -p emergent-universe --example zonecad -- 4 100 16 bridge 1    # the bridge floor
cargo run --release -p emergent-universe --example beltcensus -- 1000002 1,2,3 1.0 shipped 16 16 16  # 838×
```

**Predictions** (`predictions.md`, written before the flights). Held: bridge PASS at step 4
(1–4×10⁻⁵ predicted, 1.2–2.6 observed); clean eccentric PASS at 4 (1–3 predicted, 1.0–1.9);
no deaths/refusals anywhere; seeds within ×3 and the floor octave stable; Δe step-independent.
**Missed, reported — the headline:** I predicted the zone floor at step 5 with step 4 FAIL
(confidence 0.4); the bracket's branch (a) fired instead — step 4 passes at 4–5× margin, and
the composed headroom (predicted 180–320× on my point) lands at 838×. The coherent-phase
argument for a finer floor was wrong: at q = 2 the conjunction-sampled cadence holds *inside*
libration. The prediction file itself said this branch "retracts ddeb's premise correction" —
it does.

**What would make it wrong.** (a) Horizon: 400 planet periods ≈ 4,700 yr; 3:1 libration
periods can exceed that, and the certificate covers only what the horizon samples — but the
worst-J grew ≤ 10% from 100→400 P (bounded, not walking) and the Δe pump is cadence-independent,
so a Myr-scale walk is not evidenced either way. (b) The floor is measured at the 3:1 and applied
to weaker q ≥ 3 zones (4:1, 5:2, …) — conservative in direction (weaker resonance ⇒ coarser
floor), but not measured per zone. (c) The strong tail < 4.1 Hill (0.26%, cbe6's control died at
step 4 there) is kept at 64: its bill share is 0.11 of the 10.73 events; flipping it moves
nothing. (d) The scene is one Jupiter, circular at 5.2 AU; Cinder/Home/Moon tides at belt
distance are ~50× weaker (cbe6's bound) and cannot demand a finer cadence than the conjunctions
they ride. (e) The e-tail's margin is the thinnest (worst 8.1×10⁻⁵ ≪ but 1.2× under the bar on
one seed): if a longer horizon flips it to 256, headroom goes 838 → ~810. (f) The 9,000/orbit
anchor is the board's/cbe6's, not re-derived. The width-sweep robustness changes character: with
every class at one floor the bill is width-insensitive; the width model now controls only
first-order *exposure* (D1 = 0 at the nominal width, 0.148 AU margin; the checker's widened
window put ×2 at 2.9% first-order → headroom 0) — placement, not cadence, is the cliff, and
ddeb's placement arms ([3.0,3.5) dies; [1.4,2.4) 231×) stand unchanged.

**Cost of adopting, and fit.** Adoption is a constant, not code: the desync grid's belt class
is one — Δs = 2⁻⁴ of the Giant-period grid for 99.7% of belt bodies — and the headroom sentence
reverts to cbe6's ~10³ (now measured per class, not assumed). PRINCIPLES 33 ("a body resolves
only the influences significant at its own scale"): the census's price list collapses to one
line — the raindrop and the zone pay the same, because at 8 per conjunction both are resolved;
PRINCIPLES 2 (error type over size): the certificate is the frozen bar on the conserved
quantity, and the resonant pump passes *through* it unchanged. The 67be rule survives scoped:
*first-order* resonance is cadence-blind; q = 2 at game scale is not.

**The lens.** Second author on ddeb (taleb): the run's own heuristic — "never trust an average
where tails decide" — cut both ways. ddeb found the tail (17.8% paying 75%) but priced it with
another class's floor; the checker's instrument, flown here, shows the tail was never expensive.
What this lens may have missed: the horizon question (a) is the honest open edge — a
libration-scale flight (≥ 800 P) or B12 v3's Allan rule on the zone series would close it; and
one Jupiter is not the plane — the composed 838× is a scene constant, to be confirmed once the
desync constants land in `ext`.

**Grade suggested:** gold — the checker's named experiment flown on the named instrument, the
record regenerates from shipped code (`regen.sh`, clean tree, verdicts PASS/FAIL table printed),
the 78–700× interval pinned to 838× by measurement, and the original claim corrected in the
direction the experiment chose (retraction, the branch ddeb itself flagged as possible).
