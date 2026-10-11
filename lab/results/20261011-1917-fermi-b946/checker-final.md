Working...
Check complete — `check.md` written to `lab/results/20261011-1917-fermi-b946/`, nothing else touched.

**Grade: gold.**

**Reproduction:** patch empty, so from the clean tree — all three `steady` rows bit-for-bit (414/1738/40 hits, every deterministic counter identical), `budget.py` output identical, all cited constants traced to frozen evidence (29 µs = H0210, 32.5/114× = H0190, 0.126 bits = components-98bc, 16 B tube = law.md L12).

**Adversarial cases (5, all held):** different seed truth-checked 0.0184 (method = truth 921/921, missed 0, three seeds agree within ±15%); ρ=1e-2 upward exponent 1.03; n=10000 rate 0.1954 vs 0.207 linear; σ_e=1e-3 rate 0.0024 — quantitatively confirming the author's own P1 post-mortem mechanism; and an un-amortized discovery worst case of 1.42 cores at 100× rtf from the run's own measured constants, which makes the compute-clears verdict independent of the unmeasured amortized regime.

**Predictions:** file times consistent with pre-registration (predictions 19:22:32, all steady evidence later); P2/P3 held; P1's 15× miss was pre-committed as reportable (P7), reported loudly, and nothing downstream cites the predicted value — the miss itself proves the band wasn't tuned.

**Why gold:** it corrects ranked bottleneck 3's premise (compute at belt scale is 175× under *today*, no levers; the 190-core figure is the all-LEO bound), delivers HANDOFF's explicitly-open measurement ("H_live… not measured yet": 2.65 bits/body/orbit, recompile ~1.5 orbits), and installs capacity as the binding term with numbers. Adoption is a re-rank, no code. Caveats recorded in check.md: the 128-bit-per-scar model is assumed (cadence inherits it, verdict doesn't), and the LEO claim composes levers measured in other regimes — both flagged by the author.
