"""Criterion 4 (capture): E=1 anchors at r0=100, L = 4(1 +/- 0.01).
Truth: absorbed iff L < 4.  KILL on any misclassification.
Usage: run_capture.py CFG [CFG...]"""
import sys, json, time
import gv1b as G

cfgs = sys.argv[1:]
t0 = time.perf_counter()
rows = []
nbad = 0
for cfg in cfgs:
    print(f"== {cfg}: E=1 capture from r0=100, L=4(1+/-0.01) ==")
    for eta in (1/16, 1/32, 1/64):
        for order in (2, 4):
            line = []
            for sgn in (-1, 1):
                L = 4.0*(1.0 + sgn*0.01)
                expect = "absorbed" if L < 4.0 else "escaped"
                res, rmin, rmax, ev = G.run_capture(L, cfg, order, eta)
                ok = res == expect
                if not ok:
                    nbad += 1
                rows.append({"cfg": cfg, "order": order, "eta": eta, "L": L,
                             "expect": expect, "got": res, "rmin": rmin,
                             "rmax": rmax, "steps": ev, "ok": ok})
                line.append(f"L={L:.3f}:{res}({rmin:.2f}-{rmax:.1f},{ev}st)"
                            f"{'' if ok else ' WRONG!'}")
            print(f"  eta={eta:.4f} o{order}: " + "  ".join(line))
print(f"misclassifications: {nbad}")
with open("results_cap.jsonl", "a") as f:
    for rrow in rows:
        f.write(json.dumps(rrow) + "\n")
print(f"wall: {time.perf_counter()-t0:.1f} s")
