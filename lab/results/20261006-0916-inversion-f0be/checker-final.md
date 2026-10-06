Working...
Check complete. `lab/results/20261006-0916-inversion-f0be/check.md` written — **Grade: gold**. Nothing else in the author's folder was touched (all reproduction ran in a `/tmp` scratch copy); no git operations.

**What I did and found:**

- **Reproduction:** `probe.py s1`, `probe.py s4`, `s3b.py` all match the author's JSONs field-for-field. A file-time anomaly (probe.py newer than results-s4.json) is resolved — the shipped code regenerates every number exactly; `work/patch.diff` is content-free.
- **The headline holds:** overtakes/orbit 16449/263795/1052179 (n=128/512/1024), exponent 2.000, coefficient ≈ 1.0; 26×/122×/257× the n·k watch. My independent ring implementation reproduces all three points exactly, adds n=256 (66003) and seed 99 (exponent 1.998), and 16×-finer sampling changes S4 by +0.5% (conservative direction). The adopted gold's O(n·k) premise is wrong as stated.
- **My adversarial cases:**
  - 2D-compressed blob (radial + phase, the attack the author never ran): 668 dense-verified contacts, max λ-rank still 1 — their correctness conclusion is *stronger* than claimed.
  - Overtake decomposition: 221 swaps/body mean (not a flip-flop artifact); low-e jam scenes undercount ~19% at 4096 samples — again conservative.
  - LB-gate at e=0.9: misses exactly 1 contact of 226 (0.4%) — immaterial.
- **Faults found:** pre-registered prediction #5 was silently dropped; I tested it and it is refuted (contacts avoid quadrature, 0.222 vs 0.509 chance). The 10¹² extrapolation borrows the e=0.3 coefficient without saying so. The kill binds the flat rebuild design; the frozen-ring/hierarchical alternatives remain argued, not measured — named as the follow-up experiment.
