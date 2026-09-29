# Lens: Taleb

Ask what breaks, not what is fastest: find the fragility, survive first, optimize only what cannot ruin us, and remove before adding.

## How this lens attacks our engine
1. **Fragility.** Where is the engine concave, so that a small shock does outsized harm (one late event, one overflowing cell, one rounding carry that compounds)? Double the load or the seed spread: does cost or error more than double?
2. **Fat tails.** Is the workload Extremistan (one black hole, one 10^6-ship fleet in one cell, one player burst), so that the mean cost lies? Size the allocator and the 8 GB budget for the worst cell, not the average one.
3. **Ruin before optimization.** List the unrecoverable states (silent nondeterminism across hardware, swap death, thermal shutdown, a corrupted canonical history). Which are still reachable today, and why is any nanosecond shaved before they are closed?
4. **Barbell and convexity.** Is the spine exact and paranoid (integer law, certificates) at one end and are there many cheap, disposable probes (60 s tests, GLM sweeps) at the other, with no medium-risk hybrid between? Which bet has capped loss and open upside?
5. **Via negativa and iatrogenics.** What can we delete, and which recent intervention (a mode, a bandaid, a process change) did more harm than good? Before removing a fence, why was it built?
6. **Skin in the game and Lindy.** Who pays if a gate or a law is wrong, and is it the owner? Prefer proven machinery (integers, tree codes, multipoles, all decades old) over novelty; a new idea must earn its place.

## From Julien's library
- "anything that has more upside than downside from random events (or certain shocks) is antifragile; the reverse is fragile." (Nassim Taleb, *Antifragile*)
- "its risk of breaking makes anything you do to improve it or make it “efficient” inconsequential unless you first reduce that risk of breaking." (Nassim Taleb, *Antifragile*)
- "clip your downside, protect yourself from extreme harm, and let the upside, the positive Black Swans, take care of itself." (Nassim Taleb, *Antifragile*)
- "Knowledge is subtractive, not additive—what we subtract (reduction by what does not work, what not to do)" (Nassim Taleb, *Incerto 5-Book Bundle*)
- "In Extremistan, inequalities are such that one single observation can disproportionately impact the aggregate, or the total." (Nassim Taleb, *The Black Swan*)
- "Things designed by people without skin in the game tend to grow in complication (before their final collapse)." (Nassim Taleb, *Skin in the Game*)
- "The principle of intervention, like that of healers, is first do no harm (primum non nocere)" (Nassim Taleb, *Skin in the Game*)
- "That which is “Lindy” is what ages in reverse, i.e., its life expectancy lengthens with time, conditional on survival." (Nassim Taleb, *Skin in the Game*)

## Blind spot of this lens
It prizes robustness over speed and can veto every step: the barbell needs a real speculative end, fat-tail fear can freeze measurement-driven progress, and it says nothing about how to build fast.
