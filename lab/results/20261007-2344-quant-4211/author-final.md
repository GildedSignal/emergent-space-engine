Working...
All artifacts in place (`predictions.md` before the run, `bench.rs`, `results.txt` with reproduction commands, `dossier.md`), no git operations, every process under the memory cap and finished.

**Claim:** the plane's deadline calendar costs O(N) heap-and-sqrt work every frame (rekey-all + a structural drain) and caps the engine at ~3×10⁴ bodies, while a dyadic wheel on event time — exact and player-independent, since the law's steps are already powers of two — plus a triangle-inequality skin on deadlines cuts the queue's frame cost 7–20× at 10⁶–3×10⁶ bodies with bit-identical canonical states (13.2× at β=1, 19.5× on a 10⁶ fleet ring, degrading to 2.4× at β·rtf=1000 where the skin stops paying).
