Working...
Check complete: `lab/results/20261003-2306-redteam-4570/check.md` written — **Grade: gold** — and nothing else in the run folder touched.

What the grade rests on:

- **Port faithfulness:** read `view.rs` line-by-line against the Python — window `1−speed−1e-4` (L149), clamp `[0.5,1.5]` (L113), cold guess `unwrap_or(t_now)` (L257), 64 cap, one read per `state_rate` eval. Both scripts reproduce their recorded outputs exactly (`diff` clean).
- **Failure reproduced:** 0.9c content 1.96–2.98 readouts/emitter/frame vs 1.01 static; fast path unreachable ≥0.9999c; correctness intact everywhere (0/270, 0/10⁵).
- **The fix, rebuilt independently:** the dossier's headline combined fix had *no artifact* (`gather_fix.py` only widens the slope clamp; its output still shows transverse ~2.0). I implemented it from the one-line description: 1.01–1.05 readouts on all geometries, moving observer, and — the author's own named doubt — curved motion (offset-centre 0.9c orbit, Kepler e=0.7), plus flyby sign-flip, 10k-tick gaps, combined closing 0.99997; 0/7000 wrong ticks. Gold survives because the work is right; the folder must ship the variant next time.
- **Cross-references all true:** HANDOFF 83%/29 µs, law.md's darwin16 replacement of the Minsky map, H0205 river kill, r5/r6 absent from `lab/rungs/`, B15's 0.9c stream, B11's `5/a² ≤ 5×10⁻⁴` band (ISCO → 13.9% unjudged). Novel against HISTORY — H0211's "about one readout per emitter" is the premise killed.

Conditions flagged for adoption: pin the ε to *narrow* the window (`−((1+n·β)−1e-4)`); the dossier's literal `−(1+n·β)−ε` widens it and admits a 1e-4-level one-tick-early case (never observed, but unsound as written).
