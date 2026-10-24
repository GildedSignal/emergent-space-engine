# Second deep pass (20 October): read this first

The first pass of this lens ran on 5 October, before the plane's measurements existed (find its runs: `git for-each-ref 'refs/remotes/origin/claude/lab-*-m-meso-motion-*'`, and read their dossiers). Since then the scoreboard (`docs/HANDOFF.md`) measured the gaps: the star's doll kicks every belt body ~9,000 times an orbit on one clock (the gates hold at 8-16 per the body's own orbit; zero-kick secular phasors are killed for the belt, 14.5% pass; every resolved kick refits), a kick costs 75-160 µs against a ~50 ns floor (one compiled table per body, 90% of its panels never read), and a live body holds ~2.5-5.1 KB against a ~6 B target. Julien, 14 and 20 October: kicks "on certificates breaking", "we just need the generators", shared structure refined per body (a formation's vector refined per ship until one deviates), and "We need to find OOM improvements in micro and macro".

Your job in this pass: find what the first pass and the 400 runs since did not see. Propose at most two representations, each native to the operations at stake, that would move one of those rows by an order of magnitude or more, and run the cheapest probe that could kill each. Read the wiki pages first (`lab/wiki/index.md`); a repetition of a refuted idea is not gold unless you show what differs.

---

# Lens: mathematical representations: motion and orbits (the meso level) (a directed deep pass)

**Scope.** How motion is represented: action-angle and Delaunay variables, the hidden symmetries of the Kepler problem (SO(4), SO(2,1), Runge–Lenz, the Binet cone we found), regularizations (Levi-Civita, Kustaanheimo–Stiefel, Sundman, Burdet–Ferrándiz, Stiefel–Scheifele), Hamilton–Jacobi and generating functions, Lie series and Lie transforms, Poincaré maps and return maps, discrete mechanics and variational integrators, reversible and integer maps, normal forms and KAM, the hodograph, memoized dynamics in the spirit of Hashlife, and what turns "kicks per orbit" (the plane's dominant cost) or close encounters into something cheaper or exact.

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
