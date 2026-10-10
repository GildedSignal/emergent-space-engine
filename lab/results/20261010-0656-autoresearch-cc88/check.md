Grade: silver

**Abstract.** Claim: `num::cos4` (four interleaved copies of `cos`'s exact op sequence) in the two Gauss–Legendre panel quadratures cuts kick cost ~16% with bit-identical law. Reproduced in a clean tree: all 8 digests (replay + universe × seeds 1–4) equal the author's and the clean baseline's; both suites green (space 51, universe 54, 0 failed). Medians: seed 1 87.9→73.9 µs (−16.0%, author −15.6%); my adversarial seeds 5/7/13/42: −13.6 to −14.6%, digests identical, `refused` 0. My independent sweep (300k quads, different generator, out-of-domain extremes) agrees with the in-tree 200k exactness test. Gain 1.19×, honestly reported; gold needs 10×/deletion (lab rule). Adoption: two files, no API/law change, trivial.

**Reproduction (clean tree, `git apply work/patch.diff`, 3 full builds).**
- Baseline digests match the dossier on every seed (s1 `59ea9969…`/`13cfe88b…`, s2 `d608ef86…`/`44f39a11…`, s3 `84f30efe…`/`cac2c8c7…`, s4 `1f8769f7…`/`0b6ceac7…`); patched digests identical to baseline; `refused` 0 on all 12 runs.
- Numbers that differ, and why: my first baseline pass on seeds 2–4 read 88.8/123.7/109.8 µs (another window's run was loading the box); re-baselined under load ~2.9: 57.4–58.5/88.3–89.9/71.3 — matching the author's 58.70/88.05/71.85. Patched absolutes 49.9/74.8/60.6 vs author 49.34/73.73/60.14. Fair deltas −15 to −16%.
- p99 (author: "falls too"): mixed here — s1 371→380 (worse), s2–4 371–391→365–371 (better). Tail is noise-dominated on this shared box; the median claim is what reproduces.
- Tests: `emergent-space` 51 passed (dossier says 41 — miscounted, immaterial), `emergent-universe` 54 passed 1 ignored.

**Attack.**
1. Held-out seeds of my own (5, 7, 13, 42): digests bit-identical, gains −13.6…−14.6% — within the pre-registered ±5 pp of seed 1.
2. Exactness beyond the author's test: my `cos4_adversarial_checker_sweep` (removed after running) — 300k quads from a different LCG plus adversarial values (±1 around 0/PI/PI/2 and PI/64 grid points, negatives, psi > PI, 2^61…2^64, 2^100, i64/i128 extremes, mixed-domain quads): zero mismatches. Also verified by construction — each lane runs `cos`'s operations textually identically (same casts, same shifts; integer ops vectorize without fast-math semantics), and both quadrature rewrites preserve psi visit order and accumulation order.
3. Digest sensitivity: the patch adds no struct fields or `Debug` changes; the author's own noted hazard (format-sensitive digest) is not triggered.

**Predictions.** `predictions.md` pre-registered (tuned seed 1; held-out 2–4; three named held-out claims). All three held on my re-measurement: gains within 1.7 pp (mine: ≤2.4 pp), digests equal + `refused` 0, made-kick gain −11.8% ≥ half of leavers' −17.0%. The author honestly reports the H-B/H-C predictions (i128 division cost) failing and being reverted by measurement.

**Novelty.** No interleaving/lane work in docs/HISTORY.md or docs (grep: cos4/interleave/Horner/SIMD); kick cost is the documented limiter (H0210 "kicks cost 29 µs", H0211 "kicks still dominate"). The memoization negative is the 5 Oct taste-log entry, cited and independently reconfirmed, not re-claimed. `keep.patch` == `work/patch.diff` (md5).

**Goal fit.** Board focus line 1: kicks dominate; this cuts µs per kick at fixed behaviour, zero law change ("Simplify, never dumb down", "compute only surprises" — same compute, overlapped latency). But 1.19× is below the gold bar by the lab's own definition (10×, deletion, or premise-kill), and the author says so.

**The one experiment for gold:** none exists inside this configuration — a constant-factor polish cannot reach 10×. Gold on this bottleneck is deleting the rebind compile itself (the re-anchored jet, law.md "Not adopted", gold-graded once), and this run's profile is the evidence that pins that: compile ≈ 84% of bind, `cos` was 33 µs of 63 µs, division/isqrt are *not* the cost (B2/C reverted), so ≈40 µs/compile of irreducible div/add/knot-stores remains for every exact recompile. Next run should take the jet; on adoption, `cos4` rides along either way.

**What the author missed.**
- p99 on seed 1 did not improve in my reproduction; tail claims should carry rep spreads like the medians do (P12: smoothness is p95/99).
- The space-suite count (41 vs 51) is wrong in the dossier; record hygiene is what past silvers lost gold on.
- The profile's per-op table (759 cos × 42.9 ns) is arithmetic-consistent, but no command regenerates it — the phase-timer instrumentation was stripped, so the 84%/33 µs split is not re-verifiable from the shipped patch.
- fast_quad (strong field) untouched and unmeasured here; the author flags it, but on a board where B17/Kerr scenes are the next gates, the weak-path-only tuning deserves one sentence of risk, not just lens honesty.
