Working...
Check complete. `check2.md` is written to the run folder; nothing else there was touched, and no git operations were run.

**Grade: gold** (second checker, blind to the first).

**What I did:**
- **Reproduced** everything from a clean tree + `work/patch.diff` (adds only `cross.rs`, byte-identical to the folder copy): all six dossier commands regenerate `evidence.log` **bit-for-bit** — 40000/40000 and 160000/16000 cross candidates (100%), 80000/320000 sections all Cross-kind, 0 setup evals, hits 36/145/34 at 51–55 evals/hit, truth audit 0 missed/0 extra, truth_evals=5988010 identical, station diag 6.31e-2/1.41e-1 exact. The guard's `method=0` is the disclosed print bug (counter never incremented; provably 36 matched events).
- **Verified pre-registration**: `predictions.md` (07:21:40) precedes `evidence.log` (07:26:32); P1–P3 held, P4's failure honestly reported through the pre-registered P5 mechanism.
- **Seven adversarial cases** (my probe binary `cross2.rs`, left in `crates/encounters/src/bin/`): held-out seed 3, doubled horizon H=40, ρ=10⁻³ and 10⁻⁵, e_B=0.2, tight formations Δϖ=10⁻³/10⁻⁴, plus the pre-registered-but-never-run rankscale n=240. Soundness held 0/0 in every one; saturation stayed 100% everywhere.
- **Novelty**: no H entry or doc covers two-swarms-crossing; taleb-09b5 was intra-formation only. Law.md's dense-order quote is accurate.

**Notable findings for the author's record** (in check2.md): swarm A also fails the clump test (dia 3.4e-3 ≫ ε_u 1.5e-4 — the adopted train has *zero* coverage in engagement scenes, stronger than claimed); the "what would make it wrong" Δϖ≲10⁻³ escape hatch doesn't exist (the Rayleigh e-spread floors dia_B at 4.35e-3 = 11× ε_u even at Δϖ=10⁻⁴); rankscale held-outs were never run (I ran them — max rank grows 6→9 with n, consistent with the kill).

Gold per the lab's own precedent (components-4643: a decisive, pre-registered kill with nothing to build): a measured boundary of the board's top scaling risk plus a pre-adoption kill of a blind certificate, fully regenerable.
