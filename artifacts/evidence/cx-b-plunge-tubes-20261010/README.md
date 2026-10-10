Incoming plunge tubes; partial result, not gold. Work is uncommitted on `wt/cx-b-plunge-tubes`; base/main a838a284.

[Gates](gate-detail-lines.txt) retain every before/after detail line; [raw runs](after.txt) include machine state (M1, AC, load, swap, thermal status). Original restricted-sandbox and full-access baseline engine results are both preserved in [before.txt](before.txt); E1's Metal availability changed with permissions, not this patch. E6 lacks prepared mutant provenance and E9 remains failing.

[Tests](tests.json): 112 passed, 1 failed, 1 pre-existing ignored; all 9 new tests pass. Each ran separately below 60 seconds; sampled peak process RSS 1,043,939,328 bytes. [Resources](resources.json) retain bounded gate/build runs. These are observed RSS samples, not an OS hard memory limit.

The sole failure is the unchanged `a_stuck_ship_keeps_a_view` assertion requiring the old radial-fall refusal. [Controls](controls.txt) show 1053 refusals before versus zero after, with a live ship and valid view. This expectation contradicts the requested radial-fall support; no frozen assertion was edited. The old envelope test's only edit unwraps the newly optional turning key, without changing its assertion.

B13's remaining outward near-radial bound legs require a return through an apoapsis; this compiler only handles inward arcs. The retained refusal diagnostic used an intermediate test binary and is a probe, not final-source qualification. Final-source B13 gates remain failing at every tested cadence. Horizon compiler readout is finite in proper/advanced clocks; the plane's horizon clock and absorption ledger remain unbuilt.

The first integration used remaining arrival time for kick spacing and timed out the fleet-dissolution control. Local gravity/crossing time fixes that shrinking-step tail; the final untouched lifecycle/replay tests pass, and a new test checks endpoint-independent motion scale. No performance improvement is inferred from the lifecycle wall times.

[Provenance](provenance.json) names source/dependency/binary hashes and verifies frozen judge/law/throttle-test sources against base. [Summary](summary.json) is machine-readable. The implementation contract and explicit refusals live in [PLUNGE.md](../../../crates/space/PLUNGE.md). No merge, journal or handoff edit.
