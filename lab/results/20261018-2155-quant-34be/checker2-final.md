Working...
**Grade: gold** — written to `lab/results/20261018-2155-quant-34be/check2.md`.

**Reproduction.** Applied `work/patch.diff` in a clean tree, rebuilt, ran the decisive example: census bit-identical on all four arms (mism_naive 166/180/215/206 per 100,000, mism_sound 0, 0/400,000 tuples ≥ 2⁶³, identical step histograms); timing within clock noise on the shared box (u128 p50 190.8–192.9 ns; win 1.59/1.58/1.42/1.42×). Shipped dioph tests pass 2/2 (regen.log's `tail -3` only showed the later empty test binaries). Tuple construction verified verbatim against `tier::arm_pair` (tier.rs:550–571); predictions.md (22:00) predates the decisive output (22:05), and its falsifications (naive-port mismatches, depth 2–4, win 1.4–1.6×) are the no-tuning kind.

**Adversarial (mine, outside the author's domain).**
- a = 30 AU (next decade; pi ≈ 2⁴²): naive port corrupts **41.2%** of calls (46.7% second arm) — the page's folded "41%" line confirmed; sound port still exact; win 1.58×/1.36×.
- 10× wider a-window (1e-3): depth p50 6/max 14, win 1.75× — still under the kill line.
- keys=8 (structured periods, the author's named risk): 0 naive mismatches, win 1.68×.
- Semantics: all 166 mismatches on the shipped class return k whose residue lands **outside** the window while u128's lands inside — real wrong dues, zero Some/None flips. The kill does not hinge on timing at all: even a free `first_hit` leaves the row at ~10² cores against the 10³ gap.

**Verdict rationale.** Premise-is-wrong gold in the components-4643 mold: od 1's "all section values < 2⁶³" parenthetical is a soundness trap on the belt's own magnitudes (m·y ≈ m² ≈ 2⁷⁴ wraps u64), and the sound port's 1.42–1.60× is below its own pre-registered kill rule. Novel (e87d named it unpriced; nothing in HISTORY prices it). Nits recorded: "p99 within 2%" is 3% on one arm of their own output; m² ≈ 2⁷⁴·⁰ not 2⁷⁴·⁴; "≪ 2×" is optimistic wording at 1.75× on the wider window.

**Page.** Author's fold-in faithful; I appended my blind confirmation to the Runs line in `wiki/encounters.md`. Tree cleaned (scratch example and applied patch files removed; nothing committed).
