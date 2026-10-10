# Raw outputs — run 20261010-0656-quant-d540

Machine: the lab's Linux box (8 vCPU x86, 15 GB, shared; load printed by the bench). Binary:
`cargo run -p emergent-universe --release --offline --example nwall` (source:
`crates/universe/examples/nwall.rs`, copied here as `nwall.rs`; run.sh saves it as the run's
patch). The `find us` column is the mean of 3 calls (the header says p50 — 3 samples, the
difference is noise). First-sweep numbers (S1) ran at load 3.46 with other jobs; every S1 point
re-measured isolated at load ~2.2 reproduced within 1.3× except 10⁴ (3×: 7276 → 2262 µs), so
the isolated numbers are the record and S1 is kept for honesty.

## S1 — first sweep (load 3.46, pessimistic)

    $ cargo run -p emergent-universe --release --offline --example nwall -- 100,1000,10000,100000 100 2654435761 3
    | n | frame us p50/p99/max | sched-only us p50 | rekey us p50 | events | find us (hits) | build s |
    | 100 | 28/41/63 | 28 | 6 | 0 | 247 (0) | 0.0 |
    | 1000 | 359/376/388 | 354 | 61 | 0 | 2666 (1) | 0.0 |
    | 10000 | 7276/8518/9194 | 7202 | 584 | 0 | 17427 (11) | 0.2 |
    | 100000 | 68061/105373/106224 | 68192 | 12437 | 0 | 192999 (90) | 1.4 |

## S2 — fresh layout (stride 40503), load 2.19 — the reproduction control

    $ ... --example nwall -- 100,10000,100000 100 40503 2
    | 100 | 14/24/28 | 14 | 3 | 0 | 146 (0) | 0.0 |
    | 10000 | 2236/3644/3683 | 2217 | 341 | 0 | 16346 (3) | 0.1 |
    | 100000 | 55019/60597/62878 | 53776 | 6961 | 0 | 161353 (99) | 1.0 |

## S3 — rtf independence (same layout as S1, rtf 1 vs 100)

    $ ... --example nwall -- 10000 1 2654435761 2
    | 10000 | 2251/2519/2714 | 2291 | 360 | 0 | 34011 (0) | 0.1 |

    $ ... --example nwall -- 10000 100 2654435761 3   (isolated rerun of S1's point)
    | 10000 | 2262/2570/2905 | 2262 | 361 | 0 | 16194 (11) | 0.1 |

## S4 — the far end, with peak RSS (load ~2.2; 63 s, the one command over 60 s)

    $ /usr/bin/time -v /home/glmlab/lab-target-2/release/examples/nwall 300000,1000000 100 2654435761 0.3
    | 300000 | 193578/217480/217480 | 193203 | 31619 | 0 | 885923 (278) | 3.1 |
    | 1000000 | 721515/862304/862304 | 795481 | 117868 | 0 | 3010890 (842) | 10.4 |
    Maximum resident set size (kbytes): 1930272

## Control — frames never change outcomes (both budgets, one settled horizon)

    $ ... --example nwall -- control
    control: events settled 1674, digests 4c390dfb…c70a 4c390dfb…c70a (EQUAL)

Events column: total events resolved during the whole frame run (3 s at 60 Hz × rtf); 0 at
every N: belt-like cadence, the universe does nothing between frames. `perf stat` is blocked on
this host (perf_event_paranoid 4), so per-event cache-line counts are arithmetic from the op
counts, not measured.
