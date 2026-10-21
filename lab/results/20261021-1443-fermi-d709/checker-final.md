Working...
Check complete. **Grade: silver** — written to `lab/results/20261021-1443-fermi-d709/check.md`, with the tree restored to its shipped state.

**Verdict basis:**

- **Reproduced.** The runner's regen (exit 0) and my own flights from `work/patch.diff` all land in the dossier's bands: boundary item 8.65–9.93 µs x86, kick 50.1–56.2 µs, row 29.1–38.1 cores shipped / 5.9–7.7 after split8. Arithmetic re-derived by hand.
- **Instrument sound.** `plan.first().what` classifies exactly the item `process` dispatches (step.rs:830–839); the timed window is `resolve_body` only, identical to the shipped `cost_ns` window; one Boundary + one Kick per clock interval (step.rs:717–718) makes rate_b/k ≈ 1 the law. Unclassified ship items <0.1% (≈ opens).
- **Adversarial.** N=2×10⁵ (outside the author's range): every law extends (8.83 µs, ratio 0.163, row 29.0). Seed 3: in-band. N=3×10³, below the domain: a real regime edge — items cost ~1.5–2× more, rate_b/k 0.87 — but the row only *grows* there; nothing shrinks it toward the 10-core kill bar.
- **Predictions** pre-registered (14:51 < flights 15:00) and held; the one band miss (kick control above 40–50) was disclosed with the correct load-independent ratio cross-check.
- **Silver, not gold:** it prices and re-ranks (+15–19% on the stream row, 2× on the closure bar by arithmetic), but the deletion itself — 15d7's od 2 build, the row going to ~0 — is one measured experiment away. That experiment is named in the check.
- **Page:** faithful and within budgets; one overstatement corrected in place ("spends the 4-core budget" → "is itself the size of the 4-core budget", since the M1-anchored band 3.5–4.5 straddles 4). Author's misses recorded: the fabricated 5.7 low end of the headline band, the unmeasured "locals fire faster" mechanism, and the unexplored low-N regime edge.
