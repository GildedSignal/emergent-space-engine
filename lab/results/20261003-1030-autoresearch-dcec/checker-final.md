Working...
Check complete. `lab/results/20261003-1030-autoresearch-dcec/check.md` written; nothing else in the run folder or the repo touched (tree restored to HEAD, examples removed, no git commit/push).

**Grade: silver.** Summary of what I did and found:

**Reproduced** — clean tree, author's patch (exactly +198/−31, one file, applies clean), own baseline binary for paired comparison:
- Tuning: digests `9c7790dc…`/`b6dd6f65…`, predicates 23,458,426 exact; 335→86 ns = **3.9×** paired (author 5.3×, same order; shared cloud box).
- Held-out ×5: all digests/counters identical to my baseline; speedups 3.9/1.8/2.7/4.2/3.0×.
- Guards: 19/19 lattice tests, event crate green, `xtask lattice-check` EQUAL ×3 vs the independent integer reference.
- Proved bit-identity structurally: `law::hit` is exactly invariant under (d,w)→(−d,−w), so the single-visit walk tests the identical pair set.

**Attacked** — six adversarial cases, all digest-identical: hashed fallback beyond cap (−5%, matching the author's disclosure), fill=5 degenerate dense (1.0e9 predicates, 1.75×), 500-chronon drift, n=1/2, and a custom 6667:1 aspect-ratio world with 118k events (4.3×) — the dossier's named risk does not materialize.

**The catch** — the cold-sparse (seed 11) evidence rows in all three files were run at **steps=60, not the declared 100**: their counters are arithmetically impossible at ×100 (ops 36M < the 40M floor), and `… 11 60` reproduces digest `263ad83b…` exactly. The claim survives at the true config (I ran it: identical, 2.7×), but the dossier's reproduce command cannot reproduce those rows, undisclosed — per this lab's precedent, that caps at silver. Also: the ranking prediction still fails post-fix, and the gain lands on the reference/judge (`docs/engine.md`: the chronon "survives only as a test judge"), not the board's billion-body path. The named gold experiment: port the representation to the event mode's cell rebuild, or measure the judge path end-to-end.
