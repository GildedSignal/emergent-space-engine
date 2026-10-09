| Term | value |
|---|---|
| M1/x86 factor (frozen M1 anchor 4345.4 us / this run 8071.9 us) | 0.61 |
| pairs/kick law check: a4/g5w/g5W/g6w/g6W/g6Wd measured vs 0.0346*n*(1+X)/(2(X-1)) | 866~865 / 8284~8650 / 1975~1977 / 86332~86500 / 18704~17532 / 20926~19771 |
| 1e7 case | not run to completion (>300 s/kick, loaded runner); law extrapolates 1.7e5 pairs/kick |
| cells soundness (exact candidate-set equality vs global, kicks with mismatches) | 30 kicks, 0 mismatches |
| kick arithmetic (incremental + 0.05 compiles/kick) | 4.89e-05 cores |
| cascade per CELL of n=1e+04, two-tier, no skin (M1-implied) | 0.966 cores |
| cascade per cell, + slack skin 12.6x | 0.0767 cores |
| cascade per cell, phase-neighbour rank-4 | 4.75e-03 cores |
| local cell index: per-pair gain at equal geometry (n=1e6, X=150: 8.68 -> 3.95 us x86) | 2.20x -> skin cascade 0.0349 cores |
| SINGLE BELT at 1e9, X=1.5 (law 8.66e7 pairs/kick): cascade | 1.0e+05 cores |
| SINGLE BELT at 1e9, wide (law 1.75e7 pairs/kick): cascade | 2.1e+04 cores |
| cascade per cell, UNAVERAGED k=32, +skin / no skin | 8.76 / 110 cores |
| event queue, WINDOW-level keys, no skin (813 pop+push/kick @ 176 ns) | 0.0318 cores |
| event queue, window-level, with skin | 0.0017 cores |
| event queue, CELL-level keys (7.2 updates/kick) | 2.82e-04 cores |
| queue memory: per-body keys / cell keys (1 per 128-body block) | 12.0 GB (>8) / 94 MB |
| queue depth at cell keys (1e5 cells) / window keys (per pair) | 1e+05 / 4.3e+16 windows (does not fit; even cell-partitioned: 4.3e+11 x 12 B = 5190.0 GB) |
| encounter handling (0.04/body/orbit, corrected) | 3.17e-05 cores |
| program memory | 15.8 MB |
| scars at live fraction 1% (24 B each) | 0.24 GB |
| scars at live fraction 10% (24 B each) | 2.40 GB |
| scars at live fraction 33% (24 B each) | 7.92 GB |
| global U-index, shipped Sorted layout (16 B/body) | 16.0 GB  (> 8 GB — cell-local indexes, built on demand, 0.07 s per 1e6 measured) |
| scar creation vs reabsorption | 222/s vs 5.7e+06/s/core (3e+04x slack) |
| max rtf on 4 cores: averaged + skin | 5,216 |
| max rtf on 4 cores: averaged, no skin | 414 |
| max rtf on 4 cores: averaged + phase-neighbour | 84,125 |
| re-derivation of board's '190 cores' (k=32, no skin, rtf 100, per cell) | 110 cores |
