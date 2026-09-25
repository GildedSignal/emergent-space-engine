# C1 diagnosis — 25 September 2026

Before the fixes, the 64-body packed stop cascade (C1 rung 0) depended on the slice budget
(`xtask ladder-rung C1-budgets 64`, single release runs):

| Slice budget | Contacts | Matches the independent audit |
|---|---|---|
| 1,000,000,000 | 446 | no (audit 865) |
| 100,000 | 446 | no (audit 865) |
| 1,000 | 431 | no (audit 595) |
| 64 | 363 | no (audit 427) |
| 8 | 897 | no (audit 900) |

Two engine faults, reproduced with the temporary examples kept here (they were run from
`crates/engine/examples/` and removed afterwards):

1. `zz_repro_stop.rs`: a stop applied to a body already at rest opened a new trajectory revision,
   re-arming contacts with every overlapping resting neighbour, so three motionless bodies produced
   28 contacts and 28 segments in 40 ticks at every budget.
2. `zz_repro_c1.rs 47 55`: body 55 stops in tick 15 and body 47 reaches it in tick 17. With incremental
   repair the next queued batch committed before 55's repair ran (and a later repair overwrote it), so
   the contact came at tick 18 (large budgets) or not until tick 29 (budget 8). With
   `incremental_sap = false` the engine agreed with the audit at every budget.

After both fixes every budget gives digest `c617cad640d0…` and 30 contacts equal to the audit.
Regression tests: `crates/engine/tests/contact_cascade.rs`; disabling either fix fails its test.
