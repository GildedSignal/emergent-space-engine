# Reproduce (each command < 60 s wall; Linux/x86 — orders of magnitude only)

    cargo build --release -p xtask
    cargo run --release -q -p xtask -- universe --hlive-bench --rtf 100 --seconds 30            # tuned (seed 1)
    cargo run --release -q -p xtask -- universe --hlive-bench --seed 2 --rtf 100 --seconds 30   # held out: seed
    cargo run --release -q -p xtask -- universe --hlive-bench --rtf 100 --seconds 30 --members 400  # held out: dense fleet
    cargo run --release -q -p xtask -- universe --hlive-bench --rtf 20 --seconds 30             # held out: time factor

Stored JSONs: `hlive-seed1-rtf100.json`, `hlive-seed2-rtf100.json`, `hlive-seed1-members400.json`,
`hlive-seed1-rtf20.json` (same folder). The instrument is `xtask/src/universe/hlive_bench.rs`
 plus the `--hlive-bench` flag in `xtask/src/universe/mod.rs` (both in this run's patch).
