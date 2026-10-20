# Dossier — 20261020-1116-scout-df8e (scout)

**Claim.** The belt's standing comb is not phased by the fictitious clock's `dt_carry`: a
golden-ratio carry (and a full half-gap common carry) injected at `Ext` creation changes the
law's bits but leaves the comb unmoved to the bin — so the stagger the board wants must move
the body's plan anchor (the mint tick), where d5c3 already priced the bill, and the offset
VALUES should be golden-ratio (the deterministic jitter), not random.

**Bottleneck.** The furthest-gap item: bodies in the flyable engine, 28 vs 10⁹. The comb's
freeze channel is the crest (0a46: 718/42/339/12 ms alternating eras; this run: 877/530/600).
Deleting the crest deletes every era's mega-frame at zero per-frame cost; the 3× served-path
split (47 vs 12-17 µs/event) is then the only wave cost left.

**Prior art (the lens).** The comb is the thundering herd / critical instant: synchronized
release of periodic tasks (Liu & Layland 1973), cured everywhere by offset assignment —
Tindell/Audsley offset scheduling in automotive AUTOSAR, jitter in cron/DNS/TCP retries
(random: illegal here — floats may explore, only integers decide, and the player is the only
seed). The legal deterministic equivalent is Knuth's Fibonacci/golden-ratio hash (TAOCP 3,
6.4): frac(i·φ) is the optimally even spread (three-distance theorem, Sós), costs one u128
multiply at birth and zero stored bits — against 32 bits/body of stored random phases
(~4 GB at 10⁹, dead on arrival against the 0.126 bits/body belt program). UNVERIFIED at the
source: the Tindell/Audsley line and the AUTOSAR tooling claim (known from the scheduling
literature; not re-read this run). Liu & Layland and Knuth are textbook-solid.

**Evidence** (this Linux box, 8 shared cores, load recorded in run.log; orders of magnitude
only). Shipped tree + work/patch.diff (env-gated, off = shipped bits; `nladder` also needed a
`/proc` stand-in for the macOS `proc_pid_rusage` footprint probe, disclosed in the patch).
Scene: the record's — `nladder 100000 burn 26 2000 12`, seed 1, 12 ms budget. Three arms:

| arm | worst ms | crest bin (1.5k gs) | peak/mean | era worsts (ms) | events tot |
|---|---|---|---|---|---|
| OFF (shipped) | 876.9 | 14,250 gs | 7.33 | 402/877/530/600 | 441,626 |
| ON golden carry | 822.5 | **14,250 gs** | 7.61 | 327/823/525/594 | 448,640 |
| ON half-gap carry | 857.1 | **14,250 gs** | 7.61 | 384/857/445/612 | 452,980 |

P1 held (the anchor reproduces the record family: worst ~0.9 s at 1e5, crest events/frame
p99 ~7.3k, max 17.4k, three standing eras, busiest-29% share 0.75-0.77 — 0a46's standing
comb, independently, at a third cadence and OS). P2's kill bar fired: the golden spread did
NOT flatten the crest, and the discriminator (every body offset by the same half gap — the
largest common translate the channel can carry) did not move the crest by even one 1,500-gs
bin. The arms are NOT identical (event totals ±1.6%, worst-frame indices 582-587 vs 476-483,
lost ships 11/9/9): the carry is live and law-visible, but the belt's comb channel does not
read it. P3 held (events/body/era equal ±2% across arms: a phase move, not a rate move). P6
not flown (time; the on/on determinism replicate is in regen.sh).

**Mechanism reading (code + measurement).** The belt's clock stream is planned by
`plan_clock` (step.rs:626): each plan sets `anchor = t` and `interval = 2·half` with items at
`t+half` (kick, middle) and `t+2·half` (boundary) — the stream's phase is the body's plan
chain origin, i.e. its first plan tick (the mint), not the carry. The injected `dt_carry`
perturbs `half` at creation (clamped paths repay it within the first interval) without
translating the item chain. Two candidate mint-synchrony anchors follow: the bodies' first
plan ticks at scene build, or (if belt ships start as pure tubes, step.rs:549-552) the first
pull that observes them — cc9d's `pull_ships`. Distinguishing those is the named next
experiment; both are per-body anchor questions, and both are exactly where birth-stagger's
d5c3 measured a one-time, unbiased ~3×-band element bill for shifting the per-body kick grid.
The combined sentence for adoption: **stagger = golden-ratio offsets on the per-body plan
anchor, minted at birth from the ordinal (one multiply, zero stored bits); the carry is not
a stagger channel.**

**What would make it wrong.** The anchor arm is one box (shared, loaded), one seed, one
rung, three eras — but it reproduced the record family, and the kill is a null result
against a positive prediction (the crest had to move under a half-gap translate; it did
not). The mechanism reading (anchor vs pull) is code-derived, not yet instrumented; if the
comb is the pull channel, the stagger target changes from plan anchors to pull scheduling.
Memory: arms peaked 1.9-2.0 GB (VmRSS stand-in), at the cap, disclosed.

**Fit with PRINCIPLES.** "Store the generator, not the generated" (P6): the phase rule is
computed from the ordinal, not stored. "There's no continuum… physics loves e while we love
2" (P16): the golden ratio is the one irrational a dyadic machine should keep, because it is
what keeps 10⁹ dyadic clocks from re-locking. "A failed experiment kills that configuration,
never the method" (P9): the killed configuration is the carry injection; the method
(deterministic offsets) stands, re-aimed.

**Commands.** `bash lab/results/20261020-1116-scout-df8e/regen.sh` (build + 5 flights +
analysis, ~6 min; every number above). Individual: see regen.sh; analysis `python3
lab/results/20261020-1116-scout-df8e/analyze.py <dir>`.

**The lens (scout) may have made me miss:** I spent the window proving where the phase is
NOT, on shipped code, rather than surveying deeper offset-assignment practice (the
Tindell/Audsley line is UNVERIFIED at the source this run); and the falsifier flew one rung
only — the alternation channel (0a46's era-cost split) was not re-measured here beyond the
era worsts, which did not alternate in any arm.
