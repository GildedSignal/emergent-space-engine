# Lens: premise red-team

Attack the premise before the letter. Your target is `docs/representation.md`, the design, which is judged against `docs/PRINCIPLES.md`.

1. **Premises first.** For each load-bearing claim, ask whether it is true, and find the cheapest case that would make it false. Do this in order:
   1. The two-body doll: 1PN effective one body, with ν only in the energy map.
   2. Binet cells: the linearised band equation as a rotation, and orbits repeating per cycle.
   3. Kicks and cycle derivatives absorbing perturbations.
   4. The dense order being bit-identical to the sparse one.
   5. The view gathered at the past light cone.
   6. Costs of about zero for undisturbed bodies.
2. **Principles.** Where does the design violate a principle: ticks, bandaids, error size instead of error type, categories, or something that isn't local?
3. **Missing behaviours.** What will a player see that is wrong, and which rung in `lab/rungs/` would miss it?
4. **Run the cheapest falsifier yourself** for your strongest attack: float, at most 60 s.

**Deliver** a ranked list of the attacks, with your falsifier's numbers for the top one. For each attack, name the rung criterion that should have caught it, or say that none does. A premise that survives is worth reporting too.

**Blind spot:** red-teams overweight exotic cases. Rank by how likely the player is to see the failure.
