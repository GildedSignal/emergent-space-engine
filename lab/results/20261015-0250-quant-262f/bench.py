#!/usr/bin/env python3
"""Prices the belt's first-kick promotion with a closed (Carlson-form) readout.

Channels are the shipped walk's own integrands (crates/space/src/orbit.rs `node`):
  advance integrand a/(sqrt(D)(1+sqrt(D))) = (1/q)(1/sqrt(D) - 1)   [exact, since 1-D = q a]
  t   = t_num /(sqrt(D) x^2 (1-2q x))
  tau = tau_num/(sqrt(D) x^2)
with x = k+(1-k)cos psi, D = 1-q a, a = 6k+2(1-k)cos psi, psi = 2u:
  x = 1 - n3 sin^2 u (n3 = 2(1-k)); D = A(1-m cos^2 u), A = 1-2q(4k-1), m = 4q(1-k)/A
  1-2qx = (1-2q)(1+n4 sin^2 u), n4 = 2q n3/(1-2q)
Squared-pole reduction (Hermite): boundary coefficient kappa = n^2/(2(n+1)(M+n)),
independently derived here by exact rational solve and equal to cd6e's (wiki).
"""
import numpy as np, time, sys
from scipy import integrate, special

AU = 101_300_000.0  # crates/universe/src/scenario.rs

def i2_coefs(n, M):
    """q0,q1,c1,kappa with int du/((1+n s^2)^2 sqrt(1-M s^2)) =
    q0 F + q1 (F-E)/M + c1 Pi(-n) + kappa s c sqrt(1-Ms^2)/(1+n s^2)."""
    Mx = np.array([[1,0,1,1],[2*n,1,n,-n-2-2*M],[n*n,2*n,0,3*M],[0,n*n,0,M*n]], float)
    return np.linalg.solve(Mx, np.array([1.0,0,0,0]))

def channels_closed(k, q, u):
    n3=2*(1-k); eta=1-k
    A=1-2*q*(4*k-1); m=4*q*(1-k)/A; mg=-m/(1-m); n4=2*q*n3/(1-2*q)
    tnum=np.sqrt(k*(1-2*q)*(1+2*q*(1-2*k))); dnum=np.sqrt(k-q*(3*k*k+eta*eta))
    s=np.sin(u); c=np.cos(u); s2=s*s; c2=c*c
    W2=1-mg*s2; W=np.sqrt(W2); V=1-n3*s2
    F=s*special.elliprf(c2,W2,1.0)
    Pi=lambda nn: F+(nn/3)*s**3*special.elliprj(c2,W2,1.0,1-nn*s2)
    E=F-(mg/3)*s**3*special.elliprj(c2,W2,1.0,1.0)
    q0,q1,c1,kap=i2_coefs(-n3,mg)
    I2=q0*F+q1*(F-E)/mg+c1*Pi(n3)+kap*s*c*W/V
    aa,bb2,gg=np.linalg.solve(np.array([[1,1,1],[n4-n3,n4,-2*n3],[-n3*n4,0,n3*n3]]),np.array([1.0,0,0]))
    adv=(1/q)*(2/np.sqrt(A*(1-m))*F-2*u)
    tau=2*dnum/np.sqrt(A*(1-m))*I2
    t=2*tnum/((1-2*q)*np.sqrt(A*(1-m)))*(aa*Pi(n3)+bb2*I2+gg*Pi(-n4))
    return adv,t,tau

def channels_simpson(k,q,u):
    eta=1-k
    tnum=np.sqrt(k*(1-2*q)*(1+2*q*(1-2*k))); dnum=np.sqrt(k-q*(3*k*k+eta*eta))
    f_adv=lambda th:(1/q)*(1/np.sqrt(1-q*(6*k+2*eta*np.cos(th)))-1)
    f_t=lambda th: tnum/(np.sqrt(1-q*(6*k+2*eta*np.cos(th)))*(k+eta*np.cos(th))**2*(1-2*q*(k+eta*np.cos(th))))
    f_tau=lambda th: dnum/(np.sqrt(1-q*(6*k+2*eta*np.cos(th)))*(k+eta*np.cos(th))**2)
    return [integrate.quad(f,0,2*u,limit=400)[0] for f in (f_adv,f_t,f_tau)]

def belt_draw(rng, n):
    a=2+rng.random(n); e=0.07*np.sqrt(-2*np.log(rng.random(n)+1e-18))
    while (e>0.4).any():
        r=e>0.4; e[r]=0.07*np.sqrt(-2*np.log(rng.random(r.sum())+1e-18))
    p=a*(1-e)*AU
    return p, 1/(1+e), 1/p, e

