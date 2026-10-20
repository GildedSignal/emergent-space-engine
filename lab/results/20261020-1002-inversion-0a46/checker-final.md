Working...
Check complete. `check.md` written, page corrected, tree restored.

**Grade: silver** (`lab/results/20261020-1002-inversion-0a46/check.md`)

**Reproduced** — every dossier digit regenerates; my own A1 re-flight (38 s) matches the author's per-2k-bin arrivals **exactly** (0.400/0.717/0.415/0.702/0.373/0.737/0.393/0.695 ev/body), worst frames 712.7/44/345.5/11.9 vs 718/42/339/12, net µs/event 46.8/17.6/48.8/11.1 vs 47/17/49/12. Onset frames f2117/f2142 identical across every seed, rung and cadence flown. Predictions pre-registered (mtimes verified); P2's honest refutation is the alternation finding. Note: `regen.sh`'s `[ -s ]` guard reuses the author's CSVs — only my re-flight independently regenerates the arms.

**Adversarial arms, all outside the author's grid** — rtf 800 to 76k gs: eras 1–4 arrivals identical to rtf 400, era 5 = 1.013/body with a 492 ms freeze (alternation holds at a fifth era and a new cadence). 5e4 to 120k gs: **eight eras** at the same 14k period, −26% by era 8 (faster decay than the dossier's extrapolation); the max_ms alternation fades below 1e5 but the µs/event cost alternation holds through all eight (41/12/41/8/44/9/43/11) — the cost split, not the mega-frame, is the robust object. Seed 3: same onset frames, 715 ms era-1 freeze.

**Why not gold** — the 3× lever's mechanism is unprobed, and its stated cause (the player's gulp path) is contradicted by the author's own coast CSV: coast pays the same 47/12 µs/era alternation with no gulp (era walls 5.5/1.7/5.2/1.6 s — the dossier's "~11 flat" doesn't regenerate). Also corrected on the page: "λ to the digit" (it's 1.2–1.3× the canonical 4e-5 ledger λ), "0/600 frames behind every arm" (coast era 1 defers 160 frames to 5.0 s), and the anchor's true spread (re-flew at 947.9 vs the claimed 817.6 family). Gold experiment named: cc9d's per-item decomposition across a freeze and a clean era, plus a clock-phase-spread stagger arm.
