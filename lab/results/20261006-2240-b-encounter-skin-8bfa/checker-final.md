Working...
Check complete. **Grade: silver** — written to `lab/results/20261006-2240-b-encounter-skin-8bfa/check.md`; tree restored to as-found.

**Reproduced in a clean tree** (patch applied, deterministic counters bit-for-bit): 0 missed / 0 false on belt ε=1e-8/1e-6/1e-4 (s4 and s16), ring 1e-4, fleet 1e-6; setups/kick 142.3→17.1 (8.3×) at the plane's kick size; 7 tests pass; `verify a/b/c` identical to both stored baselines.

**Key findings:**
- **The disputed case regenerates as 0/0 of 73.** The author's own stored `work/belt1e-4.out` and `results.jsonl` say `"missed":1`, and its `fresh_finds`-only diag is impossible from the shipped bin (which prints `at_miss`/`lib` first) — a stale pre-final binary. The dossier's 54.2 setups number appears in no stored raw. The shipped code reproduces the headline, but the record contradicts it on that one case.
- **Falsifiability holds:** terms 3b+6 compiled out → `exact_at_kick_eps_1e4` fails; restored → passes.
- **My adversarial cases all held:** fresh seeds (0/0 of 75 and 74), κ=1.0 (0/0 of 66, 3.4×), ε=1e-2 beyond the named range (0/0 of 67; economics collapse to 1.13× as designed), ring 1e-6 (0/0 of 817).
- **Why not gold:** at the plane's kick size the 8.3× is the *setups counter*; total evals/kick rise 1.5× (4468 vs 2921 — undisclosed at 1e-6) and wall gains ~1.2–1.6×. Skin-mode setups cost ~12× more evals each (padded arcs + 100·TAU horizon queries), so the deferral currently converts setup into check work at a loss on the belt. The ring shows it's churn-specific (evals drop 1.44× there). Gold experiment: measure total work and p99 on the plane's own kick pattern / N=10⁴ belt, and regenerate the stale raw in the same run.
