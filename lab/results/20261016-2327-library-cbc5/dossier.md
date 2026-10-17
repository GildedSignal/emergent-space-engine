# Dossier — 20261016-2327-library-cbc5 (library lens)

**Claim:** at 10⁹ the compact↔live promotion's **byte size never binds** — the demotion dwell does, and the record diet makes even dwell free — while the mint+demote **cost** is numerically the same 23 µs requirement as e7ef's kick (promotions ARE the kicks), so the promotion's only 10⁹ levers are cadence (÷8) and delete coverage (ES_SECULAR = a promotion-skip), and the record diet is a 10⁶-flyability lever, not a 10⁹ one.

**Bottleneck:** the board's named open item under nladder: "the smallest promotion between a compact body and a live one". Expected gain: decides which of the two in-flight efforts (record diet vs secular delete) moves 10⁹ — deletes a redundant effort, not 10× compute.

**Evidence** (`python3 work/promo_ledger.py`, <1 s, pure arithmetic from page-cited constants; controls reproduce e7ef/98cb: 23.1 vs 23 µs, 5.1 vs 5.1 M1 cores, wall 1.19–1.65×10⁶):

| term | shipped rate 3.55e-5 ev/B/gs | +÷8 split | +61% delete | + diet ~80 B |
|---|---|---|---|---|
| promotions/s at 10⁹ rtf 100 | 3.55M | 444k | 173k | — |
| mint+demote cores at 44 µs (bind/refit share) | **157** | 19.7 | **7.7** | — |
| resident at dwell 1 game-s | **35.5k** ≈ measured N_hot 13–27k (ba64) | 4.4k | 1.7k | — |
| dwell* busting 6 GB, ~5 kB record | **33 gs (0.1% of interval)** | 267 gs | 685 gs | — |
| dwell* busting 6 GB, ~80 B record | 2,808 gs (10%) | 22,460 gs (80%) | **57,591 gs (205%: never)** | ✓ |

- **Working-set identity (no fitted parameter):** λ×1 game-s = 35,500 vs the measured hot set 13,000–27,000 (ba64, rtf 100) — the hot set IS the dwell≈1-s working set. A certificate-clear-class demotion timer is the only memory rule needed.
- **Promotion≡kick:** every fired event mints a live body on the shipped store (fire rate 1.000, accumulator inert — 3294), and the re-fit is 84–89% of kick cost (b063), so promotion CPU = kick CPU: 157 cores at shipped rate and 12 ms-budget crest class (9e75's 176–187 at 50 µs = my 177.5 control), 7.7 cores composed+delete, and the 4-core mint budget is 23.1 µs — e7ef's number, unchanged. **Byte-shrinking the record moves memory, never CPU.**
- **Delete coverage = promotion-skip coverage** (1a46): in-situ 85.8%, belt 38.5% as frozen / 99.4% with RES (ledger effect −0.7%) — ES_SECULAR is not a kick optimization, it is the compact store's no-mint path.

**Predictions:** `predictions.md` — controls reproduced exactly; P3 held (35.5k in the measured 13–27k class); P4 held on shipped bytes (33 gs) and on composed+delete+diet (never busts) but **missed** in one cell: diet at shipped rate gives dwell* = 2,808 gs = 10% of the interval, not the predicted >30%; P5 held (identity exact).

**What would make it wrong:** the working-set match is a class match on one measured hot set (ladder scenes, ba64), not a 10⁹ measurement — a 10⁹-relevant N_hot could carry longer dwell (rebind certificates, 128 bits/rebind class) and lift dwell* columns; the mint cost is priced at the bind/refit share, not measured as a standalone mint+demote on shipmem (unmeasured — the store is not wired); rtf and crest corrections (9e75) apply to the frame ledger, not these totals.

**Cost of adoption:** near zero — no code; it re-ranks in-flight work: (1) wire shipmem with demotion at certificate-clear (~1 game-s class) and price mint+demote standalone; (2) promote ES_SECULAR from "comb cure" to "the compact store's no-mint path" (its coverage IS the promotion rate); (3) demote the record-diet effort to the 10⁶ ladder (its 75–615× is real there; at 10⁹ it only buys dwell headroom).

**Fit with PRINCIPLES:** "Store the generator, not the generated" (6) — the promotion must mint the key + packed state, never derived quadrature; "the best part is no part" (17) — the no-mint path outranks the cheaper mint; "Compute only surprises" (3) — dwell, not bytes, is the memory dial.

## The five lessons (the lens's deliverable; all quotes verbatim, `work/quotes.py`)

1. **"They had wasted all their time memorizing stuff like that, when it could be looked up in fifteen minutes."** — Feynman, *Surely You're Joking*. Mechanism: a stored answer costs memory forever; a derivable answer costs compute once, at use. Change: the promotion mints the key + packed state (56.0–56.8 B, 42e6), never the compiled quadrature (58% of a doll body, proven regenerable bit-identically, 5465); knots become an evictable cache. Cheapest test: the ledger's resident rows — P_diet vs P_ship.
2. **"Chunking relates to the mind's ability to assimilate large amounts of information into a cluster that is bound together by certain patterns or principles particular to a given discipline."** — Waitzkin, *The Art of Learning*. Mechanism: share the pattern, store the per-instance residue. Change: the store's unit is the shared program (one chunk per orbit), member = 17.3–29.6 bits (9d49); kills `Catalogue::insert`'s 2,000-entries-per-orbit (cae7). Cheapest test: chunk count per orbit before/after dedup on a dumped scene.
3. **"The maximum of an average is necessarily less volatile than the average maximum."** — Taleb, *Fooled by Randomness*. Mechanism: a budget set on the mean rate says nothing about the worst spell. Change: a lever counts only if it moves E_spell (9e75's law spell = E·Ĉ/0.72, ratio 1.01–1.04), never the average — a4ed's 10⁹-passing sentence was exactly the maximum-of-an-average artifact. Cheapest test: every ledger row prints crest and mean (this ledger does: 157 cores vs the rtf-1 average 1.75).
4. **"Redundancy is ambiguous because it seems like a waste if nothing unusual happens. Except that something unusual happens—usually."** — Taleb, *Antifragile*. Mechanism: prefer deleting the source of the unusual to provisioning against it. Change: adopt the genesis stagger (free; deletes the crest's phase-lock, f82a) before any idle-time compute-ahead; the doll grid's deterministic schedule stays a free option if a second spell ever prints. Cheapest test: fly ≥3 intervals with the stagger (9e75-checker2's unprinted recurrence case) as the stagger's adoption gate.
5. **"We can be blind to the obvious, and we are also blind to our blindness."** — Kahneman, *Thinking, Fast and Slow*. Mechanism: an instrument concludes only on the population it samples. Change: the frozen gates see no doll-born body (21a7: all gate bodies root-doll, four arms identical digits; 3463's dashboard under-reported ~20×), so the promotion census (memory-h-live dir 3) must be wired with its own visible population before any freeze cites it. Cheapest test: every freeze proposal names the population its instrument sampled.

**The lens's blind spot:** the Readwise library is self-help-heavy; the systems practitioners this problem most resembles (Denning's working sets, Erlang blocking, Skunk Works) are absent from it — lesson 1's demand-paged mechanism is imported and marked so, only its quote is native. Analogies were kept only where they change a decision: 1, 2 and the re-ranking; 3–5 are rules for the record, not designs.
