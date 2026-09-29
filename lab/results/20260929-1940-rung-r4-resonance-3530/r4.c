/* Rung r4: does the design's event layer (exact Kepler cycles + one analytic
 * tidal kick per conjunction) reproduce mean-motion-resonance behaviour?
 *
 * Scene (restricted, coplanar, G=1): central m0=1, outer perturber m2=3e-3 on a
 * fixed Kepler ellipse, inner test particle. Truth = dense barycentric
 * velocity-Verlet N-body at 600/1200/2400 steps per inner orbit.
 *
 * Kick (frozen before any run): at each conjunction (lambda1 = lambda2, exact
 * Kepler ephemerides), both paths are linearized about the conjunction state
 * and the multipole tidal acceleration of m2 (l=2, optionally +l=3; the l<=1
 * part cancels the indirect term exactly) is integrated in closed form over
 * (-inf, inf) via Beta-function integrals. No dense N-body integration
 * anywhere in the event layer.
 *
 * configs: conj-quad (l=2), conj-oct (l=2+3), averaged (phase-averaged l=2
 * kernel, H0190-K2 style), none (pure Kepler).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define PI 3.14159265358979323846
static const double G  = 1.0;
static const double M0 = 1.0;
static const double M2 = 3.0e-3;
static const double M1 = 0.0;
static const double MTOT = 1.0 + 3.0e-3;

enum { CFG_NONE = 0, CFG_AVG = 1, CFG_QUAD = 2, CFG_OCT = 3 };
static const char* CFGNAME[4] = {"none", "averaged", "conj-quad", "conj-oct"};

typedef struct { double a, e, w, M0, t0, mu; } Orb;

static double orb_n(const Orb*o){ return sqrt(o->mu/(o->a*o->a*o->a)); }

static double solveE(double M, double e){
  double E = (e < 0.8) ? M : PI;
  for (int i = 0; i < 200; i++){
    double f = E - e*sin(E) - M, fp = 1.0 - e*cos(E);
    double d = f/fp; E -= d;
    if (fabs(d) < 1e-15) break;
  }
  return E;
}
static void orb_state(const Orb*o, double t, double r[2], double v[2]){
  double n = orb_n(o);
  double M = o->M0 + n*(t - o->t0);
  M = fmod(M, 2*PI); if (M < 0) M += 2*PI;
  double E = solveE(M, o->e);
  double cE = cos(E), sE = sin(E), sq = sqrt(1 - o->e*o->e);
  double x  = o->a*(cE - o->e), y = o->a*sq*sE;
  double Ed = n/(1 - o->e*cE);
  double vx = -o->a*sE*Ed, vy = o->a*sq*cE*Ed;
  double cw = cos(o->w), sw = sin(o->w);
  r[0] = cw*x - sw*y;  r[1] = sw*x + cw*y;
  v[0] = cw*vx - sw*vy; v[1] = sw*vx + cw*vy;
}
static double ecn_f(double M, double e){          /* nu - M, M principal */
  double E = solveE(M, e);
  double nu = 2.0*atan2(sqrt(1+e)*sin(0.5*E), sqrt(1-e)*cos(0.5*E));
  return nu - M;
}
static double orb_lam_u(const Orb*o, double t){   /* unwrapped longitude */
  double n = orb_n(o);
  double M = o->M0 + n*(t - o->t0);
  double Mc = fmod(M, 2*PI); if (Mc < 0) Mc += 2*PI;
  return o->w + M + ecn_f(Mc, o->e);
}
static void rv2el(const double r[2], const double v[2], double mu, double t_now, Orb*o){
  double R = hypot(r[0], r[1]);
  double v2 = v[0]*v[0] + v[1]*v[1];
  double rv = r[0]*v[0] + r[1]*v[1];
  double a = 1.0/(2.0/R - v2/mu);
  double ex = (v2/mu - 1.0/R)*r[0] + rv/mu*v[0];
  double ey = (v2/mu - 1.0/R)*r[1] + rv/mu*v[1];
  double e = hypot(ex, ey);
  double w = (e > 1e-12) ? atan2(ey, ex) : 0.0;
  double nu = (e > 1e-12) ? atan2(ex*r[1]-ey*r[0], ex*r[0]+ey*r[1]) : atan2(r[1],r[0]);
  double E = 2.0*atan2(sqrt(1-e)*sin(0.5*nu), sqrt(1+e)*cos(0.5*nu));
  double M = E - e*sin(E);
  o->a=a; o->e=e; o->w=w; o->M0=M; o->t0=t_now; o->mu=mu;
}

