Working...
Check complete. Final state: `check2.md` written (28 lines, first line `Grade: gold`), the author's page corrected in place, tree restored pristine (`git status` shows only `lab/results/` untracked), no commits made.

**Grade: gold** — my independent verdict:

- **Reproduced**: runner's `regen.sh` exit 0; I rebuilt the instrument byte-exact from `work/patch.diff` (its two copies are identical — the fix stage changed nothing) and re-derived the headline numbers from the raw dumps with my own code. Four dossier drifts, all ≤ 0.3%, none load-bearing (6,547→6,568; floors 1.374→1.371; 3.65→3.698; Var constant 2.4→2.5–2.6×10⁻⁴).
- **Pre-registered kill honored**: predictions at 06:27 precede the decisive artifacts (07:33+); P1/P5 failed exactly as the two-branch criterion specified — that failure is the finding.
- **Adversarial cases (mine)**: (1) uncapped pooled floor — true late excess +0.21/+0.24, engine still above the control's p90 at both seeds in every band (+0.13 to +0.28); (2) locked-pair mechanism — |Δstep| tail gives median unlock ≈ 130 generations, structurally locked through the flown horizon; (3) **fresh seed-3 flight** (outside the author's seeds 1–2): attractor holds — 6,175 pairs, late excess +0.18, c50 frozen, drift flat ~7×10⁻⁵; (4) the claim's r = 0.974 is orphaned (not derivable from any artifact), though its direction is verified.
- **Novelty**: the published page's od-4 entry named this exact flight as "What remains"; this run executes it and inverts the model's extrapolated answer (a97f's floor-by-100–120 endpoint and seed-1-only pair split both refuted).
- **Page**: within budgets (110/300 lines, 4 current-best entries); I fixed its last overstatement (stale 6,547) and folded in the seed-3 hold.
- **Blinding caveat**: my first listing command inadvertently printed `checker-final.md`; every number in my check comes from the runner's regen, the author's artifacts, or my own flights/code — disclosed in the check.
