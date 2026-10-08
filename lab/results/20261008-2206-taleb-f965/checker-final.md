Working...
Check complete. `lab/results/20261008-2206-taleb-f965/check.md` written; nothing else in the run folder touched; tree restored to pristine.

**Grade: silver.**

What I did and found:

**Reproduction** — clean tree at a838a28, applied `work/patch.diff`, built offline (4.3 s), ran the binary (94 s, exit 0): all 35 JSON lines and the 80-line miss dump match the author's `coorb-final.jsonl` / `coorb-miss-final.txt` field-for-field (excluding `ms`). Tuning path is auditable and `predictions.md` (22:12:55) precedes every output file (first at 22:17:23).

**The kills stand** — global phase-rank trigger catastrophically misses cross-population encounters; static rank-4 needs the one-orbit refresh cadence; family gates fail when internal spread ε≫ρ.

**My four adversarial scenes** (fresh seeds, my outputs in /tmp):
- **A1** (10× a-spread fleet): cadence repair holds, 0 missed — the repair generalizes.
- **A2** (wedge at ρ=1e-5): gate misses shrink to 1/25 but its cost *grows* 5.8× over the cone — opposite of the dossier's ρ-direction claim.
- **A3** (eight crossing fleets): gate sound but 6.3× the cone's evals.
- **A4** (fleet × tight cold belt): **gate misses 3/130 — the ε≫ρ hole is not wedge-specific** — and costs 620 M evals vs the cone's 15 M (40×).

**Why not gold**: P4 failed on held-out wedges (author-acknowledged), plus three evidence sentences the log contradicts: the "70× fewer evals" repair claim (measured 1.4× — 70× only matches the *dead static* rank's evals), the headline "66–94%" range (table shows 34–87%), and "P5 held" (S2/S8 hits/encounter are 908/1172, an order above the ~10² prediction). The miss-count table itself is fully regenerable and honest; the one-gold experiment is the author's own named fix (member-extremal arcs / ρ-tight families, then the 10⁶-fleet pair count at game ρ).
