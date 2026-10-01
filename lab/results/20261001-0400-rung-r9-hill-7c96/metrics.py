"""Metrics for rung r9. Definitions (rung text, applied literally):

- class_match_fraction: over the configuration's domain, seeds whose truth is
  not chaotic (truth's bound/escaped class is unchanged under a 1e-6 relative
  change of a): fraction whose class matches the truth's. The truth's class is
  its own; kick-avg, no-tide and hill-torus conserve their doll (always bound),
  so their class is 'bound'.
- precession_match_fraction: over the domain's truth-bound seeds, the fraction
  whose apsidal precession rate (dominant |nu|<0.6 frequency of the secular
  eccentricity vector: secular_z + prec_rate, one identical pipeline for every
  configuration) is within 10% of the truth's.
- tau0 (kick-avg): the largest tau below which both fractions are >= 0.99
  (evaluated over all seeds).
- compiled_fraction (hill-torus): the fraction of seeds with tau >= tau0 that
  lie on tori hill-torus follows with class and precession matching.
- dense_steps: fallback dense-order steps in the engine's sense (law.md,
  orders). None of these configurations is the dense order - the truth is the
  external reference - so all report 0; the truth's actual integration work is
  reported in the dossier.

Domains: truth = all seeds; kick-avg, no-tide = a/R_H <= 0.3; hill-torus =
a/R_H > 0.3 and declared a torus (its declared-chaotic seeds count against
compiled_fraction, not against behaviour).
"""
import json
import numpy as np
from common import prec_rate, secular_z
from cands import TS


def slope(z):
    if z is None:
        return None
    zs = secular_z(TS, z)
    trim = 40                                   # drop 2 planet orbits at each edge
    return prec_rate(TS[trim:-trim], zs[trim:-trim])


def main():
    with open("truth.json") as f:
        truth = {r["i"]: r for r in json.load(f)}
    shards = [np.load(f"truth_shard{k}.npz") for k in range(4)]
    cz = np.load("cands.npz")
    with open("tori.json") as f:
        tori = {r["i"]: r for r in json.load(f)}

    rows = []
    for i in sorted(truth):
        r = truth[i]
        zt = shards[i // 64][f"z{i}"].astype(np.complex128)
        dec = tori[i]["declared"]
        rows.append(dict(
            i=i, aRH=r["aRH"], retro=r["retro"], tau=r["tau"],
            escaped=r["escaped"], chaotic=r["chaotic"],
            nu_truth=slope(zt) if not r["escaped"] else None,
            nu_kick=slope(cz[f"zk{i}"]),
            nu_notide=slope(cz[f"zn{i}"]),
            nu_hill=slope(cz[f"zh{i}"]) if dec else None,
            hill_declared=dec))

    def fractions(sub, key):
        cls = [r for r in sub if not r["chaotic"]]
        prc = [r for r in sub if not r["escaped"] and r[key] is not None and r["nu_truth"] is not None]
        cm = sum(not r["escaped"] for r in cls) / max(len(cls), 1)
        pm = sum(abs(r[key] - r["nu_truth"]) <= 0.1 * abs(r["nu_truth"]) for r in prc) / max(len(prc), 1)
        return cm, pm, len(cls), len(prc)

    hier = [r for r in rows if r["aRH"] <= 0.3]
    tor = [r for r in rows if r["aRH"] > 0.3 and r["hill_declared"]]
    km = fractions(hier, "nu_kick")
    nm = fractions(hier, "nu_notide")
    hm = fractions(tor, "nu_hill")

    out = {
        "truth": {"class_match_fraction": 1.0, "precession_match_fraction": 1.0, "dense_steps": 0},
        "kick-avg": {"class_match_fraction": round(km[0], 4), "precession_match_fraction": round(km[1], 4),
                     "dense_steps": 0},
        "hill-torus": {"class_match_fraction": round(hm[0], 4), "precession_match_fraction": round(hm[1], 4),
                       "dense_steps": 0},
        "no-tide": {"class_match_fraction": round(nm[0], 4), "precession_match_fraction": round(nm[1], 4),
                    "dense_steps": 0},
    }

    tau0 = 0.0
    for tstar in sorted(r["tau"] for r in rows):
        cm, pm, _, _ = fractions([r for r in rows if r["tau"] <= tstar], "nu_kick")
        if cm >= 0.99 and pm >= 0.99:
            tau0 = tstar
    out["kick-avg"]["tau0"] = round(tau0, 4)

    sub = [r for r in rows if r["tau"] >= tau0]
    good = [r for r in sub if r["hill_declared"] and not r["escaped"] and r["nu_hill"] is not None
            and r["nu_truth"] is not None
            and abs(r["nu_hill"] - r["nu_truth"]) <= 0.1 * abs(r["nu_truth"])]
    out["hill-torus"]["compiled_fraction"] = round(len(good) / max(len(sub), 1), 4)

    with open("metrics.json", "w") as f:
        json.dump(out, f, indent=1)
    with open("table.json", "w") as f:
        json.dump(rows, f, indent=1)
    print(json.dumps(out, indent=1))
    print(f"non-chaotic {sum(not r['chaotic'] for r in rows)}/256, "
          f"bound {sum(not r['escaped'] for r in rows)}, "
          f"declared tori {sum(r['hill_declared'] for r in rows)}, "
          f"kick domain n={km[2]}/{km[3]}, torus domain n={hm[2]}/{hm[3]}")


if __name__ == "__main__":
    main()
