Working...
The count includes the trailing blank separator — content lines 10–24 = exactly 15, within budget. No trim needed. Check complete.

**Grade: silver** — written to `check.md`, with the author's page corrected in place.

**What I did:**
- **Reproduced**: regen clean; verified every dossier number against the outputs. Built an independent harness on the same shipped calls — fork counts match bit-for-bit (0/4,194 at 1 AU incl. ring; 10/5,763 belt δx=10⁶ first kick 767; 54 ring). Verified the probe's `quantize` is verbatim (truncating `/`/`%`), the 61-bit word is real (`to_word` shift = bits−61), and the 11-bit "memo width" is real (ENVELOPE.md:86-89).
- **Adversarial (3 arms + parity)**: (1) the plane's real **e=1/20 Giant** — no verdict changes, belt δx=10³ still 0 forks; (2) **10× horizon** — 1 AU ring still 0, belt δx=10⁶ stationary (288/57,638), **but belt δx=10³ (Ξ=3.2e-7 ≪ 2⁻¹⁶) forks: first at kick 14,030** — "bit-identical forever" is falsified inside the certified zone (`fixed` truncates toward zero → boundary-straddle events walk the carries; only the rate is bounded, never zero); (3) **word scaling** — w8: 0, w14: 304, w16: 1,182 — the mechanism confirmed steeply in the width.
- **Novelty**: HISTORY's "family" hits are old population-IR work; the run's contribution (225d's "one kick erases" is the word's property, not the kick's; the certificate Ξ answers the board's families row) stands.
- **Page corrections**: "forever" → horizon-bounded + the 300-syn refutation; the wrong rate formula (Ξ·2¹⁶/kick) removed; the unregenerable "620 root" number dropped; current best at exactly the 15-line budget.
- **Not gold**: the ÷F win is derived, not flown — the w11-family plane against B12/B13/B17/B18 plus the engine-side key census (the author's own named next step) is the one experiment that makes it gold; and the headline certificate misstates a rate bound as an exact forever. Minor slips noted: res5:2/res7:3 transcription, Home ρ=10⁶ "kick ~0" vs first-11.

Tree left clean (my probe removed; only `lab/results/` untracked, as before); nothing committed or pushed.
