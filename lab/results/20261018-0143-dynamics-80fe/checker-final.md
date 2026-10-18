Working...
Check complete. `lab/results/20261018-0143-dynamics-80fe/check.md` written; the proposed wiki page needed no corrections (checked line-by-line against the evidence); the repo tree is restored to its pre-check state and nothing else in the run folder was touched.

**Grade: silver.**

**Reproduced** (clean tree, `work/fix.diff` applied, own runs, ~15 min total):
- Truth arms content-identical at both μ and both rtols (144/144 rows each); `parity.txt`/`burst.txt` regenerate **line-for-line identical** from my data.
- μ=1e-3 plane 512 P: my 144 rows content-identical to the author's, dead set exactly e846's 47, max |Δepoch| = 0.0000 P (P6 holds on a third machine).
- μ=1e-2 burst: 8/8 same ICs, epochs to 0.014 P; both cost walls reproduce (16 P unfinished at 120 s/2 workers; 64 P → 2 rows at 120 s/4 workers, the finished rows carrying normal ~220–240 kicks/P loads — a tail, not a rate shift).
- All full-horizon μ=1e-2 headline numbers (32/39/7, hazard ratio 16.9, 0.0019/syn, 22%) recompute exactly from the raw JSONL.

**Why not gold** — two one-run gaps:
1. The runner's regen exited 1 because `work/patch.diff` is `work/fix.diff` concatenated with itself; `git apply` rejects it on any clean tree. The exact "shipped code cannot regenerate" defect class the taste log records.
2. The certificate's negative control (a deliberately skipping law must fail it) is unrun — the author names it themselves.

**Adversarial findings beyond the author's domain**: at held-out μ = 3.16e-3 the rate is 0.0060/syn (fall is monotone 1e-3→1e-2), but at μ = 1e-4 there are **zero** entries in 512 P (closest approach 4.5 Rp, 0 gave-ups) — the rate curve is non-monotone with a peak near 1e-3, strengthening the "no single-μ rate law" conclusion. The 4× fall also survives proper at-risk exposure censoring (0.0097 → 0.0024/syn). Recorded in check.md along with the "1389 syn exposure" misprint (~16,705 syn actual; rate correct).
