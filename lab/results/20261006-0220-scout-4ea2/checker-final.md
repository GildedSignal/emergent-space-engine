Working...
**Grade: gold** — written to `lab/results/20261006-0220-scout-4ea2/check.md`; nothing else in the run folder touched.

**What I did (30 min, all ≤ 2 GB):**

1. **Reproduced bit-for-bit.** Plane B13: FAIL 60/64, worst ΔE 1.26e0, 9 draws replaced; trace has exactly 2 ships with `handoffs=0` (kicks 2 and 113 — the entry never fires), 62 with handoffs 1–2, kicks 89–427, events 161–644. Falsifier rerun: every dossier cell matches (L1 0/60, L2@1.0 7/41, L2@1.5 0/60, L3@1.5 59/60 worst 1.43e-2, set B 15/15 worst 2.38e-3, events 65–120, selftest 6.54e-12, 12/72 excluded).
2. **Verified transcription** against `restricted.rs`/`assist.rs`: scene constants, `ship()` algebra, gate 1e-2, CONVERGED 1e-4, t_exit protocol, `heliocentric` E/L, judge rel_err — faithful, not a strawman. `patch.diff` empty, clean tree.
3. **Held-out:** predictions.md (02:29) precedes the decisive run (json 02:44); ledger honest (P3 held; P1/P2/P4/P5 failed-as-reported with mechanisms).
4. **Three adversarial probes of my own, all holding:** fresh RNG seed → L3@1.5 **58/58**, worst 4.88e-3 (incl. e−1 = −2.5e-10); slow+deep corner (q∈[1.2,3] R_p, v∞≈1.7–2.2e-5) → 8/8, worst 6.75e-4; door sweep 1.0/1.25/1.5 → monotone improvement on every set, independently corroborating the door-radius mechanism.
5. **Novelty:** resolves m-meso-motion's condition ("deep flybys still fail") and H0214's named next step; no prior entry measures the one-event insufficiency or the door radius.

**Demoting findings (recorded, none fatal):** "error flat from 91 to 5796 kicks" is loose — on my probes it falls ~10²× then floors, always ≥70× under gate; L1 is the plane's cadence rule in form but at 1/64 vs the plane's 2^7; the detection leg at 1.5·SOI free-rides on the start condition; only 2 of the 4 plane failures are traced to handoffs=0. The integer wiring stays the named adoption step.
