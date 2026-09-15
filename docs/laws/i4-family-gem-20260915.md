# I4 family-sourced GEM — 15 September 2026

Not `production_law`. `CANONICAL_GRAVITY_ACCEPTANCE` remains `diagnostic-only`.
Does not rewrite frozen [I4 six-card](i4-six-card-crossing-20260915.md) (H0139).
Galaxy admitted method remains **direct small-world GEM sums** (quadrupole 0.478).
This closes the named leftover that represented family mass did not source GEM.

## Declared before results

| Item | Declaration |
|---|---|
| Remainder band | `I4_FAMILY_POS_BAND=0.05` (same as I3/I4; not widened) |
| Approximation | Affine equal-μ family as one COM/moment GEM source plus `FamilyIdentities` sidecar |
| Fallback | Extract-and-collocate every member that must gravitate |
| Mass | Do not drop μ; moment μ equals extracted Σμ |
| Identities | Retain member ids in the sidecar even when GEM sees one body |
| Galaxy | Direct sums until a multipole meets 0.05 with a remainder bound |

Fixture: `laboratory_two_body` plus N=4 members, μ=0.01 each, y=18, rest, H=min(4,2)=2, dt=1/16, `store_pair_inverse: false`. Observer is body 1 at t=1.

## Results

| Measurement | Value |
|---|---|
| Remainder vs extract | **0** ≤ 0.05 KEEP |
| Explicit bound | octupole-like `4 μ ℓ³ / R⁵` / `|a_extract|` = 1.04×10⁻⁶ |
| Mass | 0.04 = 0.04 accounted |
| Identities | 4 ids retained in `FamilyIdentities` |
| Extract ledger | **127395** |
| Moment ledger | **1906** |
| **Admitted method** | **`family-moment-gem-source`** |

### Nested Charge (extract vs moment)

| Role | Extract | Moment |
|---|---|---|
| construction (`init` + `source_evolution`) | 1 + 474 | 1 + 9 |
| certificate (`validation` + `factorization`) | 1 + 559 | 1 + 15 |
| reconstruction | 480 | 12 |
| fallback | 0 | 0 |
| history | 1 | 1 |
| query (`field_evals`) | 2284 | 261 |
| `ledger_total` (includes nested children) | 127395 | 1906 |

Remainder 0 is monopole agreement of an affine rest family at large R, covered by the 10⁻⁶ bound. It is **not** a galaxy multipole KEEP.

## Domain

Admitted: affine equal-μ families as one GEM source with an identity sidecar, on this quiet laboratory pair at H≤2. Extract-and-collocate remains available if a family is not affine or the 0.05 band is missed. Direct small-world GEM sums remain the galaxy method.
