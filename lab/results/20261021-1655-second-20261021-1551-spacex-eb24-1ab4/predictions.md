# Predictions (1ab4, second author on eb24 — written before the decisive arms)

Arms: B = 3e4 coast 20 s rtf 100 (already flown to prove the counters: eligible 188, miss_me
188/188, other-dirt min 52 — tuned on, disclosed); held-out: A = 3e3 coast, C = 1e5 burn rtf 100,
tiny belts n = 1/3/8 coast (the base plane alone), 3e5 coast (3× the largest, the checker's
adversarial size), and 3e3 burn (the checker's corner). The decisive question: does the shipped
plane ever offer a *quiet* eligible pair (other-dirt == 0: nothing but the player's own apply
mutated the store between two eligible captures), and can v1 fire on one?

1. **v1 hits 0 on every arm** (mechanism, not luck: the player's own `apply` unconditionally
   `put`s its row immediately before `encounters_for_player` — universe.rs:661→772 — so the
   global epoch rises by ≥ 1 between any two captures; `dg == 0` is unreachable at this call
   site in any scene, quiet or not).
2. **miss_me == eligible on every arm** under v2 (the same put bumps the player's row epoch).
3. **No arm reaches other-dirt 0:** the eligible-pair gap (~5 game-s) carries a Poisson load of
   other bodies' rebinds (≥ 3 events/game-s even from the 28-body base plane alone), so
   min(other-dirt) ≥ ~20 wherever eligible > 0 — the "settled universe between kick waves" quiet
   stretch does not exist on the shipped plane at any belt size, including n = 1.
4. **Tiny belts still eligible:** n = 1/3/8 have eligible pairs (eligibility is the player's own
   (event_time, step) repeating — N-independent), all killed by miss_me, other-dirt > 0.
5. **v3 on B (unflown by eb24):** me-by-value passes on most of B's 188 eligible pairs (an
   eligible pair re-puts the same rec), then **miss_near ≈ eligible** fires (the other-dirt 52
   includes near rows' rebinds; the memo missed all 188 through candidate changes — the same
   dirt), miss_reg small, hits 0. On C the checker's attribution (me 0-miss, near 723, reg 138)
   reproduces with the new counters showing C's other-dirt min ≥ 20 too.
6. **The always-on epoch cost is invisible at flight level:** pristine scanpre0 vs patched
   scanpre0, arms A and B, interleaved ×3: |Δp50| under the shared machine's run-to-run spread
   (the bookkeeping is a few atomic adds per rebind and one wide snapshot per capture against
   40–70 µs frames); the honest record is the code fact (always-on) plus this bound, replacing
   eb24's "off = shipped paths" wording, which is true of outcomes, not cost.

Kill criteria: if any arm shows v1 hits > 0, or other-dirt 0 with v1 still missing being
unverifiable, or miss_me < eligible anywhere, the structural story is wrong and the dossier says
so. If the patched-vs-pristine Δp50 is stable and > 20% on either arm, the epoch bookkeeping has
a real price the wiki must carry as a number.
