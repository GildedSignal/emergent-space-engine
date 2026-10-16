# Dossier — 20261016-1835-second-20261016-1740-taleb-a8cd-32a1 (second author on taleb-a8cd)

## Claim

The parent's silver is gold on its own terms once its one delivery hole is fixed — dropping the
phantom `work` workspace member from `patch.diff` makes every regen step run, and in a clean
restored tree steps 1–7 now reproduce **all** of its numbers bit for bit — and the checker's
named missing experiment (the CR-only seed path) returns a sharp negative: **glibc's entire seed
path is already correctly rounded (0 ulp on r, v, cos, sin for all 16 ships), so the CR corpus is
bit-identical to this box's corpus (14/16 judged, #57 at 8.409466703853747e-8 > 5e-8): CR seeds
alone do not restore the frozen 16/16, and they turn the across_a_kick red into a
machine-portable truth.** The machine channel is the oracle's 200-period walk, not the seeds.

## Bottleneck

The same ruin-state bottleneck as the parent (PRINCIPLES, Truth: "Canonical outcomes are exact
and independent of … hardware. Floats never decide them"): the xtask suite is the control behind
the wiki's "reproduced on shipped code" claims, and its B12 corpus verdicts are decided by libm
bits. This run closes the record gap (the silver cause) and prices the fix: the seed leg of
"make the oracle CR-only" is measured to be a **no-op on glibc**, so the repair is either the
walk (deeper) or freezing the assessed fields (fix (a), one table) — the integrator no longer
has to guess which.

## Evidence (clean restored tree, HEAD c9657cd1, xtask/crates identical to the parent's base
a523ace9 — verified by `git diff a523ace9 HEAD -- xtask crates` = empty; regen:
`bash lab/results/20261016-1835-second-20261016-1740-taleb-a8cd-32a1/regen.sh`, core 281 s,
log in `regen.log`)

1. **The record now regenerates (the gold leg).** `work/patch.diff` adds only the `libm`
   dev-dependency (lock checksum included) and five `#[ignore]` probes — no workspace member, no
   `libmprobe`. From a stashed-clean tree, regen step 0 applies it and steps 1–7 all run and are
   non-empty (the parent's delivered regen.log had steps 1–5 empty: its patch pointed the
   workspace at a `work/` crate that was never delivered, so every `cargo test -p xtask` died on
   the missing manifest). `set -euo pipefail` plus grep-or-die per step means a future silent
   hole kills the script instead of exiting 0 vacuously.
