#include <stdio.h>
#include <math.h>
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
int main(void) {
    /* same IC as cadence.c: a=0.3846 e=0.05 pom=0.3 f=1.1, barycentric */
    double a0=0.3846,e0=0.05,pom0=0.3,f0=1.1,p=a0*(1-e0*e0),rr=p/(1+e0*cos(f0));
    St hel = { rr*cos(pom0+f0), rr*sin(pom0+f0),
               -sqrt(GMS/p)*(sin(pom0+f0)+e0*sin(pom0)), sqrt(GMS/p)*(cos(pom0+f0)-e0*cos(pom0)) };
    St tru = { hel.x - MU*cos(THJ0), hel.y - MU*sin(THJ0), hel.vx + MU*sin(THJ0), hel.vy - MU*cos(THJ0) };
    double h = 2*M_PI/8192.0;
    for (double t=0; t < 4*M_PI-1e-9; ) { double hh=fmin(h, 4*M_PI-t); tru=rk4_step(t,tru,hh); t+=hh; }
    printf("C truth at t=4pi: %.15f %.15f %.15f %.15f\n", tru.x, tru.y, tru.vx, tru.vy);
    return 0;
}
