Grade: silver

**Abstract.** Claim: on the motion-law-v2 plane no fixed kick cadence passes the plane's frozen gates, so the board's "fewer kicks at a fixed cadence" is the wrong lever; the cost lever is one full cycle rebind per distinct kick (43 µs). Reproduced bit-for-bit: B13 FAIL at every N=1..9 (N=7: 60/64, worst 2.12e-2; N=9: 58/64, 1.77e-1/1.28e0), the same 9 replaced draws at every N; kick-bench digest identical, median 44.2 µs, rebinds 23/23, zero reuse. Not reproduced: B14 at N=2 — the claimed 59.75 s completion (243/255, apsides 0/53) is in no log and timed out (60.0–60.1 s) in both of my runs. My per-draw probe shows the tail is NoBoundOrbit refusals, not depth. Adoption: re-aim q-cadence; fix the flyby representation first.

## What I reproduced (clean tree, author's binary path, no patch — patch.diff is empty)

- `behave --law plane --gates B13 --plane-step 7` → 60/64, worst ΔE 2.12e-2 ΔL 2.12e-2; `--plane-step 9` → 58/64, worst ΔE 1.77e-1 ΔL 1.28e0. Bit-identical to `work/sweep.log`/`work/extra.log`, same 9 replaced draws. The B13 sweep's h² coarse direction and non-convergent refinement direction are on the record and consistent.
- Kick bench: replay digest `72a4b8c4…` identical, median 44.2 µs (author 43.4), p99 54.9 (59.9), 23/23 cycle_rebinds, exact and quantized hit rates 0.0, refused 0. Zero-reuse and per-kick cost confirmed.
- B14 N=3 isolated: FAIL timeout 60.1 s — the author's sweep was killed before this verdict, so I verified it for them.
- Predictions: `predictions.md` (08:42:59) precedes the sweep (08:43:36+); file times and log order check out. The pre-registered knee hypothesis is honestly reported killed; the negative control (N=1 fails decisively) held.

## What did not reproduce, and what is wrong

1. **B14 at N=2, the second pillar of the headline.** The dossier's "completes in 59.75 s, classification 243/255, apsides 0/53" appears in no log (the sweep log stops at N=3's start line). I ran it twice, once isolated: FAIL timeout at 60.0 and 60.1 s. The claimed margin was 0.25 s against a frozen 60 s wall limit on a shared cloud machine — the verdict is load-dependent and flips under the checker. The unlogged behaviour numbers are unverifiable. The conclusion "B14 has no passing fixed cadence" survives (everything times out here), but "the only cadence its budget admits" is false on this machine, and the specific counts are not on the record. This is the lab's named silver-killer: numbers the shipped run cannot regenerate.
2. **The tail's mechanism.** The dossier says "the 2–6 deepest flybys sit on a cadence-independent error floor". The tree ships the probe (`cargo test --release -p xtask b13_by_draw -- --ignored`, `B13_STEP`), listed by the author under "what would make it wrong" but not run. At N=9 the six failures are draws #5 (q 7.4), #14 (9.7), #27 (4.1), #40 (39.1 — a *far* flyby, second-worst ΔE), #57 (6.7), #68 (5.5); all end alive with fault `Space(NoBoundOrbit)` and 10–330 refused kicks. At N=7 the four failures are a different set (#18, #27, #50, #57), all marginal (1.3–2.1e-2), zero refusals. So the floor is real and cadence-independent, but it is the missing tube for unbound planet-centric states (refusals multiplying with cadence), not depth, and the failing population is not even stable across N. The dossier's mechanism sentence is contradicted by its own named check.
3. Minor: B13 needs 64/64 (`ok*100 >= 99*judged`, assist.rs:130), not "≥ 63/64"; and the ~50 ns arithmetic share of the 43 µs is inference, correctly flagged.

## Novelty and goal fit

No cadence sweep on v2 exists in HISTORY (H0215 has B13 at the default only; the taste log queues q-cadence). The exact-memo-hits-0%-on-distinct-kicks half is known (5 October correction); new is cycle_rebinds = 100% of distinct kicks with the 43–44 µs cost, and the full N-verdicts. The B13 half genuinely shows a premise wrong: board focus #1 reads "fewer kicks per orbit at the same behaviour" at a fixed cadence, and no 2^N passes — refinement does not converge the tail (it multiplies refusals). PRINCIPLES #9 ("A failed expectation is not automatically a failed method: diagnose which one broke") is applied correctly to the fixed-cadence premise, and the run redirects the lever to the representation (H0214's next step) and the rebind cost (law.md's re-anchored jet, currently 1.0 compiles/kick against a designed 0.05).

## The one experiment that would make it gold

Put B14 on the record at an admissible cadence: separate the oracle's cost from the law's on the B14 scene (the author's own third what-if — a law-only timing harness, or a logged run on a quiet machine that completes inside 60 s), and fold in the refusal mechanism from `b13_by_draw` at N=7/8/9. Then "no fixed cadence passes the plane's frozen gates" stands on two recorded, regenerable pillars.

## What the author missed

- `b13_by_draw`/`b13_refusals` already existed in the tree; seconds of runtime would have replaced the wrong "deepest flybys" sentence with the refusal evidence and would have shown the failing set is cadence-dependent — a stronger kill of the cadence premise than non-monotonic counts.
- An unlogged, 0.25 s-margin run was load-bearing for the headline; the lab's own record rule (5 October: "results that the shipped code could not regenerate") predicted this failure.
- The sweep was abandoned mid-B14 (step 3) and B12/B17 were never run, though predictions named them; B17's N=4–6 pass is cited from law.md, not measured here.
