# Lens: first principles, one component at a time

Take one component: the cells, the β rule, the event queue, the integer representation, generators and certificates, or storage.

**For that component:**
1. What requirement does it serve? Quote the PRINCIPLES line that owns it. A requirement with no owner is a candidate for deletion.
2. What is its floor, set by physics or information theory: the bits of state, the operations per event, the bytes moved per event, the memory traffic?
3. How far is our design from that floor? That ratio is the idiot index.
4. What design sits within 10× of the floor? Build a small version and measure it.

**Deliver** the component with the largest gap and a design closer to its floor, with the measurement.

**Blind spot:** a local optimum can move cost to another component. Measure the neighbours too.
