# Dossier — 20261014-2130-quant-d7e3 (Quant lens)

## Claim

The wave fix's named untested exposure is real and it is a memory ceiling, not a stutter: with
the player inside the belt band, the first-kick wave kills the process — OOM at the ladder's
standard 2×10⁵ under both arms (uncapped at 77 s, capped at ~210 s: `ES_PULL_CAP` delays the
death and does not prevent it), at 5×10⁴ (both arms, 6.87/6.88 GB) and 10⁵ (11.83 GB) — on a monotonic accumulation
of held scans (~6.5 MB standing each, no demotion, ~10³× the out-of-band record's ~10 KB), while
the whole out-of-band flight at 4× the bodies holds 0.89 GB. The cap's digest certificate is
unanswerable at 2×10⁵ on this box: neither arm survives to the cut.

## Bottleneck

Board item 1 (bodies: 28 against 10⁹, the furthest gap): the wave is the belt's first-kick freeze
and `ES_PULL_CAP` (bf21, certified twice, pending merge) is its fix. bf21's checker-2 named the
player-inside-the-band case "the real untested exposure"; 38bf listed it Unmeasured. Expected
gain: none claimed — this is the adversarial edge measurement before adoption (the lens's "edge
before the bet"). What it deletes if it holds: nothing; what it names if it breaks (it does): the
guard the cap needs before merge.

## Evidence

1. **Validity control (out-of-band, seed 1, N=2×10⁵).** Uncapped: max 1,321.5 ms, 9 over, kicks
   225,949, encounters 1,624, **digest `c2b834bb…` — 38bf's recorded digest exactly**. Capped
   (ES_PULL_CAP=64): the same digest, the same counters (225,949 / 1,624), max 657.9 ms / 2 over
   (the two spikes are shared-box wall noise — bf21's checker-2 already showed capped-arm spikes
   of this kind vanish on a quiet box; the digest is the machine-independent fact). My tree
   reproduces the record's canon.
2. **In-band, every N ≥ 5×10⁴ dies, both arms.** 2×10⁵: uncapped killed 77 s in, capped ~210 s
   in (the cap delays the death, does not prevent it). 5×10⁴: uncapped and capped killed at the
   same 6.88/6.87 GB peak, their progress trajectories identical to the MB (rss 6,604 MB, held
   1,196 at frame 9,000 in both) — the accumulation is deterministic and pull-independent.
   10⁵ capped: killed at 11.83 GB (≈ 2× the 5×10⁴ peak — the per-held answer scales with N).
   The out-of-band control on the same box holds 0.89 GB.
3. **In-band, N=5×10⁴ uncapped: the accumulation, watched.** RSS climbs monotonically through
   the flight — 6.05 GB at frame 5,700 (game 9,000 s) to 6.6 GB at frame 9,000 (game 14,500 s,
   the wave's tail) — with the held-scan count 1,110 → 1,196 and no demotion: ~6.5 MB of
   standing memory per held scan (an all-bodies-sized answer; the out-of-band record's held
   answers stand ~10 KB, a2c1) — and the process is killed at 6.88 GB peak before the cut. At
   4× the bodies the whole out-of-band flight holds 0.89 GB.
4. **In-band, N=10³: the engine holds budget** (0 frames over, max 11.6 ms, held max 82, 96 MB
   peak, digest `ad8a0e78…`, kicks 26,054 — the player's own burn chain; it is now a root-doll
   ship under thrust). A first pass on a busy box showed 13 over / 351 ms worst, but the rerun
   with the **same digest and the same kick counter** is clean: those spikes were schedule
   noise, not engine terms (bf21's checker-2's trap, re-caught). At small N the in-band seam's
   cost is the memory growth rate, not frame time.
5. **No in-band digest exists at any N ≥ 5×10⁴**: every arm dies before the 16,000 game-s cut,
   so the cap's digest certificate cannot be posed in-band on this box — the guard question is
   not "does the cap move bits" but "what bounds the held answers". Raw logs: `out/*.txt`
   (progress lines every 300 frames with game-s, RSS, held-scans; `/usr/bin/time -v` peaks).

## Predictions

`predictions.md` was written before the flights. Outcomes: **P1 failed as written and the
failure is the finding** — the bet was frame monsters (≥ 100 ms in-band); measured instead: the
engine holds frame budget at 10³ in-band (0 over, 11.6 ms max) and the exposure arrives as
**memory**, an unbounded held-scan accumulation that kills the process at 5×10⁴ and 2×10⁵. (The
one 351 ms pass at 10³ was box noise — same digest, clean rerun.) **P2 was not decidable as
written** at 2×10⁵ (neither arm survives to the cut, so there is no digest to compare); the
capped 5×10⁴/10⁵ arms are the nearest answer. **P3 (seed 7):** not flown to completion (killed
to free the box; its arm had started and was accumulating the same way). **P4 half-held:** the
belt's kicks are position-blind as predicted, and the in-band kick counter adds the player's own
burn chain (26,054 at 10³) — a root-doll term the out-of-band scene never had.

## What would make it wrong

The OOM could be the bench's own retention (rows + trace) rather than engine state — the progress
RSS lines discriminate (they print the trajectory before death; `rows` is ~100 B/frame, the
doll trace is tiny). The per-held-scan attribution (~6.5 MB) is a rate read off the trajectory
(ΔRSS/Δheld across 3,300 frames), not a heap profile. The cap-does-not-save conclusion rests on
one capped death at 2×10⁵ plus the capped 5×10⁴/10⁵ arms; a quieter box or a larger cap could
move a death past the cut. One seed flew to completion at 10³.

## Cost of adoption / fit

Nothing to adopt: the finding is a guard requirement on a pending merge. PRINCIPLES #12 ("i care
about the p95/99 results i want the game to be smooth") and the lens's item 6 (the player action
priced at p99.9 on a warm machine): here the worst case is not a slow frame but a dead one. The
named guard, in the engine's own idiom: the capture/scan already holds off the critical path
(`SCAN_BACKLOG`); the in-band seam needs the same hold keyed on the candidate's doll being
mid-wave, and the held-scan standing memory (a2c1's ~10 KB a scan) is the term to bound first —
it is my leading suspect for the OOM.

## The lens

The Quant lens prices tails and capacity; it measured the death and its rate, not the interior of the
blowup (no heap profile, no per-stage attribution — the `prof` feature build was skipped for
time). A systems lens would own the decomposition; the memory mechanism (held scans vs capture
buffers vs item backlog) is inferred from a2c1's standing-memory numbers, not measured here.
