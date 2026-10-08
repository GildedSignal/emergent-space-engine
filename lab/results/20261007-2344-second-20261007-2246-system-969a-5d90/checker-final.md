Working...
**Grade: gold** — written to `check.md`.

**What I reproduced (clean rebuild, byte-identical diffs against the author's logs):**
- **steady** (25 s): truth 922 events, key 0/0, cone 0/0, key-only 191 570 pairs → 0 tier-2 work; the 10⁵-orbit gate numbers (1.400 key / 1.296 cone vs ≤ 2.0; 1.103 checks/hit vs ≤ 1.5) all match.
- **spread** (5 s): 0/0 both tiers, tier-2 bit-identical across candidate sources.
- **extremee400** (93 s): the boundary finding exactly — key 26 155 pairs, **206/289 missed**; cone on all 79 800 pairs, **0/289**.
- **Port**: `keydump` u-intervals match my independent Python to 9 decimals; pair counts exact on three scenes (590 153 / 26 155 / 163 461). Shipped code byte-identical (`diff`).

**My adversarial cases:** the untested gap e∈[0.9,0.95] is sound (300 k samples, three ρ, min margin +2.3×10⁻³); inversion confirmed analytically at e≈0.9685–0.969 (ρ-dependent; the dossier's 0.9692 is the leading-order √q_p form); and I found selectivity is already dead slightly *below* the boundary (window ≈ everything at e=0.96) — the honest fallback regime is wider than stated.

**Record blemishes, named in the check:** `check_port.py` crashes as shipped (`keydump` prints no rows), so the "0.0 max diff, 50 bodies" line isn't regenerable by its stated command — the claim is true by other shipped means, and every load-bearing number regenerates, so I judged it a broken validator rather than an unregenerable result; predictions say seed 20261020 vs the code's 20261013; "frozen gates" is threshold reuse on a sibling seed/truth, not the frozen rung instance.

Gold rationale: it runs exactly the experiment the first checker named as the silver's path to gold, corrects that checker's e≈0.9995 boundary to e≈0.969 with a measured mechanism and a one-line fix, and leaves adoption one integrator step (the wiring, outside lab authority). Still open: joint N-scaling (case c), tier-2 under precession, chirality.
