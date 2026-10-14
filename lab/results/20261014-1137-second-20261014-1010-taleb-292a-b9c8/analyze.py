import json, sys, collections, statistics as st

rows = json.loads(open(sys.argv[1]).read().replace('},\n]', '}\n]'))
n = len(rows)
Q48 = 1 << 48
E = {0: 0.0, (Q48)//1000: 0.001, (Q48)//10: 0.1, (Q48)//2: 0.5, 9*Q48//10: 0.9, 99*Q48//100: 0.99}
def drel(r, sfx):
    return r[f'dstate_quanta{sfx}'] / float(1 << (60 - r['shift']))
def dwturns(r, sfx):
    return r[f'dw_max{sfx}'] / 2**32
def cls(e):
    return 'circle' if e == 0 else ('near' if e == (Q48)//1000 else 'ecc')

stage = collections.Counter(r['refused'].split(' ', 1)[1].split(':')[0] if r['refused'] != 'None' else 'ok' for r in rows)
print(f"chains={n} depth=256 refusal_stages={dict(stage)}")

done = [r for r in rows if r['refused'] == 'None']
print(f"completed={len(done)}")

# --- headline per phase: boundedness class and drift, depth 64 and 256 ---
print("\n== per true phase (all dolls, all words) ==")
for phi in (1, 3, 5, 7):
    sub = [r for r in done if r['phi'] == phi]
    for tag, sfx, cut in (("64", "64", lambda r: r['unique64'] >= 64), ("256", "", lambda r: r['unique'] >= 256)):
        walk = [r for r in sub if cut(r)]
        cyc = [r for r in sub if r['cycle_at'] is not None and r['cycle_at'] <= (64 if sfx == '64' else 256)]
        d = [drel(r, sfx) for r in walk]
        line = f"phi={phi}/8 d{tag}: walk={len(walk)} cyclic={len(cyc)}"
        if d:
            line += f" drel min/med/max = {min(d):.2e}/{sorted(d)[len(d)//2]:.2e}/{max(d):.2e}"
        print(line)

# --- the near-circle w lottery, per phase (the checker's first question) ---
print("\n== near-circles (e=0, 0.001) per phase, depth 64 ==")
for phi in (1, 3, 5, 7):
    sub = [r for r in done if r['phi'] == phi and cls(r['e_q48']) in ('circle', 'near')]
    dw = [dwturns(r, '64') for r in sub]
    dr_c = [drel(r, '64') for r in sub if r['e_q48'] == 0]
    dr_n = [drel(r, '64') for r in sub if r['e_q48'] != 0]
    print(f"phi={phi}/8: n={len(sub)} per-crossing |dw| max={max(dw):.3f} med={sorted(dw)[len(dw)//2]:.2e} turns | e=0 drift med/max={sorted(dr_c)[len(dr_c)//2]:.2f}/{max(dr_c):.2f} | e=.001 med/max={sorted(dr_n)[len(dr_n)//2]:.2e}/{max(dr_n):.2e}")

# --- circles: position drift vs radius drift (orientation lottery pricing) ---
cir = [r for r in done if r['e_q48'] == 0]
print(f"\ncircles: n={len(cir)} pos drift 256 med/max={sorted(drel(r,'') for r in cir)[len(cir)//2]:.2f}/{max(drel(r,'') for r in cir):.2f} radius drift max={(max(r['dr_rel'] for r in cir))/2**20:.2e} (2^-20 units)")

# --- fixed points and cycles: key-level vs column-level ---
cyc = [r for r in done if r['cycle_at'] is not None]
cyc64 = [r for r in cyc if r['cycle_at'] <= 64]
cyc1 = [r for r in cyc if r['cycle'] == 1]
colfix = [r for r in cyc1 if r['dw_max'] == 0]
keyfix_wob = [r for r in cyc1 if r['dw_max'] > 0]
print(f"\ncycles: total={len(cyc)} closed<=64={len(cyc64)} new in (64,256]={len(cyc)-len(cyc64)}")
print(f"fixed points (cycle_len=1): key-level={len(cyc1)}, column-level (w also fixed)={len(colfix)}")
print(f"  key fixed but w keeps wobbling: {len(keyfix_wob)} chains, |dw| max={max((dwturns(r,'') for r in keyfix_wob), default=0):.2e} turns/crossing")
print("  cycle-length census:", dict(collections.Counter(r['cycle'] for r in cyc)))

# --- word dependence of closure ---
bycfg = collections.defaultdict(dict)
for r in done:
    bycfg[(r['p'], r['e_q48'], r['phi'], r['mu'])][r['shift']] = r
flip = sum(1 for cfg, ss in bycfg.items() if len(ss) == 3 and (any(x['cycle_at'] is not None for x in ss.values()) != all(x['cycle_at'] is not None for x in ss.values())))
allwalk = sum(1 for cfg, ss in bycfg.items() if len(ss) == 3 and all(x['cycle_at'] is None for x in ss.values()))
print(f"\nword-closure flips (some shift closes, another walks): {flip}/{len(bycfg)} (p,e,phi,mu) groups; all-walk groups={allwalk}")
# invariance of the drift where every shift walks
def inv(sfx):
    ratios = []
    for cfg, ss in bycfg.items():
        if len(ss) == 3 and all(x['cycle_at'] is None and x['steps'] >= (64 if sfx == '64' else 256) for x in ss.values()):
            ds = [drel(x, sfx) for x in ss.values()]
            if min(ds) > 0:
                ratios.append(max(ds) / min(ds))
    return ratios
r64 = sorted(inv('64'))
print(f"word-invariance on all-walking groups d64: n={len(r64)} ratio med={r64[len(r64)//2]:.2f} p90={r64[int(len(r64)*0.9)]:.2f} within2x={sum(1 for x in r64 if x <= 2)}/{len(r64)} max={max(r64):.2f}")

# (strong walkers are the hazard class; the record max drift at 256:)
print(f"record max drift d256 = {max(drel(r, '') for r in done if r['cycle_at'] is None):.2f} radii")
print("\n== saturation (walking at 64, no cycle by 256) ==")
sat = []
for r in done:
    if r['unique64'] >= 64 and r['cycle_at'] is None and drel(r, '64') > 0:
        sat.append(drel(r, '') / drel(r, '64'))
print(f"n={len(sat)} ratio d256/d64 min/med/max = {min(sat):.2f}/{sorted(sat)[len(sat)//2]:.2f}/{max(sat):.2f} (linear ~4, bounded ~1)")
strong = [drel(r, '') / drel(r, '64') for r in done if r['unique64'] >= 64 and r['cycle_at'] is None and drel(r, '64') >= 1e-3]
if strong:
    print(f"strong walkers (d64>=1e-3): n={len(strong)} med={sorted(strong)[len(strong)//2]:.2f} max={max(strong):.2f}")

# --- mu vs unity paired ---
print("\n== mu doll vs unity, paired per (p,e,phi,shift) ==")
by_pes = collections.defaultdict(dict)
for r in done:
    by_pes[(r['p'], r['e_q48'], r['phi'], r['shift'])][r['mu']] = r
within2 = tot = 0
mu_smaller = 0
ratio_list = []
for cfg, ss in by_pes.items():
    if '1' in ss and 'x' in ss and ss['1']['cycle_at'] is None and ss['x']['cycle_at'] is None:
        a, b = drel(ss['1'], ''), drel(ss['x'], '')
        if a > 0 and b > 0:
            tot += 1
            ratio_list.append(b / a)
            if 0.5 <= b / a <= 2:
                within2 += 1
            if b < a:
                mu_smaller += 1
if tot:
    print(f"paired walking pairs={tot} within 2x={within2} ({100.0*within2/tot:.0f}%) mu-smaller={mu_smaller} ({100.0*mu_smaller/tot:.0f}%) ratio med={sorted(ratio_list)[len(ratio_list)//2]:.2f} max={max(ratio_list):.2f}")
for mu in ('1', 'x'):
    sub = [r for r in done if r['mu'] == mu]
    d = [drel(r, '') for r in sub if r['cycle_at'] is None]
    print(f"mu={mu}: chains={len(sub)} walking={len(d)} drel256 med={sorted(d)[len(d)//2]:.2e} max={max(d):.2e}")

# --- k column ---
print("\n== k column (Q48 ulps) ==")
dk = [r['dk_max64'] for r in done]
print(f"|dk| per crossing: med={sorted(dk)[len(dk)//2]} max={max(dk)}")
dkf = [r['dk_final64'] for r in done if r['unique64'] >= 64]
print(f"|dk| over 64 (walkers): med={sorted(map(abs, dkf))[len(dkf)//2]} max={max(map(abs, dkf))}")

# --- controls ---
p1 = sum(1 for r in done if r['p1'])
p2 = [r['p2_dk'] for r in done if r['p2_dk'] > 0]
print(f"\nP1 reconstruct exact left inverse: {p1}/{len(done)}")
print(f"P2 kick control: n={len(p2)} min={min(p2)} max={max(p2)} Q48 ulps; zero on {len(done)-len(p2)} arms (p=-1, e=0.001, phi 1,3: fit on the kicked state refuses or moves k<1 ulp)")
