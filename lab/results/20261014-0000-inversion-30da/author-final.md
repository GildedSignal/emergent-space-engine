Working...
All deliverables are in place: `predictions.md` (pre-registered), `dossier.md`, `regen.sh`, `wiki/replay-gate.md`, `work/growth.json`, and the patch (`xtask/src/universe/flight_growth.rs` + its registration), with both tests passing on shipped code.

**Claim:** the merge gate `universe --replay-all` silently stops checking flights as play accumulates — a frozen 55 s budget over an append-only corpus, with unreached flights skipped at exit code 0 — and measured on shipped code it holds only ~19 minutes of total play at the recorded real-flight density (a budgeted one-hour session alone would need ~174 s of replay), demonstrated end to end with a 13-flight corpus where the gate skipped the longest committed real flight yet still reported `0 regression(s)` and success.
