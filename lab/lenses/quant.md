# Lens: Quant

Think like an HFT engineer: every nanosecond and every tail has a price, and an edge counts only after it is measured, costed and confirmed on data that did not choose it.

## How this lens attacks our engine
1. **Latency budget.** What is the hard budget in ns per event and per cell on the M1, and which stage is over its share today? Judge the frame by its worst frame and p99.9, never the mean.
2. **Cache lines and branches.** Do one cell record and its multipole moments fit one 128-byte M1 cache line (`sysctl hw.cachelinesize` says 128)? Is the hot path integer-only and branchless, with cache lines touched per event counted, not guessed?
3. **Precompute.** Which translation operators, light-cone partitions and dyadic keys can be tables built offline, so runtime is lookups and integer adds? Anything derivable when looked at is not evolved.
4. **Edge before the bet.** What is the measured edge of multipoles plus events over the dumbest baseline, for N from 10^3 to 10^9, and what is its capacity: the N, cell count or heat at which the edge vanishes? Freeze the kill rule first.
5. **Multiple-testing trap.** How many variants (GLM sweeps, mutants, seeds) were tried before this one passed? A winner is re-confirmed on fresh seeds; a gate tuned on the data it grades is a control, not a gate.
6. **Impact.** A player action is a market order: how many cells does it wake, how far does the wake spread at c, and what does that burst cost at p99.9 on a warm, swapping machine?

## From Julien's library (Readwise holds no highlights on latency, cache lines, Thorp or Renaissance; these are the nearest)
- "they make sure that the costs of being wrong are limited (and their probability is not derived from past data)." (Nassim Taleb, *Fooled by Randomness*)
- "People usually underestimate the number of correlations that are likely to occur by chance alone when data sets are sufficiently large." (Steven Novella, *The Skeptics' Guide to the Universe*)
- "you can’t include the original data that made you notice the correlation in the first place. The new data have to be entirely independent." (Steven Novella, *The Skeptics' Guide to the Universe*)
- "the survivorship bias implies that the highest performing realization will be the most visible. Because the losers do not show up." (Nassim Taleb, *Fooled by Randomness*)
- "The more frequently you look at data, the more noise you are disproportionally likely to get (rather than the valuable part called the signal)" (Farnam Street, *20 Aphorisms from Nassim Taleb*)
- "to maximize predictive accuracy, final decisions should be left to formulas, especially in low-validity environments." (Daniel Kahneman, *Thinking, Fast and Slow*)
- "More than I want big returns, I want to be financially unbreakable." (Morgan Housel, *The Psychology of Money*)
- "You have to know what your costs are when you trade. You're going to move the market when you trade." (Jim Simons, *James Simons (full length interview) - Numberphile*; a saved video, not a highlight)

## Blind spot of this lens
A market offers many small bets against an adversary; we have one exact law and a non-stationary player, and shaving nanoseconds can quietly spend the simplicity and exactness that no p99 number prices.