2. **Every parent number reproduces bit-exactly** (this run vs the parent's dossier/check):
   crossings `[10,8,8,14,16,30,22,22,12,34,42,8,28,12,12,22]`; the B12 gate line "1 not
   converged, 1 inside the planet", 14 of 14 judged, excluded 2 > 1.6; Echo
   `left: [("B11",true),("B12",false),("B13",true),("B14",true)]`; `across_a_kick` ship 3 =
   #57: 7016 kicks, `across_kick 24.37109375`, `across_kick_over_work 8.409466703853747e-8`
   (ships 0–2: 1.60e-8, 3.10e-9, 6.55e-9); census judged **14/11/8** at pristine/α±1 ulp, musl
   **15/16**, seed trig differing on 4 ships, powf on 2 (kept[0]: 59.530 → 4.156 → 0.040 Rp;
   #88 musl 1.578 Rp; #106 musl 0.030 Rp; #138 musl converged); ulp-stability **7016 → 5423 /
   5424** kicks with 8.409e-8 / 4.563e-9 / 1.478e-7; the freeze control at c84f5787
   bit-identical; crcheck glibc +0 ulp vs CR on all flagged calls.
3. **The CR-only seed path (the checker's named missing experiment), step 5b.**
   `work/crseeds.py` rebuilds the draws exactly (SplitMix64; validated bit-identical k and α
   against the Rust draws in-probe, and r/α against the parent's crcheck prints) and every
   non-CR seed call — `cbrt` in `hill`, `powf(r,−0.5)`, `cos`, `sin` — correctly rounded at 60
   digits. Result: **glibc sits 0 ulp from CR on every component of every ship** (r, v, cos,
   sin; the seed array follows by exact multiplication), so the CR corpus is *this box's* corpus:
   14/16 judged, the same crossings vector, #88 inside at 0.271 Rp, #138 unconverged — B12 still
   fails. Two consequences, both new: (i) "CR seeds return judged to 16/16" is **refuted on this
   box** — the seed leg of fix (b) is a measured no-op under glibc, so the corpus's
   machine-conditionality lives in the oracle **walk** (per-step `sin_cos`/`hypot` over 200
   periods) or in macOS's own seed libm; either way seeds alone cannot repair both machines, and
   fix (a) — freezing the assessed fields beside `HANDOFF_KEPT` — is the only one-leg repair
   left; (ii) the failing observable becomes portable: on CR seeds `j_run`(#57) reads exactly
   7016 kicks / 24.37 quanta / **8.409466703853747e-8 > 5e-8 everywhere** (ships 0–2 pass), so
   `across_a_kick` stops being a per-machine coin flip and becomes a deterministic, portable
   failure — the 5e-8 bar is genuinely exceeded by #57 once the machine is removed, and the
   bar/test is the integrator's to re-derive. Caveat, one line: portability is modulo the
   scene's own `powf` in `period()`/`omega()` inside `j_run`'s setup, the same residual the
   parent disclosed.
4. **The flaky three, one correction reproduced.** In this window's load `scale::echo_is_linear…`
   **fails even when run alone** (step 2), exactly as the checker observed under load; the
   parent's "pass when rerun filtered" did not reproduce. The checker's reading — load-class,
   load-contingent, not a property — is confirmed as the right one; the other two pass alone.
5. **Full suite** (`REGEN_FULL=1`, same script, `regen-full.log`): **202 passed / 9 failed /
   21 ignored** in 521 s — the parent's 10-then-9 load behaviour from the other side; the seven
   deterministic reds stay fixed with identical messages and values, the tail wanders with
   load as the load-class reading predicts. Steps 1–7 have now reproduced bit-identically in
   two independent executions (once from the clean tree with step 0 applying the patch, once
   with the patch pre-applied — the checker's path), plus a third core rerun for the shipped
   `regen.log`.

## Predictions

`predictions.md` was written before the decisive run (mtime precedes regen.log). PG1/PG2 held:
steps non-empty, numbers bit-identical. PC1/PC2 held — PC2 stronger than predicted (0 ulp
everywhere, not ≤1–2). PC3 held in its central branch (CR corpus ≠ frozen 16/16) and sharpened:
the CR corpus is *identical to the current red corpus*, the strongest form of the refutation;
the kill criterion (CR returns the frozen corpus) did not fire. PC4 held: #57 landed at the
pristine end of the predicted scatter range [4.6e-9, 1.5e-7], 8.409e-8; no directional call was
made and none was needed.

## What would make it wrong

- The M1 leg is inferred, not run (no macOS here): the freeze-time 16/16 is the M1's corpus, and
  whether macOS's seed libm is CR on these calls is unmeasurable from this box. Both branches
  (macOS seed CR → the walk is the sole channel; macOS seed non-CR → the seed channel is live
  only there) leave the conclusion standing: seeds alone cannot give both machines one corpus,
  because this box's CR corpus is 14/16, not 16/16.
- The CR table depends on mpmath's 60-digit values (regen regenerates and prints its sha256,
  `e370148d…`); a different mpmath version could move a last bit of a tie. Same exposure as the
  parent's crcheck.py.
- The across_a_kick portability claim covers the seed leg; the scene's `powf` calls in
  `period()`/`omega()` remain non-CR (disclosed above).

## Cost of adopting, and fit

No engine change: the adoption is the parent's fix menu with one leg priced out — (a) freeze the
assessed corpus fields (a small frozen table beside `HANDOFF_KEPT`, the gate keeps its physics
and loses its libm), since (b)-seeds is now measured to be a no-op on glibc and (b)-walk is the
deep fix. PRINCIPLES: "Laws are versioned. Canonical outcomes are exact and independent of
cache, partition, observation, schedule and **hardware**. Floats never decide them" — this run
removes the last ambiguity about *where* the floats decide them (the walk, not the seeds), and
delivers the parent's evidence as a record that regenerates from shipped code in 281 s.

## The lens

Second author: I did the checker's named experiment and the record repair, and attacked the CR
idea from the "what would falsify the fix" side (a no-op on glibc is the sharpest possible
outcome — it deletes a proposed repair leg). What this lens may have missed: the walk channel is
now isolated but not measured per-step (which of `sin_cos`/`hypot` moves the corpus, and how
far macOS sits from glibc there, stays for a run with macOS access or a CR-walk prototype); and
I did not chase the flaky-three mechanism beyond reproducing the checker's solo failure.

## Files

`regen.sh` (core 281 s, ≤ 15 min budget; REGEN_FULL=1 adds ~10 min) · `work/patch.diff` (libm
dev-dep + 5 probes, no workspace member) · `work/crseeds.py` → `work/cr_seeds.txt` (sha256
e370148d3be163d80f88614b50b15630f9039213599d4cef578f7163d7ab5661) · `work/crcheck.py` (the
parent's, unchanged) · `regen.log`, `regen-full.log` · `wiki/replay-gate.md`.
