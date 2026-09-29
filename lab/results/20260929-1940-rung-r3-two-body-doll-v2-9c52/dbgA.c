#include "r3nomain.h"
static void pr(const char* tag, double t, const double* y) {
    double px, py, vx, vy; planet_state(y, &px, &py, &vx, &vy);
    double d = sqrt((y[4]-px)*(y[4]-px)+(y[5]-py)*(y[5]-py));
    static double tl = -1;
    if (t - tl > 0.01) { printf("%s t=%.4f d=%.5e own=%d\n", tag, t, d, OWNER); tl = t; }
}
int main(int nargs, char** args) {
    gl_nodes(32);
    double s = atof(args[1]);
    LAW = 1; OWNER = 0; AIM_S = s; MIND = 1e9; NCROSS = 0; NEV = 0; HANDOFF_HOOK = NULL;
    double y[8], y0[8]; init_flyby(2.13e-4, y); memcpy(y0, y, sizeof(y0));
    propagate(y, 0.6, 1, 1e-5, pr, NULL, NULL);
    return 0;
}
