# Dossier — second author on 20261014-2248-inversion-4af4: the named experiments, done

**Claim.** The checker's named experiments are done to this box's limit and the 4af4 claim now
holds on a regenerating record: flown through **25 wave periods at 2×10⁵ (cut 700,000 game-s ≈
2 h of play at rtf 100, digest `90348a69…`)** memory stays a step, not a staircase (rss 905 →
913 MB = +0.9% from wave 1 to wave 25; +0 MB over the last 600,000 game-s; one retired binding
per body standing; catalogue constant; 0 frames over 12 ms in 420,062; lag 0.000 at every
sample; settle 0), and at **4.2×10⁵ — the largest N that fits this box's 2 GB rule (rss 1,909 MB,
4,766 B/body)** the step holds again (+13 MB at wave 2; wave-1 peak 76,620 kicks/sample, the
sharpest ever measured on the plane, absorbed with 1 frame over budget and 0 backlog), while
the wave train's **dissolution — extrapolated by 4af4 — is now a measurement**: the peak/floor
ratio falls 103× → 2.3× by 685 k game-s not because the peak collapses alone but because the
between-wave floor rises (343 → 1,479 kicks/sample) as the sheared cohort fills toward its
equilibrium (the steady belt stream, ~2.96×10⁻⁵ kicks/body/game-s, converging to b30b's
3.33-3.50×10⁻⁵), with memory and cadence flat through the transition. The 10⁶ flight the
checker named stays **one command on a 6+ GB box** (`wavetrain 1000000 90000`: build ~2.6 GB,
steady ~5.1 GB — impossible under this box's 2 GB/process rule, so its cheapest decisive parts
were run instead: the time axis pushed 2.8× past the extrapolated dissolution, the N axis to
the ceiling).

**Bottleneck.** The board's first (real bodies in the flyable engine, 28 → 10⁹). The 4af4
certificate said "the plane is flat in play time at 3×10⁵" over 5 waves with the dissolution
extrapolated; this run extends it to 25 periods / 117 min of play, to 4.2×10⁵ bodies / 1.9 GB,
and repairs the record so the numbers regenerate from the run's own script. What it deletes:
the "is retention stable past wave 10?" question and the "is the dissolution real?" question,
on every N this box can fly. What remains open is unchanged and named: the cadence law and the
compact store to 10⁷⁺, and the 10⁶ line itself.

**Evidence** (all from `examples/wavetrain.rs`, the plane bit for bit — `plane_extra`, seed 1,
coast, rtf 100, 12 ms budget, 60 fps frames, player at Home, canonical absolute-tick cut;
commands and raw logs in `out/`, `regen.sh` regenerates everything in ~10 min):

Arm D — N = 2×10⁵ (200,028 bodies), cut 700,000 game-s, 420,062 frames, wall 427 s,
digest `90348a698294dd47ccfca67a70dc890b8ea8835030bdd1a22eb2a74ee8293004`:

| era (game-s) | floor kicks/sample | peak kicks/sample | peak/floor | rss (MB) | frames over |
|---|---|---|---|---|---|
| 10k-35k (waves 1-2) | 343-345 | 35,697 / 35,484 | 103× | 455→906 | 0 |
| 60k-110k (waves 3-5) | 343-369 | 23,830 → 13,575 | 70× → 37× | 906→912 | 0 |
| 135k-235k (waves 6-9) | 350-371 | 11,893 → 7,958 | 34× → 22× | 912→913 | 0 |
| 260k-385k (waves 10-14) | 424-631 | 7,208 → 4,488 | 17× → 7× | 913 | 0 |
| 410k-585k (waves 15-21) | 701-1,011 | 5,048 → 3,748 | 7× → 4× | 913 | 0 |
| 610k-700k (waves 22-25) | 1,137-1,479 | 3,656 → 3,442 | 3× → 2.3× | 913 | 0 |

- Memory: 455 MB build → 905 after wave 1 (the step: one binding per kicked body) → 913 at
  wave 4 → **913 at game-s 700,000** (hwm = rss at the end, never exceeded). Per-wave deltas
  +1/+5/+1/+0, then zero for 599 k game-s. Engine accounting ends at 1,395 B/body; rss
  4,781 B/body. Zero refusals; encounters exactly linear (48.55/ks here vs 48.68/ks over arm
  C's 250 k: 33,984 by the cut — predicted 34,000 ± 10%); catalogue 200,076 at every sample;
  opens 200,637 = N + 637, the same invariant as 3×10⁵ and 4.2×10⁵.
- Census (4,161 fixed belt bodies, every 5,000 game-s, 141 samples): hist = 4,161/4,161 from
  20 k game-s to the end; **h2 > 0 at 29/141 samples, always ≤ 3 bodies (max 0.07%), hmax ≤ 2,
  hsum back to 4,161** — a second retired binding exists transiently at wave edges and never
  stands. This corrects 4af4's wiki clause ("h2 = 0 at every census": true at 3×10⁵ except
  3 samples with h2=1; at 2×10⁵ over 700 k it is ≤ 3).
