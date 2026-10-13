Working...
Check complete. **Grade: silver** — written to `lab/results/20261013-1428-components-2368/check.md`.

**What I did:**
- Applied `work/patch.diff` myself on the restored pristine tree (the harness had saved the diff and reverted; the runner's regen numbers were already in `regen.log`).
- **Reproduced every claim**: primitive 2.97–2.99× (14.1 vs 42 ns/cos), compile −11 to −14% across arms with digest `b5ef99aabce2f641` identical everywhere, kick resolve 33.7→29.0 µs, 71/71 tests over 10 binaries.
- **Three adversarial cases, all outside the author's tested range**: (1) full-i128-domain fuzz of `cos4` vs `cos` — 0 mismatches over 3M random + 4,011 structured edges (the author only fuzzed [0, π]; identity is actually domain-unbounded); (2) compile digest on a wider grid (p to 2²¹, e to 0.99, non-power-of-two scales) — identical digest and refusal census across arms; (3) three held-out plane seeds/fleet sizes — digests bit-identical pristine vs patched.
- **Novelty**: the published `lab/wiki/kick-jet.md` names exactly this as "(untested)"; HISTORY has no prior entry. Page additions are faithful — no correction needed.
- Restored the tree to how I found it (pristine, only `lab/results/` untracked); scratch examples removed.

**Why silver, not gold**: fully reproduced and predictions genuinely held out, but a ~1.1× compile cut confirms the wiki's hypothesis rather than refuting a premise, deletes no component, and moves no bottleneck 10×. The gold-making experiment is named in the check: one build stacking 9384's isqrt + this `cos4` + interleaved division/isqrt chains, measured against b063's information floor — landing at the floor refutes the "primitive headroom" premise; not landing it kills the lever family in favour of panel count. Either way decisive.

**Missed by the author**: full-range identity was free to claim, held-out seeds cost seconds and all hold, the p99 tail (the number the integrator needs) is unmeasured, and the patch accidentally deletes `panels`' doc comment plus widens `num`/`tables` visibility for the bench.
