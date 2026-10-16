Working...
Check complete. **Grade: silver** — written to `lab/results/20261016-0117-library-cfe5/check.md`.

**What I did:**

- **Reproduced** from a clean tree at the base commit: applied `work/probe.patch` myself, rebuilt, re-flew the full 8-arm grid. Every digest bit-identical to the runner's regen and across both hoist arms; pass 33.7–33.9 µs/body, secondaries 30.2–30.5%, hoist-on 22.9–23.6, `sec_calls` = n+28, 7 memo keys. All dossier numbers regenerate.
- **Predictions timeline verified**: `predictions.md` (01:22:28) precedes the flights (author-final 01:29:36). Prediction 1 failed as reported (secondaries is 30%, not >50%) — the honest failure is what bars gold.
- **Three adversarial cases beyond the author's domain**, all holding: held-out seed 3 (30.2–30.3%), N=3×10⁵ flat (30.4%, digest-identical, RSS 688 MB), and N=10³ where the share dips to 26.7% — "30%" is honest for 10⁴–3×10⁵, not a ladder constant.
- **Mechanism code-verified**: `secondaries` (ctx.rs:79) runs once per body at birth (open/project paths); the memo key is exact; the digest hashes plans, clock constants and carries, so identity is a real check, not a tautology. The second reread path (`ext::constants`→`source`, ext.rs:133) exists but is untimed — the dossier admits it.
- **Novelty confirmed**: the standing nladder page's open direction #1 is exactly this question; no prior run flew a shared-state hoist (the kick-memo and ES_LAZY_ALL are different mechanisms).
- **Lens verified**: all five library quotes present verbatim in `work/library.json` with correct authors.
- **Page corrected in place**: the "~17 µs remainder holds another planet-reread path" overstatement softened to code-verified-but-untimed, and a checker bracket appended per the page convention.

Tree restored clean; nothing outside the run folder touched. The one experiment to gold: wire the shared "planets at t" readout across both read paths as a real change, fly digest-identical at 10⁵, and re-price (predicted ≲13 µs/body).
