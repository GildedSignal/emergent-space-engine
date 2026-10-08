Grade: silver

**Abstract.** Claim: the plane's commit path carries ~60 bits of live information per kick and writes 660 B (88× the floor). Reproduced bit-identically: all three CSVs (plus my independently built stride-2), digests, event totals, `analyze.py` output. Controls hold: kick-bench digests identical pristine vs patched; `--h-live` deterministic across three executions. Held-out seed 3 and a 50-member fleet give 63.9–66.6 bits/kick, 659–663 B/kick. law.md's "+62 bits per kick" is confirmed — with my sign correction (the shape term omits sign) the measured floor is 62.1 bits, exact. Silver because the 88×→1.12× varint-scar store is measured ex ante, not built, and the brief's `--bench`/page wiring and tests are undelivered. Adopt the number and the method (description length, not frequency entropy) now.

## Reasons

**Reproduction (clean tree, `git apply work/patch.diff`).** Built patched, ran all three dossier commands: seed1/rtf1e4 and seed7/rtf1e4 CSVs are md5-identical to the stored ones; the rtf1e5 stride-2 file, rebuilt through my own gzip+awk pipeline, is also identical; `digest`, `events_total` and every `by_kind` count match. `analyze.py` (with its `analysis.json` write redirected out of the run folder) reproduces `analysis-output.txt` byte for byte. The stored seed1 JSON (02:06) postdates its CSV (01:59) — a re-run; harmless, since my independent execution matches both.

**Controls.** Kick-bench on patched vs pristine builds: `digest` and `replay_digest` identical (only timing percentiles and timestamps differ — shared-machine noise). So the recorder is digest-neutral as claimed. `--h-live` is deterministic across three executions on two checkouts.

**Predictions.** `predictions.md` (01:58:47) precedes every run artifact (01:59:05+). P2, P4, P5 held; P1, P3, P6 refuted, each with the right mechanism: P3's refutation is in the code (`frame_to`: prune every 64 frames at 2× light distance + margin, universe.rs); P6's refutation is legitimate — law.md's allocator model does say "+62 bits per kick and −60 per reabsorption" (line 13; my first grep missed it only because of display truncation).

**Adversarial (my own).**
1. Held-out seed 3: floor 63.9 bits (65.8 with sign), kick share 0.511 — inside P5's ±25%, confirming pace/seed independence extends beyond the tuned seeds. 50-member fleet: 64.7 (66.6). 
2. `--members` is clamped to [4,400] in pristine main (mod.rs:34), so the scene cannot scale past 400 through the CLI; my "1200" run was a silent 400 duplicate. The "one system, 400 members" limit is a harness cap — worth stating when projecting to 10⁹.
3. The author's claim that frequency entropy saturates: verified (plug-in H of the dv pairs = 16.5 vs log₂n = 16.6 — it measures nothing). The method result stands.
4. The floor is coding-dependent: delta-coding each body's log against its previous dv gives mean bit-length 21.2 vs 27.0 raw (~10 bits saved per pair), and consecutive bit-length buckets carry 0.37 bits of conditional structure. "Exact description length" as computed is an upper bound under value-coding, not a floor; the true floor is ~50–62 bits depending on coding. No conclusion changes (88× becomes ~106×; one kick per body still ≈ the whole 8 GB at a billion).
5. Sign correction: the shape term omits sign (entropy 1.93 bits) → 62.1 bits/kick. law.md's +62 is exact, not "honest to 3%" — strengthens P6's refutation.
6. Varint: I measure 8.78 B/kick (zigzag, all kicks, seed1) vs the dossier's 8.36 — 5% off, unexplained, immaterial to the 1.12–1.17× floor claim.

**Novelty.** First measurement of the plane's commit-path H_live; HANDOFF line 70 had it "not measured yet". H0173 measured bits per lattice collision (different law and layer); components-98bc measured the birth program's static 0.126 bits/body. Neither subsumes this.

**Goal fit.** Directly the board's "fitting 10⁹ in 8 GB … decided by distinctions created per game-second", and it fixes the *definition* before the dashboard instrument is wired (a saturated frequency-entropy dial would hold no information — principle 28). P6/P24 ("the memory floor is information") served: the floor is exact description length.

**Why silver, not gold.** The brief (b-h-live.md) asked for the measure in `--bench` and the page, with tests, gates reported both ways; that gold criterion is not met — the author shipped `--h-live` and an off-line definition, defensible (the definition had to exist first, and frequency entropy fails the brief's own "define precisely"), but the dashboard work is undone. No 10× moved yet: the 88×→~1.1× varint-scar store is designed and its encoding measured against the real stream, not built. Everything reproduced is the measurement, not the gain.

**The one experiment to gold:** implement the append-only varint-scar store (bindings, plans and history re-derived on read) behind the existing resolver, and measure live bytes/body against the floor (7,277 → ~floor-scale) with digests unchanged — or, minimally, wire description-length H_live into `--bench` and the page with tests, per the brief.

**What the author missed.**
- The sign bits (floor 60.1 → 62.1): the formula's own "(sign, bit-length) shape" description is not what the code computes.
- The floor's coding dependence (delta-coding saves ~10 bits): "exact" overstates; the coding must be named.
- The patch silently removes `--unpaced` (dead `paced`, stale help text) — an undisclosed regression the integrator must restore on adoption.
- `analyze.py` line "kept forever (no prune on the flight path)" contradicts the dossier's correct P3 refutation two paragraphs later in the same artifact.
- The dossier's "98.7% of pairs distinct" is seed 7; the headline seed-1 run gives 97.0%.
- The member axis is capped at 400 by the CLI clamp — a billion-body projection rests on one system size, disclosed only as "one system, 400 members".
