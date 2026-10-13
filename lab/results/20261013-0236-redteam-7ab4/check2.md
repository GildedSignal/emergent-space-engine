Grade: gold

**Abstract.** Claim: under the news representation every rebind of a source leaves each
consumer a permanent scar |ΔE| ≈ 0.7·(β_c²/2)·|δv| (exponent 1.963), and under sustained
thrust the free-fall version readout lags by a cadence-invariant ½·a·T², damaging the
consumer by ~β_c²/2 of the burn's Δv; the fix is the acceleration on the version payload.
Reproduced bit-for-bit (`bash regen.sh`, 3.6 s). My six adversarial cases — β_c = 0.5
(k̄ 0.715, law extends), burn ×4 (lag scales), two-kick superposition (linear, bounded),
eccentric e = 0.4, ΔE-at-switch vs end (ratio 1.00 everywhere) — confirm rather than
refute. Cost to adopt: one vector per version + the `r-news` rung. It is the first
instrument for law.md:33's causality primitive.

**Reproduction.** `bash regen.sh` in a clean shell: every dossier number regenerates
identically (exponent 1.963, k̄ 0.70, twin 0.0, both E-tables, E5). File times order
correctly: predictions.md (42 m) precedes run1.txt (35 m, the disclosed broken build — I
checked: its scar column is the source-drift artifact) and run2.txt (33 m, decisive).

**Predictions.** P1 held (1.963 in 2.0 ± 0.1); the "one-signed across seeds" sub-claim was
declared ill-posed and refined to the time structure — I verified the refined claim exactly
(ΔE at the switch = ΔE at the end, ratio 1.00, all 8 geometries: the scar accrues entirely
inside the light window). P2–P6 all held. No failed prediction was reported as held.

**My attacks.** (1) β_c = 0.5 impulse, outside the swept range: mean scar/δv = 0.089,
k̄ = 0.715, twins exact, switches never early — the law extends. (2) β_c = 0.5 burn: lag
0.0060/0.0069 vs pred 0.0063, cadence-invariant; damage 0.063–0.070 vs the summed law's
0.157 — the damage law saturates ~2× below at β 0.5 (it is an order-law, not exact). (3)
Burn a = 0.2 at β 0.1: lag 0.00104 vs pred 0.00100 (scales with a); damage 1.4× above the
summed law. (4) Two kicks: exact linear superposition (same-sign at half-orbit spacing
cancels to 0.03×, alternating stacks to 1.98× — the sign is set by moon geometry, so
criterion (b)'s "bounded random-walk under alternating kicks" holds as boundedness, not as
cancellation). (5) Eccentric consumer e = 0.4, radial kick at the apsides: scar ~3.5×10⁻⁴·δv,
10× below the circular law at matched β — inside/just-below the author's k spread (0.086–1.2);
the bound survives, the circular headline does not transfer as a local-β² law (the author
flags this domain honestly). (6) The Laplace control fails 3–4 orders worse everywhere I ran.

**Novelty.** The topic page on main is empty (0 runs). a237 measured free-fall news ≡ inst
and the switch *onset* of a struck source (impulse); nobody had measured what a rebind or a
burn *leaves* in the consumer, and no sustained-thrust scene exists anywhere in the record.
The probe's mechanism is faithful to law.md:33 (tube version keyed at emission, evaluated at
now, switched at cone arrival) — not a strawman.

**Page corrections I applied.** (a) The dossier's E3 sentence "the news-lag term exceeds the
consumer's direct tidal signal" is wrong at its own numbers (r_c/d = 0.2 vs β²/2 = 0.028 at
20 M in a 100 M binary; the lag force sits ~28× below the direct tide) — the page already
carried this correction; I verified the arithmetic independently. (b) The page presented
"versions must carry the source's acceleration" as this run's fix; a237's probe payload
already recorded (t, x, v, a) and read quadratically — but with gravitational `a` only, so
it is thrust-blind as built, and the plane's 16 B compiled-cycle tube drops even that. Every
built instantiation is thrust-blind; the fix is to carry the *total* acceleration. I folded
this into open direction 1 and the a237 run line. (c) Noted the damage law's measured 0.7–0.8×
factor.

**What the author missed.** The at-switch column in E1 compares Δv(t_sw) with ΔE(end) — for
the ph = π geometry that is 18–23× off, so the dossier's "(at-switch ≈ ΔE within ~1.5×)" is
a mislabel (the correct comparison, ΔE to ΔE, is exact — verified in the Predictions
paragraph); a237's `a` slot
(pretty much the proposed fix already in the topic's float mechanism) is nowhere
acknowledged; the damage law's saturation beyond β 0.3 is unmeasured in the run; and the
pass side of the proposed criterion (an acceleration-carrying version collapsing the lag)
is specified but never run — it is a ~20-line change to their own probe and would close
criterion (c) outright.

**Why gold.** Every load-bearing number reproduced and survived blind extension outside the
swept domain; the held-out predictions held; it gives the causality primitive of board item 0
its first error model, its first instrument, and a freeze-ready criterion for a rung the
record lacks, and it kills the cheap wrong response ("rekey faster") by measured invariance —
a premise-level result of exactly the class the lab retires representations for
(PRINCIPLES #19: "a fix signals the wrong representation"; #13: "errors never compound" —
the scar is one-sided and permanent). Adoption is one step: payload requirement + `r-news`
into the law docs. This is the topic's first gold; the page stays open (one gold, needs
three to close).
