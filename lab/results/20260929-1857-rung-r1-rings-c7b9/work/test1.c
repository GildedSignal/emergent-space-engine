#define main rung_main_disabled
#include "rung_r1.c"
#undef main
int main(void)
{
    gauss_legendre_into(32, GL32); gauss_legendre_into(16, GL16); gauss_legendre_into(12, GL12);
    // seed 0: p=84.251, e=0.441
    double p = 84.251, e = 0.441, E, L;
    bound_constants(p, e, &E, &L);
    printf("E=%.6f L=%.6f r_p=%.3f r_a=%.3f adv_GR=%.6f T_GR=%.3f\n",
           E, L, p/(1+e), p/(1-e), periapsis_elliptic(p,e), bound_period_quad_t(p,e));
    for (int eng = 0; eng < 4; eng++) {
        int mm = (eng==0)?32:(eng==1?32:16);
        CycM cyc[8]; int s1[MAXSEQ],n1,s2[MAXSEQ],n2;
        int n = walk_bound(eng, mm, E, L, (1.0+e)/p, 3, cyc, s1,&n1, s2,&n2, NULL,NULL,NULL,0);
        printf("eng=%d n=%d", eng, n);
        if (n >= 2)
            printf(" dphi0=%.6f adv=%.6f T0=%.3f rperi=%.3f rapo=%.3f cross=%lld",
                   cyc[0].dphi, cyc[0].dphi-2*PI, cyc[0].dt, cyc[0].r_peri, cyc[0].r_apo, cyc[0].cross);
        printf("\n");
    }
    return 0;
}
