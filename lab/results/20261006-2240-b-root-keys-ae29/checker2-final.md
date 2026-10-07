Working...
Check complete. `check2.md` written to the run folder, grade **silver**.

**What I did:**

1. **Reproduced everything in a clean tree** (`70f27a9` + `git apply work/patch.diff`): P6 (2 passed, 0.83 s, offsets −8,314..+6,002, worst miss 0.500 tick — matches the author's log exactly), the plane example (Moon −25, Skimmer +1, bit-identical to `rootkey-plane.txt`), B13 both directions myself (baseline on clean main and patched: identical detail lines, even the 2.53 s), full suite 58 green / 272 s.

2. **Falsifiability control re-run**: forced `root_offset` to the identity — both P6 tests fail with the author's exact numbers (member 1: −110.524; the pair tied at 16,384).

3. **Adversarial cases of my own**:
   - **β 0.9 / 0.99**: the shear is correct wherever the centre's readout works (worst 0.498 ≤ 0.5 tick, offsets −44,837..+72,939), **but 52/200 members' keys silently revert to the unsheared doll tick** — `root_offset`'s `else { break }` swallows the centre readout's "state outside the integer word" refusal at tick 2²⁰ with no fault recorded. That is the one real defect; unreachable by any current gate or the plane, reachable through this patch's own `retune` relaxation.
   - **Depth-2 doll chain** (planet 0.5 c → bound moon → ships): both edges' shears compose to my independent oracle within 0.5 tick; the author's admitted blind spot is sound as built — the hierarchy forces child centres slow (a 0.3 c moon refuses `NoBoundOrbit` by construction).

4. **Novelty**: closes law.md's registered Open ("a boost also maps event times") and HANDOFF's simultaneity risk; no prior implementation in HISTORY or git log. Predictions genuinely preceded the decisive runs (mtimes + machine timestamps); all five held.

**Silver, not gold**: physics right, everything at 0.5 c reproduces bit for bit, but the core claim ("a relativistic doll orders its events correctly") is silently falsified at β ≥ 0.9 — one named experiment from gold: make the fallback loud (recorded refusal) and re-run P6 at 0.9/0.99. Tree restored to clean `main`; nothing else in the run folder touched.
