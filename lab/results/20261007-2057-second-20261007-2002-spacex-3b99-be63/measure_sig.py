#!/usr/bin/env python3
"""Sigma-instrumented rerun: per-field spread of the scar walk at each checkpoint.
Entropy per field = min(Gaussian log2(sig*sqrt(2*pi*e)/q), uniform cap log2(W/q)).
Histogram entropies (hlive.py) are authoritative where spread << N/4 bins; the
Gaussian value is an upper bound for peaky fields (measured 4 bits high on dL)."""
import json, sys, numpy as np
sys.argv=["hlive"]
import hlive
G=hlive.G
cps=[1,3,10,30,100,300]
def run_full(name,n,se,a0,w_,mb,mp,thin,seed):
    a,e,vp=hlive.belt(n,se,w_,a0,seed)
    E=-G/(2*a); L=np.sqrt(G*a*(1-e**2)); Ax=e*np.cos(vp); Ay=e*np.sin(vp)
    E0,L0,Ax0,Ay0=E.copy(),L.copy(),Ax.copy(),Ay.copy()
    E_typ=G/(2*a0); L_typ=np.sqrt(G*a0)
    rg=np.random.default_rng(seed+777)
    e_bar=se*np.sqrt(np.pi/2); n_mean=2*np.pi/a0**1.5
    lam=n*(a0*2*e_bar)/(2*w_)*(1.5*(a0*2*e_bar*2/3)/a0)
    lam_p=1.5*n_mean*(2*w_)/a0 if mp>0 else 0.0
    mb2=mb*np.sqrt(thin); lt=lam/thin
    recs={}
    for t in range(1,301):
        for li,mi in ((lt,mb2),(lam_p,mp)):
            if mi<=0: continue
            d,tot=hlive.kick_deltas(None,(a,e,E,L,Ax,Ay),mi,se,li,a0,rg)
            if d is None: continue
            E=E+d[0]; L=L+d[1]; Ax=Ax+d[2]; Ay=Ay+d[3]
        if t in cps:
            dE,dL=E-E0,L-L0
            dvp=np.angle(Ax+1j*Ay)-np.angle(Ax0+1j*Ay0); dvp=(dvp+np.pi)%(2*np.pi)-np.pi
            recs[t]={"sigE":float(dE.std()/E_typ),"sigL":float(dL.std()/L_typ),
                     "sigW":float(dvp.std()/(2*np.pi)),"meanE":float(abs(dE.mean())/E_typ)}
    return {"case":name,"lam":lam,"lam_p":lam_p,"recs":{str(k):v for k,v in recs.items()}}
if __name__=="__main__":
    cases=[("cold_m1e-10",2000,0.01,1e-10,0.0,1),("cold_m1e-12",2000,0.01,1e-12,0.0,1),
           ("cold_m1e-8",2000,0.01,1e-8,0.0,1),("hot_m1e-10",2000,0.10,1e-10,0.0,50),
           ("pert_m1e-7",2000,0.01,1e-10,1e-7,1)]
    out=[]
    for name,n,se,mb,mp,thin in cases:
        for sd in (1,2): out.append(run_full(name,n,se,2.1,0.05,mb,mp,thin,sd))
        json.dump(out,open("hlive_sig.json","w"),indent=1); print(name,flush=True)
    SQ=4.1327; W=0.0477
    for r in out[::2]:
        print(r["case"],"lam=%.1f"%r["lam"])
        for t in cps:
            s=r["recs"][str(t)]; line=f"  t={t:4d}"
            for q in (2**-16,2**-20,2**-24):
                hE=min(np.log2(max(s["sigE"]*SQ,1e-12)/q),np.log2(W/q))
                hL=min(np.log2(max(s["sigL"]*SQ,1e-12)/q),np.log2(W/q))
                hW=min(np.log2(max(s["sigW"]*SQ,1e-12)/q),-np.log2(q))
                line+=f" | q2^{int(np.log2(q)):+d} {hE:5.1f}+{hL:5.1f}+{hW:5.1f}={hE+hL+hW:6.1f}"
            print(line)
