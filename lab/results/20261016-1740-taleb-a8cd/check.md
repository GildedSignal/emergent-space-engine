Grade: silver

**Abstract.** Claim: main's xtask red on the lab box is libm-conditional corpus selection, not a law regression; the law is bit-identical at the freeze commit. Reproduced bit-exactly after recreating one missing file: the seven deterministic reds (B12 false for Echo; ship #57 at 8.409466703853747e-8, 7016 kicks), census judged 14/11/8 at pristine/±1 ulp, musl corpus 15/16 with different members, glibc correctly rounded on every flagged call, and (mine, ±4 ulp) 14→9→12 — churn persists outside the tested range. Gain: 7 of 10 reds reclassified broken instrument; the M1 rerun becomes optional. Cost: freeze the assessed corpus fields or make the oracle CR-only. Not gold: regen.sh as delivered regenerates nothing in steps 1–5 — patch.diff adds workspace member `work/`, whose Cargo.toml was never delivered.

## Reproduction

Every core number regenerates exactly — but only after I diagnosed and repaired a delivery hole. `work/patch.diff` adds `lab/results/20261016-1740-taleb-a8cd/work` to the workspace (and a `libmprobe` package to Cargo.lock), while the delivered `work/` holds only `crcheck.py`, `patch.diff`, `tree610`. Every `cargo test -p xtask` therefore dies: "failed to load manifest for workspace member …/work … No such file or directory". `regen.sh` (`set -uo pipefail`, no `-e`) still exits 0, and the runner's own `regen.log` shows steps 1–5 **empty** — the delivered artifact regenerates none of the dossier's core numbers, and `regen.txt` records a vacuous "exit 0". After recreating a minimal `libmprobe` stub (name/version per the patch's own lock), on tree a523ace9 + patch:

- The seven deterministic reds, identical messages and values: five `behave::handoff` tests, `events_tests::echo_passes…` with `left: [("B11", true), ("B12", false), ("B13", true), ("B14", true)]`, and `across_a_kick…` ship 3 = 7016 kicks, `across_kick 24.37109375`, `8.409466703853747e-8`.
- Corpus drift: crossings `[10,8,8,14,16,30,22,22,12,34,42,8,28,12,12,22]` (gate line "8..42, at least 20 when frozen"), #88 at 0.271 Rp inside, #138 unconverged, 14/16 judged, excluded 2 > 1.6 → B12 fails. Mechanism verified in source: `kept()` re-assesses through `ship()` (`powf(-0.5)`, `sin`, `cos`) every process; `excluded = kept.len() − converged` (handoff.rs:202–205); the quoted freeze design line is verbatim at handoff.rs:20–21.
- Census: judged pristine 14/16, α+1 ulp 11/16, α−1 ulp 8/16, musl 15/16; trig differ on #70/#83/#88/#138, powf on #83/#106; kept[0] 10→38→30 crossings, closest 59.530→4.156→0.040 Rp; #88 musl 1.578 Rp; #106 musl 0.030 Rp; #138 unconverged→converged. All exact.
- Ulp-stability: 8.409e-8 / 4.563e-9 / 1.478e-7, kicks 7016→5423/5424. Exact. The 5e-8 bar provably sits inside the scatter.
- Freeze control: runner's regen step 6 matches the dossier bit for bit; worktree verified at c84f5787.
- CR check (runner's regen step 7): glibc +0 ulp vs CR on all 15 flagged calls; "musl is the one off" follows from the census flags. Valid.
- Full suite: 10 failed (my first run, 533 s ≈ author's 523 s), 9 failed on the immediate rerun — headline and flaky-tail behaviour reproduced.

## Predictions

`predictions.md` (mtime 17:47) precedes regen.sh (17:57) and dossier (17:58); decisive-run times are not independently logged, but content matches outcomes: P1, P3, P4, P5 verified exactly; P2 honestly amended (the channel is the observable's own chaos, one level deeper than the predicted membership flip) and the amendment is what the selection probe shows (filter keeps kept[0..3]; ship 3 = #57). Kill criterion did not fire.

## Attacks

1. **±4 ulp census (outside the author's ±1 range):** judged 14→9→12. The corpus churns O(ships) at the next decade too — the mechanism holds a fortiori; no ulp distance stabilises membership.
2. **Flaky three solo:** `the_other_gates_can_fail_too` and `each_planted_law_fails_exactly_its_gate` pass alone, but `scale::echo_is_linear…` **failed even solo** under my load — same signature (`Option::unwrap()` at scale.rs:187:44: B10's refusal leaves no "exponent " token to parse). Classification as load-class stands (it fails more under load), but the dossier's "pass when rerun filtered" is load-contingent, not a property.
3. **Two consecutive full-suite runs:** 10 then 9 failures — the extra reds wander with load exactly as the load-class reading predicts, while the seven stay fixed.
4. **Determinism of the seven:** identical messages/values across the author's runs, 7559's 14-October signature, and mine.

## Novelty and the page

Replay-gate open direction 4 (7559's lead: "one M1 rerun decides") is answered by mechanism on the lab box alone. No HISTORY or wiki entry names libm-conditionality; decision-log's machine-noise canon (dfd0, 13 Oct) is the same disease at another layer and is cited, not repeated. The proposed page folds the result in faithfully; I corrected in place: "8 ships under the frozen 20 crossings" → **9** (the vector has 9), the "pass when rerun alone" overstatement (scale test fails solo under checker load), and I folded in the ±4 ulp datapoint.

## Goal fit

PRINCIPLES, Truth: "Canonical outcomes are exact and independent of cache, partition, observation, schedule and **hardware**. Floats never decide them." Today floats decide the B12 corpus's verdicts; the run shows that premise wrong with a measured mechanism (1 ulp → 14→8 judged; verdict flips both directions) and prices three fixes. Not a compute bottleneck — the dossier says so honestly; it is a ruin-state result (every checker on this box has been reading these reds as possible regressions). Taleb-appropriate: fragility of the instrument, concave to one bit.

## Why silver, and the one experiment for gold

The physics and the record-keeping are both real, but the delivered record **cannot regenerate its own numbers**: steps 1–5 of regen.sh silently empty from the missing workspace member, while regen.txt says "exit 0" — precisely the "results that the shipped code could not regenerate" class that has capped runs at silver before (5 October lesson). The fix is one edit: drop the `work` member from patch.diff (the xtask probes need only the `libm` dev-dependency, not `libmprobe`) or deliver `work/Cargo.toml` + `src/`; rerun regen.sh in a **clean** tree and show steps 1–5 non-empty and identical. With that, this is gold on every other leg: reproduced bit-exactly, pre-registered predictions held (one honest amendment), novelty clean, premise shown wrong, adoptable in one step.

## What the author missed

- The clean-tree regen discipline itself: the missing crate means the author never ran regen.sh from a restored tree; the runner's vacuous "exit 0" went unnoticed.
- Fix direction (b) (CR-only oracle) is proposed but unprobed: a CR-only seed path (sqrt/Taylor trig, as the lattice's galaxy generator already does per H0175's "identical on every machine") would show whether judged returns to 16/16 — that is the experiment that proves a fix, not just the disease.
- The flaky-three mechanism stays black-box; my solo-failure observation narrows it to the wall-budget refusal, and the unwrap at scale.rs:187 is a test-harness bug worth one line in its own right.
- The musl arm's understatement (per-step `sin_cos`/`hypot` stay glibc) is disclosed, but the author could have bounded it cheaply: the seed-call distance alone already moves 2–6 ships, and the per-step calls can only add.

Checker's repair disclosure: to reproduce I created `work/Cargo.toml` + `work/src/main.rs` (libmprobe stub, matching the patch's own lock), ran everything above, then **deleted them and restored the tree**; the run folder now differs from as-delivered only by this check.md and the corrected wiki page.
