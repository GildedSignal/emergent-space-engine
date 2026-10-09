# Predictions (held out; written before the tuning loop runs)

Held-out set (not tuned on; different p, e, phases from the 8-case tuning bank):
- HO1 p=3_456_789_001, e=(1<<48)/50, 4 phases
- HO2 p=2_000_000_000, e=(1<<48)/4
- HO3 p=987_654_321, e=(1<<48)/20
- HO4 p=1<<44, e=0 (circular, far)
- HO5 p=64, e=(1<<48)/3 (strong field)
- HO6 p=1_500_000_000, e=(1<<48)*0.9 (near-separatrix-ish, 0.9)

Measured via `autoresearch` harness extended with this bank at the end (`heldout` stage).

## Predictions

1. **Digest invariance:** every kept change leaves the harness digest bit-identical
   (`7bd1878c3161c1776abb75107ecf3423` at 500 iters) on the tuning bank AND produces
   identical per-case outputs on the held-out bank (compared against a pre-change run
   saved to `heldout_before.txt`).
2. **fast_quad division replacement (H1)** cuts `compile` and `state` on weak-field
   (q≈0, ship-like) cases by 15–35% (four `__udivti3`-class multiword divisions per node
   become two native u64 divisions each). Held-out weak cases HO1, HO3, HO4 should show
   the same relative gain (within noise) since the mechanism is per-node arithmetic,
   not orbit shape.
3. **Strong-field cases (HO5) gain less** from H1 (word_root may be false there, taking
   the multiword isqrt path), unless H2 (isqrt via div_word Newton) also lands.
4. Near-separatrix (HO6, and tuning e≈1) is panel-count-bound, so relative gain is
   similar to other weak cases but absolute time stays ~10× a ship orbit: no structural
   change in panel count is attempted (that would change bits = law change).
5. If three consecutive rounds gain <10% each, I stop and report the best configuration.

## Kill criteria for the whole run

- Any digest change on any kept change → revert that change immediately, log it.
- Final total gain (sum of stages) < 10% → report as lead, not silver.
