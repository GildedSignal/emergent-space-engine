# Autoresearch log — chronon CPU reference, ns per body-chronon

Protocol: `taskset -c 4 chronon-bench 200000 32 0.1 256 2718281828 5`, median of 5
(linux x86 shared runner, 8 vCPU, load 1-2; orders of magnitude only, relative gains are the signal).
Behaviour lock: `World::digest` + `Log::digest` == baseline `af1ddc8f…|81428e3f…` every round.

| round | hypothesis | change | ns/body-chronon | verdict |
|---|---|---|---|---|
| 0 | — | baseline (pristine main) | 771 (min 763) | — |
| 1 | H1: SipHash dominates the ~2.4M map ops per chronon | multiply-xor hasher (`FastKey`) on `ranges`, `consumed`, `local` | **542** (min 535) | **KEPT (1.42×)** |
| 2 | H2: sort + `ranges` map dominate; open-addressed scatter table (epoch-cleared, reused buffers) removes both | 512k-slot table, packed keys, count/prefix/scatter | 686 | REVERTED (0.79×: 14 MB random-probe footprint loses to near-linear pdqsort on nearly-sorted keys + hashbrown SSE iteration) |
| 2b | H2a: hashbrown load ~0.87 makes miss probes expensive | `with_capacity(2n)` | 551 | REVERTED (noise; misses are cache-bound, not probe-bound) |
| 2c | H2b: most of the 1.8M neighbour lookups/chronon are misses; a 512 KiB 2-bit Bloom filter skips them in L2 | occupied-cell bitset gate before `ranges.get` | 641 | REVERTED (0.85×: two random bit-loads + re-mix cost more than hashbrown's one SIMD group probe) |

Stop rule: three consecutive rounds under 10% → stopped after H2b.

Fine section profile of the H1 build (h=16, instrumented copy, reverted):
pair loop 77% (1.8M `ranges.get` + 6.2M `consumed.get` + `hit`), kmax+order+sort 13%,
ranges build 4%, advance+walls 3.4%, respond 1.8%, retain ~0. The remaining cost is
cache misses on the bodies array and the map, not arithmetic.

## Held-out set (run once at the end; never tuned on; digests equal in all 8)
| config | baseline | final | speedup |
|---|---|---|---|
| n=50k | 652.2 | 308.1 | 2.12× |
| n=400k | 819.4 | 553.6 | 1.48× |
| fill 0.05 | 566.6 | 318.2 | 1.78× |
| fill 0.2 | 1308.3 | 930.1 | 1.41× |
| vmax 64 | 517.3 | 315.6 | 1.64× |
| vmax 512 | 1005.3 | 710.8 | 1.41× |
| RelativisticV1 | 626.7 | 585.9 | 1.07× |
| seed 31415926 | 730.9 | 572.9 | 1.28× |

Final gates on the shipped configuration: `lattice-check` 3/3 EQUAL,
`lattice-check-rel` 4/4 EQUAL (independent all-pairs integer reference).
