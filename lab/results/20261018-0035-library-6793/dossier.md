# dossier.md — 20261018-0035-library-6793 (library lens)

**Claim.** The 10⁹ memory wall, composed from measured constants only, is decided by two
dials no other row can substitute for — the scar quantum (q16 3.0 GB ↔ q24 5.2 GB ↔ the
scoreboard's 126-bit worst 15.75 GB, which busts 8 GB at zero live bodies) and the live
plateau (b30b's 4.85–5.06 kB/B ↔ ~1.3 kB post-Carlson) — and five verbatim library lessons
split their freeze: the reversible live ceiling now, the irreversible scar quantum late.

**Bottleneck.** Board #1's binder: every comb arm saturates the same wall at 1.2–1.65×10⁶
live bodies (1051); the scoreboard's memory row is "~2× over in the worst case (a driven
belt at 126 bits/body)". The composed table (below) says the worst case is not 2× but
**nonexistent**: 15.75 GB busts the 8 GB machine with nothing else in the box, while q16
scars leave room for 3.85M post-Carlson live bodies. What it deletes: any memory plan that
freezes one global "bits/body" (the ruin boundary is a pair, per population), and any
priority list that ranks the Carlson wiring (cd6e/a765) by its kick row rather than its
memory row.

**Evidence** (all numbers regenerate: `./regen.sh`, ~10 s, no flight — the fermi-lens
precedent; `nladder` does not link on Linux).

Table 1 (`python3 compose_mem.py`; inputs each cited in the script):

| mix (10⁹ bodies) | compact | live@6GB now | live@8GB now | live@6G post-C | live@8G post-C |
|---|---|---|---|---|---|
| ship belt (program, 98bc) | ~16 KB | 1.19M | 1.58M | 4.62M | 6.15M |
| rock, phase-locked 20.7–22.1 b | 2.59–2.76 GB | 0.64M | 1.04M | 2.49M | 4.03M |
| driven q16 (ab9d) | 3.00 GB | 0.59M | 0.99M | 2.31M | 3.85M |
| driven q24 (ab9d) | 4.8–5.2 GB | 0.16M | 0.55M | 0.62M | 2.15M |
| driven worst 126 b (scoreboard) | 15.75 GB | BUST | BUST | BUST | BUST |
| fully mixed 63 b (a91f) | 7.88 GB | BUST | 0.02M | BUST | 0.10M |

Checks (compose_mem.py output, `work/compose_out.txt`): P1 identity — 8 GB/5,060 B =
1.58M, 6 GB = 1.19M, the measured wall 1.20–1.65M: the table reproduces the wall with
zero new constants. P3 — the 126-bit driven belt busts 8 GB at zero live bodies; q16
leaves 3.85M post-Carlson. P4 — neither dial alone rescues the worst mix (Carlson cannot
fit 15.75 GB; q24 + the wall's own live count at the 5 kB plateau = 13.5 GB > 8 GB).
P5 — fences (held-scan pin 0.46 GB at C=1,000, 1fcf; FLOW latch 0.17–0.95 GB, b8e2) are
3% of 6 GB quiet but 16% at the battle-alive latch worst: second-order except in battle,
where q24's slack goes negative. The census pyramid (9d49): individuals 9.5–12.9% of
population, scarred 24%; the promotion jump store→runtime is 53× post-Carlson, 206× at
the shipped plateau (196.6 bits = 24.6 B at rest).

Quotes: 5/5 byte-identical (`python3 verify_quotes.py`; 4,590 highlights; regen re-fetches
fresh — that fresh-export verification is P2's held-out property).

**The five lessons** (each changes one decision):

1. **Naval (Almanack): "The one thing you have to avoid is the risk of ruin."** Mechanism:
   survival is decided by the worst mix, not the average row. Change: the memory
   requirement is frozen as the worst admissible (compact-bits, live-count) **pair**, per
   population — a global "bits/body" cannot see that the ship-belt row fits 1.19M live at
   6 GB while the 126-bit row fits nothing anywhere. Test: any arm whose worst mix exceeds
   the machine is dead regardless of its CPU letter (1051's four comb arms saturating one
   wall is the precedent; this table is its memory twin).
2. **Keynes via Kaufman (Personal MBA): "It is better to be roughly right than precisely
   wrong."** Mechanism: precision nothing reads is cost, and here it is ruin: ab9d's q24
   flyby scars are chaotic for every bounded program (min |Δz| = 43× the quantum — the
   precise scar is precisely wrong), and they cost 5.2 GB where q16 costs 3.0. Change:
   derive the scar quantum from its consumer (the regenerated body's readout bar — e29c's
   q_view pattern), never from the tube's 32-bit angle grid; price the residual as
   kick-layer work (ab03's staleness finding). Test: compose the regenerated readout's
   bar; if q24's extra 1.8–2.2 GB serves no consumer bar q16 misses, q16 wins by
   arithmetic.
3. **Farnam Street (Second-Order Thinking): "A lot of extraordinary things in life are the
   result of things that are first-order negative, second order positive."** Mechanism: a
   lever found on one scoreboard row pays on another. The Carlson wiring is queued as the
   kick's compile wall (84–87% of the rebind, a765); its second-order payoff is the wall:
   it deletes the per-body knot/crossing table and takes the plateau 5,060 → ~1,300 B — a
   3.9× move on the binder of board #1, at every mix in Table 1. Change: rank the wiring
   by its memory row. Test: count the knot-table share of b30b's plateau on a shipped
   dump; that share is the wall bytes the wiring deletes.
4. **Tiago Forte (Building a Second Brain): "A helpful rule of thumb is that each layer of
   highlighting should include no more than 10–20 percent of the previous layer."**
   Mechanism: layered stores live or die by their pyramid ratios, not their layers. The
   measured census (individuals 9.5–12.9%, scarred 24%) already sits at Forte's band
   (scarred 1.2× over its top edge). Change: freeze the store as a pyramid with bounded
   level ratios, enforced by **demotion** (the resting state is the lowest layer; efd4's
   eviction half — 58% of dead entries regenerable at 17 ns/body — is the unbuilt
   mechanism), so the 53–206× store→runtime jump is paid only by bodies whose reads
   justify it. Test: the shipped flights' census ratios (program:scarred:individual:live)
   against the band; a ratio already inside it makes the freeze free.
5. **Farnam Street (Reversible and Irreversible Decisions): "Make reversible decisions as
   soon as possible and make irreversible decisions as late as possible."** Mechanism:
   the two dials freeze on opposite schedules. The live ceiling is reversible (promotion
   restores any mix — freeze it now; it bounds the FLOW fence, the crowd wall and the
   comb letter at once). The scar quantum is irreversible — carries cannot recover
   information below their own resolution (r2's KILL), so a coarse q permanently caps what
   any future consumer can read from a driven belt. Change: split the wall's freeze; never
   bundle the two. Test: regenerate a q24-scarred belt at q16 and diff the readouts — the
   diff is the information the late freeze protects; if no shipped consumer sees it, the
   freeze is safe to defer, not to make.

**Predictions** (`predictions.md`): P1 held (identity), P3 held, P4 held, P5 half-held
(3% quiet, 16% at the battle-alive latch worst — over the 15% bar exactly where q24's
slack goes negative), P2 held on the run's own fetch and re-verified fresh by regen.

**What would make it wrong.** Any input constant moving: the plateau (b30b), the 1.3 kB
post-Carlson figure (HANDOFF's interlock, not a flown measurement — the table's post-C
columns inherit that), the scar-store GB (ab9d, q-parameterised), the census (9d49, at
4 GiB not 6–8). The 126-bit worst is the scoreboard's own reading of 98bc's driven belt;
if the driven belt's mature phase-locked program (6baf-2b8e's 20.7–22.1 bits) applies
there too, the worst row softens to q16/q24-class and the ruin claim narrows to the
event-scarred store. Cost of adopting: none for lessons 1/3/5 (framing and priority);
lesson 2 needs the scar-consumer derivation (one rung); lesson 4 needs the demotion half
(efd4's own next step). Fit with PRINCIPLES: "The memory floor is information-theoretic
(entropy given shared structure), not bytes × count" — the table is the bytes-side
composition of exactly that standing decision; "a failed experiment kills that
configuration, never the method".

**The lens.** A library run composes; it does not fly. The two softest numbers here are
borrowed, not measured by me: the ~1.3 kB post-Carlson plateau (an interlock, not a
flight) and the 126-bit worst (a scoreboard reading). Both are named above; a dynamics or
spacex run should measure the first before the Carlson wiring is ranked on it. What the
lens may have missed: whether Julien's "the quanta decide" already intends lesson 2's
derivation (then this run only prices it).