/* ---- closed-form multipole tidal kick (interior source) ---------------- */
/* Body 1 (pumped, exterior, position P) is perturbed by m2 (interior, Q).
 * The kick is the phase-dependent tide at multipole order lmax (2 or 3),
 * the l<=1 part being axisymmetric/indirect and owned by the averaged layer:
 *   a2 = Gm2 [ 3(Q.P)Q + 1.5|Q|^2 P ]/|P|^5  - 7.5 Gm2 (Q.P)^2 P/|P|^7
 *   a3 = 1.5 Gm2 { [5(Q.P)^2 - |Q|^2|P|^2] Q/|P|^7
 *                 + [5|Q|^2(Q.P)|P|^2 - (35/3)(Q.P)^3] P/|P|^9 }
 * Both paths are linearized at the conjunction; the time integral over
 * (-inf,inf) is closed-form: numerator polynomial over D(t)^{n/2} with
 * D quadratic -> shift to vertex, even part, Beta integrals.
 */
static double qint(double m, double n, double c2, double delta){
  return pow(c2,-m-0.5)*pow(delta,m+0.5-n)*tgamma(m+0.5)*tgamma(n-m-0.5)/tgamma(n);
}
/* integral of F(t)/D(t)^(n/2), F polynomial (coeffs t^0..deg), D=c0+c1t+c2t^2 */
static double poly_int(double*F,int deg,double n,double c0,double c1,double c2){
  double mu=-c1/(2*c2), delta=c0-c1*c1/(4*c2);
  double tot=0;
  static long long C[8][8];
  static int init=0;
  if(!init){ for(int i=0;i<8;i++){C[i][0]=1;for(int j=1;j<=i;j++)C[i][j]=C[i-1][j-1]+C[i-1][j];} init=1; }
  for (int k=0;k<=deg;k+=2){
    double coef=0;
    for (int j=k;j<=deg;j++) coef += F[j]*C[j][k]*pow(mu,j-k);
    tot += coef*qint(0.5*k,n,c2,delta);
  }
  return tot;
}
static void tidal_kick(const double r1[2], const double v1[2],
                       const double r2[2], const double v2[2],
                       double gm2, int lmax, double dv[2]){
  double u[2]={r1[0],r1[1]}, wv[2]={v1[0],v1[1]};   /* P path (exterior body) */
  double x[2]={r2[0],r2[1]}, y[2]={v2[0],v2[1]};    /* Q path (interior m2)   */
  /* P2 = |P|^2, Q2 = |Q|^2, SP = Q.P (all deg-2 polys in t) */
  double P2[3]={u[0]*u[0]+u[1]*u[1], 2*(u[0]*wv[0]+u[1]*wv[1]), wv[0]*wv[0]+wv[1]*wv[1]};
  double Q2[3]={x[0]*x[0]+x[1]*x[1], 2*(x[0]*y[0]+x[1]*y[1]), y[0]*y[0]+y[1]*y[1]};
  double SP[3];
  SP[0]=u[0]*x[0]+u[1]*x[1];
  SP[1]=u[0]*y[0]+u[1]*y[1]+wv[0]*x[0]+wv[1]*x[1];
  SP[2]=wv[0]*y[0]+wv[1]*y[1];
  dv[0]=0.0; dv[1]=0.0;
  for (int i=0;i<2;i++){
    /* N2a = 3 SP*Q_i + 1.5 Q2*P_i  (deg 3) over |P|^5 */
    double N2a[4]={0,0,0,0};
    for (int k=0;k<4;k++){
      if(k<3) N2a[k]+=3.0*SP[k]*x[i]+1.5*Q2[k]*u[i];
      if(k>=1) N2a[k]+=3.0*SP[k-1]*y[i]+1.5*Q2[k-1]*wv[i];
    }
    double val = gm2*poly_int(N2a,3,2.5,P2[0],P2[1],P2[2]);
    /* N2b = 7.5 SP^2 * P_i (deg 4) over |P|^7 */
    double SP2[5];
    SP2[0]=SP[0]*SP[0]; SP2[1]=2*SP[0]*SP[1]; SP2[2]=SP[1]*SP[1]+2*SP[0]*SP[2];
    SP2[3]=2*SP[1]*SP[2]; SP2[4]=SP[2]*SP[2];
    double P1lin[2]={u[i],wv[i]};
    double N2bP[6]={0,0,0,0,0,0};
    for (int k=0;k<6;k++){ if(k<5) N2bP[k]+=7.5*SP2[k]*P1lin[0]; if(k>=1) N2bP[k]+=7.5*SP2[k-1]*P1lin[1]; }
    val -= gm2*poly_int(N2bP,5,3.5,P2[0],P2[1],P2[2]);
    if (lmax>=3){
      /* N3a = [5 SP^2 - Q2*P2] * Q_i (deg 5) over |P|^7 */
      double B3[5];
      for (int k=0;k<5;k++){ B3[k]=5.0*SP2[k]; }
      double Q2P2[5]={0,0,0,0,0};
      for (int k=0;k<5;k++){ for (int m=0;m<3;m++){ int l=k-m; if(l>=0&&l<3) Q2P2[k]+=Q2[m]*P2[l]; } }
      for (int k=0;k<5;k++) B3[k]-=Q2P2[k];
      double N3a[6]={0,0,0,0,0,0};
      for (int k=0;k<6;k++){ if(k<5)N3a[k]+=B3[k]*x[i]; if(k>=1)N3a[k]+=B3[k-1]*y[i]; }
      double oct = 1.5*gm2*poly_int(N3a,5,3.5,P2[0],P2[1],P2[2]);
      /* N3b = [5 Q2 SP P2 - (35/3) SP^3] * P_i (deg 7) over |P|^9 */
      double Q2SP[5]={0,0,0,0,0};
      for (int k=0;k<5;k++){ for (int m=0;m<3;m++){ int l=k-m; if(l>=0&&l<3) Q2SP[k]+=Q2[m]*SP[l]; } }
      double A4[7]={0,0,0,0,0,0,0};
      for (int k=0;k<7;k++){ for (int m=0;m<5;m++){ int l=k-m; if(l>=0&&l<3) A4[k]+=Q2SP[m]*P2[l]; } }
      for (int k=0;k<7;k++) A4[k]*=5.0;
      double SP3[7];
      for (int k=0;k<7;k++) SP3[k]=0;
      /* SP^3 = SP2 * SP */
      for (int k=0;k<7;k++){ for (int m=0;m<5;m++){ int l=k-m; if(l>=0&&l<3) SP3[k]+=SP2[m]*SP[l]; } }
      for (int k=0;k<7;k++) A4[k]-=(35.0/3.0)*SP3[k];
      double N3b[8]={0,0,0,0,0,0,0,0};
      for (int k=0;k<8;k++){ if(k<7)N3b[k]+=A4[k]*P1lin[0]; if(k>=1)N3b[k]+=A4[k-1]*P1lin[1]; }
      oct += 1.5*gm2*poly_int(N3b,7,4.5,P2[0],P2[1],P2[2]);
      val += oct;
    }
    dv[i]=val;
  }
}
/* exact accelerations on linear paths, for the self-test */
static void a_exact_lin(const double r1[2],const double v1[2],const double r2[2],const double v2[2],
                        double gm2, int lmax, double t, double a[2]){
  double p[2]={r1[0]+v1[0]*t, r1[1]+v1[1]*t};
  double q[2]={r2[0]+v2[0]*t, r2[1]+v2[1]*t};
  double sp=q[0]*p[0]+q[1]*p[1], p2=p[0]*p[0]+p[1]*p[1], q2=q[0]*q[0]+q[1]*q[1];
  double pm=sqrt(p2), pm5=pm*pm*pm*pm*pm, pm7=pm5*p2, pm9=pm7*p2;
  for (int i=0;i<2;i++){
    a[i] = gm2*(3.0*sp*q[i]+1.5*q2*p[i])/pm5 - gm2*7.5*sp*sp*p[i]/pm7;
    if (lmax>=3)
      a[i] += 1.5*gm2*((5.0*sp*sp-q2*p2)*q[i]/pm7
                       +(5.0*q2*sp*p2-(35.0/3.0)*sp*sp*sp)*p[i]/pm9);
  }
}

