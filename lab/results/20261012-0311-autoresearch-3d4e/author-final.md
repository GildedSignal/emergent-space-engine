Working...
Universe suite green too (all `test result: ok`, 0 failed) with the final patch — downstream bit-identity holds. Run complete: predictions (P1/P2 failed, P3/P4 held), log, dossier, patch and bench all in `lab/results/20261012-0311-autoresearch-3d4e/`.

**Claim:** the orbit compiler's per-kick cost is no longer division-bound — replacing every remaining 128-bit software division on the compile path with exact word-size divisions (`div_word`, bit-identical by construction) buys only ~3% end-to-end because the cost is diffuse (cos ~18%, node arithmetic ~20%, ~60% structural bookkeeping), so the next ns/compile lever is shape reuse, not arithmetic.
