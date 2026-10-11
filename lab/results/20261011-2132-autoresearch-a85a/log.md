# autoresearch log — artifact: crates/encounters (r8 v3 Binet-cone method), metric: us_per_kick (n=10k belt, 100 kicks, horizon 1000 orbits)
# behaviours held fixed: verify sets a/b/c/d/long zero missed encounters, same events as truth; kick event lists unchanged.

baseline: us_per_kick 7712/7824/7936/7553 (eps 1e-9..1e-3), us_per_pair 9.49; setup_frac 0.83; numeric_window = 1187 windows, 34.7 sweeps each, 1148 evals each = ~80% of setup evals; 78% of sweeps sample d<3rho (near-miss shelf crawl; Lipschitz steps ~rho/vmax are structural).

R1 hypothesis: j's states on the fixed tau-grid are recomputed identically in every sweep of a numeric window -> cache them once (plus mi/mj means).
R1 change: numeric_window precomputes js[33] + (mi,mj); d_of_s -> d_of_s_cached (i's states only; full-f fallback kept for refine).
R1 metric: us_per_kick 5736 (-25.6%), us_per_pair 7.06; pairs_with_proposals 3972, identical to baseline. KEEP.

R2 hypothesis: the tau-grid (k=32) over j's arc crossing over-resolves the minimum; the sign-change refine is the real min-finder, so k=16 halves per-sweep cost at unchanged behaviour.
R2 change: k=32 -> 16 in numeric_window. Metric: us_per_kick 4502 (-21.5% vs R1; cumulative -41.6%). Gate: ALL shipped verify sets (a,b,c,d,long: 14 belts) missed=0 false=0. KEEP.

R3 hypothesis (edge probe): k=8.
R3 metric: us_per_kick 4067 (-9.7% vs k=16, below the 10% round bar) though all shipped sets still pass. REVERT to k=16 (thinner margin on unseen long arcs not worth a sub-10% gain).

Held-out (predictions written first, see predictions.md): set e (3 fresh belts, sigma 5e-2 / rho 1e-3 / coorbital w 1e-4 unseen) + kick at rho=1e-3, both against a byte-clean baseline binary.
- P1 held: missed=0 false=0 dup=0 on all three.
- P3 held: event lists, checks, hits, sections, queries, qsteps IDENTICAL to baseline; evals 0.578x/0.610x/0.655x; method_s 0.61x/0.30x/0.38x.
- P2 WRONG in the conservative direction: predicted 12-30% gain at rho=1e-3, measured 2.08x (41,455 -> 19,901 us/kick). Bigger rho widens eps_u, more arcs fall to the numeric-window path, so windows carry MORE of the kick there, and the change bites harder.
- P4 not run (k=8 was already reverted; edge claim left untested on set e).

Stopped: last round (k=8) < 10%.