- The drain: lag 0.000 at **every** one of 2,801 samples; 0 events outstanding at the cut; 0
  frames over 12 ms in 420,062 (worst 11.96 ms).
- The dissolution, measured (4af4 extrapolated "after ~20 waves / ~550 k game-s"): the last
  window above 10× the median sample sits at ~99 k game-s (wave 5) — earlier than extrapolated,
  because the **floor rises** as the sheared train fills: +210 kicks/sample per 1,000 game-s
  after 250 k, reaching 1,479 at 685 k. The implied mean kick interval lengthens from the birth
  cohort's ~27.5 k to ~33.8 k game-s (200,000 bodies / 5.92 kicks/game-s), i.e. the stream rate
  converges on the belt's own rate constant — 2.96×10⁻⁵/body/game-s at 685 k against b30b's
  end-to-end 3.33-3.50×10⁻⁵. No sharp wave survives past ~460 k (ratio < 5×). Through the whole
  transition: rss flat, cadence flat.
- Internal consistency: arm D extends arm C's flight (same seed, N, protocol); the h-census
  counters agree at 49/50 shared samples; the one difference (game-s 15,002, inside wave 1:
  encounters 643 vs 630) is the census trigger's presented-time quantization — the same
  wall-wobble class 4af4 diagnosed for the cut, here on a mid-flight sample, and the reason
  certificates sit at absolute-tick cuts.

