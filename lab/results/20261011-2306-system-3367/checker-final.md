Working...
Check complete. `check.md` written to the run folder; nothing else touched, tree restored to clean, no commits.

**Grade: silver.**

**Reproduction (clean tree at a838a284, patch applied):**
- `--bench --rtf 100 --seconds 30`: digest `41343a14…` and cut 609076340 **bit-exact**; frame split and cost-by-kind *ratios* hold (engine 17% vs 16.4%; player/fleet 23× vs 25.5×).
- `--kick-bench`: replay digest `0e02bf0f…` **bit-exact**; memo integers identical (1125 rebinds, exact 0.0%, 51 keys, 95.5%).
- Absolute µs/item ran ~2× faster on my quieter pass (player 473 vs 1009 µs) — contention band, orders of magnitude intact.

**Adversarial (4 cases):** exact 0.0% and quantized 94–97% held at seed 7, rtf 1000, and a 200-member fleet (126 keys — key count scales with fleet, the *rate* is the robust number); paced vs unpaced at one cut give one digest (schedule-independence, matches the author's saved unpaced digest).

**Why silver, not gold:** P4's threshold missed (p99 9.2 vs <8 ms, disclosed; my quiet run's 3.1 ms shows it was window contention), and the headline ~95% deletion is the already-assigned memo hook's gain — this run is a reproduced, honest audit that prices it and exposes two real instrumentation gaps (profiler wired to an unused path; zero handoffs in the dashboard's scene), not a 10× move itself. The named gold experiment: wire `Orbit::compile` into the profile hook (or prototype the jet rebind on the kick bench) and show the kick path's *time* collapses ~10×.

**Defects recorded:** the Commands block fails as written (build needs `--features emergent-space/profile` once patched); "25–50×" overstates (within-run 18–30×); "1158 kicks" conflates samples with the 1125 rebinds.
