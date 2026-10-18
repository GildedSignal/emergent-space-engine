# Dossier — 20261018-1617-spacex-37c1 (SpaceX lens)

## Claim

In the flown fleet, the contact-skip channel is closed at the shipped speeds by the scene's
own radius scale (0 skips in 1,620 detected contacts, ρ = reach/|w| ≥ 10⁴), and it reopens at
relativistic closing (~0.8 c) through a mechanism the driven-pair law does not cover: ~10–12%
of detected contacts ghost because their crossing completes inside the detection-to-resolve
window — skips observed at ρ up to 9.6, where the per-pair law `max(0, 1−ρ)` predicts exactly
zero — and the skip set is bit-identical between the sparse and dense steppers.

## Bottleneck

`lab/wiki/contact-speed.md` open direction 3 ("the real rate in a flown fleet … unmeasured";
the board's encounters class). Not a 10× on a board axis: it closes an open direction with a
measured boundary and corrects the mechanism's domain (the per-pair bin law vs the batch's
resolve-instant gate), which is the input to direction 1's adoption decision (whether the
root-normal fix is needed for the shipped plane: it is not, at today's speeds and radius
scale; it is, the day missiles or fast crossers fly in the lattice frame).

## Evidence

All numbers from shipped code (`xtask universe --bench`, headless scripted player, seed as
stated, 30 s of game at rtf 100, members as stated), with a print-only census at the
resolver's receding gate (`relativity.rs::resolve_law`): every pair reaching a response batch
logs (|w|², d·w, reach) — the gate's own integers; skip ⟺ d·w ≥ 0, exact. The battle's
closing speed is dialled by `SPACEX_SPEED_DIV` (shipped 2¹⁵), the stepper by `SPACEX_ORDER`
(shipped sparse = EventCore). Files: `sweep.sh`, `analyze.py`; raw censuses in `cens/`.

| arm (speed_div, members, seed) | order | contacts | skips | skip % | ρ = reach/\|w\| p50 (min) | \|w\| p50 |
|---|---|---|---|---|---|---|
| 2¹⁵ = shipped, 48, s1 | sparse | 49 | 0 | 0.0 | 3.7×10⁴ (1.2×10⁴) | 44 q/ch |
| 2¹⁵ = shipped, 400, s1 | sparse | 1,571 | 0 | 0.0 | 4.2×10⁴ (1.0×10⁴) | 38 q/ch |
| 128, 48, s1 | sparse | 50 | 0 | 0.0 | 1.3×10² (58) | 1.3×10⁴ |
| 8, 48, s1 | sparse | 53 | 0 | 0.0 | 9.4 (4.0) | 1.6×10⁵ |
| 4, 48, s1 | sparse | 44 | 2 | 4.5 | 3.8 (1.7) | 4.5×10⁵ ≈ 0.43 c |
| 2, 48, s1 | sparse | 41 | 5 | 12.2 | 1.7 (0.93) | 8.8×10⁵ ≈ 0.84 c |
| 2, 48, s1 | dense | 41 | 5 | 12.2 | — census bit-identical (`cmp`) | |
| 2, 48, s2 (held out) | sparse | 32 | 3 | 9.4 | 3.0 (1.05) | 5.5×10⁵ |
| 2, 400, s1 | sparse | 1,451 | 46 | 3.2 | 2.8 (0.83) | 5.7×10⁵ |

Dose-response: the arm skip rate falls with the arm's dwell 2ρ — 12% at ρ p50 1.7 (sd2),
4.5% at 3.8 (sd4), 3.2% at 2.8 (sd2m400, the 400-member battle mixing in scatter-speed
contacts), 0 at ρ p50 ≥ 9 (sd8, sd128, shipped). Per contact, a skip is observed wherever
the whole crossing fit the resolve window, up to ρ = 9.6 (sd2m400): the per-pair arrival
law's zero at ρ ≥ 1 does not bound the flown scene at any measured speed.

