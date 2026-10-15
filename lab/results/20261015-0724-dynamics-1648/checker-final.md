Working...
Check complete. Verdict written to `lab/results/20261015-0724-dynamics-1648/check.md`: **Grade: gold**.

**Reproduction.** Applied `work/patch.diff` to the clean tree myself and reran c2+h1: all ten scene-arm records bit-identical to the author's regen output, both shipped digests equal. The runner's full regen (exit 0) matches every dossier number I traced — the d1/d2/h1 table, both controls, the tau residues, Fano, ledgers.

**Instrument audit.** The twins mirror the shipped code at source level: `hit_f` ≡ `law::hit_narrow` branch for branch, the reflection ≡ `relativity.rs`'s N = (d·Pₛ, E·d), step order and consumed-retain ≡ `chronon.rs:67-140`. The no-op proof verified independently — and it's stronger than claimed: the shipped integer law itself returns "no exchange" at the τ* geometry (`relativity.rs:135`, `mdot(pa,n)==0`), so the refutation binds the integer law. `work/controls.jsonl` (timestamped before `predictions.md`) corroborates the discovery narrative: first-build fix arm applied 3,665 impulse over 46,600 skip-class contacts.

**Adversarial cases (3, one outside the author's range):**
1. **Fence speed vth=2000** (untested interval 700–4000): skip 24%, dropped transport 23.5% — the "law change" boundary sits exactly where the dossier puts it; rate law and classifier (99.4%) extend.
2. **3× density** (the author's named weakness): contamination stayed ≤4, canary intact, innocence extends beyond the claimed domain.
3. **Dilute fast gas**: tau's applied transport fell 0.30%→0.05% as contaminated contacts fell 1420→26 — the no-op residue is the multi-pair path, confirmed.

**Deductions.** One imprecision noted: d1's pre-registered "t_half within 10%" measured 18.8% and is summarized as held — defensible as noise (rule-identical arms spread −12.5%…+44%, raw values printed) but it belonged with the disclosed misses. The skip-fraction bands missed 3–10× high, honestly reported with cause.

**Page.** Corrected two overstatements in `wiki/contact-speed.md`: per-ρ agreement ±0.06→±0.09, contacts "within 4%"→"within 5% (d1 4.4%)". Tree restored to its pre-check state.
