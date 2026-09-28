exec(open('reanchor.py').read().split("t0=time.time()")[0])
def run2(mode, spacing, orbits):
    x,y,vx,vy=0.9,0.0,0.0,math.sqrt(1/0.9*(1.1))
    el0=elems(x,y,vx,vy)
    P=2*math.pi; dt=P/43*(1 if spacing=='locked' else (math.sqrt(5)-1)/2*1.618)
    nsteps=int(orbits*P/dt); cE=cL=0.0
    for i in range(nsteps):
        el=elems(x,y,vx,vy); x,y,vx,vy=prop(*el,dt)
        if mode=='round': vx=round(vx/q)*q; vy=round(vy/q)*q
        elif mode=='sigma':
            r=math.hypot(x,y); Et=0.5*(vx*vx+vy*vy)-1/r; Lt=x*vy-y*vx
            bx,by=round(vx/q),round(vy/q); best=None
            for i2 in range(-2,3):
                for j2 in range(-2,3):
                    ux=(bx+i2)*q; uy=(by+j2)*q
                    dE=0.5*(ux*ux+uy*uy)-1/r-Et; dL=x*uy-y*ux-Lt
                    c=((cE+dE)/q)**2+((cL+dL)/q)**2
                    if best is None or c<best[0]: best=(c,ux,uy,dE,dL)
            _,vx,vy,dE,dL=best; cE+=dE; cL+=dL
    xt,yt,_,_=prop(*el0,nsteps*dt)
    return math.hypot(x-xt,y-yt)
for orbits in (100,1000,3000):
    for mode in ('round','sigma'):
        print(orbits,mode,"pos err (units of a) = %.2e  -> LEO %.1f m"%(run2(mode,'irrational',orbits),run2(mode,'irrational',orbits)*6.7e6))
