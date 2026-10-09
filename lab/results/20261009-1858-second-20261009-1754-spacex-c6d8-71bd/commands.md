# Reproduce (each command ≤ 60 s wall on the lab's Linux/x86 — orders of magnitude only)

    cargo build --release -p xtask
    # (binary at $CARGO_TARGET_DIR/release/xtask; here /home/glmlab/lab-target-0/release/xtask)

## The first run's four commands, instrument v2 (record regeneration; digests must equal the
## stored first-run JSONs: 83d96bed…, e56d1c12…, e3eb62e6…, 6ddafe96…)

    xtask universe --hlive-bench --rtf 100 --seconds 30                 # hlive-seed1-rtf100-v2.json
    xtask universe --hlive-bench --seed 2 --rtf 100 --seconds 30        # hlive-seed2-rtf100-v2.json
    xtask universe --hlive-bench --rtf 100 --seconds 30 --members 400   # hlive-seed1-members400-v2.json
    xtask universe --hlive-bench --rtf 20 --seconds 30                  # hlive-seed1-rtf20-v2.json

    xtask universe --kick-bench --rtf 100 --seconds 10                  # the regression the checker
                                                                        # named: --kick-bench works again

## The checker's named experiment: the quiescent belt (star + 3 planets, no moon/fleet/player/
## input), per-binding program refit, debt/cause journal split

    xtask universe --belt-bench --belt 120 --rtf 1000000 --seconds 55   # belt-seed1-rtf1e6-s55.json (tuned; 13 s)
    xtask universe --belt-bench --belt 120 --seed 2 --rtf 1000000 --seconds 55    # held out: seed
    xtask universe --belt-bench --belt 120 --belt-lo 0.55 --belt-hi 0.85 --rtf 1000000 --seconds 55  # held out: inner belt (cadence law)
    xtask universe --belt-bench --belt 120 --rtf 1000000 --seconds 20   # held out: horizon (stationarity)
    xtask universe --belt-bench --belt 240 --rtf 1000000 --seconds 55   # held out: density
    xtask universe --belt-bench --belt 120 --rtf 300000 --seconds 55    # control: rtf (frame merging)
    xtask universe --belt-bench --belt 120 --rtf 1000000 --seconds 5    # smoke (tuning only)
    xtask universe --belt-bench --belt 120 --rtf 1000000 --seconds 55   # rerun → identical digest (d6387a3e…)

Everything is in this folder; `work/patch.diff` is the full v2 patch (first run's patch plus the
fixes and the belt) against the tree this run started from.