The contention measurement (the regen's own rerun, an unplanned arm — and a second, heavier
one): arm D has now been flown **three times in full — once idle, twice contended (the window's
other runs building on the same box, load up to 7.4) — with one digest, `90348a69…`, and every
law counter identical each time** (kicks 6,040,477, events 12,172,103, encounters 33,984,
opens, boundaries, handoffs, refused, lost, b_per_body 1,395; `regen.sh` asserts this and
passed). The wall view moved exactly as the budget model predicts under contention: frames over
12 ms (627 in the worst flight vs 0 idle), the drain holding scans mid-flight — and **held
saturates at exactly 2,048 in both contended flights, the shipped `SCAN_BACKLOG` bound
(universe.rs:79: "answered, inside the frame's budget … once this many are waiting, the oldest
first, so the memory they hold is bounded")** — with rss 913 → 995/1,004 MB (+82/+91 MB,
allocator-retained after the flush; settle 0.62/0.20 s) and **lag still 0.000 at every sample
of every flight**; the per-body retention (catalogue, history, b_per_body) never moved. So the
wall-dependent columns the 4af4 checker saw drift (frames over, max_ms, and rss with them)
have a mechanism and a bound: box contention pushes frames over budget, the held path stands
memory up to `SCAN_BACKLOG`, and the cost is capped near +90 MB at 2×10⁵ — bounded, not
open-ended, and invisible to the digest. The certificate numbers above are the idle-box flight
(load 0.16 at launch, recorded in `out/clean-run-record.txt` with the overwritten first log's
grep record; the two contended logs ship beside it); a checker on a contended box regenerates
the digest and counters exactly, and the wall columns within this measured envelope (frames
itself wobbles — E's clean rerun flew 37,083 frames vs 36,366 at the same tick cut).


Arm E — N = 4.2×10⁵ (420,028 bodies; the 2 GB ceiling: steady 4,766 B/body → 1,909 MB), cut
60,000 game-s (two waves), 36,366 frames, wall 85 s, digest `0dec42f3c4416fec8e11b31e55edc456…`:

- Wave 1 (13,502-16,001): peak **76,620 kicks/sample** (196× median — the sharpest load measured
  on the plane; the birth cohort packs ~2.2 kicks/body into 2.5 k game-s); the climb is inside
  the wave (rss 1,551 → 1,842 over 500 game-s); transient lag 0.905 game-s; held up to 267;
  **1 frame over 12 ms (12.24 ms)**; absorbed — settle 0, lag 0.000 at the next sample.
- Wave 2 (40,501-44,501): peak 34,796 (0.45× wave 1 — the shear is stronger at this N), rss
  1,896 → 1,909 (+13 MB, +0.7%), 0 frames over, lag 0.000.
- Scale-free per-body state (held-out prediction 8): rss 4,766 B/body vs 4,743 at 3×10⁵
  (predicted ±150); the wave-1 step +2,372 B/body; catalogue 420,076 = N + 76 constant;
  refusals 0; encounters 2,886 by 60 k = 48.1/ks (the player's sweep, N-independent).

The record fix (the checker's named defects, all repaired and verified in `out/report*_*.txt`):
`analyze.py` crashed as shipped (`'%.0f-%.0f' % s` with `s` a list → TypeError, masked by
`|| true`); fixed with `tuple(s)` plus a proper `hist_sample=a/b` parse, and it now regenerates
4af4's central tables from that run's own shipped logs — windows `13502-15752 / 40752-43502 /
68251-72251 / 96251-101251 / 124251-130001`, peaks 35,629/35,285/33,883/25,448/20,189, rss
deltas +7/+2/0/0, census 2,858/4,106 mid-wave-1 → 4,106/4,106. `regen.sh` no longer masks
errors and asserts both canonical digests. The MiB/10⁶ slip is corrected everywhere (post-wave
4,743 B/body, not 4,515). The 10⁶ command for an M1-class box, recorded for the integrator:
`wavetrain 1000000 90000` (three waves, ~5.1 GB steady, est. a few minutes on an idle M1).

**Predictions.** `predictions.md` was written before arms D and E ran. Outcome: 1 held
(+0.9% over 25 periods, kill bar +5%/wave never approached); 2 split — the sharp windows ended
at wave 5, earlier than the predicted 12-22, and the "stream's median grows with play" clause
**fired as written**: the median rose 419 → 2,034 kicks/sample. Diagnosis (H0183): the rise is
the dissolution mechanism itself — the sheared cohort filling toward the bounded belt-rate
equilibrium, not a compounding term; memory and cadence stay flat through it, which is what the
claim needs, but the clause as pre-registered failed and is reported as failed; 3 held for the
peak, width under-assessed (the 10× detection stops catching widened waves — the floor table is
the honest instrument); 4 held (h2 ≤ 3 of 4,161 transiently, exactly the predicted ≤ 4 class);
5 held (D: 0 over in 420,062; E: 1 over at the 76.6k peak, worst 12.24 < 13 ms); 6 held exactly
(33,984 vs ~34,000 ± 10%); 7 held — `regen.sh`, run end-to-end after the flights, reproduced
both canonical digests bit-for-bit (`90348a69…`, `0dec42f3…`) with every law counter, on a
rerun that flew under box contention — the frames count and the over/max_ms/rss columns wobble
with the wall (the contention envelope is measured above); 8 held (4,766 vs 4,743 ± 150,
catalogue N + 76, step ~2.37 KB, lag clean).

**What would make it wrong.** One seed (the ladder's), coast only, the player at Home (the
in-band ruin is d7e3/625b's measured territory), N ≤ 4.2×10⁵ on this box — the 10⁶ memory line
is still an extrapolation of a constant measured over 7× in N, never at 10⁶ itself; the floor's
asymptote past 700 k is inferred from the interval census, not flown; the width/shear constants
are detection-threshold-dependent; Linux VmRSS against the ladder's macOS phys_footprint (~9%
platform offset). If the stream's floor kept rising past the belt-rate equilibrium (it had
reached ~85-90% of b30b's rate constant by 685 k), cadence — not memory — would be the term to
re-measure, and that is the Fermi line, not a flight, at 10⁷⁺.

**Cost of adopting.** None for the engine: no code change is proposed. The protocol rule
(wave rungs cut at absolute ticks) is now backed by a second, longer digest-stable flight, and
the long-flight certificate costs one 7-minute command per rung on this box. `analyze.py` in
this folder supersedes 4af4's copy for any future wave rung.

**Fit with PRINCIPLES.** "Compute only surprises. Cost follows change" (§3): after dissolution
there are no waves — only the belt's steady surprise stream — and the engine's bill (memory,
frames) does not move. "Errors never compound" (§13): twenty-five periods, one step, one
retired binding per body, zero backlog. "A failed expectation is not automatically a failed
method: diagnose which one broke" (H0183): prediction 2's floor clause failed as written and
the diagnosis is the measurement.

**The lens (second author).** I was pointed at the checker's named gap and closed what this
box could close; what that may have made me miss: the floor's long-horizon behaviour (a
birth-staggered scene or a 2×10⁶ game-s flight would separate shear-fill from interval drift),
the burn and in-band axes (other runs' measured ruin, untouched here), and the 10⁶ flight
itself, which only the integrator's M1 can fly.
