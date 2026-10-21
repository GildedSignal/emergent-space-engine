#!/usr/bin/env bash
# Regenerates every number in the dossier: control, map check, both grids
# (truncated + exact ICs), convergence/repro, then the analysis tables.
# Total ~3 min on the lab's 8-core Linux runner.  All JSONs + analysis.txt
# are rewritten from scratch; exit nonzero on any failure.
set -e
cd "$(dirname "$0")"
[ -f work/patch.diff ] && git apply --allow-empty work/patch.diff || true
for m in control mapcheck flyby flyby2 conv; do
  echo "== falsifier.py $m"
  python3 falsifier.py "$m" > "$m.json"
done
python3 analyze.py > analysis.txt
echo "== controls summary (must all pass)"
python3 - <<'EOF'
import json
c = json.load(open("control.json"))
mc = json.load(open("mapcheck.json"))
cv = json.load(open("conv.json"))["conv"]
fly = json.load(open("flyby.json"))["flyby"]
ok = True
def chk(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name)
    ok = ok and cond
chk("eigen dev < 1e-13 (7 points, 4c79 closed forms)",
    max(r["eig_dev"] for r in c["eigen_control"]) < 1e-13)
chk("eigen u_drift < 1e-9 and orthonorm < 1e-9",
    max(r["u_drift"] for r in c["eigen_control"]) < 1e-9
    and max(r["orthonorm"] for r in c["eigen_control"]) < 1e-9)
chk("rhs_check (vectorized member RHS) < 1e-12", c["rhs_check"] < 1e-12)
chk("sign: member u.u at tau=0 < 1e-14 (normalized ICs)",
    max(max(s["udrift0_max_by_xi"].values()) for s in c["sign_control"]) < 1e-14)
chk("sign: roundtrip0 quadratic in xi (ratio in (3e4, 3e5) over 300x xi)",
    all(3e4 < max(s["roundtrip0_max_by_xi"].values()) /
        min(s["roundtrip0_max_by_xi"].values()) < 3e5 for s in c["sign_control"]))
chk("map: dual residual < old residual (except one radial cell)",
    sum(1 for r in mc["map_check"] if r["resid_dual"] < r["resid_old"]) >= 14)
repro = [c for c in cv if c["cfg"] == "repro451f"][0]["exit"]
ref = json.load(open("ref-451f-flyby.json"))["flyby"][1]["checkpoints"]
m1 = [r[2] for r in repro if r[1] == 1e-4][0]
m2 = [r[2] for r in repro if r[1] == 3e-2][0]
chk("repro451f z@1e-4 within 1e-3 of 451f", abs(m1 - ref["z|0.0001"]["3999"]) / ref["z|0.0001"]["3999"] < 1e-3)
chk("repro451f z@3e-2 within 5% of 451f", abs(m2 - ref["z|0.03"]["3999"]) / ref["z|0.03"]["3999"] < 0.05)
fixed = [c for c in cv if c["cfg"] == "fixed"]
z1 = [[r[2] for r in c["exit"] if r[0] == "z" and r[1] == 1e-4][0] for c in fixed]
chk("fixed z@1e-4 flat under 8x refinement (spread < 1%)", (max(z1) - min(z1)) / min(z1) < 0.01)
chk("fixed z@1e-4 at least 10x below frozen 451f value", z1[-1] < 0.1 * ref["z|0.0001"]["3999"])
chk("grid drifts < 1e-9 everywhere", max(r["u_drift"] for r in fly) < 1e-9
    and max(r["member_u_drift_exit"] for r in fly) < 1e-9
    and max(r["orthonorm"] for r in fly) < 1e-9)
raise SystemExit(0 if ok else 1)
EOF
echo "ALL CONTROLS PASS"
