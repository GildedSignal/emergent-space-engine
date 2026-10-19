Grade: silver

r11 exists, hash-frozen before its run and executed: PASS. Blind-checker reproduction
is total: regen.sh exit 0, every dossier number bit-identical (author metrics; check path
agrees to 1e-12; verdict PASS; diagnostics; c78d base byte-identical). The one-sample
negative fails three bars (0.841/0.800/0.058); pixel-h2/h1 pass at 113/29 samples. The
doppler correction is real (c78d's `cosang` is already v·n̂, then multiplied by β again;
correct SR is 1/(γ(1+β·px/q)) — I re-derived it, made c78d's mistake myself first
(sky f_true_min 0.8135≈their 0.815), and measured the delta fresh: 0.5273 vs 0.5206).
Gain: the c78d refutation becomes a one-step-adoptable guard; the licensed cure drops
145→29 samples. Cost: commit one file, amend representation.md L59.

Not gold: occlusion is not a board bottleneck, the premise refutation is c78d's, and the
hash-frozen domain line omits the density axis — uniform-pixel weights err p99 0.226/0.205
on a Gaussian-core fleet (253 samples, my fresh measurement; checker3's 0.229/0.210
reproduced), and the game's own fleets are non-uniform. One experiment makes it gold:
re-freeze with the density clause or a density-weighted candidate arm.

## Reasons

1. **Reproduction (complete).** `regen.sh` in a clean tree: rung sha256 OK; the four
   decisive configs byte-identical to `metrics.json`; the independent bisection path
   identical to ~1e-12; `verdict.py` → PASS; `diagnostics.json` identical; c78d's own
   script reruns byte-identical. Pixel counts (113/29/3/41/168) re-derived by hand.
2. **Physics verified from first principles.** Third independent retarded solver (Newton
   on φ(te)=t−te−|P(te)|, residual < 1e-9), both predicate forms, and the corrected
   doppler. The typo claim is confirmed in c78d's code (`orig-occlusion.py` L167-168,
   L235-236: `cosang = −β·prx/nrm` is v·n̂, then `1/(γ(1−β·cosang))` re-multiplies β).
   My fresh-path frozen-case numbers (own seed): sky f_true_min 0.8022 vs author 0.7999,
   pixel-h2 p99 0.0149 vs 0.0163 — same physics, seed-level variation only.
3. **Predictions.** Written after the rung hash (mtime order 31m→29m→25m→13m), and every
   decisive-case prediction held exactly (pixel-h2 five numbers; negative's three
   failures; positive 0.0018; verdict; β0.9 cure; static scaling; arc one-sample 1.000).
   Two disclosed misses, both on diagnostics, both with mechanisms (pixel-h1 p99-vs-peak
   semantics; arc h=0.15 edge fraction). Residual caveat: `eclipse_rung.py`'s mtime
   (19m) postdates `predictions.md` (25m) — the order claim rests on the author's word;
   regen proves determinism, not authorship order.
4. **Adversarial arms (mine, fresh code, seeds 777xxx; one outside the author's range).**
   The pixel-h2 cure HOLDS at: impact 1.0/2.0/2.8 at β 0.5 (p99 ≤ 0.0168, zero blink —
   the author froze impact 0 and never tested β×impact); β 0.99 (0.0215/0.0131, zero
   blink — next decade); 10× truth fleet N=2×10⁵ (0.0152 — no MC masking); 5× path steps
   6001 (0.0106/0.0153, peak ≤ 0.024 — no aliasing). The frozen case's neighbourhood is
   robust in every direction except density.
5. **The density axis (what the frozen rung cannot see).** Gaussian core σ=R_f/2, truth
   2×10⁴ ships, support disc = the aggregate's extent: uniform pixels err p99
   0.077/0.103 at 2σ support, 0.226/0.205 at 3σ support (253 samples — checker3's setup
   exactly, independently reproduced). Refining pitch does NOT restore 5%
   (h=0.25 uniform: 0.072/0.110) — the readout converges to the wrong uniform-disc law.
   Density-weighted pixels at the SAME pitch and cost restore it: 0.0089/0.0282 at 3σ.
   So the missing requirement is a weight moment (and the support radius itself is a
   moment: truncating at 2σ leaves 13.5% of mass outside the readout). The hash-frozen
   domain line ("the transit resolved on screen; cost = min(N, support pixels)") carries
   neither clause; a committed r11 would pass an engine whose uniform-pixel readout errs
   20% on cored fleets — and the game's formations are not uniform discs.
6. **Novelty.** No r11 or eclipse/occlusion rung in `lab/rungs/`; no HISTORY entry; the
   live page's direction 2 names exactly this freeze as c78d's gold-blocker. Not a
   repetition: the freeze fixes both checker-named criterion flaws, and the doppler
   typo is a new instrument finding (both prior checkers had "reproduced" the bug —
   the 5-October lesson again; I reproduced it myself before fixing, which is the
   cleanest possible demonstration that re-implementing a description is not
   independence).
7. **Page.** Faithful; checker3's folded numbers match my fresh measurements. I appended
   a blind-checker paragraph with the support-dependence nuance and the weight-not-pitch
   decomposition (the page's "uniform-density aggregates or pixels weighted by the
   density moment" clause is now measured at equal cost). Three gold runs do not agree
   on the topic; the page stays open.
8. **Goal fit.** Defends principle 28 ("the view is an instrument… it's a space clock
   literally") via principle 10's simplest falsifying test made mechanical; principle 21
   ("rough first, refine when a certificate could break") is exactly the 145→29
   refinement with the certificate holding. The per-pixel license is principle 3
   (derivable at pixel resolution) and principle 17 (29–113 predicates where per-ship
   loops pay N).

## The one experiment that would make it gold

Re-freeze r11 as v2 (the integrator's or the next run's): add the density clause to the
domain line, and/or a `pixel-density` candidate (density-weighted pixels) judged against
a cored or clumped truth alongside the uniform one — priced already at zero extra samples
by checker3's clump arms and my Gaussian decomposition. With that, the guard covers the
game's own fleet shapes and the c78d→4ff1 arc is gold as a unit.

## What the author missed

- The density axis is absent from the dossier's "what would make it wrong" (the page has
  it only via checker3); the frozen domain line still lacks it.
- The magnitude of the density failure is support-convention-dependent (0.077 at 2σ
  support vs 0.226 at 3σ): an unbounded fleet has no disc support, so the aggregate must
  carry its support radius as a moment too — part of direction 3's spatial-extent moment,
  not only the profile.
- The static positive control lives in a 2D flatland (orthogonal projection) that is not
  the β→0 limit of the 3D transit geometry (which magnifies the shadow by ~25/20 at the
  fleet plane). Harmless for the control's job (closed form vs per-point within one
  model), but the rung text calls both "exact" without noting the model change.
- p99-over-the-seen-window semantics: ~80% of the window is empty path, so p99 ≈ the
  worst ~12 steps of the ~225-step transit — effectively stricter than a transit-local
  p99, opposite in direction to the dilution one might fear (disclosed implicitly by the
  pixel-h1 miss, but the mechanics are worth a line in the rung).
