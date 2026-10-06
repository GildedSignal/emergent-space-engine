Grade: gold

**Abstract.** With the Riemann sign fixed and windows Richardson-extrapolated to zero, the Fermi-frame Schwarzschild tide is confirmed as the q-fermi2-tide closed form, and phase-2 cadence follows N/orbit = 512π√2·3f√g/√((2−3x)²+g²), 3047→421 monotonically. All artifacts reproduce byte-identically. The prior run's axis epoch columns (3214/4017/4038/16081, its checker's included) are unwrap artifacts; honest sweep is exactly 2π per their window; their tensor columns survive (2877/2395 exact). Held-out attacks confirm: epoch formula vs einsum at r=8/30 to 1e-5, kernel at r=3.5/5 to 4e-5. Gain: E9 freezes (positive = this kernel, negative = naive); strong-field cadence fear deleted (421, not 16081, at 3.1M). Cost: none new — the closed form is already schwarztide.py; the epoch rule is one rational comparison. P6's unbound half failed (6898/5320 vs <1500), honestly reported.

## Reproduction (clean tree, /tmp/check-b7a4, patch.diff empty)

- `python3 sanity.py` (0.70 s): reproduces; fixed-sign einsum = diag(−3w, +w) at 6M and (−32w, +w) at 3.1M; static-r̂ sweep 4.4429 = 2π−geod at 6M (the geodetic anchor).
- `python3 kernel.py` (49.4 s vs the dossier's 56 s — same order, only number that differs): `decisive.log` and `kernel-table.json` **both byte-identical** to the stored copies.
- `python3 leakage.py` (3.6 s): identical to `leakage.log`; 3.1M members plunge at every orbit-scale window, 6M gives −2.2463/−2.6432/−0.5476 at T_p/4, T_p/2, T_p.
- Timeline: `predictions.md` 02:34:24, before the decisive run (decisive.log 02:47:07). `kernel-table.json` mtime 02:48:58 reveals a second, unlogged run of the identical `kernel.py` — benign (my independent rerun is byte-identical, so both stored artifacts regenerate), but it should have been disclosed.

## Held-out predictions

P1, P3, P5, P7 held (P5's numbers to 0.3%: predicted 3055/2035/1337/421, got 3047/2035/1338/421). P2 partial (mechanism and magnitude confirmed at 6M; the 3.1M full-window value is unmeasurable — members plunge, reproduced). P4 partial (0.4–0.7% vs predicted 1e-3). P6 eccentric half held (4459 in 2000–6000); **P6 unbound half failed** (predicted <1500/passage, measured 6898 parabolic / 5320 hyp) — reported as failed, with the correct mechanism (amplitude drift ∫|ṁ|/m ≈ 6 ln(r_max/r_p) accruing at large r).

## Adversarial cases (4)

1. **The prior artifacts reproduced from the prior run's own code.** `probe-orig.py` is byte-identical to their `probe.py` (verified). Their formulas (their lines 246–256) on their window at r=1000/6/3.1: their half-angle unwrap `np.unwrap(arctan2(·)/2)` gives 3211/3211/3210 at my grid (their stored JSON: 3214.2/4017.2/4037.7 — all land on 2.0–2.5 turns of 1608.5, exactly the "(1+k/2) full turns" the author predicted); their non-unit naive reference gives 16014 at 3.1M (stored: 16080.9). The author's doubled-angle fix gives **1608.5 = 256·2π at every radius**, as the identity ω = √(M/r³) demands — I re-derived that identity independently before running. Their tensor counts (no unwrap involved) reproduce exactly: 3051/2877/2395 with the fixed sign, and normalized per true orbit match the closed form (2034.6 vs 2034.6 at 6M; 430.1 vs 421.1 at 3.1M). The bug is confirmed in their source at their line 118.
2. **Held-out radii for the epoch formula (not in their table).** r=8: einsum-path tensor quadrature 2324.0 vs formula 2324.1 (1.0e-5); r=30: 2874.1 vs 2874.1; axis 1272/1526.0 vs 512π√g = 1271.6/1526.0. The formula is the einsum measurement to five digits.
3. **Held-out kernel scenes.** circ r=3.5 (between their 3.1 and 4, near the photon sphere): geodesic Richardson −3.99996 vs closed −4.00000, transverse +0.50000; r=5: −1.74997 vs −1.75000. Sequences monotone, second order (ratios ≈4). No breakdown where they did not look.
4. **E-independence at the original P4 scene** (L=4.1, r=6, E=1.05 vs 1.5): closed-form eigenvalues bit-identical [−3.40083333, 1, 2.40083333]m. The scene re-label of the prior run's "eccentric" checks out: L=3.5, rp=6.5 ⇒ ra=7.5 exactly (e=0.071, not their e≈0.88).

## Novelty

No HISTORY entry (newest H0214) or doc contains the corrected h→0 kernel table, the epoch rule, or the artifact correction; docs have no epoch-rule formula. This run is the exact experiment the prior run's checker specified as gold-making ("re-run the decisive table with the template sign fixed … windows pushed to h→0; freeze E9's controls"), and HANDOFF queues exactly this second author. It corrects the prior *checker* too: their "corrected true-axis count 4017" was itself an artifact.

## Goal fit

Board focus item 4 (the Fermi-frame Schwarzschild tide, phase 2 after E9). "Shows that a premise is wrong": the prior epoch columns, at 16081/orbit near the photon sphere, are artifacts; the honest number is 421, and cadence is set by the weak field — the strong-field fear is deleted (principle 1: compute not done). E9's controls are now freeze-ready: positive = the closed form agreeing with geodesic pair differences at h→0; negative = the naive kernel (accuracy, per K1 of the prior run — and the same 512π√g cadence on circulars, so its crime is not cost). Validation against geodesic pair differences, never against the formula — principle 22.

## Why gold, not silver

Reproduced byte-identically from the shipped code (the record-keeping failure that capped the 5 October silvers is absent). The claims being adopted — kernel table, epoch rule, artifact correction — all held under prediction *and* under my independent attacks at scenes and radii the author never touched. The one failed sub-prediction (P6 unbound) is a cost estimate secondary to every adopted number; it was reported as failed, not claimed as held (unlike the 1 October red-team), and diagnosed per H0183. Every anchor of K4 is reproduced from the prior run's own code and JSON. Adoptable within one step.

## What the author missed

- **Three claims the log contradicts.** "Transverse eigenvalue +w at every scene to ≤2×10⁻⁴": rosette peri is +0.50115 (2.3e-3), parab outbound +0.49918 (1.6e-3), ecc peri +0.50053 (1.1e-3) — it holds at circulars and hypers only. The K3 table's "axis rule (true = naive)" prints 289 at 3.1M, but the log's naive count there is 308 (+6.6%); equality holds only for r ≥ 4M. The dossier cites `leakage6.log`, which does not exist (both probes are in `leakage.log`).
- **P4's scene silently changed**: predicted L=4.1 at r=6 outbound, measured L=6.5 at r=20 — the magnitude miss (0.4% vs 1e-3) is reported, the scene change is not.
- `sanity.py` carries two cosmetic bugs that do not touch the decisive path: its "closed" print miscomputes λ (shows −8w/−3.19 not −3w/−1.07), and its axis sweep unwraps 2·(2θ), doubling the printed sweep (8.8858 = 2×ωT_p at 6M).
- The undisclosed second `kernel.py` run (see timeline).
- Carried forward, as the lens admits: out-of-plane eigenvalue quoted from the closed form, never measured from geodesics; the τ₁₀×epoch-rate product (kicks per battle) taken from the prior run's table, not re-measured; member-level L1/L2/L3 error tables not redone; eccentric/unbound epoch counts are closed-form quadratures along measured r(τ), not geodesic-path counts; and the unbound cost's practical cap (amplitude drift accrues where no battle exists — the honest r_max for a battle-scene passage is an engine decision, not a physics one).
