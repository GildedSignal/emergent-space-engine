# Probe: does re-anchoring an exact Kepler orbit onto a velocity lattice make E random-walk or drift?
# GM=1, a=1, e=0.1. Velocity quantum q/v ~ 3.5e-8 (LEO at Q=2^40). 43 re-anchors per orbit (tidal-kick rate).
import math, sys, time
q = 3.5e-8
def elems(x,y,vx,vy):
    r=math.hypot(x,y); v2=vx*vx+vy*vy
    E=0.5*v2-1/r; L=x*vy-y*vx
    a=-1/(2*E); ex=(v2-1/r)*x-(x*vx+y*vy)*vx; ey=(v2-1/r)*y-(x*vx+y*vy)*vy
    e=math.hypot(ex,ey); w=math.atan2(ey,ex)
    # true anomaly -> eccentric -> mean
    nu=math.atan2(y,x)-w
    Ea=2*math.atan2(math.sqrt(1-e)*math.sin(nu/2), math.sqrt(1+e)*math.cos(nu/2))
    M=Ea-e*math.sin(Ea)
    return a,e,w,M,L
def prop(a,e,w,M0,L,dt):
    n=a**-1.5; M=M0+n*dt
    Ea=M
    for _ in range(30):
        f=Ea-e*math.sin(Ea)-M; Ea-=f/(1-e*math.cos(Ea))
    cE,sE=math.cos(Ea),math.sin(Ea); b=a*math.sqrt(1-e*e)
    xp=a*(cE-e); yp=b*sE; r=a*(1-e*cE)
    vxp=-a*n*sE*a/r; vyp=b*n*cE*a/r
    sg=1 if L>0 else -1
    yp*=sg; vyp*=sg
    cw,sw=math.cos(w),math.sin(w)
    return xp*cw-yp*sw, xp*sw+yp*cw, vxp*cw-vyp*sw, vxp*sw+vyp*cw
def run(mode, spacing, orbits):
    x,y,vx,vy=0.9,0.0,0.0,math.sqrt(1/0.9*(1.1)) # periapsis of a=1,e=0.1
    E0=0.5*(vx*vx+vy*vy)-1/0.9; L0=x*vy-y*vx
    P=2*math.pi; dt=P/43*(1 if spacing=='locked' else (math.sqrt(5)-1)/2*1.618)
    nsteps=int(orbits*P/dt); cE=0.0; cL=0.0
    for i in range(nsteps):
        el=elems(x,y,vx,vy); x,y,vx,vy=prop(*el,dt)
        if mode=='floor': vx=math.floor(vx/q)*q; vy=math.floor(vy/q)*q
        elif mode=='round': vx=round(vx/q)*q; vy=round(vy/q)*q
        elif mode=='sigma':  # choose lattice velocity in 5x5 box minimizing carried E,L error
            r=math.hypot(x,y); Et=0.5*(vx*vx+vy*vy)-1/r; Lt=x*vy-y*vx
            bx,by=round(vx/q),round(vy/q); best=None
            for i2 in range(-2,3):
                for j2 in range(-2,3):
                    ux=(bx+i2)*q; uy=(by+j2)*q
                    dE=0.5*(ux*ux+uy*uy)-1/r-Et; dL=x*uy-y*ux-Lt
                    cost=((cE+dE)/q)**2+((cL+dL)/q)**2
                    if best is None or cost<best[0]: best=(cost,ux,uy,dE,dL)
            _,vx,vy,dE,dL=best; cE+=dE; cL+=dL
    E=0.5*(vx*vx+vy*vy)-1/math.hypot(x,y); L=x*vy-y*vx
    return nsteps,(E-E0)/abs(E0),(L-L0)/abs(L0)
t0=time.time()
for orbits in (100,1000):
  for spacing in ('locked','irrational'):
    for mode in ('floor','round','sigma'):
        n,dE,dL=run(mode,spacing,orbits)
        # along-track drift per orbit implied at end: 1.5*dE/E*2pi (in units of a)
        print(f"orbits={orbits:5d} {spacing:10s} {mode:5s} steps={n:6d} dE/E={dE:+.2e} (={dE/q:+8.1f} q) dL/L={dL:+.2e}  alongtrack/orbit={1.5*abs(dE)*2*math.pi:.1e} a")
print("wall",round(time.time()-t0,1),"s")
