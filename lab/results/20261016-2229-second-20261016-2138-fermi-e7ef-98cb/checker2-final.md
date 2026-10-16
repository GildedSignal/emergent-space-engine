Working...
Check complete. Verdict written to `check2.md`: **Grade: gold**.

**What I did:**

1. **Reproduced from a clean tree** — applied `work/patch.diff`, rebuilt, ran the core arms myself: `belt_first` off/on bit-identical to the author (14,072 → 112,574 game-s = 8.000×); shipped 3×10⁵ freeze spell 20.9 s / deficit 36,268 vs composed 0.0 s / 656, fires 1,179. Third independent regen in agreement.

2. **Three adversarial cases**, one outside the author's range:
   - **6×10⁵ composed** (their ceiling was 3×10⁵; 10⁶ container-blocked): cure holds — spell 0.0 s, 1,544 MB, fires 1,179 again.
   - **Burn arm** (the author's admitted gap): freeze stays cured (spell 0.6 s) but the burn's binding remains — 133 over-budget frames, p99 32.9 ms, memory climbing to 1,759 MB in 25 s.
   - **Past the staggered first interval's end** (366,867 game-s, no arm had gone beyond ~17% of it): no second crest, spell 2.0 s; sustained 36× pace delivers 85% — a window-length effect the author's 40-s windows didn't show.

3. **Verified** the ledger arithmetic exactly (22.45 → 8.76 x86, 5.13 M1, required kick 23.1 µs — robust even at the composed arms' cheapest Ĉ), prediction-file ordering (22:41 before all decisive artifacts), and novelty (9e75 measured the disease, f82a the stagger's tails at 10⁴–10⁵, e7ef was arithmetic — the flight-proven cure and b583's belt-emptiness are new).

4. **Corrected the proposed page** once: "99.5%" delivered → measured 99% (98.1–99.4% across runs). Tree restored to pristine.

**Gold rationale:** reproduced 3× with a bit-identical deterministic instrument; pre-registered two-branch predictions all held; moves the board's top bottleneck ~200× (34% → 99% of due game time, adoptable as two constants-only env flags); and refutes the named composition's 10⁹ closure premise with a clean measurement — the crash-search lever never runs on the belt population, so a 10⁹-motivated crash-search programme would have been misaimed. Misses named in check2.md: the sustained-36× erosion, the uncommitted 10⁴ fire count, and the burn arm's memory climb now measured as the next wall.