Mechanism (per-contact τ\* = −d·w/|w|², the chronons to closest approach at the resolve
instant; full table in `analyze.py` output, `cens/tau-star.txt`): every skipped contact has
τ\* ∈ (−1, 0) — the crossing finished within the chronon before resolution — and every
resolved contact has τ\* > 0; skips occur at ρ = 0.93 … 9.6. So the gate fires on
**resolve-instant receding**, not on the driven-pair law's ρ < 1 condition: with the scene's
radii (reach ∈ [1.1, 2.1]×10⁶ quanta against c = Q = 2²⁰ quanta/chronon, v\* ≈ 1.4 c), the
dwell at any legal closing is ≥ ~2 chronons and the skip rate is set by the fraction of
contacts whose whole crossing fits inside the detection-to-resolve window, not by ρ alone.
At the shipped speeds the dwell is 10⁴–10⁵ chronons and the gate can never fire (measured 0
in 1,620).

Reproduce (`regen.sh`, ≈ 7 min): `cargo build --release -p xtask`, then the sparse arms
(ship48, ship400, sd128, sd8, sd4, sd2, sd2s2, sd2m400; ≤ 60 s each), the short dense
identity check (3 s of game covers the whole battle: 41 contacts, `cmp`-identical census),
then `analyze.py` over `cens/*.cens` and the per-contact τ\* table. The sd4 and sd2m400 arms
were added after `predictions.md` was frozen, as the dose-response check; no number in the
table was tuned after the fact.

Instrument note (a lab trap worth recording): the machine's ambient `CARGO_TARGET_DIR`
(`~/lab-target-1`) is shared by the window's parallel runs; a sibling's clean-tree build can
replace a patched rlib under a running experiment, which silently reverted this run's speed
dial mid-session (every fast arm came back at shipped speed until noticed — the census was
still internally consistent, which is what made it sneaky). `regen.sh` therefore builds into
its own target directory with the ambient variable unset; every number above was re-derived
that way, bit for bit.

## Predictions

`predictions.md` was written before the sweep. P1 held (0 skips, ρ ~ 10⁴–10⁵). P2 **failed as
worded** ("sparse arms skip ≤ 2%, single-pair components cannot skip"): skips are 12% at
speed_div 2 — the resolve instant is not the pair's own root-bin start in a many-body
component, so the "approaching at detection" guarantee does not survive to resolution; the
failure is the finding (the skip in flight is a scheduling ghost, not the bin law). P3 held
in value (dense arm ~10–30%) but for the wrong reason — it is not a stepper difference: the
two steppers' censuses are bit-identical, so the dense arm is a control, not a contrast. P4
held (seed 2: 9.4%). P5 held (ρ ≥ 0.9 everywhere; the deep-skip regime ρ ≪ 1 is unreachable
in this scene at any legal speed).

## What would make it wrong

A contact census that misses pairs the resolver sees (mine is inside `resolve_law`, after
the consumed filter and component assembly — it counts exactly the pairs the gate decides
on, both steppers); or a flown fleet whose members do not share the battle scene's radius
draw (r ∈ [q/2, q]) — a future scene with ship-scale lattice bodies (reach ~ 10²–10³ quanta)
would put v\* at 10⁻³–10⁻² c and the bin law's regime, not this one, would govern. The
domain is the plane's fleet battle (two armies, one seed pair, 30 s of game); the player's
own contacts with fleet members are doll-level and only logged (`universe.rs`), so they are
outside this census by construction.

## Cost of adopting, fit with PRINCIPLES

Nothing to adopt in the engine: the shipped plane needs no fix (0 skips, structural margin
10⁴). The page's direction 1 (the root-normal impulse fix) stays unscheduled for the plane
and stays required for fast crossers/missiles in the lattice frame. Cost of the measurement
itself: a print-only census, deleted with the patch. Fit: "Compute only surprises" and "a
failed expectation is not automatically a failed method: diagnose which one broke" — the
driven-pair law and the flown-fleet rate are two different laws of the same gate, and the
flown one is now measured. "Measure before claiming, and never strawman": the prior bound
("at manoeuvre-scale relative speeds the skip channel is ≤ 10⁻² of transport") is confirmed
at the shipped arm with the margin now known to be structural (radius scale), not
statistical.

## The lens

The SpaceX lens pushed requirements-first ("which requirement owns the skip channel?") and
controls on both sides (shipped arm as negative, dense stepper as a second instrument —
which turned out to be the same instrument, a lesson the memo artifact taught the lab). What
it may have missed: the player-side contact path (doll-level, unresolved) is where a real
game would first feel a fast crosser, and this run does not touch it; and the census is
30 s of game per arm, so rare slow channels (a leaver re-entering after minutes) are unbodied
here.
