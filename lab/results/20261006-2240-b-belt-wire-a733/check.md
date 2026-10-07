Grade: silver

**Abstract.** Claim reproduced end to end: the patch applies to pristine main (70f27a9); B18b goes FAIL ("belt_birth is not implemented") → PASS on all five frozen runs with the dossier's statistics bit-identical (chi2 2.80/4.5, serial 3.13/5, KS 0.56, birth 31 B, 32 B at 1e9, 11.4% scarred at 9.7 B); B18 FAIL unchanged; shipmem 5+2 and xtask 3+1 tests pass; two CLI invocations give identical bits. My adversarial probes pass: unseen seeds 424242, 777 at 2^20 and 555 at 2^23 all inside limits; restore fuzz refuses every mutation/truncation. wt/belt's frozen E[0]=1174440 vs judge threshold ≈1062976 confirms the claimed old-table bottom-tail kill (z −7.25). Silver, not gold, for two record defects (below); gain: the components-98bc program certified mergeable, one step to adopt.

**Reasons.**

1. **Reproduction (clean tree, patch applied by me).** Before, on main: `B18b FAIL belt: 1 of 1 findings fail: 2^20 seed 20261008: belt_birth is not implemented [0.00 s]`; `B18 FAIL memory: 0/12 ladder scenes … 12 not answered`. After: `B18b PASS belt: 5 runs, every criterion; worst: chi2 |z| 2.80 … birth 31 B for info 31 B … 11.4% are scarred, 9.7 B each (floor 54 bits) … [26.5 s]` — every number matches `gates-before-after.txt` except timing (26.5–29.1 s vs 16.9 s; 28 vs 17 ns per body at 2^20, 17 ns at 2^23; shared cloud machine, orders of magnitude agree). A second process invocation printed the identical statistics line. The frozen judge `xtask/src/behave/belt.rs` is untouched by the patch; no threshold moved.

2. **Adversarial cases (mine, beyond the frozen set).**
   - Seed 424242, 2^20, thorough, through `judge_findings`: PASS (worst conditional mean 2.39, serial 2.47).
   - Seed 777, 2^20: PASS (worst count 1.59, serial 2.63).
   - Seed 555, 2^23 — unseen size *and* seed, attacking the author's own named thin margin (bottom-e reach ~1.8×): PASS (worst count 1.86, KS 0.69 of critical, serial 3.03; reach findings passed).
   - Restore fuzz on a scarred store: all 2×len single-byte mutations, four truncations, trailing junk — every one refused or self-consistent, no panic.
   - Finding 1 verified from the frozen artifacts: `git show wt/belt:…/belt_quantiles.rs` has `E[0] = 1174440` (the dossier's exact number), dyadic octaves only at the survival end; the judge's EBottom threshold at 2^20 is ≈1062976, so X = 0 and z = −7.25. The committed gold program would have failed its own gate; the both-ends restructure is real, necessary work.

3. **Predictions.** `predictions.md` (23:10:38Z) precedes the decisive gate output (23:28:18Z) and the dossier (23:28:49Z); run.log is empty, so file order is the only witness, and it is consistent. All six predictions held (chi 2.80<3, serial 3.13<4, KS 0.56 vs "<0.5" — the 12% miss the author disclosed, still half the limit; 31≤32 B; 9.7≈10 B; B18 identical; no regression from the patch — I verified the last directly, see defect 2).

4. **Novelty.** H0214 froze B18b on 5 October with "no wired belt yet (Astra and Sol, after 9 October)"; wt/belt a2b777 is unmerged pending exactly this judgment. The wiring, the exact-op derivation of the table at birth, and the bottom-tail failure of the committed table are all new. Not a redo of any H entry.

5. **Goal fit.** Board item "fitting 10⁹ in 8 GB (crates/shipmem: population programs plus scars)": the population program goes from unmerged/umjudged to certified (31 B any n, ~9.7 B per rewrite, 1.10 GB of scars at 1e9), and the 28 KB frozen table is deleted as stored information. PRINCIPLES: "Store the generator, not the generated" — the store is parameters plus scars; the gate's own freeze wording ("a table derived from the spec is a working constant, not counted, and not stored") is honoured rather than weakened.

**Why silver, not gold — two record defects, both confirmed on my machine:**

1. **The held-out claim is overstated.** The dossier says predictions were "tuned only on a non-frozen seed at 2^20", but `predictions.md` itself discloses "one thorough judged 2^20 run at seed **20261008**" — and `RUNS[0] = { log2n: 20, seed: 20261008, thorough: true }`. Frozen run #1 was exercised pre-prediction (it also ships as the patch's unit test), and `predictions.md`'s own "the frozen seeds … are held out" is internally inconsistent. The disclosure was honest; the dossier's summary mislabels it. Runs 2–5 and both 2^23 sizes were genuinely unseen and passed.
2. **A workspace-evidence line the machine contradicts.** "cargo test --workspace --release — all pass except lattice-metal's fuzz_free_worlds" is not regenerable: on this machine 9 further xtask tests fail (events B12-echo, 5 handoff, 1 plane kick, 2 behave_cli). I ran all 9 on **pristine main: they fail identically** — the patch regresses nothing, but the quoted line is false. Most likely an aborted run read carelessly (lattice-metal fails first in build order and cargo's default fail-fast then skips xtask's suite).

Per this lab's own rule — a headline the log contradicts costs the grade (r3 v3, r4 v2 precedents) — gold waits on the record, not the physics.

**The one step to gold:** append the corrections (never rewrite): (a) frozen run #1, seed 20261008, was the disclosed pre-prediction run, held-out = runs 2–5; (b) replace the workspace line with the regenerable truth — "the patch regresses nothing; main itself currently fails 9 xtask tests (B12 echo, handoff ×5, plane kick, behave_cli ×2), reproduced identically on pristine main, plus lattice-metal's environmental fuzz failure" — with `cargo test --release --no-fail-fast -p xtask` quoted. The evidence itself (bit-identical B18b PASS, four unseen frozen runs, this checker's three unseen probes) already carries the gold bar: it deletes a component (the frozen table) and corrects a premise (the committed gold's table was not tail-safe), adoptable in one step.

**What the author missed.**
- The two record defects above; the patch's smoke test bakes frozen run #1's exact parameters in as a dev test — worth stating outright.
- Degenerate `Params` slip through `check()`: `p_bits`/`w_bits`/`t_bits` = 0 give `mix >> 64` (shift overflow — panic in debug, silently masked in release). Unreachable from the judged SPEC; a latent trap for engine callers. Reject 0 like `kind_bits`.
- The distinctness unit test checks only the (t_p, ω, kind) projection at both sizes; full-state distinctness rests on the judge's finding at the judged seeds.
- Birth-derivation cost (~1 ms) is asserted, never measured on record; cross-machine bit-exactness is argued, not tested (the author flagged the latter).
- Cost note for adoption: `Prog` loses `Copy` (the `Arc`-held table); shipmem hot paths now clone; the judged path avoids `Prog` entirely, and `Program::bytes()` now charges the table once per population — shipmem-internal, no external consumer touched.
