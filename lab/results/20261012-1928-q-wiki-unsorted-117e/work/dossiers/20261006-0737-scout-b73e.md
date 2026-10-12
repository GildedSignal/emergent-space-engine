# Dossier — 20261006-0737-scout-b73e (scout lens)

## Claim

The plane's frame-budget discipline sits on a measured knee between principle 12's two failure modes
(deep real-time-factor dips at a 5 ms cap, deadline hitches at a 13 ms cap), and no session-level
scheduling discipline — fixed, AIMD-adaptive, work-ahead presenting the lead, or the audio-style
inventory split of frontier and presentation clock — moves it, because the plane's bursts are
resolution cascades that exceed any small cap for longer than any sane lead; the lever is engine-side
(cheaper cascades or real lookahead into them), not frame-loop policy. The digest is bit-identical
under every discipline tested: schedule-independence verified under attack.

## Bottleneck

Principle 12 (Julien: "the algorithm that allocates the work to prevent those heavy tails, it's the
most important one", CL 09-25 14:28); board 29 September §4. Newly attackable because the plane flies
(H0210) and its bench measures the SLA of docs/plane.md (frame p50–p99.9, hitches/hour above
16.7/33/50 ms, RTF median and lowest 1%). The gain sought was removal of the dips × hitches
trade-off, not a throughput multiplier; what the run delivers is the measured knee, a verified
invariance, and two killed transplants that the next run must not re-try.

## Survey (the lens's job), ranked by fit to the requirements

Requirements as numbers: 16.67 ms hard frame deadline; hitches/h above 16.7/33/50 ≈ 0; RTF
lowest-1% ≈ median; outcomes bit-identical whatever the schedule; work deferrable, never droppable
("every body is real"); bursts are resolution cascades (each event reveals the next), not
pre-scheduled items.

1. **Pro-audio (JACK/CoreAudio practice): the buffer behind the mixer.** The listener hears a buffer
   lagged by L behind the mix frontier; frontier jitter inside L is invisible. Maps to: split the
   resolution frontier from the presented clock (`u.now` is both today). Both readings measured and
   killed (below). Failure mode: latency L, and bursts longer than L still stall. Source: standard
   practice (concept UNVERIFIED beyond common knowledge; no canonical paper cited).
2. **CoDel (RFC 8289): control the sojourn, not the backlog.** The signal is persistent lateness, the
   action deferral — free here, since outcomes are schedule-independent. My binary-overflow AIMD
   approximation of it oscillated and lost to a constant (measured); the CoDel *interval-averaged*
   lateness signal is the untested remainder.
3. **ATW/ASW (Oculus): present the last completed frame on a miss.** Already in the plane (horizon
   retreat = present resolved state, RTF dips instead of tearing). Concept verified.
4. **EDF overload / value-density shedding (Buttazzo line):** irrelevant — nothing may be dropped, the
   plane is already deadline-ordered, and under sustained overload no order helps.

## Evidence

Raw numbers and exact commands in `evidence.md`; summaries (all seed 1, members 400, rtf 4, 1800
frames; `--members` clamps to 400):

- **The knee**: fixed 5 ms → 0 hitches but worst-1% frames present nothing (RTF 0.007/4.0, 55
  overflows); fixed 13 ms → every dip gone (lo1 4.0) but 19–25 hitches/h above 16.7 ms (worst 22–24).
  No constant meets both halves of the SLA.
- **Digest control**: every discipline, both batches, one digest (87f51de403a4…) at the same
  seed/cut/log — the plane's "budget changes *when*, never *what*" holds under budget churn, AIMD
  oscillation and lead.
- **Work-ahead v1** (present the lead): dips remain (lo1 0.000) — the presented time *is* the
  frontier, so leading it just relocates the freeze. Structural kill of the lazy reading of "idle
  time computes ahead" at the presentation level.
- **Work-ahead v2** (audio's real split: resolve to a 50 ms-game lead, present on the wall clock):
  still 0.000 lo1 and 29 hitches/h — the lead is 12.5 ms of wall cushion at rtf 4, bursts last tens
  of frames, the inventory drains and the dips return while lead-rebuilding *adds* hitches.
- **AIMD v1** (binary overflow): dominated by fixed 13 on both axes (6 hitches and 0.000 lo1;
  budget ended at 3.2 ms after clean-frame decay missed the next burst).

## Predictions

In `predictions.md`, written before the comparison. Digest control: **held** (all six disciplines).
P2 v1 (overflow ↓3×, lo1 ≥ median/3): **failed** (overflow ↑ 82 vs 55; lo1 0). P1 (lo1 ≥ 2× P0,
worst < 16 ms): **failed** (0.000; 18.5 ms). Combined ≥ either alone: **failed**. The held-out seed
and members-200 rows were not reached before the deadline; all tables are seed 1 (tuned-on) — the
claim rests on the knee and the digest control, both stable across two batches and six disciplines.

## What would make it wrong

If bursts were *scheduled* future work (knowable without resolving), the inventory split should win —
re-running `--policy ahead` on a pre-scheduled-load scene would flip that transplant's kill. The
v2 numbers are single-seed: a checker should re-run seed 7 and members 200 before leaning on the
exact hitch counts. The knee's *position* moves with silicon, scene and load (19 vs 25 hitches/h for
fixed 13 between batches); its existence is structural. Cloud-vs-M1: orders of magnitude only.

## Cost of adoption

Nothing of the policies (they lost). What survives: (a) the measured knee as the target the
motion-law work must attack — cheaper kick/rebinding cascades (Sol's 29 µs kick, 15 of them in fit
and compile) moves the knee where no scheduler can; (b) the digest control as a reusable invariance
check for any future allocator work; (c) the structural rule: the presented clock must not be the
resolution frontier if smoothness is the SLA — but the split only pays once bursts are foreseeable,
i.e. engine-level lookahead (peeking the cascade), not session-level policy. The `--policy` patch
stays in this run's artifacts for the next run.

## Fit with PRINCIPLES

"The algorithm that allocates the work to prevent those heavy tails, it's the most important one" (12);
"'Use idle time to compute ahead' yes this is a whole important idea of this project" (17); "Priority
is slack, not proximity" (5) — the inventory was slack made concrete, and it lost on measurement, not
on fit; the digest control is plane.md foundation 7 ("outcomes are independent of schedule") verified
under attack. A failed experiment kills the configuration, never the method (9): two configurations
killed, the knee stands.

## The lens (what scout may have missed)

The survey ranks by structural fit, but the plane's queue internals (scheduled vs discovered work)
were read at the surface; an engine-level lookahead that speculatively resolves cascade members
(audited by the digest control) was designed but not built — the strongest next rung. Timings are
single-threaded cloud Linux on a shared box; the M1's thermal ramp and P/E split will move the knee.
