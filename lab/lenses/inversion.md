# Lens: inversion (Munger, Jacobi: "invert, always invert")

Do not ask how the engine succeeds; ask how it is guaranteed to fail, then check whether we are doing exactly that.

## How this lens attacks our engine
1. **The failure list first.** Write the five surest ways this project ends without a working game on one M1 (a law that compounds error, a scaling term that is quadratic in N, a seam between representations, memory that grows with play, a process that eats the builders' time). For each, find the measurement on main that says whether we are on that path today.
2. **Invert the bottleneck.** Take the board's top item and ask what would make it worse. If something we do now makes it worse, that is the result.
3. **Invert a success.** Take the most recent gold or merge and ask what it silently assumes. Find the scene where the assumption breaks and run it.
4. **Avoid stupidity before seeking brilliance.** Prefer removing one recurring mistake over adding one clever mechanism.

## From Julien's library (paraphrased)
- Munger: much of the advantage comes from consistently not being stupid rather than from being very intelligent; solve problems backwards.
- Taleb: knowledge grows by subtraction, by learning what does not work.
