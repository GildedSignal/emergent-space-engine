# Dossier — 20261013-2252-second-20261013-2130-library-ae3d-7497 (second author, library lens)

## Claim

The missing experiment is done: on four shipped `scenario::plane` settles (idle seeds
1/7, a held L12 burn, a 4,000-member battle), the per-body kick distribution is **not
heavy-tailed** — the tube bulk is flat per orbit by construction (CV 0.17–0.19, max/
median 1.4–1.5), the per-second spread is three decades of *orbital period and clock
regime* (rankable from body constants at birth), and the head is not a property of
bodies but of drivers (the burn: player 70.6%; the battle: mass spread over 3,769
promoted members, top body 0.07%). **Rule 2 of 20261013-2130-library-ae3d ("the live
set is a rank, not a count") dies as a ladder rule; the fixed fraction stands**, and
the gold path folds to the page's open direction 4 (compaction as the scheduled spike)
plus rule 4's option.

## Bottleneck

Board focus 1 (28 bodies against 10⁹), deciding a rung of the in-flight N ladder
(`wt/nladder`): is promotion compact→live chosen by rank in a measured surprise
distribution (rule 2), or by a fixed fraction? Expected gain: a deleted design path
(promotion-by-rank rungs, surprise-rate instrumentation for the ladder) and the
redirect of the promotion question to what is already measured to matter (ephemeral,
driver-caused promotions; frame-cost's `resolve_handout`).

## Evidence

Probe (work/patch.diff, 102 added lines): `Update.kick` set in `step::process`, an
opt-in `Universe::kick_log` (None by default), and the example `kick_tail`. **Digest-
neutral, proven by regen**: the `frame_digest` reverse-L15 burn flight gives
`e0972a1ce81d30950df93a0b1ec8d37c` (kicks 1684, encounters 597, 4 schedules agree)
identically on base and patched trees. All numbers regenerate: `regen.sh` (~80 s warm,
build ~30 s more cold).

Scenes (deterministic settles of the shipped scenario; Linux/x86 shared runner; the
per-orbit normalisation uses each body's compiled period):

| scene (span) | bodies | kicks body/origin | tube bulk per orbit | head |
|---|---|---|---|---|
| idle seed 1, m48 (40,000 game-s) | 76 | 9,176/96 | CV 0.179, max/med 1.47, Gini 0.100, Zipf −0.23 (r² 0.94) | player 21.1% **by frequency** (250.3/orbit, flat with the bulk) |
| idle seed 7, m48 (40,000 game-s) | 73 | 10,800/969 | CV 0.173, max/med 1.44, Gini 0.096 | player 17.9% |
| burn L12 held, m48 (1,000 game-s) | 71 | 2,142/48 | CV 0.189 (unchanged) | **player 70.6%** (1,513 kicks: 816 sub-level ≥ 1, 89 clock) |
| idle seed 1, m4000 (3,600 game-s) | 3,988 | 78,299/88 | CV 0.189 (unchanged) | player 0.2%; 3,769 members per-lived-second: Gini 0.549, top1 0.07%, max/med 4.68 |

Reading:

- **The bulk is flat per orbit by construction.** Planets, moon, orbiters, skimmers
  and the idle player all sit at 141–250 kicks/orbit (`step_for` = 1/2⁶ of the body's
  own period, plus alignment stubs and doll-exit caps); the identical per-body numbers
  across all four scenes (Orbiter 2: 212.4/202.0/212.1/210.6) show deterministic
  cadence, not sampled surprise. Top-1 ≤ 12% within the bulk on every scene.
- **The per-game-second spread is three decades (4.8×10⁻² → 3×10⁻⁵), but it is
  structure, not surprise**: rank per second = rank in 1/P_orbit plus the clock's
  regime. The 12 haulers (root doll, motion law v2) take 0–2 kicks *each* in 40,000
  game-s (0 at 3,600 s) — the quietest bodies per second while nominally the richest
  per orbit (620–26,000/orbit extrapolated: the over-provisioning of 27ce/7f97, not a
  tail). A promotion bar at any rate is therefore a **period/clock-regime threshold,
  knowable from body constants at birth** — the certificate the ladder wants is a
  constant, not a measured rank.
- **The head is driver-caused, sparse, and already light-cone-scheduled.** With no
  burn, no body is an outlier in the cadence sense (per-orbit max/med 1.4; the
  player's 18–21% share is its short period, and it is *flat per orbit with the
  orbiters*). Under a held burn the player takes 70.6% of the scene's kicks (816
  sub-kicks — the waterfall of 174d/0f2a, re-measured here as a distribution). In the
  4,000-member battle the stream spreads over 3,769 handed-out members (p50 5, mean
  20.6, max 174 kicks; top member 0.07% of the stream): **no rank structure to
  promote by**. Passage sub-kicks land on whichever members the battle hands out deep
  in the well (8/38 at m48 with 14–261 sub-kicks; 22/3,769 at m4000) — discovered by
  due-ness, not rankable ahead.

The store baseline this completes regenerates on this box (regen.sh, third section):
`shipmem` n2e4 12.347 bits/member at 7 ns/update, storm 48.38 with inference fallen
back (0 mismatches), convoy hot max 10.9 µs against a 1.29 ms compaction step (2,570
repacks) — the previous silver's record, orders of magnitude agreeing.

Commands (repo root, after `regen.sh`'s patch step; each ≤ 60 s):

```
T=<target-dir>/release/examples
$T/kick_tail idle 40000 1 48    # probe/idle-s1-m48.jsonl
$T/kick_tail burn 1000 1 48 1 12 1  # probe/burn-s1-m48.jsonl
$T/kick_tail idle 3600 1 4000   # probe/idle-s1-m4000.jsonl
python3 <run>/analyze.py <run>/probe/*.jsonl
```

## Predictions

`predictions.md` was written before any probe ran (this box's file mtimes show the
probe captures after it — the previous run's pre-registration gap, closed). Outcome:
P1 held (CV 0.17–0.19; three decades per second). P2 half-held: the haulers' per-orbit
spread is 42× as predicted, but it is period-driven extrapolation from ~1 kick — per
second they are uniform (~3×10⁻⁵), so "regime spread" is real per orbit and absent per
second. P3 half-failed on the letter: the burn clause held exactly (player ≥ 30%:
measured 70.6%, top-3 76.9%), but the idle top-1 share is 21.1% at seed 1 against a
predicted < 20% — and the mechanism is frequency, not surprise (per-orbit the player
is flat with the bulk, max/med 1.4); seed 7 gives 17.9%. P4 held (this verdict, as
predicted). P5 half-held: no rank structure among members (per-lived-second top-10%/
median 1.0–1.2), but two details were wrong — mean kicks per member is 20.6, not
single digits, and at this span (3,600 s vs fermi's 8 s) member kicks (78,299)
dominate hand-outs (3,960), the reverse of the fermi mix.

## What would make it wrong

A shipped scene whose per-body surprise is heavy-tailed *without* a driver would
revive rule 2; none of the four shows it, and the counterexample class (a dense belt
where conjunctions cluster on bodies) is not in the plane — the belt scenarios are the
place to falsify next. The hauler numbers are far-field rates measured over 0.03–0.3%
of an orbit (a full-orbit hauler measurement needs ~10⁷–10⁸ game-s, wall-days); their
per-second quietness is directly measured, the per-orbit extrapolation is weak and
marked so. Linux/x86 shared runner throughout; the integrator re-measures on the M1.

## Cost of adoption, and fit with PRINCIPLES

Negative: the ladder never builds the rank-rule rungs or the surprise-rate
instrumentation; the compact→live certificate is a body constant (period/regime), and
promotion stays due-ness-driven — which points the promotion cost exactly where
frame-cost already measured it (`resolve_handout`, 486–585 µs, sticky: make it
ephemeral). Fit: "Compute only surprises" (the head is drivers, already events);
"behaviours matter, not continuum fidelity" (judged by distribution shape, not
trajectory identity); "the cheapest compute is compute not done" (a rank nobody needs
to measure). The one-law reading (PRINCIPLES #19): one cadence law (per-body period +
clock regime) already explains the bulk; a promotion-by-rank rule would have been the
second convention.

## The lens

A second-author run inherits the first run's frame: I measured the distribution its
rule 2 assumed, on shipped code, and the rule died — the useful outcome the checker
named, but a librarian's sympathy for the rank rule (Zipf's law as a prior) is a lens
bias worth naming: the shipped law's *construction* (per-body period cadence) makes
flatness nearly inevitable, so the measurement's bite is in the driver half (burn,
battle) and the constant-certificate reading, not in refuting a power law that the
cadence law never allowed to form. What this lens may have missed: the belt and
conjunction clustering (rule 2's honest revival path), and any population where
surprise is intrinsic rather than driver-caused.
