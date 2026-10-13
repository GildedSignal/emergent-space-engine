# Dossier — 20261013-0037-system-174d (lens: the whole system)

## Claim

The flight sweep's burn-input waterfall is not a replan storm and not field work: it is the velocity word's sampling of an exactly-solvable burn — one rebind per 1/64 of |v| — and its events carry 10⁹–10¹⁰ times less gravity than thrust per kick, so the burst can be deleted (not spread) by carrying the burn in the tube's generator, exactly as the retired kick jet carries the cycle.

## Bottleneck

`frame-cost`, open direction 2 (the sweep's L8+ stutter), and through it `kick-jet`. The measured lever: the burst's 325–1,036 player items per input reduce to ~0–10 field events (the tide's own carry cadence) when the burn stops minting rebinds — a ≥50× cut in burst events at L8, more at higher levels, deleting the 1.4–1.7 s presented-time lag the integrator's item 2/3 builds are about to chase. It also retires the wiki's standing guess for the mechanism, which the fix builds would otherwise target.

## Evidence

All from shipped code plus an env-gated probe (`ES_WATERFALL`, counters only — no state path changes; `crates/universe/examples/waterfall.rs` runs it). Reproduce everything with `lab/results/20261013-0037-system-174d/regen.sh` (~3 min total; each command ≤ 20 s of flight time).

**Instrument control, digit for digit.** Demand-mode worst frames: 42 (L8), 579 (L12), 1,036 (L15) player items — exactly the published waterfall counts (20261012-2257-quant-32ab), and the paced run's lag 1.59–1.66 s matches its 1.43–1.66 s. The probe also counts what no one had: every item's kind, and every kick's tide dv against burn dv in the velocity word's quanta.

**What the items are (P1 held).** Every flight: `kick0 ≈ boundary ≈ (items − decisions)/2`; opens 0; decides = script inputs (1 for a hold). There is no refit of scheduled kicks — `decide` clears the plan and plans one kick; the burst is the player's own Kick(0)+Boundary chain.

**Why there are that many (P3 held, 99.6%).** The chain's step is the law's own thrust step `2^⌊log2(β·2⁻⁶/α)⌋` (α = 2^(thrust_log2+level), thrust_log2 = −44), clamped to [128, 2⁵⁰]: 2,283 of 2,293 demand-run thrust kicks match exactly; the 10 misses are the first post-input kick's `aligned()` remainder, MIN_STEP=128 floors, and one transition. Measured at L8 start: step 16,384 = 2^⌊log2(β·2³⁰)⌋ with β = 2.84×10⁻⁵. The coast control's step is 2²² — the tide's own cadence is 256× coarser at L8.

**What each event buys (P2's letter failed, its intent held by 9–10 orders).** The tide is never literally zero in quanta (it is ~10⁶ quanta ≈ 10⁻¹² of |v|), so my prediction "tide_q == 0" failed — but the ratio is the truth: tide/burn per kick, over all 2,293 burst kicks: min 2.6×10⁻¹², median 2.8×10⁻¹¹, max 1.3×10⁻⁹. At L15 in demand mode all 906 thrust kicks are below 2⁻³⁰. The counterfactual: the same flights' tide, accumulated at the coast cadence (median 4.98×10⁸ quanta/kick), mints ~0–2 events against 226–906 burn events.

**The coast control inverts (P4 held).** Coast: 38 items over 4 s, 19 kicks, tide fires 19/19 at ~5×10⁸ quanta — the clock cadence belongs to the tide. Brake within 2× of forward (P5 held: 325 vs 548); the turn segment mints coast-level items only, the burst arrives with the burn keys (P6 held: 376/377 kicks tide/burn < 2⁻³⁰).

## Predictions

`predictions.md` was written before the decisive run. P1, P3, P4, P5, P6 held. P2 failed as written (binary sub-quantum tide) and the run's headline number is its resolution: the tide is 10⁹–10¹⁰ below the burn, not below one quantum. Reported as a miss; the kill criterion ("the kicks carry real gravity") is not triggered — they carry 10⁻⁹ of what they cost.

## What would make it wrong, cost, fit

Wrong if: the rebind's word margin is load-bearing in a way the ramp cannot hold (the thrust step exists so "the velocity leaves its word" never happens — a generator-carried burn must still respect the word at readout), or near-star burns (where the tide grows: 49 late-flight L15 kicks reached tide/burn ≥ 2⁻³⁰) need the fine cadence for the field's sake. The L15 plunge-adjacent kicks are exactly where a tide-carry law must keep its own events. Adoption cost: a law change in the shipped code (the burn rides the tube as a ramp — the representation already has all three pieces: `rec.b.kick`'s ramp for readers, `thrust::owed` exact in rapidity, `rec.carry` for the tide), so it is the integrator's to take, priced by this run: it deletes the burst rather than scheduling it. PRINCIPLES: "you don't advance a ship tick by tick you just map where it wants to go" (14) and "Nothing is evolved that can be derived when looked at" (3) — a held burn is the derivable case par excellence. The stutter fix in flight (HANDOFF item 3, spreading the waterfall) would buy smoothness while paying the same total work; this says the work itself is empty.

## The lens

The whole-system lens unified the stutter with the kick jet and saw one mechanism (continuous influences chopped into word-sized rebinds); what it may have missed is the exception the data names — the 49 strong-tide kicks near the plunge, where the field genuinely wants the cadence, and any doll-edge/handoff cost hiding in the burst's later frames. It also did not measure the read side (a ramp-carrying tube read every frame per viewer) against the kick side; that is the named counterweight from `frame-cost` direction 3, and it stands.
