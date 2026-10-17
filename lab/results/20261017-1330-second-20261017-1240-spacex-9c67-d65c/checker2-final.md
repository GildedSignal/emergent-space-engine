Working...
**Grade: gold** — written to `check2.md`. Verdict basis:

**Reproduced.** Runner's regen (exit 0) matches every deterministic number exactly: plane census `(35275, 39, 17643)` with all six per-kind rows, belt census (boundaries 719,845/719,845, kicks 283/725,976, walked 100,093), both digest anchors matching 5ade's recorded values. I applied `work/patch.diff` myself at base `f66d63ac` (+110/−7, round-trips) and diffed it against 9c67's: the behavioural core is byte-identical; additions are counters whose expensive half is `ES_POS_VERIFY`-gated. Timing differs only within shared-box noise, in the same direction (fresh normalized median −9.8% vs dossier −10.5%).

**Predictions genuine.** Two mechanism predictions *failed* (`apply ≤1.2 µs`, `ROOT calls ≤0.05/kick` — landed 2.2–2.6 µs and 2.06/kick), which is the strongest evidence of real pre-registration; the verdict-relevant ones held.

**Attack (3 cases, 2 outside the author's domain), all held:**
1. Census at 150–230 ks: boundaries 100% mismatched with |Δx| to **1,747,192** root units (the pre-registered ">10⁶" clause fires; window-scoped, not law-level); kicks stay exactly 283, same span; walked stays 100,093 (births).
2. Digest identity at 150–230 ks, N=10⁵: bit-identical arms — the digest is blind to 1.13 M divergences, beyond the author's 80 ks open surface.
3. N=2×10⁴ at 330 ks (3.25× window): digests identical, −9.2% wave CPU with a stable control; walked 20,093 ≈ N confirms the birth attribution at a second size.

**Page faithful** — all d65c lines check against evidence, and it resolves the live page's unresolved publish conflict; I corrected nothing. Novel on the record (no prior belt measurement of this hand-off; the −13% → −9…−11% correction with its cause is new). Named dings: the two missed mechanism predictions aren't tallied under Predictions, "untouched resolver" is ~99.9% true, the 99.99%-coverage fraction mixes cumulative and in-window counts, and one seed throughout.
