# Predictions (written before the decisive arms)

Question: the checker broke 9292's window at (L15 × ≥ 4× flight length) and (L15 × 10× zoom) and
priced a naive staleness-repair tier (~0.4 %·K far rows/frame, root-side). 9292's design says the
record composes the shared (β, **displacement**) warp — the displacement half was never measured.
If the broken-window root churn is the observer's own displacement parallax (a shared,
per-frame-composable vector), the repair tier collapses and the deletion license extends through
the broken window; if the churn is emitter-side (retarded drift), the checker's K-scaling tier
stands and the claim's letter dies outside the interior.

Probe: `skyserve` (this folder's patch) flies the record as accounting beside the shipped
`gather_cached`: per far row it stores the root offset at last repair, serves
`stored − (o_now − o_at_repair)` displayed through the shipped `aberration`, and repairs only
when the serve error crosses θ/2. Eight policies at once (naive/warp × root/disp trigger ×
θ_f/θ_f/10), plus a never-repair drift observer. The smoke test (L8 interior) already shows the
warp one-step residual machine-zero (4.4e-16 rad): between tube-quantum jumps the emitters'
retarded positions are frozen and the whole root churn is the observer's displacement.

Arms (held-out until now): A = 1e3 L15 1500 frames (the checker's broken window, 4× flight
length); C = 1e3 L15 360 frames at θ_f = 8e-4 (the 10×-zoom window); A2 = 1e4 L15 as far as a
240-s wall allows (K-law + the observer crossing the belt); controls = coast 360 and L8 1e4 360.

- **P1 (anchor reproduction):** arm A one-step past θ_f/2: root 0.2-0.5 %/frame, displayed
  2-4 %/frame (checker: 0.357 / 2.923); arm C at the fine floor: root 0.4-1 %/frame, displayed
  30-60 % (checker: 0.676 / 46.5). If my anchors miss these bands, the probe differs from the
  census and nothing downstream counts.
- **P2 (the decisive):** warp-policy repairs in arm A's last quarter ≤ 0.05 % of far rows per
  frame at the stock floor and ≤ 0.5 % at the 10× floor, against naive-root ≥ 0.3 % at stock.
  **KILL (refutation):** warp-root repairs > 0.1 %/frame at the stock floor in the last quarter —
  the displacement warp does not collapse the tier and the record needs a K-scaling repair tier
  inside the broken window.
- **P3 (mechanism):** the warp one-step residual stays ≤ 1e-5 rad p99 through arm A
  (machine-zero between tube-quantum jumps; jumps ≤ 3e-4 rad p99, ≈ v_em × quantum / d); the
  never-repair warp error at the end is ≤ 2e-3 rad p99 (the emitters' coherent retarded drift).
- **P4 (near tier):** near set ≤ 600 rows through arm A at 1e3; in arm A2 (1e4) it rises above
  350 while the observer is inside the belt annulus, ∝ local density (the honest K-scaling term
  on the near side).
- **P5 (cells and re-bin):** displayed cells(θ_f) changed per frame ≤ 786 everywhere (the re-map
  is O(occupied cells), never O(K)); a full re-bin at θ_f/10 costs ≤ 150 ns/row (≤ 1.5 ms at
  1e4) — one cold pass per zoom event.
- **P6 (the dial's end):** β ≥ 0.4 by frame 1500 at L15 and the ship stays alive (the checker's
  churn was still growing at f1440); if the ship wrecks, the churn freezes and I report the arm
  as dead-sky instead.

Budget sentence to verify at the worst point (arm A2 last quarter): near + warp repairs + cells
changed ≪ the K-row walk (≥ 10× below), and priced at the M1's ~5 µs/row the record's far tier
stays ≤ 5 ms/frame.
