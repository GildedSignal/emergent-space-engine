Grade: gold

**Abstract.** Claim: the held-scan mint rate is the player's pacing, not a law constant — a burning player mints 13.5× the 0.0526 coast rate continuously (nladder 10⁴, level 8) and ~116× inside paced burst phases, while the same burn eats the drain's margin (held 1→258 at 12 ms; 0 at 24 ms with identical arrivals). Reproduced: regen exit 0, plus four fresh adversarial flights — seed 3 digit-identical, L15 gives 18.9/game-s, the load axis leaves arrivals invariant while held goes 114→370, and the 10⁵ decade holds the multiplier at ~21× (held 1→650, p99 8.0→11.4 ms). Gain: deletes any fence or expiry cadence sized on the coast record; adoption is one requirement line (cadence > λ_burn), no code. The 10⁶ wall rescale stays labeled inference.

## Reasons

**1. Reproduction.** The runner's regen.sh exited 0 and regenerated every table number (deterministic counts identical: bench entries 43/393/1215, census, λ 0.090/5.865/13.485; ladder coast 0.0971 entries / ~0.054 distinct vs burn 0.9766 / 0.728 = 13.5×; budget pair intact — b24 held 0, coast-b5 held 1; p99 5.1→10.8 ms; footprints 27→34 vs 27→54 MB). In my own hands: the digest-neutrality control gives `20a45aa4…` probe off and on (385 MINT lines on-arm); a fresh b-L8 gives entries 393, distinct 197, census {197,0,196}, λ 5.865/0.0027 — the digit. The original run's regen failure (patch double-apply, hardcoded target dir) was fixed with full disclosure and the commands now regenerate from a clean tree; I applied/reversed the patch myself.

**2. Predictions.** predictions.md predates the dossier (mtime 16 min earlier; its arm list is exactly the flown matrix) and all six held; the kill criterion (ratio < 2) never came close. Caveat, not fatal: the runner's regen overwrote the original flight outputs, so pre-registration rests on content + mtime rather than raw logs — but the deterministic counts reproduce identically across four independent executions (author, fix agent, runner, this check), which is stronger evidence than a timestamp.

**3. Adversarial (mine, four; one per axis the author left open).**
- *L15, beyond the swept dial (0/8/12):* λ_in-window 18.93/game-s, held max 1,022, player alive — monotone to the top of the throttle; no saturation or regime flip.
- *Seed 3 (held-out):* identical to the digit — 393/197, census equal, λ 5.865. Arrivals are structural (the canonical decision log), as claimed.
- *The load axis (the author's named unflown gap, b8e2's question):* under load ~4–5 on the same arm, arrivals are bit-identical (393/197/5.865) while held max goes 114 → 370. The convexity (arrivals up AND service down) extends from the engine-budget axis to machine load; the claim's mechanism survives, its low-margin numbers worsen.
- *The K decade 10⁴→10⁵ (author flew 10⁴):* coast 0.0973 entries / 0.0578 distinct per game-s (acf2's checker flew 0.059 distinct at 10⁵ coast — agrees), burn 1.596 / 1.233 → 16× entries, ~21× distinct; held 1 → 650; engine p99 8.0 → 11.4 ms; footprint 237→273 MB, no truncation, under the cap. The K-flatness premise carries a decade up, and if anything the multiplier grows.

**4. Novelty.** memory-h-live's open direction 3 still read "Still open: the burn arm (thrust changes the item rate)" — this run is its answer. acf2 sized the wall with the coast λ and this run re-sizes it; the 5 October memo finding (the player re-times a pending kick every frame in a burn) was the known mechanism, unquantified at the mint. No run in the wiki or HISTORY measures a burn-phase mint rate. Not a repetition.

**5. The page.** The NEW block is faithful to the evidence (I checked every number against out/analysis.json and my own flights). I added a checker bracket with the load-variance and the four extensions; no closure (not three golds on this best).

**6. Goal fit.** Board focus "memory at 10⁹" / the nladder pin, interlocked with #1: the premise that the fence-sizing rate is the coast constant is shown wrong by a measured >10× on two scales and two harnesses, with the mechanism named (the player's event clock, census t-dominated). PRINCIPLES 5: "The player is the only wildcard" — the mint rate is literally his throttle hand; 12: the burn raises arrivals and p99 in the same frames. Adoptable within one step: a requirement line on the unwritten answer-or-expire fix.

## What the author missed

- **The between-burn tail is itself a fence problem:** at L12 the coast-phase λ is 0.431 (≈ 8× the coast constant; L15: 0.487) — the post-burn event tail means a fence sized only on in-window λ_burn still undersizes the sustained high-throttle rate (L12 overall: 1.52 entries/game-s). The author names the tail but does not price it into the requirement.
- **λ_burn's absolute value rides the frame cadence** (0.98 continuous on the unpaced ladder vs 5.87 in-window on the paced loop — two rates for one throttle level). The invariant is the ratio (13.5–21×) and the census; the page's "> 6–14 answers/game-s" bracket is cadence-scoped. As a sizing floor the paced-loop number errs safe, but the page should say the domain.
- **held_max is load-elastic everywhere** (reruns: 8–114 at L0/L8 quiet, 182–258 at 10⁴, 370 loaded, 650 at 10⁵ loaded): point values should not be quoted as law; the author disclosed this only for the ladder.
- At 10⁵ under load, entries include '0'-class re-pushes that inflate λ_entries; distinct λ is the cleaner comparator (still ~21×).
- The 10⁶ point remains unflown (self-declared, honestly labeled [INFERENCE]); the load axis I flew — it confirms.
