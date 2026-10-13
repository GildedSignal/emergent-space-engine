# Dossier — 20261013-2252-components-be78 (lens: first principles, one component at a time)

**Claim.** The promotion's fit-again retry — 40–62% of hand-outs compiling their member's tube
twice — is deleted by deriving the integer word from the state's own turning key *before* the
bind (env-gated probe `ES_WORD_FIRST`, bit-identical digests on all seven scenes and the plain
build): one compile where 1.4–1.6 ran, the hand-out 538 → 360 µs calls-weighted (−29…−46% per
scene; the author pass gave −16…−45%), the bind term −38…−52%, no map and no standing bytes — which also deletes
the quant memo's reason to exist (its catchment *is* the retry).

**Bottleneck.** The furthest gap on the board: 28 bodies against 10⁹. The measured wall on the
compact side is the promotion stream (fermi-367f: the leak × 486–585 µs sticky hand-outs), and
quant-7055 showed 52–63% of hand-outs pay a second full compile because the state arrives at a
word its own orbit outgrows. The component taken: **the bind's word choice**. Its requirement
owner is PRINCIPLES #3 — "Compute only surprises. … Nothing is evolved that can be derived when
looked at" — and the word is not a surprise: it is a function of the turning key the compile
itself reads. The shipped code derives two i16 exponents by running the whole compiler and
checking; the floor is the key derivation (`fit_key`, closed-form energy–angular-momentum
algebra, already computed inside every compile). On that decision the idiot index was a full
compile (~230–420 µs) per retrying bind; the fix sits at the floor. PRINCIPLES #19 agrees:
the retry was a fix living in the wrong representation (the word as the compile's *output*
instead of its *input*).

**Evidence** (Linux/x86 shared runner, orders of magnitude only; `bash
lab/results/20261013-2252-components-be78/regen.sh` reproduces the table, ~6 min warm):
| scene (8 game-s, paced) | digest off=on | hand-outs | retries off→on | hand-out µs off→on | bind µs off→on |
|---|---|---|---|---|---|
| m1500 seed 1 (tuning) | = | 232 | 120→0 | 555→392 (−29%) | 427→266 (−38%) |
| m1500 seed 3 | = | 205 | 121→0 | 638→427 (−33%) | 510→295 (−42%) |
| m1500 seed 5 | = | 247 | 98→0 | 506→310 (−39%) | 373→200 (−46%) |
| m1500 seed 7 | = | 190 | 104→0 | 626→337 (−46%) | 494→236 (−52%) |
| m4000 seed 3 | = | 2,041 | 1,063→0 | 510→337 (−34%) | 407→233 (−43%) |
| m8000 seed 3 | = | 6,099 | 3,200→0 | 544→368 (−32%) | 433→260 (−40%) |
| m400 seed 1, rtf 100 | = | 381 | 236→0 | 505→339 (−33%) | 369→203 (−45%) |

Aggregate: 538 → 360 µs per hand-out (calls-weighted, −33%). These are the regen.sh numbers
(the table the shipped tree regenerates); the author's first pass on the same scenes gave the
same equalities with −16…−45% per-scene deltas — the per-scene µs wobble with the shared box's
load, the equalities never do. ~9,400 hand-outs per pass (the counts themselves wobble a few
percent in the overflow scenes, as below); main-thread retries (the hand-out path; wave-thread
kick rebinds are not counted by the main-thread `prof::take`) went to zero at every scene, in
both passes. **The m400/rtf-100 scene sits in the collapse regime** (174–231 overflow frames of
480): there the *run-path* counters (lost 145–151, bodies 402–403, presented tick 91–111 M)
wobble between two shipped runs as much as between arms — the control row `off2` in the regen
table — while the digest at the canonical cut is `540ec08d304060d6…` in every run, as the
budget-independence contract promises. **Plain build** (the shipped feature set, no `prof`):
seed 3 m1500 digests equal off/on and equal to the prof-on digest (`7b33d0b866149e71…`) — the
timers reach no outcome.

