Working...
Check complete. `lab/results/20261010-1706-redteam-e07f/check.md` written: **Grade: silver**.

**What I did**

- **Reproduced** both scripts bit-identically (3.35 s / 8.81 s, matching the dossier's 3.5/8.9 s); `patch.diff` empty.
- **Verified the premise against the frozen text**: r1's spec itself decides stability per band (line 10: "a rotation when 1−6u_k > 0", u_k at the geometric centre), the sampler never seeds the strip (p ≥ 6.5+2e), the ISCO probes sit at r = 7/5.5 — the blindness argument is exact. Un-frozen, r1's equation is precisely the author's oracle.
- **Pre-registration holds**: predictions.md mtime precedes both scripts and outputs; its hand-derived band edges ([5.9067, 6.1669)) were left uncorrected against the measured values — genuine. 6/8 predictions held; 2 misses honestly reported.
- **Six adversarial probes of my own, all confirming**: strip arithmetic from scratch (centre 6.0367, 1−6u_k = +0.0061); exact plunge step-converged with clean hyperbolic eps-scaling; the shelf is a real attractor (r_eq = 6.054 in-band) sticky to ε ≤ 1e-2; the m=8 mirror pumps apoapsis +4.6%; photon b_crit shifts only −0.015% (the dossier's unmeasured guess, measured true); r1's ±3% light cases safe.
- **Novelty**: no HISTORY entry, doc, or commit records the strip.

**Why silver, not gold**: the premise it kills is already retired — law.md (`space-darwin16-v1`, 30 September) replaced the in-band map with the (E,L)-rooted Darwin cycle, so the phantom shelf is not established for the shipped law, and the dossier never cites law.md. The r1 clean re-run it aims at is absent from `lab/queue.txt` and HANDOFF, and B19 already freezes an ISCO outcome-class clause. One experiment to gold: run the falsifier on the shipped Darwin-compiled representation. Minor errors noted (±10% vs 1%, attack-4 derivative values, loose mirror prose).
