#include "r3nomain.h"
int main(void) {
    gl_nodes(32);
    LAW = 1; OWNER = 0; AIM_S = -2.00727528e-04; MIND = 1e9; NCROSS = 0; NEV = 0; HANDOFF_HOOK = handoff_hook;
    double y[8]; init_flyby(2.13e-4, y);
    propagate(y, 3.0, 1, 1e-5, fb_track, NULL, fb_stop);
    printf("with stop: MIND=%.6e crossings=%ld NEV=%d\n", MIND, NCROSS, NEV);
    return 0;
}
