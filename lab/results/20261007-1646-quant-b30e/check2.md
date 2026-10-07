Grade: gold

**Abstract (for the integrator).** First measurement of H_live on the real engine (restricted problem, live `Binding` invariants): a kicked belt convoy scars every member within half an orbit, reabsorption never fires (512 orbits), and the live distinguishing state plateaus at ~130 bits/member ≈ 16 B at law widths — 11× under the 176 B flat binding; μ/256 buys exactly −8 bits; Form P's strict-majority `infer` dies on the first kicked window. So 10⁹ fully-live belt bodies ≈ 16 GB: over 8 GB before programs. Adopt the corrected resonance letter (see below): growth at 2:1 is a transient; the layer plateaus ~134–140 bits. No engine change; the numbers size b-belt-wire/B18b and the shipmem deletion decision.

**Reproduction (fresh target dir, `cargo build --release` 44.7 s; probe is self-contained in the run folder; `work/patch.diff` empty, tree clean).**
- belt15w 64 8, belt21 64 8, belt15 512 4, hill 32 4: **bit-identical** to the stored CSVs (every kicks counter and bits column).
- belt15 32 8 (whose stored CSV is empty): reproduces the quoted n=32 numbers exactly (orbit 8: 128.5 bits/member, med 41, p99 57; 119,474 kicks).
- Arithmetic checks: 3,824,004 kicks ÷ (16 ships × 512 orbits) = 467/ship/orbit ✓; flat = 1,408 bits = 176 B ✓; 176/16.3 = 10.8× ✓; belt15w−belt15 = −8.0 bits on med (33→41) and p99 (49→57) ✓.
- Engine side verified by source read: `scenario::restricted`, `Stats{kicks,handoffs,lost,refused}`, `Binding`/`Tube` Q32 angle and Q48 k columns are the real crates' own state — the probe measures live bindings, not a reimplementation. shipmem's `infer` is strict Boyer–Moore majority per column (program.rs:60-82); applying `Program::build` to deviation rows is equivalent up to affine composition, so the Form P death test is fair.

**Predictions.** predictions.md (16:58:19) precedes every decisive CSV (17:07–17:11); the two empty CSVs (16:58:23/31) are a killed first launch whose numbers I regenerated bit-exact. 6/7 held; #5 (hill handoffs) failed and is disclosed — its substance (monotone departures, no returns) I confirmed to 32 orbits (lost 3, refused 6, clean 0, no handoffs).

**Adversarial cases (mine).**
1. belt15 n=8, 64 orbits (tiny n): plateau holds, 105–121 bits/member, same column widths (med 41, p99 57), 466.7 kicks/ship/orbit, clean 0 throughout. The orbit-0 falsifier is n-sensitive though: 1.6 bits/member > 1 at n=8 (one birth-rounded member weighs 1/8).
2. **belt21 32 64 (double the author's span): the resonance growth turns over** — 137.2 bits at orbit 32 → **134.2 at orbit 64**. "+0.3 bits/member/orbit" and analysis's "unbounded-ish" are a 32-orbit transient, not a regime; the corrected statement is a higher plateau (~134–140 vs belt15's 121–130). Level, not growth, sizes the store, so no conclusion flips.
3. hill 32 32: departures continue monotone; scarlayer stable 135–142 despite the non-affine birth (author's caveat verified).

**Novelty.** docs/HISTORY.md has the static end only (H0192-era "a perfect convoy costs 488 B per 10⁶ ships"; 5 Oct gold components-98bc, born belt 0.126 bits/body). No entry measures live scar growth under real kicks; HANDOFF line 70 names H_live "not measured yet; they, not the body count, decide whether 10⁹ fit in 8 GB". This run is that measurement, and it kills a shipped premise: program.rs documents reabsorption ("a ship whose state returns to its program is reabsorbed and costs nothing again") — measured: it never fires, and `infer`'s strict majority dies on the first kicked window. Goal fit: board "fitting 10⁹ in 8 GB"; P24 "the memory floor is information-theoretic"; P6 "influences below one quantum accumulate" (measured: to full-width scars regardless of μ).

**What the author missed.**
- The resonance turnover (case 2): the claim sentence and author-final still say "grows +0.3 bits/member/orbit at 2:1"; adopt the plateau reading.
- The decisive unmeasured variable for the 8 GB verdict is the **live fraction of a real belt** (occupancy of hot radii × kick rate), not the per-member width: 16 B/member is the all-hot ceiling (every ship at 1.5·sep, 466 kicks/ship/orbit — 58× the belt cadence rungs); a real belt's quiet majority may stay born-programs. The author concedes the hot regime in wrong-making (b) but the claim letter reads general.
- Letter slips: analysis's N-scaling line says "128.5 (n=16)" — 128.5 is n=32; n=16 at orbit 8 is 121.0 (so +12%, not +5%; still <15%); the dossier's repro list "belt15 64 64 (88 s)" is belt15w (the belt15 n64 64 CSV is empty); belt15w's rate is 269.7, not 262, kicks/ship/orbit.
- The scar account is analytic (EF bound, byte-aligned rows): byte alignment inflates ~10 bits/member vs the shipped block codec, and the probe's 3 columns [p,k,ω] are a subset of shipped Form P's 5 [t_p,kind,E,L,ω] — both errors point the same way, so ~16 B is a floor, as claimed.
- Seal/repack CPU cost against frame budgets unmeasured (flagged by the author); dead no-op loop at main.rs:112-122.

All runs single-threaded, well under 2 GB. Gold despite the letters above: every stored number regenerates bit-exact, the predictions were pre-registered with a falsifier and the one failure disclosed on a config excluded from the claims, and the measurement is the board's named unknown, adoptable in one step — with the resonance clause corrected as stated here.
