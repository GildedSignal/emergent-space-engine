#include <stdio.h>
#include <math.h>
#define MU 1.0/1047.35
#define GMS (1.0-MU)
typedef struct { double x, y, vx, vy; } St;
#include "kepler_inc.h"
int main(void) {
    /* near-circular orbit a=0.3846, e=0.05 */
    double a0=0.3846,e0=0.05,p=a0*(1-e0*e0);
    St s = { p/(1+e0)*1.0, 0.0, 0.0, sqrt(GMS/p)*(1+e0) };  /* periapsis */
    double T = 2*M_PI/sqrt(GMS/(a0*a0*a0));
    St t1 = s; kepler(&t1, T);
    printf("one period roundtrip: dx=%.3e dy=%.3e dvx=%.3e dvy=%.3e\n",
           t1.x-s.x, t1.y-s.y, t1.vx-s.vx, t1.vy-s.vy);
    /* 1000 windows of T/1000 */
    St t2 = s; for (int i=0;i<1000;i++) kepler(&t2, T/1000);
    printf("1000 windows:        dx=%.3e dy=%.3e dvx=%.3e dvy=%.3e\n",
           t2.x-s.x, t2.y-s.y, t2.vx-s.vx, t2.vy-s.vy);
    /* forward then back */
    St t3 = s; kepler(&t3, 0.37*T); kepler(&t3, -0.37*T);
    printf("fwd/back:            dx=%.3e dy=%.3e dvx=%.3e dvy=%.3e\n",
           t3.x-s.x, t3.y-s.y, t3.vx-s.vx, t3.vy-s.vy);
    return 0;
}
