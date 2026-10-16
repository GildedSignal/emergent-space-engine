Grade: silver

**Abstract.** The belt wave kick's interior is decomposed on shipped code (N=10⁵): fit ~41%,
three source reads ~23%, the tau pair ~15% — two exact duplicate decode walks — own readout 8%.
The built `ES_TAU_CARRY` deletes the pair (W_TAUT 389,211→11, W_TAU0→1; fired kick −15.5% on the
checker's re-run, −17% on the author's box), digests identical at both cuts, on all 8
frame_digest flights × 4 schedules, and off-arm == pristine main bit for bit. Checker's
adversarial cases (N=2×10⁵ first wave; a WH-dominated 70–400 ks window at 2×10⁴): digests
identical, counters →0 in both. Apply's position walk priced (−13% more, not built). Adoption:
~60 lines, default off, no API change. The anchor half re-derives 2833's unadopted cache; the
t-walk carry and the decomposition are new. Gain 1.2× built, 1.5× priced — not the 10× bar.

**Reasons.**
1. **Reproduction.** The runner's `regen.sh` exited 0; every deterministic number regenerates
   exactly: W_TAUT 389,211→11, W_TAU0→1, repeat share 0.296, worst multiplicity 322, digests
   `0d8ced80…`/`07891363…` identical across arms, `frame_digest` identical across arms, off-arm
   identical to a pristine-main build. My own re-run of the timing table confirms the structure;
   absolute µs sit ~12% below the dossier (shared-box load, disclosed in the dossier); the ratios
   hold: fired kick −15.5% (dossier −17%), WH kick −18.5% (−20%), wave CPU −9.2% (−10.2%).
2. **Exactness by construction, confirmed in code.** `readout_with_state` is line-for-line the
   shipped `readout` (bind.rs:160-170) with the orbit state kept; `bind_in` decodes at the same
   `t` that becomes the new binding's `event_time` (bind.rs:276), so `anchor_proper` caches
   exactly the value `old.orbit_state(old.event_time)` re-derives; bindings are immutable
   history, so the cache cannot go stale. Off-arm is the shipped path plus counters only.
3. **Adversarial, both outside the author's range.** (a) N=2×10⁵ first wave (2× the decisive N):
   digest `c55dcf84…` identical across arms; W_TAUT 0 on-arm, W_TAU0 first-kicks-only (199,710) —
   the predicted first-wave mechanism. (b) N=2×10⁴, window 70–400 ks — a regime the author did
   not test: the mix flips (WH 68% vs 31%), encounters 4×, repeat share 0.651; digest
   `6a0837f4…` identical, W_TAUT 731,015→13, W_TAU0→1, wave CPU −6.5% ≈ 82% of the deleted
   walks' time. The (a) kick-item timing is polluted by fit drift (+6% between arms on the
   loaded box); the deterministic counters and digests are the evidence there.
4. **Predictions.** Pre-registered with a kill criterion; 5 of 6 held. #5 failed honestly
   (source-repeat share 0.029 vs ≥0.6 predicted; the 0.614 smoke at N=2000 was the locals' comb)
   and the dossier kills the memo lever on its own evidence — the miss is itself evidence the
   file predates the decisive runs.
5. **Novelty.** The kick-jet page named "the wave's ~85–93% non-compile attendants" as the next
   lever; this run is that decomposition, new. But the anchor-half carry re-derives
   `20261010-1947-autoresearch-2833` (proper_at_event cache, silver, unadopted, pure-kick
   microbench 9–10%) — now measured on the shipped wave path, belt scale, digest-identical. I
   corrected the proposed page to cite it. New: the t-walk carry (the larger half), the stage
   table, the memo kill, the apply-walk pricing, the 10⁹ core pricing.
6. **Page.** The fold-in is faithful (prior content untouched, one paragraph, one run line);
   corrected in place: the 2833 citation and the double-count below.
7. **Corrections to the numbers (none load-bearing).** The item decomposition double-counts the
   bind decode: W_BIND's clock sits inside FIT's, so "fit 20.3 + decode 3.8" counts the decode
   twice; walks+fit is ~93% of the item (item ≈45 µs on the author's box), not 95%+3.8. "389,211
   fired kicks" is 389,200 kicks + 11 hand-outs. "17 cores per billion" is ~14 from its own
   inputs (8.4 µs × 1.68M kicks/s); the order of magnitude stands (board background: ~190 cores
   for the whole stream).
8. **Goal fit.** Board focus item 3 (the kick). PRINCIPLES #3 "Nothing is evolved that can be
   derived when looked at"; #17 "the best part is no part". The lens caveat is honest: the fit's
   41% is the compile wall another program owns, and the cadence split (kick-cadence open 2)
   dwarfs both deletions.

**The experiment to gold.** The author's own: build the apply-walk carry (hand the resolved
state to `apply`, deleting `root_state_raw`'s re-read at the event tick) and re-price on the M1
where the fit's share halves — but note that lands ~1.5–1.6×, still timing; gold then needs the
carry to delete a component outright (the resolver→apply state hand-off removing the position
walk from every event), not merely shave the cycle.

**What the author missed.**
- The 2833 prior art (page corrected).
- The W_BIND-inside-FIT double-count in the headline decomposition.
- The belt A/B is single-seed (seed 1); my different-regime window partially covers this, but a
  second belt seed would close it.
- The "17 cores" arithmetic vs its own inputs (~14); "1.68M kicks/wall-s" is not regenerable
  from raw/ (it is the author's box rate; my re-run gives ~1.9M at 52 µs/kick on the first-wave
  window — same order).
