Grade: gold

**Abstract.** Claim: the adopted co-orbital phase-neighbour certificate (taleb-09b5, feeding `b-coorbital-cert`) is a zero-e-noise statement; with injection e-noise, fleet encounters move to an epicyclic channel that mean-motion conjunction machinery cannot enumerate. Reproduced exactly: rank-4-at-epoch catches 100% of convoy encounters at σ_e=0 but 0.84 at σ_e=0.01 and 0.56 at 0.03 (0.55–0.64 across my seeds); encounters jump 39→535 (14×) at σ_e=0.003; the synodic engine finds 0 encounters where integration finds 125 (dt-converged: 133; 78 mean-longitude events exist in the same window, none an encounter). My n=2048 probe confirms k ∝ n·σ_e (median rank 9 vs the formula's 9.2). Gain: stops a certificate that silently drops ~44% of fleet contacts from freezing. Cost: a design amendment inside `b-coorbital-cert` before the build starts.

## Reproduction (clean tree, no patch needed — `work/patch.diff` is empty)

- `python3 probe2.py`: **identical** — convoy (n=256, σ_a=1e-4, T=8, dt=0.05) enc 39/535/542/536 at σ_e=0/0.003/0.01/0.03, rank max 3/7/11/21, frac≤4 1.00/0.98/0.84/0.56; ring (seed 99, σ_a=1e-3, T=2) enc 91/124 births-excluded with frac≤4 1.00/0.54. The dossier's ring totals "116" and "125" are these plus t=0 births (25 and 1) — the snippet counts births, probe2 excludes them; consistent.
- The dossier's item-2 snippet: **identical** — synodic engine 0, integration 125.
- Mechanism verified: a pair closing to 7.6e-5 (mine; the author's was 1.7e-4) has |Δλ_mean| = 0.0134 inside the ±2√(e_i²+e_j²) = 0.059 band; its relative true longitude swings ±0.032 per orbit; the mean longitudes do not meet for ~745 orbits in the drift direction (the author's "≈500 orbits").
- `python3 probe.py` (the retracted sweep) does **not** regenerate `results.json` bit-for-bit: e.g. ctrl-fresh-convoy events 3754→3581, enc 82→75, d0_max 1472→12, d0_p99 1344→11.3. Root cause, verified: `abs(hash(name)) % 10_000` is salt-randomized per process (two runs give 7230/9305; `PYTHONHASHSEED=0` fixes it). The distributions match; the single number still cited from it (cone pairs ≈ all partners, 4095.0 per body in co-orbital swarms) regenerates exactly and is seed-insensitive at these parameters. Since the author retracted every column of this table and no dossier claim rests on it, this defect costs the record, not the claim.

## Predictions

`predictions.md`'s pre-registered part is credible but not provable from mtimes (the disclosed post-mortem edit touched the file; `run.log` is empty). Its smoke-test numbers (enc 150, d0≤4 0.47, etc.) appear nowhere in `results.json`, and the post-mortem negates the registered table rather than curating it — the signature of a real pre-registration. Substantively: prediction 1 was voided by the broken instrument (disclosed); prediction 2's direction is confirmed on the σ_e axis (1.00→0.98→0.84→0.56, monotone, untuned values); 3–6 untested. The pre-registered kill criteria never fired. The run's decisive evidence is the falsification plus the channel, both of which reproduce exactly — the prediction regime failed, not the physics.

## Attack (my own cases)

1. **dt robustness:** ring σ_e=0.03 counts 94/125/131/133 at dt=0.1/0.05/0.025/0.0125 — dt=0.05 undercounts ~6%, converges upward; the channel is not a sampling artifact, and the dossier's flag "the epicyclic passes are fast" is accurate.
2. **Seed robustness:** frac≤4 at convoy σ_e=0.03 = 0.56/0.55/0.63/0.64 over four seeds. Not seed luck.
3. **Channel purity:** the engine's 78 mean-longitude events in T=2 contain **0** encounters — all ~133 encounters are epicyclic. The measured decomposition is 0 synodic + 133 epicyclic, so the dossier's "~8 synodic" is an unmeasured (conservative) Fermi estimate; the truth is stronger than stated.
4. **Fleet scale (the extrapolation the dossier flagged as estimate-only):** n=2048 convoy, σ_e=0.01 → 32,256 encounters, median rank **9** against the predicted k = 2√2·σ_e·n/2π = **9.2**; but coverage needs several× k (frac≤32 = 0.93, max 83). Per-band-partner encounter rate is constant across n (≈0.11/orbit at n=256 and n=2048), confirming encounters per body per orbit ∝ n·σ_e (0.26 → 1.97). The certificate's k grows with fleet size; O(n·k) is O(n²σ_e) unless it churn-tracks. This measured n-scaling makes the design warning sharper than the dossier states.
5. **Precession:** rigid apsidal precession (0.2 rad/orbit) changes nothing (539 enc, frac≤4 0.56, as rotation invariance demands); a J2-like differential over the convoy's σ_a=1e-4 gives only 0.001 rad/orbit spread — also nothing. My test is weak (spread too small to bind); meaningful differential precession remains untested, as does 3D. Neither plausibly kills the 2D channel in the design's own model class (r8's: candidates = orbit overlap, encounters = close conjunctions).

## Novelty

`docs/HISTORY.md`, the docs and the board record taleb-09b5's "every real encounter lies within partner rank 4 along the orbit" with no e-noise qualification, and the encounters design's timing (r8 v2's continued fractions on mean motions) with no band term; no prior entry mentions epicyclic channels or e-spread in co-orbital swarms. `crates/shipmem/src/pop.rs` (lines 167–184) births convoys with per-member e, l and w jitter, so "fleets have e = 0" is indeed an unowned and false requirement. Novel against the record.

## Goal fit and grade

The board's top scaling risk is "candidate work must track real encounters"; the gold taleb-09b5 was adopted precisely because a tier that silently drops real contacts is unacceptable — and this run shows the adopted certificate has exactly that defect once fleets carry e-noise (44% dropped at σ_e=0.03), while the timing machinery under-enumerates 0-to-125. That is "shows that a premise is wrong," reproduced exactly and adversarially confirmed (seeds, dt, n-scaling), adoptable within one step: size the neighbour set or rebuild cadence by the epicyclic band (σ_e is dimensionless and already carried by the swarm) and add the band term to conjunction timing, inside `b-coorbital-cert` before it freezes. PRINCIPLES 19 ("a fix signals the wrong representation" — mean-motion timing is the wrong water for co-orbital fleets) and 32 (the symmetry — the oscillation band — appears by changing representation). The run also embodies the 5 October lesson: it falsified its own harness before trusting it, kept the falsified instrument as evidence, and retracted every number that rested on it.

## What the author missed

- The `hash()`-salted seeds make `results.json` unregenerable run-to-run even as a retraction artifact; a fixed seed (as probe2 uses) costs nothing.
- The "~8 synodic" component of the 125 is presented beside measured numbers but is an estimate; the measured synodic share is 0.
- The band formula 2√(e_i²+e_j²) is the maximum swing; realised swings are phase-dependent (0.032 vs 0.059 on my pair) and near-alignments need not be exact zero-crossings — the channel is a proximity statement, worth stating precisely in the design note.
- k ∝ n·σ_e is stated as a tail estimate but is in fact a median (verified at n=2048); as a coverage bound it needs a tail factor of several, and the per-body encounter rate itself grows ∝ n·σ_e — at 10⁶ ships the encounters, not the certificate, become the load. The certificate-vs-churn design question (his "rebuild every orbit" branch) is now measurable with probe2 and was left unmeasured.
- Differential precession and inclination: argued, not measured; my precession probe was too weak to bind.
