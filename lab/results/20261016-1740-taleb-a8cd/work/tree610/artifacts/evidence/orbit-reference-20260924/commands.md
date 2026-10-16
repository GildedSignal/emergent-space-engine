# Reproduction

Worktree baseline 52675aa plus source changes in this evidence commit.
Use CARGO_BUILD_JOBS=1 and CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never.
Use CARGO_TARGET_DIR=/Users/julien_laurent/.cache/emergent-space/full-engine-integration-target.

- Reference probe: cargo test --release -p emergent-law-lab --lib retained_genesis_reference_probe --offline --locked -- --ignored --nocapture
- Set ORBIT_REFERENCE_SEED to 4/8/9/10/11, ORBIT_REFERENCE_STEPS to comma-separated doublings. See frozen experiment document for ladders.
- Set ORBIT_REFERENCE_OUTPUT to a new absolute JSON path (existing files are refused).
- Compiler probe: cargo test --release -p emergent-law-lab --lib causal_block_refinement_probe --offline --locked -- --ignored --nocapture
- Set ORBIT_REFERENCE_INPUT to a decompressed reference JSON and ORBIT_BLOCK_OUTPUT to a new absolute JSON output path.
- cargo test -p emergent-law-lab --lib --offline --locked
- I6_MATRIX_OUTPUT=<new absolute path> cargo test -p emergent-engine --test i6_qualification --test orbit_initialization --offline --locked
- cargo xtask history check

Decompress gzip JSON losslessly with gzip -dc. Original byte hashes are in provenance.json. Current code has the corrected accelerated root; pre-fix compiler measurements remain historical evidence.
