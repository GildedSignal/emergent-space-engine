# The read census: what reads the body store at burn, and at what rate

## Claim

On shipped code the engine's read demand is **O(1) in N** on the ladder's flights (absolute
read counts identical at N=1e4 and 1e5), the player's scan reads a bounded near set (~70
candidates a scan — the radial apsidal filter cuts the belt), and the only N-linear reads
ride the kick cadence at **2.9–4.3 reads an event** — so the compact store's 10⁹ read bill
is the kicks' own mint reads (the ladder's break 1, kick-cadence's territory), not an
observer read stream, and the dwell cliff's hot set is a ~70-body near set that a pin
deletes.

## Bottleneck

Memory at 10⁹ (the board's fourth), via the promotion page's open direction 1: the second
author (8792) priced "the read stream" at 5.74×10⁷ reads/s at 10⁹ rtf 100 (b = 11.48
reads/body/20k gs, N-linear) and asked what the re-reads are FOR. This census answers on
shipped main: **no N-linear observer exists**; the premise "burn-10⁹ memory = the read
stream's question" dies as stated, and with it the "~6 cores of pure hit-path ε". What
remains at 10⁹: ~7×10⁶ event-riding reads/s wall (≈0.7 core at the measured 67–129
ns/read) — a term of the kick bill, deletable only by the cadence — plus a bounded hot set.
Orders of magnitude, x86 cloud; the M1 re-measures.

## Evidence

Instrument: `prof::reads` (this run's patch; counters only, feature `prof`, no behaviour
change — plain and prof binaries print the same flight digest, `d1822b88…`), example
`read_census` = the ladder's flight (plane_extra, seed 1, 1 thread, rtf 100, 12 ms budget,
L8 burn from 1 s, counters from 1 s; the `digest` rec row and the build's settle reads are
instrument artifacts, excluded from every statement). Commands: `bash
lab/results/20261017-0428-quant-c439/regen.sh` (~25 s of runs after two ~12 s builds;
every number below is in its output).

| arm | total binding_at | scan cand (reads/scan) | scans | state_of | raw | rec/event | events | reads/event |
|---|---|---|---|---|---|---|---|---|
| burn 1e4, 20 s | 188,181 | 148,996 (70.0) | 2,127 | 14,164 | 22,890 | 0.56 | 16,204 | 2.85 |
| **burn 1e5, 20 s** | 188,227 | **148,996 (70.0)** | 2,127 | 14,164 | 22,939 | 0.56 | 16,196 | 2.85 |
| coast 1e4, 20 s | 64,935 | 33,875 (184.1) | 184 | 10,828 | 20,048 | 0.63 | 11,115 | 3.41 |
| coast 1e5, 20 s | 64,935 | 33,875 (184.1) | 184 | 10,828 | 20,048 | 0.63 | 11,115 | 3.41 |
| burn 1e4, 150 s (wave) | 375,361 | 152,232 (60.6) | 2,511 | 102,454 | 118,160 | 0.89 | 65,153 | 4.28 |

The identity across N (every reader's absolute count equal to 0.03%; only root_state_raw
drifts 49 counts with wall jitter) is the result. Readers that are none of the above are
noise (ext::source 3, handoffs 1, misses 0 everywhere; history hits 0.06% burn, 4.3% coast).
Hit-path price on this box (warm, one pass over all bodies): binding_at 67–129 ns (a 192 B
`Binding` clone), rec 114–167 ns (464 B). Machine: 8 vCPU, load 1.3–2.3, 13 GB free.

The reconciliation with 8792's b = 11.48: their window (20k gs, burn, dwell dial) holds the
wave (1 kick/body) plus the steady cadence (128/88 d ≈ 2.9 kicks/body) ≈ 3.9 kicks/body ×
~4.3 reads/kick ≈ 16.8 — their 11.48 sits between that and the locals-only pre-wave rate;
their reads are the kicks' own (mint-path) reads, which an N-linear counter records exactly
when the retention layer counts a mint as a read. The engine's observers never scale with N
on these flights.

## Predictions

Written before the arms (`predictions.md`): P1 held (scan 79% of burn reads) but its 10×
coast magnitude was wrong (2.9×); **P2 refuted by its own kill criterion** (reads/scan 70.0
at both N — the filter cuts); P3 held (4.28 reads/event through the wave); P4 held (misses
0); P6 held (digest identity plain=prof). The refutation is the result, not a loss: the
falsifiable side was pre-registered.

## What would make it wrong

A scene where `radial::candidates` returns None (most of the doll inside the window) — a
flight into the belt at density, the player-seam question (ladder break 3, encounters page),
not measured here; the page's per-frame view gather (O(N) reads, outside the engine,
unchanged by this census); and any retention/demotion layer of its own (unmerged patches)
whose sweeps read per body — on main none exists. One box, 1 thread, seed 1: counts are
deterministic, prices are x86 orders of magnitude.

## Cost of adoption, fit with PRINCIPLES

None: the patch is counters behind the `prof` feature (the shipped engine verbatim without
it, digest-proven); the example is a new file. "Compute only surprises" — the census shows
the engine already reads only surprises plus a bounded near set; the read stream as a 10⁹
question was double-counting the kick bill ("the cheapest compute is compute not done").
The named deletions: the dwell cliff's hot set (pin ~70 bodies live at any scale) and the
attribution error itself (the read row leaves the 10⁹ memory ledger; the cadence and the
bytes/body keep it).

## The lens

Quant counted events and priced the clone, but read no tails (no p99 of read latency under
load; reads sit on the frame path through capture), priced the mint behind a miss from
c4d3's 9.2 µs instead of re-measuring, and flew one seed at one population program — the
near set's size is a property of the ladder's spread belt, and a formation (co-orbital
concentration, the encounters gold) would swell it.
