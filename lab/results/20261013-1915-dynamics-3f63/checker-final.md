Working...
Check complete — **Grade: silver**, written to `lab/results/20261013-1915-dynamics-3f63/check.md`.

**What I did:**
- **Reproduced**: applied `work/patch.diff` myself on the clean tree at 4503420; pilot and repeat arms bit-identical to the runner's regen and the dossier (determinism confirmed across three invocations). All derived numbers (κ table, plateau 2.852±0.071, fit 2.72+1.71·(r/R−1), ×8.2 Λ span, held-out verdicts, 8574 cross-checks) trace to `analysis.py` and the logs; the Λ formula is grounded in shipped `thrust.rs` and the page's twice-checked ladder.
- **Attacked** with 8 arms of my own, all confirming the fitted curve — including two discriminators the author's held-out set lacked: **(1.004R, L7) ALIVE** where constant-κ said DEAD (L7 never swept; its boundary lands inside (1.002, 1.004)R), and **(2.6R, L0) DEAD** where plateau-only κ said LIVE (the drift is real, not noise); plus a fresh 1.45R column, a 2³⁷ horizon extension (both borderline ALIVE arms stay alive), and coast controls at five new radii.
- **Novelty**: the page's open direction 2 named exactly this flight; no prior tangent/κ ruler in HISTORY.
- **Page**: faithful, no correction needed.

**Why silver, not gold**: no 10× board move (author concedes), the ruler is untested on the plane's own world (validated only through the D-row bracket), circular starts leave the Λ↔Ψ degeneracy unbroken, and the held-out discrimination rested on one arm. The gold-making experiment: fly the boundary arms on the plane's real scene — if κ holds, the HUD certificate adopts in one step. Author's misses noted: undisclosed L6 beyond the pre-registered levels 0–5, L1's 8.9% miss unreported, and the unread near-surface L7 death anatomy (r_last ≥ surface, death before first checkpoint).

Tree restored to as-found state; nothing else in the run folder touched.
