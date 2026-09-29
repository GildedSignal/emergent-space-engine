#include "r3nomain.h"
static int nstop = 0;
static int mystop(double t, const double* y, void* c) {
    int r = fb_stop(t, y, c);
    if (r && nstop++ < 3) {
        double px, py, vx, vy; planet_state(y, &px, &py, &vx, &vy);
        printf("STOP fired t=%.6f d=%.6e\n", t, sqrt((y[4]-px)*(y[4]-px)+(y[5]-py)*(y[5]-py)));
    }
    return r;
}
int main(void) {
    gl_nodes(32);
    LAW = 1; OWNER = 0; AIM_S = -2.00727528e-04; MIND = 1e9; NCROSS = 0; NEV = 0; HANDOFF_HOOK = handoff_hook;
    double y[8]; init_flyby(2.13e-4, y);
    propagate(y, 3.0, 1, 1e-5, fb_track, NULL, mystop);
    printf("MIND=%.6e crossings=%ld\n", MIND, NCROSS);
    return 0;
}
