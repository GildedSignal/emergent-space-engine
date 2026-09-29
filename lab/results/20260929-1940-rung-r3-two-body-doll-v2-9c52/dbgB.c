#include "r3nomain.h"
int main(int nargs, char** args) {
    gl_nodes(32);
    double s = atof(args[1]);
    LAW = 1; OWNER = 0; AIM_S = s; MIND = 1e9; NCROSS = 0; NEV = 0; HANDOFF_HOOK = NULL;
    double y[8]; init_flyby(2.13e-4, y);
    double t = 0, h = 1e-5;
    while (t < 0.6) {
        double y1[8], y2[8];
        memcpy(y1, y, sizeof(y1)); memcpy(y2, y, sizeof(y2));
        rk4(y1, h, deriv_doll); rk4(y2, h/2, deriv_doll); rk4(y2, h/2, deriv_doll);
        double err = 0;
        for (int j = 0; j < 8; j++) { double e = fabs(y1[j]-y2[j])/(ATOL+RTOL*fabs(y2[j])); if (e > err) err = e; }
        if (err > 1) { h *= 0.5; continue; }
        memcpy(y, y1, sizeof(y1)); t += h;
        double px, py, vx, vy; planet_state(y, &px, &py, &vx, &vy);
        double d = sqrt((y[4]-px)*(y[4]-px)+(y[5]-py)*(y[5]-py));
        static double tl = -1;
        if (t - tl > 0.02) { printf("t=%.4f d=%.5e own=%d h=%.2e\n", t, d, OWNER, h); tl = t; }
        if (err > 1e-28) h *= fmin(2.2, fmax(0.2, 0.9*pow(err, -0.2))); else h *= 2.2;
    }
    return 0;
}