/* ---- conjunction finder ------------------------------------------------- */
static double lam_diff(const Orb*o1, const Orb*o2, double t){
  return orb_lam_u(o2,t) - orb_lam_u(o1,t);
}
static double next_conj(const Orb*o1, const Orb*o2, double t_now){
  double n1 = orb_n(o1), n2 = orb_n(o2);
  double Tsyn = 2*PI/fabs(n1-n2);
  double Dnow = lam_diff(o1,o2,t_now);
  double target = (floor((Dnow + 0.05)/(2*PI)) + 1.0)*2*PI;   /* margin > kick-induced lambda jump */
  double tlo = t_now, thi = t_now + 1.9*Tsyn;
  int N = 200;
  double prev_t = tlo, prev_f = lam_diff(o1,o2,tlo) - target;
  for (int i=1;i<=N;i++){
    double t = t_now + (thi-t_now)*i/N;
    double f = lam_diff(o1,o2,t) - target;
    if (prev_f < 0 && f >= 0){
      double a=prev_t, b=t;
      for (int k=0;k<200;k++){
        double m=0.5*(a+b);
        double fm = lam_diff(o1,o2,m) - target;
        if (fm < 0) a = m; else b = m;
      }
      double r=0.5*(a+b); return (r>t_now+1e-12)? r : t_now+1e-9;
    }
    prev_t=t; prev_f=f;
  }
  return -1.0;
}

