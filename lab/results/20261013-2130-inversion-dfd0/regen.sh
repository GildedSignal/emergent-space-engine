#!/usr/bin/env bash
# Regenerates every number in dossier.md from the shipped tree + this run's patch.
# The runner applies work/patch.diff before this runs; the guard re-applies it only if needed.
# NOTE: the probe's specific ticks/digests are load-dependent — that IS the finding. The test
# asserts the invariants on every machine: (a) the same session at two budgets records two
# different flights (inputs or digest differ), (b) every file replays to itself exactly,
# (c) --replay-all over all of them exits 0. Exact hex varies with box load, by design.
set -euo pipefail
cd "$(dirname "$0")/../../.."  # repo root
RUN=lab/results/20261013-2130-inversion-dfd0
grep -q one_session_two_loads_two_flights xtask/src/universe/flight_tests.rs || git apply "$RUN/work/patch.diff"
cargo test -p xtask one_session_two_loads_two_flights -- --nocapture 2>&1 | tee "$RUN/regen-output.txt"
