#!/usr/bin/env python3
# Extra cells for the dossier: (a) coarse de-phased fixed cadences at the
# resonance centre/detuned/second-phase; (b) TRIG2 (equidistributed budget)
# on S1, missing from the main S1 sweep. Usage: python3 extra.py
import json, importlib.util
spec = importlib.util.spec_from_file_location("cad", "cadence.py")
cad = importlib.util.module_from_spec(spec); cad.__name__ = "cad"; spec.loader.exec_module(cad)
out = {}
for s in ("S2c", "S2c2", "S2d"):
    sc = cad.make_scene(s)
    fin, _ = cad.truth(sc)
    at, et, _, _ = cad.elems(sc["GM"], fin[1], fin[2], fin[3], fin[4])
    row = {}
    for pol, kw in [("FIXED", dict(n_fixed=1)), ("FIXED", dict(n_fixed=2)),
                    ("FIXED", dict(n_fixed=4)), ("AVG", {})]:
        r = cad.layer(sc, pol, **kw)
        row[f"{pol}-{kw.get('n_fixed','')}"] = dict(
            kpo=round(r["kpo"], 2), epump=round(r["e"]/et, 3) if et > 1e-12 else None,
            unb=r.get("unbound", False))
    out[s] = dict(truth_e=round(et, 5), **row)
sc = cad.make_scene("S1")
fin, _ = cad.truth(sc)
at, et, _, _ = cad.elems(sc["GM"], fin[1], fin[2], fin[3], fin[4])
s1 = {}
for k in (0.125, 0.5, 1.0, 2.0):
    r = cad.layer(sc, "TRIG2", kappa=k)
    s1[f"TRIG2-{k}"] = dict(kpo=round(r["kpo"], 2),
                            da_rel=round(abs(r["a"]-at)/at, 8),
                            epump=round(r["e"]/et, 3))
out["S1_TRIG2"] = s1
print(json.dumps(out, indent=1))
json.dump(out, open("out_extra.json", "w"), indent=1)