/* ---- scene -------------------------------------------------------------- */
typedef struct { const char* name; double Prat, w2; } CaseDef;
static const CaseDef CASES[5] = {
  {"r21",  2.0,  0.0},   /* resonant, as the red-team ran it */
  {"r21b", 2.0,  4.0},   /* phase-shifted (w2 = 4.0) */
  {"p5",   5.0,  0.0},   /* controls */
  {"p255", 2.55, 0.0},
  {"p215", 2.15, 0.0},
};
static double E1_0 = 0.05;          /* inner start eccentricity (inner at pericentre, w1=M1=0) */
static double E2_0 = 0.0;           /* outer eccentricity */
static double M2PH = PI;            /* outer start phase: lambda2(0) = w2 + M2PH (e2=0) */
static double PRAT_OVR = 0.0;       /* >0: override the case's period ratio (scene scan) */
static const int    RESO[2] = {0, 1};                      /* which cases are resonant */
#define NSAMP 4096
static const int SYNODIC_N = 200;

static void scene(int ci, Orb*o1, Orb*o2, double*Tend, double*Tsyn){
  double Prat = CASES[ci].Prat;                  /* P1/P2: pumped body exterior */
  double n2 = sqrt(G*MTOT);                      /* a2 = 1 -> perturber */
  double n1 = n2/Prat;
  double a1 = cbrt(G*M0/(n1*n1));
  o1->a=a1;  o1->e=E1_0; o1->w=0.0; o1->M0=0.0; o1->t0=0.0; o1->mu=G*M0;
  o2->a=1.0; o2->e=E2_0; o2->w=CASES[ci].w2; o2->M0=M2PH; o2->t0=0.0; o2->mu=G*MTOT;
  *Tsyn = 2*PI/(n2-n1);
  *Tend = SYNODIC_N*(*Tsyn);
}

/* ---- osculating quantities from a heliocentric state -------------------- */
static void osc(double r[2], double v[2], double mu, double*ecc, double*wret, double*lam){
  double R = hypot(r[0],r[1]);
  double v2 = v[0]*v[0]+v[1]*v[1];
  double rv = r[0]*v[0]+r[1]*v[1];
  double ex = (v2/mu - 1.0/R)*r[0] + rv/mu*v[0];
  double ey = (v2/mu - 1.0/R)*r[1] + rv/mu*v[1];
  *ecc = hypot(ex,ey);
  *wret = atan2(ey,ex);
  *lam = atan2(r[1],r[0]);
}
static double wrap_pi(double x){
  x = fmod(x+PI, 2*PI); if (x<0) x += 2*PI; return x - PI;
}

