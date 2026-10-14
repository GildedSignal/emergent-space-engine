#!/usr/bin/env python3
"""Exact-rational analysis of ikick.out: the integer impulse delivery vs the shipped refit.

Conventions (shipped Scalar): value = significand * 2^(exponent-62).
Darwin inverse (lib.rs Key::darwin, exact rationals here): with p = semi-latus, e,
  L^2 = p^2/(p-3-e^2), u_p = (1+e)/p, E^2 = (1-2 u_p)(1+(L u_p)^2).
The refit's OrbitKey carries (periapsis, k); k = floor(Q48/(1+e)) -> e = 2^48/k - 1,
p = periapsis*(1+e).
"""
from fractions import Fraction as F
import json, random, sys

Q48, Q32 = 1 << 48, 1 << 32

def val(sig, exp):
    return F(sig) * F(2) ** (exp - 62)

def darwin(p, e):
    l2 = p * p / (p - 3 - e * e)
    L = l2 ** F(1, 2)
    up = (1 + e) / p
    E = ((1 - 2 * up) * (1 + (L * up) ** 2)) ** F(1, 2)
    return E, L

def quantaE(x):
    return float(x * Q48)

def quantaL(x):
    return float(x * Q32)

def rkey_quanta(rsig, rexp, k):
    if k == -2 or k == -1:
        return None
    rp = val(rsig, rexp)
    e = F(Q48, k) - 1
    p = rp * (1 + e)
    E, L = darwin(p, e)
    return E, L

