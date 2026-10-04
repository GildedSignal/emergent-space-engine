// q-correctors (quant lens): the kick-cadence curve of the drift+impulse-kick layer.
//
// Faithful float prototype of crates/universe step.rs+force.rs in the regime where the SyMBA
// changeover never engages (hierarchical, non-crossing orbits): exact Kepler drift under the
// dominant mass, stepped in the drift's own phase (mean anomaly, dm = 2*pi/steps per step, so
// the time step is exactly dm*a^1.5), an impulse kick of the perturbing acceleration with the
// full interval's true dt as weight, evaluated at the step's midpoint state and time (planet
// on its exact circular orbit), and a rebind (elements recomputed from state) after every kick
// — one event per kick, exactly like the engine. Circular restricted three-body: GM_star=1,
// a_p=1, omega_p=1, mu=m_planet/M_star. Conserved truth: J = v^2/2 - 1/r - mu/|r-r_p| - h_z.
//
// kdk <steps/orbit>: 2nd-order KDK, one kick event per step.
// y4  <macro/orbit>: Yoshida-4 triple jump (w1,w2,w1), 3 kick events per macro step.
//
// Metrics over 4096 ship orbits: max |dJ|/|J0|; growth exponent alpha of the |dJ| envelope in
// log-t bins (0 if under the 1e-13 float floor, per B12's rule); apsidal rate domega/dt from
// the element omega (unwrapped, linear fit over orbits 100..4096).
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

typedef struct { double a,e,om,M,t; } Orb;           // M: mean anomaly (unwrapped)
typedef struct { double x,y,vx,vy; } St;
static const double PI=3.14159265358979323846;

static double kepler(double M,double e){             // solve E - e sinE = M
  double m=fmod(M,2*PI); if(m<0) m+=2*PI;
  double E=m+e*sin(m);
  for(int i=0;i<100;i++){ double f=E-e*sin(E)-m, d=f/(1-e*cos(E)); E-=d; if(fabs(d)<1e-15) break; }
  return E;
}
static St state(const Orb*o){
  double E=kepler(o->M,o->e), cE=cos(E), sE=sin(E), s=sqrt(1-o->e*o->e), d=sqrt(o->a)*(1-o->e*cE);
  double xo=o->a*(cE-o->e), yo=o->a*s*sE, vxo=-sE/d, vyo=s*cE/d;
  double co=cos(o->om), so=sin(o->om);
  St st={ xo*co-yo*so, xo*so+yo*co, vxo*co-vyo*so, vxo*so+vyo*co };
  return st;
}
static void rebind(Orb*o, St s){                     // exact elements from state (the engine's rebind)
  double r=hypot(s.x,s.y), v2=s.vx*s.vx+s.vy*s.vy, rv=s.x*s.vx+s.y*s.vy;
  double a=1.0/(2.0/r-v2);
  double ex=(v2-1.0/r)*s.x-rv*s.vx, ey=(v2-1.0/r)*s.y-rv*s.vy, e=hypot(ex,ey);
  if(!(e>1e-8)||a<=0||a>1e3){ fprintf(stderr,"rebind guard e=%g a=%g\n",e,a); exit(3); }
  double E=atan2(rv/(e*sqrt(a)),(1.0-r/a)/e); if(E<0) E+=2*PI;
  o->a=a; o->e=e; o->om=atan2(ey,ex); o->M=E-e*sin(E);
}
static void acc(St s,double t,double mu,double*ax,double*ay){   // perturbation only: the star's pull is the drift
  double px=cos(t), py=sin(t);
  double dx=px-s.x, dy=py-s.y, d3=pow(dx*dx+dy*dy,1.5);
  *ax=mu*(dx/d3-px); *ay=mu*(dy/d3-py);
}
static double jacobi_t(St s,double t,double mu){    // conserved: v^2/2 - 1/r - mu/|r-r_p| - h_z + mu*(r.r_p)
  double px=cos(t), py=sin(t);                      // (dJ/dt = -mu d(r.r_p)/dt for this flow)
  return 0.5*(s.vx*s.vx+s.vy*s.vy)-1.0/hypot(s.x,s.y)-mu/hypot(px-s.x,py-s.y)
        -(s.x*s.vy-s.y*s.vx)+mu*(s.x*px+s.y*py);
}

