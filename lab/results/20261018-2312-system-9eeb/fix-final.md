Working...
Fixed and verified. `regen.sh` failed because its `cd "$(dirname "$0")/../../../.."` climbed one level past this checkout's root (`…/emergent-space-engine/lab-2`); it now walks up to the nearest ancestor with a `Cargo.toml`, and I added the missing `--features prof` pass so the dossier's FIT column regenerates too.

Verification, end-to-end exactly as the runner does it (`work/patch.diff` applied, then the script):
- Full regen run: exit clean, 399 s; space + universe suites green gate-off; standing `memo.rs` off-arm passes at 0.947 with the on-arm guard-trip disclosed in the script's own echo.
- Every dossier number matches: 796 cycles, 1,764 rebinds served by 58 cold builds (3.29%), 85 cells, period max 6.786e-4 / med 5.839e-5, advance max 1.322e-4, knot delta 0, exact-key recurrence 0.000, outcome hash `0x7f43b75a59fff0f3` identical on rerun; off-arm period error exactly 0 with the served memo untouched.
- New FIT pass: on-arm `fit_ms=45`, off-arm `fit_ms=125` → −64%, the dossier's headline (46-47 vs 129 ms, same jitter band).

Claim: regen.sh now regenerates every number in the dossier from the shipped code plus `work/patch.diff` in under 15 minutes.