def main():
    cases = []
    prices = {}
    for line in open(sys.argv[1] if len(sys.argv) > 1 else "work_ikick.out"):
        f = line.split()
        if f[0] == "price":
            prices[" ".join(f[:2])] = f[2]
            continue
        if f[0] == "case" or not f[0].lstrip("-").isdigit() or len(f) != 18:
            continue
        (psig, pexp, e4, t, d, dvrf, dvtf, rsig, rexp, rk,
         e0s, e0e, l0s, l0e, eps, epe, lps, lpe) = map(int, f)
        cases.append(dict(
            p=val(psig, pexp), e=F(e4, 10000), t=t, d=d, dvrf=dvrf, dvtf=dvtf,
            refit=(rsig, rexp, rk), E0=val(e0s, e0e), L0=val(l0s, l0e),
            Ep=val(eps, epe), Lp=val(lps, lpe)))

    out = {"n_cases": len(cases), "prices": prices}

    # C0: my invariants on the un-kicked state vs the key's own darwin conversion.
    c0 = max(max(abs(quantaE(c["E0"] - darwin(c["p"], c["e"])[0])),
                 abs(quantaL(c["L0"] - darwin(c["p"], c["e"])[1]))) for c in cases)
    out["C0_max_quanta"] = c0

    rows = []
    for c in cases:
        dE, dL = c["Ep"] - c["E0"], c["Lp"] - c["L0"]
        Ed, Ld = darwin(c["p"], c["e"])
        E_stored, L_stored = Ed * Q48, Ld * Q32  # darwin floors; Fraction floor via //
        E_stored, L_stored = F(int(E_stored), Q48), F(int(L_stored), Q32)
        # Arm: round-to-nearest and floor variants of the increment.
        def rnd(x):
            return int(x + F(1, 2)) if x >= 0 else -int(-x + F(1, 2))
        dEq, dLq = dE * Q48, dL * Q32
        arm_r = (E_stored + F(rnd(dEq), Q48), L_stored + F(rnd(dLq), Q32))
        arm_f = (E_stored + F(int(dEq), Q48), L_stored + F(int(dLq), Q32))
        rf = rkey_quanta(*c["refit"])
        if rf is None:
            continue
        Er, Lr = rf
        refit_q = (F(int(Er * Q48), Q48), F(int(Lr * Q32), Q32))
        rows.append(dict(
            p=float(c["p"]), e=float(c["e"]), t=c["t"], d=c["d"],
            scale=c["dvtf"] if c["dvtf"] != 99 else c["dvrf"],
            dE_q=quantaE(dE), dL_q=quantaL(dL),
            arm_vs_refit_E=quantaE(arm_r[0] - refit_q[0]),
            arm_vs_refit_L=quantaL(arm_r[1] - refit_q[1]),
            armf_vs_refit_E=quantaE(arm_f[0] - refit_q[0]),
            armf_vs_refit_L=quantaL(arm_f[1] - refit_q[1]),
            refit_vs_exact_E=quantaE(refit_q[0] - c["Ep"]),
            refit_vs_exact_L=quantaL(refit_q[1] - c["Lp"]),
            arm_moved=(rnd(dEq) != 0 or rnd(dLq) != 0),
            refit_moved=(refit_q[0] != E_stored or refit_q[1] != L_stored),
            arm_bits_same=(rnd(dEq) == 0 and rnd(dLq) == 0),
        ))

    multi = [r for r in rows if abs(r["dE_q"]) >= 1 or abs(r["dL_q"]) >= 1]
    sub = [r for r in rows if abs(r["dE_q"]) < 0.5 and abs(r["dL_q"]) < 0.5]
    tiny = [r for r in rows if r["scale"] == -50]
    def mx(rs, k):
        return max(abs(r[k]) for r in rs) if rs else None
    out["single_kick"] = {
        "n_multi": len(multi),
        "max|arm-refit|_E_q": mx(multi, "arm_vs_refit_E"),
        "max|arm-refit|_L_q": mx(multi, "arm_vs_refit_L"),
        "max|armfloor-refit|_E_q": mx(multi, "armf_vs_refit_E"),
        "max|refit-exact|_E_q": mx(multi, "refit_vs_exact_E"),
        "max|refit-exact|_L_q": mx(multi, "refit_vs_exact_L"),
        "subquantum_n": len(sub),
        "subquantum_arm_moved": sum(r["arm_moved"] for r in sub),
        "subquantum_refit_moved": sum(r["refit_moved"] for r in sub),
        "tiny_n": len(tiny),
        "tiny_arm_bits_same": sum(r["arm_bits_same"] for r in tiny),
        "tiny_refit_bits_same": sum(not r["refit_moved"] for r in tiny),
        "impulse_range_E_q": [min(r["dE_q"] for r in rows), max(r["dE_q"] for r in rows)],
    }

    # The train: integer Q96 simulation of the two rounding policies vs exact truth.
    def train(seed0, N=10_000, seeds=32):
        ck = [1, 10, 100, 1000, 10_000]
        err = {k: [] for k in ck}
        errf = {k: [] for k in ck}
        errR = {k: [] for k in ck}
        errNA = {k: [] for k in ck}
        drift = {"arm": [], "floor": [], "refit": [], "noacc": []}
        for s in range(seeds):
            rng = random.Random(seed0 + s)
            Et = 0          # exact, Q48 quanta scaled by 2^48 -> use Q48 quanta ints *2^48? use quanta*2^0 in Q48 units as ints (exact since draws are quantized)
            # represent exact E offset in units of 2^-96 (Q48 quanta * 2^48)
            E96 = 0
            arm, armf, refit, noacc = 0, 0, 0, 0  # in Q48 quanta (ints)
            for i in range(1, N + 1):
                for ch in ("E",):
                    if rng.random() < 0.5:
                        mag = rng.uniform(0.05, 0.9)   # sub-quantum: accumulator domain
                    else:
                        mag = rng.uniform(0.5, 6.0)
                    d = mag * (1 if rng.random() < 0.5 else -1)
                    d96 = round(d * (1 << 48))         # exact draw in Q96-of-E-units
                E96 += d96
                q = E96 >> 48                          # floor lattice cell (E<1: negative care)
                # refit: re-anchored floor of the exact state each kick
                refit = floor_div(E96, 1 << 48)
                # arm rounded increment
                arm += round_div(d96, 1 << 48)
                armf += floor_div(d96, 1 << 48)
                noacc += round_div(d96, 1 << 48) if abs(d96) >= (1 << 47) else 0
                if i in ck:
                    err[i].append(abs(arm * (1 << 48) - E96) / (1 << 48))
                    errf[i].append(abs(armf * (1 << 48) - E96) / (1 << 48))
                    errR[i].append(abs(refit * (1 << 48) - E96) / (1 << 48))
                    errNA[i].append(abs(noacc * (1 << 48) - E96) / (1 << 48))
        med = lambda v: sorted(v)[len(v) // 2]
        return {
            "N": ck,
            "median|arm-truth|_q": [round(med(err[i]), 2) for i in ck],
            "median|armfloor-truth|_q": [round(med(errf[i]), 2) for i in ck],
            "median|refit-truth|_q": [round(med(errR[i]), 2) for i in ck],
            "median|no-accumulator-truth|_q": [round(med(errNA[i]), 2) for i in ck],
            "sqrtN_half": [round(0.5 * i ** 0.5, 2) for i in ck],
        }

    def floor_div(a, b):
        return a // b
    def round_div(a, b):
        return (a + (b >> 1)) // b if a >= 0 else -((-a + (b >> 1)) // b)

    out["train"] = train(0x29F4)

    # Binding-relative observability at belt keys (from the swept keys).
    obs = []
    for c in cases[::27]:
        Ed, _ = darwin(c["p"], c["e"])
        binding_q = quantaE(F(1) - Ed)
        obs.append(dict(p=float(c["p"]), e=float(c["e"]), binding_E_quanta=binding_q))
    out["binding_scale"] = obs

    json.dump(out, open("analysis.json", "w"), indent=1)
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    main()
