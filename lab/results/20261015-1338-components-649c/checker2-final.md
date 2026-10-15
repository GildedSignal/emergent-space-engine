Working...
Check complete. `check2.md` written: **Grade: silver**.

**What I did**

- **Reproduced**: regen.sh (runner, exit 0) matches the dossier table; my independent anchor arm gives bit-identical deterministic drift statistics (p99 6.102e-7⁻⁸, n=715, near 308). Timing deltas recorded (10⁵ coast 25.85 µs/body regen vs "~23" dossier; one table slip: 10⁴ coast "max 1.6e-9" contradicted by regen's 4.156e-7 and the dossier's own burn8 row).
- **Predictions**: timestamps confirm they precede the decisive runs (13:55 vs 14:05+). P2/P5 held; P6 held live by my re-measurement; P3/P4's "≥100/≥60 frames bit-frozen under burn" were untestable — every burn window is 40 frames — yet the dossier says "held everywhere".
- **Regime artifact confirmed independently** (first checker's correction, verified with the instrument's stderr probes): far rows sit at 1215–1648 light-s; the 10⁴/10⁵ "bit-exact" windows end at game 434/134 s, before first light — where `view.rs` pins every far row at tick 0 by construction.
- **Four adversarial arms** (logs in `out/check2/`): **(A)** burn15 over the 999-frame live staircase — drift 2.47e-7 p99, 1.26× coast, not "identical" (a receding relativistic burn retards emission ticks through $(1-\mathbf{n}\cdot\beta_{obs})$; probe t_e pins at 60.6 s), still observer-side, alive throughout; **(C)** freeze before burn onset — bit-exact ≤4e-16 for 248/249 frames across the onset; **(E)** the decisive missing number — 10⁴ live staircase: drift 2.003e-7 (2% from 10³'s 1.964e-7 — N-independent as predicted), horizon 8.17e3 frames ≥ 5,000, demand 1.23 readouts/frame vs 10,028 shipped; **(B)** 10⁴ at rtf 10⁴ — the engine refuses and the view returns None (instrument prints zeros silently; a limit, not a refutation).
- **Page**: corrected the overstatements — the burn entry's "unchanged to 1.3%" (pre-light windows), checker 1's "live post-first-light" mislabel of freeze-260, and folded in the live-regime 10⁴ measurement and my burn numbers.

**Why silver, not gold**: the physics core stands everywhere I attacked it (price solid; burn-is-observer-side confirmed live; the corrected floor still ~10³× under the shipped walk; view open 3's premise is dead) — but the record leads with pre-light artifacts, "9,714/10,028 never step in 260 frames" is wrong on its own arm's numbers, and "predictions held everywhere" overstates. Per the lab's precedent, silvers fall short on the record, not the physics. The gold step: restate the claim on the live-regime numbers (now measured at 10³ and 10⁴) and add one 10⁵ live arm.

Tree untouched outside `lab/results/`; no commits, no push, `check.md` unread.
