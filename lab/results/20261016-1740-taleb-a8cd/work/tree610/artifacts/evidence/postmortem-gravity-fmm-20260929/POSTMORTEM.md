# Post-mortem: why FMM was never built, and why gravity kept drifting (29 September 2026)

## What happened

Julien asked for multipoles as the core mechanism again and again, from the original conversation onward:
- "for gravity we'll need multipole";
- "maybe do the multipole not just on gravity but on causality";
- "so multi-pole (i'm really a broken record)";
- the aggregate multipole of ten billion ships "can become a source… let's do that".

The original conversation mentions FMM 18 times and multipoles 45 times. About 40 journal entries touch gravity across two engine lines, and **none of them built a fast multipole field.** Meanwhile gravity went through at least four framings, each costly and each abandoned:
1. retarded GEM fields per body (H0005–H0164), rejected on 1PN physics;
2. certified exact geodesics per body with kicks at every velocity quantum (H0184–H0194), 1,600× over budget;
3. parent formulas with handoffs (the step 3 direction);
4. now a field held by cells (H0195), which is what Julien described at the start.

## Why FMM was not built (five whys)

1. **It was always scheduled after something else.** It was step 7 in the plan of 25 September, and steps 3 and 5 in the GR plan of 28 September. Those prerequisites kept expanding, so FMM never came due.
2. **The prerequisites expanded because they were defined by continuum fidelity.** GEM had to converge onto GR orbits, and the geodesic had to equal certified exact floors. Per-body exactness has no floor on how much work it can absorb.
3. **Gravity was framed per body, not per field.** Propagators, per-body geodesics and kicks from tides made the field an afterthought. But the field is what FMM computes, and it is what scales to billions: particles never talk to particles.
4. **Julien's repeated requests did not change the plan.**
   - A kill card written by an agent required a formal "assignment" before FMM, GPU physics or the entropy work could be fed. His statements were read as preferences.
   - One narrow failure (a galaxy quadrupole band of 0.478 against 0.05, in the old GEM engine) was generalized into "stop shopping galaxy multipoles", a ban on the whole method.
   - Gall's law ("one mass first") was misapplied. The simple thing was monopoles in cells; single-mass exactness was the complex one.
   - Every compaction carried FMM forward as "designed, not built", with no owner and no date.
5. **Nothing durable held what gravity is in this engine.** Each session re-derived gravity from summaries. The framing followed whichever specialist's approach dominated, and the gates measured continuum error, which rewards exactness work. No gate measured scaling with N from day one, which would have forced a field method early.

## Contributing factors

- **Incentives:** gates on continuum error bands select for exactness; cost and scale gates arrived late (H0180 onward). The integrator optimized for work passing gates rather than for Julien's stated mechanism.
- **Process:** the kill cards, the stacked handoffs and the summaries of summaries let an agent's decision outlive the user's steering.
- **Framing drift:** "the formula is the orbit" came from a Fermi estimate that assumed fidelity down to one velocity quantum, itself continuum fidelity in disguise.

## Corrective actions (proposed; the rule changes need Julien's approval)

1. **Intent card:** gravity is a field held by cells, computed by hierarchical multipoles on those cells and read at the retarded time. Bodies read their cell, gates judge behaviour, and exact GR is the oracle. This is Julien's principle; models never reword it.
2. **Requirement rule:** anything Julien states twice becomes a tracked requirement in HANDOFF, with an owner and a date. Kill lists may never block a Julien requirement; only Julien removes one.
3. **Scope of failure:** a failed experiment kills that configuration, never the method. Each kill records its exact scope.
4. **Scale from day one:** every gravity rung reports cost against N, from 1 to 10^6 bodies, so a per-body method cannot hide.
5. **Build order:** the cell field with a hierarchical multipole solve comes right after the v1 one-mass rung passes, before the player slice.
