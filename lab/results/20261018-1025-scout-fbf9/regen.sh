#!/bin/sh
# Regenerates every number in dossier.md from the shipped-constant toy.
# Runtime ~10 s; needs python3 with numpy only.
cd "$(dirname "$0")" && python3 toy.py > regen.out 2>&1 && tail -5 regen.out
python3 - <<'EOF'
import importlib.util
spec = importlib.util.spec_from_file_location("toy", "toy.py")
toy = importlib.util.module_from_spec(spec); spec.loader.exec_module(toy)
for seed in (777, 424242):
    v = toy.run_dilute(10000, seed=seed, dv_list=[2**-23], n_kicks=200)["dv_2e23"]
    print(f"seed {seed}: armed={v['armed_per_body']} flips={v['flips_on_per_kick']+v['flips_off_per_kick']} nearband={v['near_band_per_body']:.3f}")
EOF
