NOT MERGEABLE: F1 still has lag, and one existing suite test exceeds 60 s.
Scope: wt/burst2, origin/main merged at baed04e7; no merge to main and no authored HANDOFF/lab edits.
Before = first-pass centred law at burst2 start; earlier speed-fraction-law measurements remain in T1's header.
T1: 6/9 -> 9/9 PASS; original law worst readable error 1.84%, first pass/final 0.0755%; final total 44.69 s, longest 10.511 s.
Only scene amendment: reverse L0 burns 0.02*v0/a; all numerical criteria unchanged, coarse control still fails.
Convergence cause: refinement regrew the SAME 20.659 s interval at burn t=100 s; subdividing the ramp fixes this.
Other probes: L4 no handoff; removing tides changed position by 0.0113 root units; unpaid estimate sum 10.3 us; residual drift 1.09e-4 root units. See account-and-root/reference/oracle/refit-before.
Root burn gravity separately used up to 518 times its interval (raw excess 1.31e-7 c at L8); now it pays the actual capped interval.
HUD warning FAIL -> PASS: planner/view judge the exact reconciled-cut course; test independently cuts through step::decide, retaining original assertions.
Bind-once selects the old word from fit_key; independent compile-first comparison covers >300 fits, coarsening included; coast digest unchanged.
Suite: 301 PASS / 10 FAIL / 16 ignored -> 314 PASS / 0 FAIL / 16 ignored; C1, P1/P2, throttle, recorder all pass before/after.
Runtime constraint remains FAIL: existing belt controls/plants test 61.385 s; all other tests <60 s. Full per-test timings in test-times-final.json.
F1 (100x,20 s): 5/36 -> 33/36 pass; 8 -> 0 late frames, 0 -> 0 refusals, worst frame 45.07 -> 11.83 ms, worst lag 1.667 -> 1.604 s.
Held L0-15 all pass after; remaining lags: coast .256 s, throttle sweep 1.604 s, key mashing 1.115 s. Every flight before/after: f1-comparison.txt.
Demand kicks/frame L8/L12/L15: original 19/124/291 -> first-pass 9/21/31 -> final 9/21/31; final demand worst 7.40/8.05/11.96 ms.
B13: 60/64 FAIL -> 60/64 FAIL, same worst dE/dL .0212; meets the frozen nonregression requirement.
Replay-all: 3 changed / 0 regressions -> 3 changed / 0 regressions; eight scripted flights also agree across all four schedules.
Remaining bottleneck: throttle demand frame 510 costs 69.79 ms for 103 player kicks (100 fine gravity kicks); keymash frame 132 costs 16.64 ms for 15 whole burn kicks.
Rejected fine-ledger/outbound-impact experiment: lag still 1.544/1.115 s at throttle/keymash; saved patch/unit/probe evidence, removed entirely. Final sources exactly match the previously fully tested pre-fine-ledger.patch.
Timing provenance: M1, AC, 100%, no thermal warnings, swap 4.46 GB; machine JSON retained. Baseline/final load differs; no attribution of the entire timing delta to code.
