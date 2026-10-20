# Dossier — 20261020-1503-second-20261020-1326-inversion-3b88-cca6 (second author on 3b88)

## Claim

The checker's named gold experiment is flown and it held: with the wall fix —
`next_periapsis` reads "next periapsis past every representable tick" as `Ok(None)`,
one branch in `crates/universe/src/step.rs` — **every wall loss vanishes (0/229 flown
draws at each of steps 7, 8, 9, 10, against the baseline's 1/229, 2/229, 0/229 at
8/9/10), B13's step-9 verdict flips FAIL 63/64 `inf` → PASS 64/64 worst ΔE 1.33e-3 —
bracketed by the untouched octaves (step 8: 5.30e-3, step 10: 3.32e-4, both
bit-identical to the baseline prints)** — and the record now regenerates from a clean
tree (`regen.sh` applies two standalone patches, `work/tests.diff` and
`work/wall-fix.diff`, and rebuilds between the baseline and fixed legs; verified
clean-tree exit 0). The deletion 3b88 named is demonstrated, not just proposed.

## Bottleneck

Not a compute term; closing 3b88's gap to gold (a verdict-integrity hazard plus a
one-line deletion). The record repair removes the defect that kept 3b88 silver (its
`work/patch.diff` carried the diff twice; `git apply` refused on a clean tree); the
fix flight converts 3b88's "named deletion target" into a measured deletion: the
`Refused("periapsis")` lost-ship class is gone at every cadence, and every future
B13-style single-octave verdict is de-noised at the source. Expected gain for 10⁹
today: none (the belt is deeply bound); for near-escape populations (assists,
ejections, scattering): a whole `lost`-ship class stops existing.

## Evidence

All numbers regenerate from shipped code + the two patches via `regen.sh`
(~11 min from a clean tree, verified exit 0). Baseline leg (shipped law, tests only)
re-anchored 3b88's record on this tree bit-for-bit before the flight:
gate 9 FAIL 63/64 `worst ΔE inf` with the `lost at sample 1 of 1 (kicks=926 … lost=1)`
trace (`base-gate-9.txt`); walk fault #0 at tick 910984136830, doll 0, period
3.195e19 ticks (`base-escape-9.txt`); scan 2/229 draws 27+104, same fault
(`base-scan-9.txt`).

Fixed leg (`work/wall-fix.diff`: `i64::try_from(...).ok()` in place of the
`map_err(|_| Error::Refused("periapsis"))`, plus doc lines; the two print-only tests
byte-identical to 3b88's `work/fix.diff`):

1. **Survival (the deletion):** `B13_STEP=N cargo test --release -p xtask
   b13_draw_scan -- --ignored --nocapture` — **0/229 at steps 9, 8, 10 and the
   held-out octave 7** (`fix-scan-*.txt`); baseline: 2/229 at 9 (draws 27, 104),
   1/229 at 8 (draw 104), 0/229 at 10, and the checker's 0/229 at 7. No draw dies to
   any fault.
2. **The gate flips by losing only the anomaly:** `behave --law plane --gates B13
   --plane-step 9` — **PASS 64/64, worst ΔE 1.33e-3 ΔL 1.33e-3**, no loss trace
   (`fix-gate-9.txt`); inside the brackets, on the n⁻² ladder between 5.30e-3 (step 8)
   and 3.32e-4 (step 10). `b13_by_draw`: 64/64 within 1%, no `inf` row
   (`fix-bydraw-9.txt`).
3. **Other rows unchanged, bit-for-bit:** fixed gate 8 = **PASS 64/64 worst ΔE 5.30e-3
   ΔL 5.30e-3** and fixed gate 10 = **PASS 64/64 worst ΔE 3.32e-4 ΔL 3.33e-4** —
   identical to 3b88's baseline prints to every digit (`fix-gate-8.txt`,
   `fix-gate-10.txt` vs its `gate-8.txt`/`gate-10.txt`). The fix touches only orbits
   whose next periapsis is past i64::MAX ticks; no healthy row's plan changes.
4. **The mechanism dissolves, not mutates:** `B13_STEPS=8,9,10 b13_escape_refusal`
   on draw 27 with the fix — **alive at all three octaves, faults 0, refusals 0,
   lost 0**, min kick E −1.171e-9 / −1.172e-9 / −1.172e-9 doll-units (the swing is
   the same orbit), dE err **4.49e-3 / 9.63e-4 / 2.00e-4** (the octave brackets'
   values, unremarkable), kicks 601/1202/2405 — a clean 2× cadence ladder
   (`fix-escape.txt`). Baseline step 8/10 for the same draw: 4.49e-3 / 2.00e-4 —
   the never-walled path is bit-identical under the fix.
5. **Law-contract guard:** `cargo test --release -p emergent-universe` passes with
   the fix applied (no shipped unit test depends on the refusal).

## Predictions

`predictions.md` was written after the baseline legs and before any fixed run. All
four held: P1 (0/229 at every octave incl. the held-out 7), P2 (PASS 64/64, worst
1.33e-3 inside the predicted 1e-4..1e-2 band; draw 27's own dE 9.63e-4 unremarkable),
P3 (steps 8/10 identical to the baseline prints, digit for digit), P4 (no fault,
alive, same swing −1.17e-9, kicks 1202 = 1.3× the baseline's death-at-926). The
pre-registered kill criterion (a second `Refused("periapsis")` source, or a shifted
8/10 row) did not trigger.

## What would make it wrong

The flight is one stream (B13's JUPITER assist census) at four octaves: it shows the
class deleted wherever it was measured to strike, not that no other stream can reach
the wall by a different refuser (`Refused("exit")` at `step.rs:229` shares the
i64-tick horizon). Adoption is a law change — a digest move; the B-gates must be
re-flown on the M1 before merge, and this run's gate evidence is Linux/x86 (orders of
magnitude only, per the lab's rule; B13 is deterministic, so the verdicts should
carry, the timings will not). Cost of adopting: one branch plus two doc lines in
`next_periapsis`; nothing else in the plane's plan reads differently, by P3's
bit-identity. Fit with PRINCIPLES: #19 — "a fix signals the wrong representation …
the right representation always just feels right": the plan asked for a tick that
cannot exist, and the representation already had the right word (`Ok(None)`, the same
word a passage past its periapsis speaks); the flight shows the fix lands like
"cutting butter": losses vanish, every other row bit-identical. #13 — errors never
compound: the wall killed outright; now it saturates (the step tops out at MAX_STEP
until a handoff retimes the body).

## The lens

The second-author lens ran exactly the named experiment and repaired the record; what
it may have missed: (a) whether B12/B17's streams brush the wall at their octaves —
needs stream-specific scans, not flown here; (b) the wall's clock_exp < 0 dependence
(deeper dolls move the threshold proportionally — unmeasured); (c) the checker's
observation that draws 27 and 104 stall at the identical state (r 5.280e8,
v 6.155e-5 doll-units), suggesting the assist's exit-energy distribution piles up
near E = 0 — a census of exit binding energies was not flown (it needs a new
instrument; with the fix, walled draws complete silently, so the scan no longer
surfaces them); (d) the fix demonstration is this run's patch only — the shipped
crate is untouched, and adoption is the integrator's digest move.
