Working...
Check complete. `lab/results/20261011-1729-system-2c68/check.md` written: **Grade: silver**.

**What I did** (clean tree, patch applied, ~20 min):

1. **Reproduction** — `jet_probe` output matches `jet-probe-out.txt` **bit for bit** (all 27 numbers). `cost_split` matches (34.4 vs 35.6 µs kick). `from_state` does **not** reproduce: 11.3–13.8 µs over four runs vs the author's 17.5 — the rebind is ~35% of a kick here, not 49%, so the speedup is ~1.5×, not 1.9× (same order, load-sensitive).

2. **Central finding — the bodies are mislabeled.** The probe passes raw body ids (14, 1, 6) where the predictions name `ships[14]`/`ships[1]`/`ships[6]` (ids 18/5/10). Verified via kinds/dolls: "Orbiter 3" is actually **Hauler 11**, "Hauler 1" is **Home the planet**, "Hauler 6" is **Hauler 3**. The reported prediction miss and the "inversion" (with its coherent-tide diagnosis) are artifacts of that mixup — on the *intended* bodies (my runs: medians 72/314/705 at 10⁻⁶) the author's original predictions actually **held**.

3. **Attack** — intended bodies across seeds 1/2/7 (medians stable per class), 10000-kick stationarity (no leak, no decay), interval floor (minima 6–12: a fixed-cadence trigger would overshoot; the trigger must be state-based), and probe-validity (bound scaling proves the error check fires).

4. **Novelty** — the re-anchored jet is documented prior art (law.md, red-team 20261006-0346); new here is the measured rebind share and the interval on the plane's real bodies and both kick paths. Queue check holds: no directed build owns the rebind.

**Why silver, not lead:** the measurements are real, exactly reproducible, and my corrected runs make the claim stronger than the dossier reports (intervals 28–903 kicks at 10⁻⁶ on six bodies). **Why not gold:** the evidence table as written misstates what was measured, the gain is ~1.5–1.9× not 10×, and the probe's trigger cheats by reading the exact path — the one experiment for gold is implementing the jet with a cheap drift-bound trigger and re-facing B5/B12/B13/B17.

Tree restored (my checker examples and the author's patch removed); nothing else in the run folder touched; no git commit or push.
