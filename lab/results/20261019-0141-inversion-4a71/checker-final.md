Working...
Check complete — `Grade: gold`, written to `lab/results/20261019-0141-inversion-4a71/check.md`, tree restored clean.

**What I did:**
- **Reproduced** from a clean tree (patch applied from the repo root — note: `git apply` from a subdirectory silently no-ops, exit 0; and the shipped example doesn't link on Linux without the patch's disclosed `/proc` port). Regen's deterministic core matches: ctrl bpb 1,417 / cat 30,076 / 1.07 retained/body (d839's digits); pins 3.00 and 5.04/body, RSS 281/383 MB, gap = D exactly; negative control inert. Timing-elastic digits differ and are recorded (ctrl max gap 1,655.1 vs 2,302.5 — both flat, both inside P1's band).
- **Three adversarial arms, all outside the author's grid:** D=2.4e10 (staircase continues, 6.7/body, 460 MB, no saturation); K=10⁵ pinned (same ~1.7 KB/binding law, and the pin's frame cost is **K-growing**: 23% of frames over, p99 61 ms — a new finding beyond the dossier); pin at the 5 ms corner (inert early, no interaction).
- **The code check the author deferred:** `apply` (universe.rs:662–666) sets `ship_ticks` for every ship unconditionally — the global min in `prune` reads all dolls today; his premise is code-fact, only E9 far scheduling stays open.
- **Novelty:** docs/HISTORY.md has zero prune/oldest entries; the page's own Open directions named this exact probe as unflown (d839).
- **Page:** faithful; added a checker note with regen digits, the two new arms, and the `ship_ticks` fact; marked "byte-identical" as proven-by-inertness only.

Gold because a standing premise on the memory-at-10⁹ bottleneck (worst case within ~2× of a local floor) is shown wrong by mechanism in shipped code, predictions were pre-registered and held, and adoption is one step: record the per-body `oldest` scope requirement before E9 far wiring lands.
