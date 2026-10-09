Working...
**Grade: silver** — written to `lab/results/20261009-1345-scout-9c12/check.md`, nothing else touched in the run folder.

What I did and found:

- **Reproduction:** ran a clean copy of `probe.py` — all eight configurations match the stored outputs and the dossier table bit-for-bit (base 0 births/838 dusted; q=1e-9 → 719; crossers 10,373 @ exponent 0.0716; fleet 172,875; 26 s wall). Deterministic seeds confirmed.
- **Predictions:** file timestamps show `predictions.md` (13:57) precedes all outputs (14:00+). P1/P3/P4 held; P2 missed ~300× on its bracket, P5 3.5–5× — both honestly reported, and the miss (Malthusian joint rate vs single-channel R₀) is itself the finding.
- **My attacks:** (1) 20-seed sweep shows "0 births in base" is a Poisson zero — true rate ≈ 0.013/orbit (confirmed steady at T=5000), so the dossier's "the base belt's rate is 0, so it never saturates" is falsified; base saturates too at 1e10 yr, which *strengthens* the reabsorption thesis. (2) Crosser exponent robust across 5 seeds (0.063–0.076). (3) ε₀ ×10/×100 and q=1e-7 keep belt-scale boundedness — no hidden cliff.
- **Novelty/source:** no HISTORY/docs entry on the influence-series question; HANDOFF line 74 confirms the unowned risk; Hu & Shi arXiv:0911.2227 verified to exist.
- **Why not gold:** two quantitative predictions missed, a hand-calibrated toy (admitted order-of-magnitude at f ≫ 1), one falsified dossier line, and "bytes not compute" is true by construction (fixed Poisson rates), not measured. Gold path named: measure reabsorption (re-fit vs birth rate) on the real belt — b-h-live/B18b.

One integrity note for the integrator: the dossier's claim that the mid-run instrument fix is "in `work/`-visible history" is dead — `work/patch.diff` and `run.log` are both 0 bytes. Nothing rests on it (the final instrument reproduces everything), but the pointer overstates the record.
