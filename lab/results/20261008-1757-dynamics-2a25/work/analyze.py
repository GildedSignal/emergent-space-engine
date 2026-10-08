#!/usr/bin/env python3
"""Analysis for run 20261008-1757-dynamics-2a25: the plane's event-demand attractor,
the burn wake, and the per-frame budget bifurcation. Inputs: the CSVs written by
`cargo run --release -p emergent-universe --example stream -- SECONDS RTF SEED MEMBERS BUDGET OUT.csv`."""
import csv, math, statistics as st, random, sys

WANT = 338375  # ticks per frame at rtf 100 (60 fps)
def load(fn): return list(csv.DictReader(open(fn)))
def pct(x, q): y = sorted(x); return y[int(q*(len(y)-1))]

rows = load('main.csv'); n = len(rows)
ev  = [int(r['events']) for r in rows]
fl  = [int(r['fleet']) for r in rows]
BUR = [30, 36, 887, 893, 2660, 2666, 3547, 3550]  # frame of each scripted burn's first effect

print("== attractor ==")
for i, (a, b) in enumerate([(60,850),(940,2650),(2700,3540),(3600,6599)]):
    print("segment %d (frames %d-%d): mean %.3f  fleet-slice share %.2f" % (i,a,b,st.mean(ev[a:b]), st.mean(fl[a:b])/st.mean(ev[a:b])))
era = ev[3600:6599]
print("attractor: mean %.2f p50 %d p99 %.0f max %d  burst p99/p50 %.1f" %
      (st.mean(era), pct(era,.5), pct(era,.99), max(era), pct(era,.99)/max(1,pct(era,.5))))

print("== spectrum (attractor era) ==")
m = len(era); mu = st.mean(era); x = [v-mu for v in era]; tot = sum(v*v for v in x)
def dft(y, K=600):
    N = len(y); out = []
    for k in range(1, K):
        c = sum(y[t]*math.cos(2*math.pi*k*t/N) for t in range(N))
        s = sum(y[t]*math.sin(2*math.pi*k*t/N) for t in range(N))
        out.append((k, 2*(c*c+s*s)/N))
    return out
sp = sorted(dft(x), key=lambda p: -p[1])
random.seed(1); sh = era[:]; random.shuffle(sh)
sps = sorted(dft([v-st.mean(sh) for v in sh]), key=lambda p: -p[1])
print("top-16 harmonic variance share %.3f (shuffled control %.3f)" % (sum(p[1] for p in sp[:16])/tot, sum(p[1] for p in sps[:16])/tot))
print("top periods (frames):", [(round(m/p[0],1), round(p[1]/tot,3)) for p in sp[:5]])

print("== wake (per burn; baseline = mean of frames -40..-10) ==")
for name, f in zip(['b1','b2','b3','b4','b5','b6','b7','b8'], BUR):
    base = st.mean(ev[max(0,f-40):max(1,f-10)]); w = ev[f:f+30]
    print(" %s frame %4d base %.2f  spikes>3: %s  net excess(30 frames) %+.0f  late(+9..+29) %+.2f" %
          (name, f, base, [(i, v-base) for i, v in enumerate(w) if v-base > 3], sum(v-base for v in w), st.mean(w[9:])-base))
random.seed(2)
sums = [sum(v-st.mean(ev[f-40:f-10]) for v in ev[f:f+30]) for f in (3547, 3550)]
cl = sorted(sum(ev[f:f+30])-sum(ev[f-40:f-10]) for f in (random.randrange(3640, 6500) for _ in range(400)))
print("flat-era burns b7/b8 net excess(30): %s | control: mean %+.1f p95 %+.0f p05 %+.0f" %
      (["%+.0f" % s for s in sums], st.mean(cl), cl[int(.95*len(cl))], cl[int(.05*len(cl))]))

print("== N and rtf scaling (attractor era) ==")
for fn in ['n6.csv','main.csv','n192.csv','r1000.csv']:
    e = [int(q['events']) for q in load(fn)][3600:6599]
    print(" %-9s mean %.2f p50 %d p99 %.0f max %d burst %.1f" % (fn, st.mean(e), pct(e,.5), pct(e,.99), max(e), pct(e,.99)/max(1,pct(e,.5))))

print("== budget bifurcation (rtf 100; attractor mean 3.40 events/frame) ==")
for b in [2,3,4,6,8,16,32,64]:
    try: r = load(f'b{b}.csv')
    except FileNotFoundError: continue
    lag = [int(q['target'])-int(q['now']) for q in r]; fr = len(r)
    if fr < 6600:
        slope = (lag[-1]-lag[fr//2])/(fr-fr//2)
        print(" b%-2d DIVERGED at frame %d, lag %.0f frames, slope %.2f frames/frame" % (b, fr, lag[-1]/WANT, slope/WANT))
    else:
        nows = [int(q['now']) for q in r]
        rtf = (nows[-1]-nows[400])*4.925490947e-6/((fr-400)/60.0)
        print(" b%-2d bounded: max lag %.1f frames at frame %d, final 0, realized rtf %.1f" % (b, max(lag)/WANT, lag.index(max(lag)), rtf))
