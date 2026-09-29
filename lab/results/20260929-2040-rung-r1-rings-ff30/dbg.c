#include <stdio.h>
#include <stdlib.h>
#define main rung_main
#include "rung.c"
#undef main
int main(int argc, char **argv) {
    gauss_legendre(32, gln64_x, gln64_w);
    gauss_legendre(16, gl16_x, gl16_w);
    int kind = atoi(argv[1]), m = atoi(argv[2]);
    double p = atof(argv[3]), e = atof(argv[4]);
    int ncyc = atoi(argv[5]);
    Eng eng; BoundOut bo;
    eng_init_bound(&eng, kind, m, p, e);
    long cnt[6] = {0};
    int nperi = (eng.kind == K_BINET) ? 1 : 0;
    double rperi1 = 0, rapo1 = 0, dphi1 = 0, dt1 = 0, phip = 0, tp = 0;
    for (long i = 0; i < 20000000; i++) {
        int ev = eng_step(&eng);
        cnt[ev]++;
        if (i < 400 || (i % 1000000 == 0))
            printf("ev=%d u=%.17g v=%.17g j=%d phi=%.6g t=%.6g turn=%.6g\n",
                   ev, eng.kind==K_BINET?eng.u:0.0, eng.kind==K_BINET?eng.v:0.0, eng.j, eng.phi, eng.t, eng.turn_r);
        if (ev == EV_ERR) { printf("ERR at %ld\n", i); break; }
        if (ev == EV_ABSORB || ev == EV_ESCAPE) { printf("%s at %ld phi=%.4g\n", ev==EV_ABSORB?"ABSORB":"ESC", i, eng.phi); break; }
        if (ev == EV_PERI) {
            nperi++;
            if (nperi == 1) { rperi1 = eng.turn_r; phip = eng.phi; tp = eng.t; continue; }
            double dphi = eng.phi - phip, dt = eng.t - tp;
            printf("PERI cyc=%d dphi=%.12g (adv=%.9g) dt=%.9g rperi=%.6g (1st %.6g)\n",
                   nperi-1, dphi, dphi-2*PI, dt, eng.turn_r, rperi1);
            if (nperi-1 == 1) { dphi1 = dphi; dt1 = dt; }
            phip = eng.phi; tp = eng.t;
            if (nperi-1 >= ncyc) break;
        }
        if (ev == EV_APO && nperi >= 1 && rapo1 == 0) rapo1 = eng.turn_r;
    }
    printf("counts: edge=%ld peri=%ld apo=%ld absorb=%ld esc=%ld err=%ld\n",
           cnt[0],cnt[1],cnt[2],cnt[3],cnt[4],cnt[5]);
    (void)bo;
    return 0;
}
