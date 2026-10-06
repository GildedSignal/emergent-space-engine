# Lens: The slack skin on the Binet cone (crates/encounters) (a directed build)

Lab `q-skin` (silver) and gold `20261006-0737-components-4643`: a slack Verlet skin keeps the encounter certificate exact in its regime and cuts setups per kick 12.6×; deferral and the wake calendar are killed; the literal skin is killed. Implement the slack skin in crates/encounters with its exactness argument as code comments and tests (zero misses against an independent truth across ε = 1e-8 to 1e-4, setups per kick measured). Gate: the crate's own tests, plus rung r8's truth construction.

**How to build.** Work in this tree against `main`; your edits become `work/patch.diff`, which a reviewer applies later (you never commit, push or merge). Read docs/law.md, docs/HANDOFF.md ("In flight", "Astra's queue") and the references named above before writing code. Ship tests (each under 60 s) and run the named gates before and after; report every gate's detail line both ways. A gate is frozen: never edit a gate, a threshold or frozen evidence; if a gate seems wrong, say why and leave it. Keep every process under 2 GB. If the change cannot pass its gates, a clean measured failure with its diagnosis is a result: say so rather than patch around it.

Gold: the patch applies to main, its tests pass, and the named gates improve or hold, measured, with nothing else regressing.
