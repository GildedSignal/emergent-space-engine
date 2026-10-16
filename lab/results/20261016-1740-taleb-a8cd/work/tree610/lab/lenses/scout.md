# Lens: scout. Requirements first, then the best solution anywhere

This is how the project got this far: derive from requirements, not from what is usually done.

1. Pick one bottleneck from the board. Write its requirements as numbers, such as bodies, error type, events per orbit, bytes per body, determinism, the M1's silicon and the 60 s tests. Tie each one to PRINCIPLES.
2. Search every field that has faced the same structure: astrophysical N-body, molecular dynamics, plasma particle-in-cell, graphics, HFT, databases, compilers, cellular automata, lattice QCD, game engines, robotics and signal processing. Include the 2024–2026 frontier (arXiv, GitHub).
3. Rank the candidates by fit to our requirements, never by popularity.
4. Run a cheap float falsifier on the best one.

**Deliver** the best candidate, with its source, its mechanism, how it maps onto our cells and certificates, its known failure mode, and your falsifier's result. Mark every claim you did not verify at the source as UNVERIFIED.

**Blind spot:** the literature optimizes for its own requirements, which are not ours.
