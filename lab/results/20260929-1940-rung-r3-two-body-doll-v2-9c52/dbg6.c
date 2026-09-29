#include "r3nomain.h"
static void pr(const char* tag, double t, const double* y) {
    double px, py, vx, vy; planet_state(y, &px, &py, &vx, &vy);
    double d = sqrt((y[4]-px)*(y[4]-px)+(y[5]-py)*(y[5]-py));
    static double tl = -1;
    if (t - tl > 0.005) { printf("%s t=%.4f d=%.5e own=%d\n", tag, t, d, OWNER); tl = t; }
}
static void evd(double t, const double* y, void* c) { pr("DOLL", t, y); fb_track(t, y, c); }
static void evr(double t, const double* y, void* c) { pr("REF ", t, y); fb_track(t, y, c); }
int main(void) {
    gl_nodes(32);
    LAW = 1; OWNER = 0; AIM_S = -2.99246197e-04; MIND = 1e9; NCROSS = 0; NEV = 0; HANDOFF_HOOK = NULL;
    double y[8], y0[8]; init_flyby(2.13e-4, y); memcpy(y0, y, sizeof(y0));
    propagate(y, 3.0, 1, 1e-5, evd, NULL, NULL);
    double dvx = y[6]-y0[6], dvy = y[7]-y0[7];
    printf("doll mind=%.4e crossings=%ld dv=%.5e %.5e\n", MIND, NCROSS, dvx, dvy);
    OWNER = 0; MIND = 1e9; NCROSS = 0;
    double y2[8]; init_flyby(2.13e-4, y2); memcpy(y0, y2, sizeof(y0));
    propagate(y2, 3.0, 0, 1e-5, evr, NULL, NULL);
    printf("ref  mind=%.4e dv=%.5e %.5e\n", MIND, y2[6]-y0[6], y2[7]-y0[7]);
    return 0;
}
