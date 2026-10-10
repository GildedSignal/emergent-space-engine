Grade: silver

**Abstract.** Claim: the pending co-orbital train certificate (`b-coorbital-cert-152e`, never executed — empty run-log, 429) is sound on first run but covers only strict formations: certified share 100→99→83→55→0% as σ_e rises 0.001→0.25, residue cone-admitted with 0 numeric evals and 2 Cross sections/pair, high-e declined, residue store ~0.7–12.6 TB at 10⁶ for σ_e 0.005–0.05. I reproduced every logged count bit-exact (all 25 lines; ring600, claimed but absent from evidence.log, holds when run: 17 enc, 0 missed). Adversarial: the watch is sound forced at e = 0.7/0.85 (141–270 enc, 0 missed — P4's untested half); a-dispersion steepens the cliff (a ±1% at σ_e 0.02: certified 0.5%, admitted 50% ≈ 36 TB); a second latent ζ bug (spread misses the circular wrap gap) over-fires tight-λ̄ clumps ~100×, flipping no author decision. Gates the 152e merge; nothing to merge itself.

## Reproduction (clean tree at a838a28, `git apply work/patch.diff`, CARGO_TARGET_DIR=/tmp/enc-target)

- `train-verify phalanx|rings|equalp|disp` and `frag`: every counted field identical to evidence.log (watched/cone_filtered/queries/windows/evals/events/missed/false per scene; frag clumps, certified_share, cross_cone_admitted, kinds [3588,0,0] etc.). Only wall-times differ (total ~25 s here). Determinism exact.
- `train-verify ring600` (in the dossier and P1, but **no line in evidence.log**): fires, 17 encounters, 0 missed, 0 false — the claim holds; the omission is a log-completeness defect, not a fabrication.
- Store arithmetic verified: admitted fractions 1.0/4.9/17.5% → 5·10¹¹ pairs × frac × 144 B = 0.72/3.6/12.6 TB. Consistent.
- Build 152e confirmed dead pre-run: branch run-log.txt is 0 bytes; checker-final.md ends in a 429. "First execution" is true.

## Held-out predictions

predictions.md predates the decisive run as far as evidence allows (mtimes share a minute with evidence.log); the decisive behavioral evidence is that P2 **failed against the author's own kill criterion and is reported as failed** (predicted certified_share < 5% at σ_e = 0.02 with the pre-registered "adoption value dies" kill; measured 83.1%; the kill explicitly did not land, with the transitive-closure mechanism verified in code — `clumps()` same-cell auto-merge plus union-find). P1, P3, P4-decline and P5-latent all held. P4's soundness half was untested by the author (hie declines, so the watch never runs at high e); I closed it below, in the certificate's favour.

## Attack (my three adversarial cases)

1. **Forced high-e fire (the admitted blind spot).** Fixed e = 0.7 and 0.85, aligned ϖ (±0.02), λ̄ Gaussian σ 0.01–0.05, a jitter 1e-5 — ζ fires where every author scene declines. Result: sound — e 0.7: 192 encounters, 0 missed, 0 false; e 0.85: 141/0/0; e 0.7 σ 0.05 over 4 orbits: 270/0/0 (truth and pairwise method agree). The windowed watch is sound to at least e = 0.85, well past the build's own test coverage (e ≤ 0.4) and past the e ≈ 0.6 the dossier called unexercised. Caveat found: at e 0.85 the train costs *more* than the pairwise tier (370,870 vs 168,820 evals/enc; watch touches ~all pairs) — ζ is a pair-count gate blind to sweep width, so "fires" ≠ "cheaper" at high e.
2. **a-dispersion (the lens's own story, unprobed by the author — every frag scene holds a at ±1e-5).** At σ_e = 0.02: a ±1e-3 → certified 66.6%, admitted 11.3% of all pairs (≈ 8 TB at 10⁶); a ±3e-3 → 11.0%, 28.6% (≈ 21 TB); a ±1e-2 → 0.5%, 50.2% (≈ 36 TB, the near-full ruin). a ±3e-3 with σ_e 0.001 stays 100% (clumping survives e-tight fleets). So the oasis is narrower than reported and the 0.7–12.6 TB headline is a **lower bound**; the direction strengthens the run's thesis.
3. **A second latent ζ bug the author missed.** `zeta()`'s spread loop takes gaps between adjacent sorted λ̄ but never the circular wrap gap, so a tight cluster away from the branch cut gets spread ≈ TAU (measured: occupied 0.064, max internal gap 0.0038 → spread 6.279) and ζ under-reported ~100× (my e 0.7 scene: code 0.055, honest 5.4 → should decline). Same over-fire class as the author's δ bug (P5, confirmed in code: `with_delta` multiplies by 0.0), no unsoundness (the watch is sound regardless; `train_events` sets its own correct δ). I audited honest-ζ on the author's scene families: **no fire/decline decision flips** (phalanx tight-λ̄ max honest ζ 0.22; uniform-λ̄ scenes and the frag ladder are wrap-immune; hie honestly declines at 1.45). Two one-line fixes when 152e is revived.

## Novelty

- The dispersion sensitivity of co-orbital phase-neighbour certification is not new: efc9 (gold, 7 Oct) and 6f01 (gold, 7 Oct) killed the fixed-rank reading and derived the gate (S = N·(extent + Δn·W)/2π) that became ζ. What is new here: the shipped build's own code runs for the first time (152e died at 429; the kills ran on hand-rolled rank-sort harnesses), the watch is shown sound where the fixed-rank certificate died — the kills do **not** transfer to the λ̄-window design — and the trigger's actual calibration (certified share vs σ_e, residue admission fractions, decline at high e) plus the silent-declined-budget finding are first measurements. 2e81's 72 B/section signature is borrowed with citation.
- Minor dossier defects: ring600 claimed but unlogged; the illustrative "phalanx-1e-3-u21: 31 watched pairs" mislabels sw001-41's 31 (u21's is 55) — substance (watched ≪ 19,900) holds on every scene.

## Goal fit

Board's top scaling risk ("candidate work must track real encounters"): this run prices exactly the regime where it does not. PRINCIPLES: "compute only surprises" (#3) — a declined clump silently handing back a Θ(n²) cone-admitted store is the violation named; "regimes are chosen by dimensionless numbers" (#4) — certified_share vs σ_e (and now vs Δa) is that number's calibration; "the oracles are guards, not shepherds" (#34) — declined must reject loudly. "A failed experiment kills that configuration, never the method" (#9) is respected: nothing is killed, the domain is priced.

## Why silver, not gold

Real, reproduced, and load-bearing for the integrator's decision on 152e — but: (a) the author's own pre-registered kill (P2) failed as stated (the certificate is *more* robust than predicted), so the headline is a corrected measurement, not a confirmed prediction; (b) the 10⁶ store figures extrapolate n = 600 admitted fractions rather than measuring any large fleet; (c) the dispersion premise was already established by two golds on proxies, so the marginal novelty is execution-of-shipped-code and calibration, not the discovery; (d) soundness counts are small (≤ 5 encounters on fired disp scenes; several scenes vacuous) — my adversarials strengthen but were not the author's.

**The one experiment that would make it gold:** run the shipped binary at 10⁵–10⁶ bodies with joint (a, e) dispersion and both ζ one-line fixes, measuring directly: honest fire/decline per clump, certified share, cone-admitted pair count and section bytes actually allocated, and the train-vs-pairwise eval ratio on fired clumps — replacing the extrapolated 0.7–12.6 TB ladder with a measured store and delivering the trigger's true calibration curve (σ_e, Δa, ρ) for the merge.

## What the author missed

1. The wrap-gap bug in ζ's spread (over-fires tight-λ̄ clumps ~100×; found alongside their δ bug — the ζ audit stopped one bug early).
2. a-dispersion: every frag scene pins a to ±1e-5, yet dispersion in a (burns, debris) collapses the certificate faster than e-spread alone; the oasis is narrower than the dossier's ladder.
3. ζ is a pair-count gate only: my e = 0.85 fire shows the train can cost more than the tier it replaces (370k vs 169k evals/enc) while ζ reports 0.077 — "fires" does not certify "cheap".
4. ring600 in P1/dossier but absent from evidence.log; the 31-watched example mislabels its scene.
