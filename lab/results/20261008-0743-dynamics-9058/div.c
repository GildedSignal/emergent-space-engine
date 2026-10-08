/* Truth pair divergence (Lyapunov floor) + truth e(t) for each scene. */
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#define MU 1.0/1047.35
#define GMS (1.0-MU)
static double THJ0 = 0.4;
typedef struct { double x, y, vx, vy; } St;
static void acc_bar(double t, const St *s, double *ax, double *ay) {
    double cc = cos(t + THJ0), ss = sin(t + THJ0);
    double dxs = s->x + MU * cc, dys = s->y + MU * ss, rs3 = pow(dxs * dxs + dys * dys, 1.5);
    double dxj = s->x - (1 - MU) * cc, dyj = s->y - (1 - MU) * ss, rj3 = pow(dxj * dxj + dyj * dyj, 1.5);
    *ax = -GMS * dxs / rs3 - MU * dxj / rj3;
    *ay = -GMS * dys / rs3 - MU * dyj / rj3;
}
static St rk4_step(double t, St s, double h) {
    double y[4] = { s.x, s.y, s.vx, s.vy }, k1[4], k2[4], k3[4], k4[4], yy[4]; St st;
    k1[0]=y[2];k1[1]=y[3];acc_bar(t,&s,&k1[2],&k1[3]);
    for(int i=0;i<4;i++)yy[i]=y[i]+0.5*h*k1[i]; st.x=yy[0];st.y=yy[1];st.vx=yy[2];st.vy=yy[3];
    k2[0]=yy[2];k2[1]=yy[3];acc_bar(t+0.5*h,&st,&k2[2],&k2[3]);
    for(int i=0;i<4;i++)yy[i]=y[i]+0.5*h*k2[i]; st.x=yy[0];st.y=yy[1];st.vx=yy[2];st.vy=yy[3];
    k3[0]=yy[2];k3[1]=yy[3];acc_bar(t+0.5*h,&st,&k3[2],&k3[3]);
    for(int i=0;i<4;i++)yy[i]=y[i]+h*k3[i]; st.x=yy[0];st.y=yy[1];st.vx=yy[2];st.vy=yy[3];
    k4[0]=yy[2];k4[1]=yy[3];acc_bar(t+h,&st,&k4[2],&k4[3]);
    St o;
    o.x=y[0]+h/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0]); o.y=y[1]+h/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1]);
    o.vx=y[2]+h/6*(k1[2]+2*k2[2]+2*k3[2]+k4[2]); o.vy=y[3]+h/6*(k1[3]+2*k2[3]+2*k3[3]+k4[3]);
    return o;
}
int main(int argc, char **argv) {
    double a0 = atof(argv[1]); long norb = atol(argv[2]);
    double e0=0.05, pom0=0.3, f0=1.1, p=a0*(1-e0*e0), rr=p/(1+e0*cos(f0));
    St hel = { rr*cos(pom0+f0), rr*sin(pom0+f0),
               -sqrt(GMS/p)*(sin(pom0+f0)+e0*sin(pom0)), sqrt(GMS/p)*(cos(pom0+f0)-e0*cos(pom0)) };
    St t1 = { hel.x - MU*cos(THJ0), hel.y - MU*sin(THJ0), hel.vx + MU*sin(THJ0), hel.vy - MU*cos(THJ0) };
    St t2 = t1; t2.x += 1e-12;
    double h = 2*M_PI/8192.0, tt = 0;
    printf("t_jup,sep,e_truth\n");
    for (long j = 1; j <= norb; j++) {
        double target = j * 2 * M_PI;
        while (tt < target - 1e-12) { double hh = fmin(h, target - tt); t1 = rk4_step(tt, t1, hh); t2 = rk4_step(tt, t2, hh); tt += hh; }
        double r = hypot(t1.x, t1.y), v2 = t1.vx*t1.vx + t1.vy*t1.vy;
        double xs = -MU*cos(tt+THJ0), ys = -MU*sin(tt+THJ0), vxs = MU*sin(tt+THJ0), vys = -MU*cos(tt+THJ0);
        St hh2 = { t1.x-xs, t1.y-ys, t1.vx-vxs, t1.vy-vys };
        double rh = hypot(hh2.x, hh2.y), vh2 = hh2.vx*hh2.vx + hh2.vy*hh2.vy, rvh = hh2.x*hh2.vx + hh2.y*hh2.vy;
        double ex = (vh2/GMS - 1/rh)*hh2.x - rvh/GMS*hh2.vx, ey = (vh2/GMS - 1/rh)*hh2.y - rvh/GMS*hh2.vy;
        printf("%.6f,%.3e,%.6f\n", tt/(2*M_PI), hypot(t1.x-t2.x, t1.y-t2.y) + hypot(t1.vx-t2.vx, t1.vy-t2.vy), hypot(ex, ey));
    }
    return 0;
}
