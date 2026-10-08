Working...
Check complete. `check.md` written to the run folder; tree restored (patch reversed, only untracked `lab/results/`).

**Grade: silver.**

What I did and found:

- **Reproduced** both paths: clean-tree shipped `--kick-bench` gives 97.29 µs median / digest `13cfe88b…` / 682 samples; the patched `--jet-bench` matches every deterministic counter bit-identically (663 cycles, 653 shape-key changes, 45 bodies, 0 cell changes) and every timing within 1% (compile 62.1 µs = 64.5%, rebind 78.7%, forces 8.8%, from_shape 0.465 µs). Verified in source that `Orbit::compile` is memo-free (no cache-hit artifact) and that `bind` is fit-contains-compile + residual, so the decomposition is faithful.
- **Timeline holds**: predictions.md (02:42:48) precedes the decisive JSONs (02:51:12) with a pre-registered kill criterion; 5/6 predictions held, the failure reported honestly and turned into the sharpest result.
- **Adversarial**: seeds 3/7 and 30 s windows keep compile at 51–65% and rebind ≥71% (kill criterion nowhere near); trivial shape reuse stays dead at 0.8–1.5%. One correction: the "0 cell changes" is a 10 s-window artifact — at 30 s the rate is ~0.07–0.09%/kick (one change per ~1100–1500 kicks), which still supports the jet's re-anchor cadence. The 4.4× ceiling recomputes to 3.3–4.4× across scenes. `--level 15` is a dead axis (bit-identical digest — the script never burns).
- **Why not gold**: 3.3–4.4× is a priced ceiling, not a built lever; the one experiment to gold is the minimal offset-jet build measured end-to-end (the author names it themselves).
- **Flagged**: the patch disables the shipped `--kick-bench` (module replaced rather than added alongside, 5 build warnings), contradicting the dossier's "visibility and one accessor only" parenthetical — universe behaviour itself is provably unchanged (matching digests).
