import sys, math, heapq, json
import numpy as np
import probe_slack as P

def run2(pols, lam, seed):
    r, N, A, E, W, Mc, Nc, ii, jj, cand = P.init(seed)
    P.CAND_G = cand
    Kk = np.zeros(N, np.int64)
    for p in pols:
        p.__init__(p.name, p.mode, p.m, p.R, p.eta)
        for i in range(N): p.rebuild(i, 0.0, Mc, A, Nc, Kk)
    phi_prev = (Mc[ii] - Mc[jj]) % (2*np.pi); ev = 0; quanta=[]
    for step in range(P.NSTEPS):
        t = step*P.DT; te = t+P.DT
        Mc = (Mc + Nc*P.DT) % (2*np.pi)
        phi = (Mc[ii]-Mc[jj]) % (2*np.pi)
        cross = np.where(np.abs(phi-phi_prev) > np.pi)[0]
        for idx in cross:
            i, j = int(ii[idx]), int(jj[idx])
            Mi = Mc[i]
            Ei = Mi + E[i]*math.sin(Mi)
            Ei -= (Ei - E[i]*math.sin(Ei) - Mi)/(1 - E[i]*math.cos(Ei))
            fi = 2*math.atan2(math.sqrt(1+E[i])*math.sin(Ei/2), math.sqrt(1-E[i])*math.cos(Ei/2))
            Ej = Mi + E[j]*math.sin(Mi)
            Ej -= (Ej - E[j]*math.sin(Ej) - Mi)/(1 - E[j]*math.cos(Ej))
            fj = 2*math.atan2(math.sqrt(1+E[j])*math.sin(Ej/2), math.sqrt(1-E[j])*math.cos(Ej/2))
            ri = A[i]*(1-E[i]*math.cos(Ei)); rj = A[j]*(1-E[j]*math.cos(Ej))
            if math.hypot(ri*math.cos(fi+W[i])-rj*math.cos(fj+W[j]),
                          ri*math.sin(fi+W[i])-rj*math.sin(fj+W[j])) < P.TAU_CLOSE:
                ev += 1; quanta.append(int(Kk[i]+Kk[j]))
                for p in pols:
                    if p.caught(i, j, te, Nc): continue
                    p.miss += 1
                    if (p.Tc[i,j] > 0) or (p.Tc[j,i] > 0): p.stale += 1
                    else: p.struct += 1
        phi_prev = phi
        if lam > 0:
            hit = r.random(N) < lam*P.DT
            for i in np.flatnonzero(hit):
                s = r.choice([-1,1],3)
                A[i]+=s[0]*1e-4; E[i]+=s[1]*1e-3; W[i]+=s[2]*1e-2
                Nc[i]=2*np.pi*A[i]**(-1.5); Kk[i]+=1
        for p in pols:
            if p.mode in ("quantum","disp"):
                thr = p.m if p.mode=="quantum" else P.M_D
                due = np.flatnonzero((Kk-p.Kr)>=thr) if (lam>0) else []
                for i in due: p.rebuild(i, te, Mc, A, Nc, Kk)
            if p.mode in ("cad","disp"):
                while p.heap and p.heap[0][0] <= te:
                    _, i = heapq.heappop(p.heap)
                    p.rebuild(i, te, Mc, A, Nc, Kk)
    return ev, quanta

def rec(p, ev, N=400):
    return dict(rebuilds=int(p.rebuilds), renewals=int(p.renewals),
                cert_builds=int(p.rebuilds*P.K+p.renewals),
                per_body_orbit=round(p.rebuilds/(N*P.ORBITS),4),
                misses=int(p.miss), struct=int(p.struct), stale=int(p.stale), close_events=ev)

if __name__ == "__main__":
    which = sys.argv[1]
    if which == "nokick":
        pols=[P.Pol("nokick_B8","quantum",8)]
        ev,q = run2(pols, 0.0, 11)
    elif which.startswith("C,"):
        R = float(which[2:])
        pols=[P.Pol("C","cad",R=R)]
        ev,q = run2(pols, 2.0, 11)
    elif which.startswith("B,"):
        ms=[int(x) for x in which[2:].split(",")]
        pols=[P.Pol(f"B{m}","quantum",m) for m in ms]
        ev,q = run2(pols, 2.0, 11)
    out = {p.name: rec(p, ev) for p in pols}
    print(json.dumps(out))
