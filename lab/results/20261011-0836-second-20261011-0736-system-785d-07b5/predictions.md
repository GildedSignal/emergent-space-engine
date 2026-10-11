# Predictions — second-author run 20261011-0836 (before the decisive experiment)

Written BEFORE the 4:3 scans and the gate runs. Already seen: the five scanned
cases' truth (scan npys), quad.json/calib.json (bit-identical regeneration),
final.json's numbers (reproduced by final.py, one authoring slip found: the j2 W
conversion). NOT seen: any j=3 (4:3) data, the switch-level gate behaviour.

## The experiment

The certificate as the ONLY resonance gate (classifier and B17's W table deleted):
switch to the exact handler ("doll stand-in" = the reference integrator, so any
behaviour mismatch is the gate's fault, not the handler's) exactly when
excursion(delta) = min(2 pdot_coh/|thdot|, c_H mu^(1/3)) >= q_e, with c_H
re-derived per geometry from the exact-resonance column alone (8 seeds, the
engine's one-column calibration; NOT the analytic derivation — that is open
theory and is named as such). Compared against the old gate (switch iff
|Delta(P1/P2)| <= W/2, W = 2.5 mu^(2/3)) and against pure truth, on r4 v3's
cases (2:1, 3:2; mu 3e-4, 1e-3, 3e-3) plus the 4:3 family (mu 3e-4, 1e-3).

Miss = truth fails at quantum q_e (running-mean e leaves [e0-q_e, e0+q_e]) while
the gate keeps the system on the averaged law.

## Predictions

- **PA (2:1 and 3:2, switch level).** j=1 at all three mu: ZERO misses at every
  quantum (the capped certificate over-predicts there; p90 of F = 1.2).
  j=2 mu=1e-3: a few misses (<= 4 of 120 systems) at some quanta — its F tail
  reached 3.42 — all absorbed by the guard form (switch at q_e/2), which I
  predict has zero misses on all five cases (P4a's margin, now at the switch).
- **PB (4:3, mu=3e-4): MISSES — the claim's domain ends at 3:2.** The 5:4
  resonance sits at delta ~ +0.027 in Delta-a/a (P1/P2 0.833 -> 0.8), INSIDE the
  scan grid (+-0.032). The 4:3 certificate's pdot_coh knows nothing about it, so
  systems detuned to the 5:4 side pump while the certificate says safe. I
  predict misses concentrated at large q_e (> ~2 cap ~ 0.10, where the cap can
  no longer cover the pumping) and on the +delta side. If instead there are zero
  misses, the certificate extends to 4:3 and the claim is broader than the
  checker's adversarial result suggested.
- **PC (4:3, mu=1e-3, overlap): fails safe.** c_H from the exact-resonance
  column will be O(10) (e pumps to ~2), so the cap ~ 1.9 exceeds every quantum:
  zero misses, but the zone swallows the grid at small q_e — "unsafe near
  resonance", no cadence information (same degeneration the checker found at
  3:2 mu=3e-3).
- **PD (cost).** At each case's design quantum (calib q_e = 2x far band), the
  certificate's doll-fraction is within ~2x of the old W-gate's on the same
  grid, and the certificate's zone shrinks as q_e grows (quantum-aware) where
  the W-gate's does not move.
- **PE (controls).** mu = 0: pdot_coh = 0 exactly, so excursion = 0 (the cap is
  c_H mu^(1/3) = 0): zero switches anywhere, including exact resonance. Far
  controls (pr 2.15 / 1.9): excursion < the calib quantum, no switch, and the
  truth band there is inside the quantum by construction (calib).

## Kill criteria

- Any miss at the guard level (q_e/2) on 2:1/3:2 kills the certificate as the
  gate (P4a would have been luck, not structure).
- Zero misses at 4:3 mu=3e-4 would refute PB and EXTEND the claim (reported
  either way).
- If the old W-gate has (near-)zero misses where the certificate has many on
  2:1/3:2, the deletion is not free and the claim dies as an engine change.
