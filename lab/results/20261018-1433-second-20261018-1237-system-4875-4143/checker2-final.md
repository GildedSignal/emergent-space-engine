Working...
**Grade: gold** — written to `check2.md`, with the author's page corrected in place.

**What I did (independent of checker 1):**
- **Reproduced from a clean tree**: applied the author's three patches to pristine HEAD myself, rebuilt (40.6 s), re-flew. My numbers match author and runner-regen within load noise: b10000 260.7–264.6 ms → r10000 1.20 ms p50 (217–220×); engine digest `03abdbc9…` bit-identical with/without `--rows` at all three sizes (71/1,071/10,071).
- **Three adversarial arms, one beyond the author's domain**: (1) held-out decade **10⁵ bodies** (author stopped at 3×10⁴): p50 **1.28 ms**, engine p99 4.47/max 4.86 ms, wire 26.3 KB, worst hitch 686.8 ms ≈ exactly one fill cohort (6.8 µs/body) — the flat-in-N claim and the transient scaling both extend; (2) held-out **seed 3 + audit**: 0 violations / 822 drawn rows, panel 0; (3) **2× duration**: hitch counts [32,32,3] identical at 360 and 720 frames — transient bounded, not periodic.
- **Tests**: universe crate 10 lib + all integration suites pass on the patched tree; the `nladder` link failure is the pre-existing macOS-only symbol, as the dossier disclosed.
- **Novelty**: closes the published page's open direction #1 (2df1's deletion was example-harness only); first measurement inside `Session::step`.

**One instrument error found and corrected**: the audit is **not** "charged to no channel" — its full `gather_cached` runs between `t3` and `dash.parts` in `session.rs:180-193`, landing in the wire channel and the timed frame (audit arms: wire max 245 ms, worst 271.7 ms @f89; non-audit arms ≤ 0.15 ms). No dossier number comes from audit-arm tails, so no result changes; the page now warns future readers to take tails from non-audit arms only.

Tree left pristine; my probe JSONs live outside the repo in `/tmp/c2/`.