The patched tree with the probe *unset* passes the universe suite (70 passed, 0 failed,
2 ignored clock flights, `cargo test --release -p emergent-universe`): the default path is
the shipped one plus one `LazyLock` read per bind.

**Why bit-identity is structural, not luck.** `bind_surface`'s shipped retry re-expresses the
state at `max(word_for(entry), state word)` and binds again. The probe (`word_before` in
`crates/universe/src/bind.rs`) computes the *same* shift from the *same* quantities — for a
turning orbit the apoapsis `periapsis/(k−1)`, for a flyby the compiled-out edge (the very
argument `from_state` passes to `Passage::compile`), for the speed `1/√(periapsis·k)` — read off
the key that `fit_key` returns for the state (published as `space::binding::fit_of_state` +
`word_of_key`, the same arithmetic `word_for` runs on the finished entry). Since `from_state`
compiles from exactly that key, predicted word = `word_for(entry)` by construction for Cycle and
Passage; a Plunge is reachable only when `fit_key` itself refuses (`NoBoundOrbit` originates
inside `fit_key`; `Passage::compile` refuses with `Topology`), and then the prediction is
`None` and the shipped path runs verbatim. Any error on the pre-shifted bind falls back to the
shipped path, so refusal behaviour cannot change. The one hole — a compile that errors at the
state's own word but succeeds at the coarser one — would save a member shipped loses and move
the digest; in 8,908 hand-outs it never fired (every digest equal, `lost` wobble bounded by the
off/off2 control).

**Predictions** (`predictions.md`, written before the decisive runs): P1 digests equal
everywhere — **held**, all seven scenes plus the plain build. P2 retries → 0 with the probe on —
**held**. P3 retry share off = 50–65% — **missed low**: measured 40–62% (seed 5 at 40%); the
band came from fermi's 52–63%, the low tail is real. P4 hand-out −40…−55% — **partly held**:
−16…−45% (weighted −36%); seed 5's shipped bind was already cheap (332 µs). P5 run-path
counters unchanged — **refined, not held as written**: they differ *between shipped runs too* in
the collapse regime (the `off2` control); the canonical digest is the equality instrument and it
never moved. P6 no hand-outs at flying pace — **wrong for this box**: m400/rtf-100 collapses
here (198 overflow frames) and hands out 381 members; the prediction was calibrated on quant-7055's
faster box. P7 plain-build digests equal — **held**.

**What would make it wrong.** A state whose key compiles at the coarse word but refuses at its
own (the hole above): it would change a `lost` list and the digest — falsified by any future
scene where the digest pair splits. Cost of adopting: ~40 lines — two small `pub fn`s in
`crates/space/src/binding.rs` and the env-gated path in `bind_surface` (or the same choice
inlined unconditionally inside `from_state`, which makes the first bind the only bind for every
caller — kick and hand-out alike); no map, no standing bytes; the quant memo
(`(OrbitKey, edge)` cache) becomes dead code and should go with it. Fit with PRINCIPLES: #1
"Delete before optimizing", #3 "Nothing is evolved that can be derived when looked at", #16/#19
(the word belongs to the representation, an input, not a repair). For the 10⁹ consequence,
fermi-367f's promotion-stream arithmetic improves by the same factor the hand-out does
(~1.6× fewer compile-µs per promotion), and the finding generalizes: every state handed to a
binder should arrive at the word its key implies, so the promotion never pays to discover what
the key already knows.

**The lens.** One component, its floor and its idiot index, as asked. What the lens may have
missed: the neighbours. (a) The kick path shares `bind_surface`, and its retries ride wave
threads my main-thread timer cannot see — the deletion should help kicks equally, but that is
inference, not measurement here. (b) `replan` (100–160 µs of the hand-out) is now the larger
half of the promotion and was not touched. (c) The sticky promotion itself (8,257 B, no demote
path) is untouched and remains the term the 10⁹ arithmetic actually breaks on; this run makes
each promotion cheaper, not ephemeral.
