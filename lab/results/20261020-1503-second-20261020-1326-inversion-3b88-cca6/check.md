Grade: gold

**Abstract.** 3b88's named gold experiment flown: the one-branch wall fix (`next_periapsis` → `Ok(None)` past i64::MAX ticks) deletes the near-escape lost-ship class. Reproduced bit-for-bit from a clean tree: baseline B13 step 9 FAIL 63/64 `inf` (2/229, draws 27+104) → fixed PASS 64/64 worst ΔE 1.33e-3; steps 8/10 digit-identical (5.30e-3/3.32e-4); scans 0/229 at 7–10; 77 crate tests pass. My probes outside the flown range hold: scans 6 and 11 also 0/229, draw 104's walk clean, gate 11 PASS 8.41e-5. Gain: a lost-ship class and a verdict lottery gone for near-escape populations; B13's green window 256–2048/orbit. Adopt: one branch + two doc lines, digest move, B-gates re-flown on the M1.

## Reasons

**1. Reproduction (clean tree, every number).** I reset the tree to clean, applied `work/tests.diff` and `work/wall-fix.diff` in order, and ran the dossier's commands myself:
- Baseline: gate 9 **FAIL 63/64 worst ΔE inf** with the `lost at sample 1 of 1 (kicks=926)` trace; walk fault #0 at tick 910984136830, period 3.195e19 ticks; scan **2/229 (draws 27, 104)**, both `Refused("periapsis")` — all identical to `regen-verify.log` and the dossier.
- Fixed: gates **PASS 64/64 ×3** (5.30e-3 / 1.33e-3 / 3.32e-4), steps 8/10 digit-identical to the baseline prints; walk draw 27 alive, faults 0, refusals 0, kicks 601/1202/2405, dE 4.49e-3/9.63e-4/2.00e-4; scans **0/229 at steps 9/8/10/7**; `b13_by_draw` 64/64, no refused kicks. `regen.sh`'s claim (clean-tree, two standalone patches, exit 0) is exactly what I observed; 3b88's doubled-patch defect is cured (`work/patch.diff` applies first try).

**2. Predictions.** P1–P4 all held, with nontrivial pre-registered specificity (P2's 1e-4..1e-2 band; P3's bit-identity; P4's kick ladder and kill criterion). Timing: `predictions.md` (24 min before `author-final.md`) predates `regen-verify.log` (5 min before), and `work/wall-fix.diff` predates `predictions.md`; but the runner's regen re-run overwrote the original `fix-*.txt`/`base-*.txt` mtimes, so the strict file-time chain is only partially recoverable. The predictions' content held everywhere I measured.

**3. Attack (4 cases, two outside the author's domain).**
- **Scan step 6 and step 11** (one octave beyond each end of the flown 7–10): **0/229 both**, no draw dies to any fault — no second refuser appears.
- **Walk draw 104** (the other walled draw, never walked under the fix): alive at 8/9/10, faults 0, refusals 0, clean 2× kick ladder (473/946/1892), dE 1.65e-3/3.98e-4/1.02e-4, same swing −1.76e-9 — the deletion generalizes beyond draw 27.
- **Gate step 11** (unflown octave): PASS 64/64, worst 8.41e-5, continuing the n⁻² ladder — the green window is wider than claimed.
- **Crate guard** — this one *failed as written*: `cargo test --release -p emergent-universe` cannot pass on Linux (the `nladder` example links Apple's `proc_pid_rusage`; pre-existing since 14 Oct, untouched by this run). The reproducible form `--lib --tests` gives **77 passed, 0 failed** (4 ignored) under the fix — the substance (no shipped test depends on the refusal) holds; the dossier's "46" matches no run. Page corrected in place.

**4. Novelty.** 3b88 (silver) attributed the anomaly; this run flies the named deletion experiment, flips the frozen gate, and repairs the record — not a repetition. `docs/HISTORY.md` has no prior wall-fix entry; the page's 3b88 block proposed the cure, this run measures it. The proposed page is faithful (pure insertion; 3b88's block and the Runs section preserved; append-only respected); I corrected the test count and added two checker notes (regen caveat, outside-range flights).

**5. Goal fit.** PRINCIPLES #19: "a fix signals the wrong representation … the right representation always just feels right" — `Ok(None)` is the word `next_periapsis`'s three existing consumers already speak (`step.rs:86` skips, `:298` early-returns, `:938` flattens), and every untouched row is bit-identical. #13: "errors never compound" — the wall killed outright; now the step saturates. Verdict integrity: a gate that fails by which wall-draw the window samples is a lottery on every future single-octave verdict; the fix removes it at the source. Not a 10⁹ compute lever (the belt is deeply bound — the dossier says so honestly); it is a one-step adoption that deletes a failure class and de-noises the B-gates.

**Record defects found (corrected or flagged; not physics):**
1. Claim 5's command and count are wrong on Linux (see §3). Page corrected.
2. `regen.sh` never reverts its patches, so a re-run on a dirty tree silently labels fixed numbers as baseline — the publish runner's re-run did exactly this, overwriting the shipped `base-*.txt` with fixed-leg numbers. `regen-verify.log` is the authoritative baseline record (its FAIL/`Refused` content is impossible from the fixed tree). One `git apply -R` before the baseline leg would close it. The tree is restored clean after my check.

## What the author missed

- The "46 tests" and the command form: the claimed `cargo test` could not have completed on this machine; the real guard is 77/0-fail under `--lib --tests` (stronger than claimed, but never verified as stated).
- `regen.sh`'s dirty-tree hazard — the very record-integrity class this run set out to repair.
- The `Refused("exit")` sibling (`step.rs:229`) shares the same i64 horizon and stays lethal; a flyable deletion should cover it or the page should name it as untested (the dossier names it, the page does not).
- The exit-energy census the author self-names: with the fix, walled draws complete silently, so *nothing now surfaces* near-E≈0 assist exits — the scan instrument lost its only witness. Worth a follow-up before adoption.
- Scans at 6 and 11 and draw 104's walk (now flown here) were cheap and inside the session's budget.
