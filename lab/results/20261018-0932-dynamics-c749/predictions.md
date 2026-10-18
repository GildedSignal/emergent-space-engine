# Predictions (written before the decisive draws)

Setup: e517's print-only PRE/HAZ/RB/FIRE instrument (alloc.rs, verbatim from
`claude/lab-20261017-1829-...-e517`'s patch) + bf83's `exposure.rs` battle harness
(`claude/lab-20261018-0035-inversion-bf83`), both applied to this tree; my only
extensions are two battle args (fleets, galaxy size, seconds) and a bbox print on the
FIRE line (disclosed in the dossier). Decisive arms: `battle` = `worlds::galaxy`
power-law fleets, rate 2400, min_region 32, margin 0.5 (bf83's fire protocol), galaxies
4352/12 and 8704/24 (checker2's higher-incidence scene), one process per draw.

The law under test was established by e517 **only on the selfchurn harness** (a loose gas
cluster); the fleet scene has real merges/splits (pilot: 13→1 regions, 8 merges, 3 splits)
and bulk fleet convergence — a different lineage topology. Transfer is the held-out case.

- **P1 (fire is state-decided at certify):** every FIRE is preceded, on the immediately
  preceding PRE line of the same stride, by D > 0, and D equals fin_hi − s0 of the fatal
  pair (the FIRE line's own numbers).
- **P2 (armed precedes fire):** every firing draw shows HAZ A > 0 in publishes before the
  fire (e517: armed lead of a whole scene start on churn; here I only predict A > 0 at
  some publish strictly before the fatal certify, no lead-time claim).
- **P3 (realized non-fatal ⇒ margin 0):** every RB line on a surviving draw has m = 0
  exactly (all realized clashes restore exactly at the boundary).
- **P4 (the sibling-closure hole stays shut):** `out=` is empty (mo = 0) on every RB,
  fires included — i.e. rollback's union-find `affected` ⊆ the clashing lineages'
  descendants closure even under the battle's merge/split topology.
- **P5 (which lineage crosses):** the last pre-fire HAZ armed pair (b, t) identifies the
  fatal lineages: b ∈ affected of the fatal RB and t ∈ affected (or t is the lid).
- **P6 (negative control, margin 2.0):** battle draws at the shipped default margin never
  arm (A ≤ 0 or '-' at every publish) and never fire.
- **P7 (incidence):** galaxy 8704/24 fleets at margin 0.5 fires more often than 4352/12
  (checker2: 2/4 vs pooled 4/62) — incidence rises with battle scale.

Kill criteria for the transferred law: any FIRE with D ≤ 0 or no matching pre-fire armed
pair kills P1/P2 transfer; any non-fatal RB with m < 0 (restore strictly inside the
boundary) is a new fact, not a kill (e517 only claimed m = 0 on realized clashes);
`out=` non-empty on any fire kills the containment half (P4) and with it the soundness
argument as written for the fix.
