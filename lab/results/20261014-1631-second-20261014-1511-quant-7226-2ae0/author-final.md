Done. The cEverything is in place and verified. Final state:

- **The named experiment done**: guarded AB-IQI policy (`ES_FP=3`) — IQI through the three newest readouts + Anderson–Björck retention decay + crawl bail — passes the frozen tail rule everywhere (worst 11–18 vs ≤ 30, mean 10.6–11.1 vs 29.4, probes −62…−64% at 3 seeds × both paces, flying leaver −34…−35%, digests bit-identical at every layer, refused 0, suite 11/11).
- **Composed with the warm start (0b85)**: readouts −78…−83% vs shipped (23,552→3,932 at s3 flying, worst 32→11), flying leaver −43…−47%, savings add, identity holds at every layer.
- **The kill table regenerates from the patch** (secant row exactly: 35,621/57); the earlier variants lost their gain to the retention discipline.
- **Honest pre-registered miss (P2)**: battle leaver *median* flat — the descents sit in the dipping minority, so the cut lands at all-kick p99 (−13…−14%); no probe policy moves a search-free median.

`regen.sh` regenerates every number (~30 s after build, tested end-to-end); predictions, dossier, and the wiki page proposal are in the run folder.

**Claim:** the checker's named gold experiment holds — a tail-guarded Anderson–Björck/IQI probe policy on the kick's crash search passes the frozen rule at three seeds and both paces with bit-identical digests (worst 11–18 probes, mean ~10.7 vs 29.4, flying leaver −34…−35%), and composed with the warm start it deletes 78–83% of the search's exact readouts exact.
