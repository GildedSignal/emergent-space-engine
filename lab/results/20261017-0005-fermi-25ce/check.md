Grade: gold

**Abstract.** Claim: at 10⁹ the schedule ("who is due") costs no per-body bytes, and that fact chooses the store class — only a class-major per-body store (21–40-bit records) plus ≤1.8 MB cursors fits; explicit entries (7.1–9.1 GB), due-rings (≥3.6 GB Shannon ordering floor) and per-frame rescans (measured 21.7–25.7 ns/body, ≥8 frames of bandwidth floor) all die — so the bijective program class is excluded by enumeration, not by its bytes, and the board's "queue" first-break candidate is dead. Reproduced bit-for-bit; ledger cross-check 13.0 vs 13.2 cores (0.985). Checker verified beyond the author's range: 10⁹-scale concentration 1.050–1.055 (claimed 1.05), N=10⁸ dial 1.186 vs law 1.179, mixed dyadic steps 1.17× safe. Adoption: a wiring-time layout choice; the quantized-stagger law line still needs B-gates.

## Reproduction

`python3 fermi_calendar.py` (2 s): P3/P4/P2 identical digit for digit against `regen.out`; P1 timings 24.6/23.0 ns/body (shared box; author 23.1/23.3, regen 21.7/22.4) — same verdicts. `work/patch.diff` is empty (no tree edits — consistent with a constants-cited replica). `predictions.md` mtime 00:13:04 precedes the script (00:16:02) and its output (00:16:10): pre-registration is genuine. `proc_pid_rusage` is indeed declared unconditionally (`crates/universe/examples/nladder.rs:17`), so the no-flight-on-Linux claim has a real mechanism.

## Predictions

Held: P2 comb control fails, 512-class concentration 1.06× (≤1.25 predicted), P3 all memory arithmetic, P4 within 1.15× (0.985). Missed, both disclosed in the dossier: P1's 1–5 ns/body band (measured 22–26 everywhere — the kill strengthens: dead by ~1,300 frames, and by ≥8 frames even at the bandwidth floor with a 21–40-bit store); P2's working-point figure at the sim's μ=7.4 (2.84×) — the law itself (max/μ = 1+√(2lnF/μ), 1.8% error at μ=7.4) is confirmed and, per below, now measured at scale. The author's own framing error (the dial is set by frames-per-interval, not N/budget) was found and reported by the author.

## Attack (4 cases, all outside or at the edge of the author's range)

1. **The 10⁹ extrapolation, run for real** (author only extrapolated): multinomial(10⁹, 1/135,079), 5 seeds → max/μ = 1.050–1.055 vs claimed 1.05, law 1.056. Holds.
2. **The author's own hash-class model one decade up** (N=10⁸, μ=740, author ran 10⁶): K=10F → 1.186 vs law 1.179; K=F → 1.213. Saturation at K≈F confirmed.
3. **P1's declared held-out arm (3×10⁷) — never run by the author**: 25.7 ns/body, and 21.9 at 10⁸; flat in N, within the 2× held-out bar. Verdict unchanged. (Discipline gap: the pre-registered held-out size was silently swapped to 10⁷; I ran the declared one.)
4. **Mixed dyadic steps** (the shipped reality — steps are powers of two, `step.rs`; the author assumed one composed interval): 8 step groups at N=10⁸ → max/μ = 1.17, cursor total 56.6 MB, inside the ×100 fan-out budget (175.8 MB). No hidden concentration or cursor blow-up.

**The named falsifier, read.** Open direction 1 ("is the bulk's next-due derivable without carried per-body state?") — I did the read: the shipped interval law is `aligned` (`crates/universe/src/step.rs:107`, block time steps: on-grid intervals are `step`, one stub after a handoff/decision, then back on the absolute grid). No carried chain state exists in shipped code (ES_CHAIN was a lab patch arm, absent from crates). The stability premise of form (d) holds against the shipped law, which is stronger evidence than the wiki record the author cited.

## Novelty

No page prices the schedule's bytes ("who is due"): `memory-h-live` has no due/cursor content; `frame-cost`'s queue runs (4955, 4211) price the live queue's **CPU** at 10⁶ (heap vs wheel); `scan-queue` is the player's scan; the `encounters`/`belt` "conjunction calendars" are who-meets-whom structures (killed on other grounds). The cross-claim — 98cb's bijective program class fits bytes but fails **enumeration**, so the calendar axis excludes it from the flyable store — is new and adoption-relevant; e7ef's ledger is complemented, not repeated.

## The page

Faithful to the evidence; two overstatements corrected in place: "the adopted hash stagger (f82a)" (nladder's c840 record kills the stagger *configuration* and sends the cure to the birth program; f82a's own gates are open — kick-cadence od8) and the 10⁹-scale concentration figure, now marked as checker-measured. Not closable: one run, one topic.

## Goal fit

Board focus item 1 ("which term breaks first… the queue") and item 5: it kills the queue as a first-break candidate (a premise shown wrong) and deletes a per-body calendar structure before it is built. PRINCIPLES #17: "the best part is no part" — the calendar is the deleted part; #6 survives with the page's stated boundary (the generator is the birth program; the standing store must be per-body). Fermi-replica epistemics match prior golds on this board (fe6b: measured at 10⁶, arithmetic to 10⁹), with an independent ledger cross-check (0.985) on top.

## What the author missed

- The lens note is right that cursors answer WHEN not WHO, but the membership consequence is understated in the claim sentence: form (d) silently requires the **per-body record** class; the "no per-body bytes" headline is really "no per-body *schedule* bytes — the store pays instead" (the dossier's third wrong-maker says this; the claim's first line can be misread).
- A display bug: P1's "frames of budget" divides ns by s (×10⁹ slip — "1.3×10¹² frames" should read ~1,300). The dossier quotes only the correct "0.13–23 s vs a 16.7-ms frame", so nothing false reaches the claim.
- The pre-registered 3×10⁷ arm was swapped for 10⁷ without saying so (it holds when run).
- The bandwidth floor assumes 8 B/body; the 21–40-bit store would halve it (~2.5–4 frames) — still dead, but the "8 frames" figure is for an 8-byte store.
- "Exactly 1+√(2lnF/μ)" is 1.8% off at μ=7.4 — confirmed within 2% at every μ I tested, but "exactly" overstates the small-μ end.
