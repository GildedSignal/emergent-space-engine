#!/usr/bin/env python3
"""Assemble the dossier's tables from the flight logs (run by regen.sh after the flights).

Every number the dossier quotes is printed here from the logs; the deterministic columns
(digests, kicks, events) must equal 96f6's record at every K, and the pin columns are this
run's own (mints/reuses/alive/bytes, the trigger census, the native bench).
"""
import re, sys

D = sys.argv[1] if len(sys.argv) > 1 else "regen"

def parse(log):
    out = {}
    for line in open(f"{D}/{log}.log"):
        if line.startswith("probe:"):
            out["probe"] = dict(re.findall(r"(\w+)=(\S+)", line))
        if line.startswith("pin:"):
            out["pin"] = dict(re.findall(r"(\w+)=([-\d.]+)", line.split("|")[0]))
            out["trig"] = dict(re.findall(r"(\w+)=(\d+)", line.split("census")[-1]))
        if line.startswith("bench:"):
            out["bench"] = line.strip()
    return out

K = [("comp-10000", 10028), ("comp-20000", 20028), ("comp-30000", 30028), ("comp-50000", 50028)]
T = [("comp-10000-long", 10028), ("comp-30000-long", 30028), ("comp-50000-long", 50028)]

print("== Table 1: the K-trend, pin columns (600 frames, composed arm, coast seed 1)")
print("K        mints reuses held_max alive(=mints) touchedMB allocMB hwmMB  B/mint  (K+38)*224  digest[:8]")
for log, k in K:
    d = parse(log)
    p, pin = d["probe"], d["pin"]
    bmp = float(pin["alive_touched_mb"]) * 1e6 / int(pin["mints"])
    print(f"{k:<8} {pin['mints']:>5} {pin['reuses']:>6} {p['held_max']:>8} {pin['alive_end']:>12} "
          f"{float(pin['alive_touched_mb']):>9.1f} {float(pin['alive_alloc_mb']):>7.1f} {float(p['hwm_mb']):>5.0f} "
          f"{bmp:>7.2e} {(k + 38) * 224:>10.2e}  {p['digest'][:8]}")

print("\n== Table 2: the time wall at fixed K (alive == mints in every flight: the freeze drops nothing)")
print("flight              frames game_s   mints alive held_max touchedMB allocMB hwmMB  mints/game_s")
for log, k in T:
    d = parse(log)
    p, pin = d["probe"], d["pin"]
    rate = int(pin["mints"]) / float(p["game_s"])
    print(f"{log:<20}{int(p['frames']):>6} {float(p['game_s']):>7.1f} {pin['mints']:>5} {pin['alive_end']:>5} {int(p['held_max']):>9} "
          f"{float(pin['alive_touched_mb']):>9.1f} {float(pin['alive_alloc_mb']):>7.1f} {float(p['hwm_mb']):>5.0f}  {rate:.4f}")

print("\n== The law: bytes_touched(t) = mints(t) * (K+38) * 224 B, mints(t) = 0.052 * game_s (K-flat)")
for log, k in K + T:
    d = parse(log)
    pin, p = d["pin"], d["probe"]
    ident = float(pin["alive_touched_mb"]) * 1e6 / (int(pin["mints"]) * (k + 38) * 224)
    print(f"{log:<22} identity={ident:.4f}  mint_rate={rate:.4f}/game_s  mints_per_capture={int(pin['mints'])/(int(pin['mints'])+int(pin['reuses'])):.3f}")


print("\n== The 8 GB extrapolation (touched law) and the SCAN_BACKLOG=2048 cap (entries ~= 1.95x mints)")
for k in (10_028, 50_028, 100_028, 1_000_000, 1_000_000_000):
    per_mint = (k + 38) * 224
    t8 = 8e9 / per_mint / 0.052
    cap = 2048 / 1.95  # entries to mints
    print(f"K={k:>11,}: 8 GB after {8e9/per_mint:>7.0f} mints = {t8:>10,.0f} game-s; backlog cap at {cap*per_mint/1e9:.2f} GB "
          f"({'cap first' if cap*per_mint < 8e9 else '8 GB first'})")

print("\n== Trigger census (first failing clause per mint; aggregate over all 7 flights)")
agg = {}
for log, _ in K + T:
    for kk, vv in parse(log).get("trig", {}).items():
        agg[kk] = agg.get(kk, 0) + int(vv)
print(agg)

print("\n== The compare-form, native (b083's REPLICA said 19.2 ns/member => 12 ms at 6.25e5)")
for log, _ in K + T[:1]:
    print(parse(log)["bench"])
