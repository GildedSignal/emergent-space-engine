# Lens: mathematical representations: numbers and arithmetic (the micro level) (a directed deep pass)

**Scope.** How numbers are held and combined: integer and fixed-point forms, shared exponents and block floating point, logarithmic and residue number systems, posits and unums, p-adics, dyadic and Stern–Brocot rationals, continued fractions, exact real arithmetic, interval and affine arithmetic, balanced ternary, CORDIC and Minsky circle algorithms, sigma-delta carries, error-free transformations, SWAR and bit-slicing, and whatever else serves "change is an addition", exactness across CPU and GPU, and the cheapest arithmetic on an 8 GB M1.

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