/* ---- event layer -------------------------------------------------------- */
static void run_event(int ci, int config, double*T, double*E, double*TH, long*events, int*ok){
  Orb o1, o2; double Tend, Tsyn;
  scene(ci,&o1,&o2,&Tend,&Tsyn);
  double t = 0.0; long ev = 0; *ok = 1;
  double r1[2],v1[2],r2[2],v2[2];
  for (int k=0;k<NSAMP;k++){
    double tk = Tend*k/(NSAMP-1.0);
    if (config != CFG_NONE){
      for (;;){
        double tc = next_conj(&o1,&o2,t);
        if (tc < 0){ fprintf(stderr,"NC-1 cfg=%d case=%s ev=%ld t=%.6f a=%.4f e=%.4f\n",config,CASES[ci].name,ev,t,o1.a,o1.e); *ok = 0; break; }
        if (tc > tk) break;
        orb_state(&o1,tc,r1,v1); orb_state(&o2,tc,r2,v2);
        double dv[2] = {0,0};
        if (config==CFG_QUAD) tidal_kick(r1,v1,r2,v2,G*M2,2,dv);
        else if (config==CFG_OCT) tidal_kick(r1,v1,r2,v2,G*M2,3,dv);
        else if (config==CFG_AVG){
          /* orbit-averaged quadrupole kick (H0190 K2): same kernel averaged
             over the inner's phase at the conjunction */
          double lam_c = orb_lam_u(&o1,tc);
          double acc[2]={0,0}; int NAVG=64;
          for (int j=0;j<NAVG;j++){
            double phi = 2*PI*(j+0.5)/NAVG;
            Orb ot = o1; ot.w += phi;
            double M = lam_c - ot.w;
            M = fmod(M,2*PI); if (M<0) M += 2*PI;
            for (int it=0; it<100; it++){
              double g = ot.w + M + ecn_f(M,ot.e) - lam_c;
              double h = 1e-7, Mp = fmod(M+h,2*PI); if (Mp<0) Mp+=2*PI;
              double g2 = ot.w + Mp + ecn_f(Mp,ot.e) - lam_c;
              double d = g/((g2-g)/h);
              M -= d; M = fmod(M,2*PI); if (M<0) M+=2*PI;
              if (fabs(d)<1e-13) break;
            }
            ot.M0 = M; ot.t0 = tc;
            double rr[2],vv[2]; orb_state(&ot,tc,rr,vv);
            double dj[2]; tidal_kick(rr,vv,r2,v2,G*M2,2,dj);
            acc[0]+=dj[0]; acc[1]+=dj[1];
          }
          dv[0]=acc[0]/NAVG; dv[1]=acc[1]/NAVG;
        }
        v1[0]+=dv[0]; v1[1]+=dv[1];
        double Mbef = o1.M0 + orb_n(&o1)*(tc - o1.t0);
        rv2el(r1,v1,G*M0,tc,&o1);
        o1.M0 += 2*PI*round((Mbef - o1.M0)/(2*PI));   /* keep M unwrapped */
        t = tc; ev++;
        if (o1.e > 0.9 || o1.a*(1.0-o1.e) < 1.1*o2.a*(1.0+o2.e) || ev > 20000){ *ok = 0; break; }
      }
    }
    orb_state(&o1,tk,r1,v1); orb_state(&o2,tk,r2,v2);
    double ecc,w1,lam1;
    osc(r1,v1,G*M0,&ecc,&w1,&lam1);
    double lam2 = atan2(r2[1],r2[0]);
    TH[k] = wrap_pi(2.0*lam1 - lam2 - w1);
    T[k]=tk; E[k]=ecc;
  }
  *events = ev;
}

