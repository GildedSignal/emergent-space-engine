# Lens: Fermi (estimate before building)

Every claim gets an order-of-magnitude estimate before a line of code: decompose, assign rough values, multiply, check units, bound with known constraints. A Fermi estimate wrong by 10× still deletes half the solution space.

## How this lens attacks our engine
1. **The 10⁹ budget.** For the board's top item, estimate bytes per body, events per body per game-second, and nanoseconds per event at 10⁹ bodies on one M1 (8 GB, about 10¹⁰ simple operations per second across cores, memory bandwidth about 60 GB/s). Which term breaks first, and by how many orders of magnitude?
2. **Distinctions per game-second.** Estimate how many bits of live distinguishing information a typical scene creates per game-second (kicks, encounters, player actions) against what reabsorption removes. Is H_live bounded in steady play?
3. **Check a claim.** Pick a recent result's headline and re-derive its order of magnitude independently. If the result and your estimate disagree by more than 10×, find which is wrong.
4. **Kill early.** If the estimate already rules an idea out, stop and report that: it is the cheapest possible result.

## From Julien's library (paraphrased)
- Musk: physics is the only real constraint; reason from first principles and the limits they set.
- Shannon: information has a floor; you cannot store less than the surprise.
