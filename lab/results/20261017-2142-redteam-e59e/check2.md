Grade: gold

**Abstract.** Claim: docs/representation.md §2's observable set omits opacity — no capture
rule, no occluder test — so as specified and as shipped the player sees stars through black
holes (25.0% of the sky at r_o = 6 M, 46.6% at 3.2 M) and through planets (16.7% at two
radii). Reproduced bit-identically (`falsifier.py`, 0.2 s); every citation verified in
place: §2 L53–59, `view.rs` L15 straight light, `kerr.rs` L717, occlusion in no rung, r6's
presence oracle (`rows_found ≥ 0.999`) forbids the fix, Julien's conversation names it six
times and G6 kept it. Gain: a load-bearing premise shown wrong — the spec 45 view runs
inherited. Cost: one interval test per occluder per row plus one asin per BH doll, both
closed-form; adopt in one step.
**Reasons.**

1. **Reproduction.** `falsifier.py` output identical to `evidence.json`; `regen.sh` exit 0
   in under a second; `work/patch.diff` empty (no tree edits). mtime order: predictions.md
   21:51:30 → final script 21:52:50 → dossier 21:53:49 → saved evidence 21:55:38; the
   disclosed mid-run P5 sign fix is consistent with it. All seven predictions held, and the
   held-out structure is real: the numeric bisection is an independent control, the near-rim
   predictions were theory-derived before integration.

2. **The physics, three independent ways.** Closed form (Synge at the four radii: 2.949°,
   14.269°, 45.000°, 83.917° — the author's values exactly; 45° at 6 M is the textbook
   result); my own RK4 classifier at his radii gives 24.86%/46.53% blocked vs his
   25.0%/46.62% (720-direction sampling); my periapsis-symmetric deflection instrument
   (different formulation, dphi 1e-4) gives 2.0806/4.2298/6.5108 rad at 1.1/1.01/1.001·b_c
   vs his 2.0804/4.2304/6.5104, and the strong-deflection law −ln(b/b_c−1)+ln[216(7−4√3)]−π
   reads 6.5075 and 8.8101 at 1.001/1.0001. Monte-Carlo segment-vs-disk (no asin identity)
   gives 0.1666 vs 1/6 at d = 2 R. Every number stands.

3. **Adversarial cases, mine, outside the author's domain.** (a) r_o < 3 M, never tested by
   him: at 2.5 M the Synge reading is 38.0% but the true blocked fraction is 62.1% (my
   integration; escape = outward directions with b ≤ b_c, so the closed form's complement);
   at 2.9 M, 51.8% vs 48.1% — the gap deepens inside the photon sphere, nothing he reported
   is wrong. (b) b = 1.0001·b_c: 8.8106 rad vs law 8.8101 — the log divergence extends.
   (c) d/R = 1.01 (grazing): 45.7% of the sky blocked — every landing approach.

4. **The "no gate" half, verified independently.** `grep occlu|eclipse|opaque` over
   docs/representation.md, docs/law.md, lab/rungs/: NONE (ray-side capture is gated in r1
   `photon-capture`, b/(3√3) ∈ {0.9, 0.97, 1.03, 1.1} — the falsifier's P1 cases exactly).
   r6 read from its published branch (claude/lab-20261017-1018-redteam-13c6): truth "every
   live emitter must have a `Seen` row each frame", `rows behaviour rows_found >= 0.999`,
   `amnesiac` negative — its presence bar demands precisely the rows true occlusion must
   remove, so the omission is not merely ungated, it is forbidden by the frozen oracle.
   Conversation lines all verbatim (L984, L4273, L4283 "A shadow from a circular body can
   often be treated analytically", L4864, L4872, L5032, L6450, L7375); G6 of the
   approved-build-plan carries occlusion — the blind-spot note is accurate.

5. **Novelty.** view.md's 45 runs cover multiplicity (6eae), delay (5977), deflection keys
   (8be2), photon ring (a616/8f00), cost and the row set — none measured opacity; its
   "unmeasured physics" list does not name it. HISTORY's occlusion is the pre-pivot
   inertial law (H0013/H0014, explicitly "no gravity"), with no recorded decision dropping
   it from the pivot's spec. New on this record.

6. **Page.** Faithful to the evidence (I checked each new line against evidence.json and the
   tree; the Contradictions entry honestly keeps that the doc never asserted completeness —
   the gap is against Julien's conversation). I corrected one line in place: the first
   check's moving-observer note had the aberration direction inverted ("closing" 27.7%;
   27.7% is receding — approaching at β 0.5 shrinks the 30° half-arc to 17.6° — and its
   54.9% at β 0.9 does not reproduce; I measure 45.1%), and added the interim-freeze note
   (absence-only parity freezes now; rim presence needs lensing).

7. **Goal fit.** PRINCIPLES 30: "what really matters is navigation, knowledge and dynamics
   those need to be perfect" — this gather is the knowledge half; 34: "the oracles are
   guards, not shepherds" — the proposed eclipse-parity criterion is a guard with a
   well-formed negative (the shipped straight gather must fabricate at the measured rates).
   Same shape as the adopted gold 5977 (missing light delay), with a larger player-visible
   effect and an oracle that forbids the fix.

**Disclosure.** One broad grep of mine swept the run folder and surfaced fragments of
check.md; I discarded them as evidence and re-derived everything cited above independently
(r6 from its branch, the 62% at 2.5 M, kerr.rs) — the grade rests on my own instruments.

**What the author missed.** The r_o < 3 M domain boundary (the closed form becomes its
complement there; the §2 amendment must carry the validity domain — now measured). Observer
motion: the blocked interval aberrates (17.6° approaching β 0.5, 49.8° receding on a 2 R
planet), so the interval test must run in the observer's frame at player β; the static
pricing understates the gate's case coverage. Rim-emitter presence in the parity rung needs
the deflection readout the shipped view lacks — freeze the absence half first. Minor:
overlapping occluders (a planet transiting the shadow arc) need an interval union, still
O(occluders) per row.
