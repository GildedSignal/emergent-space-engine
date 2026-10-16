# Lens: the law's red-team (before its freeze)

Attack `docs/law.md` (law `es-space-v2`, a draft that changed heavily on 30 September), judged against `docs/PRINCIPLES.md` (principles 1–35) and `docs/representation.md`. Premise first, then the letter.

1. **Premises, in this order:**
   1. the compiled geodesic's representation (`crates/space/ENVELOPE.md` on branch `wt/envelope`, if present, else the crate docs): scale as an exponent, shape (k, q), weak field as a series in q, exact rebinding remainders;
   2. the tide selector τ (averaged kicks below τ₀, the Hill problem beyond);
   3. resonance through the normal form;
   4. the battle frame as Fermi normal coordinates along an exact tube;
   5. populations (program plus scars, packed blocks, identity by provenance, H_live as the memory budget);
   6. "every body is real", with averaging only for predictable behaviour;
   7. gates B11–B15.
   For each, ask whether it is true, and find the cheapest case that would make it false.
2. **Principles:** where does the law contradict one? Look especially at 14 (no ticks), 19 (bandaids), 32 (symmetry is found), 33 (each scale resolves what matters) and 34 (the oracles guard).
3. **Missing behaviours:** what would a player see that is wrong, and which gate would miss it?
4. **Run the cheapest falsifier yourself** for your strongest attack (float, at most 60 s).

**Deliver** a ranked list of attacks, with your falsifier's numbers for the top one. For each attack, name the gate that should catch it, or say that none does. Premises that survive are worth reporting too.

**Blind spot:** red-teams overweight exotic cases. Rank by how likely the player is to see the failure.
