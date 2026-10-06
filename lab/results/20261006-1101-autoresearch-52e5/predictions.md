# Predictions — run 20261006-1101-autoresearch-52e5 (autoresearch lens)

Artifact: `crates/lattice` CPU chronon reference (`chronon.rs::step`), the reference every
mode must reproduce bit for bit. Metric: **ns per body-chronon** (board bottleneck 3,
"cheaper events"; also speeds every future verification run — iteration speed, P10).

Tuning config (all loop decisions made only on this): `chronon-bench 200000 32 0.1 256 2718281828 3` (median of 3).
Behaviour lock: `World::digest` + `Log::digest` identical to baseline for every config, plus
`cargo run --release -p xtask -- lattice-check` (independent all-pairs reference) at the end.

Baseline (this machine, load ~1.7/8): **725 ns/body-chronon** (h=16 probe).
Section profile: detect phase (ranges HashMap + neighbour loop + consumed lookups) 92.7%,
order sort 9.7%, advance+walls 2.4%, respond 1.5%.

## Hypotheses, in attack order
- H1 (cheap hasher): replacing SipHash on `ranges`/`consumed` with a multiply-xor hasher
  keeps digests identical (outputs are already hash-order independent: `pairs` is re-sorted
  canonically; `consumed` is only get/insert/retain) and cuts the detect phase.
  Prediction: ≥ 1.4× overall (detect is ~93% and hashing is most of it).
- H2 (flat scatter table): replacing sort + `ranges` HashMap with one open-addressed
  (key → slot) table built by count+prefix+scatter over reused buffers removes the O(n log n)
  sort and makes neighbour probes ~1 cache line. Prediction: combined with H1, ≥ 2.5× overall.
- H3 (buffer reuse): per-chronon `Vec` allocations (`order`, `pairs`) moved into `self`.
  Prediction: 3-8% at n=200k (bigger at 1M).
- H4 (single-pass kmax): fold the kmax scan into the advance loop of the previous chronon.
  Prediction: ≤ 3%; will try only if rounds remain.

Stop rule: three consecutive rounds < 10% gain.

## Held-out set (run once at the end, never tuned on)
- n = 50_000 and n = 400_000 (fill 0.1, vmax 256)
- fill = 0.05 and fill = 0.2 (n = 200_000, vmax 256)
- vmax = 64 and vmax = 512 (n = 200_000, fill 0.1)
- law = RelativisticV1 (n = 100_000, fill 0.1, vmax 256)
- seed = 31415926 (n = 200_000, fill 0.1, vmax 256)

Predictions on held-out:
- P1: gains hold across n (within ±30% of the tuning-config speedup ratio); the mechanisms
  (hash cost, sort) are per-body, not per-n. At fill 0.2 the predicate count per body roughly
  doubles, so the *ratio* shrinks somewhat (more time in `hit`, which I do not change).
- P2: at vmax 512 the cell grows (2·kmax term), cells per body rise, range lookups per body
  rise → ratio should hold or improve (more lookups to save).
- P3: digests identical to baseline on every held-out config (this is the behaviour lock; a
  single mismatch kills the configuration, not the method).
- P4: relv1 changes only `respond`, which is 1.5% of time → ratio unchanged within noise.

## Blind spot (stated up front)
Local search on the reference's machinery may miss the structural winner: detect cost is
~2 predicate tests + ~9 cell probes per body per chronon *because the cell is sized by the
worst kmax*. A per-body reach tier (bodies binned by their own reach+k) or an event-sorted
frontier (the event mode's approach) would restructure the work, not just cheapen it —
out of scope here (law semantics must stay fixed), named as the structural alternative.
