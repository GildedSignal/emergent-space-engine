# Dossier — 20261009-0208-fermi-fe6b

**Claim.** At 10⁹ bodies on one 8 GB M1, the steady-state budget binds on one term only —
the kick→pair-certificate cascade (each orbit-averaged kick re-derives ~813 candidate-pair
windows at ~5.4 µs/pair) — which costs 0.077 of the machine's 4 cores at rtf 100 with the
slack skin, 8.8 cores (2× the machine) without orbit-averaging, and 110–440 cores
unaveraged and unskinned (re-deriving the board's "about 190 cores" within 2×); every other
term — kick arithmetic (5×10⁻⁵ cores), encounters (5×10⁻⁶), program memory (16 MB), scar
reabsorption (3×10⁴× slack) — sits ≥ 3 orders below the ceiling, and per-body event keys
alone are 12 GB, so the one-queue design must key programs, not bodies.

**Bottleneck.** Board items "fitting 10⁹ in 8 GB… decided by distinctions created per
game-second" and the top scaling risk (candidate work vs real encounters); HANDOFF's named
unmeasured risk H_live. Gain: the budget ranks the three published levers by orders of
magnitude — orbit-averaging 114×, slack skin 12.6×, phase-neighbour certificate 200× over
the two-tier (and the only survivor of the fixed-extent O(N²) corner, 9.7×10⁴ cores
otherwise) — and deletes the per-body event key from the design space (12 GB > 8 GB;
program-level keys: 94 MB).

## Evidence

Working point: N = 10⁹, belt period P = 1.26×10⁸ game-s (4 yr), rtf = 100 (the plane's
speed), fixed belt density. Full table: `budget-table.md`; constants and citations:
`budget.py`, `budget.json`.

| Term | Value | Source |
|---|---|---|
| kick arithmetic (50 ns + 0.05 compiles/kick) | 4.9×10⁻⁵ cores | design [S6] + compile 3.4 µs [F1] |
| cascade, two-tier certs, no skin | 0.97 cores | 812.8 pairs/kick × 5.35 µs/pair [S1] |
| cascade, + slack skin 12.6× | **0.077 cores** | board taste log 6 Oct |
| cascade, phase-neighbour rank-4 | 4.8×10⁻³ cores | gold taleb-09b5 |
| cascade, fixed-extent belt (pairs ∝ N) | 9.7×10⁴ cores | O(N²) corner, no cert fix |
| cascade, unaveraged k=32, +skin / no skin | 8.8 / 110 cores | [S3] H0190 |
| encounter handling (0.00586/body/orbit) | 4.7×10⁻⁶ cores | steady.jsonl [S2] |
| program memory | 15.75 MB | 0.126 bit/body, gold components-98bc |
| scars, live fraction 1% / 10% / 33% | 0.24 / 2.4 / 7.9 GB | 24 B/scar [S5] |
| per-body event keys | **12 GB — does not fit** | 12 B (time,id) × 10⁹ |
| program-level keys (1 per 128-block) | 94 MB | shipmem packing |
| scar creation vs reabsorption | 222/s vs ≥5.7×10⁶/s/core | [F2] |
| max rtf on 4 cores: avg+skin / avg+phase / k=32+skin | 5,200 / 84,000 / 46 | table |

Fresh measurements (this Linux x86 shared runner, load 0.1–0.4, 16 GB; orders only — the
integrator re-measures on the M1):
- [F1] `cargo run --release -p emergent-universe --example cost` (shipped code, 9 s):
  compile 3.4 µs, state 2.8 µs, cartesian 0.3 µs, from_state 11.1 µs. Even a full
  recompile per kick is 1,275× below the measured 4.3 ms cascade.
- [F2] `python3 reabsorb.py` (18 s, `reabsorb-out.json`): re-band 5.7–7.0×10⁶
  bodies/s/core (numpy stable argsort — a lower bound; Rust radix ~10× more). Peak RSS
  3.6 GB on the 5×10⁷ case — over the 2 GB guidance, completed without harm.
- `python3 budget.py` (<1 s) regenerates the table.

Reproduce: the three commands above, in `lab/results/20261009-0208-fermi-fe6b/`.

## Predictions (`predictions.md`, written before any output was seen)

Held: state 2.8 µs (1–10), from_state 11.1 µs (5–50), cartesian order; cascade ≫ compiler
(1,275×); §6 kick-row omission ≥10³× (measured 1,570× with skin); 190-cores within 2×
(110–440); memory rows (16 MB program, 0.24 GB scars at 1%, 12 GB keys); ranking (cascade
the only term near a core at P=4 yr — 0.077 vs predicted 0.5–10; at P=1 yr it is 0.97,
inside the bracket).
Missed: compile predicted 20–200 µs, measured 3.4 µs (6–60× pessimistic — the compiler is
cheaper than guessed, which strengthens the cascade-dominates conclusion); reabsorption
predicted ≥5×10⁷/s, numpy measured 5.7×10⁶/s (the prediction presumes a radix sort the
proxy does not have).

## What would make it wrong

- The 5.35 µs/pair is the r8 prototype's window-setup cost (30 Sept); if the integrated
  certificate path is ~10× cheaper, every cascade number drops 10× — direction: budget
  even more comfortable. If kick cadence and certificates are paid per element change
  (the r8 v2 "next"), the same.
- k = 0.28/orbit assumes averaging holds; near resonance kicks stay per-conjunction
  (representation.md:68), multiplying the cascade 4–35×: rtf ceiling 5,200 → ~150–1,300.
  The resonant belt is the corner to watch, and a fleet battle co-located with the belt
  inverts the comfortable terms (dense order, not certificates).
- 24 B/scar and 12 B/key are orders, not measurements; M1 compute taken as 4 s/s (E-cores
  would add ~1.5×). P and rtf are game choices; corners, not fits.
- Nothing here was measured on the M1 itself (Linux proxy; the eight pending M1 probes in
  HANDOFF would pin the same constants natively).

**Cost of adopting:** none in code — a corrected §6-style budget row for representation.md
(the kick line must carry the cascade) and one structural rule into the b-h-live build:
event keys are program-level, never per-body. **Fit with PRINCIPLES:** "Cost follows
change and entropy" (3) — the cascade is exactly change fanning out into certificates;
"the memory floor is information-theoretic" (24) — keys at program level price the belt's
entropy, not per-body boilerplate; "minimize spike compute" (12) — the resonant corner is
the p99 risk this table names.

**The lens may have missed:** central-value thinking — the budget's tails (a resonance
sweep, a battle inside the belt, the player's light cone crossing a dense ring) are where
it inverts, and a Fermi table prices means, not tails; the reabsorption model is a sort,
not the shipped `shipmem` re-banding with Elias–Fano scars; and all throughput constants
come from one harness family (r8 + the plane), so shared-harness bias (the 5 Oct lesson)
cannot be ruled out by agreement alone.
