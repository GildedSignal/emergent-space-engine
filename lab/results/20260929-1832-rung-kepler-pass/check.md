# Check — rung canary kepler-pass (directed rung; verdict.py decides)

**Abstract.** The canary holds and the machinery is calibrated. Rerunning the author's scripts in a clean tree reproduced every number bit-exactly (metrics.json md5 equal, all six data files and picture.svg byte-identical, deterministic across reruns, 0.106 s wall). My independently written implementation of the frozen rung agrees: leapfrog exponent ~3e-10 (author 2.98e-10), bound_fraction 1, 200 steps/orbit, max|dE| 1.34e-3, L conserved to 1.6e-13; euler first unbound at step 15547 (orbit 77.7350), bound_fraction 0.007773. All five oracle values check. `verdict.py` returns PASS under the exact `run.sh` invocation, and its VOID/DISPUTED tamper paths fire. Adoption cost: none. One gap found: a bound-but-drifting euler (h = T/2000, 10^3-orbit horizon) passes both E1 (0.07) and B1 (1.0) with |dE| = 0.49 — near-saturation drift is invisible to both metrics.

## Reasons

**Reproduction.** `work/patch.diff` is empty (no repo edits to apply). Dossier commands in a scratch tree: gcc -O2 → 0.106 s wall (dossier 0.11 s), stdout, `metrics.json`, `summary.txt` and all of `traj_*/ener_*/win_*.txt` byte-identical to the author's (`cmp`); a second run gives the same md5. Machine: 4 vCPU Xeon @ 2.1 GHz, load 0.01–0.06, 0.9/16 GB used, up 8 min, cold — same class as the author's record.

**Independent implementation.** I wrote my own from the rung text (own window logic, velocity derived by vis-viva instead of the literal `sqrt 3`). It agrees: leapfrog max|dE| = 0.00134469 and final|dE| = 0.00128182 identical, exponent 3.74e-10 vs 2.98e-10 (float-path noise on a flat line; both ~10 orders under 0.2), bound 1, 200 steps/orbit; euler exponent agrees to 6 digits, first unbound step identical (15547, orbit 77.7350). I also recomputed both slopes from the author's `win_*.txt` with an independent least-squares: identical, and the 20 midpoints match the geometric midpoints of log-spaced edges 0.1·t_end·10^(i/20) exactly.

**Spec and oracles.** KDK ordering correct; euler updates position and velocity both from the old state (position uses the old velocity before overwrite). E and dE taken after every step, E = |v|²/2 − 1/|x|. Oracles: E0 = −0.5 (mine: −0.5 + 2e-16), L = 0.8660254037844386 exact, T = 2π, r envelope 0.500000000–1.505947 (oracle apoapsis 1.5 + O(h²) breathing, no secular growth over 10⁴ orbits), apoapsis speed L/1.5 exact, initial speed √3 by vis-viva. `bound_fraction` reads (j−1)/N; the alternative j/N differs by 5e-7 and changes no outcome.

**Predictions.** Held out before the decisive run: predictions.md mtime 18:35:44 < binary 18:35:47.48 < all outputs 18:35:47.5x; single run, no earlier artifacts. All bands hit: leapfrog max|dE| 1.34e-3 inside the stated 1e-5…1e-3, euler unbound at 77.7 < 500 orbits, bound_fraction 0.007773 inside 0.005–0.05, and the vacuous-E1 caveat was predicted in advance and confirmed.

**Adversarial cases (mine).**
1. Slow euler, h = T/2000, 10⁴ orbits: unbinds at orbit 4585 (inside the window span), exponent 0.0087 — saturation still blinds E1; B1 catches it (0.4585).
2. Bound-but-drifting euler, h = T/2000, 10³-orbit horizon: never crosses E ≥ 0 (rmax 118), yet |dE| = 0.49 — passes E1 (0.070) **and** B1 (1.0). The metric pair can be defeated by near-saturation drift that runs out of horizon before escape.
3. Unsaturated drift, euler h = T/20000, 100 orbits: exponent 0.708 > 0.2 — E1 fires as the rung's description promises; the metric is alive, not structurally dead.
4. Extremes: leapfrog at e = 0.6/0.7/0.8 stays bounded with slope ≤ 1.5e-7 and L conserved to 1e-9; at e = 0.9 with the same 200 steps/orbit it unbinds at step 1 (periapsis half-kick ≫ v_esc) — B1 catches it. The frozen e = 0.5 case sits well inside the stable region, not on a knife edge.
5. Machinery tamper: verdict.py gives VOID when the negative is neutered (euler bound_fraction forced 1.0), DISPUTED on an author/checker outcome mismatch, VOID on missing metrics — all paths exercised, plus PASS under the exact `run.sh` line-115 invocation.

**Novelty.** The canary and verdict machinery land in commit `6b22aee` (verdict.py + kepler-pass/kepler-kill); HISTORY.md's Kepler entries (H0052, H0164 and neighbors) are law-lab orbit banks, not rung canaries. Nothing to cite as a redo; the dossier itself claims calibration only, no physics novelty.

**Goal fit.** This calibrates the directed-rung machinery before real rungs count, per lab/README. It respects "A test that cannot fail is a control": euler is that control, it failed where it must, and the machinery detects a neutered control (VOID). "baby Spartans start small" — this is the smallest falsifying rung.

## What the author missed

- The author's caveat covers *escaped* negatives; case 2 above shows a **bound** near-saturation drifter also slips past both E1 and B1. Future rungs over longer horizons should add a max|dE| criterion or anchor windows at t = 0, or E1's blindness class grows with horizon length.
- C1's step budget is eccentricity-blind (leapfrog dies at e = 0.9 with 200 steps/orbit). Harmless here because the case is frozen at e = 0.5, but eccentric future rungs need a periapsis-resolution criterion, not steps-per-orbit alone.
