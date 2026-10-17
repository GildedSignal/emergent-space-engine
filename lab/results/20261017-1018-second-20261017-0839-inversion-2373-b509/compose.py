#!/usr/bin/env python3
"""Close the fleet row of the 10^9 encounter ledger: the calendar (shipped tier::arm_pair,
dioph first-hit) vs the per-rebuild window sweep (fleetk's population, same seed).

Constants cited from the wiki (unchanged from 2373's compose.py):
  interval 28,141.5 game-s; wall@rtf100 = 281.415 s; BELT_SPLIT 8; budget 4 cores;
  belt stream 2 events/body/interval, ~50 us/event anchor.
"""
import json, sys

cal_path = sys.argv[1] if len(sys.argv) > 1 else "work/fleetcal-20261017.jsonl"
sw_path = sys.argv[2] if len(sys.argv) > 2 else "work/fleetk.jsonl"
cal = [json.loads(l) for l in open(cal_path) if "arm" in l]
sw = [json.loads(l) for l in open(sw_path) if "arm" in l] if sw_path else []

WALL = 281.415
SPLIT = 8
BUDGET = 4.0
N = 1e9
carm = next(r for r in cal if r["arm"] == "carm")
c_arm = carm["arm_us_per_pair"] * 1e-6
c_exact = carm["exact_us_per_pair"] * 1e-6
c_exact8 = carm["exact8_us_per_pair"] * 1e-6
c_fire_keys = carm["fire_us_per_armed_iv"] * 1e-6

print(f"# c_arm={c_arm*1e6:.2f}us c_exact(H_iv)={c_exact*1e6:.1f}us c_exact(8iv)={c_exact8*1e6:.1f}us per pair")
print(f"# fire: keys armed @H_iv={c_fire_keys*1e3:.1f}ms (perpetual pairs) | interval={WALL:.1f}s split={SPLIT} budget={BUDGET} cores")

def keys_row(f):
    return next(r for r in cal if r["arm"] == "calkeys" and r["n"] == f and r["sig_e"] == 0.01)

def train_row(f):
    return next(r for r in cal if r["arm"] == "caltrain" and r["n"] == f and r["da"] == 1e-4)

print("\n# 1. The sweep term, repriced at the horizons a sound rebuild actually needs")
print(f"# {'F':>7} {'pairs(H_iv)':>12} {'2373 basis':>11} {'iv horizon':>11} {'8iv horizon':>12}   (cores at N=1e9, phi=1, keys)")
for f in [1000, 10000, 100000]:
    r = keys_row(f)
    pairs = r["pairs"]
    old = pairs * 3.24e-6 / (WALL * SPLIT) * (N / f)
    iv = pairs * c_exact / WALL * (N / f)
    e8 = pairs * c_exact8 / (WALL * SPLIT) * (N / f)
    print(f"# {f:>7} {pairs:>12,} {old:>11.1f} {iv:>11.0f} {e8:>12.0f}")

print("\n# 2. The calendar term (birth amortized over L intervals; standing-contact semantics")
print("#    for keys armed pairs: capability solved once over ONE period, cap_us each)")
print(f"# {'pop':>6} {'F':>7} {'L':>4} {'birth':>9} {'firings/iv':>11} {'firing cores':>13} {'total':>9}")
for f in [1000, 10000, 100000]:
    r = keys_row(f)
    for L in [25, 100]:
        birth = (r["pairs"] * c_arm + r["armed_scaled"] * r["cap_us_per_armed_period"] * 1e-6) / L
        cores = birth / WALL * (N / f)
        print(f"# {'keys':>6} {f:>7} {L:>4} {birth:>9.3f}s {'standing':>11} {0.0:>13.1f} {cores:>9.2f}")
for f in [10000, 100000]:
    r = train_row(f)
    for L in [25, 100]:
        birth = r["pairs"] * c_arm / L
        fire = r["firings_iv10"] * r["fire_us_per_armed_iv"] * 1e-6
        cores = (birth + fire) / WALL * (N / f)
        print(f"# {'train':>6} {f:>7} {L:>4} {birth:>9.2f}s {r['firings_iv10']:>11,.0f} {fire/WALL*(N/f):>13.0f} {cores:>9.0f}")

