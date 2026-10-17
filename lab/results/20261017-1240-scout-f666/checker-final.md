Working...
Check complete. **Grade: silver** — written to `lab/results/20261017-1240-scout-f666/check.md`, with the author's wiki page corrected in place where it overstated.

**What I did:**

1. **Reproduced bit-identically.** Fresh `regen.sh` run (49 s, exit 0): results.json, both held-out μ logs, longwindow-kick.txt and the main table all regenerate byte-for-byte from the committed script. Every dossier number traces to regenerable output. predictions.md predates first execution (12:47:21 vs pycache 12:48:40); the author honestly reported P1/P2/P4 failures.

2. **Ran 12 adversarial arms outside the author's domain** (200P window, eccentric births, the never-exercised capture arm, prograde 0.55/0.6, in-band births). Eleven hold — R0's chatter stays linear (1871 at 200P) with R3 = 0, classification = truth everywhere. **One real hit:** a plain circular (0.62 R_H, retro) birth wanders its apoapsis 0.62–0.87 R_H through the f±m band → **R3 = 89 handoffs/40P (0.32/moon-orbit)** — K3's Zeno-free bound survives, but "0 handoffs on stable bodies" is band-dependent, and on that body R3 loses to R0's 1. The dossier disclosed the mode as unmeasured; I measured it.

3. **Corrected the page:** the claim's "~9.4 per moon-orbit" is per **planet** orbit (per moon-orbit it's ≈1.3 — the script's own rate metric divides by apsides); added the band as a third measured dial class; added the band-wander arm to open direction 2's judged set; fixed the same unit in the refuted entry.

4. **Silver, not gold:** the rule class (per-apse decision on the cycle's radial extent, Λ-continuous) is proven only on a float replay replica — no rebind feedback, no relativistic shears (the shipped probe's 21,403 chatter never reproduced), f/m unfrozen. One named experiment away: wire R3 into 18d2's relativistic build and pass the six-case table + P5 + moon test + the band-wander arm.
