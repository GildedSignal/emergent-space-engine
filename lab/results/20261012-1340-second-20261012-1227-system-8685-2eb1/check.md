Grade: gold

**Abstract.** Claim: the named experiment succeeds — a discrete, orbit-anchored secular term (one midpoint kick per fixed mean-longitude segment, K per orbit, conjunction windows riding on top) removes tick-anchored aliasing at every segment length (Δė 84–134 MADs → 0.01–0.11; Jacobi 48–175× floor → 1.0×) and closes the belt ϖ̇ break (+64% → +2.5% at K=16, +0.5% at K=32): the averaged term need not be continuous. Everything reproduced bit-identically from the shipped source in a clean copy, including truths and the original-run lineage. Deployable rule: K ≥ 16 percent-level, K ≥ 4 kills the subharmonic, K = 2 forbidden; tick-anchored rejected at every length. Cost: one scheduling rule, no new component. My adversarial cells (K=3, K=5, W=2.5 at K=16/32, resonant p8/p16) confirm.

## Reproduction

Compiled from `window_clock.c` in a copied tree (no `patch.diff`, no repo edits). Twelve decisive belt cells (u64/u8, w0.5, seg4/8/16, seg8m/n/mn, p2/p4/p8/p16/p32 at 64 seeds), the w0.5p8 sweep cell, encounter u8 and w0.5 at 64 seeds, and the u2048 truth part (seeds 0–7): **all bit-identical** to `work/`. Lineage verified against the published branch (commit 77443410): `work/orig/` copies match the original run's committed CSVs, and truth seeds 0–15 of `belt-truth64.csv` are md5-identical to the original `belt-truth.csv`; the rerun u/w/seg8 cells' first 16 seeds match the originals row for row. `analyze.py` regenerates every dossier number I checked: the p-K ladder (rel% +33.0/+10.0/+2.49/+0.50 at K=4/8/16/32, Δė 0.11/0.06/0.03/0.01, Jacobi 1.0× everywhere), p2 (+91%, Δė 259, 3.6×), the ablations (seg8m 2.5×/−78%, seg8n 195×/+25%, seg8mn 90×/+21%), the W-sweep (+4.5/+6.3/+6.6/+0.9/+4.0%), truth convergence (0.37/0.50 MADs), floor 1.181e-3, and the encounter inversion (u8 2.43, w0.5 2.78, u16 0.60, w1.0 0.44, w0.25 6.08). The pure-grid control (`w0.01p8`) gives +2.0% at 15.1 k/orb as claimed.

## Predictions

`predictions.md` (13:56:03) predates the final code (13:56:44) and every decisive CSV (first at 13:59:01); only 1–2-seed machinery smokes precede it, as stated. PB2 (subharmonic gone at K ∈ {4,8,16,32}, K=2 fails exactly as mechanistically predicted), PB3 (ablation split: sampling owns Jacobi, re-origin/drop owns the rate; seg8mn still broken), PB4 (no cost win — u8 holds 0.04 MADs at 8 k/orb), PB5 (inversion reproduced exactly) all hold. PB1's letter failed at K=8 (+10.0%, not ≤2%) and is self-reported as the author's calibration miss, with the author's own kill criterion honored in substance: K=8 is demoted in the deployable rule (K ≥ 16), and closure is claimed only with the monotone 33→10→2.5→0.5% trend plus the W-sweep and pure-grid controls, not a single cell. The registered gold condition ("subharmonic gone at every length AND the ϖ̇ break closed") is met at K=16/32.

## Adversarial cases (mine)

1. **K=3 and K=5** (64 seeds, belt): K=3 gives +48.4% ϖ̇, Δė 4.65 MADs (above the 2-MAD falsification bar), Jacobi 1.04×; K=5 gives +23.4%/0.13/1.01×. This confirms the harmonic mechanism rather than weakening the rule: the alias at K=3 is the m=3 harmonic (weaker than K=2's m=2), and the K ≥ 4 boundary is real, not an artifact of the tested powers of two.
2. **Extreme window at high K** (W=2.5, 16 seeds): K=16 −3.6%, K=32 −3.5%, Jacobi 1.10×, Δė 0.50. Percent-level closure holds, but note the K=32 advantage of W=0.5 (+0.5%) does not carry to wide windows — the window–grid few-percent interaction the author flagged at K=8 saturates near 3.5% at W=2.5.
3. **Resonant scene under p-cadence** (the lens's own named blind spot, 16 seeds, vs the original's u2048 truth): w0.5p8 −2.1% ϖ̇ / Δė 0.13; w0.5p16 −0.6%/0.02 — no phase-lock pathology, clean where window-only is −45% and seg8 −72% (ė 45 MADs). The original's resonant kill stands for w-only; p-cadence is safe there too.

## Novelty

Direct lineage: this is the first checker's named gold experiment on run 20261012-1227 (silver), and the run says so. No prior orbit-anchored schedule is measured anywhere in HISTORY (H0204 averages-away-from-resonance, H0205 conjunction kicks, the original run's tick-anchor kill). New measured facts: discrete per-phase kicks carry the secular term (continuity not required — one of the two pre-declared decisive outcomes); the K threshold quantified; the seg failure decomposed by ablation into endpoint sampling (Jacobi) and re-origining/drop (rate); the window–grid interaction isolated by a pure-grid control.

## Goal fit

Board bullet 1 (fewer kicks per orbit / cadence; feeds q-cadence), as a component rule for motion-law v2, honestly scoped as structure rather than cost (PB4). Principle 14 ("no work for no reason, so no ticks") now measured on both sides: tick-anchored aliases at every length, orbit-anchored is clean. Principle 19 ("a fix signals the wrong representation"): keying the kick to orbital phase deletes the seg fix-family (endpoint weighting, re-origin, dropped gaps) at a stroke. Principle 4: K is chosen by the harmonic content of the averaged term, a number, not a category.

Adoptable in one step: the rule needs only mean longitude, which the scheduler already holds; no new component.

## What the author missed

- The K=3 boundary cell was one command away and would have sharpened the rule's justification from "K=2 is special" to "K must not alias the strongest surviving harmonic" (my run: +48%).
- The K-trend (and the +0.5% headline) is quoted at W=0.5 only; at W=2.5 the closure saturates at ~3.5% for K=16 and K=32 alike, so the rule's percent-level claim should carry the W-qualification the K=8 row already has.
- The rel% thresholds are calibrated on the same 64 seeds they are quoted from; the W-sweep (16 seeds) is the only quasi-held-out corroboration in the record (my W=2.5 cells add two more).
- Resonant p-cadence was left to the lens section; one cheap run would have retired the worry in the record rather than leaving it to the checker (it retires cleanly).
