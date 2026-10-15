#!/bin/sh
# Regen for 20261015-2041-redteam-0e9d: reproduces every dossier number from
# the shipped tree + this run's script. Patch (if any) applies first; the run
# made no edits outside its own folder, so patch.diff may be empty or absent.
set -e
cd "$(dirname "$0")"
if [ -f work/patch.diff ] && [ -s work/patch.diff ]; then
  git apply --check work/patch.diff 2>/dev/null && git apply work/patch.diff || true
fi
python3 falsifier.py falsifier_out.json
echo "--- key rows (compare with dossier.md) ---"
python3 - <<'EOF'
import json
d = json.load(open("falsifier_out.json"))
rows = {(r["e"], r["kick"]): r for r in d["A"]["rows"]}
for k in [(0.99, "encounter 1e-3"), (0.9, "deep passage 1e-2"), (0.999, "belt 2^-23")]:
    r = rows[k]
    print(f"A: e={k[0]} kick={k[1]}: eps1={r['eps1']:.3e}")
print("A e*(1%):", d["A"]["estar"], " 2nd-order:", d["A"]["estar2"])
for arm in ("one_sided", "random_sign"):
    for r in d["B"][arm]:
        last = r["hist"][-1] if r["hist"] else None
        print(f"B: {arm} {'chained' if r['chained'] else 'fresh'} kicks={r['kicks']}"
              f" last_err={last['mean_anom_err_turns']:.2e} turns" if last else "")
print("C control tau relerr:", f"{d['C_control']['relerr']:.2e}")
lf = [f for f in d["C"]["fit"] if "log_fit_slope" in f][0]
print(f"C: T = {lf['log_fit_a']:.1f} + {lf['log_fit_slope']:.2f} ln(1/d)")
for r in d["C"]["ma"]:
    if r["eps"] is not None:
        print(f"C MA: d={r['d']:.0e} dL/L={r['dl_rel']:.0e} eps={r['eps']:.3e}")
    else:
        print(f"C MA boundary kick: T_ma={r['T_ma_bound']:.1f} exact={r['exact']}")
print("wall_s:", round(d["wall_s"], 2))
EOF
