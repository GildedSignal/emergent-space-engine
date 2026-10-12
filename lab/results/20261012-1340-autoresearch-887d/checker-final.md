Working...
Check complete. Tree restored to pristine; only `lab/results/20261012-1340-autoresearch-887d/check.md` written.

**Verdict: silver** (`Grade: silver`).

What I verified, all from a clean tree with `work/patch.diff` applied:

- **Exactness reproduced.** Digests byte-identical to pristine (rebuilt from main with the same bench) on all four held-out configs — baseline 82d40ca8…f324 matches the author's — with identical event counts. Interleaved 3× A/B: **−19.7% ns/kick** on 64/2/7 (39.6–40.7 → 31.5–32.2 µs), **−20.8%** on 128/2/9; N-independent as predicted.
- **Adversarial cases held.** Four scenes of my own, including the author's named gap: eccentric crash (e up to 0.9, 4 bodies lost into the star), heavy-planet co-orbital (1 refused, 1 lost), near-surface grazers, 256 ships/1.02 M kicks — digests and counts byte-identical everywhere.
- **Pre-existing failure confirmed.** The single failing xtask plane test fails identically (12 pass/1 fail) on pristine main and on the patched tree.
- **The blocking defect.** The headline −26% (38.8 → 28.8 µs/kick) rests on round 4 (`boundary_clock` from tube bounds), which is in **neither patch file** — zero boundary hunks; pristine `boundary_clock` still does the full readout. The shipped code regenerates rounds 1–3 only (~−20%). Same failure mode the taste log killed runs for on 5 October: numbers the shipped code cannot regenerate. Secondary record error: the suite count is 104 passed, not 66.

Real, exact, adoptable in one step — but a 1.25× constant-factor with an unregenerable headline is silver. The gold path is named in check.md: ship round 4 (or restate at −20%), then delete the per-kick full refit via the incremental one-quantum rebind the dossier itself points at.
