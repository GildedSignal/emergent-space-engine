Grade: gold

Abstract: The checker-named experiment is done and holds, total for the two gate-dark
mutants: `cargo test -p emergent-universe -p emergent-lattice` (23 binaries, 91 tests)
passes 91/0/3 — identical to baseline — under M-kick and M-prune, while the M-wrap
control dies in the lattice's own `hit_is_exact_past_the_i128_products` (teeth proven)
and restore equals baseline. The xtask suite (227 tests) adds no mutant-specific
failure; the two M-prune extras are the B10 timing gate, passing 7/7 serially.
`behave --law plane` fails on the clean tree on this box (M1-calibrated) — the one
instrument left to the integrator. Checker arms beyond the author's range (M-kick3
`>>(2L+3)`, M-prune margin `1<<2`) also pass 91/0/3, and the running readout test's
values are bit-identical under M-kick: the suites never observe the slip. Cost to
adopt: the parent's small `replay.rs` patch (corpus currency + exit 2) — now the only
automated line of defence, no longer a judgement call.

## Reasons

**Reproduction.** The runner's `regen.sh` exited 0 and its summary matches the
dossier's arm-1 table exactly (baseline 91/0/3; M-wrap 3 passed/1 failed at
`law.rs:711`, d [157,106] w [20,22] reach 32 scaled by 2^61; M-kick and M-prune
91/0/3; serial B10 control 7/0; restore 4/0/0; rlib fingerprints all distinct:
4f87…/a35a…/ebe2… — liveness). I re-verified the raw logs line by line: 23 binaries,
91 passed, 3 ignored = `clock.rs:154` (γ-clock), `motion.rs:229` (known chaos),
`t1_burn.rs:63` (frozen T1) — the dossier's identification is exact. The xtask arm's
227 = 206+7+14; M-prune's 204+9+14; the two extras are the B10 gate
(`["G5","B10"]` vs `["G5"]`, `behave/mod.rs:385`) — planted laws never enter
`universe.rs`, and the serial control passes 7/7 under M-prune (runner-reproduced).
`across_a_kick…` prints bit-identical values (1.0/3.0/1.0/24.4 quanta, identical kick
counts) in all four arms. The behave arm's clean-fail strings match (B12 "1 not
convered… median exponent inf", B13 worst 2.12e-2, B14 "60.0 s over the 60 s limit").

**Predictions.** `predictions.md` (mtime 1791953647) precedes every run log (first:
1791954484). P1 held (0.55, honest; the named risk — motion.rs — passed, and the
post-hoc mechanism is the right explanation, see below), P2 held (0.8), P3 held
exactly including the M-wrap control prediction, P4 resolved vacuously with its
substance confirmed. This is what held-out means.

**My attacks (three, two outside the author's range).** (1) M-kick3
(`len >> (2·level+3)`, an 8× shorter kick — the author tested only +1): full suite
**91/0/3**, zero FAILED lines, distinct rlib stamp — the darkness is the coverage
hole, not a knife-edge at +1. (2) M-prune2 (margin `1<<2`, absurd; suites never
tested it): **91/0/3**, distinct stamp. (3) Behavioral: the running readout test's
per-ship printed values are **bit-identical** under M-kick (only wall-clock differs)
— the suites never observe the mutated path at all, which is the strongest form of
"guarded nowhere". Source confirms the mechanism: `observe::partial` uses `k.len`
only as the window bound (`observe.rs:139`, Δv recomputed from the field at
`observe.rs:147`), `credit`'s shape uses `len` (`observe.rs:86`) and its test
(`motion.rs:229`) is `#[ignore]`d; the digest (`universe.rs:1121`) hashes the plan's
kick ticks and levels, never `b.kick`. Tree restored clean after my arms.

**Novelty.** The published page's open direction 4 named exactly this experiment
("the named next experiment", 20261014-0059-inversion-8e84); this run closes it.
No prior HISTORY entry covers the suites' reach over the dark mutants. Not a
repetition.

**Page.** `wiki/replay-gate.md` is faithful: every new line matches the logs; the
Refuted addition and the rewritten open directions (the credit-ramp test as M-kick's
real closure; behave-on-M1; main's xtask suite red on x86) are supported. No
correction needed. Not three golds on this topic (30da ungraded, 8e84 silver, this):
the page stays open.

**Goal fit.** PRINCIPLES: "a test that cannot fail is a control" — for M-kick and
M-prune every automated instrument on the merge path is now measured to be one, with
controls on both sides (M-wrap dies; restore equals baseline). The premise "the
shipped suites catch what the gate misses" is shown wrong, which makes the parent's
adoption (corpus currency + exit 2) a one-step, no-judgement patch.

## What the author missed

- **The behave arm was stronger than reported.** The four behave outputs are
  gate-line identical across baseline/mutants/restore (only `machine_state`
  timestamps and B14's 60.0→60.1 s differ): even where it runs, on this box,
  `behave --law plane` would not have bitten these mutants. Totality had one more
  leg than the dossier claims.
- **Wording:** "All numbers regenerate with regen.sh" overstates — regen.sh covers
  arm 1 and the serial control; arms 2–3 regenerate from `xtask.sh`/`behave.sh`
  (present and self-contained; I verified their logs rather than rerunning the
  ~25-minute xtask suite, whose distinctive claims are corroborated by four
  mutually consistent logs plus the runner-reproduced serial control).
- **`work/patch.diff` is the M-prune mutant itself** (a run.sh snapshot taken while
  a mutant was applied), not an author edit; applying it as a checker would start
  from a mutated tree. The tree is clean at base 8498d1c8 and regen.sh is
  self-contained — harmless here, worth knowing for the next second checker.
