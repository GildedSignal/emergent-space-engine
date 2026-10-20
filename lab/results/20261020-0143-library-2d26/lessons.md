# Five lessons for the wave's three exits (prepay / amortize / delete), the gate's cadence, and the invariance

All quotes verbatim by Readwise id, 5/5 byte-identical against a fresh 770-doc/4,590-highlight export (`work/verify_quotes.py`).

1. **The gate must live in the player's environment.** Taleb — "the notion of 'performance' needs to be associated with a specific environment and necessarily predictive of it" (IQ is largely a pseudoscientific swindle, [519760175]).
   *Mechanism:* the same wave is two different diseases at two cadences — rtf 2000: 110 frames over, p99 319 ms, lag 32 s; rtf 400 (the play side): 13 frames over, **p99 11.94 ms = at budget**, one 1.59-s freeze, lag 5.5 s recovering to 0.
   *Change:* the burst's freeze gate is judged at play cadence (one frame's freeze length), never over-count at rtf 2000. *Test:* the rtf-400 arm at 3×10⁵ (unflown).

2. **An 18-second window shows variance; the rung's law is the return.** Taleb — "Over a short time increment, one observes the variability of the portfolio, not the returns" (Fooled by Randomness, [886213225]).
   *Mechanism:* the wave's over-budget excess scales ×2.37 per ×2 K (6.6 s → 15.7 s) while the flight's whole ebb is K-flat (slack 5.3/5.1 s); excess/total-slack 1.26 → 3.13: amortization is horizon-bound and the horizon shrinks as K grows. The lag itself is honest — 0.0 s at flight end in every arm: bounded deferral, no compounding (PRINCIPLES 13).
   *Change:* adopt the drain (ee4d/1d47) with its price named — presented-time lag ∝ K (9.2/21.8 s of play-cadence lag at 10⁵/2×10⁵) — and cap the rung where lag crosses the player-differentiable floor. *Test:* the stagger arm deletes the excess at 2×10⁵ (below).

3. **Empirical agreement is not the mechanism.** Feynman — "The first principle is that you must not fool yourself—and you are the easiest person to fool" ("Surely You're Joking", [678770473]).
   *Mechanism:* 4063's own verdict — OFF = ON = REACH across 34 cut runs, yet "the invariance is empirical, not structural"; 1d47's checker saw bistability that 4063 did not reproduce. Two runs sharing a harness agree for free (the memo lesson, 5 October).
   *Change:* the adoption ships the one-line structural guarantee (canonical bindings at capture) or re-freezes on the M1; never "34 more agreeing runs". *Test:* 1d47's checker's bistability scene at 2×10⁵, several schedules — a structural fix passes by construction.

4. **Delete the synchrony before scheduling it.** Musk via Isaacson — "Always wait until the end of designing a process—after you have questioned all the requirements and deleted unnecessary parts—before you introduce automation" (Elon Musk, [779884732]).
   *Mechanism:* the wave is burn-gated mint-synchrony (0c0f checker: coast has no wave; the stagger rides the per-body kick-grid shift, birth-stagger's bill). Scheduling (drain, prepay, allocator) treats a requirement nobody questioned: that the whole doll re-mints on one tick.
   *Change:* the stagger precedes all allocator/compute-ahead work; compute-ahead is demoted to the small-N band (lesson 5). *Test:* stagger the burn's re-mint by one tick per body at 10⁵ — excess 6.6 s → ~0.

5. **The coverage law selects the lever per rung.** Brown — "assess context and discriminate between problems, selecting and correct solution" (Make It Stick, [1045882272]).
   *Mechanism, measured:* prepay coverage = pre-onset ebb / wave excess. Onset is game-time-locked (frame 458/455 at rtf 2000, 2,067 at rtf 400), so ebb-before-onset is K-flat (2.0 s at rtf 2000; 20.8 s at rtf 400) while excess ∝ K^1.24 — coverage(rtf 400) = 6.0 / 2.55 / 1.54 / 0.34 / 6×10⁻⁵ at 10⁵ / 2×10⁵ / 3×10⁵ / 10⁶ / 10⁹; at rtf 2000 it is 0.31 / 0.13 already dying.
   *Change:* the ladder table gains a coverage column; prepay is a ≤10⁵ patch (a band-aid in Julien's language), amortize covers ≤ ~3×10⁵ at play cadence, only deletion scales. *Test:* one flown 5×10⁵ rtf-400 arm against the composed crossover 4.6×10⁵.
