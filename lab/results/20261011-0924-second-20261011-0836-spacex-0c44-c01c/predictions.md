# Predictions (written before the decisive experiments)

Question (the checker's named gold experiment for run 20261011-0836-spacex-0c44): does
"no fixed kick cadence passes the plane's frozen gates" stand on two recorded, regenerable
pillars — (a) B14's oracle cost separated from the law's, with B14's behaviour verdict on the
record at an admissible cadence, and (b) the B13 tail's mechanism (refusals, not depth) on the
record at N=7/8/9?

Already read (controls, not held out): the author's B13 sweep N=1..9 (reproduced bit-for-bit by
me at N=7 and by the checker at N=7/9), the checker's own b13_by_draw findings, the author's
unlogged B14 N=2 line (243/255, apsides 0/53), and the B14 timeout walls at N=4..7.

## Held-out: the B14 cost split (new harness `b14_cost_split`, plus shipped CLI at N=1,2)

1. **The oracle dominates the phase budget.** `hill::moons()` (768 law-independent reference
   runs, 4 threads) alone takes 40–60 s wall on this machine. So a `behave --gates B14` phase is
   oracle-dominated at every cadence: the shipped CLI at N=1 and N=2 straddles 60 s with the
   machine's load (the author's 59.75 s pass and the checker's 60.0/60.1 s timeouts are the same
   coin). If the oracle alone exceeds 60 s here, the CLI times out at every N and only the
   harness can put B14's behaviour on the record.
2. **The law's share doubles per +1 in N** (256 sequential `restricted` runs, 50 periods each,
   kicks ∝ 2^N): ~2–10 s at N=2, ~1–5 min at N=7. So the only cadences a 60 s phase could ever
   admit are N ≤ 2, and only when the machine is quiet.
3. **B14's behaviour fails at every N in 1..7.** N=1: decisive fail (classification well under
   99%, many lost ships). N=2: the author's counts return exactly (243/255, apsides 0/53 —
   deterministic integers). N≥3 (never measured anywhere): classification may rise toward 99%
   at fine cadence — I do not predict which side of 99% it lands on at N=6/7 — but the apsidal
   rate (needs the tide's phase right, r9's harder half) stays far from 99% of rated at every
   N. **No N in 1..7 passes B14.** This is the strongest held-out claim: the apsides half.
4. **The judged population is law-independent and fixed:** 255 judged moons (≥ 64 needed), 53
   with a stable apsidal rate (≥ 32 needed) — the same at every N, matching the author's N=2
   denominators.

## Reproduction (not held out): the B13 tail's mechanism

5. `b13_by_draw` at N=7: four failures (#18, #27, #50, #57), all marginal (1.3–2.1e-2), zero
   refused kicks. At N=9: a different failing set (#5, #14, #27, #40, #57, #68), all ending
   alive with fault NoBoundOrbit and 10–330 refused kicks — the tail is the doll refusing to
   bind unbound planet-centric states, multiplying with cadence, not flyby depth. This is the
   checker's finding; I re-run it to put it on the record in this run's logs (the integers
   should match exactly).

## Controls

6. Negative: N=1 fails B14 decisively (if it passed anywhere near, the gate would not see
   cadence and the record would measure nothing).
7. The B13 step-7 baseline reproduced bit-for-bit before this file was written (60/64, worst
   2.12e-2/2.12e-2, the same 9 replaced draws) — the harness path is the same binary and tree.

What would make the run's claim wrong: if B14 passes at some N in 1..7 on the harness record
(then "no fixed cadence passes" survives only through B13, and the B14 pillar becomes "B14
cannot run within its budget"), or if the author's N=2 counts do not regenerate (then the
original dossier's behaviour numbers stay unverifiable and the pillar is only mine).
