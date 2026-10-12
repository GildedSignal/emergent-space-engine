# Predictions — 20261012-1621-q-wiki-kick-jet-9392 (compiler run)

No new experiment: this run compiles `lab/wiki/kick-jet.md` from the 36 clustered
runs. These are the held-out expectations a checker can verify without me, written
before the page is final. Each is falsifiable against `origin/claude/lab-<id>`
branches and `main`.

- **P1 (the adopted state).** `docs/law.md` line 35 on `main` contains "The jet is
  retired (12 October)", cites golds `20261006-1249-redteam-4978`,
  `20261008-1757-second-…-0ccd-b33f`, `20261012-1227-second-…-4808-d617`, says "the
  adopting run of 6 October had one checker", and ends "Inspiral is not a jet: Peters'
  a(t) is its generator". `docs/HANDOFF.md` says "six golds refute it".
- **P2 (which six).** The standing gold refutations of the multiply-add update are
  exactly six runs: 4978, 9a04, a059, b33f, ee08, d617. df81's checker graded gold but
  it had one checker (4978's abstract says so); 6164, 7922, e86c, 96b4, 67f2, 8306 have
  gold check.md grades but stand silver in the integrator's clustering (no confirming
  second check).
- **P3 (design doc lags).** `docs/representation.md` still contains "so a kick updates
  the cycle by a multiply-add" (line 67 on `main`) — a contradiction with law.md:35 the
  page should record, not fix.
- **P4 (topic split of the 36).** 29 runs belong to kick-jet; 6 belong elsewhere:
  be63 → memory-h-live, 3e48 → frame-cost, 4c5b → gravity-news (Peters inspiral
  generator), e3bc + c4ce → memory-h-live (10⁹ capacity), 67f2 → kick-cadence (kick
  deferral). b242 is a missing branch (empty check.md, no local branch).
- **P5 (sampled numbers appear verbatim in their sources).** All of: 4978 "10³–10⁹×"
  / plunge mispredicted; 9a04 "15/8" / "1.2×10⁸"; a059 "s ≲ 0.05–0.1" / "2.6–6.6×";
  b33f "2.75×" (dossier) or "2.79×" (abstract) / "41/64" / "12×"; b18f "1.5×10⁻³" /
  "1.80×" / "0.0160 compiles/kick"; ee08 Kerr spins χ ∈ {0.5, 0.9, 0.998}; d617
  "μ = p − p_crit(e) ≤ 0.3" / "30–40%" / "~4×10⁴"; 1e74 "1.3–1.5×" / "3.0–3.8×" /
  "26 µs"; fa08 "270×" / "7–13×" / "38 kicks"; 6c47 "92.5–95.1%" / "0.55 µs" / "70×".
- **P6 (the one real contradiction).** b33f (gold) and 2c68 (silver) disagree about the
  same mechanism — a frozen-cycle carry — on different observables (behaviour gates vs
  the 10⁻⁶ drift floor); no run measured both on one build. This goes to
  `## Contradictions`, and the deciding experiment (a behave-suite run on 2c68's carry)
  is named but not run (out of the compiler's mandate).

If any of P1–P6 fails on inspection, the page is wrong in that claim and the checker
should downgrade.
