# Predictions (written before the decisive run)

Question (the checker's named experiment for gold): does the churn census, measured as a
function of window (60 -> 600 radial periods) with an *angle-based libration classifier*
replacing the slope t-stat, and on a *second potential and bar shape*, converge to an
adoptable design number (doll-edge width vs bar strength) — or does the claim collapse
(most "walkers" turn out to be wide librators and churn is rare)?

Setup, not tuned on:
- Potential P1 = the run's own (log halo RC=0.5 + MN-slice GM=0.5,B=0.2), bar A1 = the
  run's own extended bar r^2/(r^2+1), OmegaP=0.5.
- Potential P2 = centrally concentrated (RC=0.25, GM=0.8, B=0.1), bar A2 = localized
  Gaussian-shaped oval, peak at r=1.2, decaying as exp(-(r/1.2)^2); OmegaP=0.5.
  P2/A2 has never been run by anyone: all its numbers are held out.
- Populations: Rg in [0.35,4.0] (19 radii) x de in [0,0.3] (11 amplitudes) = 209 orbits;
  DOP853 rtol 1e-10, atol 1e-12, same as the original truth. Circular de=0 rows are kept
  and the compile gets a circular closed form (the original's nfail=19 double-root edge).
- Classifier (angle-based, replaces slope t-stat on L):
  omega_phi_bar = total dphi/total T; OmR from a cycle compiled at the window's median
  (E,L); k* = round(2(Om_phi_bar - OmP)/OmR); beat angle
  theta(t) = mod(2 phi(t) - 2 OmP t - k* OmR t, 2pi); Rbar = |mean(e^{i theta})|.
  - librator: Rbar >= 0.5 (angle confined; trapped, L oscillates but does not walk);
  - walker: Rbar < 0.5 AND |dL| > 5% (net L change, first vs last decile medians);
  - quiet: Rbar < 0.5 AND |dL| <= 5%.
  Windows are prefixes of ONE 600-period integration per orbit: 60, 120, 240, 480, 600.

Predictions (each falsifiable, thresholds fixed now):

- W1 (window growth, P1 eps=0.03): walker fraction grows monotonically with window, from
  ~14% at 60 periods to >= 20% at 600. The 60-period census is a lower bound.
- W2 (libration reclassification): at 600 periods the angle classifier splits off a
  librarian class the t-stat could not see: librators >= 3% of the population at eps=0.03
  (they were counted as walkers or quiet before). Their L oscillates with amplitude > 2%
  but no net drift.
- W3 (spatial pattern-lock, both potentials): the walker band's inner edge stays within
  0.4 of the corotation radius of each potential (Omega_phi = OmP) at every window, and
  the band's outer edge grows with window (resonance overlap spreading outward through
  the OLR). On P2/A2 the band sits at P2's own corotation (predicted ~2.2-2.4), NOT at
  P1's 2.17 (different potential must move it if the lock is to the pattern, not to a
  remembered number).
- W4 (doll-edge width vs bar strength): at fixed window the walker band's radial width
  grows with eps; the growth is faster than sqrt(eps) (single-resonance width) — closer
  to linear in eps between eps=0.03 and 0.10 (overlap regime). Prediction: width(0.10) /
  width(0.03) >= 2 at the 60-period window on P1.
- W5 (compile edge): the circular closed form removes all compile failures: nfail = 0
  in every population, including the de=0 rows (P1 had 19/399 = 5% failing before).
- W6 (quiet orbits keep the error type): among quiet orbits at 600 periods, E wobble
  stays bounded (no secular E drift): max |E(t)-E(0)|/|E| does not exceed ~3x the
  60-period wobble for >= 95% of quiet orbits (bounded, non-compounding; the doll's
  readout error type is unchanged).

What would refute the claim: walker fraction saturating or *shrinking* with window (the
14% was transient), the angle classifier absorbing most former walkers into a bounded
libration class (churn is rare; static dolls mostly fine), the P2 band not tracking P2's
corotation (no spatial law to adopt), or width(eps) flat (no design number to report).

## Outcomes (appended after the run; nothing above edited)

- W1 HELD: P1 eps=0.03, walk 0.258 -> 0.282 -> 0.311 -> 0.349 -> 0.349 over W=60..600
  (monotone, saturating); median walker dL grows 0.137 -> 0.530, so the walking is real
  migration, not oscillation. The 60-period census is a lower bound.
- W2 HELD: librators 5.3% at 600 periods (3.3% at eps=0.01, 5.3% on P2 eps=0.03), sitting
  exactly at corotation (Rg in {1.97, 2.175, 2.38} on P1, all k*=0, dL <= 0.7%). The t-stat
  never flagged them; they were counted quiet before.
- W3 FAILED, and the failure is the finding: the band is NOT corotation-centered. On P1 the
  sustained band is [1.57, 3.80] (inner edge = corotation - 0.60 > my 0.4). On P2 (localized
  bar) there is NO sustained band at eps=0.03: the 60-period walkers (9.1%) are bounded
  L-oscillators (swings up to 47%) whose dL collapses below 5% by 600 periods, concentrated
  at Rg~0.96 where the bar envelope peaks (A2(0.96)=0.92). The churn band tracks eps*A(r)
  in the pattern frame, not the resonance radii alone.
- W4 UNTESTABLE AS WRITTEN (censored): at eps=0.10 the P1 band spans the whole sampled disc
  [0.55, 4.00] (77% walk), so width(0.10) is a lower bound; 3.45/2.79 = 1.24 < 2 at face
  value. Below censoring the width grows super-linearly: 0.61 -> 2.79 for eps 0.01 -> 0.03
  (x4.6 for x3; sqrt(eps) would give x1.7). At 600 periods the P1 band sharpens inward
  (0.55 -> 1.57) while the fraction grows: transient inner walkers resolve as bounded.
- W5 HELD: nfail = 0 in all 11 populations (209 orbits each, 19 circular rows per
  population compiled by the closed form; the original failed 19/399 on exactly these rows).
- W6 HELD: quiet orbits' E stays bounded: 99.2% (P1 e03) and 100% (P1 e10, P2 e03) of quiet
  orbits have Ew(600) <= 3*Ew(60); median net dE even *shrinks* with window (0.0036 -> 0.0009):
  no secular E drift outside the walker class.

Bonus (the design number, not predicted): sustained churn vs eps_eff = eps*A(r_corotation):
  eps_eff 0.008 (P1 e001): 0.5% walk at 600p; eps_eff 0.007 (P2 e03): 0.0%;
  eps_eff 0.025 (P1 e03): 34.9%; eps_eff 0.083 (P1 e10): 66.5%.
  The switch-on sits between eps_eff ~ 0.008 and ~ 0.025 (P2 e10 at eps_eff 0.025: 26.8% sustained, band [0.96,2.58] cut at the envelope).
