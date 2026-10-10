Grade: silver

**Abstract.** Claim: kick cadence should be a per-body certificate (t* = √(2q/a_bound)), not a clock. Reproduced exactly (17.6 s vs 17.5 s): gated fires 11.6/orbit against fixed-32's 32 at 3.5× worse e-error (no parity, author-conceded); self-tightens 11.6→16 under 1.5× tide, no retuning; oracle-tight 1.65×; q is a real dial (count ∝ q^-0.5, error ∝ q). Checker additions: the certificate's own cost is unpriced — as shipped the per-event 128-point orbit scan makes the policy ~30× slower than fixed-32; cached once per orbit it is 3.5× with unchanged behaviour. The window-averaged (Simpson) kick — the dossier's proposed fix — is 6–16× worse at equal cadence. At e = 0.3/0.6 the gate beats a parity-interpolated clock ~1.6×. Feed to q-cadence; no code adoption.

**Reproduction.** Clean copy, `python3 work/probe.py`: wall 17.6 s, every number in the dossier table matches `probe-out.json` cell for cell (2.76×, 3.47×, 7.58×/4.62× error growth, oracle med 1.653 / p10 1.077, B4 15.945). `work/patch.diff` is empty (no tree edits). File order: `predictions.md` 13:11:12 < `probe.py` 13:13:27 < `probe-out.json` 13:13:45 — predictions pre-registered. All five quotes verbatim in the cached 4,580-highlight export.

**Predictions.** P1 ✓ (11.6 in 10–15). P2 honest half-fail: fixed-32 parity missed by 3.5× (author concedes); beats-fixed-8 half holds (all four metrics). P3 ✓ (1.65 ∈ [0.5, 2]). P4: B/B2/B3 truth escapes at orbit 10/48/117, VOID as reported; weakened B4 form held. P5 ✓ (negative control 86.3° apsidal).

**My adversarial cases** (`/tmp/check-a2ec/adv.py`, 15 s; host load 1.0, 13.8/15.9 GB free — ratios only, shared machine):
1. *Certificate cost.* The gate recomputes `a_bound` (128 Kepler+tide evals) **per event**: policy wall 0.67 s vs fixed-32's 0.02 s per 200 orbits (~30×) — unmentioned in the dossier, and exactly the per-kick window-setup cost the 6 Oct gold killed. Caching the bound once per orbit: 0.07 s (3.5×), behaviour unchanged (A: de 1.13e-3 vs 1.19e-3, dw 0.94° vs 0.98°; E3/E6 same). The 2.8× kick saving is real only in the cached form.
2. *The deferred composition, run.* Simpson window-averaged tide in the kick is **worse** everywhere at equal cadence: fixed_32_avg dw 5.61° vs 0.235° (24×), de 3.7e-3 vs 3.4e-4; gated_avg dw 15.8° vs 0.98°. The endpoint-evaluated kick has a leapfrog-like favourable error structure that naive averaging destroys; the dossier's stated mechanism ("clock amortises phase sampling") does not survive its own cheapest fix. Only H0190's *orbit*-average (a different object) remains open.
3. *Eccentricity (held-out).* e = 0.3: gated 8.39 kicks, de 2.26e-3, dw 0.118°; fixed_8 (same count) 4.97e-3, 0.640°. e = 0.6: gated 1.04e-3, 0.075° vs fixed_8 2.02e-3, 0.127°. Parity-interpolating the fixed ladder, the gate is ~1.6× cheaper in kicks at e ≥ 0.3 but only at parity at e = 0.05 — the toy's single eccentricity sat at the gate's *worst* case.
4. *q-dial.* q 5e-5→4e-4: count 23.2→8.2 (√ scaling), de 4.7e-4→2.1e-3, dw 0.41°→2.08° (both ∝ q). The certified quantum maps monotonically to behaviour error — the property the clock lacks.

**Novelty.** Cadence-as-the-lever is established (H0212: six runs kill correctors; taste log 6 Oct; q-cadence queued), so the direction is not new. The specific mechanism — a per-body Encke-style rectification interval with measured oracle tightness (1.65×) and a certified error dial — has no prior H entry and is a legitimate rung candidate. Cites components-4643's numbers (92% window setup, 12.6× skin) accurately.

**Goal fit.** Board focus #1 verbatim ("fewer kicks per orbit at the same behaviour"). Fits #3 ("Compute only surprises") and #22 ("the simulation tells us what's next not us"). But the measured gain is 2–2.8× without behaviour parity, no component is deleted (the global constant is replaced, not removed), and the "one to two orders composed with H0190" is unmeasured. Not the 10× gold bar.

**Why silver, not lead:** reproduced, honestly reported (P2/P4 failures disclosed, held-out escapes documented not tuned around), on the top board focus, and my two structural attacks (cost, composition) *amend* rather than refute it: the cached form keeps the economics, and the eccentric/q generalizations confirm the mechanism.

**The one experiment for gold.** Compose the gate with H0190's orbit-averaged kick (secular tide between gates, conjunction phase kept), bound cached per orbit and its cost included; run it on a belt scene at e up to 0.6 against the fixed clock. If it holds B-level behaviour at ≤ ⅓ the kicks/orbit, cadence is certified, the global constant is deleted, and q-cadence has its winning configuration.

**What the author missed.**
- The certificate's own compute: 128 evals/event, ~30× the whole fixed-clock budget as shipped — in a lab whose board is compute cost, and right after a gold that killed per-kick window setup. The per-orbit cache that saves it is one line and was never measured.
- The "one experiment away" was ten lines away, and its natural form fails; the dossier presents the composition as the obvious next step without running it.
- Eccentricity untested: the toy ran only e = 0.05, which my sweep shows is the gate's worst case (parity); the advantage grows exactly where belts live.
- B4's oracle median 1.86 is 32%-censored at the 2.0 cap — the bound's conservatism there is understated (A's 0.4% censoring is fine).
- Truth is non-symplectic RK4 over 200 orbits with no convergence check; the fixed-256 positive control (3.7e-5) mitigates but does not establish it.
- Lens-level: three of five lessons are Taleb, and L2–L5 carry quotes as endorsement, not derivation — the author says so, correctly.
