# Lens: mathematical representations: structure, composition and scale (the macro level) (a directed deep pass)

**Scope.** How the whole is organized: category theory (functors between scales, sheaves for local laws glued into global state, lenses and optics for observation as a pure function, operads and wiring diagrams, polynomial functors and categorical systems theory), set theory (does it give us anything?), order theory and lattices (causality, the canonical order of ties), semirings and tropical (min-plus) algebra, monoids for exact parallel reduction, ultrametrics and p-adics for hierarchies of dolls, renormalization and coarse-graining that keep every individual, multiresolution and wavelets, Kolmogorov complexity and succinct structures for populations, and anything that makes "one law at every scale" or "every body real at the information floor" structural. Julien asked directly: would set theory help, and category theory?

**The yardstick: the behaviours we need** (docs/PRINCIPLES.md, docs/law.md, docs/plane.md). A representation matters only if it gives one of these more cheaply, more exactly, or makes it emerge:
- exact and deterministic: integers decide, bit-identical across order, threads, CPU and GPU;
- change is an addition: cheap updates, associative reductions that parallelize without changing bits;
- compute only surprises: zero work between events, certificates that say when something can happen;
- one law at every scale (scale as an exponent, self-similarity); each scale resolves only what matters to it (principle 33);
- GR native: geodesics as trivial as straight lines; light and gravity travel at c; frame dragging, ergospheres, horizons, lensing, clocks;
- symmetry is found by representation (principle 32: "under the right representation many symmetries can appear, this is a leitmotiv of compute paradigm shifts");
- memory at the information floor: every body real, never averaged, tails kept;
- bounded work per frame; emergence (no categories: dimensionless numbers choose regimes).

**How to work.** Julien, 5 October: "i want a glm pass on mathematical representations that could help us … many of them old and new and obscure at many levels from micro to macro based on desired behavior, math is a big field, this is not a small ask … in depth". Start from the behaviours, not from a list of fields (principle 18: "you start from a listicle instead of what are our requirements"). Search widely, old and new, famous and obscure, and in the language of origin. For each candidate: the structure in one paragraph; which behaviour it would give us and at which level; what it costs and whether it stays exact in integers; who used it and where it worked (skin in the game first); what we already have that it would replace or delete (read docs/law.md and docs/representation.md; do not resell what we have); and the cheapest test that would kill it. Rank by gain × probability ÷ cost of adoption. Then take your top two or three and run their cheapest falsifying probes in your folder (never edit the crates), with predictions written first. A catalogue without probes is a lead, not silver.

Deliver: `dossier.md` (the ranked catalogue, then the probes and what they showed), the probe scripts, and a one-paragraph "what this lens may have made you miss".
