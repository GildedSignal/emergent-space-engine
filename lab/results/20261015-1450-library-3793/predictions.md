# Predictions — 20261015-1450-library-3793 (written before the trace flight and replay)

Setup: the shipped engine (patched only with an env-gated read tracer on the compiled-entry
read sites: `readout`/`orbit_state`/`terminal_tick`/`step_for`/`next_exit_with`/
`next_periapsis`/`next_impact`/`plan_terminal`/`range_of`/`source`) flies the bench script
at members = 10^4, seed 1, rtf 100, 600 game-s, unpaced. The trace (u32 catalogue keys, one
entry per in-flight read) is then replayed offline through bounded caches of K = 64..8192
entries under two policies: plain LRU, and 2Q (scan-resistant: admit on the second reference,
Johnson & Shasha 1994). Baseline: "retention until next kick" (1d52's global retention,
85-90% hits, no bound).

Not tuned on any of these (the flight has not run at the time of writing):

1. **The hot set is N-independent and small.** From 1d52 (hits identical at 10^4 and 10^5),
   I predict the distinct-key working set that carries >= 80% of repeated reads is <= 1,024
   keys at 10^4 members (catalogue ~10^4+ live).
2. **2Q at K = 1,024 keeps >= 70% of the reads hit** (against the 85-90% ceiling of global
   retention), because the recurring readers are the locals (dolls, sources, the player).
3. **Plain LRU at the same K collapses under the wave's scan**: kick planning walks every
   kicked body once per wave (1d52: "the resolver's own kick planning reads every kicked
   body"), which evicts the locals wholesale. I predict LRU(1,024) hit rate < half of
   2Q(1,024) on the post-burn-in trace.
4. **The miss bill stays negligible either way**: even at 0% hits the re-mint cost is
   4.6 us (scout-760f) x misses; the decision is memory (bounded K), not compute, so the
   cheapest safe K is the one where 2Q's hit curve knees.

Kill criterion for the lesson: if LRU(1,024) is within 10% of 2Q(1,024) on the post-burn-in
trace, the scan-resistance lesson is decorative here and the adoptable cache is plain LRU
(simpler); the dossier must then say so.

Adversarial cases I will also run (not tuned): replay with the first 10% of the trace
discarded (burn-in); replay of the trace with the wave window only (the middle third).
