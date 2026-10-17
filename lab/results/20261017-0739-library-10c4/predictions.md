# Predictions (written before the decisive checks)

Held-out cases: none of these were tuned on; the census code was read only up to
`boundary_clock`/`boundary` bodies before writing this.

1. **Anchor readers.** The census of `BodyRec::anchor` readers in shipped code will show
   that between a belt body's kick (mid-interval) and its boundary (interval end) **no
   physics/ledger reader consults the body's state**: the only consumers of `anchor` are
   the map/view readout path and the boundary itself. If any engine ledger (encounters,
   scans, promotion) reads mid-interval, this prediction fails and the compute-ahead
   certificate is harder than the dossier claims.
2. **Boundary outcome classes on the belt.** In a flown belt (any published arm), the
   boundary resolutions of belt bodies are ≥ 99% "plain" (`Resolved::Boundary`, no Lost,
   no Handoff): the belt never crosses its doll's surface or edge inside a quiet interval,
   so the belt's boundary comb is certificates + anchor write + replan, not law work.
   Kill: a published per-outcome split showing belt boundaries Lost/Handoff above 1%.
3. **Split-21 legality (the one-dial closure).** A B14-class probe at the composed split
   S* ≈ 21× (belt ~6 kicks/orbit) passes the 10%-precession bar on the quiet far belt
   (1db4 already holds ~2/orbit there) and fails only inside the resonance-excluded bands
   the legality rule already carves out (06a8's 8/orbit Jupiter-belt floor). Predicted:
   pass outside exclusion bands, fail within them — i.e. the one-dial closure is legality-
   blocked only where the law already excludes averaging.
4. **Quote verbatimness.** Every quote in the dossier's five lessons is byte-identical to
   the cached Readwise export (checked by script, not by eye). Any mismatch downgrades the
   lesson it carries.
