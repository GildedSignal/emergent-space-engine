# The libraAll deliverables are in place. Final state: probe patch saved (`work/patch.diff`, 51 lines), Readwise cache (4,580 highlights), replays, pre-registered predictions (one held, one failed exactly as its kill criterion foresaw), dossier, regen.sh (~6 min), wiki page folded, and the five lessons with verbatim quotes.

**Claim:** the nladder seam's bounded retained-entry cache is priced by replaying the engine's own read trace (a 51-line digest-neutral probe): at every cut reachable in shipped time the flight read stream touches only 428 keys, so a plain LRU of K=512 entries holds 100% of the reads N-independently, 2Q's scan resistance is a named contingency rather than a need, and the ~30-line gold-blocking build now has its policy and size chosen by measurement instead of guesswork.
 window, not to N.** Mechanism: Denning's working set (virtual
   memory, 1968 — sized by observed reference behavior). Change: plain LRU, K=512 (~1 MB,
   N-independent) replaces global retention (retained set 1.0-2.0× N, 1d52). Test (run): LRU(512)
   = 1.000 at every cut.
3. **Under pressure, admit on the second reference — a contingency, not a default.** *"No
   employee makes the same mistake twice. He is fired the first time."* — Asimov, I, Robot (a
   joke's structure; the mechanism is real: 2Q/ARC, Johnson & Shasha '94, Megiddo & Modha '03).
   Change: wire admission only if a trace shows distinct > K. Test (run): +8-14 pts at K=64-128,
   decorative at K≥256 — my pre-registered kill criterion fired; say plain LRU.
4. **The add-back is measured, not guessed.** *"Delete any part or process you can. You may have
   to add them back later. In fact, if you do not end up adding back at least 10% of them, then
   you didn't delete enough."* — Musk, in Isaacson's Elon Musk (7f99's gold, now on memory).
   Change: retained set = the measured hot keys (428 of a 10⁴ catalogue; top-64 carry 67.6%), not
   "every kicked body". Test (run): the trace itself.
5. **Price the policy by replay, not by build.** *"The solution is to ignore what your body is
   telling you and listen only to your instruments."* — Paul Graham, Black Swan Farming.
   Mechanism: trace replay (the ARC method): a 51-line env-gated probe answers every K/policy
   question offline, digest-identical (ca195a2c…). Change: the ~30-line cache build lands only
   after its K is chosen this way. Test (run): this run, ~6 min end to end.

Blind spot: founder-aphorism bias can dress decisions that didn't change; I kept the five that
name one. The failed prediction (scan poisoning) is the lens's own correction: the analogies said
sweeps, the instrument said bisection walks.
