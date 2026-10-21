Working...
Check complete. **Grade: silver** — written to `check.md`, with the author's wiki page corrected in place.

**What I did:**

1. **Reproduction (exact).** Ran `bash regen.sh` in a clean directory: 2m19s, 11/11 controls PASS, and every JSON plus `analysis.txt` came out **byte-identical** to the stored files. Verified `ref-451f-flyby.json` is bit-identical to 451f's published branch data — the repro reference is honest.

2. **Predictions.** The decisive pre-registered fork (addendum A vs C) held exactly as registered — the in-plane excess is IC convention. But addendum B is reported "HELD" while the run's own data contradicts it (floor + linear, not ξ²), and `conv.err` predates `predictions.md`, so #2 may be post-dicted.

3. **Four adversarial probes** (three outside the author's range):
   - ξ = 1e-6/1e-5: no floor — linearity holds below the grid.
   - rp = 6M: converged, but **M/r bends** (exact rad 5.8× vs 3× predicted) and truncated along breaks rp-independence (96 vs 178) — the claims are domain-limited to [18,100]M.
   - β = 0.99: truncated γ²/γ⁴ scalings extend; exact rad/z rise ×2.3, beyond "weak".
   - ξ = 0.1/0.3: exact z stays linear to ±4% at 0.3 — the law's reach was understated.

4. **The key judgement:** the exact-IC channel's τ-growth is *also exactly linear* (0.255/0.503/0.751) — the same fingerprint the author used to convict the truncated channel as drift — so headlining k_exact as "the physical channel" is not earned; their own od 1 (closed-form Marck/Manasse–Misner force) settles it. Plus three smaller overstates vs their own tables (spread ≤7% vs 9.2%; "92–99.5% of the in-plane channel" vs π/8 at 57%; "2.4–5.7" vs 1.96).

5. **Page corrected in place** (still within budgets: 14-line current best, 62-line page): true spreads, the π/8 exception, the 2.0–5.7 range, the swept domain with the 6M/β0.99 bends, and the open mechanism. Novel on the topic (first run at this level after 4c79's linear and 451f's artifact); goal fit solid (board's certificate row, PRINCIPLES 33, P2).

Silver, not gold: the misreported prediction and the unearned "physical" headline — one experiment away (od 1, the closed-form second-order Fermi force; the certificate sentence itself is mechanism-independent).
