Working...
Check complete. **Grade: gold.**

**Reproduction.** Applied `work/patch.diff` to the clean tree and ran the dossier's command 7 times. Every deterministic output is bit-identical across runs and allocators: loop hash `159e3779b97f4a7c`, settle digest `b4f07b75…` (with the non-vacuous system repeat), census 9.0 allocs / 2,872 B with the same class histogram, bump traffic 9,331,410 B.

**The one discrepancy, resolved.** The runner's regen showed a +14% bump "saving" (39.08 → 33.65 µs). Six fresh runs show that is system-arm load noise, not allocation cost: unloaded system runs 32.65–34.57 µs while bump sits tight at 33.63–33.84 — the warm system arm is actually ~0.8 µs *faster* than bump (tcache-warm reuse vs fresh pages), which independently confirms allocator work owns ≈ nothing of the kick.

**Adversarial cases.**
- Extended the census to **all 23 plane ships** (outside the author's one-ship domain): 8–14 allocs/kick, 2.5–4.6 KB, 29–43 µs across haulers/orbiters/skimmers — no class approaches the ~100× that would revive an arena.
- Full-width ~127-bit i128 division: 33.5 ns vs the author's 30.9 — the ~900-division-equivalents close is robust to operand width (and honestly flagged as an estimate).
- Verified by reading: `bind_in` calls `Rebinding::from_state` directly; `Catalogue` is slots + a free list — key search is absent by construction.

**Predictions.** Pre-registered before the run (file times consistent). The pre-registered kill fired and was honored (P4: 0.3% < 10% floor). P1/P2 missed low and are disclosed as calibration errors; the shipped cost_split prints 34.4 µs for the same path on this box, so the "wrong arm" escape doesn't apply. One nit recorded: P5's "held" is generous in the letter, though the substance is what the evidence shows.

**Novelty.** No prior run censused kick allocations or ran an allocator A/B; fa08/30e1 left allocations and key search as standing suspects. This closes two of three and rewrites open direction 1 to a pure panel/division-count question — same genre as the integrator's gold `components-4643` (a measured ceiling that deletes a build path, nothing to build).

Tree restored to its pre-check state (`?? lab/results/` only); `check.md` written; nothing else in the run folder touched; no git operations.
