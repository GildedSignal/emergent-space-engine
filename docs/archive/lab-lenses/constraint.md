# Lens: the constraint (Goldratt's theory of constraints, on measured data)

A system's throughput is set by one constraint at a time. Improving anything else is waste. Find it in measurements, never in opinions.

## How this lens attacks our engine
1. **Measure the whole.** Run the plane (`cargo run --release -p xtask -- universe --bench`, `--kick-bench`) and the gates (`behave --law plane`, `engine-judge`) on main. Where does the time go (`where_the_time_goes_ms`, `engine_cost_by_kind`, `frame_cpu_ms`)? Which gate fails, and why?
2. **Name the one constraint** for the goal (billions of bodies, smooth frames, GR behaviours, 8 GB). Show the number that makes it the constraint.
3. **Exploit, subordinate, elevate.** What is the cheapest change that gets more out of the constraint as it is? What else should be slowed or stopped so that it is never starved? Only then propose a new mechanism.
4. **When the constraint moves,** say where it goes next, so the next run starts there.

## From Julien's library (paraphrased)
- Goldratt: an hour lost at the bottleneck is an hour lost for the whole system; an hour saved elsewhere is a mirage.
- Musk's algorithm: question the requirement, delete the part, simplify, then accelerate, and automate last.
