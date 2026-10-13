# Dossier — 20261013-0037-components-009b

**Claim.** The shipped `bind` chose the integer word from the *compiled* entry, so every word
transition compiled a full trajectory only to throw it away; the word is a function of the fit's
key alone, choosing it before the compile is bit-identical everywhere tested and cuts total bind
time 12.9–17.5% on plane settles (binds are 43–50% of settle wall at 400 members).

**Bottleneck.** `kick-jet` open direction 1 ("cheapen the exact recompile… the word-transition
double-compile"), the board's live question. Component: the bind's word choice. Requirement (law:
the word must hold the new tube's largest radius and periapsis speed in 60 bits). Floor: two
exponents, ~10 exact Scalar ops on the fit's key — nanoseconds. Shipped design: `word_for(&entry)`
needs the compiled `Entry`, so a transition pays fit+compile+readout (~278–310 µs measured,
leaver-class) to learn two integers, then pays it again at the coarser word: the dependency
direction is inverted (PRINCIPLES 18/19: the right representation makes the math trivial; a fix
signals the wrong representation). Idiot index of the *decision*: ~10⁵×; of the kick overall this
run moves 1,400–1,800× → ~1,200–1,550× (b063's floors), still far from done.

**Evidence** (all from shipped code, this shared Linux/x86 box, one binary, both arms; orders of
magnitude only per the lab rules; regenerate with `regen.sh`, ~8 min cold, ~3 min warm):

- Frequency: plane settle, 600 s game — seed 1/48 members: 533 binds, 27 transitions (5.1%);
  seed 3/48: 498, 30 (6.0%); seed 1/400: 4,422, 233 (5.3%).
- Waste, measured in-situ (time of the discarded first pass): 8.4/55.3 ms, 8.8/48.8 ms,
  64.8/446.1 ms of bind time = **15.2%, 18.0%, 14.5%**. Transitions are rare but are the
  expensive binds: 278–310 µs discarded per transition against a ~104 µs mean bind (leavers
  flip to a Passage whose outer radius exceeds the old word).
- Fix: `Rebinding::fit_of` (fit without compile, `space/binding.rs`), `word_of_key`
  (`universe/bind.rs`), `bind_with(fit, …)`; one compile per bind, ever. Same binary, `ES_BASELINE_ARM=1`
  restores the shipped path: bind time 47.0/40.3/388.7 ms → **−15.0%, −17.5%, −12.9%**; the word
  decision costs 0.3% of bind time; transition counts identical (27/30/233).
- Digests bit-identical on all three scenes (664ea84e…, dadbd1bc…, 887cd3bd… — matched across
  arms and against the pristine baseline build). Suites green: `cargo test --release -p
  emergent-space -p emergent-universe`, 0 failed (clock's ignored test stays ignored; 17.9 s).
- Settle wall: 0.86 s → 0.80 s at 400 members (−7%, matches binds' share); 0.11–0.12 s → 0.10–0.11 s
  at 48 (noise-level).

**Predictions** (`predictions.md`, written before the decisive run): P1 ≥10% transitions — **missed**,
measured 5.1–6.0% (above the 5% dead-code threshold I set, barely); P2 held in structure —
transitions are ≈5× a mean bind, waste ≈ the kept pass (the "≈2×" framing held per transition
bind); P3 held for digests, but I under-predicted the cut (share×45% ≈ 2.4%): the cut follows the
*waste share* (14.5–18.2%), not the count share, because transitions concentrate on expensive
binds — measured 12.9–17.5%; P4 held (settle −7% vs bind −13%).

**What would make it wrong.** The one behavioral delta: the baseline could fail inside the first
compile and return the error where the fix proceeds to the coarser word (the failure at the tight
word is an artifact; the fixed path is arguably the law's intent). No such state occurred in three
scenes + all suites. Also: only plane regimes probed (48/400 members, seeds 1/3, 600 s); fleets,
handouts and belt scenes unprobed, and the box is shared, so the −13–17% is an order-of-magnitude
figure. If word transitions were ~0 in some regime, the fix there is a no-op (it cannot be slower:
non-transition binds run the identical code path with the fit hoisted, 0.3% overhead).

**Cost of adoption.** ~60 lines, two files: the `fit_of`/`from_fit` split (from_state becomes a
delegating wrapper, all other callers unchanged), `word_of_key` (word_for keeps its signature),
`bind_timed` rewritten. No API break, no law change, digests bit-identical. Delete on adoption:
the `probe` module, the `ES_BASELINE_ARM` branch and `bind_in` (this run's instrumentation),
`bind_probe.rs` example. Not a 10× lever — a digest-identical slice of the recompile path; the
compile's interior (allocations, key search, i128 panels) and fit-once-per-read remain the big
gaps.

**Fit with PRINCIPLES.** "we just need to have the right representation so that math is trivial"
(#18) — the word trivially belongs to the key; "if you find yourself fixing things that's oftentimes
a signal that it is the wrong representation" (#19) — the double compile was the smell. "The
cheapest compute is compute not done" (#1): a compiled cycle is deleted from every word
transition. Errors never compound (#13): bit-identical outputs, proven.

**The lens.** First-principles, one component: I priced one dependency inversion and built it. The
lens may have missed that the transition share is scene-dependent (fleets, handouts, belts not
probed — captures/handoffs rebind in a different doll's word and could transition far more often;
`handout cost 443 µs, 12× a kick` on the frame-cost page smells like this same waste). The
measurement neighbours (settle wall, stats) were watched; the lens's blind spot on moved cost is
covered by the digest identity.
