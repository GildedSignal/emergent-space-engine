#include "r3nomain.h"
int main(void) {
    gl_nodes(32);
    LAW = 1; OWNER = 0; AIM_S = -2.007e-4; MIND = 1e9; NCROSS = 0; NEV = 0; HANDOFF_HOOK = NULL;
    double y[8]; init_flyby(0.0, y);
    printf("t=0 ship (%.6f,%.6f) v (%.6f,%.6f) d=%.6e\n", y[4], y[5], y[6], y[7], g_soi(y)+RSOI);
    double t = 0, h = 1e-5;
    for (int i = 0; i < 8000 && t < 0.3; i++) {
        double y1[8], y2[8];
        memcpy(y1, y, sizeof(y1)); memcpy(y2, y, sizeof(y2));
        rk4(y1, h, deriv_doll); rk4(y2, h/2, deriv_doll); rk4(y2, h/2, deriv_doll);
        double err = 0;
        for (int j = 0; j < 8; j++) { double e = fabs(y1[j]-y2[j])/(ATOL+RTOL*fabs(y2[j])); if (e > err) err = e; }
        if (err > 1) { h *= 0.5; continue; }
        memcpy(y, y1, sizeof(y1)); t += h;
        double px, py, vx, vy; planet_state(y, &px, &py, &vx, &vy);
        double d = sqrt((y[4]-px)*(y[4]-px)+(y[5]-py)*(y[5]-py));
        if (i % 60 == 0) printf("t=%.5f d=%.6e own=%d\n", t, d, OWNER);
        h *= 2.0;
    }
    return 0;
}
