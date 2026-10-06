# Check — 20261006-0346-redteam-df81

Grade: gold

**Abstract.** The kick update "multiply-add from the cycle's stored derivatives" (representation.md §3) has unbounded error: measured C·drift², crossing the 1e-6 floor after 730 correlated 1e-6 kicks (formula √(floor/C)/ε = 729). No re-anchor rule, cost term or rung exists — verified in the repo, and law.md line 35 makes the jet the adopted strong-field mechanism, so the finding is live, not a strawman. Checker's own run at the design's Peters sizes (ν = 0.25): the Δt jet fails on kicks 1, 1, 4 at a = 20/50/100M — inspirals need Peters' a(t) as a generator (a deletion). The view gather survives even at emitter β = 0.99 (checker's extension: max 9 Newton iterations, zero escapes). Adopt in one step: re-anchor rule + ~0.05 crossings/kick term in §3/§6 and law.md, Peters as generator, the proposed rung criterion frozen. Both scripts reproduce bit-identically (~20 s each).

## Reproduction

- `python3 f1_jet.py` → identical to `f1_out.txt` (diff empty, 19.4 s). `python3 f2_view_newton.py` → identical to `f2_out.txt` (23.0 s).
- `work/patch.diff` empty; the tree is clean outside the run folder. `predictions.md` (03:57) precedes both outputs (04:01, 04:02); the VOIDED first control is disclosed in the dossier and printed in the output.
- The attacked text is verbatim in the repo: representation.md §3 line 67 ("a kick updates the cycle by a multiply-add"), §2 line 60 ("Shortcuts reproduce the law exactly"), §6 line 114 (≈50 ns/kick, no re-anchor term). No re-anchor rule anywhere in either doc. `lab/rungs/` holds r1–r4, r7–r10: **no r5, no r6** — the "no catcher" claim holds. B5 judges the unperturbed cycle only (law.md), B9 crossings only.
- Peters kick sizes check analytically: (128π/5)·ν·(M/a)^{5/2} gives 1.12e-2, 1.14e-3, 2.0e-4 at a = 20/50/100M, ν = 0.25 — the dossier's 1.1e-2/1.1e-3/2.0e-4. Floor (1e-6, law.md "about 10⁻⁶ at m = 16") and B5's 10⁴-cycle horizon both verified in law.md. HANDOFF's 29 µs/kick and the ~99% recompile rate verified.

## Adversarial cases (mine)

1. **The Peters rows at their exact sizes, mode E** (`run_case(p, 0.5, ε, "E")`): n*(Δt) = **1** at a = 20M (ε = 1.1e-2), **1** at 50M (1.1e-3), **4** at 100M (2.0e-4); end Δt errors 1.0/0.19/0.91. Stronger than the dossier claimed — every reading of the inspiral row fails within a few orbits.
2. **Weak-field rescue?** C(Δφ; dL) drops 17× from p = 20M to 100M (1.88 → 0.11), but C_E(Δt) is scale-free: 1.76 at 20M, 1.85 at 100M — Kepler's T ∝ |1−E|^{−3/2} (15/8 = 1.875). The inspiral channel is not rescued by distance; at p = 100M systematic L-kicks of 1e-6 still cross at n* = 2973 < 10⁴.
3. **View at relativistic emitter speed** (author capped β_e at 0.6 in a 0.9c game): β_e = 0.99, β_o = 0.99, min g′ = 0.01 — median 3, p99 5, max 9 iterations, zero window escapes, zero non-convergences; closest-approach passes (impact parameters 0.05R, 0.5R) trivial (2–3 iterations). The survival claim is robust beyond the author's own envelope.

## Novelty

No HISTORY entry measures the jet's validity domain. The 5 October memo finding was hit *rates* (and its artifact is the taste log's lesson); H0207's 0.44% re-anchor is the Fermi frame, not the cycle memo; law.md's jet clause (5 October, from the Opus memo) states no bound. law.md is DRAFT pending "GLM has red-teamed this text" — this run is that red-team, and its finding must be resolved before freeze.

## Predictions

Pre-registered before both runs (file times; the P1 VOID fired and was honored — the pre-registered control working as designed). P2, P6, P7, P8 held; P3's functional form held with the author's n* arithmetic wrong and honestly reported; P4 failed and was reported as failed. The failed guesses are about where the jet degrades worst, not about the falsification itself, which held everywhere I probed, including the design's own example. This is honest reporting, unlike the 1 October red-team's "reported as held".

## Reasons for gold

- Reproduced bit-identically; the attack is faithful to the text (accumulated multiply-adds ≡ first-order Taylor from the anchor), and the author preemptively argued the strongest alternative reading (quantized-key anchoring) — which law.md line 35 itself complicates by rejecting per-kick re-keying, leaving the offset to grow. Every reading still needs the missing rule; the Peters row fails under all of them (my case 1).
- It shows a premise of the live design is wrong as written ("shortcuts add speed, never error" for the jet), names a component to delete (Peters-as-kick-source → Peters-as-generator, principle 1), and adds the missing cost term to the board's #1 focus (kicks).
- Adoptable in one step: doc edits to §3/§6 and law.md's jet clause plus one rung criterion (well-formed, with the frozen cycle as negative control). No crate changes.
- Adversarially strengthened, not weakened, by every case I ran.

## What the author missed

- **Mode 'E' drifts the wrong way, undisclosed:** `En += ε·|1−E0|` moves E *toward* 1 (outspiral to the parabolic limit), while the comment says "deepen binding: inspiral-like" (inspiral decreases E). Conclusion unaffected — C_E is symmetric at 1.76–1.85 and my outward-direction runs still fail at kicks 1–4, and the n* crossings occur at δ ≈ 7.5e-4, far from the endpoint — but the label is wrong and the "end error 1.000" rows partly ride the unbound limit.
- "Δφ is safe (C_E small)" under energy kicks is overstated: n*(Δφ) = 290 at ε = 1e-4 (in the table, glossed in the text).
- The phase-locked resonant sequence is classified unsafe by argument only; no measured run.
- "β up to 0.99" in the claim is the *observer's* β; emitters were capped at 0.6 (survives anyway, case 3).
- "Briefed to Astra on 9 October" is future-tense (Astra returns 9 Oct per HANDOFF); motion-law-v2 inheritance is [INFERENCE], though grounded in law.md's jet clause.
