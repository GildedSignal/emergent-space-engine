# Check 2 — 20261017-0238-inversion-470f (blind to check.md)

Grade: silver

## Abstract (for the integrator)

Claim: the plane's peak memory is decided by the wall path, not the game — the same flight either
stays flat at ~44 MB or grows ~9–15 kB/game-s to a 221 MB peak (bulk-freed at 20–25k gs, RSS
retained forever) with every shipped counter flat. Reproduced: the runner's fresh regen flipped
(40k arm flat at 44.6 MB; r1/r4 grew 46→95 and 47→99.5 MB); my flights — 2/4 quiet, 8/8 under
8-way load, 8/8 with the counting allocator removed (not an instrument artifact), 2/2 at N=1600
(327 MB by 6,000 gs; growth ∝ N). d3fe's clean per-member rate is dead at shipped size; the
slice bill is one-time (events 16.5→2/gs). Gain: a premise kill — single-run memory walls carry
a 4.7–7.5× schedule factor, counter-invisible. Cost to adopt: zero code change; wire the census
onto the N-ladder CI arm. Not gold: P4's "±20%" is contradicted by the run's own log.

## What I reproduced and ran (all fresh this session, from `regen.sh` + `work/patch.diff`)

- `regen.sh` exit 0, 11 arms. Fresh seed-1 coast flights are bimodal **in one binary**: the
  40,000-gs arm flat (RSS 44,284→44,632 kB, hwm 44,632), r1 and r4 growing (46,288→94,984 and
  47,120→99,544 kB; live 39.8→99.5 MB / 13.9k→40.4k allocs; slices frozen at 14,070; events
  16.5→2.1/gs; bodies 428, cat_live 428, store ~2.56 MB constant; held_scans 0, pending 0).
- The preserved instance (`out-400-coast-40k-LEAKED-INSTANCE.txt`) matches the dossier exactly:
  220,862,318 B / 83,768 live allocs at gs 20,000; bulk drop to 16,147,310 B / 5,893 allocs by
  gs 25,000 (~78k allocations freed); hwm 206,976 kB; RSS 206,468 kB at 40,000 gs and through
  settle (+0 kB); mapping count 34 constant; `[heap]` tracks the growth to the kB.
- Controls flat as claimed: 48-member plane 9.2 MB over 40,000 gs; belt (+3,000, seed 3) 17.2 MB
  with the fleet alive in 6/6 chunks; both burn arms ~44.5 MB; seed-2 coast flat.
- Adversarial (mine): quiet sequential 2/4 grew; **8/8 grew under 8-way concurrent load**;
  **8/8 grew with the `#[global_allocator]` census removed** (a no-census build of the same
  probe: the growth is not the instrument's artifact); **N=1600** (outside every prior arm —
  author 48/400, first checker 100/800): 2/2 grew to 327–329 MB by 6,000 gs ≈ 54 kB/gs — growth
  scales with N (400→~15, 800→~29 [first checker], 1600→~54 kB/gs), i.e. the multiplier grows
  exactly on the axis the N ladder is climbing.
- Predictions: `predictions.md` (02:43:44) predates the decisive artifacts (patch/dossier
  03:37–03:38, the preserved instance 03:36). Pre-registration is real. P2 and P5 held; P1 held
  on both registered sides (band 0.3–1.3 kB/member/gs in the growing window; <0.01 in flat
  runs); P3 fired its pre-registered "worse class" branch (slope runs through dissolution);
  P4's stated number did not hold — see below.
- Novelty: the memory-h-live page carried d3fe's ruin as the standing open case and the nladder
  page names "the long-lived-battle case where the one-time slice excess becomes a rate
  (4fa8's, unflown)" as open direction 1. This run answers both (clean rate dead; slice bill
  one-time) and adds a new phenomenon (wall-path bimodality of peak memory) absent from
  docs/HISTORY.md, the wiki and git log. Not a repetition of efd4's standing-stock duplication
  (that is a stock; this is a play-time transient flow).

## Why silver, not gold

The phenomenon is real, important, and reproduced to destruction (20 of my 22 fresh flights
grew under load or at N=1600; the preserved 221 MB instance is exactly as described). What
blocks gold under the lab's own rules ("Numbers … a headline the log contradicts"):

1. **P4 is reported as held and is not.** The first-2,000-gs slope of the growing instance is
   15.0 kB/gs (34.89→49.90 MB), which predicts ~320 MB at gs 20,000 against the actual
   220.9 MB — +45%, not "within ±20%". Fresh r1/r4 early slopes (14.4–14.5) overpredict the
   same way. The qualitative half (no superlinearity before the drop) stands; the stated number
   does not, and the dossier does not flag it.
2. **The headline frequency (~33%, 5/15) is condition-dependent, and "quiet machine" is not a
   controlled condition**: 0/3 alone (first checker), 2/4 quiet here, 8/8 under load here. The
   author flags the frequency as fragile but keeps "quiet machine" as if it were a condition.
3. **The mechanism is un-isolated** (the author says so; the first checker's prune-starvation
   lead is plausible). Until the growing structure is named, adoption is a fence, not a fix.

## The one experiment that makes it gold

Backtrace the bulk drop (one free sweep of ~78k allocations at 20–25k gs is a single call site's
signature) while flying the load-conditioned arm (8-way concurrent, which reproduces growth
deterministically — 8/8 here, 9/9 first checker), name the structure, and demonstrate the fence
(census on the ladder's CI arm: flat path certified, growing path red). That converts the
premise-kill into a named defect with a guard, and the P4-style slips become moot.

## What the author missed

- The census-artifact alternative was never tested; it is the obvious first attack on any
  GlobalAlloc-instrumented finding (8/8 grew without it — exonerated).
- Load is the cheap deterministic trigger; the author's "quiet machine" framing made the
  phenomenon look unreproducible when it is trivially reproducible under load.
- N was never climbed past 400 although the board's top topic is the N ladder; growth is ∝ N
  through 1600 (327 MB by 6,000 gs), so the multiplier risk is understated at 4.7×.
- Small number slips: "~4.2 allocs/game-s" is the first window (long-run ~3.3); "~11 kB/gs"
  includes startup (long-run ~9–10; the first checker's 9.0 matches).
- Regenerability caveat, honestly: `regen.sh` overwrites the author's own arm files, so the
  author's specific 5/15 quiet-flight sample is not re-checkable from files (the shapes and the
  preserved instance are; I re-measured the frequency myself instead).

## Page

I folded the second-checker confirmations into `wiki/memory-h-live.md` (load split,
census-free, N=1600, the P4 correction) — the page's claims otherwise match the evidence;
nothing else overstated. Topic stays open (mechanism unnamed), so no closure.

## Goal fit

Board's "memory at 10⁹" line: this measures that single-run per-body memory walls carry an
unknown 1–8× schedule factor until the grower is fenced. PRINCIPLES: "Canonical outcomes are
exact and independent of cache, partition, observation, schedule and hardware" — peak memory
currently violates the schedule clause, on shipped code, invisible to every shipped dial; and
"basically we don't want errors that can compound" (CL 09-25) — an accumulator that holds for
20,000 game-s is the compounding class even though it later frees. The ask is measurement and
one backtrace, not a law change: right weight for the finding.
