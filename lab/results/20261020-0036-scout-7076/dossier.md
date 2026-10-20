# Dossier — the cadence ladder on the frozen certificates

## Claim

The kick-cadence lever's legal floor is measured on the frozen certificates for the first
time: the tide class holds to 8× coarser (flight-backing the ledger's split8+Carlson
closure; 16× destroys resonant libration, 0.981 → 0.023), but the encounter class is
legal only at 2× **finer** than the shipped default (B13: 64/64 at step 8, 60/42/15/3/1
at 7/6/5/4/3) — the shipped cadence has no green octave, and the encounter cliff is the
certificate case for the exact pair event.

## Bottleneck

The board's kick line: "how many kicks a body really needs per orbit". The 10⁹ ledger
(budget-1e9, 3aec) makes the cadence cut mandatory and Carlson equally mandatory ("the
cost bar is ≤ 4.9 µs/event" at split8), with split8's legality *cited, not re-flown*
(7f97/1db4). Two premises to test: (a) can the cut go deeper than 8× (then the Carlson
bar relaxes 2× per octave and today's kick cost may fit), (b) is the legality
class-independent (the ledger applies split8 to the belt stream; the encounter class
was never swept). Gain if (a) held: ~2-8× on the cost bar; if it fails: the closure's
only remaining path is the kick cost, now flight-proven.

## Evidence

All rows: shipped code, `behave --law plane --plane-step N --gates G` (the frozen gates
judge the shipped engine through its public API; the cadence is the only dial), plus the
shipped `jacobi` example. Linux/x86, 8 vCPU, load low; pass/fail rows are
integer-deterministic. Full log: `ladder.txt`; regenerate: `regen.sh` (~12 min).

| step | kicks/radial period | B17 resonance | B13 assists (bar ≥ 63.4/64) | B14 | Jacobi worst (Hill class; B12's bar 1e-4) |
|---|---|---|---|---|---|
| 9 | 512 | — | FAIL 63/64, worst **inf** | — | — |
| 8 | 256 | FAIL timeout (60 s judge) | **PASS 64/64**, worst 5.30e-3 | — | — |
| 7 (shipped) | 128 | FAIL timeout (60.1 s) | 60/64, worst 2.12e-2 (the standing baselined red, reproduced) | timeout | Range refusal (example's own default is 6) |
| 6 | 64 | **PASS** [0.99949, 1.00009], libr 0.998 | 42/64, worst 8.47e-2 | timeout | 5.1e-6 |
| 5 | 32 | PASS [0.99767, 1.00031], libr 0.996 | 15/64, worst 3.39e-1 | timeout | 1.8e-5 |
| 4 (= split8) | 16 | **PASS** [0.99049, 1.00282], libr 0.981 | 3/64, worst 1.34e0 | timeout | Range refusal |
| 3 | 8 | FAIL [0.95175, 1.30636], libr **0.023** | 1/64, worst 2.87e3 | timeout | 3.2e-4 (over B12's bar) |
| 2–0 | 4–1 | FAIL (pump [0.556, 3.730] at 2; regime 13/19) | — | — | — |

Numbers in B17 brackets: e-pump ratio bounds over the resonant cases (bars [0.8, 1.25]);
"libr" = min libration amplitude ratio (bar 0.8).

**Three laws, read off the table.**

1. *The tide class degrades second-order until a phase cliff.* B17's pump error and the
   Jacobi error both rise ×4 per octave coarser (Jacobi 5.1e-6 → 1.8e-5 → 3.2e-4; pump
   deviation 0.0005 → 0.0022 → 0.0095 at 6/5/4). B17's failure at step 3 is **not**
   that law (h² predicts ~0.04, measured 0.31): the libration amplitude collapses
   0.981 → 0.023 — the resonant angle's libration is destroyed by phase aliasing at 16×.
   The smooth error and the cliff are ~1 octave apart: **split8 sits one octave below
   the cliff with ~9× margin on the smooth law.**
2. *The encounter class is legal only at step 8.* B13's distribution collapses at every
   octave (64 → 60 → 42 → 15 → 3 → 1), with worst ΔE growing super-quadratically
   (5.3e-3 → 2.1e-2 → 8.5e-2 → 3.4e-1 → 1.3 → 2.9e3): the perijove arc's impulse
   sampling, not a smooth tide error. The finest edge fails too (step 9: one row `inf`).
   **The legal window is one octave wide and does not contain the shipped default.**
3. *B14 is not cadence-bound*: it times out at every flown step (7–3) — its cost is the
   judge's scene (256 moons × 50 orbits through the plane's per-event path), not kicks
   per orbit. The B14 row stays dark for cadence questions.

**Composition into the 10⁹ ledger** (arithmetic on budget-1e9/3aec's own constants; the
stream rate ∝ 2^(N−7), so the cost bar at plane-step N is 4.9 µs · 2^(4−N)):
- The mandatory-cadence-cut clause is **flight-backed, not citation-backed**: split8
  (step 4) is legal on B17 with margin. The deeper-cut alternative is dead on the
  certificates (step 3 breaks B17's libration and crosses B12's Jacobi bar), so
  **Carlson (or an equal-cost kick ≤ 4.9 µs) remains the only closure path**, exactly as
  composed.
- The class-split is certificate-necessary, not convenient: the encounter class cannot
  follow the belt's cut even one octave (42/64 at step 6). BELT_SPLIT's ≥ 4 R_H scoping
  is the right shape; encounter-bearing tubes must keep fine cadence *or* leave the
  metronome.
- New row the ledger lacked: to make B13 green by cadence alone, the plane's
  encounter-class tubes must run at step 8 — **2× the encounter-class event rate**. The
  alternative already in the design (m-meso-motion's silver: the close encounter as one
  exact pair event, regime chosen by U/√(μ_p/b)) deletes the arc from the cadence budget
  entirely; the B13 cliff is its certificate-side necessity argument (no metronome
  cadence is both legal and economical for perijove arcs).

## Predictions

`predictions.md`, written before the ladder. C1–C3 (controls) all held — B17@6 PASS and
B13@7 = 60/64 reproduce the record exactly. P1 held (×4/octave Jacobi law, two octaves
refused by the example's Range edge, disclosed). P2 held (B17 first breaker; first
failing octave exactly step 3). P3 **failed in the interesting direction**: I predicted
B13 stable to step 4; it collapses immediately, and the un-predicted fine side (B13@8
PASS 64/64) is the run's most adoptable atom — the standing baselined red is
cadence-curable. P4 failed (B14 times out at every cadence). P5: the k* = 4 branch —
"the composed clause stands" — realized.

## What would make it wrong

The gates judge the strong-tide restricted class (μ = 1e-3, sep 5.27×10⁸ M); the
belt-real class (2⁻¹⁰ planet, belt at 2–3 AU, ≥ 4 R_H) has weaker synodic coupling, so
the belt's own legal floor can only be deeper — my B17 row is the conservative cap, and
the belt's split8 legality rests on the same gate family either way. The B13@8 pass is
one scene set (64 fixed draws, 9 replaced); a different flyby draw set could sit closer
to the bar (worst 5.3e-3 against 1e-2 — a 1.9× margin, one octave of h² headroom). The
`inf` row at step 9 is not attributed (PLANE_TRACE would name it; disclosed). The
Jacobi column comes from the example's 6-ship Hill-radius class, not the B12 gate
itself (whose v3 instrument is under redesign; used here only as the 1e-4 bar).

## Cost of adopting, fit with PRINCIPLES

Nothing to adopt in code — the dial is shipped. The two decisions this arms: (1) the
integrator's Carlson bar stays ≤ 4.9 µs (premise now flight-backed); (2) the
encounter-class cadence: either step 8 for flyby-class tubes (one config change, +2×
encounter-class events) or the exact pair event (law work, deletes the whole row). Fits
PRINCIPLES #18/#19 ("A fix signals the wrong representation": a metronome resolving
perijove arcs the two-body generator already knows exactly) and Julien's cadence note
("kicks belong on certificates breaking, not on a metronome" — B13's cliff is the
certificate breaking under the metronome). Fits #2 (behaviours, not error size: the
cliff is a regime break — libration destroyed, regime rows mismatched — not a large
smooth error).

## The lens

The scout lens searched for the floor where the certificates say it is; what it may
have missed is the *cost* side of step 8 (I did not re-price the locals' stream in the
ledger — the ×2 is a rate fact, the core-count consequence is the integrator's
arithmetic), and any legal cadence deeper than 8× that a *different* certificate set
(a belt-scene gate, B18b) might permit — the board's B18 belt rung is the instrument
that could extend the belt's floor past B17's cliff.
