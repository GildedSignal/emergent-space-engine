Working...
Run complete: measurements, pre-registered predictions, probe (`--view-probe`, saved as patch), verified digest reproduction, dossier at `lab/results/20261010-1152-constraint-c575/dossier.md`.

**Claim:** the plane's frame is constrained by the view gather, not the engine — it is the only unbudgeted, synchronous O(N) cost per frame (~70% of the frame at player rtf, 2.2–3.1× the whole engine's cost per body per second), and 63–77% of it is spent re-gathering emitters whose on-screen appearance changed less than half a pixel or one 8-bit colour step, so a rate-bounded refresh skin on the existing view memo cuts the frame's median cost 3–4× and re-binds the view to the player's channel instead of body count.
