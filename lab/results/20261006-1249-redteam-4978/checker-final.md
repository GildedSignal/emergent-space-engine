Working...
Check complete. `check.md` written; only file added to the run folder; no commits.

**Grade: gold** — with one defect found and reported.

**Reproduction**: `sep_jet.py` output identical to `sep_jet.out` (2.9 s, 79 MB); every dossier number matches. `patch.diff` empty. `predictions.md` (13:02) precedes the decisive output (13:08).

**Premises verified in the repo**: law.md line 35 (jet adopted from df81, C treated as constant, "0.05 compiles per kick", second check never ran); gate table B5/B9/B12/B19 cover nothing that kicks then classifies; HANDOFF line 25 grounds the `NoBoundOrbit` player-visibility claim.

**Adversarials** (independent implementation): instrument verified to 7 digits by RK at the deepest zoom-whirl case; energy kicks fail too (10⁷× floor); second-order jet still fails 3×10⁴×; curvature 2.7×10⁵× weak field, making the re-anchor threshold 50–2500× too lax; ε-scaling cleanly quadratic; at the plane's own kick quanta (10⁻⁴–10⁻⁵ of L) the kill band narrows to δ ≲ 0.03/0.003 but persists.

**Defect found**: `plunge_phi` prefactor √(2s) instead of 2√s — P4's horizon azimuth is 12.51 rad, not 8.85 (quadrature ratio exactly √2; RK confirms). Non-load-bearing: the plunge itself and the phantom pericenter (13.8 rad, now 1.3 rad past the horizon) both stand.

**Why gold**: bit-identical reproduction, every strengthening I threw at it held, it falsifies a singly-checked adopted premise in exactly the strong-field regime it was named for, and adoption (per-kick root-count regime test + forced recompile in a declared band) is one local step. The author's honest P1 amplitude miss and my √2 find don't touch the kill.
