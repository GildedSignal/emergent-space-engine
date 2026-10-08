Working...
Check complete. `check.md` written; nothing else in the run folder touched.

**Grade: silver.**

What I did:
- **Reproduced everything**: built `exp` in a clean tree (empty patch.diff — self-contained), ran F1/F2/X/B — all 16 result lines match the stored JSONL bit-identically on every counter (pairs/evals/checks/hits/sections/missed/matched); only wall times differ (shared machine). `BANDS=1 F2` regenerates the maximal-band row (4,957/439,206/0 missed); `BANDS=1 B` regenerates the margin-712 self-destruction; `K_OVERRIDE=0/1/2` gives 98/12/4 missed vs adaptive 0 — the k-boundary is real. Truth independence verified in `truth.rs` (Lipschitz-bounded conservative advancement, Halley vs Newton).
- **Found the kill**: a convoy scene — F1's exact a/e distribution, mean longitude clustered in 0.1 rad, which is literally "a fleet on one orbit" (the motivating case) — **silently misses 11,736 of 15,497 truth encounters (76%)** while the crate's cone misses 0. Root cause: `k` derives from mean spacing `TAU/m`, assuming uniform longitude density; clustered phases (convoys, Trojan clouds) violate it ~63×. Two more adversarial scenes (σ_e=3e-2 hot formation; a-spread 1e-6 Trojan) hold exact, so the failure is specifically phase clustering — absent from the author's disclosed risk list, and silent (0 false positives).
- Also flagged: predictions.md declared different scene parameters than were run (N=800→500 etc., undisclosed), and the "k=138" negative-control number isn't regenerable from the shipped binary's output.

Silver not lead: the unification shape, drift-bound tier selection, P5's honest falsification, and the cost numbers are real, reproduced and novel vs taleb-09b5/HISTORY. Gold path is one step: replace the rank-count scale with an angular window (sound under local density), re-run all scenes plus clustered convoys, judged under kicks by r8 v4 case (d).
