# Lens: SpaceX

Think like a SpaceX engineer: physics is the only rule, and the order is question, delete, simplify, accelerate, automate last.

## How this lens attacks our engine
1. **Requirements, each with a named owner.** List every requirement on the engine (billions of bodies, 8 GB, one law at all scales, cells with multipoles, five modes) and the person who owns it. A doc or a model is not an owner: a requirement with no human name is deleted.
2. **Delete.** Which mode, crate, gate, document or per-body step goes first? If we never add back about 10% of what we deleted, we did not delete enough.
3. **Idiot index.** For each subsystem, divide the measured cost (ns per event, bytes per body) by its physical floor (entropy changed, information stored). Which ratio is worst, and is that where we are working?
4. **Simplify, accelerate, then automate.** Is any harness, scheduler or agent loop being built before the design it serves is stable? What is the rate-determining step this week, and is its cycle time measured in hours?
5. **Physics as the only limit.** Separate real limits (c, exact integers, 8 GB, thermals, the 60 s test) from recommendations (modules, ticks, float tricks, our own docs). Push each real limit until it breaks.
6. **Hardware-rich, fast iteration.** How many full build-run-measure loops per day on the real fanless M1, heat included? Blow up small, cheap prototypes early: a failed test kills that configuration, not the method.

## From Julien's library (no highlights from Founders episodes on Musk or SpaceX; these come from Isaacson and Farnam Street)
- "Make them less wrong and dumb, because all requirements are somewhat wrong and dumb. And then delete, delete, delete." (Walter Isaacson, *Elon Musk*)
- "if you do not end up adding back at least 10% of them, then you didn’t delete enough." (Walter Isaacson, *Elon Musk*)
- "Always wait until the end of designing a process—after you have questioned all the requirements and deleted unnecessary parts—before you introduce automation." (Walter Isaacson, *Elon Musk*)
- "The only rules are the ones dictated by the laws of physics. Everything else is a recommendation." (Walter Isaacson, *Elon Musk*)
- "It’s about building the machine that builds the machine. In other words, how do you design the factory?" (Walter Isaacson, *Elon Musk*)
- "Designers had to feel the immediate pain if something they devised was hard to engineer." (Walter Isaacson, *Elon Musk*)
- "what are the material constituents of the batteries? What is the spot market value of the material constituents?" (Elon Musk, quoted in Farnam Street, *First Principles: The Building Blocks of True Knowledge*)
- "You should take the approach that you, the entrepreneur, are wrong. Your goal is to be less wrong." (Elon Musk, quoted in Farnam Street, *The Wrong Side of Right*)

## Blind spot of this lens
Delete-and-rebuild is cheap for a rocket you can blow up weekly; here a frozen law is a one-way door, and a deleted certificate may have been the only thing catching a rare divergence.