def main():
    rng=np.random.default_rng(3)
    print("== verification vs Simpson of the shipped integrands (belt mix) ==")
    mx={'adv':0,'t':0,'tau':0}
    for _ in range(10):
        p,k,q,e=belt_draw(rng,1); u=float(rng.random())*np.pi/2; k=float(k); q=float(q)
        C0=channels_simpson(float(k),float(q),float(u)); C1=channels_closed(float(k),float(q),float(u))
        for i,kk in enumerate(['adv','t','tau']): mx[kk]=max(mx[kk],abs(C1[i]-C0[i])/abs(C0[i]))
    print("max rel err:", {kk:'%.2e'%v for kk,v in mx.items()})

    print("== batched price over the wave's promotions (SoA, vectorized Newton, N=1e6) ==")
    N=1_000_000
    p,K,Q,e=belt_draw(rng,N); u_t=rng.random(N)*np.pi/2
    n3=2*(1-K); eta=1-K
    A=1-2*Q*(4*K-1); m=4*Q*(1-K)/A; mg=-m/(1-m); n4=2*Q*n3/(1-2*Q)
    tnum=np.sqrt(K*(1-2*Q)*(1+2*Q*(1-2*K))); dnum=np.sqrt(K-Q*(3*K*K+eta*eta))
    CH=2/np.sqrt(A*(1-m)); n=-n3; M=mg
    Amt=np.empty((N,4,4))
    Amt[:,0,0]=1; Amt[:,0,1]=0; Amt[:,0,2]=1; Amt[:,0,3]=1
    Amt[:,1,0]=2*n; Amt[:,1,1]=1; Amt[:,1,2]=n; Amt[:,1,3]=-n-2-2*M
    Amt[:,2,0]=n*n; Amt[:,2,1]=2*n; Amt[:,2,2]=0; Amt[:,2,3]=3*M
    Amt[:,3,0]=0; Amt[:,3,1]=n*n; Amt[:,3,2]=0; Amt[:,3,3]=M*n
    q0,q1,c1,kap=np.linalg.solve(Amt,np.tile([1.0,0,0,0],(N,1))).T
    Amt2=np.empty((N,3,3))
    Amt2[:,0]=1; Amt2[:,1,0]=n4-n3; Amt2[:,1,1]=n4; Amt2[:,1,2]=-2*n3
    Amt2[:,2,0]=-n3*n4; Amt2[:,2,2]=n3*n3
    aa,bb2,gg=np.linalg.solve(Amt2,np.tile([1.0,0,0],(N,1))).T
    def read_batch(u):
        s=np.sin(u); c=np.cos(u); s2=s*s; c2=c*c
        W2=1-mg*s2; W=np.sqrt(W2); V=1-n3*s2
        F=s*special.elliprf(c2,W2,1.0)
        Pi=lambda nn: F+(nn/3)*s**3*special.elliprj(c2,W2,1.0,1-nn*s2)
        E=F-(mg/3)*s**3*special.elliprj(c2,W2,1.0,1.0)
        I2=q0*F+q1*(F-E)/mg+c1*Pi(n3)+kap*s*c*W/V
        adv=(1/Q)*(CH*F-2*u)
        tau=2*dnum*CH*I2
        t=2*tnum*CH/(1-2*Q)*(aa*Pi(n3)+bb2*I2+gg*Pi(-n4))
        return adv,t,tau,s,W,V
    _,t_true,_,_,_,_=read_batch(u_t)
    t0=time.perf_counter()
    _,Th,_,_,_,_=read_batch(np.full(N,np.pi/2))     # cold start needs the half-period
    u=(np.pi/2)*(t_true/Th); iters=0
    for it in range(24):
        adv,tt,tau,s,W,V=read_batch(u)
        s2=s*s; c2=(1-s2); D=A*(1-m*c2)
        dtdu=2*tnum*CH/(1-2*Q)/(V*V*np.sqrt(D)*(1-2*Q*(1-n3*s2)))
        du=(t_true-tt)/dtdu
        u=np.clip(u+du,1e-12,np.pi/2-1e-12); iters=it+1
        if np.max(np.abs(du))<1e-13: break
    t1=time.perf_counter()
    err=np.abs(u-u_t)
    print(f"batched: {(t1-t0)/N*1e6:.3f} us/promotion | newton iters={iters} | recovered-u err max={err.max():.1e} p99={np.quantile(err,0.99):.1e}")
    print(f"belt mix: e mean={e.mean():.3f} p99={np.quantile(e,0.99):.3f}; q in [{Q.min():.2e},{Q.max():.2e}]")

    print("== scalar reference (python loop, interpreter-inflated; 2e3 bodies, no Newton) ==")
    t0=time.perf_counter(); Ms=2000
    for i in range(Ms):
        channels_closed(float(K[i]),float(Q[i]),float(u_t[i]))
    t1=time.perf_counter()
    print(f"scalar: {(t1-t0)/Ms*1e6:.2f} us/readout (upper bound; no Newton)")

if __name__=="__main__":
    main()
