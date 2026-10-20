# Predictions (written before the decisive runs)

Arm v5 = `stride_gate` + per-region publish floors + merge-capping (`ESE_FLOOR=v5`, default
with gate=1). Baselines: shipped (gate=0) and v4 (f1ca's global floor0, `ESE_FLOOR=v4`).
Harness: `crates/allocator/examples/exposure.rs` (f1ca's, unchanged), one process per draw,
fire = exit non-zero + the finality assert (`would revise its published tick`).

Protocol (f1ca's): battle = galaxy 8704/24 fleets, rate 2400, min_region 32, margin 0.5,
4.5 s, seeds 11,13,15,17,19,21,23,25; quiet = the 8-island negative control, same seeds;
crush = the same battle draws run 12-concurrent (load-coupled, f1ca's class).

- **P1 (safety).** v5 fires 0/8 on the battle protocol in every window flown, where shipped
  fires (f1ca measured 3/8 in one window, wall-clock-owned). Any v5 fire with the signature
  `fin_hi > s0` kills v5 as a configuration (a missed channel or the descendants-closure
  assumption wrong), not the method.
- **P2 (the decoupling, the claim).** Under 12-way crush, v5's median present ≥ 3× v4's
  median present in the same crush window (f1ca: v4 43 vs shipped 529 — the global floor
  min-coupled by a never-accepting region; v5 must decouple unrelated lineages). If v5 ≈ v4
  under crush, the per-region floor does not pay: lead.
- **P3 (quiet cost).** Quiet windows, v5 present ≥ 60% of shipped, median (v4's band was
  51-100%, median 74-93%). v5's floor walk is O(truths + lineage edges) per finalize: if the
  overhead pushes v5 below 60% on quiet draws, the implementation cost dominates: lead.
- **P4 (the equality law).** Every v5 rollback line has `m ≤ 0` and `out=[]` (the restore
  instrument stays shut; restores land at or below published ticks, e517's law).
- **P5 (control).** The quiet class stays clean in all arms: 0 fires, 0 rollbacks.

Held-out (checker's own): fresh seeds, other scales (gn 4352/17408), the gas class, margin
2.0, and any adversarial scene of its own choosing.
