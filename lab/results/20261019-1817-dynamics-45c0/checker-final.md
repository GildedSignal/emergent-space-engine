Working...
Check complete. **`Grade: silver`** written to `lab/results/20261019-1817-dynamics-45c0/check.md`; the author's `wiki/calendar.md` corrected in place.

**What I did:**

1. **Reproduced** — regen exit 0; my own fresh `ship 3000 2 1` from the patched binary is bit-identical to the author's log on every value; `analyze.py` matches all headline numbers.

2. **Confirmed the refutation past the author's range** (three adversarial flights + floors):
   - **Floors** (never computed by the author): iid-uniform C50 at n=2700 = 1.032±0.014 → the stagger arm (1.03–1.07) is floor-level, "stationary at birth" holds; Poisson max/μ at μ=42 = 1.378±0.080.
   - **4.33×N** (belt 11,700, the shipped anchor): C50 trajectory identical g-for-g — mixing time is N-independent, so the ~13–16-fire scale extrapolates toward 10⁹.
   - **Horizon g=40**: C50 → 1.19–1.23, but **load_max stands at 1.54–1.92 flat from g=25–40** vs floor 1.378 — and at 11,700 (floor 1.185 at μ=183) reads 1.83: the post-mix load excess does not shrink with N. Structural, not finite-size.
   - **Instrument question closed**: exact conversion to d520's step denominator gives 2.00/1.63/1.35/1.05 at g=13–16 — the instruments coincide post-saturation, so the d520 checker1 plateau (2.2–3.0) is simply irreproducible on the shipped-draw arm (likely read on the slower-σ classes=1 arms). Birth dump verifies the mechanism: C50(due0) = 57.9× step-denominator (d520's 58.2) and 3.0 own-span = the step law's own shape.

3. **Why silver, not gold** — two headline-vs-log overstresses: (a) the 1% forecast horizon is ~16 fires (log: fc_p50 = 0.0104 at g=16, 0.0145 at g=19), not the dossier's "g ≈ 19" / page's "~20 fires"; (b) "deletes the need for any standing-tail mitigation at 10⁹" is premature — the *genesis* wave is a transient, but the post-mix worst-window tail (+35–50% over Poisson, the allocator's own number) is standing and non-shrinking with N. Gold is one experiment away: price that residual's source and scaling (μ ladder + the unflown σ-28.5% wide-draw arm), then re-freeze the 10⁹ worst-frame line.

4. **Page corrections applied**: news-rate horizon, load-consequence scoping, instrument explanation replaced with the resolution, checker1/checker2 attribution, census count (55 not 39), shear-ratio bounds, plus a dated checker block carrying the new numbers into Open direction 2.
