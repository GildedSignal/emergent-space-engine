Working...
Check complete. Summary of what I did and found:

**Verdict: silver** (`check.md` written).

**Reproduced** — applied `work/patch.diff` to a clean tree, rebuilt, reran all four scenes: digests and every per-body census array bit-identical to the saved files; all dossier tables match. The load-bearing instrument claim (digest-neutrality, probe off = probe on) verified on two scenes.

**Adversarial** (three, one outside the author's range):
- seed 11 m48 30 s: kill criterion still doesn't fire, but promoted rank ρ sits *below* the Poisson null at 30 s windows — the dossier's Claim line quietly drops tune's 0.55-vs-0.78.
- m1200 request: the bench clamps `--members` to [4, 400], so it reproduced m400's digest exactly — 428 bodies is the shipped ceiling, not a chosen domain. The rtf 300 point (16,500 game-s) agrees with all claims.
- 55 s on the tune seed: everything extends; top-1 %-of-frames reaches 26 %, worse than stated.

**Why not gold**: the prediction record is mixed (P3 falsified as written — the refinement is the finding; P1/P2/P5 half-held), and three dossier numbers aren't regenerable from the given commands, two contradicted by the author's own `analysis.json` (decile share "55–70 %" — only ho1; "82–83 % zero-frames at m48" — ho2 is 0 %). Also found an undisclosed instrument jitter: `per_frame_events` shuffles across ~3 early frames run-to-run (totals conserved; every derived statistic identical across 5 runs, so no reported number moves).

**Page corrected in place** (`wiki/nladder.md`): window-qualified rank claim, 47–64 % death range, sign-flagged age correlation, 0–86 % zero-frames, the members clamp, and the rtf 300 agreement.

**Gold path named**: the death-vs-exposure sweep (rtf 1/10/30/100/300 at fixed seed — ho3's 0 %-death is its unexploited first point) plus quarter-window rank stability, with every headline number emitted by the script.
