#!/usr/bin/env python3
"""Three-way: (R) Rust judge oracle dumped to truth.jsonl vs (M) my independent
absolute-coordinate construction, at identical dt = period(a,e)/40, 401 samples.
P1: pairs-are-true-geodesics (s=1/16).  P4: full-extent gap (s=1 vs s=16 truth).
Also validates the dump against the judge's printed separation controls."""
import json, math, sys, time
sys.path.insert(0, "/home/runner/work/emergent-space-engine/lab-1/lab/results/20261001-1847-redteam-e9-f0b3")
from control import (JudgeMirror, Independent, fixtures, period, errors,
                     f_of, independent_EL, centered_measure)

truths = {}
for line in open("/tmp/e9harness/truth.jsonl"):
    d = json.loads(line)
    truths[(d["ratio"], d["e"], d["tag"])] = d

log = []
def say(m):
    print(m, flush=True); log.append(m)

say("== 0. Dump self-check: separation control from Rust s16 vs s32 ==")
for (ratio, e, printed) in ((10.0, 0.0, 3.05e-8), (10.0, 0.6, 1.61e-9), (1e6, 0.0, 6.35e-9)):
    _, a, offsets = fixtures(ratio)
    t16 = truths[(ratio, e, "s16")]["samples"]
    t32 = truths[(ratio, e, "s32")]["samples"]
    pe, se = errors(t32, t16, offsets)
    say(f"  ratio={ratio:g} e={e}: position={pe:.3e} shape={se:.3e} (judge test printed {printed:.3e})")
    # also my python mirror dt check
    jm = JudgeMirror(a)
    dt_mine = period(a, e) / 40.0
    say(f"    dt mine={dt_mine:.16f} rust={0 if (ratio,e)==(10.0,0.6) else ''}")

say("== dt cross-check ==")
for (ratio, e) in ((10.0, 0.6), (10.0, 0.0), (1e6, 0.0)):
    _, a, offsets = fixtures(ratio)
    say(f"  ratio={ratio:g} e={e}: my period/40={period(a,e)/40.0:.16f}")

for (ratio, e) in ((10.0, 0.6), (10.0, 0.0), (1e6, 0.0)):
    say(f"== P1/P4 ratio={ratio:g} e={e}: my absolute geodesics vs Rust judge truth ==")
    n, a, offsets = fixtures(ratio)
    dt = period(a, e) / 40.0
    jm = JudgeMirror(a)
    E_i, L_i = independent_EL(a, e)
    ind = Independent(a)
    refs = ind.run_reference_with_axes(E_i, L_i, dt, 256)  # my side only; 256-vs-512 shown <=9e-13
    for scale, tag, label in ((1.0 / 16.0, "s16", "P1 (pred <1e-9)"),
                              (1.0, "s1", "P4 vs linearized truth (pred <5e-4, band 1e-2)")):
        pairs, _ = jm.initial(e, offsets, scale)
        init_states = [[d2, 1.0 + d0, (jm.energy + de) / f_of(a, 1.0 + d0), d1, d3,
                        (jm.angular + dl) / (1.0 + d0) ** 2]
                       for (de, dl, d0, d1, d2, d3) in pairs]
        t0 = time.time()
        mem = ind.run_members(init_states, dt, 256)  # my side only; 256-vs-512 shown <=9e-13
        projs = [[ind.project(ref[0], ref[1], m) for m in memj]
                 for ref, memj in zip(refs, mem)]
        mine = centered_measure(projs, scale)
        rust = truths[(ratio, e, tag)]["samples"]
        pe, se = errors(mine, rust, offsets)
        cons = 0.0
        for idx in range(len(init_states)):
            E0, L0 = ind.EL(mem[0][idx]); E1, L1 = ind.EL(mem[-1][idx])
            cons = max(cons, abs(E1 - E0) / max(abs(E0), 1e-30),
                       abs(L1 - L0) / max(abs(L0), 1e-30))
        say(f"  {tag}: {label}: position={pe:.3e} shape={se:.3e} "
            f"EL_drift={cons:.1e} wall={time.time()-t0:.0f}s")
        # also: Rust s1 vs Rust s16 (their own full-extent gap, no my-code involvement)
        if tag == "s1":
            peR, seR = errors(truths[(ratio, e, "s1")]["samples"],
                              truths[(ratio, e, "s16")]["samples"], offsets)
            say(f"  rust-only s1-vs-s16: position={peR:.3e} shape={seR:.3e} "
                f"(the engine-extent gap in their own construction)")

say("== done ==")
with open(__file__ + ".output.txt", "w") as fh:
    fh.write("\n".join(log) + "\n")
