Working...
Check complete. `check2.md` written; tree restored to HEAD (only untracked `lab/results/` remains).

**Grade: gold.**

**Reproduction** — `git apply work/patch.diff`, build, all four dossier commands: every field bit-for-bit identical to `work/seam-raw.jsonl` (seam cost 222/422/1122/3122; mixed-arc0.1 waste 94.3%, 25,985 cross setups vs 1,488 encounters; graded ladder medians 0/1/3/7/12; ring control max rank 4). `verify a`/`c` pass — the patch is additive, no regression.

**Predictions** — `predictions.md` predates the raw results by ~6 min; P1 and P3 held, P2's completeness half failed and is reported as failed with a diagnosis. My check of the crate's own `coorbital` scene corroborates the reinterpretation: cone tier complete (2093/2093) while the dead r8 window reference leaks 393/2093 — the gold's miss premise belongs to the window tier.

**Six adversarial probes** (local parameterization of seed/da/σ_e/alignment/belt σ_e, reverted after): two fresh seeds (waste 94.1/94.3%), ρ=1e-3 at 3× horizon (waste 96.1%, setups/encounter 25.2 vs ~29 predicted — the 1/ρ extrapolation direction holds), non-aligned swarm (rank med 11 vs 6 — alignment moves the coefficient), tight convoy da=1e-4 (rank@setup med 32, exactly the boundary the author's "what would make it wrong" predicted), hot belt σ_e=0.15 (waste 94.9%). `dup=0`, `outside_cone=0` everywhere — the memo-artifact distinctness check passes.

**Why gold** — it shows an adopted premise is wrong (rank 4 is one point of a density law Θ(ρ·n/arc); setup-rank covers ≤ 27% even at ring density) at the board's top scaling risk, and adoption is a contract edit to `b-coorbital-cert`, which is still queued unshipped — within one step, no code.

**Caveats recorded for the integrator:** the 0.2–0.5 coefficient drifts (0.35–1.0 across my probes; tail margin max/med 4–37, not 30) so the contract must certify it, not inherit a range; the ~10⁴ setups/encounter at game ρ is scaling arithmetic plus one direction point, not a measurement at 1e-5; the window-tier miss regime remains unmapped by either run.
