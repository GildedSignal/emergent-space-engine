#!/usr/bin/env python3
"""Adjudicate the nladder conflict: is ea91's heavy-tailed surprise census an intrinsic
per-body tail (rule 2 lives) or manufactured by the compiled period ladder + promotion
transient + driver head (7497's reading)?

Inputs: the two prior runs' saved data (checked out from their result branches by
regen.sh into ea91/ and p7497/) plus this run's held-out censuses (census-hoA.json,
census-ho1rep.json, census-hoB.json, produced by regen.sh from shipped code).
Output: every table in dossier.md.
"""
import json, os
import numpy as np
from scipy import stats as st

HERE = os.path.dirname(os.path.abspath(__file__))
TPS = None  # ticks per game-second, derived from the roster's own fields

def gini(x):
    x = np.sort(np.asarray(x, float)); n = len(x)
    return float((2*np.arange(1, n+1)-n-1).dot(x)/(n*x.sum())) if n and x.sum() else float('nan')

def zipf(x):
    c = np.sort(np.asarray(x, float))[::-1]; c = c[c > 0][:int(0.9*len(c))]
    return float(np.polyfit(np.log(np.arange(1, len(c)+1)), np.log(c), 1)[0]) if len(c) >= 3 else float('nan')

def roster_rates():
    global TPS
    rows = [json.loads(l) for l in open(f'{HERE}/p7497/idle-s1-m48.jsonl')]
    rows = [r for r in rows if r.get('body') is not None]
    nat = [r for r in rows if r['body'] < 28]
    r0 = nat[0]
    TPS = r0['kicks_per_sec']*r0['period_ticks']/r0['kicks_per_orbit']
    return np.array([r['kicks_per_sec'] for r in nat])

def load(tag, prior=False):
    sub = f'{HERE}/ea91' if prior else HERE
    d = json.load(open(f'{sub}/census-{tag}.json'))
    s = d['surprise']
    items = np.array([float(x or 0) for x in s['items']])
    kicks = np.array([float(x or 0) for x in s['kicks']])
    member = np.array([bool(x) for x in s['from_member']])
    alive = np.array([bool(x) for x in s['alive']])
    half = np.array([float(x or 0) for x in (s['half_items'] or [])])
    h2 = items.copy(); h2[:len(half)] -= half
    T = d['cut_tick']/TPS
    return d, items, kicks, member, alive, h2, T

rates = roster_rates()
print(f"roster: ticks/game-s={TPS:.0f}, native rate ladder {rates.max():.4f}..{rates.min():.2e} ({rates.max()/3e-5:.0f}:1)")

print("\n== Table 1: the census decomposed (ea91's saved scenes; model = roster-rate x T for natives, measured counts for members)")
for tag in ['tune', 'ho1', 'ho2']:
    d, items, kicks, member, alive, h2, T = load(tag, prior=True)
    nat = ~member
    pred = rates*T
    model = np.concatenate([pred*(items[nat].sum()/max(kicks[nat].sum(), 1)), items[member]])
    rho = st.spearmanr(kicks[nat][:28], pred).statistic
    print(f"{tag}: T={T:5.0f}gs G_all={gini(items):.3f} (model {gini(model):.3f}) | G(nat) items/kicks={gini(items[nat]):.3f}/{gini(kicks[nat]):.3f} vs roster-pred {gini(pred):.3f} | rho={rho:.3f} | members alive {int((member&alive).sum())} dead {int((member&~alive).sum())}")

print("\n== Table 2: same-rate determinism (native counts, kicks; ea91 saved scenes + held-out)")
for tag, prior in [('tune', True), ('ho1', True), ('ho2', True), ('ho1rep', False), ('hoA', False), ('hoB', False)]:
    d, items, kicks, member, alive, h2, T = load(tag, prior)
    nk = kicks[~member][:28]
    print(f"{tag:7s} T={T:6.0f} orb1,2=({nk[16]:.0f},{nk[17]:.0f}) orb3-5=({nk[18]:.0f},{nk[19]:.0f},{nk[20]:.0f}) sk2,3=({nk[25]:.0f},{nk[26]:.0f}) player={nk[27]:.0f}")

print("\n== Table 3: held-out scorecard")
d, items, kicks, member, alive, h2, T = load('hoA')
nat_items = items[~member][:28]
rhoA = st.spearmanr(nat_items, rates*T).statistic
deadA = (member&~alive).sum()/member.sum()
print(f"A (seed 11 m120 55s): G_all={gini(items):.3f} in [.64,.78]? {0.64<=gini(items)<=0.78} | G(nat)={gini(nat_items):.3f} in [.70,.78]? {0.70<=gini(nat_items)<=0.78} | rho={rhoA:.3f}>=0.93? {rhoA>=0.93} | dead frac={deadA:.2f} in [.45,.70]? {0.45<=deadA<=0.70} | alive h2 med={np.median(h2[member&alive]):.0f}<=5? {np.median(h2[member&alive])<=5}")
d1, i1, k1, m1, a1, h21, T1 = load('ho1rep')
d, items, kicks, member, alive, h2, T = load('hoB')
nB = items[~member][:28]; n1 = i1[~m1][:28]
print(f"B (seed 3 m400 rtf200 55s, T={T:.0f}): orb12 {nB[16]:.0f},{nB[17]:.0f} = 2x({n1[16]:.0f},{n1[17]:.0f})? {abs(nB[16]/max(n1[16],1)-2)<0.05} | orb345 {nB[18]:.0f},{nB[19]:.0f},{nB[20]:.0f} = 2x{n1[18]:.0f}? {abs(nB[18]/max(n1[18],1)-2)<0.05} | G(nat)={gini(nB):.3f} band [.716,.756]? {0.716<=gini(nB)<=0.756} (player {nB[27]:.0f} vs 2x{n1[27]:.0f}: schedule-bound) | G_all={gini(items):.3f} vs predicted <{gini(i1):.3f}: {'held' if gini(items)<gini(i1) else 'FAILED (rose; per-second rate '+f'{items.sum()/T:.1f}/s vs {i1.sum()/T1:.1f}/s amortized)'} | zipf={zipf(items):.2f} in [-2.3,-1.5]? {-2.3<=zipf(items)<=-1.5}")

print("\n== Table 4: counter choice (items vs kicks) changes nothing")
for tag, prior in [('ho1', True), ('hoA', False), ('hoB', False)]:
    d, items, kicks, member, alive, h2, T = load(tag, prior)
    print(f"{tag:7s} G_all items={gini(items):.3f} kicks={gini(kicks):.3f} | zipf items={zipf(items):.2f} kicks={zipf(kicks):.2f}")
