#include <stdio.h>
#include <math.h>
#define MU 1.0/1047.35
#define GMS (1.0-MU)
typedef struct { double x, y, vx, vy; } St;
#include "kepler_inc.h"
int main(void) {
    double a0=0.3846,e0=0.05,p=a0*(1-e0*e0);
    St s = { p/(1+e0), 0.0, 0.0, sqrt(GMS/p)*(1+e0) };
    double T = 2*M_PI/sqrt(GMS/(a0*a0*a0));
    /* replicate the solve for one full period to inspect convergence */
    double r0 = hypot(s.x,s.y), v2=s.vx*s.vx+s.vy*s.vy;
    double rdv = s.x*s.vx+s.y*s.vy, alpha = 2/r0 - v2/GMS;
    double dt = T;
    double X = sqrt(GMS)*fabs(alpha)*dt;
    for (int it=0; it<12; it++) {
        double z=alpha*X*X,C,S; stumpff(z,&C,&S);
        double F = X*X*X*S + rdv/sqrt(GMS)*X*X*C + r0*X - sqrt(GMS)*dt;
        double dF = X*X*C + rdv/sqrt(GMS)*X*(1-z*S) + r0;
        printf("it=%2d X=%.15f F=%.3e dF=%.3f\n", it, X, F, dF);
        double dX=F/dF; X-=dX;
        if (fabs(dX)<1e-14*(1+fabs(X))) break;
    }
    return 0;
}
