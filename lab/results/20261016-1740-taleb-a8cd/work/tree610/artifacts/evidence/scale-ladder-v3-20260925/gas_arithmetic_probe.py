# Tiny trapped gas with EXACT fractions, engine-style: move one tick, then bounce every
# overlapping approaching pair (equal masses, elastic) and reflect off the walls.
from fractions import Fraction as F
import random, time
def run(n=16, L=24, ticks=400, quant=None, seed=1, limit=60):
    start=time.time()
    random.seed(seed)
    P=[]; V=[]
    while len(P)<n:
        p=[F(random.randint(2,L-2)),F(random.randint(2,L-2))]
        if all((p[0]-q[0])**2+(p[1]-q[1])**2>4 for q in P):
            P.append(p); V.append([F(random.randint(-256,256),1024),F(random.randint(-256,256),1024)])
    def snap(x):  # optional velocity lattice with denominator quant (round half to even)
        return F(round(x*quant),quant) if quant else x
    E0=sum(v[0]**2+v[1]**2 for v in V); hits=0; out=[]
    for t in range(1,ticks+1):
        for p,v in zip(P,V): p[0]+=v[0]; p[1]+=v[1]
        for i in range(n):
            for j in range(i+1,n):
                d=[P[j][0]-P[i][0],P[j][1]-P[i][1]]; dd=d[0]**2+d[1]**2
                w=[V[j][0]-V[i][0],V[j][1]-V[i][1]]; dot=d[0]*w[0]+d[1]*w[1]
                if dd<=4 and dot<0:
                    k=dot/dd; hits+=1
                    for c in (0,1):
                        dv=k*d[c]; V[i][c]=snap(V[i][c]+dv); V[j][c]=snap(V[j][c]-dv)
        for p,v in zip(P,V):
            for c in (0,1):
                if (p[c]<1 and v[c]<0) or (p[c]>L-1 and v[c]>0): v[c]=-v[c]
        slow = time.time()-start > limit
        if t % 10 == 0 or slow:
            bits=max(max(x.denominator.bit_length(),x.numerator.bit_length()) for v in V for x in v)
            pbits=max(max(x.denominator.bit_length(),x.numerator.bit_length()) for p in P for x in p)
            E=sum(v[0]**2+v[1]**2 for v in V)
            print("  tick %4d  bounces %5d  largest velocity number %7d bits  position %7d bits  energy ratio %.6f  (%.1fs)" % (t,hits,bits,pbits,float(E/E0),time.time()-start), flush=True)
            if slow: print('  stopped: time limit', flush=True); return out
    return out
for q in (None, 1024):
    print("exact fractions" if q is None else f"velocities snapped to 1/{q}", flush=True); r=run(quant=q)
