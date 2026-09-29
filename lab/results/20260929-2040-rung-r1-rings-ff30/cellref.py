import math
# direct RK4 through the banded cell law: u'' = F - 3uk^2 - (1-6uk) u, uk from current band
def run(m, p, e, cycles=2):
    invL2 = (p-3-e*e)/(p*p)
    def uk_of(u):
        j = math.floor(m*math.log2(1.0/u))
        while u > 2.0**(-j/m): j -= 1
        while u < 2.0**(-(j+1)/m): j += 1
        return 2.0**(-(j+0.5)/m)
    u = (1+e)/p; v = 0.0; phi = 0.0
    h = 2e-5
    seen_pos = False
    peris = []
    n = 0
    while n < int(30*math.pi/h):
        uk = uk_of(u)
        def f(uu, uk=uk): return invL2 - 3*uk*uk - (1-6*uk)*uu
        k1u, k1v = v, f(u)
        k2u, k2v = v + h/2*k1v, f(u + h/2*k1u)
        k3u, k3v = v + h/2*k2v, f(u + h/2*k2u)
        k4u, k4v = v + h*k3v, f(u + h*k3u)
        u1 = u + h/6*(k1u+2*k2u+2*k3u+k4u)
        v1 = v + h/6*(k1v+2*k2v+2*k3v+k4v)
        if v1 > 0: seen_pos = True
        if seen_pos and v > 0 and v1 <= 0:
            peris.append(phi)
            if len(peris) >= cycles+1: break
        u, v, phi = u1, v1, phi+h
        n += 1
    dphi = peris[2]-peris[1] if len(peris)>2 else float('nan')
    return peris[1], dphi-2*math.pi
for m in (4,8,16,32,64):
    t0, adv = run(m, 84.250535430432734, 0.4413757444233366)
    print(f"m={m:3d} first-peri phi={t0:.9f} adv={adv:.9f}")
