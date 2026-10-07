Working...
Check written to `lab/results/20261007-1334-quant-7334/check.md`. Summary of the verdict:

**Grade: silver.**

| Check | Result |
|---|---|
| Reproduction | Exact, bit-for-bit (38 s; all dossier numbers match to the printed digit) |
| Predictions | Written before the run (13:44 < 13:55); P1 held; **P2, P3 falsified** and honestly reported |
| Attack 1 — solver noise | dt=1/128 vs 1/32 delta difference 160–1050× below scar spread → scar is physics |
| Attack 2 — 2:1 resonance | H_raw grows 29.3→33.7 over 100 yr (+0.66 bits/decade) vs flat control — flat-in-t is regime-bound |
| Attack 3 — floor metric | kNN + birth mean anomaly: 22.60→20.81 bits only; wound field defeats any smooth model |
| Attack 4 — pre-registered N | 16384 vs 8192: immaterial (±0.04 bits) |
| Novelty | First H_live measurement (HANDOFF: "not measured yet"); distinct from born-floor 98bc |
| Goal fit | Kills "birth program + scars" as a belt cache (22–38 bits/body ≈ 2.8–**4.8** GB at 10⁹); fits "compute only surprises" |

Why silver, not gold: two held-out predictions failed (honest reporting, but that bars gold by the 1 October precedent), and the constructive half — the compiled secular field actually re-deriving the belt to ~0 bits — is asserted, not measured. The one experiment: run the belt through H0190's compiled averaged field and measure the residual entropy, including at the resonance strip.

Author's misses beyond the above: the scar omits the phase column (winds ∝ t, +log-t entropy — reinforces the conclusion but "flat" is optimistic), the quoted instrument-verification numbers (2×10⁻¹⁵ round-trip, 1.4×10⁻¹¹ drift) exist in no shipped artifact and my harsher round-trip contradicts the figure, and "scenes unchanged since" contradicts the pre-registered N=16,384 vs the run's 8,192.

Nothing else in the run folder was changed (the author's own reproduce command regenerates `hlive.json` identically — disclosed in the check).
