Working...
**Grade: silver** — written to `lab/results/20261016-0117-taleb-51b7/check2.md`, with one in-place correction to the author's wiki page.

**What I verified:**

- **Reproduction.** The runner's regen matches every dossier number within load noise (beltburn 10⁵: fenced at 148 scans / 1,915 MB / digest `c85be13a…` identical; quiet and wave arms held 0, enc 0; budget-free digests identical ×2). Diffs noted: p50 33.5 vs 29.2 ms, 10³ held 83 vs 103 — timing variance, disclosed class. I independently confirmed the pristine `ladder_digest` values (`4b822570…`/`6895ce06…`/`df0e87cd…`) equal the patched tree's — the scenario edit leaves the shipped plane bit-for-bit — and the code mechanisms: `same_inputs` demands tick equality (every player item mints), `SCAN_BACKLOG = 2048` is a count cap forcing in-frame answers, capture is uninterruptible by the budget.
- **Three adversarial arms, one beyond the author's domain:** 3×10⁵ burn fences at 34 scans = **118.6 B/body** (the 113 B/body law extends; p50 95 ms = 317 ns/body); a 31,000-game-s quiet 10⁵ flight flips held 0→1 at ~28.5k game-s (the claimed ~2.8×10⁴ doll interval, confirmed at the headline N); 10³ burn over 60 s drains its backlog to zero — the cap never engages, the small-N ruin is transient.
- **Novelty.** The ruin, mint site, count-cap refutation, fence, and digest instability were already on the page (625b/c481/d7bc/4487). New and real: the separation (only the player's own binding changes mint; the wave and belt density mint nothing) and the playability fact that the encounter instrument is cadence-off at belt radii. No 10× move, no deletion, nothing adoptable in one step — hence silver, one experiment from gold: mint per candidate-set change (or bound the candidate set by the radial certificate) on the 10⁵ burn and show ≥10³× fewer mints with identical encounters.
- **Page correction.** "The cap can never engage… the machine dies first" is box-relative: 2.3 GB at 10⁴ kills this 2 GB box but not the 8 GB M1 (ordering holds only for N ≳ 3.5×10⁴ at 8 GB). Corrected in place with my 3×10⁵ extension recorded beside it.

Tree restored (`git apply -R`, clean); nothing committed or pushed.
