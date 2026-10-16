Working...
Tests pass on the patched tree; all deliverables are in place (predictions.md, dossier.md, regen.sh tested end-to-end, raw outputs, wiki proposal). The work is complete.

**Claim:** On the shipped representation the fired kick's rebind is compile-bound, not fit-bound — `Orbit::compile` is 85–90% of a 60–72 µs mean rebind (4,553 rebinds, three seeds) while `fit_key` is 6%, its 128-step bisection worth 3%, and a Newton-from-seed prototype reproduces the shipped key exactly at the law's quantum on 4,553/4,553 — so the kick's true floor is ~6 µs (not b063's 42–56 ns write floor, nor 1e74's ~26 µs machinery residue) and the shipped rebind sits ~10–12× above it, with the verified Carlson compile (~18× cheaper) as the deletion that reaches it.