/* ---- dense truth -------------------------------------------------------- */
static void accel(const double r0[2],const double r1[2],const double r2[2], double a0[2],double a1[2],double a2[2]){
  double d02x=r2[0]-r0[0], d02y=r2[1]-r0[1], d02=cbrt(d02x*d02x+d02y*d02y);
  d02 = d02*d02*d02;
  double d01x=r0[0]-r1[0], d01y=r0[1]-r1[1], d01=sqrt(d01x*d01x+d01y*d01y);
  d01 = d01*d01*d01;
  double d12x=r2[0]-r1[0], d12y=r2[1]-r1[1], d12=sqrt(d12x*d12x+d12y*d12y);
  d12 = d12*d12*d12;
  a0[0]=G*M2*d02x/d02; a0[1]=G*M2*d02y/d02;
  a2[0]=G*M0*(-d02x)/d02; a2[1]=G*M0*(-d02y)/d02;
  a1[0]=G*M0*d01x/d01 + G*M2*d12x/d12; a1[1]=G*M0*d01y/d01 + G*M2*d12y/d12;
}
static void run_truth(int ci, double steps_per_orbit, double*T,double*E,double*TH, long*nsteps, double*de){
  Orb o1,o2; double Tend,Tsyn;
  scene(ci,&o1,&o2,&Tend,&Tsyn);
  double rr[2],vr[2],r1h[2],v1h[2];
  orb_state(&o2,0.0,rr,vr);
  double r0[2]={-M2/MTOT*rr[0],-M2/MTOT*rr[1]}, v0[2]={-M2/MTOT*vr[0],-M2/MTOT*vr[1]};
  double r2[2]={ M0/MTOT*rr[0], M0/MTOT*rr[1]}, v2[2]={ M0/MTOT*vr[0], M0/MTOT*vr[1]};
  orb_state(&o1,0.0,r1h,v1h);
  double r1[2]={r0[0]+r1h[0],r0[1]+r1h[1]}, v1[2]={v0[0]+v1h[0],v0[1]+v1h[1]};
  /* total energy of the (m0,m2, massless particle) system, for drift diagnostics */
  double Einit;
  {
    double dx=r2[0]-r0[0], dy=r2[1]-r0[1];
    double vpx=v1[0], vpy=v1[1];
    double d1=sqrt((r1[0]-r0[0])*(r1[0]-r0[0])+(r1[1]-r0[1])*(r1[1]-r0[1]));
    double d12=sqrt((r1[0]-r2[0])*(r1[0]-r2[0])+(r1[1]-r2[1])*(r1[1]-r2[1]));
    Einit = 0.5*M0*(v0[0]*v0[0]+v0[1]*v0[1]) + 0.5*M2*(v2[0]*v2[0]+v2[1]*v2[1])
          - G*M0*M2/sqrt(dx*dx+dy*dy)
          + 0.5*(vpx*vpx+vpy*vpy) - G*M0/d1 - G*M2/d12;
  }
  double dt = 2*PI/(steps_per_orbit*(orb_n(&o1)/(2*PI)));  /* steps per pumped-body orbit */
  long N = (long)ceil(Tend/dt);
  long stride = N/NSAMP; if (stride < 1) stride = 1;
  double a0[2],a1[2],a2[2];
  accel(r0,r1,r2,a0,a1,a2);
  int si = 0;
  double Emax_drift = 0.0;
  for (long st=0; st<N; st++){
    r0[0]+=v0[0]*dt+0.5*a0[0]*dt*dt; r0[1]+=v0[1]*dt+0.5*a0[1]*dt*dt;
    r1[0]+=v1[0]*dt+0.5*a1[0]*dt*dt; r1[1]+=v1[1]*dt+0.5*a1[1]*dt*dt;
    r2[0]+=v2[0]*dt+0.5*a2[0]*dt*dt; r2[1]+=v2[1]*dt+0.5*a2[1]*dt*dt;
    double an0[2]={a0[0],a0[1]}, an1[2]={a1[0],a1[1]}, an2[2]={a2[0],a2[1]};
    accel(r0,r1,r2,a0,a1,a2);
    v0[0]+=0.5*(an0[0]+a0[0])*dt; v0[1]+=0.5*(an0[1]+a0[1])*dt;
    v1[0]+=0.5*(an1[0]+a1[0])*dt; v1[1]+=0.5*(an1[1]+a1[1])*dt;
    v2[0]+=0.5*(an2[0]+a2[0])*dt; v2[1]+=0.5*(an2[1]+a2[1])*dt;
    if ((st+1)%stride==0 && si<NSAMP){
      double rh[2]={r1[0]-r0[0],r1[1]-r0[1]}, vh[2]={v1[0]-v0[0],v1[1]-v0[1]};
      double r2h[2]={r2[0]-r0[0],r2[1]-r0[1]};
      double ecc,w1,lam1;
      osc(rh,vh,G*M0,&ecc,&w1,&lam1);
      double lam2=atan2(r2h[1],r2h[0]);
      T[si]=(st+1)*dt; E[si]=ecc; TH[si]=wrap_pi(2.0*lam1-lam2-w1);
      si++;
    }
  }
  /* energy drift at end */
  {
    double d02=sqrt((r2[0]-r0[0])*(r2[0]-r0[0])+(r2[1]-r0[1])*(r2[1]-r0[1]));
    double d1=sqrt((r1[0]-r0[0])*(r1[0]-r0[0])+(r1[1]-r0[1])*(r1[1]-r0[1]));
    double d12=sqrt((r1[0]-r2[0])*(r1[0]-r2[0])+(r1[1]-r2[1])*(r1[1]-r2[1]));
    double Efin = 0.5*M0*(v0[0]*v0[0]+v0[1]*v0[1]) + 0.5*M2*(v2[0]*v2[0]+v2[1]*v2[1])
                - G*M0*M2/d02
                + 0.5*(v1[0]*v1[0]+v1[1]*v1[1]) - G*M0/d1 - G*M2/d12;
    Emax_drift = fabs(Efin-Einit)/fabs(Einit);
  }
  for (int j=si;j<NSAMP;j++){ T[j]=Tend; E[j]=E[si-1]; TH[j]=TH[si-1]; }
  *nsteps = N; *de = Emax_drift;
}

