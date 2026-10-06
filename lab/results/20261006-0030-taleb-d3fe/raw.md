# Raw measurements (this run, 6 October; Linux, 8 vCPU, shared; release build at /home/glmlab/lab-target-3/release/xtask)

All bench runs: `--seconds 8 --unpaced --threads 1` unless noted. RSS = `/usr/bin/time -v` Maximum resident set.

## The law (seed 3, members 48; game time = rtf x 8 s)
| rtf | game-s | RSS MB | kicks | opens | boundaries | slices | bodies | B/body |
|---|---|---|---|---|---|---|---|---|
| 1e4 | 8e4 | 31 | 17,195 | 649 | 13,743 | 65,680 | 74 | 9,147 |
| 2e4 | 1.6e5 | 70 | 17,049 | 646 | 13,601 | 69,360 | 74 | 9,125 |
| 4e4 | 3.2e5 | 142 | 16,916 | 635 | 12,598 | 63,826 | 74 | 8,733 |
| 8e4 | 6.4e5 | 279 (349 in an earlier identical run: 25% run-to-run spread) | 17,062 | 646 | 13,617 | 67,916 | 74 | 9,094 |

Slope ~443 B per game-second with 2 surviving members (leavers 46, dissolved 0). Every canonical event counter is flat
while memory grows 9x. Wall 4.1 s -> 28.3 s over the same sweep with frame CPU flat (p50 5.9 ms, p99 6.7 ms): the growth
is in the settle-to-cut path, not the frames.

## Controls and discriminators
- members 16, rtf 4e4: RSS 19 MB, leavers 16, **dissolved 1** -> flat. The doll/universe path itself does not accumulate.
- members 96, rtf 2e4: RSS 104 MB, leavers 93, dissolved 0 (3 survive) -> ~181 B per surviving member per game-s.
- members 48, rtf 8e4, seeds 4/5: RSS 101 / 211 MB (seed 3: 279). Same config, 2.8x spread; seeds 4 and 5 dissolved (leavers 48),
  their peak is what accrued while the battle lived.
- members 4, rtf 8e4: RSS 17-18 MB (stats output unreliable in one run; not leaned on).

## Determinism (P-A)
- Two processes, seed 3, threads 1: digest 21f483f5... identical, cut_tick 1015127 identical.
- threads 4: identical. Seed 4 control: 76d8b3f9... differs. PASS with working controls.

## Pre-contact cost scaling (rtf 1, seconds 8, seed 3; the default bench regime)
| members | cpu_p50 ms | cpu_p99 ms | fleet us/item | fleet total ms |
|---|---|---|---|---|
| 48 | 0.47 | 0.62 | 9.7 | 4.66 |
| 96 | 0.62 | 0.74 | 15.2 | 7.30 |
| 192 | 0.96 | 1.06 | 21.7 | 10.41 |
| 384 | 1.61 | 2.02 | 32.0 | 15.36 |
| 400 (asked 768/1536/3072) | 1.65 | 1.87-1.96 | 34.5-35.2 | 16.6-16.9 |

`--members` clamps to [4,400] silently; 768/1536/3072 were all 400 (identical digests). Exponent of fleet cost ~ n^0.6.
In 8 s at rtf 1 no contact ever happens (kicks 0): the default bench never sees the battle fight.

## Contact regime reached (rtf >= 10)
rtf 10/100/1000 at seconds 4, members 48: kicks 6/353/1439, encounters 3/39/100, leavers 8/43/44; p99 == p99.9 == worst
~6-7 ms: one class of tail frames (contact/kick frames), ~10x the p50.
