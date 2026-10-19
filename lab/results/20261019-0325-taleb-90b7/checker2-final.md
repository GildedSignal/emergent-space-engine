Working...
**Grade: gold** — written to `lab/results/20261019-0325-taleb-90b7/check2.md`, with my findings appended to the author's wiki page.

**Reproduction:** Applied `work/patch.diff` to a clean tree, rebuilt, reran three arms — byte-identical tsvs including digests. All 7 regime rows of the dossier's table match `work/table.txt`; the ops pair reproduces exactly (2,085,467 burst vs 1,591,692 quiet = 1.310×, isotropic q/256 at n=6400), as do P7's walls (6,650 vs 98,812) and the 1.20× late rate. Predictions were registered before the flights and scored honestly (P1's kill branch fired and is reported as fired).

**My adversarial cases** (beyond the author's and checker1's ranges), flown via a throwaway `fleetadv.rs` example since deleted:
- **σy = 1 quantum** → one-shot (F64_late 0.9–1.1): the page's binary-kill sharpening confirmed.
- **Oblique crossing** (coherent +q/8 transverse mismatch, zero randomness) → identical one-shot signature: the kill is *mismatch*, not dispersion randomness.
- **Unequal fleets** (n/2 vs n/4, ky=0 both, columns aligned) → the **train stands** (6 peaks, amp 0.951, F64_late 935, maxc = n/4): the operative condition is exact integer ky-equality + column alignment; "swap symmetry" is a loose name but the dossier's stated condition predicts both directions.
- **Mixed fleet-through-thermal-cloud** (the game case, unflown): no 3× season — worst window only 1.51× — but **never flat**: persistent m_late 8.2% vs thermal 2.4–2.8%, F64_late ~9.5. "Flat forever" is a fleet-fleet statement.

**Confirmed corrections:** comb teeth are 8 ch apart at all three n (dossier says 4 — wrong everywhere); `worlds.rs:154` shows galaxy draws drifts as random integers in ±q/4 with ±q/16 dispersion and ±q jitter, so *generated* fleets always sit in the one-shot regime — the train needs authored fleets.

Novel (the page's own "unpriced half", open direction 2), zero-cost to adopt, premise-correcting per PRINCIPLES 3 and 4. Tree left clean; nothing committed or pushed.
