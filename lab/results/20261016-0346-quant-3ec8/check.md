Grade: silver

**Abstract.** `plan_clock`'s three own-state reads served by one pure `readout`: the birth pass
cuts 6.05–7.43 µs/body (18–22%) and the birth rail 42.4–43.7 → 35.8–37.4 µs/body, digest-identical
everywhere. Reproduced: all 18 flights re-flown on a clean tree — digests byte-identical between
arms at all 8 configs **and equal to the record's own digests**; a pristine build's digests equal
the OFF arm's. My cuts: 6.4–7.8 µs/B (median 6.74, 6/8 configs; outliers 2.1–10.7 under load, this
box shared). Held out: seeds 11/3 digest-equal (cuts 5.5–7.6), N=6×10⁵ (2× max) digest-equal, cut
8.3 (24.4%), and all 13 `ladder_digest` scripted flights (burns, mashing, wave, crossings)
digest-identical post-flight. Gain ~1.2× on the rail — adoptable in ~15 lines, but under gold's
letter. One record defect: the shipped `patch.diff` is doubled, so `regen.sh` fails on a clean tree.

**Reasons.**
1. **Reproduction (bit-exact).** The runner's `regen.sh` exit 101 is diagnosed:
   `work/patch.diff` contains every file's diff **twice**, so `git apply` fails atomically;
   regen's idempotence check misreads "does not apply" as "already applied", skips, and
   `cargo build` dies on the missing `pass_bench` bin. With one de-duplicated copy applied by
   hand, everything regenerates: the full `ab.sh` matrix gives digests equal between arms at all
   8 (N, seed) configs **and equal to the author's recorded `ab.jsonl` rows** (cross-box,
   cross-build). My own pristine build (step.rs+universe.rs reverted, harness kept) digests
   `3c02e035…` (10⁴ s1) and `6338ec25…` (3×10⁵ s7) — the author's pristine numbers, equal to my
   OFF arm. The pristine≡OFF≡ON triangle holds independently.
2. **Timing** (Linux/x86, shared 8-vCPU box, orders of magnitude per the lab rules): my pass
   cuts 6.72/6.43/7.79/7.53/6.75 at 10⁴–10⁵ (author 6.05–7.43); two contended outliers (3.35 at
   3×10⁴ s1, 2.09/10.71 at 3×10⁵) — the same spread the fix pass itself re-measured (4.8–11.1).
   Rails 43–46 → 36–39 µs/B (author 42.4–43.7 → 35.8–37.4). requeue+rekey ≤ 0.154 µs/B (author
   ≤ 0.099): immaterial either way.
3. **Predictions.** `predictions.md` (03:52) predates the decisive flights (04:14). P1 held
   (8/8, plus my 3 new configs); P2 held (6.4–7.8 central vs predicted 6–8); P3 held on the
   author's held-out seed 7 and on my seeds 11 and 3 (5.5–7.6); P4 held (≤ 0.154, load noise).
4. **Attack, beyond the author's domain.** (a) Held-out seeds 11 (10⁵) and 3 (3×10⁴), flown by
   d31c/404b but not this author: digest-equal, cuts inside the band. (b) N=6×10⁵ seed 7, 2× the
   author's max: digest-equal, cut 8.30 µs/B (24.4% of the 35.98 pass), rail 48.0→38.5, peak RSS
   1.37 GB — no cache cliff; the per-body-redundancy mechanism extends. (c) The dossier's own
   admitted gap — identity after flight: `ladder_digest` (main's own instrument) flown under both
   arms, all 13 scripted cases (coast, forward-L8/L10 burns, 120-key mashing, coast through the
   first-kick wave, belt crossings) digest-identical at canonical cuts, each already asserted
   across 4 schedules. In-flight `decide`→`plan_clock` with thrust is covered; exactness is not
   tick-0-only.
5. **Code.** `Binding::readout` (bind.rs:160) reads only the binding's own fields; between the
   three `plan_clock` reads only `rec.ext` is written (`ext::constants` takes `&Ctx`;
   `project_at` writes `rec.ext`) — the shared value is provably each OFF read's value, and the
   OFF path is a transparent refactor. Suite with the patch: **77 passed, 0 failed, 3 ignored**
   (`--lib --bins --tests`; the author's `tests.txt` shows only the last binary's 5 — a `tail -3`
   artifact, the green claim is accurate). The disclosed Linux break (`examples/nladder.rs`'s
   `proc_pid_rusage`) is real and pre-existing.
6. **Novelty.** d31c's decomposition named this exact rung ("one readout serves `plan_clock`'s
   two `readout` calls"); no earlier run measures or lands it. A new lever, not a repetition.
7. **Goal fit.** Board #1 (bodies in the flyable engine; the birth pass is 404b's 76–78% of the
   rail and ~6 of ~8 M1-core-hours of a 10⁹ fill). PRINCIPLES #1: "The cheapest compute is
   compute not done. Delete before optimizing." Exactness untouched — integers decided (digests),
   honouring #2. Composes with d31c's shared-planets readout (disjoint terms, as the dossier
   argues).
8. **Why silver, not gold.** The letter wants 10×, a deleted component, or a killed premise;
   this is a ~1.2× rail cut (20% of one pass) — a named incremental rung, verified end to end,
   but the lever cannot reach the gold axis alone. Not lead: everything reproduced bit-exactly,
   the predictions held inside and outside the flown domain, and the run's self-named gap closed
   clean. The record defect (doubled patch) costs the runner its one-command regen but is a
   container bug, not fabrication: the content applies and regenerates once de-duplicated.

**The experiment that would make it gold.** Compose the deletions into the plane's default birth
path — `ES_ONE_READ=1` ∧ d31c's shared planets readout ∧ the Hill/cbrt block (d31c's remaining
28%) — priced as one adoption against the 404b rail with `ladder_digest` identity as the
certificate. The decomposition already names a ~15 µs/B floor for the pass; a composed default
that lands near it and breaks the rail by the multiplication is the integrator-scale step this
rung feeds.

**What the author missed.**
- The doubled `patch.diff`: the fix pass fixed root discovery but ran on a tree that already
  carried the patch, so `git apply --check` failing was never distinguished from "already
  applied". regen.sh's guard cannot tell the two apart; a clean-tree regen (this check) fails.
- Per-config single flights (rep 2 only at 10⁴ s1): the dossier's per-config means are mostly
  n=1; my re-flight supplies the second sample, and the central value agrees, but the author
  could not have known the spread (2–11 µs/B) their box class produces under load.
- The identity certificate was one `ladder_digest` invocation away the whole time — main already
  ships the instrument, and it passes; "not flown: re-plans in flight" was stronger than the
  truth needed to be.
