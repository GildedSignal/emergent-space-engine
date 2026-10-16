# Gravity v1 draft: red-team and premise probe 1 (29 September 2026)

Byte-identical copies from `artifacts/runs/gravity-v1-freeze/` and GLM's scratch folder `/private/tmp/glm-scratch/gv1/` (the probe's Python scripts, standard library only). Both runs were GLM 5.3 (omp, sandboxed), against the H0195 draft of `docs/gravity-law.md`.

- `redteam-prompt.md`, `redteam-out.md`: the red-team of the draft contract.
- `probe-prompt.md`, `probe-out.md`, `probe-scripts/`: the float premise probe. Verdict: three of four kill criteria pass; the energy-growth criterion kills the per-body step rule Δ = η·r^{3/2}(current state), while a fixed-Δ control stays flat.
- probe2/: the float re-probe of cell-owned steps (C1 shell-constant, C2 symmetrized, C3 fixed), GLM, 29 September; prompt, final message, scripts and raw results. prior-art-*.md: the GLM prior-art scout on cell-owned time steps.
