# Run logs (console outputs; each section is one full execution of news_scale.py)

## v1 — first decisive run (routing: circumscribed radius >= r_q; disk-exclusion flush)
```
== analytic (q=0.01) ==
N=    1000 naive/body=   1000.0 gated/body=   6.33 (4 lvls) inflight naive/body=   29.74 gated/body=83.3493
N=   10000 naive/body=  10000.0 gated/body=   9.50 (6 lvls) inflight naive/body=   94.03 gated/body=264.5428
N=  100000 naive/body= 100000.0 gated/body=  12.66 (8 lvls) inflight naive/body=  297.35 gated/body=836.7492
N= 1000000 naive/body=1000000.0 gated/body=  14.25 (9 lvls) inflight naive/body=   940.32 gated/body=2646.0637
fits: {'naive_del_exp': 1.0, 'naive_inflight_exp': 0.5, 'gated_del_exp': 0.1181, 'gated_inflight_exp': 0.5005, 'ratio_1e6': 70195.1041}
fleet: {'K': 10000.0, 'N': 1000000.0, 'naive': 10000000000.0, 'gated': 675366.3, 'ratio': 14806.78}

== MC s32_q1: 16384 bodies, 98251 events, 6 levels ==
 per body/time: direct=34.83 flush=21.14 writes=2.41 emissions=0.416
 bursts: med=0.00 p99=0.00 max=1427792.00   <-- BURST INSTRUMENT BROKEN (np.add.at row bug), fixed in v2
  t=2 gated err: max=0.0294 med=0.00411 (q=0.01)
  t=4 gated err: max=0.953  med=0.0251   (q=0.01)
  t=6 gated err: max=2.32   med=0.0527   (q=0.01)   <-- boundary double-count, compounding
  t=6 DROP err: max=0.147  med=0.0496

== MC s16_q1: 4096 bodies, 24629 events, 5 levels ==
  t=6 gated err: max=1.26 med=0.0635 ;  t=6 DROP err: max=0.153 med=0.0558

== MC s32_q1f (q=0.001): 16384 bodies, 97870 events ==
 per body/time: direct=337.59 flush=148.03 writes=2.55 emissions=0.565
  t=6 gated err: max=0.072 med=0.00344 ;  t=6 DROP err: max=0.0108 med=0.0033
```
(The analytic in-flight column in v1 used the wrong lifetime model — 2646 words/body at 10⁶ —
disproven by the MC emission counter; corrected from v2 on.)

## v2 — ring-inscribed routing + exact square-complement flush; burst instrument fixed
```
== analytic (q=0.01) ==
N=    1000 naive/body=   1000.0 gated/body=   40.10 (4 lvls) inflight naive/body=   29.74 gated/body= 8.9305
N=   10000 naive/body=  10000.0 gated/body=   43.27 (6 lvls) inflight naive/body=   94.03 gated/body= 9.3770
N=  100000 naive/body= 100000.0 gated/body=   46.43 (8 lvls) inflight naive/body=  297.35 gated/body= 9.4887
N= 1000000 naive/body=1000000.0 gated/body=   48.01 (9 lvls) inflight naive/body=   940.32 gated/body= 9.5073
fits: {'naive_del_exp': 1.0, 'naive_inflight_exp': 0.5, 'gated_del_exp': 0.0265, 'gated_inflight_exp': 0.0087, 'ratio_1e6': 20827.1188}
fleet: ratio 14806.78

== MC s32_q1: 16384 bodies, 98251 events, 6 levels ==
 per body/time: direct=34.83 flush=18.58 writes=2.04 emissions=0.039
 bursts: med=17.00 p99=24.50 max=28.50 (ratio 1.4)
  t=2 gated err: max=0.0294 med=0.00411
  t=4 gated err: max=0.0722 med=0.0244
  t=6 gated err: max=0.238  med=0.0494   <-- interior receivers unserved: drop-like growth
  t=6 DROP err: max=0.147 med=0.0496

== MC s16_q1: 4096 bodies ==
  t=6 gated err = DROP err exactly: max=0.153 med=0.0558

== MC s32_q1f (q=0.001): direct=337.59 flush=46.71; bursts ratio 1.3
  t=6 gated err: max=0.0108 med=0.00333 = DROP (max=0.0108)
```

## v3 — v2 + leaf member-residue accumulator (member quantum q*d_near^2)
```
== MC s32_q1: 16384 bodies, 98251 events, 6 levels ==
 per body/time: direct=34.83 flush=53.12 writes=2.04 emissions=1.023
 bursts: med=33.33 p99=49.17 max=61.50 (ratio 1.5)
  t=2 gated err: max=358  med=0.00427   <-- member flush double-counts ring-covered receivers
  t=4 gated err: max=373  med=0.0253
  t=6 gated err: max=377  med=0.0527    (persistent offset, not growing after t=2)
  t=6 DROP err: max=0.147 med=0.0496

== MC s32_q1f (q=0.001): direct=338.99 flush=385.88; bursts ratio 1.3
  t=4 gated err: max=1.42e+04 med=0.00113 ; t=6: max=1.42e+04
  t=6 DROP err: max=0.0141 med=0.00381
```
Raw JSON: v2/v3 in out/results.json (v3, final code state), v2 configs in out/results-v2.json.
