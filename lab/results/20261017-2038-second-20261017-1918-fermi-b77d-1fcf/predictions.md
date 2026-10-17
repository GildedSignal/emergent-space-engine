# Predictions — second author on 20261017-1918-fermi-b77d (run 20261017-2038-…-1fcf)

The checker's named gold experiment: crowd arms K = 1.6e3–1e4, pin counted in REAL BYTES at
capture (7bd9's counting GlobalAlloc, not the RSS slope), quiet and loaded, in the PACED
per-frame loop (60 fps wall, one warm view gather per frame — the page's direction-3 rung),
then state the pin law including its superlinear term.

Instrument: `crates/universe/examples/flowcrowd.rs` (print-only, engine untouched; counting
global allocator → live bytes / live allocation count per frame, plus held_scans, catalogue,
RSS, warm gather ms; LIVE_GUARD_B stops a flight before live allocations pass the guard).
Arms: MEMBERS ∈ {1000 (anchor to b77d/7bd9), 1600, 2400, 4000, 10000} × {quiet, 7-spinner
loaded}, coast rtf 100, budget 12 ms, ≤ 50 s wall each, seed 1, threads 1.

## Pre-registered predictions (written before the first flight)

P1 (instrument control). The counting-alloc pin at K = 1,000 (frozen arms) lands within
0.35–0.65 MB/scan — agreeing with b77d's RSS slope (0.40–0.56 MB) within ~30% and 7bd9's
~428 B/candidate at cat ≈ 1,030. If it differs by > 3×, the instrument is broken and the run
is VOID on P1.

P2 (the superlinear term is per-candidate, not candidate-count). At K = 2,400 the per-scan
pin in real bytes is 4–7 MB (checker: 5.0–5.8 by RSS slope). Candidates per scan cannot
exceed bodies (≈ K + births), so ≥ 1.8 kB must be PER CANDIDATE: the superlinearity lives in
the candidates' own bytes (individualized bindings), not in a growing candidate count.
Predicted discriminator: pin/scan ÷ catalogue_live grows ~K^1.5–2 across K = 1e3→1e4
(≈ 0.5 kB → ≥ 15 kB per entry), i.e. pin/scan ~ K^2.5–3. Kill of my own expectation if
per-entry stays < 1 kB at K = 1e4 (then the checker's RSS numbers were retention, not pin).

P3 (K = 1e4 arm). Per-scan pin ≥ 150 MB at cat ≈ 1e4 (extrapolating P2's law), so the 1.3 GB
guard fires after ≤ ~8 held scans (guarded = true in the summary). If K = 1e4 instead pins
< 50 MB/scan, P2's exponent is wrong (report the measured law, whatever it is).

P4 (quiet vs loaded in the paced loop). Crowd arms freeze (held grows monotonically,
held == held_max at every probe after the first freeze) in ≥ 1 of 2 quiet flights at each
K ≥ 1,600 and in all loaded flights; when both arms of one K freeze, their pins agree within
2× (the pin is the capture's own allocation, load-independent). The paced loop's per-frame
gather adds ≤ 5 ms/frame at K ≤ 4e3 (warm cache) and does not drain the backlog (the drain's
room is budget-internal, before the gather).

P5 (fence arithmetic, measured). With P2's law, the shipped SCAN_BACKLOG = 2,048 caps bytes
at 2048 × pin(C): ≥ 0.95 GB already at C ≈ 1,030 (b77d's number, now in bytes), and 8 GB
busts at pin(C) ≥ 3.9 MB → C between 1.6e3 and 2.4e3 — confirming the checker's "~2e3, not
8,500" against the author's sub-kB extrapolation.

Kill criteria: P1 outside its band → VOID (instrument). P2/P3 are measurements with stated
expectations, not gates: a flat per-entry law at 1e4 would REFUTE the checker's
superlinearity reading (and resurrect b77d's 8,500 number) — that is a valid gold-grade
outcome either way, as a clean decision between the two readings.

Postscript (after the flights): see dossier.md.

## Postscript (17 October, after the twelve flights)

P1 HELD: whole-flight pin 477 kB/scan at K = 1,000 on the committed re-flight (first
flight: 379; b77d's band 403–514 by RSS); the transition estimator gives 233 kB (first
flight: 278). All in band.

P2 REFUTED (by my own cleaner estimator): the per-transition pin is FLAT, 226–287 B/entry
across cat 1,028→8,156 — no per-candidate growth at all. The superlinear window slopes that
carried my prediction (and the checker's 2.2–2.5 kB/entry, and 7bd9's m1,600 ~2 MB/scan)
alias birth churn into the pin: at higher K the 50-s window sits ever earlier in the battle
where births are collinear with held growth. The pooled transition fit is 226 B × C (r²
0.974) = size_of::<(usize, Binding, Scalar)>() = 224 B: the pin is the candidates Vec.

P3 REFUTED in magnitude: K = 1e4 pins 1,846 kB/scan (226 B/entry at cat 8,156), not ≥ 150
MB; the guard never fired. The 77 MB "window pin" in that arm is births (cat 7,959→8,437
during the window).

P4 SPLIT: quiet crowd froze at K ≥ 1,600 (ambient 2.5–5.6) and loaded pins match quiet
within 1.8× — held. "Gather ≤ 5 ms at K ≤ 4e3" REFUTED: 6.7/9.7/13.7/27.5 ms at
1e3/1.6e3/2.4e3/4e3, and 74 ms at 1e4 (the paced K=1e4 loop presents 5–10 game-s: the view
is the first wall there; 0 FLOW arrivals).

P5 MEASURED: the 2,048-count fence's price is 0.46 GB per 1,000 candidates on the capture
law (bust at C ≈ 1.7e4), ~5–8e3 on the retained-growth tail — between b77d's 8,500 and the
checker's ~2e3, killing neither cleanly but replacing both with the measured bytes.
