Working...
Check complete. `check2.md` written with **Grade: gold**.

**What I did:**
- **Reproduced** all four dossier commands from the clean tree with `work/patch.diff` applied (patch adds only the example, byte-identical to the run copy): every entropy/store number bit-exact — state floor 49.904→68.263 bits/ship (K=1→1024), shelf 7.94 B/ship at K̄=8 with mismatches=0 every epoch including the K̄≈4.5 repack, compaction 1.22 µs/kick, and `verify a` exactly 1.75×10⁻⁴–4.96×10⁻³ encounters/body/orbit. Only wall-clock timings differed (machine load).
- **Adversarial probes** (throwaway example, removed after): K=8192 floor ≈66 bits — far under the pre-registered 140-bit kill line; full saturation (x=1.0, K̄=24) stays bounded at 8.11 B/ship with the floor-gap peaking then *declining*, bit-exact throughout; `Shelf::bytes()` audited as honest whole-store accounting; the Fermi/belt-0 arithmetic cross-checked against r8 v2's own numbers.
- **Novelty/goal fit:** no prior H_live measurement exists (HANDOFF line 69: "not measured yet"); predictions were pre-registered and held (P1–P5).

**Verdict rationale:** reproduces bit-exact, predictions held, measures the named unmeasured decider for "10⁹ in 8 GB", and corrects the compute-vs-memory premise (8% of one core, not 190 cores) — adoptable in one step (no code, one B18 scene, f as the memory dial).

**Defects found (listed, none load-bearing):** the draw account is 50·K not 44·K (Δt is a 17-bit draw; the K=256 ratio is 196×, not 173×); the "correlated victims help compression" hedge is contradicted for the shipped store (8.19 vs 7.94 B/ship at K̄=8 — set structure isn't exploited); the 0.3%/core kick figure is quoted, not measured.
