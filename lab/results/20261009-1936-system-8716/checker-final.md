Working...
Check complete. `lab/results/20261009-1936-system-8716/check.md` written; nothing else in the run folder touched (my scripts live in `/tmp`).

**Grade: silver.**

What the check established:

- **Reproduction:** `truth1`, `truth2`, `sweep` all diff-identical to the shipped jsonl (26.9/41.9/94.9 s). The physics numbers are real.
- **The claim's index half is falsified.** The binned U-scan is *not* pure acceleration: it drops 9–11 rule-passing pairs even on the author's own scenes, and my constructed workload (constant-p belt, bimodal e, H=16) makes it miss **66 of 495 true encounters (recall 0.867)** while the naive per-pair rule holds 1.0. Root cause: `n = (U(1−e²))^1.5` — shear has a Δe component the U-distance bin window cannot see.
- **The rule itself survived every attack:** e up to 0.55 (beyond the claimed domain), apse-anti-aligned fleets, T=8192 fine truth — recall 1.0 everywhere.
- **Record defects:** `scale.jsonl` regenerable by no shipped command (I regenerated its fractions myself: 0.718/0.223 — right physics, broken record); "preserved in git history" is false (patch.diff is empty, folder untracked); two failed predictions (evals within 3× of ideal-trigger — actually 36–96× off; sub-√N per-body growth — actually linear) went unreported.
- **Not a strawman:** the ideal-trigger baseline got oracle labels and the board's actual adopted rank-4 constant; the portability criticism of taleb-09b5's constant stands.

Gold path named in the check: bound the bin drift term by Δn's full (U, R) dependence, prove emitted = naive rule on the adversarial class, re-run pre-registered on fresh seeds, ship a command that regenerates the scale row.
