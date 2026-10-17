Working...
Check complete. Verdict: **gold**, written to `check.md` with the page corrected in place.

**What I verified:**

- **Reproduction** — Re-ran the author's `analyze2.py` on the raw window-sweep logs: every dossier number regenerates (9/18 fires, 0 P2/P3 fails, `out=` 0/2,295, 950 PRE at D=0, m≠0 only on the 9 fires, 9/9 armed survivors). Raw logs carry what the analyzer's weak P2 check didn't: armed leads of 51–452 publishes before every fire. The FIRE line prints the assert's exact inputs (`s0=32 fin_hi=48`) immediately before the *unmodified* assert panics — print-only confirmed by reading the patch.
- **Predictions** — `predictions.md` (18:33:44) precedes the sweep outputs (18:33:47→18:35:36); one disclosed pilot; P1–P6 all held.
- **Adversarial (5 new fires, ~2,632 RB events, all outside the author's tested range)** — batch driver 4/9 fires (viol 16 = D exact, armed from publish ~20); vmax-8 late-reclash fire at s0=1376 (viol **48 = 3 windows**, D=viol still exact, armed lead >314); crossing family and seeds 21/23 hold the equality law; window 32 never fires but shows 114–116 armed D=32 lines per draw; min_region-32 control clean. `out=` never opened on anything.
- **Novelty** — HISTORY holds no prior state-decision claim; fd35's page named exactly this experiment as the open item.

**Two overstatements corrected on the page:** "violations always exactly one window" and "D>0-without-fire never" are window-16/vmax-2 family descriptors, not laws — my vmax-8 fire (viol 48) and window-32 arms refute them as generalities while confirming the actual invariants (fire ⇒ D = violation; realized non-fatal ⇒ m = 0; closures coincide). Also fixed the armed-share range (85–99%, not 89–99%).

Gold because: reproduced twice, held-out predictions held, and it deletes a component — the window Monte Carlo the engine fix's validation would have needed is now a per-draw state read (`armed ≤ 0 ∧ D ≤ 0 ∧ out = ∅`), adoptable in one step with zero engine changes. The remaining open item is correctly named: the geometry derivation of why `alone_at` and `certify` pin the same tick.
