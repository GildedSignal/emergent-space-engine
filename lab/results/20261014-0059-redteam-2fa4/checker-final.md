Working...
Check complete. **Grade: silver** — written to `lab/results/20261014-0059-redteam-2fa4/check.md`, with one correction to the author's proposed page.

**What I did:**

1. **Reproduced bit-identically** — applied `work/patch.diff` to the clean base tree (`33c83f1a`), ran `regen.sh` (< 10 s): every oracle.txt/seams.txt number matches. All three seams verified verbatim in shipped code (`view.rs:397/288/308/319`, `observe.rs:272`).

2. **Held-out predictions verified** — `predictions.md` predates the dossier; all four held. The "no gate judges a seen value" claim checked directly: no r6 file exists, B7 judges rates only, no view example touches `shift`.

3. **Four adversarial cases beyond the author's sweep** — emitter β 0.999, observer 0.999, 10× emitter distance, 5× horizon: exact path still float noise (≤ 1.4×10⁻⁹, growing with closing speed exactly as the author's lens note predicted).

4. **Engine-level S1 confirmation the author didn't do** — built a live fast fleet (`plane_with` + `scenes::battle` at speed_div 8), inverted `Seen.shift` through the view's own outputs: the engine's member rate equals the Newtonian line to **5.6×10⁻¹⁶**. The seam is in shipped output, not just on paper. (First probe attempt had my own inversion bug — transpose of the rate formula — found and fixed before concluding.)

5. **Novelty confirmed** — the published view page's Domain line names this exact hole; nothing in HISTORY measures `Seen` values.

**Why silver, not gold:** the premise-wrong lives on a dormant branch (the plane flies 2⁻¹⁵c → 4.7×10⁻¹⁰ error), no compute gain or deletion, and the fix + r6 `Seen`-value criterion — the named gold experiment — is unrun (my probe got it 80% of the way: scene built, rows judged, line confirmed).

**Page correction:** the author's proposed `wiki/view.md` Domain line still listed "moving observers, the seen/Doppler instruments" as "not measured anywhere," contradicting the run's own result — scoped it to the stream class. Tree left clean at base.
