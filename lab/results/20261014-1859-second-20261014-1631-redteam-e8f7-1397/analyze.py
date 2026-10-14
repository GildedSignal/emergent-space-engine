#!/usr/bin/env python3
"""Analyze probe_out.jsonl (the positive control on the shipped path) against the frozen
predictions in predictions.md, and assert every dossier number. Exits nonzero on any miss."""
import json
import sys

rows = [json.loads(l) for l in open("probe_out.jsonl")]
g1 = [r for r in rows if r["tag"].startswith("g1_")]
g2 = [r for r in rows if r["tag"].startswith("g2_")]
g3 = [r for r in rows if r["tag"].startswith("g3_")]
named = {r["tag"]: r for r in rows if r["tag"] in
         ("player_group", "inspiral", "high_gamma", "perp_offset", "worst_cell")}
scale = {r["tag"]: r for r in rows if r["tag"].startswith("scale_")}
depth = {r["tag"]: r for r in rows if r["tag"].startswith("depth")}
tb = {r["tag"]: r for r in rows if r["tag"].startswith("tb_")}
comp = [r for r in rows if "err_comp" in r]

# 1. Positive control: composed integer key <= 1e-9 ticks everywhere (predicted; kill at 1 tick).
worst = max(comp, key=lambda r: abs(r["err_comp"]))
assert abs(worst["err_comp"]) < 1e-9, worst
print(f"composed key: max |err| = {abs(worst['err_comp']):.3e} ticks at {worst['tag']} "
      f"(<= 1 tick by {abs(1.0/worst['err_comp']):.1e}x); {len(comp)} cases, 0 over 1 tick")

# 2. Scaling signature: oracle-noise-limited error scales with the offset.
r = abs(scale["scale_d80000"]["err_comp"] / scale["scale_d10000"]["err_comp"])
assert 2.0 < r < 32.0, r
print(f"scaling signature: err(d=8e4)/err(d=1e4) = {r:.2f} (oracle-noise-limited, as predicted)")

# 3. Negative control: the additive keys reproduce the frozen record.
n1 = sum(1 for r in g1 if max(abs(r["err1"]), abs(r["err2"])) >= 1.0)
n10 = sum(1 for r in g1 if max(abs(r["err1"]), abs(r["err2"])) >= 10.0)
assert (n1, n10, len(g1)) == (79, 52, 108), (n1, n10, len(g1))
w = max(g1, key=lambda r: max(abs(r["err1"]), abs(r["err2"])))
assert w["tag"] == "g1_b0.9_b0.3_th0_d10000"
assert round(w["err1"], 1) == 4069.9 and round(w["err2"], 1) == 5066.9, w
for tag, e1, e2 in [("player_group", 15.18, 15.18), ("inspiral", 178.63, 357.27),
                     ("high_gamma", 130.07, 140.47), ("perp_offset", 0.0, 0.0)]:
    assert round(named[tag]["err1"], 2) == e1 and round(named[tag]["err2"], 2) == e2, tag
for n, e1 in [("depth2_collinear", 15.2), ("depth3_collinear", 78.1), ("depth4_collinear", 227.5),
              ("depth5_collinear", 511.9), ("depth6_collinear", 994.7), ("depth8_collinear", 2921.0)]:
    assert round(depth[n]["err1"], 1) == e1, (n, depth[n]["err1"])
print(f"additive keys: G1 census {n1}/{len(g1)} >= 1 tick, {n10} >= 10; worst {w['err1']:.1f}/{w['err2']:.1f}; "
      f"depths 15.2/78.1/227.5/511.9/994.7/2921.0 - the frozen record reproduced")

# 4. The understated worst case, measured (predicted 2.67e4 / 4.56e4 from the analytic law).
assert abs(named["worst_cell"]["err1"] - 26721.0) < 1.0 and abs(named["worst_cell"]["err2"] - 45615.6) < 1.0
print(f"worst cell (0.9,0.9,45deg,1e4): V1 {named['worst_cell']['err1']:.1f}  V2 {named['worst_cell']['err2']:.1f}  "
      f"composed {named['worst_cell']['err_comp']:.2e}")

# 5. t_B channel: the composed map's time factor carries the child tick.
tbc, tbp = tb["tb_collinear"], tb["tb_perpendicular"]
assert round(tbc["t_exact"], 2) == 16666.67 and round(tbc["err_unscaled"], 1) == 6666.7
assert round(tbc["err_gamma12"], 1) == 3333.3 and abs(tbc["err_comp"]) < 1e-9
assert round(tbp["t_exact"], 2) == 13333.33 and tbp["err_gamma12"] == 0.0
assert abs(tbp["err_comp"]) < 1e-9
print(f"t_B channel: collinear t_exact {tbc['t_exact']:.2f} = gamma1*gamma2*(1+b1b2)*tB "
      f"(unscaled misses {tbc['err_unscaled']:.1f}, per-link gamma1*gamma2 misses {tbc['err_gamma12']:.1f}, "
      f"composed errs {tbc['err_comp']:.1e}); perpendicular gamma1*gamma2 exact ({tbp['err_gamma12']:.1f}), "
      f"composed {tbp['err_comp']:.1e}")

# 6. Extended + planar coverage sanity.
assert len(g2) == 20 and len(g3) == 16
assert max(abs(r["err2"]) for r in g2) > 4e4  # the additive key is worse than the record's worst cell
assert all(abs(r["err_comp"]) < 1e-9 for r in g2 + g3)
flips = [r for r in g3 if "t110" in r["tag"]]  # exercises the rotation flip path
assert flips and all(abs(r["err_comp"]) < 1e-9 for r in flips)
print(f"extended G2 (beta up to 0.99): worst additive {max(max(abs(r['err1']),abs(r['err2'])) for r in g2):.0f} ticks; "
      f"planar G3 (theta1 != 0, flip path): composed max {max(abs(r['err_comp']) for r in g3):.1e}")

print("analyze: every frozen prediction held; all dossier numbers asserted")
