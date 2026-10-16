#!/usr/bin/env python3
"""Analyze the ES_SECULAR flights' end states: the legality domain (measured, cross-checked two
ways), the residual storm's composition, and the B14-class probe (what the freeze drops).

Reads work/states_<arm>_<off>.csv (ES_STATES dumps) and flights/*.txt. Pure arithmetic on the
dumps; prints every number the dossier quotes."""
import math, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.dirname(HERE)

def load(path):
    dolls, srcs, B, fleet = {}, {}, [], set()
    for ln in open(path):
        p = ln.split()
        if not p:
            continue
        if p[0] == 'D':
            dolls[int(p[1])] = dict(name=p[2], parent=None if p[3] == 'None' else int(p[3].strip('Some()').rstrip(')').split('(')[-1]) if p[3].startswith('Some') else None,
                                    shift=int(p[4]), mu=float(p[5]), centre=None if p[6] == 'None' else int(p[6].strip('Some()').rstrip(')').split('(')[-1]) if p[6].startswith('Some') else None,
                                    mass_log2=int(p[7]))
        elif p[0] == 'S':
            srcs.setdefault(int(p[1]), {})[int(p[2])] = float(p[3])
        elif p[0] == 'B':
            B.append(dict(i=int(p[1]), doll=int(p[2]), kind=p[3], plan=int(p[4]), alive=int(p[5]),
                          a=float(p[6]), e=float(p[7]), ang=float(p[8]), r=float(p[9])))
        elif p[0] == 'F':
            fleet.add(int(p[1]))
    return dolls, srcs, B, fleet

TAU0 = 3.6e-3

def legality(dolls, srcs, b, res_on=False):
    """Independent recomputation of ES_SECULAR's rule from the dump's own ingredients."""
    d = dolls[b['doll']]
    host = d['mu']
    a = b['a']
    if b['kind'] != 's' or not (a == a) or a <= 0:
        return False
    if d['parent'] is not None:
        # the parent star: mass ratio 2^-mass_log2 / mu_host; a_host from the centre body
        c = next(x for x in dolls_body if x['i'] == d['centre'])
        a_host = c['a'] if c else None
        # convert a_host (parent doll units) to this doll: x 2^(shift_d - shift_p)
        a_host = a_host * 2.0 ** (d['shift'] - dolls[d['parent']]['shift'])
        m_ratio = 2.0 ** (-d['mass_log2']) / host
        if 3.0 * m_ratio * (a / a_host) ** 3 >= TAU0:
            return False
    for j, gm in srcs.get(b['doll'], {}).items():
        jj = body_by_id[j]
        if jj['i'] == b['i'] or jj['a'] != jj['a']:
            continue
        a_j = jj['a']
        if 3.0 * (gm / host) * (a / a_j) ** 3 >= TAU0:
            return False
        if not res_on:
            if abs(a / a_j - 1.0) < 0.05:
                return False
            pr = (a / a_j) ** 1.5 * math.sqrt(host / (host + gm))
            for q in range(1, 9):
                for r in range(1, 9):
                    if abs(pr / (q / r) - 1.0) < 0.02:
                        return False
    return True

arm = load(os.path.join(HERE, 'states_1900_arm.csv'))
off = load(os.path.join(HERE, 'states_1900_off.csv'))
global dolls_body, body_by_id
dolls_body, body_by_id = arm[2], {x['i']: x for x in arm[2]}

dolls, srcs, B, fleet = arm
sh2 = 2.0 ** dolls[2]['shift']  # doll-2 units -> root: /2^shift... (doll = root x 2^shift)

print("== dolls ==")
for i, d in sorted(dolls.items()):
    print(f"  {i} {d['name']:7s} parent={d['parent']} shift={d['shift']} mu={d['mu']} mass_log2={d['mass_log2']}")
print("sources:", {k: v for k, v in srcs.items()})

# populations
d2 = [b for b in B if b['doll'] == 2 and b['kind'] == 's' and b['i'] not in fleet]
insitu = [b for b in d2 if b['a'] / sh2 < 200_000]
quart = [b for b in d2 if b['a'] / sh2 >= 200_000]
belt = [b for b in B if b['doll'] == 0 and b['kind'] == 's' and b['i'] not in fleet]
print(f"\n== populations (doll 2: {len(d2)} non-fleet ships; fleet {len(fleet)}; doll 0 ships {len(belt)}) ==")
print(f"in-situ {len(insitu)}: arm-deleted {sum(b['plan']==0 for b in insitu)}; python-legal {sum(legality(dolls,srcs,b) for b in insitu)}")
print(f"quarter {len(quart)}: arm-deleted {sum(b['plan']==0 for b in quart)}; python-legal {sum(legality(dolls,srcs,b) for b in quart)}")
print(f"belt    {len(belt)}: arm-deleted {sum(b['plan']==0 for b in belt)}; python-legal {sum(legality(dolls,srcs,b) for b in belt)}")
# cross-check: every non-fleet ship's arm decision == python legality
mism = [b['i'] for b in B if b['kind'] == 's' and b['i'] not in fleet and (b['plan'] == 0) != legality(dolls, srcs, b)]
print(f"cross-check (engine vs python, all {sum(1 for b in B if b['kind']=='s' and b['i'] not in fleet)} non-fleet ships): mismatches = {len(mism)} {mism[:8]}")

