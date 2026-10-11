# Predictions — second author, written before the decisive runs (2026-10-11 ~12:40 UTC)

Base: the run's own `inspiral.py` (copied from 4c5b) with the checker's one-line fix
`circ_L: sqrt(a/(a-3)) -> a/sqrt(a-3)` (verified against the author's own control
`EL_from_ae(a, e->0)`: agrees to 1e-15; R(u0) double-root residual 1.1e-16). New
experiments in `second.py`, importing the fixed module. Cases below are held out: I have
not run them on the fixed code. The checker measured some of them with its own replication;
where I cite its number I mark it [C] — my ranges are for MY run of the shipped-fixed code.

## A. P9 rerun with the fix (decisive for the wiring rule)

- **A1.** `python3 inspiral.py` on the fixed code: `P9_spurious_e` (two-flux drift from a
  circular birth a0=100, nu=0.25) comes out **< 1e-3** — the author's original pre-registered
  band [1e-4, 1e-2] actually held, and the dossier's "two-flux wiring is inconsistent →
  projection rule" was an artifact of the broken harness. [C: checker measured 0.0000]
- **A2.** Every other field of `inspiral-out.json` is **bit-identical** to the original run's
  JSON (`circ_L` enters no other output: the circular drift's state is E alone, `a_end=6.0`
  is hard-coded, and `run_eccentric` never calls `circ_L`).

## B. The pre-registered kill criterion, applied to high-e births (the missing experiment)

The author's kill line: wall(eps=1e-2) >= 5x outside the separatrix at nu >= 0.01 kills
"Peters' a(t) as the generator" for that corner. Domain note the checker missed: B11's
frozen domain is **p 20-1000, e <= 0.6, nu <= 0.25** (law.md, gate table) — the dossier
quoted it as "(nu <= 0.25, p >= 20M)", dropping the e-cap. Grid: births at the p=20M
boundary (a0 = 20/(1-e0^2)), nu in {0.25, 0.01}, e0 in {0.5, 0.6, 0.65, 0.7, 0.75, 0.8, 0.9};
plus the checker's exact case (nu=0.25, e0=0.9, a0=110).

- **B1.** At nu=0.25 the wall/separatrix ratio crosses 5 between e0=0.6 (ratio ~3.8, from the
  original table: 26.1/6.8) and e0=0.8; i.e. **e_kill(0.25) in [0.6, 0.8]**. My guess: ~0.65-0.7.
- **B2.** At nu=0.01 the ratio at e0=0.9 is **>= 10** (wall at start ~110 vs separatrix ~9);
  e_kill(0.01) in [0.6, 0.9]. My guess: ~0.8.
- **B3.** For all grid points with e0 <= 0.6 (inside B11's frozen e-cap): ratio < 5 at the 1%
  bar — the kill does NOT fire inside the frozen domain at the 1% behaviour bar; it fires
  only in the high-e corner the frozen gate already excludes. At the 0.1% (watched-binary,
  B2) bar the wall sits at/over the start already at e0=0.6, nu=0.25.
- **B4.** The checker's exact case (nu=0.25, e0=0.9, a0=110, p=20.9M): wall(1%) at start
  (>= 110M) vs separatrix <= 10M → ratio >= 11x: kill line met, as the checker said [C].

## C. Re-keys from 1000M, measured in the shipped code (not telescoped)

- **C1.** Circular nu=0.25 from a0=1000M: measured re-keys at eps=1e-2 in **[550, 750]** over
  ~(5-7)e5 orbits → **rate < 1.5e-3/orbit** (the telescoped table said 690; the analytic
  telescoping gives ~551; the true measured number replaces both). [C: eccentric e0=0.3 gave
  642 re-keys / 479k orbits = 1.34e-3/orbit]
- **C2.** Eccentric e0=0.3 nu=0.25 from a0=1000M: re-keys(1e-2) in **[600, 700]**, orbits
  ~(4.5-5)e5, rate in [1.2e-3, 1.5e-3]/orbit. The dossier's "0.005/orbit" overstates the
  calendar load by ~4x (the generator is cheaper than claimed).
- **C3.** a_end for the from-1000M eccentric run lands in the handoff band **[6, 12]M,
  e_end <= 0.1** (the checker saw 11.57 shipped / 6.78 its replication — near-separatrix
  sensitivity, not a physics change; see D).

## D. Handoff endpoint stability under step tightening (the soft-edges attack)

- **D1.** Tightening the dt cap 4x (dt factor 0.05->0.0125 and the hard caps halved twice)
  moves a_end by **<= 2M** and e_end by <= 0.05 for e0 <= 0.6, nu=0.25 births: the handoff
  band is ~[6, 12]M near-circular, a band, not a 0.1M constant.
- **D2.** W2's step-scaling claim: relerr at dt=P/256 vs P/64 drops by **[2, 8]x** (endpoint
  O(h)-dominated, not the RK4 256x; the dossier's "2x" was one sample of a noisy ratio).

## Kill criteria for this run

- If A1 fails (fixed P9 still pumps e > 1e-2), the two-flux wiring really is inconsistent on
  the exact family and the projection rule stands as a design rule — I would then report the
  refutation of the checker's expected outcome.
- If A2 fails (other JSON fields shift), `circ_L` leaks into the main results and the whole
  record must be re-read, not just P9 — that would be a deeper break than the checker found.
- If B3 fails (kill fires inside e0 <= 0.6 at the 1% bar somewhere in p >= 20, nu >= 0.01),
  the generator is not adoptable in any comparable-mass corner and the dossier claim falls
  further than the checker said.