/* ---- metrics ------------------------------------------------------------ */
static double max_e(const double*E){ double m=-1; for(int i=0;i<NSAMP;i++) if(!isnan(E[i]) && E[i]>m) m=E[i]; return m; }
static double concentr(const double*TH){
  double cr=0,ci=0; int n=0;
  for(int i=0;i<NSAMP;i++){ if(isnan(TH[i])) continue; cr+=cos(TH[i]); ci+=sin(TH[i]); n++; }
  return n ? hypot(cr,ci)/n : 0.0;   /* diverged run -> 0 concentration */
}

int main(int argc, char**argv){
  if (argc>1 && !strcmp(argv[1],"--selftest")){
    /* closed-form kick vs trapezoid on the same linear paths */
    srand(42);
    double worst=0;
    for (int trial=0; trial<24; trial++){
      double r1[2],v1[2],r2[2],v2[2];
      r1[0]=1.0+0.3*(rand()/(double)RAND_MAX-0.5); r1[1]=0.3*(rand()/(double)RAND_MAX-0.5);
      v1[0]=0.1*(rand()/(double)RAND_MAX-0.5); v1[1]=1.0+0.1*(rand()/(double)RAND_MAX-0.5);
      double sep = 0.5+0.3*rand()/(double)RAND_MAX;
      double ang = 2*PI*rand()/(double)RAND_MAX;
      r2[0]=r1[0]+sep*cos(ang); r2[1]=r1[1]+sep*sin(ang);
      v2[0]=0.1*(rand()/(double)RAND_MAX-0.5); v2[1]=0.8+0.1*(rand()/(double)RAND_MAX-0.5);
      int lmax = 2 + (trial%2);
      double dv[2]; tidal_kick(r1,v1,r2,v2,G*M2,lmax,dv);
      double L=30000.0, num[2]={0,0};
      int NS=15000000; double h=2*L/NS;
      for (int i=0;i<NS;i++){
        double t=-L+(i+0.5)*h; double a[2]; a_exact_lin(r1,v1,r2,v2,G*M2,lmax,t,a);
        num[0]+=a[0]*h; num[1]+=a[1]*h;
      }
      double err = hypot(dv[0]-num[0],dv[1]-num[1])/fmax(hypot(num[0],num[1]),0.02);
      if (err>0.02)
        printf("trial %d lmax=%d err=%.3e |num|=%.3e P=(%.3f,%.3f) Vp=(%.3f,%.3f) Q=(%.3f,%.3f) Vq=(%.3f,%.3f) dv=(%.6e,%.6e) num=(%.6e,%.6e)\n",
               trial,lmax,err,hypot(num[0],num[1]),r1[0],r1[1],v1[0],v1[1],r2[0],r2[1],v2[0],v2[1],dv[0],dv[1],num[0],num[1]);
      if (err>worst) worst=err;
    }
    printf("selftest closed-form vs trapezoid: worst rel err %.3e\n", worst);
    return 0;
  }
  int nc = 5;
  static double Tt[5][NSAMP], Et[5][NSAMP], THt[5][NSAMP];
  double tmax_e[5][3], tC[5][3];
  long ns; double de;
  double steps[3] = {600,1200,2400};
  for (int ci=0; ci<nc; ci++){
    for (int r=0;r<3;r++){
      run_truth(ci, steps[r], Tt[ci], Et[ci], THt[ci], &ns, &de);
      tmax_e[ci][r]=max_e(Et[ci]); tC[ci][r]=concentr(THt[ci]);
      printf("truth %s steps/orbit %5.0f: N=%ld max_e=%.6f C=%.4f dE/E=%.2e\n",
             CASES[ci].name, steps[r], ns, tmax_e[ci][r], tC[ci][r], de);
      fflush(stdout);
      if (r==2){
        char fn[256]; snprintf(fn,sizeof fn,"data/%s.truth2400.csv",CASES[ci].name);
        FILE*f=fopen(fn,"w");
        for (int i=0;i<NSAMP;i++) fprintf(f,"%.10g,%.10g,%.10g\n",Tt[ci][i],Et[ci][i],THt[ci][i]);
        fclose(f);
      }
    }
  }
  
  double law_max[4][5], law_C[4][5]; long law_ev[4][5]; int law_ok[4][5];
  for (int cfg=0; cfg<4; cfg++){
    for (int ci=0; ci<5; ci++){
      static double T[NSAMP],E[NSAMP],TH[NSAMP];
      run_event(ci,cfg,T,E,TH,&law_ev[cfg][ci],&law_ok[cfg][ci]);
      law_max[cfg][ci]=max_e(E); law_C[cfg][ci]=concentr(TH);
      printf("%-10s %s: max_e=%.6f C=%.4f events=%ld ok=%d kicks/orbit=%.3f\n",
             CFGNAME[cfg],CASES[ci].name,law_max[cfg][ci],law_C[cfg][ci],
             law_ev[cfg][ci],law_ok[cfg][ci],
             law_ev[cfg][ci]*(CASES[ci].Prat-1.0)/CASES[ci].Prat/SYNODIC_N);
      char fn[256]; snprintf(fn,sizeof fn,"data/%s.%s.csv",CASES[ci].name,CFGNAME[cfg]);
      FILE*fo=fopen(fn,"w");
      for (int i=0;i<NSAMP;i++) fprintf(fo,"%.10g,%.10g,%.10g\n",T[i],E[i],TH[i]);
      fclose(fo);
    }
  }
  /* metrics */
  double kicks_orb[5];
  for (int ci=0;ci<5;ci++) kicks_orb[ci] = law_ev[2][ci] * (CASES[ci].Prat-1.0)/CASES[ci].Prat / SYNODIC_N;
  /* median of kicks/orbit across cases (conj-quad cadence; avg identical, none=0) */
  double kq[5]; for(int i=0;i<5;i++) kq[i]=kicks_orb[i];
  for(int i=0;i<5;i++)for(int j=i+1;j<5;j++)if(kq[j]<kq[i]){double tmp=kq[i];kq[i]=kq[j];kq[j]=tmp;}
  double med_kicks = kq[2];
  printf("\nmetrics.json:\n");
  printf("{\n");
  for (int cfg=0; cfg<4; cfg++){
    double rmin=1e9, rmax=-1e9, lmin=1e9;
    for (int ri=0; ri<2; ri++){
      int ci=RESO[ri];
      double ratio = law_max[cfg][ci]/tmax_e[ci][2];
      if (ratio<rmin) rmin=ratio;
      if (ratio>rmax) rmax=ratio;
      double lr = (tC[ci][2]>1e-9)? law_C[cfg][ci]/tC[ci][2] : 0.0;
      if (lr<lmin) lmin=lr;
    }
    int passed=0;
    for (int ci=2; ci<5; ci++){
      double ratio = law_max[cfg][ci]/tmax_e[ci][2];
      if (0.8<=ratio && ratio<=1.25) passed++;
    }
    double km = (cfg==CFG_NONE)?0.0:med_kicks;
    printf("  \"%s\": {\"e_pump_ratio_min\": %.6g, \"e_pump_ratio_max\": %.6g, "
           "\"libration_ratio_min\": %.6g, \"control_pass_fraction\": %.6g, "
           "\"dense_steps\": 0, \"kicks_per_orbit\": %.6g}%s\n",
           CFGNAME[cfg], rmin, rmax, lmin, passed/3.0, km, cfg<3?",":"");
  }
  printf("}\n");
  /* per-case table for the dossier */
  printf("\ncase table (truth2400 | laws):\n");
  for (int ci=0; ci<5; ci++){
    printf("%s truth max_e=%.4f C=%.4f | ", CASES[ci].name, tmax_e[ci][2], tC[ci][2]);
    for (int cfg=3; cfg>=0; cfg--)
      printf("%s max_e=%.4f C=%.4f%s", CFGNAME[cfg], law_max[cfg][ci], law_C[cfg][ci], cfg?" | ":"");
    printf("\n");
  }
  return 0;
}