# the in-situ tau structure (root units)
R_H = (99_300_000 / (1 - 0.02)) * (2.0 ** -18 / 3.0) ** (1 / 3.0)
lo = 5_200.0
print(f"\n== r9's domain on the in-situ (root units; R_H(Home) = {R_H:.3g}) ==")
for o in range(5):
    aa = [b for b in insitu if lo * 2 ** o <= b['a'] / sh2 < lo * 2 ** (o + 1)]
    if not aa:
        continue
    tstar = max(3.0 * 2.0 ** 18 * (b['a'] / sh2 / (99_300_000 / 0.98)) ** 3 for b in aa)
    tmoon = max(3.0 * 2.0 ** -6 * (b['a'] / sh2 / (260_000 / 0.95)) ** 3 for b in aa)
    print(f"  octave {o} a[{lo*2**o:.0f},{lo*2**(o+1):.0f}) n={len(aa):3d} deleted={sum(b['plan']==0 for b in aa):3d} "
          f"max tau_star={tstar:.2e} max tau_moon={tmoon:.2e}")
# the Moon line
xs = sorted(b['a'] / sh2 for b in insitu if b['plan'] == 0)
legal_top = max((b['a'] / sh2 for b in insitu if b['plan'] == 0), default=0)
illegal = sorted(b['a'] / sh2 for b in insitu if b['plan'] > 0 and b['a'] / sh2 < 200_000)
print(f"in-situ deleted: {len(xs)}/{len(insitu)}; top deleted a = {legal_top:.0f} root units; "
      f"lowest kept in-situ a = {illegal[0] if illegal else -1:.0f}")

# belt resonance bands
G = 500_000_000 / (1 - 0.05)
AU = 101_300_000.0
kept = sorted(b['a'] for b in belt if b['plan'] > 0)
print(f"\n== belt (root units; a in AU) == deleted {len(belt)-len(kept)}/{len(belt)}; kept at AU:", [round(k/AU,3) for k in kept])

# == the B14-class probe: what the freeze drops (angle at identical final tick, arm vs off) ==
offB = {x['i']: x for x in off[2]}
def wrap(x):
    return (x + 180.0) % 360.0 - 180.0
print(f"\n== B14-class probe: |angle(arm) - angle(off)| at the final tick, per octave (doll-2 in-situ) ==")
own_P = lambda a_root: 2 * math.pi * math.sqrt(a_root ** 3 / (2.0 ** -18)) * (1477.0 / 299792458.0)  # s
flight_s = 1900.0 * 100.0  # rtf 100 -> simulated seconds
for o in range(5):
    aa = [b for b in insitu if lo * 2 ** o <= b['a'] / sh2 < lo * 2 ** (o + 1)]
    if not aa:
        continue
    dd = [abs(wrap(b['ang'] - offB[b['i']]['ang'])) for b in aa if b['plan'] == 0]
    if not dd:
        continue
    a_top = lo * 2 ** (o + 1)
    norb = flight_s / own_P(a_top)
    tstar = 3.0 * 2.0 ** 18 * (a_top / (99_300_000 / 0.98)) ** 3
    tmoon = 3.0 * 2.0 ** -6 * (a_top / (260_000 / 0.95)) ** 3
    pred = 0.75 * 2 * math.pi * max(tstar, tmoon)  # rad/orbit
    med = sorted(dd)[len(dd)//2]
    print(f"  octave {o}: n={len(dd)} median Dangle={med:8.3f} deg  max={max(dd):8.3f}  orbits<={norb:6.0f}  "
          f"tau_star={tstar:.1e} tau_moon={tmoon:.1e}  predicted rad/orbit {pred:.2e} -> per-orbit measured {math.radians(med)/max(norb,1):.2e}")
# quarter (spared): must be bit-identical path (same events)
qs = [abs(wrap(b['ang'] - offB[b['i']]['ang'])) for b in quart if b['plan'] > 0]
print(f"  quarter kept {len(qs)}: angle deltas median {sorted(qs)[len(qs)//2] if qs else -1:.4f} deg" if qs else "  quarter: ALL DELETED (check the resonance rule!)")
