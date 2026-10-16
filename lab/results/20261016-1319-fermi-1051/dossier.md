# Dossier — 20261016-1319-fermi-1051 (Fermi lens)

**Claim.** The comb and the belt's stream are the same metronome (2^step_log2 events per P_D per
body), r9's secular bound legalizes deleting it for 100% of the comb's in-situ locals (median τ
157× under τ₀) and the whole quiet belt (57–105× under) while forbidding only the resonant L4/L5
quarter (4.3× over), and every spread-cure arm saturates at the same post-wave memory wall — so
"delete with a spared quarter" buys the same 1.9–2.6× flyable N as the de-phase, without its
+11–20% event bill or its invariant death, and is the only arm that also cuts the 10⁹ hot rail's
own constant.

**Bottleneck.** Board item 1 (bodies in the flyable engine: 10⁶ against 10⁹). The page's comb
decision (de-phase vs translate vs delete) is treated as one question and the cadence law (break
1, "a law change: written up, not done") as another. They are one lever with one legality rule;
the estimate deletes a whole decision branch and reorders the levers by what they actually buy.

**Evidence** (all from `work/legality.py`, pure arithmetic on shipped source constants; commands
below):

*The metronome identity.* `Config::step_log2 = 7` (ctx.rs:44) and `Δs = 2^−k·P_D/f'(c)` (ext.rs)
give 2⁷ kicks + 2⁷ boundaries per period P_D of the doll's shortest secondary. Root doll: Cinder
P = 89.1 d from shipped constants (a = 39.56×10⁶ ru, e = 1/10, μ_star = 1 ru) → 3.32×10⁻⁵
events/body/game-s against the measured stream 3.55–4.62×10⁻⁵ (gold a9d7, 7da3): 1.1–1.4×.
Home doll: P_Moon = 26.3 d → the comb's population (356 bodies) fires ~4.0 ev/game-s against
4c22's measured 4.02. **The comb is the belt's stream at a different doll: one law term.**
Cost of the arm at 10⁹: the stream is 7.1×10⁴ ev/game-s; the comb's 4.02 is 0.006% of it —
**no comb decision can move the 10⁹ CPU ledger** (every cure's total event delta ≤ 10⁻⁴ of the rail).

*r9's bound on the shipped populations* (τ = (a/R_H)³, τ₀ = 3.6×10⁻³ ⟺ 0.153 R_H, r9's own
equivalence "0.17 Hill radii"; R_H(Home) = 1.098×10⁶ ru from a_Home = 1.013×10⁸, m_Home = 2⁻¹⁸):
- in-situ locals (octave-uniform a ∈ [5,200, 166,400) ru, scenario.rs:366–370): **100% inside**
  (top octave's very top at τ = 3.48×10⁻³, just under τ₀; median τ = 2.3×10⁻⁵, 157× under);
- the L4/L5 quarter (a = 273,684 ru, the Moon's): τ = 1.55×10⁻², **4.3× over** — resonant with
  the Moon, exactly the class law.md's own kick rule ("a resonance is detected from the compiled
  frequencies") excludes from averaging;
- the quiet belt: τ = 6.3×10⁻⁵ under the Giant, 3.4×10⁻⁵ under Home — **57–105× under**: secular-legal.
Adversarial (held out, one miss reported): Home at 2⁻¹⁹ → 92% inside (I predicted < 60%; the
bound is more robust to host mass than my hand estimate — prediction miss, result unaffected);
2⁻¹⁷ → 100%.

*The wall ladder* (measured constants: 29.3 µs/event M1-projected (7da3), storm 334 (e070, 917c,
4c22), stream 3.55×10⁻⁵ kicks/B/gs (a9d7), rtf 100, 12 ms letter, plateau 4.85–5.06 kB/B (b30b)):
shipped letter N = 6.4×10⁵ (7da3's checker: ≈ 6×10⁵ — re-derived, agrees); translate (141 events)
2.3×10⁶; hybrid delete (storm ≈ 123 after sparing the quarter) 2.8×10⁶; de-phase (53) 3.0×10⁶ —
**every arm past the memory wall 1.2–1.65×10⁶** (6–8 GB at the plateau). All arms buy the same
1.9–2.6× flyable N; the choice between them is price and legality alone.

**Predictions.** `predictions.md`: P2 (metronome within 2× of the measured stream: 1.1–1.4×),
P3 (all three sub-cases within 10% of the stated values), P4 (all arms tie at memory, none past
3×, comb ≤ 10⁻⁴ of the rail) all held. P1 (the anchor flight) was **not flown: `nladder` does
not link on Linux** (`proc_pid_rusage`, nladder.rs:26, macOS-only) — the comb's anchor stands on
the merged-tree record (ladder.txt: max events/frame 348–452, p50 2–4, N-flat 10³–10⁶; e070's
main-tree isolation). One adversarial sub-prediction (Home at 2⁻¹⁹ → inside-fraction) missed.

**What would make it wrong.** r9's τ₀ was measured on satellite tides (the Hill regime); the
belt extrapolation assumes the same τ governs the planets' tides on heliocentric bodies — B14-class
gates must fly it (the page's own caveat). The hybrid's storm ≈ 123 assumes the storm scales with
the doll's population sharing the tick (4c22's composition supports this: the beat is one
population's boundaries+kicks); if the spared quarter alone re-combs at 334, the hybrid degrades
to the translate's letter. The delete lever is a law change (step 5): unflown legality, same as
the de-phase's.

**Cost of adopting.** Step 5's secular generator for stable non-resonant bodies (already the
law's letter for kicks: law.md "kicks are orbit-averaged on stable orbits away from resonance"),
plus a per-body legality flag (a < 0.153 R_H and non-resonant). Deletes the metronome's events
for the flagged set; the L4/L5 quarter keeps the kicked path. Fit with PRINCIPLES: "no work for
no reason, so no ticks" (#14: the metronome is a tick); "A fix signals the wrong representation"
(#19: the cures that spread a storm we could delete); "The simulation decides" (#22).

**The lens.** Fermi estimates expose assumptions; this one may have under-weighted what only a
flight can show (the hybrid's residual storm shape) and the checker's box differs from the M1
(the µs/event anchor is a projection).

**One flight this tree allows on Linux** (`exodus`, the only Linux-clean frame instrument;
N = 0 plane, so it anchors the engine and the exodus frame, not the comb's magnitude): frame
62 = 11.54 ms / 31 events / lag 1.448, neighbours 2–19 events — ladder.txt's merged-tree
"frame 61, the fleet's opening exodus" (9.6–12.0 ms) reproduced on this box, one frame later
(the recorder merge sits between). The comb's own anchor remains the merged-tree record.

**Predictions.** `predictions.md`: P2 (metronome within 2× of the measured stream: 1.1–1.4×),
P3 (all three sub-cases within 10% of the stated values), P4 (all arms tie at memory, none past
3×, comb ≤ 10⁻⁴ of the rail) all held. P1 (the anchor flight) was **not flown: `nladder` does
not link on Linux** (`proc_pid_rusage`, nladder.rs:26, macOS-only) — the comb's anchor stands on
the merged-tree record (ladder.txt: max events/frame 348–452, p50 2–4, N-flat 10³–10⁶; e070's
main-tree isolation). One adversarial sub-prediction (Home at 2⁻¹⁹ → inside-fraction) missed.

## Commands (each ≤ 60 s)

- `python3 lab/results/20261016-1319-fermi-1051/work/legality.py` — every number above.
- Source of every constant (verify): `grep -n "mass_log2\|const AU\|260_000\|5_200\|35_600_000\|step_log2" crates/universe/src/scenario.rs crates/universe/src/ctx.rs` (literals named in the script).
- `grep -n proc_pid_rusage crates/universe/examples/nladder.rs` — the Linux link refusal.
- `timeout 35 target/release/examples/exodus` (or `cargo run --release -p emergent-universe --example exodus`) — the N=0 anchor flight.
- `regen.sh` regenerates the lot.
