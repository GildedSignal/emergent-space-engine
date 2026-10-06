# Lens: B17 within 60 s at the default cadence (xtask/src/behave) (a directed build)

B17's resonance legs run serially and the `Law` trait is not `Sync`, so `--law plane` at the default step 7 runs past the 60 s test limit (it passes at steps 4–6). Make the judge run its independent legs in parallel without changing any verdict or threshold: every planted law keeps its verdict, echo passes, and `--law plane --gates B17` finishes under 60 s on a 4-core machine. This touches the judge's harness only, never its criteria.

**How to build.** Work in this tree against `main`; your edits become `work/patch.diff`, which a reviewer applies later (you never commit, push or merge). Read docs/law.md, docs/HANDOFF.md ("In flight", "Astra's queue") and the references named above before writing code. Ship tests (each under 60 s) and run the named gates before and after; report every gate's detail line both ways. A gate is frozen: never edit a gate, a threshold or frozen evidence; if a gate seems wrong, say why and leave it. Keep every process under 2 GB. If the change cannot pass its gates, a clean measured failure with its diagnosis is a result: say so rather than patch around it.

Gold: the patch applies to main, its tests pass, and the named gates improve or hold, measured, with nothing else regressing.