static long kdk(Orb*o,double dm,double mu){
  double dt1=0.5*dm*pow(o->a,1.5), dtf=dm*pow(o->a,1.5);   // exact time of flight per mean anomaly
  o->M+=dm/2; o->t+=dt1;                             // drift half
  St s=state(o); double ax,ay; acc(s,o->t,mu,&ax,&ay);      // kick at midpoint state and time
  s.vx+=ax*dtf; s.vy+=ay*dtf;
  rebind(o,s);
  double dt2=0.5*dm*pow(o->a,1.5); o->M+=dm/2; o->t+=dt2;   // drift half
  return 1;
}
static long y4(Orb*o,double dm,double mu){
  const double cb=1.2599210498948732, w1=1.0/(2.0-cb), w2=-cb/(2.0-cb);
  return kdk(o,dm*w1,mu)+kdk(o,dm*w2,mu)+kdk(o,dm*w1,mu);
}

int main(int argc,char**argv){
  if(argc<7){ fprintf(stderr,"usage: %s <a0> <e0> <mu> <M0> <method kdk|y4> <steps_per_orbit> [orbits]\n",argv[0]); return 2; }
  double a0=atof(argv[1]), e0=atof(argv[2]), mu=atof(argv[3]), M0=atof(argv[4]);
  const char*meth=argv[5]; int steps=atoi(argv[6]);
  int orbits=(argc>7)?atoi(argv[7]):4096;
  Orb o={ a0,e0,0.7,M0,0.0 };
  double dm=2*PI/steps;
  double J0=jacobi_t(state(&o),0.0,mu), dJmax=0;
  double *ts=malloc(sizeof(double)*(orbits+2)), *Js=malloc(sizeof(double)*(orbits+2)), *os=malloc(sizeof(double)*(orbits+2)), *es=malloc(sizeof(double)*(orbits+2));
  long total=(long)steps*orbits;
  for(long it=1;it<=total;it++){
    if(!strcmp(meth,"y4")) y4(&o,dm,mu); else kdk(&o,dm,mu);
    if(it%steps==0){ int i=it/steps; if(i>orbits) break;
      St s=state(&o); ts[i]=o.t; Js[i]=jacobi_t(s,o.t,mu); os[i]=o.om; es[i]=o.e;
      double d=fabs(Js[i]-J0); if(d>dJmax) dJmax=d; }
  }
  double emax=0; for(int i=1;i<=orbits;i++) if(es[i]>emax) emax=es[i];
  double alpha=0; {
    int nb=10; double bx[24]={0},by[24]={0}; int bn[24]={0}; double lgmax=log10(ts[orbits]);
    for(int i=1;i<=orbits;i++){ if(ts[i]<=0) continue; double lg=log10(ts[i]);
      int b=(int)(nb*lg/lgmax); if(b<0)b=0; if(b>=nb)b=nb-1;
      double d=log10(fmax(fabs(Js[i]-J0),1e-300));
      if(bn[b]==0||d>by[b]){ by[b]=d; bx[b]=lg; } bn[b]++; }
    double sx=0,sy=0,sxx=0,sxy=0; int n=0;
    for(int b=0;b<nb;b++) if(bn[b]&&bx[b]>log10(50.0)){ sx+=bx[b];sy+=by[b];sxx+=bx[b]*bx[b];sxy+=bx[b]*by[b];n++; }
    alpha=(n>=3&&dJmax>1e-13)? (n*sxy-sx*sy)/(n*sxx-sx*sx) : 0.0;
  }
  double domdt=0; {
    double prev=os[1],un[orbits+2];
    for(int i=1;i<=orbits;i++){ un[i]=os[i]; while(un[i]-prev>PI) un[i]-=2*PI; while(prev-un[i]>PI) un[i]+=2*PI; prev=un[i]; }
    double sx=0,sy=0,sxx=0,sxy=0; int n=0;
    for(int i=100;i<=orbits;i++){ sx+=ts[i];sy+=un[i];sxx+=ts[i]*ts[i];sxy+=ts[i]*un[i];n++; }
    domdt=(n*sxy-sx*sy)/(n*sxx-sx*sx);
  }
  printf("{\"a0\":%.4f,\"e0\":%.2f,\"mu\":%.1e,\"M0\":%.2f,\"method\":\"%s\",\"steps\":%d,"
         "\"events_per_orbit\":%.0f,\"maxdJ\":%.3e,\"alpha\":%.3f,\"domdt\":%.9e,\"emax\":%.4f}\n",
         a0,e0,mu,M0,meth,steps, !strcmp(meth,"y4")?3.0*steps:(double)steps, dJmax,alpha,domdt,emax);
  return 0;
}
