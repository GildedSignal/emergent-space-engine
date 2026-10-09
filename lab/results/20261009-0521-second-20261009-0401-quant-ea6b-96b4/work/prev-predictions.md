# Predictions (written before the decisive runs)

Question: what does one kick of the plane's resolver (motion law v2) cost in wall ns,
where inside it the time goes, how much of it is memory latency (cold vs warm caches),
and what ship-count × rtf capacity that buys at a 60 Hz frame budget?

Not tuned on: this machine has never run these benches; the law v2 (6 October) has not
been kick-benched on record since H0213's tail regression work.

Predictions:

1. **Cost level.** Median kick on this Linux/x86 box: 10–60 µs (H0210 measured 29 µs on
   the M1 before law v2; law v2 added the energy register and the partial step; cloud
   timings are same order of magnitude, not comparable). Leaver (fleet member) kicks
   worse than made-body kicks, ratio < 4.
2. **Stage share.** The rebind's cycle work (bind/compile in crates/space + crates/universe
   bind.rs) is > 50% of each kick; the drift readout < 20%; the force gather
   (secondaries + tide) < 20%; sigma-delta + planning negligible. Basis: the exact memo
   never hits on distinct kicks (H0213), so every kick pays tube work.
3. **Memory share.** The path is compute-bound, not latency-bound: cold (cache-flushed)
   kicks cost < 1.5× warm kicks. If cold ≥ 2× warm, my read is wrong and the lever is
   layout, not compile deletion.
4. **Tail.** p99/median < 5 within the resolver (one population); the resolver itself has
   no heavy tail — tails in the frame come from encounters, captures and allocator work,
   which this bench excludes by construction.
5. **Capacity.** At the measured ns/kick and the bench's kicks-per-ship-per-frame, the
   pure resolver spends the whole 16.6 ms frame at fewer than ~2×10³ ships × rtf 100
   (i.e. ≥ 2 orders of magnitude short of 10⁶, ≥ 5 short of 10⁹, before any allocator,
   view or gather cost).

Kill criterion for the run: if the benches cannot run inside 55 s each or the instrumented
build diverges in digest from the clean build, report VOID for that half and say so.

Hardware counters (perf) are blocked on this host (perf_event_paranoid=4, no sudo):
no IPC/cache-miss/branch numbers; wall-clock decomposition and cold/warm delta replace
them, and that limitation is stated in the dossier.
