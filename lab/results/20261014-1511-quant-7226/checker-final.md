Working...
Check complete. `lab/results/20261014-1511-quant-7226/check.md` written; the tree is back to clean HEAD (my probe edits reverted by the pristine control); the author's wiki page corrected in place where it overstated.

## Verdict: silver

**Reproduced bit-for-bit** from a clean tree + `work/patch.diff`:
- Census: 802 searches / 23,552 probes (mean 29.4, worst 32), exit searches 0/1,188 endpoint probes, digests `36637e67…`/`f282c907…`, refused 0.
- **Pristine HEAD build gives the same digests** — "off = shipped verbatim" verified, not asserted.
- Secant kill: 35,621 probes (mean 44.4, worst 57), leaver 306 µs. Equality test passes.

**Adversarial cases (3, one outside the author's domain):**
1. **Held-out seed 11**: census and kill both extend (off mean 29.3/worst 31; on 40.2/57; digests identical off=on).
2. **Built the "named survivor" myself** — Anderson–Björck on the same predicate: mean 21.3 probes (−28%), leaver median −26%, digest-identical, but **worst 38 > 30 fails the frozen tail rule**; bail-at-8 is worse (mean 27.5). The lever is measurably alive; the author's "kill of my update rules, not the lever" pre-registration is confirmed by measurement.
3. **Rebuilt the unregenerable kill row** (the patch ships only the secant): Illinois-on-signed reproduces exactly (mean 28.01 vs claimed 28.0, worst 30). Illinois-abs and quadratic rows remain unregenerable — disclosed in check.md.

**Page corrections**: the "expected ~6–8 probes" for AB replaced with my measured numbers; a regenerability note added to the open direction.

**Why not gold**: P1/P2 failed by the author's own hand (honest), the lever is one measured experiment short, and 2 of 4 kill rows can't be regenerated from the shipped patch. The gold experiment is named: AB-family update with a tail guard passing worst ≤ 30, ≥25% leaver cut, digest-identical, multi-seed and both paces, composed with the warm start.
