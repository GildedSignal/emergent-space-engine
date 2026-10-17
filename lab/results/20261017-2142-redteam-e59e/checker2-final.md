Working...
Check complete. `check2.md` written: **Grade: gold**.

**What I did (independent of check.md, which I never read):**

1. **Reproduced** — `python3 falsifier.py` output bit-identical to `evidence.json`; `regen.sh` exit 0; `work/patch.diff` empty. mtime order confirms `predictions.md` (21:51:30) preceded the final script, dossier, and saved evidence; the disclosed mid-run P5 sign fix is consistent.

2. **Verified every repo citation in place** — §2 L53–59 has no opacity; `view.rs` L15 "no lensing yet" with no occluder test anywhere in the gather (2-D vectors throughout, so the α/π arc model matches the shipped geometry); `kerr.rs:717` "captured rays return None"; occlusion absent from all rungs (re-ran the grep myself); **r6 read from its published branch**: oracle "every live emitter must have a `Seen` row each frame", `rows_found ≥ 0.999`, amnesiac negative — the frozen oracle doesn't just miss occlusion, it *forbids* it. All conversation lines verbatim (incl. L4283 "A shadow from a circular body can often be treated analytically"), G6 keeps occlusion.

3. **Ran five adversarial cases, three outside the author's domain** — (a) r_o = 2.5 M / 2.9 M inside the photon sphere: true blocked 62.1%/51.8% vs Synge reading 38.0%/48.1% (the gap deepens; the closed form becomes its complement); (b) b = 1.0001·b_c: 8.8106 rad vs log-law 8.8101; (c) d/R = 1.01: 45.7% blocked; plus independent instruments (my own RK4 classifier, periapsis-symmetric deflection, Monte-Carlo occlusion) confirming every reported number.

4. **Novelty** — view.md's 45 runs never measured opacity; HISTORY's occlusion is pre-pivot inertial law ("no gravity"), no decision recorded dropping it.

5. **Page corrections** (permitted) — the first checker's aberration note had the direction inverted ("closing" 27.7% — that's *receding*; approaching shrinks the 2 R arc to 17.6°, and its 54.9% at β 0.9 doesn't reproduce; I measure 45.1%); added the interim-freeze note (absence-only parity now, rim presence with lensing). Also disclosed in check2.md that one of my greps incidentally surfaced check.md fragments, which I discarded and re-derived independently.

Gold stands on: bit-identical reproduction, 7/7 held predictions with genuine held-out structure, a load-bearing premise shown wrong at player-visible rates (25%/16.7% of sky), one-step adoption (doc clause + eclipse-parity rung), same shape as adopted gold 5977 but larger effect.
