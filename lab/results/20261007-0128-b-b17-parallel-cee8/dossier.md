# Dossier — 20261007-0128-b-b17-parallel-cee8

**Claim.** B17's resonance legs run on up to four threads (`Law: Sync`, `b17` work-stealing
over its independent cases), so `behave --law plane --gates B17` at the plane's default
cadence passes inside the 60 s phase limit where it timed out before — with bit-identical
detail lines and every verdict unchanged.

**Bottleneck.** The judge's wall time, not a physics question: B17 asks a law 40 independent
`restricted` questions (each builds its own scene; the plane builds a whole universe per
call), and they ran serially because `&dyn Law` could not cross a thread. The plane at its
default step 7 and `space` both died on the 60 s Watch; only steps ≤ 6 passed. Gain: the
phase's leg cost ÷ ~2.6 (measured; four workers, straggler-limited), which deletes the
`--plane-step` workaround from every future B17 run and lets B17 judge the shipped cadence.

**Evidence** (this box: GitHub Actions Linux, 8 vCPU, load ≈ 0.4–0.8, release build; each
command as run, all outputs in this folder as `before-*` / `after-*` / `confirm-*`):

| command (all `…/target/release/xtask behave --law L --gates B17`) | before | after |
|---|---|---|
| `--law plane` (default step 7) | `B17 FAIL timeout: 60.0 s over the 60 s limit` (killed) | **`B17 PASS … [46.01 s]`**; rerun on rebuilt binary `32.56 s`, identical numbers; RSS 131 MB → ≈ 450 MB |
| `--law plane --plane-step 6` | `B17 PASS … [45.62 s]` | `B17 PASS … [22.06 s]`, detail **bit-identical** |
| `--law echo` | `B17 PASS … [9.13 s]` | `B17 PASS … [7.11 s]`, detail **bit-identical** |
| `--law space` | `B17 FAIL timeout: 60.0 s` | **`B17 PASS … [29.55 s]`** |

Detail lines (full lines in the saved outputs): plane default after = `e-pump ratio
[0.999877, 1.000034] over 35 resonant cases … regime 34/34 matched (1 borderline, not
asked); controls 5/5; 0 unanswered, 1 of 41 not converged`; step 6 and echo lines match
their baselines character for character. Reproduce: `cargo build --release -p xtask && …/xtask behave
--law plane --gates B17` (patch: `work/patch.diff`, applies to `main`'s `xtask/src/behave`
only, 12 files, +74/−38).

Verdicts: `cargo test --release -p xtask --bin xtask -- --test-threads=1 behave::resonance`
9/9 pass (echo's exact B17 line, `planted-average` fails B17, the unanswered-case law still
reports exactly "1 unanswered"); `behave::amendment_tests`, `behave::events_tests`,
`behave::tests` pass in isolation. Full-suite control: with the patch 197 passed / 8 failed;
on clean `main` 196 / 9 — every patched-run failure also fails on clean `main` (the
pre-existing B12-family and load-timing flakes of this shared box; B12's statistic is the
known miscalibration, HANDOFF 6 October). The CLI suite fails exactly its two pre-existing
tests both ways (`["G5","B12"]`).

**Predictions** (`predictions.md`, written before the decisive runs): plane default PASS
✔ but my 20–35 s wall estimate was low (46.0 s first run, 32.6 s confirm — step-7 legs are
≈ 2.6× step-6's, not the 2× I assumed, and one heavy case per worker caps the speedup);
echo and step-6 bit-identical ✔; space PASS ✔; planted verdicts kept ✔; RSS ≈ 4× one
serial leg's set, ≈ 0.45 GB ✔ (limit 2 GB).

**What would make it wrong.** A law whose `restricted` keeps call-order state would now be
asked in a schedule-dependent order — the trait doc forbids it and every in-tree law builds
per-call state (the plane's universe, the reference's steppers, `Space`'s memo now a
`Mutex` around a pure cache); any detail-line drift between serial and parallel runs of the
same law would be that bug showing (none observed: three laws bit-identical). Cost of
adopting: `Law: Sync` is a contract on future laws (state per leg lives inside the call),
and B17's phase now takes up to four threads (the truths already did). Margin is ≈ 14–27 s
against the 60 s Watch on this box; the M1 re-measures (30% thermal swings are the norm
there) — if it runs hot, raising the worker cap above four is a one-line change, but four
matches `truths()`'s own convention. Fit: "local laws are great because parallelizable"
(15); "no work for no reason" (14) — the legs were independent work done serially; the
criteria, thresholds and gates are untouched (frozen: `git diff` shows only harness).

**The lens.** A build lens sees the harness, so I could miss that the *physics* margin is
thin: B17's 46 s is legs-dominated, and the real headroom on the M1 is unknown here. I also
accepted the pre-existing B12-family test failures on this box as environment after a
stash-control, not after diagnosing each one; and mid-run a sibling lab run's cleanup
reverted this tree (its `run.sh` restores the checkout), which wiped my edits once — the
patch was rebuilt from the session's hunks (`reapply.py`), re-verified bit-identical
(`confirm-plane-B17.txt`), and saved; checkers on shared checkouts should snapshot their
diff early.
