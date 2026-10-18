Working...
**Grade: gold** — `check2.md` written. Summary of the blind check:

**Reproduction:** applied `work/patch.diff` to the clean tree, ran the full regen list — all 19 JSON lines match on every deterministic field (38 s). The instrument is the shipped law verbatim (`reach = e/p + e_max/p + eps`; churn's kick move is `main.rs kick`'s own).

**Adversarials (all confirm):**
- **n=3×10⁶** (out of range): 0.519·N, scanned still 100% — law holds; constant crawls up exactly via the disclosed √ln N e_max crawl, so the 10⁹ rescan cost is *worse* than quoted.
- **σ=0.02** (regime boundary): 0.162·N vs 0.164·N σ-linear prediction — saturated and unsaturated regimes connect quantitatively.
- **Band [2,12]** (10× wider, 2 seeds): still 0.15·N — saturation is not a narrow-band artifact.
- **The author's named-but-unrun probe**: 963,298 pair-decision slack hunt at n=10⁵ — 0 violations, skippable 0.9219.
- fe6b at a second X (0.0511 vs 0.0519) and σ=0.2 (0.862·N, cap-bound): X identification real, stirred belts worsen the verdict.

**Findings against the author:** the "anchor density 4×10⁴/AU²" label is the control band's own density (true anchor: 6.37×10⁴/AU² — direction favors the kill); the 10⁹ constant should read 0.48–0.55·N; wide-band control missing. P2 failed honestly and is the finding (saturation kills the wiki's "O(1) at fixed density" closure hope — its open direction 1, verbatim, now answered). Page corrected in place (slack decision count; domain bound). Tree restored clean.
