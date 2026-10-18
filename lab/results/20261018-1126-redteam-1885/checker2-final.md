Working...
Check complete. Verdict: **gold** — `lab/results/20261018-1126-redteam-1885/check2.md` written.

**What I did:**
- **Reproduced bit-exact**: `regen.sh` (3.6 s) regenerates every dossier number; `results.json` after regen is byte-identical to the author's. The L58/L59/L116 quotes are verbatim in the tree, original to the coherent-design commit `cd912a46`.
- **Verified the physics independently**: k = e^φ is exact for LOS approach, dφ/dβ = γ², and the closed forms (E[k⁴] = e^{4μ+8s²}, CV = √(e^{16s²}−1), log-word miss e^{8s²}, d ln k/dθ) all recomputed and matched.
- **Ran five adversarial arms** (one outside the author's range): γ 22.4 confirms s = γ²σ_β to the digit (σ_β 10⁻⁴ c → 14% error); receding mirrors approach; bounded uniform dispersion fails harder (72.5%); a two-squadron formation with zero internal dispersion still errs 41% with 2.37× square-wave flips; velocity-Gaussian dispersion is catastrophically worse (top-1% share 96–100%), making the author's table a lower bound. Nothing rescues the premise; the belt regime stays safe exactly as claimed.
- **Novelty confirmed**: no HISTORY/wiki entry measures the aggregate seen-flux readout; 2fa4's "no gate judges a seen value" is per-emitter and correctly extended; no seen-value rung exists.

**Two corrections made to the proposed page** (`wiki/representation-premises.md`): the closed-form tolerance ("≤4%" → CV/log-word exact, strobe 6–10%, coefficient 3.82s), and a checker2 block recording the one real domain limit I found — the observer arm assumes one aggregate per crowd; under per-pixel re-clipping its pure-angular error drops to 0.4–0.7%, though the LOS-dispersion fleet arms (the refutation's pillar) survive clipping.

Gold rationale: a design premise of record is shown wrong (principle 20's crushed tail made physical — 37% of seen flux on 1% of members), with pre-registered predictions (one honest, conservative miss), controls both sides, reproduction, and one-step adoption (doc amendment + freeze-ready criterion, no engine code).
