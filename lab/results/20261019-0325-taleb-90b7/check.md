Grade: gold

Abstract: The formation burst law is priced on shipped `Chronon`+`RelativisticV1`: a generic two-fleet crossing is one 3× 64-chronon episode (width ≈2.8·extent) and then flat forever; recurrence is a standing train only under exact transverse-velocity equality with aligned columns (survives arbitrary timing spread); exactly aligned, single chronons carry n/2 contacts (top-1% share 21%). Reproduced digest-identically (5 arms rerun; regen clean). Checker extended the domain: n=25600 (4× the grid's largest) confirms both regimes; 25 crossings at amplitude 1.002; σy=1 velocity quantum kills the train — the guard trigger is exactly binary. Adoption: zero code, one trigger condition; deletes the feared generic formation tail.

## Reasons

**Reproduction.** `work/patch.diff` applies clean to the shipped tree; `fleetburst` builds; five arms rerun digest-identical to `work/` (aligned n=1600, σ=q/256 n=1600 s1, aligned n=400 s2 = s1 → the aligned arm's claimed seed-freeness is real, σx-column n=6400, thermal n=1600). The runner's `regen.sh` (exit 0, REGEN_OK) rebuilt the whole 38-flight grid; every dossier number I cross-checked matches `work/table.txt` (maxc/n, maxW/meanlate, F64_late, concentration 21.4, excess/n, thermal row, late rate ≈1.20× thermal, ops 2.085M/1.592M = 1.31× — mean burst-window vs mean quiet, reproduced exactly; worst burst window is 2.254M = 1.42× quiet median).

**Predictions.** `predictions.md` predates the dossier and names its own kill criteria. P1's kill branch fired (isotropic σ dissolves the train) and the author reported it prominently, then diagnosed it (the σx/σy axis decomposition — corroborated by `analyze.py`'s pre-split header compatibility). P4/P5/P6/P7 held; P2/P3 partially failed and are disclosed as such in the dossier. No misreporting found — unlike the 1-October precedent that was held to silver, nothing here was reported as held when it failed. Per H0183, the failed expectation killed the configuration (generic "sustained ruin"), not the method, and the refined law is the deliverable.

**Adversarial (7 arms, 2 outside the author's domain; flights and digests below).**
- *Next octave (n=25600, 4× the grid's largest, H=16384):* aligned still trains with the same constants — maxc/n 0.499, concentration 21.5, period 2496 ch = 3.65·extent (fits the 3.6-3.9·extent law), F64_late 28300 (continues 437→1815→7035, mean-driven), amplitude 1.002. σ=q/256 there reads one-shot 3.43× with a genuinely flat late tail (windows 0.93-1.08× mean; no second burst at the 4× horizon). F64_late 41 in that tail is the counting identity at mean64≈24k (m_late 4.1%), not structure.
- *Horizon (n=1600 aligned, H=16384, 25 crossings — 4× the grid's):* 25 peaks, period 640, amplitude last/first 1.0019 — "constant amplitude" holds as far as flown.
- *Threshold ladder (σy ∈ {2048, 1024, 512, 256, 64, 16, 1}, n=1600, no jitter):* every arm reads the full one-shot signature (verdict, exc/n ≈ 11.5, late ≈ 21.3). σy=1 differs from aligned by digest and kills the train; `Rng::range` is inclusive so σy=1 puts real ±1-quantum velocities on ~2/3 of bodies. So the dossier's "σy ≥ q/256" is a tested sufficient condition, not the boundary: the true kill condition is **exact transverse-velocity equality — one velocity quantum breaks it**. This sharpens the proposed guard into a binary trigger and strengthens the claim's direction (the train is even more fragile than claimed). Mechanism (inference, not measured): geometric decorrelation cannot explain it (σy=16 gives Δy ≈ 0.015q per crossing ≪ the 2q contact range); off-centre contacts must deflect velocities (the tilted oblique reflection the wiki already records) so any asymmetry is amplified — consistent with the author's swap-symmetry reading.

**Novelty.** This is chaos-shadowing open direction 2 verbatim ("the formation burst law — now the only unpriced half of checker2's note; worth one run at the fleet scene with the F64_late instrument"), and no HISTORY entry prices it. It also retro-explains checker2's fleet Fano₁ 96-128 as the aligned comb's first crossing. Not a repetition.

**The page.** Faithful to the evidence; corrected in place where it overstated: comb teeth are every **8** ch at every n (not 4; heights ramp 405→794 within each ~224-ch burst, so "654-794" covered only the upper teeth); the n=6400 aligned period is 1280 (1344 is the σx arm — now "1280-1344"); the threshold is now stated as exact equality (σy=1 kills); "galaxy's drifts are exact multiples of q/4" misread the shipped code (`rng.range(-q/4, q/4)` draws any integer in range — the representability conclusion stands, since velocities are integers). Not three agreeing gold runs — the topic stays open.

**Goal fit.** Board item 4 feeding item 2: it deletes a feared allocator tail (no batch-shaping machinery for formation crossings — "the best part is no part"), names the one configuration that needs a guard, and hands the wiring a dimensionless trigger — "regimes are chosen by dimensionless numbers" (PRINCIPLES 4), "Compute only surprises" (3): the crossing is the surprise, the rest is flat.

## What the author missed

- The kill threshold is exact equality (σy = 1 quantum), not q/256 — the claim's number was the coarsest tested point; the boundary is the bottom of the integer ladder.
- Teeth every 8 ch (not 4); tooth-height ramp 405→794; the 1280-vs-1344 period slip; the galaxy-drift misread; "the burst window" ops figure is the burst-window *mean* (worst window 1.42×).
- The convexity of the response stream vs the walk is asserted from one arm at one n; the mixed fleet+thermal scene (the game case), the wall-reflection train's price, and free-space geometry remain unflown (the author flags all three).

## Checker evidence (deterministic; rerun with the same commands)

Flights (binary `/home/glmlab/lab-target-2/release/examples/fleetburst`, patch applied, all `--out /tmp/chk90b7/…`):
- `--scene head --n 1600 --aligned --horizon 16384` → train, 25 peaks, period 640, amp 1.0019, maxc/n 0.496, conc 20.7.
- `--scene head --n 25600 --aligned --horizon 16384` → train, period 2496, amp 1.0023, maxc/n 0.499, conc 21.5, F64_late 28300; digest d1ada6554b62c4ac744a442eb59adf8cf3eb8791 prefix d1ada6554b62…
- `--scene head --n 25600 --sigma 4096 --horizon 16384 --seed 1` → one-shot 3.43×, late windows 0.93-1.08× mean.
- σy ladder `--sx 0 --sy {2048,1024,512,256,64,16,1} --nojitter --n 1600 --horizon 4096 --seed 1` → all one-shot (σy=1: verdict one-shot, exc/n 11.4, digest differs from aligned).
Digest-identical reruns: head_n1600 aligned 8933160b…, head_n1600 σ4096 s1 26765e75…, head_n400 aligned s2 fc9aa892… (= s1), ax_n6400 6d89d4bd…, thermal n1600 4dab1dac….
