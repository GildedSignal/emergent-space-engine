You are a prior-art scout. Read only; create no files except in /private/tmp/glm-scratch/prior-art/. Do not run git.

First read /Users/julien_laurent/Research/emergent-space/docs/PRINCIPLES.md (the goal and philosophy). Then read /Users/julien_laurent/Research/emergent-space/docs/gravity-law.md and /Users/julien_laurent/Research/emergent-space/artifacts/runs/gravity-v1-freeze/probe-out.md.

**The problem.** A game engine moves billions of bodies in curved spacetime. Gravity is a field held by a hierarchy of cells, built from integer mass moments, in the style of fast multipole methods (FMM) and particle-mesh codes. The step size must NEVER come from the body's own state: "no ticks, not even per body". A probe showed that Δ = η·(the body's dynamical time) makes energy error grow, and that it lets distant light jump over a lens. We want long-term bounded error, deterministic integer arithmetic, and cost paid only at events: cell crossings, field-certificate expiry, contacts and commands.

This is a solved problem somewhere. Find how others solved it, using the web (arXiv, ADS, GitHub) and your own knowledge. Candidates to check:
- block and hierarchical time steps (GADGET, PKDGRAV, Pelupessy's HOLD/HUAYNO);
- time-symmetric adaptive steps (Hut–Makino–McMillan);
- Sundman and logarithmic time transforms, and algorithmic regularization (Mikkola);
- Kepler-drift (Wisdom–Holman) and "drift in the parent's field" schemes;
- event-driven molecular dynamics;
- asynchronous variational integrators (Lew, Marsden, Ortiz), which give per-element steps that stay symplectic;
- integer or bit-reversible integrators (Levesque–Verlet);
- FMM on GPUs with multipoles that are polynomial in time;
- lattice-gas and cellular-automaton gravity;
- how space games (Kerbal, Children of a Dead Earth, Universe Sandbox, Elite) handle patched conics and time warp.

**Output (your final reply), at most 40 lines.** A ranked list. For each technique, give:
- its name and a primary source;
- one line on the mechanism;
- how it maps to cells owning the step;
- its known failure mode;
- the cheapest float test that would falsify it for us.

End with your single recommendation, and the one thing the literature says we are getting wrong. Mark every claim you did not verify at a source as UNVERIFIED.
