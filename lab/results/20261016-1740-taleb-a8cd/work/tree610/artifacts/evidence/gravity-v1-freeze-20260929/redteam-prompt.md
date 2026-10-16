READ ONLY: do not edit, create or delete files. Your whole answer is your final reply. Not making mistakes matters more than efficiency.

Red-team the DRAFT contract docs/gravity-law.md (law es-lattice-gravity-v1) before its gates freeze. It replaces an exact-floor contract with a cheap local integer law: a drift-kick in a flow field held by cells, gated on behaviours against an exact-GR oracle. Context: AGENTS.md, docs/HANDOFF.md, docs/engine.md, docs/universe-quanta.md, and the oracle files named in the contract.

Find, with quote and line evidence:
1. Ways a correct implementation could FAIL a gate, or a wrong one PASS, for each of B1–B9. Check tolerances against what a time-symmetric integrator can achieve at the stated step counts, and whether each gate's case set really exercises it.
2. Anything undefined that could change a canonical outcome (a law must be a fixed algorithm).
3. Contradictions with the principles: locality, cost only on change, observables on demand, determinism across partitions and event order.
4. Whether the premise probe's kill criteria actually test the premises the plan depends on.
5. Any requirement that is continuum fidelity in disguise, or busywork.

Rank the findings: 1 = the gate outcome would be wrong; 2 = an ambiguity that could change outcomes; 3 = cosmetic. Say plainly what is right. If a check finds nothing, say so.
