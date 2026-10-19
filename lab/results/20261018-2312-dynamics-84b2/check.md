Grade: silver

**Abstract.** Claim: the dense order's "breathing mode" is the genesis shock's acoustic
ringdown (T ∝ side, decaying, never returning); its Fano N-growth is counts ∝ n under
bounded relative modulation, so no dephasing or batch-shaping machinery is needed for
thermal dense scenes. Reproduced bit-identically (patch at base 8d9e7f88, three arms
rerun, diff clean; every column regenerated). Adversarial: the bound tightens at higher β
(m 1.59% at 2¹⁷, 0.47% at 2¹⁸) and the gapped lattice shows no ringdown — but at
n = 12800 whole-run m reads 3.43% (vs the ≤ 2.4% letter) with the ringdown not yet
extinct at 2× horizon, so the m-bound is a domain statement and the instrument needs the
late-window form. Cost to adopt: zero code; one measurement rule; corrected 834e
phrasing.

**Reasons.**
1. **Reproduction: exact.** Applied `work/patch.diff` at the recorded base, rebuilt, and
   reran `regen.sh`'s arms plus three of my own: `lad_n400_s1`, `lad_n1600_s1`,
   `lad_n6400_s2` are byte-identical to the runner's regen data — the harness is
   deterministic, and the genesis mirror of `worlds::gas` is faithful to the shipped
   source (same `Rng(seed^n^0x6A5)`, same call order; verified against
   `crates/lattice/src/worlds.rs`). Identity, block decay (117→2.7 at 6400), T ∝ side
   (341/409/682/≥1024 at sides 43/85/120/170), spec_late empty everywhere, bandcorr ≈ 0,
   maxdisp 24.8-52.7 lc: all reproduced. Checker2's 33.4 at 6400 reads 38.18 here (seed
   1); fresh seed 9 reads 43.20, m 2.49% — same law. P5-mass strengthening reproduces on
   the author's leftover seed-2 arm (F64 63.74, m 2.86%).
2. **Held-out check.** `predictions.md` (27 min before dossier) pre-registers P0-P5 with
   kill lines. P0/P2/P3(acoustic)/4 held; P1 (the decisive half) and P5-mass were refuted
   and honestly reported — by the lab's letter and the 1-October precedent (one failed
   held-out caps the grade), that alone blocks gold. The failures are informative: they
   killed both pre-registered mechanisms and left the identity reading standing.
3. **Adversarial (outside the author's domain).** (a) vmax 2¹⁷ (β ≤ 0.18): m 1.59%,
   blocks 85.5→1.2 — the dossier's own kill line (m > 5% at higher β) is nowhere near
   crossed; (b) vmax 2¹⁸: m 0.47%, F64 0.90 — no mode at all; (c) gapped genesis
   (fill 0.3, cell 3): F64 3.80, no ringdown blocks — the mode is the touching lattice's,
   confirming the acoustic/contact-network reading and the page's own prediction;
   (d) n = 12800 (the octave the dossier extrapolates): the identity holds (164.0 =
   139526·0.0343²) and the allocator ratios stay flat (b0 max/p50 1.109, per-chronon
   p99/p50 1.131, inside P2's bands) — but whole-run m = 3.43% breaks "bounded at
   1.3-2.4%", the trend 1.4→2.4→3.4% (3200→6400→12800) is real, F1 = 3.33 refutes even
   the saturation branch of P1, and a burn-4096 probe shows the ringdown still decaying
   (not plateaued — transient, not attractor) but *not extinct* at t = 12288 (~5 box
   periods; late-window m 1.37% vs the 6400 steady state's 0.62%). So the deletion claim
   is safe where flown (n ≤ 6400) and its mechanism predicts the 12800 reading, but the
   quoted m-bound does not extend as a number, and the "measurement rule" (m = relstd)
   needs the late-window form to compare across n.
4. **Novelty.** The 834e wiki page leaves exactly this lead open ("both allocator-visible,
   both unpriced" — checker2's N-scaling bracket); no HISTORY entry covers it. Not a
   repetition; it corrects 834e's "long-lived coherent breathing mode" phrasing with
   evidence. The identity itself is definitional (Fano = mean·relstd² for any
   distribution) — the measured content is ν flat (0.159-0.173) plus m bounded in the
   flown domain; the dossier presents the identity as if it were a finding. Noted on the
   page.
5. **Record defects (why silver, not gold, even setting P5 aside).** Two dossier cells
   quote stale numbers the final data does not match, undisclosed — the 6400 row (F64
   "38.18-39.05", m "2.37%" are the 2-seed values; the 3-seed regen reads 38.18-43.77,
   m 2.42%, per-seed ≤ 2.52%) and the poly_r arm ("F64 34.6, m 3.19%, mean64 33934" vs
   regen 17.26, 2.26%, 33798; block0 39.1 and share 0.23 do match — the whole-run values
   were read from a partial file, the same trap the author flagged for the still-running
   arms). And the dossier says "the 12800 octave … `regen.sh` includes it": regen.sh
   contains no 12800 arm. Also minor: "T ≈ 5.7-9·side" — measured 4.8-7.9 (+censored ≥6).
   None of this changes a conclusion (I corrected the page in place), but the record must
   be the regenerated numbers.
6. **Page.** Corrected in `wiki/chaos-shadowing.md`: the stale ladder and poly_r values,
   the self-contradictory "max/p50 ≤ 1.08 everywhere … 1.115", the T range, the
   definitional caveat, and a checker bracket with the 12800/v17/v18/fill-0.3 results;
   direction 3 now says to fly n ≥ 12800 at horizon ∝ side before quoting an m. The Runs
   list stays append-only. Faithful otherwise.
7. **Goal fit.** Board #4 (smoothness/allocator): prices an unpriced allocator-visible
   lead and deletes a feared requirement on the measured domain — "the cheapest compute
   is compute not done"; the falsifiable pre-registrations honour "a test that cannot
   fail is a control". The 60 s rule is met per-arm (~2 s at 400, ~2 min at 6400); the
   ladder is 6-10 min, disclosed.

**The one experiment for gold.** Fly n = 12800 (one more octave optional) at horizon ∝
side (≥ 24576) to extinction, with late-window m as the statistic: if the ringdown
reaches the anti-bunched baseline (blocks → ~2-3, late-m ~0.5%) the bounded-modulation
law and the deletion hold across the octave and the result is gold once the record cells
are fixed; if it plateaus, the transient reading itself fails at scale. My burn-4096
probe (blocks 88.6→12.0, still falling at t = 12288) predicts the former.

**What the author missed.** The 12800 arm costs ~7 min on this machine — the single most
load-bearing extrapolation was left unflown while the dossier claims regen.sh covers it.
The n-invariant instrument (late-window m) was available from their own lifetime ∝ side
law; without it the proposed measurement rule inherits, at 12800, exactly the flaw raw
Fano has at 6400. The steady-state letter is understated: at 6400 the post-ringdown
modulation is ~0.6%, not 2.4% — the true steady state is flatter than claimed. And the
partial-file trap they flagged for the queued arms had already bitten two published
cells. Data: `data/chk/` (this check); tree restored to base after reproduction.
