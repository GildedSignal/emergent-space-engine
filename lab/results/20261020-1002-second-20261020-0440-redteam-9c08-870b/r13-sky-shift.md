# Rung r13: the sky-cell aggregate under the observer's own γ

Frozen by the second author on run 20261020-0440-redteam-9c08 (20 October 2026), from that run's
freeze-ready arm plus its checker's two named additions: the game's 2D sky, and the cell-struct
read on the record's branch (959a). The struct read settled the hinge the checker named:
`CellSums.lum += row.luminosity` with `row.luminosity = lum·shift⁴` — the record stores the exact
seen-flux sum, member by member, so the brightness half of 9c08's kill does not touch the shipped
record, and 9c08's proposed cure (a running sum Σ lum·k⁴) is already the record's own field. What
remains live is the letter (`docs/representation.md` L59, "Aggregates are one sample each"): read
as a rule it collapses the cell to one shift, and 9c08 measured that readout dying at the γ the
engine's own gates fly (the clock gate C1 at γ = 10⁶; the playability red at γ ≈ 120). This rung
freezes that channel: the record's representation must pass at every γ the gates fly, the
one-sample collapse must fail there, and both must read zero at the record's flown γ — so the
channel can never silently regress, in either direction (a future "optimization" that collapses
the sums, or an instrument that fabricates error).

**Question.**
1. Does the shipped record's cell aggregate hold the forward sky's k⁴ brightness to ≤ 5% (p99,
   flux-weighted) and its colour to ≤ ⅛ octave at γθ_f ∈ {1, 4, 8000}, on the game's 2D sky and
   on the 3D comparison sky, at both cell floors?
2. Does the letter's one-sample collapse (one lum-weighted shift per cell) fail those criteria on
   the same cases while reading zero at the controls (γ 1.0001 and 1.33, the record's own flown
   domain, where 9c08 measured 0.0025% p99)?

**Configurations.**
- `exact-sum` (candidate): the shipped record's field list (959a `CellSums`: n, Σ seen luminosity
  = Σ lumᵢkᵢ⁴, Σ blackbody(Tᵢkᵢ)·lumᵢkᵢ⁴ colour, Σ lumᵢkᵢ⁵ shift readout, kind histogram —
  brightness served from the sum, exact by construction) plus the letter's own L58 mechanism for
  the sprite colour: a per-cell equal-ln-k histogram, B = 128 bins over the cell's [k_min, k_max]
  (B frozen from the pilot: worst-case colour 0.036 oct at γθ_f = 8000, half the ⅛-octave
  threshold with the bin-bound 0.070).
- `one-shift` (negative): the letter L59 read literally — one shift per cell,
  k̄ = Σ lumᵢkᵢ/Σ lumᵢ, brightness k̄⁴·Σ lumᵢ, colour blackbody(T·k̄). It must fail.
- `flat-gamma` (positive): the exact-sum readout at the control gammas only. It must read zero;
  if it does not, the instrument is broken and the verdict is VOID.

**Cases.** A perfectly cold sky (every emitter at rest in the sky frame; zero velocity dispersion
— exactly where the dispersion channels read zero, so this isolates the geometric channel), equal
rest luminosity per member, NS = 2·10⁶ members, exact special relativity: k = γ(1+β cos φ_s),
aberration cos φ′ = (cos φ_s+β)/(1+β cos φ_s) — this is the record's own row formula
(`shift = (1−n·v_o)/rate_o ÷ (1−n·v)/rate`, view.rs L308) evaluated on a cold sky. The game's sky
is a circle (the record's 786 cells = 2π/θ_f, served as [cos θ, sin θ]): members uniform in the
sky angle φ_s. The 3D isotropic sky (uniform in cos θ_s, 9c08's idealisation) is the comparison
arm. Case set: γθ_f ∈ {1, 4, 8000} × {2D, 3D} × {stock floor 8e-3, fine floor 1e-3} (γ 125–8·10⁶),
plus controls γ ∈ {1.0001, 1.33} × {2D, 3D} × stock.

**Domains.** Multi-member cells only (n ≥ 2): singleton cells serve the member's exact row in the
record (`members.len() == 1` branch), so they are outside the aggregate's domain. The truth for a
cell is that cell's member set: brightness Σ lumᵢkᵢ⁴, colour ⟨ln k⟩ weighted by seen flux. The p99
weights each cell by its share of the seen flux (the player-visible sky); colour is the worst
multi-member cell.

**Metrics,** one set per configuration:
- `bright_p99`: max over the 12 non-control cases of the flux-weighted p99 over multi-member
  cells of the relative k⁴-brightness error.
- `colour_oct`: max over the 12 non-control cases and their multi-member cells of the served
  colour-k's error against the exact Σk⁴-weighted ⟨ln k⟩, in octaves.
- `ctrl_bright_max`: max over the 4 control cases of the flux-weighted p99 brightness error
  (the "reads zero" instrument control).
- `extra_due_ops`: counted arithmetic operations per due event beyond the shipped record's
  aggregate update (959a `sums_add`: 8 ops — n, Σlum·k⁴, 3 colour FMAs, light-seconds FMA, shift
  FMA, kind). The candidate's Σ lum·k⁴ counts 0 extra (it is the shipped field); the L58 table
  counts 4 (ln k, sub, mul, bin add); the one-shift collapse counts −5 (it deletes the sums).
  Threshold 6: the letter's "+1 FMA" cure is already shipped, and the table is the letter's own
  O(1) additive update — anything superlinear or read-adding fails.

**Output.** `metrics.json`, `metrics-check.json` (fresh seed), the per-case evidence table, the
closed-form quadrature cross-check of the forward ring (both skies; it must reproduce 9c08's and
its checker's constants: 18.3457% 3D and 16.76% 2D at γθ_f = 1), and the verdict.

```configs
exact-sum candidate
one-shift negative
flat-gamma positive
```

```criteria
bright behaviour bright_p99 <= 0.05
colour type colour_oct <= 0.125
ctrl type ctrl_bright_max <= 0.001
cost cost extra_due_ops <= 6
```
