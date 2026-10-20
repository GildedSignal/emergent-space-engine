# The cell-struct read on the record's branch (the checker's named hinge)

9c08's dossier named its own weak arm: "I measured the premise and the record's readout family in
float, not the record's shipped branch code… a checker should read its cell struct once on the
branch." Its checker made that the gold condition, with the fork stated: "if the field is already
a seen-flux sum, only the colour channel stands." This file is that read, from the record's own
branch (`origin/claude/lab-20261019-0325-spacex-959a`; the record's code lives in the run's
`work/patch.diff`, which `run.sh` applies and restores — the tree is never left edited).

Reproduce every quote below:

    git show origin/claude/lab-20261019-0325-spacex-959a:lab/results/20261019-0325-spacex-959a/work/patch.diff | grep -n "CellSums\|sums_add\|luminosity\|row.shift\|row.color"

## The verdict of the read

**The record stores the seen-flux sum, member by member. 9c08's "what would make it wrong" clause
(1) fires exactly: the brightness half of its kill does not apply to the shipped record, and its
proposed cure — "a running sum Σ(lum·k⁴)… one extra FMA per event" — is already the record's own
field, at zero extra cost.** What the letter L59 ("aggregates are one sample each") describes is
not the record; and as a *rule* the letter is now rung-dead (r13: the one-shift collapse fails
brightness p99 0.77 and colour 0.96 oct at γθ_f = 8000; reads 0 at the record's flown γ ≤ 1.33).

## The fields, verbatim (patch lines prefixed `+`)

The row maker — each member's own k enters its own row (the shipped per-body formula, `view.rs`
L308–320 on main; identical in the record's `sky_make`):

```rust
let shift = ((1. - dot(n_prop, obs.vo)) / obs.rate_obs) / ((1. - dot(n_prop, vel)) / rate);
color:      blackbody(temp * shift),
luminosity: lum * shift.powi(4),   // the seen flux: each member's own k⁴, at insert
shift,
```

The cell aggregate (959a `struct CellSums` and `sums_add` — the running sums, updated on the due
events, churn and tier moves the record already pays for):

```rust
struct CellSums { n: u32, lum: f64, lc: [f64; 3], ls: f64, sh: f64, kinds: [u32; 8] }
fn sums_add(&mut self, cell: i64, row: &Seen) {
    e.n   += 1;
    e.lum += row.luminosity;                      // Σ lum_i·k_i⁴  — the exact seen-flux sum
    e.lc[j] += row.color[j] * row.luminosity;     // Σ blackbody(T_i·k_i)·lum_i·k_i⁴  (j = 0..3)
    e.ls  += row.light_seconds * row.luminosity;
    e.sh  += row.shift * row.luminosity;          // Σ lum_i·k_i⁵  (an instrument readout)
    e.kinds[(row.kind & 7) as usize] += 1;
}
```

The serve (959a, multi-member cells; `sums_sub` is the exact mirror on removal, so due refreshes
are sub-old/add-new with fresh rows):

```rust
luminosity: lum,                                  // served brightness = the sum itself
color:      [cs.lc[0]/lum, …],                    // flux-weighted per-member blackbody mix
shift:      cs.sh / lum,                          // Σk⁵/Σk⁴ — served as a readout field
if members.len() == 1 { serve the member's exact row }   // singletons: exact, outside the aggregate
```

## What each field is, against 9c08's readout family

| record field | is | 9c08's name | 9c08's model of it |
|---|---|---|---|
| `lum` | Σ lumᵢkᵢ⁴ (exact seen flux) | — | **absent from 9c08's model of the record** |
| served brightness | `lum` itself | — | modelled as k̄⁴·n (R1a/R1b/R2 errors 18–141%) |
| `lc/lum` | flux-weighted per-member blackbody | — | modelled as one blackbody(T·k̄) |
| `sh/lum` | Σk⁵/Σk⁴ = R1b | R1b | the only field 9c08's model got right — and nothing rebuilds brightness from it |

The wiki field list that misled the model — "(n, Σlum, lum-weighted colour/light-seconds/shift, a
kind histogram)" — means Σ *seen* lum (k⁴ folded per member at insert), not Σ rest lum. The
e6c9 record (the pre-959a rebuild path, same patch) accumulates the same seen-flux sums per frame,
so the misread applies to neither generation of the record.

Downstream check (current tree): nothing rebuilds brightness from `Seen.shift`. The `shift` uses
in `observe.rs`/`world.rs` are the doll's integer level exponent (a different field of the same
name); the aggregate row carries its luminosity directly.

## What survives of 9c08 on the record

1. The geometric law itself — exact SR, reproduced here per case (2D p99 27.8% at γθ_f = 1,
   saturation 77.2% 2D / 68.8% 3D; the E(γ·θ_f) collapse case-identical across floors).
2. The letter L59 as a rule: dead, now rung-guarded (r13's negative). Any future cost cut that
   collapses the sums to one shift — the readout the letter describes — is KILLed at the gate.
3. The colour-k for a sprite table (where a single k is wanted): the letter's own L58 log-k table,
   B = 128, holds ≤ 0.036 oct at γθ_f = 8000 (r13 candidate). The record's own RGB serve
   (`lc/lum`) needs no k: the flux-weighted mix of per-member blackbodies is the summed light's
   RGB exactly (linear mixing identity — the palette sampling is the per-body path's own
   approximation, shared by both paths, not an aggregate-γ error).
4. The γ clause in the record's license: still worth writing (the record's flights stop at γ 1.3;
   the channel is now guarded at γθ_f ≤ 8000), but as a note on the *letter's* readout, not a
   defect of the record.
