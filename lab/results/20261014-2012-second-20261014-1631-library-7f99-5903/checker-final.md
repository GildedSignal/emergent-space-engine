Working...
Check complete. **Grade: silver** — written to `check.md`, with the author's wiki page corrected in place.

**What reproduced (clean tree at c027445f):** every dossier number. The four flight arms' digests are bit-identical between shipped and deletion builds (10³/10⁵ coast, 10⁴ burn, both `ES_SCAN_H` controls), walked/call 1017.4→66.0 at 10³ (15.4×), 194.4→66.0 at 10⁵, kept 319→49; the drop-contract test fails exactly as reported ("window of the player: 38 of 38 bodies", n_ladder.rs:202) while the belt exactness test passes; the chatter arm reproduces to the digit (193→0 handoffs, 0 refusals, 3.9×/8.8× events). Predictions provably preceded the runs.

**Why not gold:**
- The runner's regen failure was real and diagnosable: `work/patch.diff` contains its own 387-line diff **twice** (git apply fails; `head -387` applies cleanly), and the 887-line chatter probe (`tests/handoff.rs`) was never saved into the record — `regen.sh` step 4 cannot run, and the fix phase left `raw/chatter-baseline.txt` at 0 bytes. I verified the chatter half only via the author's surviving compiled binary (built 20:32:25). The record does not regenerate as shipped.
- The build itself fails the shipped drop contract; the working scale-relative widening is named, not built.

**New findings from my adversarial cases** (folded into the page): at 10⁵ burn — the decade the author never flew — the deletion walks **1,975/call against base 74.9** (26× penalty, growing with N; digest still identical), so "constant in N" is coast-only; and the refusal gate fails the branch's own moon test (`a_moon_born_in_the_planets_doll_never_leaves`, passes ungated) — direct proof load-bearing handoffs die with the chatter.

**The one experiment to gold:** build the scale-relative widening, pass the drop contract, bring the 10⁵-burn walk back under base, keep all digests, and land a regen that runs cold end to end.