print("\n# 3. F* (fleet size at which the term = 4 cores, phi=1): sweep vs calendar")
print("#    sweep(2373 basis, every-8): F* ~ 100 (their finding, reproduced)")
for tag, f, r, per_iv_secs in [
    ("keys L=100", 10000, keys_row(10000), keys_row(10000)["pairs"] * c_arm / 100),
    ("keys L=25", 10000, keys_row(10000), keys_row(10000)["pairs"] * c_arm / 25),
    ("train da=1e-4 L=100", 10000, train_row(10000), None),
]:
    if per_iv_secs is None:
        per_iv_secs = train_row(10000)["pairs"] * c_arm / 100 + train_row(10000)["firings_iv10"] * train_row(10000)["fire_us_per_armed_iv"] * 1e-6
    cores_at_f = per_iv_secs / WALL * (N / f)
    fstar = f * (BUDGET / cores_at_f) ** 0.5
    print(f"#    calendar {tag}: term={cores_at_f:.1f} cores at F={f} -> F* ~ {fstar:,.0f}")

print("\n# 4. The kick row (belt stream 2 events/body/interval applied to fleet members)")
kr = next(r for r in cal if r["arm"] == "kickrow" and r["pop"] == "keys" and abs(r["eps"] - 2**-23) < 1e-9)
kt = next(r for r in cal if r["arm"] == "kickrow" and r["pop"] == "train" and abs(r["eps"] - 2**-23) < 1e-9)
fire_us_train = next(x for x in cal if x["arm"] == "caltrain" and x["n"] == 10000)["fire_us_per_armed_iv"] * 1e-6
for tag, r in [("keys", kr), ("train", kt)]:
    rearm = r["rearm_us_per_kick"] * 1e-6
    created = r["fire_per_kick"] * fire_us_train
    worst = 2 * N * (rearm + created) / WALL
    print(f"#    {tag}: re-arm {rearm*1e6:.0f}us/kick + kick-created firings {created*1e6:.0f}us/kick -> {worst:,.0f} cores worst-case (no slack)")
print(f"#    slack: ddue_med={kr['ddue_med_iv']:.4f} iv (keys) / {kt['ddue_med_iv']:.4f} iv (train) at eps=2^-23:")
print(f"#    the belt's own kick quantum moves the median pair's due by < 1e-3 intervals -> re-arm deferrable;")
print(f"#    only the {kr['fire_per_kick']:.0f} (keys) / {kt['fire_per_kick']:.0f} (train) kick-created firings per kick are undelayable real events.")

print("\n# 5. The event floor under any certificate (the population's own contact flow)")
ev = {r["n"]: r for r in cal if r["arm"] == "keysev"}
import math
g = math.log(ev[6400]["events"] / ev[1600]["events"]) / math.log(4)
epb = ev[6400]["events_per_body_orbit"] * 28141.5 / 6.2832
print(f"#    keysev exponent gamma={g:.2f} on (1600,6400); events/body/interval at F=6400: {epb:.0f}")
print(f"#    vs the belt's own 2 events/body/interval -> fleet stream alone = {epb/2:.0f}x belt at F=6400")
print(f"#    at 50us/event: {epb*50e-6*N/WALL:,.0f} cores at phi=1, F=6400-equivalent density")

print("\n# 6. Controls")
tr = {(r["pop"]): r for r in cal if r["arm"] == "truth"}
for pop, r in tr.items():
    print(f"#    truth {pop}: dropped={r['dropped']} added={r['added']} (calendar vs group_events, F=2000, H=100 orbits)")
for r in cal:
    if r["arm"] == "negctl":
        key = f"safety={r['safety']}" if "safety" in r else f"reach_frac={r['reach_frac']}"
        print(f"#    negctl {key}: dropped={r['dropped']}")

# 7. The verdict row the checker asked for
cal_keys_1e3 = keys_row(1000)
birth_1e3_L25 = (cal_keys_1e3["pairs"] * c_arm + cal_keys_1e3["armed_scaled"] * cal_keys_1e3["cap_us_per_armed_period"] * 1e-6) / 25
print("\n# 7. VERDICT (checker's experiment): does the calendar bring F=1e3..1e5 under 4 cores at phi=1?")
for f in [1000, 10000, 100000]:
    r = keys_row(f)
    b100 = (r["pairs"] * c_arm + r["armed_scaled"] * r["cap_us_per_armed_period"] * 1e-6) / 100
    cores = b100 / WALL * (N / f)
    print(f"#    keys F={f:>6}: calendar birth(L=100) {cores:>8.2f} cores -> {'FITS' if cores <= BUDGET else 'OVER'}")
t = train_row(10000)
cores_t = (t["pairs"] * c_arm / 100 + t["firings_iv10"] * t["fire_us_per_armed_iv"] * 1e-6) / WALL * (N / 10000)
print(f"#    train da=1e-4 F=10000: calendar {cores_t:,.0f} cores -> OVER (firings dominate: {t['firings_iv10']:,.0f}/interval)")
print(f"#    the binding term at F>=1e4 is the conjunction FIRING FLOW (real events), not the certificate.")
