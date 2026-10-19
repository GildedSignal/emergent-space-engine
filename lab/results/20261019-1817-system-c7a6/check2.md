Grade: gold

**Abstract.** The retention law's demand side, never measured, is measured: on the shipped
ratchet scene (nladder 3×10⁴ burn, 197.7k game-s) only 20.6k of 7.27M `binding_at` calls
(0.28%) touch history, deepest 5.3k game-s (coast identical: 5,271.3), while `keep` grows to
105k game-s and 272k segments — ≥ 92% of channel 2's stock is never read; the view reads one
leg, the second leg nobody. Reproduced by regen (exit 0) and two out-of-range arms of mine:
rtf 4000 to 230k game-s (deepest 5,315.7, ratio 26.3×) and 10⁵ bodies with the view on (all
100,048 emitters delivered every gather; lawful leg 3,155.5, N-independent). Adoption: one
keep-law change (constant headless, one leg in game) plus a digest/view flight; deletes
channel 2's O(c·t) growth.

**Reasons.**

1. **Reproduction.** `regen.sh` exit 0 in a clean tree with `work/patch.diff` applied; every
   headline number regenerates within wall-cap jitter: reads 7,268,353 (dossier 7,266,323),
   hist 20,649 (20,413), lb run-max 5,276.5 (5,272.9), stock 272,324 (272,314), keep_med
   105,339 (105,316), ratio 20.0×, coast 5,271.3 exact, armD's ages p50 4,623→4,934 / max
   6,079→7,292 exact against keep_med 8,265–12,906, first wave 13,807→14,874, 7.01/body at
   gs 174,231, RSS 1,043 MB, 311/372 windows read zero history. The instrument is sound:
   `PlainBodies` is the only `BodyStore`, so every in-process `binding_at` passes the census;
   the one deeper reader (`binding_at(i, born)`) is `#[cfg(test)]`; `bindings_of` is the
   prune-side writer sweep, correctly excluded; off = shipped bits.
2. **Predictions.** `predictions.md` predates the flights (file order in the run folder). P3
   exact, P4 held with 4 orders of margin, P1 held on three clauses with its "keep passes
   3×10⁵" letter honestly reported failed — my rtf-4000 arm confirms it genuinely fails
   (keep_med 139,731 at 230k, still < 3×10⁵): a real misestimate, disclosed, not tuned. P2's
   letter failed at artificial cadences and was re-earned at the game's cadence, disclosed.
   The failures are reported as failures — the lab's gold-denial precedent (1 Oct law
   red-team) was for a miss reported as held; this is the opposite.
3. **Adversarial (mine).** (a) rtf 4000 burn to 230,308 game-s, past the author's horizon:
   demand constant 5,315.7, hist_frac 0.32%, keep_med 139,731, ratio 26.3× and rising; keep_med
   at matched gs 197,775 = 105,355 ≈ the author's 105,316 (canonical, rtf-independent). (b)
   N = 10⁵ coast + view every 60 frames, a decade up: all 100,048 emitters delivered at every
   gather, lawful leg 3,155.5 = the 3×10⁴ digit (N-independent), census keep_over_demand 0.3×
   with zero emitter loss — the None-probing recovery holds at scale, and even less than the
   rule's one leg is visibly sufficient on that scene. (c) Instrument-completeness attack:
   every `binding_at` call site in `crates/universe/src` audited (ctx, encounter, ext,
   observe, step, view) — none bypasses the census; the ViewCache tests assert any stale cache
   yields the same view, so probing artifacts cannot change the view.
4. **Novelty.** `lab/wiki/nladder.md`'s channel-2 entry (527a) ends "it belongs to the
   view/retention design" — the demand side was the named open door. 4447/e181/527a/b911/f80a
   are all supply-side (fences, freezes, TTLs). 527a's `hist_max 5,845` hints at the constant
   but with no attribution, no ratio, no cadence or phase decomposition. New topic page
   (`history-demand`), faithful to the evidence; two letter-level overstatements found and
   corrected in place (below).
5. **Goal fit.** Memory at 10⁹ is a board row; 4447 measured channel 2 as the unbounded
   ruin channel (1.6 GB guard at 332k gs). This run shows its premise wrong — the retained
   interval is not the view's necessary supply — which is a premise kill on shipped code,
   adoptable in one step (a keep-law change of the same class as b911's env-gated freeze,
   which was already flown digest-neutral). PRINCIPLES: "Less is more… Delete before
   optimizing" (1); "Nothing is evolved that can be derived when looked at (clocks, redshift,
   views)" (3) — the retained interval is exactly an evolved view cache; "The best part is no
   part" (17).

**Page corrections made (in place, marked [checker2]).** (i) "no read RETURNS a binding beyond
one leg + cadence slack": the census counts attempts, not returns; what is measured is that no
gather ever loses an emitter (now backed at 10⁵ and at keep_over_demand 0.3×). (ii) "headless
flights read nothing at all": the bench's own end-of-flight gather reads one leg once after the
last census print; the 0.28%/20,413 counts the loop. Both letters narrowed to the evidence; the
claim's substance is untouched.

**What the author missed.**

- The attempts/returns distinction was load-bearing from the start: armB's deepest census read
  (93,322) sits past two legs (2×45,564 = 91,128) and inside keep (105k), so it could have
  returned a binding; only the behaviour-level evidence (no emitter lost, ages bounded by the
  leg) closes it. One bool per history read in the census would have settled it.
- Scene universality of the 5,273 s headless constant: one scene family (nladder, one star,
  fixed seed), and my arms vary time and N, not scene class. The credit walk-back mechanism
  plausibly scales with the doll chain; a formation/belt scene could shift the constant. The
  headless keep should ship as derived-or-guarded, not as the bare constant (the author names
  this; it is the one experiment that hardens adoption, already listed as open direction 3).
- The P1 letter's β misestimate was derivable before flight from the burn script's recession
  profile; a 30-second Fermi on the script would have caught "keep passes 3×10⁵".
- The replay contract ("today's replays never re-gather at a past tick") is asserted from the
  census of benches, not from flying a replay; the census instrument cannot be armed in other
  binaries without a patch (it is switched on only in nladder's main).
