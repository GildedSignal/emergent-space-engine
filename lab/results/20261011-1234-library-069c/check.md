Grade: silver

**Abstract.** Claim: a stationarity verdict — blocked-difference F over 32 segments with a τ-guard — gives B12's rebuild the statistic that separates a slow leak from bounded error, the case that killed the recurrence ratio. Reproduced from the shipped script in 1.3 s, deterministic: slow leak 95/100 compounding (F med 10.4), diffusive 97/100, false alarms 0/200, never a wrong verdict (misses are void); fresh seeds and my own leak exponents (RMS growth t^0.08–t^0.25) hold at 77–92 % caught. F is amplitude-free (catches diffusion at 3 % of quantum scale), fixing the old B12's magnitude-ranking flaw. Cost: one O(T), integer-able statistic. Not gold: the recorded "99 bounded, 1 void" does not regenerate (script edited after the run), and a bounded phase-tied oscillation at period ≈ T/2 false-alarms 100/100 — the plausible shape of the plane's real energy residual.

## Reasons

**Reproduction (clean copy, `/tmp`, 1.3 s, bit-reproducible).** All headline numbers regenerate from the shipped `b12probe.py`: T=4096 bounded 100/100 (F med 1.015, p90 1.27 — dossier "med 1.0, p90 ~1.3" ✓), diffusive 97/100 (F med 12.7 ✓), ballistic 100/100 (F med 6.09e4 ✓), slow_leak 95/100 (F med 10.4 ✓); T=1024 compounding still 96–97 % caught, bounded → 100 % void, never wrong. Verdict breakdown at the author's exact seeds: diffusive 97 compounding + 3 void, slow_leak 95 + 5, zero wrong verdicts. Library side: 4,580 highlights / 770 non-deleted docs exact; all six quotes verified verbatim with correct attribution; no credential in the export ("bearer"/"token" are prose; hex strings are Readwise IDs).

**Held-out check.** `predictions.md` predates the final dossier (mtime order: predictions/pyc, then script, then dossier). Outcomes (a)(b)(c)(e) HELD, (d) missed upward and reported as a miss — honest. The author disclosed that two failed estimators exposed models 4–5 in structure and asked for exactly the check I ran: fresh seeds (seed0 777001) and my own parameters. Result: the killer case holds — leak RMS t^0.25 caught 92/100 (8 void, 0 bounded); author's five models all verdict-correct on fresh seeds.

**Attacks (mine, fresh seeds, T=4096).**
- *Slow-leak family:* RMS t^0.17 → 89 %, t^0.12 → 84 %, t^0.08 → 77 % + 3 false "bounded", t^0.025 → 70 % + 15 false "bounded". The false-bounded leak grows ≤ 1.3× within the window — the boundary of "compounding" itself, but it is a confident verdict, not a void.
- *Amplitude invariance:* diffusion at scale 1.0Q down to 0.03Q caught 93 % at identical F (med 12.5) — F is a variance ratio, so magnitude never masks class. Directly repairs the recorded old-B12 flaw (probe P2, H0215).
- *Phase-tied bounded oscillation (the author's disclosed risk, now measured — severe):* bounded AR(1) + A·sin(2πt/P): P=2048, A=3Q → **100/100 false alarms** (F med 8.4); P=1365, A=2Q → 79 %; P=1024 → 99 % void; P=512 → 100 % void; quasiperiodic → 100 % void. Mechanism: `F ≥ fcrit` takes precedence over the τ-guard, so the guard protects only the bounded verdict; any oscillation with period ≳ T/8 marches the segment means into an unguarded "compounding". A symplectic integrator's energy error is bounded and phase-tied to the orbit: if the window spans a few orbits, B12-v2 as shipped false-alarms on the very residual it exists to judge.
- *Near-unit-root:* AR(1) ρ=0.99 → 100 % void (honest); ρ=0.999 → 78 % false alarms; ρ=0.9999 → 92 %. The guard's honesty ends between 0.99 and 0.999.
- *Late-onset leak (starts t=3000/4096):* 100/100 read bounded — detection latency is most of a window; the verdict is true over the window but a stability gate needs a sliding statement.
- *Heavy-tailed bounded jumps (±100Q, p=0.002):* 100/100 bounded — the τ-guard survives its stated risk.

**Novelty.** HISTORY and the taste log record B12's statistic as broken (ranks bounded above compounding; H0215, HANDOFF line 71: "B12 cannot yet tell bounded from compounding error on chaotic ships") and the recurrence-ratio candidate as killed by precisely the slow-leak case (redteam-b12-stat, 6 Oct). No prior stationarity / blocked-difference / F-statistic proposal anywhere on the record. The prior library-lens run (30 Sept, faction thresholds) is different subject matter. This is a genuine candidate for queue item 1 (q-b12-design), complementary to the in-flight Codex/Sonnet rebuilds.

**Goal fit.** Direct hit on the top queue item and plan item 2 ("B12 rebuilt and frozen"). PRINCIPLES: "Errors never compound" (P13) is only checkable by an instrument that judges error *class*, not magnitude — the loser's-game lesson is the right mechanism; "the oracles are guards, not shepherds" (P34) is exactly the void verdict refusing outside its window. The statistic needs no oracle trajectory, which the old exponent implicitly chased.

**Why silver, not gold.** (i) The record: dossier and predictions both record "bounded_jumps 99 bounded, 1 void"; the shipped script gives 100/100 bounded at the author's seeds and at fresh seeds. `b12probe.py`'s mtime is *after* its own `.pyc` — the script was edited after the run that produced the recorded numbers, and the amendment's claim that `b12probe.py short` "reproduces everything" is false for this number. The lab's 5 Oct lesson is explicit: silvers fell short of gold on exactly this. (ii) It cannot be adopted within one step: the phase-tied oscillation false-alarm band (up to 100 %) sits on the plausible shape of the plane's real residual; the wire-up would fail today. (iii) Lessons 2–5 are named tests without probes (the author says so), and lesson 5's gate audit stayed inconclusive.

**Why not lead.** Reproduced end-to-end, deterministic; held-out predictions held under fresh seeds and fresh parameters; novel on the record; the exact case that killed the previous candidate is separated at 92–95 % with zero false alarms; honest miss reporting and honest disclosure of the estimator history.

## The one experiment that would make it gold

Re-order the guard so the τ/periodicity check precedes *any* verdict (or subtract the register's phase-tied component before F), then show on fresh seeds that the bounded oscillation family (P ∈ [T/4, T], quasiperiodic) goes void/bounded while the slow-leak family (RMS t^0.12–t^0.25) stays caught at ≥ 90 % — and re-freeze the record so every printed number regenerates from the shipped script. That closes both gold blockers in one run and hands B12-v2 its statistic for the wire-up on the plane's real energy register.

## What the author missed

- The F-before-guard precedence is the root of the false-alarm band: the compounding verdict is unguarded. The risk was disclosed but never measured; it is 100 % at the natural period, not a corner case.
- The near-unit-root boundary (ρ between 0.99 and 0.999) and the detection latency of a fresh leak (a whole window) were unexamined.
- The post-run script edit went undisclosed; one recorded number cannot regenerate — the same record defect that pinned previous runs at silver.
- Lessons 2–5 each name a cheapest test but run none; the per-gate fail ledger (lesson 5's real deliverable) was not built, leaving "best part is no part" as assertion.
