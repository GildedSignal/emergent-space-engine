Working...
Check complete. Verdict written to `lab/results/20261007-0341-autoresearch-9dc2/check.md`; tree left pristine (only `lab/results/` untracked, nothing else touched).

**Grade: lead** — the author's own sought grade, and the evidence agrees.

What I verified:
- **Reproduction (clean tree, both builds < 60 s):** baseline median 82.6–84.2 µs, digests `14d14cd4`/`57c91487` bit-identical to the dossier; patched build 90.7–91.2 µs, digests unchanged, panel/cut counts exact (776,786 / 774,516), quad 0.577–0.587 µs/panel. The 0% gain reproduces; P1's predicted 20–35% is far outside noise.
- **Predictions provenance:** `predictions.md` (04:04:21) predates the round-1 run (04:06:32 inside the saved JSON's `machine_before`). The failed P1 is reported as the headline, not buried.
- **Adversarial:** unseen seed-3 workload — digests bit-identical patched vs pristine, 0% transfers; 45 tests pass with `hdiv`; the `hdiv` guard is mathematically exact and `div_word`'s contract is genuinely tested; the EDGE-band-walk mechanism checks out in source (70.7 panels per bound-orbit compile, band count = 16·log₂((1+e)/(1−e))).
- **Novelty:** no prior HISTORY/docs entry attributes compile cost to panel count or tests `fast_quad`'s arithmetic width; the bench itself is unmodified since the 5 October memo work.

Two things worth the integrator's eye:
1. **Attribution overstated in the dossier's phrasing:** quad is **59% of compile**, not 75% (75% is quad's share of quad+cut only); "97% rebind" is avg-rebind/median-kick (94% measured). Panels+cuts ≈ 79% of compile survives, so the conclusion stands.
2. **The real takeable output is the lead, not the falsification:** ~70 panels per bound-orbit compile emitted by the EDGE band walk is the next rung's target — but "grows with eccentricity" was never measured, and a free Fermi bound (3.1M divisions ≈ 124 ms worst case) could have killed the hypothesis before the 45 s build. Both are named in check.md as the path forward.
