# Dossier — 20261016-0504-second-20261016-0346-spacex-917c-c840 (second author on spacex-917c)

## Claim

The checker's named gold experiment is flown and it **refutes the adoption direction: ES_STAGGER
armed fails B13 catastrophically (0/64 judged flybys, worst relative ΔE/ΔL error 4.65e0, against
the off arm's 60/64 baseline-red at 2.12e-2) and changes every one of the 13 `ladder_digest`
case digests** — the checker's own "armed digest identity (13/13 bit-identical)" does not
reproduce (their armed run lost the env var, the same way one of mine did silently). The parent's
frame findings stand; the stagger as a post-hoc first-kick mover is not a lawful birth default.

## Bottleneck

Board focus 1 (bodies: 28 → 10⁹). The parent (spacex-917c, silver) measured the staggered wave's
frame effect (28× collapse; the locals' floor binds). The checker held gold back on one named
experiment: the behaviour gates armed (B13/B14-class under the shifted first-kick tide phase,
ed3a's open direction 2). This run flies it. Gain: the adoption question is closed the cheap way —
a killed configuration, before the integrator wired a birth default that breaks the assist gate;
the cure must be birth-time-lawful (spread the birth draws, not the kick item), which is the same
law for every body and leaves single-birth scenes (every B12–B14 ship) untouched.

## Evidence (this box, Linux/x86 i7-4790, 8 vCPU; gate events and digests are deterministic and
## box-free; each command ≤ 60 s except the three parallel digest runs, ~4 min total)

The parent's own `work/patch.diff` (applied verbatim; its off arm re-verified bit-identical to a
pristine build), one patched binary; OFF = `env -u ES_STAGGER`, ARMED = `env ES_STAGGER=1`.

1. **B13 armed (the decisive gate).** `xtask behave --law plane --gates B13`:
   - OFF: `60/64 within 1e-2, worst ΔE 2.12e-2 ΔL 2.12e-2` — HANDOFF's baseline, bit-matched.
   - ARMED: **`0/64, worst ΔE 4.65e0 ΔL 4.65e0`** — every judged flyby outside the 1% band.
   - Mechanism, measured: the adapter births its ship bare (`add_body_state(Kind::Ship, ..)` +
     `start()`), so `plan_clock` takes the staggered path (verified: an instrumented build prints
     `STAGGER engages: id=1 t=0 half=5.94e10 off=6.73e10` — 64 of 64 universes). `stagger_hash(1)`
     = 0.5666, and the ship's id is 1 in **every** seed, so every flyby's first kick moves by the
     same 0.57 steps (to t + 2.13·half — past the first full step). `PLANE_TRACE`: the same flyby
     resolves with kicks 213 / boundaries 213 armed vs 305 / 304 off — the encounter is sampled
     materially differently, and the assist (ΔE ~ 1e-9 against E ~ 1e-9) is first-order in that
     phase: the first kick's window IS the encounter, which is aperiodic — there is no orbit to
     average over, which is precisely where the parent's belt argument (uniform phase of a
     periodic sequence) does not apply.
2. **The checker's armed-digest identity does not reproduce.** `ladder_digest`, 13 cases:
   OFF vs pristine: **bit-identical** (the off arm is a clean no-op — the record stands).
   ARMED vs pristine: **all 13 case digests differ** (9 with identical event counts, 4 with
   changed kick counts: e.g. `N=1000 coast through the wave` kicks 32,537 → 31,973). The parent's
   dossier expected this ("digests change as any birth-draw change does"); the checker's
   "13/13 bit-identical armed" was almost certainly an env-drop artifact — I hit the same one:
   one `ES_STAGGER=1 cmd > file` invocation silently ran unarmed (its B13 output matched the off
   arm exactly), while `env ES_STAGGER=1 cmd` and other invocations of the same form armed
   correctly. Every armed number in this dossier was re-run and is engagement-verified.
3. **B14 frozen:** `B14 FAIL timeout: 60.1 s over the 60 s limit` in BOTH arms (HANDOFF's known
   state; the frozen gate cannot judge the stagger on the plane).
4. **B14-class probe** (8 Hill moons, 0.2–0.9 R_H, e0 ∈ {0, 0.15, 0.3}, pro/retro, 10 planet
   periods, hill.rs's apsidal estimator verbatim, `stagger_probe moon`): escape class at 1.5 R_H
   **identical across off, armed and an independent RK4 reference on all 8** (3 escapes, 3/3/3).
   Apsidal rates (rad per planet period): seed 4 off 0.8906 / armed 0.8880 / ref 0.8712 (both
   arms inside B14's 10%); seed 5 off −0.1385 / armed −0.1379 / ref −0.1488 (both inside);
   seed 1 off −0.0325 / armed −0.0314 / ref −0.0389 (both OUTSIDE 10% — the law's own error,
   not the stagger's; |armed−off| = 0.011 ≪ the law's 0.064 gap to the reference). The stagger
   moves the rate by ≤ 2.9% of |rate_ref| — inside the gate's own band wherever the law already
   is. The Hill class of behaviours is robust to the shift; the assist is not.
5. Reproduce: `lab/results/20261016-0504-second-20261016-0346-spacex-917c-c840/regen.sh`
   (~9 min: builds, the three digest runs in parallel, B13/B14 both arms, the probes, the
   analysis → `probe_analysis.txt`).

## Predictions (predictions.md, written before the decisive runs)

- **P1 FAILED as written, and the failure is the finding** (predicted armed 60/64, band
  [58, 62]; measured **0/64**). The band assumed the shift was a small perturbation of the
  tide phase; it is a first-order change of an aperiodic encounter's sampling (kicks 305→213).
  My pre-registered kill criterion — "armed B13 below ~56/64 kills the adopt-as-birth-default
  direction" — fires on this number.
- **P2 HELD:** the instrument sees the stagger (states at fixed times differ; armed kick trains
  shift by ~+0.57 steps, verified by item-time traces).
- **P3 HELD:** B14 times out identically in both arms.
- **P4 held on class, missed on the rate band:** classes identical armed/off/reference on all 8
  moons; |rate_armed − rate_off| ≤ 2.9e-2·|rate_ref| (my band said ≤ 1e-2 — seed 1's 2.92e-2
  is outside it, still 3.4× below the gate's own 10% and 6× below that seed's law-vs-reference
  gap).
- **P5 FAILED as written:** I predicted the checker's armed-digest identity would hold on this
  tree; instead all 13 armed digests change (Evidence 2). Both P1 and P5 failed in the direction
  that matters for adoption: the stagger armed is NOT invisible.

## What would make it wrong

The refutation rests on B13's 64 seeded flybys and the digest record, both deterministic and
reproduced twice on this box with engagement-verified invocations; a box cannot change them. What
it does NOT show: (a) that a *smaller* stagger (off < one half-step, or scaled by 2^-k) also
fails — the failure is first-order in the fraction, so a bounded variant is the natural next
falsifier, but it is a new configuration, not the parent's; (b) anything about the parent's frame
measurements (28× collapse, the locals' floor, the break analysis) — those were armed nladder
flights and remain the standing frame record; (c) the B12 handoff gate (not wired for the plane);
(d) the M1 re-measure. The env-drop fluke itself (one `VAR=1 cmd > file` invocation running
unarmed, silent) is a hazard for every future armed/off experiment here — invocations must
engagement-verify (the probe prints `stagger=<bool>`; the digest diff is the canary).

## Cost of adopting, fit with PRINCIPLES

Nothing to adopt: a configuration killed cheaply ("A failed experiment kills that configuration,
never the method", principle 9). What survives, exactly as the parent measured: the wave's frame
term is deletable — but the deletion must be **birth-time-lawful**: spread the births themselves
(the birth program's tick grid, B18's domain), so the first kicks land spread by construction and
a lone ship (every B12–B14 scene) is untouched, instead of moving a body's first kick item after
the law has already anchored its clock. That variant changes digests as any birth-draw change
does — the honest legality surface — and needs the same B13 armed flight as its first gate.
PRINCIPLES: "the simulation decides" (the stagger moved when the first surprise lands for OUR
bookkeeping, and the assist gate felt it); "Compute only surprises" stands — the cure is to stop
creating the coincidence (one-tick births), not to shift kicks post hoc.

## The lens (what the second-author position may have made me miss)

The checker's gold sentence bundled "fix the P3/P2 recap lines"; I could not edit the parent's
branch (results live on their own branches) — the honest recap lives here and in the wiki page:
the parent's P3 recap was wrong (1/28 is outside [1/12, 1/4]) and its P2 was marginal, as the
checker said. My probe's assist errors at 0.2 P (3e-2..4.6e-1) are judged later than the gate's
SOI exit and over-sample the fast tail — I use them only for armed-vs-off differences, never as
gate verdicts. The RK4 reference is my own (not the judge's Dormand–Prince); where it matters
(the moon rates) the law arms sit on the same side of the 10% band as off, so the reference's
exact pedigree does not decide anything here.
