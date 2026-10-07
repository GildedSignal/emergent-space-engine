Working...
Check complete. `check.md` written to the run folder; nothing else there touched (benchmarks rebuilt in `/tmp/check-fermi`, outputs diffed against the stored files rather than overwritten).

**Grade: silver.**

What I did and found:

- **Reproduction:** `budget.py 3.2 19.6` regenerates `budget-out.txt` byte-identically. Benches reproduce with identical checksums at 2× worse numbers on this loaded box (fold 6.3 vs 3.2 ns, rand16 28.7 vs 19.6 ns) — every conclusion survives. Every headline number re-derives independently from the cited constants (H0190's 32.5 kicks/orbit + 114×, H0210's 29 µs + RTF 100, law.md's 16 B tube + 0.05 compiles/kick, 0.126 bits/body, r8's 786/427).
- **Pre-registration holds:** `predictions.md` (18:05:53) precedes `bench.c` (18:06:11) and `bench-out.txt` (18:06:49); the dossier's self-scoring is exact — P4–P6 held, P1/P3/P9/P7/P8 failed with all failures disclosed.
- **Novelty:** H_live was explicitly "not measured yet" in HANDOFF; now bounded (435 B/h folded, scars breach 4 GiB at 10⁶ unaveraged ships — folding is load-bearing).
- **Adversarial finding (the reason it's not gold):** the frontier table never intersects the memory wall. Strong-tide bodies need resident 16 B tubes, so 4 GiB caps that population at 2.5×10⁸ — the best frontier row (N* = 1.48×10¹⁰) needs 237 GB of tubes and is unreachable by ~60×, and the "designed corner fits 15× under" scene (all 10⁹ strong-tide) is compute-only true, machine-false. The realistic 10⁷-fleet scene and the actionable output (keep q-cadence; measure the plane's cycle-memo hit rate) are untouched.
- **One experiment to gold:** measure the plane's real hot-fold cost on distinct kicks and republish the frontier with the 2.5×10⁸ memory cap — pick-up-able by the queued q-cadence.
