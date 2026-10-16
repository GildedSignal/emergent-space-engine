Grade: silver

**Abstract.** Assembly, not measurement: the 10⁹ CPU ledger as one product; reproduced
exactly. With the measured 8× split (7f97) and 61% delete (1a46+RES), today's
104–178-core stream falls to 5.1 (M1) – 8.65 (x86) cores; fitting 4 cores requires a
≤ 23 µs kick — 1.3–2.2× under today's, 472× above the 42–56 ns floor, which fits at
0.17 cores at shipped cadence (binding only at rtf ≳ 2300). Encounters (62–571 cores)
and memory floors stay the 10⁹ blockers. New and checked: the metronome identity
(rate×interval = 0.999 — a9d7's rate and 3294's interval are one constant) and the
double-count against HANDOFF's interlock identity. Gain: the kick row (10³·³) demoted to
a 10⁶ lever; zero code to adopt. Overlaps 4093's "~20 µs at 4 cores".

*Reproduction.* `./regen.sh` exit 0; my re-run's output is identical to the runner's
(warm belt_first < 1 s; the dossier's "14.5 s" is the cold cargo build). Every constant
traced to its page and verified: a9d7 rate 3.55–3.64×10⁻⁵, 3294 interval 28,141.5 s, 7f97
8× split, 1a46 delete 274/712 and 434/712 (nladder.md: the "−70–85%" elsewhere on the
pages is the total-event cut, a different quantity — the ledger's 61% is the conservative,
correct one for the belt stream), 5030 secular marked extrapolated, b063 floor 42–56 ns,
1051 29.3 µs, 4093 50–52 µs / 0.72 clamp / 69-s crest / 120–190 cores, 1738 cube, 277d
62–571 and 14–24×, f0a2 0.03–0.6, 0820 61.6–62.1 and 125.5–126.1 bits, fc48 126.4, b30b
4.85–5.06 kB/B, 2b8e ~21 bits, b2fd ~40 bits, nladder wall 1.2–1.65×10⁶. P2's code inputs
verified: `TICK_SECONDS = 4.925_490_947e-6`, Cinder periapsis 35,600,000 with e = 0.1 →
a = 35.6e6/0.9. Independent recomputation of the whole ledger agrees; the memory wall
identity (6–8 GB ÷ plateau = 1.19–1.65×10⁶) is arithmetically exact.

*Predictions.* predictions.md (21:44:12) precedes the decisive artifacts (ledger.py
21:46:42, regen.sh 21:47:09). P1 belt HELD (14,072), locals clause FAILED and honestly
reported (661 vs ≤ 300; the diagnosis is consistent: 28,141.5 / (2×661) = 21.3× doll-clock
ratio). P2 HELD (0.4678). P3–P6 held — but they are predicted products of cited
constants, so they test transcription, not nature; the author never claims otherwise.

*Attack.* (1) rtf 1000, outside the tested pace range: required kick 110–120 ns, still
~2× above the 56-ns floor; at the floor alone 1.6–1.8 cores. The demotion is robust —
the floor becomes binding only at rtf ≈ 2300. (2) Rate spread 3.33e-5 (b30b end-to-end)
to 3.64e-5 (a9d7): 166–182 cores, no verdict change. (3) M1 composition: 8× + 61% with
today's 29.3 µs kick = 5.07 cores > 4 — the claim "closes on measured levers alone"
overstated: the final 1.3–2.2× kick cut is a requirement; no measured kick-cost lever is
composed (B_LEAVER/b583 is defined in the script but never used in a config). Page
corrected in place. (4) Memory: the fits-class is broader than "only the phase-locked
class" — the 0.126-bit ship belt and 2.4-bit self-stirred classes (belt.md) also fit,
0.02–0.3 GB, up to 200× under budget. Page corrected. (5) The dossier's rate×interval =
1.0004 is not regenerable (the script prints 0.999); both ≈ 1. Page corrected.

*Novelty.* The load-bearing closure number overlaps 4093's current best, published 2 h
before this run started: "closed by de-phase/deletion … or by kick cost ≤ ~20 µs at 4
cores; the 50-ns kick floor is the deeper cut" (kick-cadence.md, 4093). The memory-wall
identity is already on nladder.md:181; the encounter non-closure is 277d's verbatim
ledger. Genuinely new: the product form with the inversion (at the floor shipped cadence
= 0.17 cores, so the floor is off the 10⁹ path — 4093 still called it "the deeper cut"),
the explicit double-count against HANDOFF line 66's interlock identity, and the metronome
identity (a9d7's rate ≡ 1/3294's interval). All are one-line consequences of published
constants; nothing new was measured (belt_first prints canonical game-s values, so it
verifies 4093's recording, not new physics — the author says as much in the lens section).

*Goal fit.* Aims the board's framing question (bodies 28→10⁹) and re-ranks it with zero
code. PRINCIPLES #1: "the cheapest compute is compute not done" — do not buy a 10³·³ kick
programme where 2–5× closes; #18: "the right question, then the representation". Real
integrator value, adoptable within one step — which is why silver, not lead.

**The one experiment for gold.** Compose a measured kick-cost cut with the measured
cadence levers on shipped code: wire the 8× split (constants-only, per the page) plus
b583's leaver halving (and the staggered genesis for the crest) into the shipped ladder
and fly 10⁵–10⁶ at rtf 100–1800, showing the delivered stream lands under the 4-core /
0.72-clamp ceiling with no freeze — a demonstrated closure product instead of a 23 µs
requirement.

**What the author missed.** The M1 row under the levers (5.07 cores — closure also fails
on M1 at today's kick, not just x86); HANDOFF's kick row is 75–160 µs (b063), so the
honest lever statement is 3.3–6.9×, not "×44" (which divides a levered requirement by an
unlevered today); the battle/driven-belt regime is unpriced — the claim's domain is the
quiet belt (a4ed's 10⁹-battle non-closure stands outside it), and the headline should say
so; the two letter errors found in (3)–(5) above.
