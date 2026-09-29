#include "r3nomain.h"
static void dbgt(double t, const double* y, void* c) {
    (void)c;
    double px, py, vx, vy; planet_state(y, &px, &py, &vx, &vy);
    double d = sqrt((y[4]-px)*(y[4]-px)+(y[5]-py)*(y[5]-py));
    static double tl = -1;
    if (t - tl > 0.01) { printf("t=%.4f d=%.5e own=%d ncross=%ld\n", t, d, OWNER, NCROSS); tl = t; }
}
int main(int argc, char** argv) {
    gl_nodes(32);
    LAW = 1; OWNER = 0; AIM_S = -2.007e-4; MIND = 1e9; NCROSS = 0; NEV = 0; HANDOFF_HOOK = handoff_hook;
    double y[8]; init_flyby(0.0, y);
    propagate(y, 3.0, 1, 1e-5, dbgt, NULL, NULL);
    printf("final MIND via fb_track never called; crossings=%ld handoffs=%d\n", NCROSS, NEV);
    return 0;
}
