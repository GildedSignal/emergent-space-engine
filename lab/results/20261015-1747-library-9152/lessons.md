# Five lessons from Julien's library for the N ladder (28 → 10⁹)

Aimed at the board's first gap. Quotes verbatim from `work/readwise.json` (Readwise export, this run). Full grounding in `dossier.md`; each lesson names the open decision it changes.

**1. Musk — question the requirement, then delete; the cap family is automation before deletion.**
> "Step one should be to question the requirements… And then delete, delete, delete." / "Delete any part or process you can. You may have to add them back later. In fact, if you do not end up adding back at least 10% of them, then you didn't delete enough." — *Elon Musk*, Isaacson
Mechanism: five days tuned *how* the scan's read is cached (ring, ONCE, knee pricing, defaults) — accelerating a read whose requirement ("the scan captures the doll's whole retention") was never questioned; the measured law (knee = demotions ≈ N) makes every cap a fence around an O(N) read.
Change: freeze the cap family (as 0619/f55d conclude); build the neighbourhood read (co-orbital phase-neighbour certificate, gold 20261006-0346), which deletes the capture.
Test: one instrumented burn flight at 10⁵ — rank the scan's candidates by phase distance to the player; small phase-rank (≤ ~4) means the read is deletable.

**2. Musk — build the machine that builds the machine: the mint path is the factory.**
> "It's not the product that leads to success. It's the ability to make the product efficiently. It's about building the machine that builds the machine. In other words, how do you design the factory?" — *Elon Musk*, Isaacson
Mechanism: the product is the compiler turning a ~120 B key into an exact trajectory; retained bytes are work-in-process inventory, factory throughput is the mint (4.6 µs, bit-identical). A cheaper mint cuts every miss at every N; a better cache only moves the knee.
Change: optimization effort goes to mint + record format, not retention policy; the rung's cost metric becomes µs per mint.
Test: the page's named gold step — fly the two-line demote-passages variant digest-identical, measure the in-flight re-mint bill.

**3. Feynman — derive, don't memorize: the record is a lookup the engine can re-make.**
> "They had wasted all their time memorizing stuff like that, when it could be looked up in fifteen minutes." — *"Surely You're Joking, Mr. Feynman!"*
Mechanism: compiled orbits are memorization, the key is understanding (P6: 120,083/120,083 cycles re-mint bit-identical); memorizing pays only when the lookup is dearer than the memory, and measured reuse distance (≈ one demotion wave on burn) says most of the belt reads cold.
Change: retention is a pure accelerator with a priced budget (promos − dem = hits_sat − hits_cap); nothing in the law may *require* a retained entry — demote-after-kick is outcome-free.
Test: a retention-deleted arm on coast at 10⁵ — digest identity and wall within global retention's own +12.5% puts deletion on the table; add back the 10% that hurts.

**4. Taleb — size by the maximum, not the mean; the fence is sized by damage, not evidence.**
> "The maximum of an average is necessarily less volatile than the average maximum." — *Fooled by Randomness* / "When we look at risks in Extremistan, we don't look at evidence (evidence comes too late), we look at potential damage." — *Antifragile*
Mechanism: mean hit-rate (85.3%) hides the cliff (43.3/45.4/92.1% at 16k/65k/knee); the governing quantity is max reuse distance — a law of the read stream; the ruin case (14.8 GB pinned against a 1.5 GB box) was knowable as damage before it fired.
Change: retention gates report reuse distance (p50/p99/max) as primary, hit-rate derived; caps derived from the measured knee, never tuned; the byte-cap fence ships always-on, sized by box damage.
Test: one script over an existing flight's mint/fill log (counters already in the 0619/f55d patches).

**5. Naval + Waitzkin — the 10⁹ class is zero marginal cost; prove it slowly, then fast.**
> "Fortunes require leverage… products with no marginal cost of replication (code and media)." — *Almanack of Naval Ravikant* / "We may cover its every inch with leather or we can make sandals." + "We have to be able to do something slowly before we can have any hope of doing it correctly with speed." — *The Art of Learning*, Waitzkin
Mechanism: 10⁹ on 8 GB is only arithmetic if the marginal body costs ~0 — the belt as program (0.126 bits/body, 98bc) is the leveraged product; live records are inventory (measured: 2,333 B/body, flat in N, 292× over the ≤ 8 B/body budget). Sandals: capability on the body (its key), not paving the machine's road with N-scaled stores.
Change: the rung metric becomes Δfootprint/ΔN, target single digits; every rung proves digest identity before scaling.
Test: this run's flights (`regen.sh`): slope of peak footprint at N = 0/10³/10⁴/10⁵.

---
Blind spot: analogies earn their place only by changing an open decision — each above names one. The lab had already measured every mechanism; the lessons order decisions, they add no physics.
