# Predictions (written before the decisive run)

Question: can the galaxy doll's generator be the star doll's own mechanism — the cycle
compiled from (E, L) by 1D radial quadrature against the galaxy's Phi(r), with perturbations
(the bar, spirals, encounters) as orbit-averaged kicks on (E, L), and the regime boundary
chosen by the compiled frequencies (m(OmPhi - OmP) ~ k OmR) alone?

Setup not tuned on: 2D galaxy = log-core halo + Miyamoto-Nagai disc (analytic), m=2 bar
perturbation eps * v0^2 * r^2/(r^2+rb^2) * cos(2(phi - OmP t)), 512 orbits sampled over
R in [0.3, 4.0], epicyclic e up to ~0.3, DOP853 rtol 1e-10.

Held-out cases (run after the main population, no retuning):
  H1: eps = 0.10 (strong bar) — resonance overlap should create migration the
      single-resonance detector cannot tag; recall is allowed to drop, and I predict
      it drops below 60%.
  H2: OmP shifted by 25% — the resonant rings move in R; the detector must follow them
      (flagged orbits' R_g distribution must move the same way), with no retuning.

Predictions on the main population (eps = 0.03):
  P1 (separation): orbits that migrate in L (linear walk, t-stat > 4) are flagged by the
      resonance detector at min_k |2(OmPhi-OmP)/OmR - k| < w for some w <= 0.15, with
      recall >= 80% and false-positive rate among non-walking orbits <= 20%.
  P2 (error type): non-flagged orbits show bounded E and L wobble (amplitude of order
      eps * v0^2 in E), no linear walk (t-stat < 4 for >= 95% of them).
  P3 (cost): compiling the cycle (roots, T_r, Dphi by quadrature in psi panels) costs
      O(10-100 us) per orbit, and deriving a position from the compiled tables costs
      O(1 us), against O(10-100 ms) of DOP853 stepping for the same span: >= 10^3x
      cheaper per orbit, and zero re-cost until an event changes (E, L).
  P4 (regime size): the flagged fraction of a broad disc population is under 50% at
      w = 0.15 — most of the galaxy compiles, the resonant rings pay.

What would make it wrong: recall << 80% (frequencies are not enough to choose the
regime), non-flagged orbits walking (averaging dies even off resonance), or compile
cost within an order of magnitude of stepping (no saving to bank).

## Outcomes (after the run; nothing above was edited)
P1 FAILED (recall 13% vs >=80%); P2 FAILED (14% of orbits walk, none inside R<1.8);
P3 held in spirit (690x per 60 periods, rising with time; eval-on-read 2e4x cheaper than one
stepped period); P4 moot (gate does not separate; churned fraction 14% at eps=0.03, 55% at 0.10);
H1 HELD (recall 6% << 60%); H2 HELD (churned band moved inward with OmP).
