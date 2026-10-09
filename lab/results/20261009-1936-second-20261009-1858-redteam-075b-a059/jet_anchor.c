/* Second author: the design's ACTUAL policy (law.md:35) — the jet, re-anchored.
 * "strong-field reuse is the jet (exact offset plus stored derivatives), re-anchored:
 *  its error grows as C*drift^2 ... so when the accumulated offset reaches
 *  sqrt(floor/C) the cycle is recompiled exactly at the body's state"
 * Law (unchanged from 20261009-1858-redteam-075b/kick_absorb.c): 1PN Binet
 *   u'' = C + 3u^2 - u (G=c=M=1), C = 1/L^2, w^2 = 2Cu + 2u^3 - u^2 + K,
 *   kicks at each periapsis as element jumps with (u,u') continuous:
 *   dC = eps*C0*s, dK = -2*u_p*dC.  Kicks per orbit: KPO (default 32, H0190).
 * Paths:
 *   floor>0 : jet. Anchor (Ca,Ka) carries exact F, first derivatives and the
 *             clean Hessian (9-point stencil at the anchor, h_fd=1e-3*|C|).
 *             Per kick: update (C,K); trigger 0.5*|q2| > floor/margin ->
 *             recompile at the body's state (nanch++). Per orbit: consume
 *             Fhat = Fa + dF*(offset) at the pre-batch state (author's order).
 *             tmode=2: q2 = full d^T H d ; tmode=1: q2 = FCC*dC^2 (law.md's
 *             literal 1D "offset reaches sqrt(floor/C)").
 *   floor=0 : stale jet, never re-anchored (negative control).
 *   floor<0 : exact compile every orbit (positive control, author's q=-3).
 * Cost model: one compile = one exact radial cycle = cr crossing-evals,
 *   cr = 2*16*log2((1+e)/(1-e)) + 8  (law.md B9 at m=16). Derivative evals are
 *   free in the integer law (differentiated quadrature); not charged.
 * Usage: jet_anchor p e eps sign(0=rnd,1=sys) N_orbit floor margin seed \
 *           [hstep=1e-3] [kicks_per_orbit=32] [tmode=2]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

static double CAP_PHI = 400.0;

static inline double acc(double u, double C){ return C + 3.0*u*u - u; }
static inline double P3(double u, double C, double K){ return 2*u*u*u - u*u + 2*C*u + K; }

static double peri_root(double C, double K){
  double a=2.0, b=-1.0;
  double P=(3.0*a*2.0*C - b*b)/(3.0*a*a);
  double Q=(2.0*b*b*b - 9.0*a*b*2.0*C + 27.0*a*a*K)/(27.0*a*a*a);
  double shift=b/(3.0*a);
  double mp=-P/3.0, r=sqrt(mp*mp*mp);
  double cl=(Q/2.0)/r; if(cl>1)cl=1; if(cl<-1)cl=-1;
  double best=-1;
  double th=acos(-cl)/3.0;
  for(int k=0;k<3;k++){
    double u=2.0*sqrt(mp)*cos(th-2.0*M_PI*k/3.0)-shift;
    for(int it=0; it<60; it++){
      double f=P3(u,C,K), fp=6*u*u-2*u+2*C;
      if(fp==0) break;
      double un=u-f/fp;
      if(un<=0) break;
      if(fabs(un-u)<1e-16*(1+u)){ u=un; break; }
      u=un;
    }
    if(u>0 && fabs(P3(u,C,K))<1e-9*(1.0+fabs(K)) && 6*u*u-2*u+2*C<0 && u>best) best=u;
  }
  return best;
}

static void rk4(double *u, double *w, double *phi, double h, double C){
  double k1u=*w,            k1w=acc(*u,C);
  double u2=*u+.5*h*k1u,    w2=*w+.5*h*k1w, k2u=w2, k2w=acc(u2,C);
  double u3=*u+.5*h*k2u,    w3=*w+.5*h*k2w, k3u=w3, k3w=acc(u3,C);
  double u4=*u+h*k3u,       w4=*w+h*k3w,    k4u=w4, k4w=acc(u4,C);
  *u+=h/6.*(k1u+2*k2u+2*k3u+k4u); *w+=h/6.*(k1w+2*k2w+2*k3w+k4w); *phi+=h;
}

static double cycle_from_h(double C, double ustart, double *u_out, double h){
  if(acc(ustart,C)>=0) return -1.0;
  double u=ustart, w=0.0, phi=0.0;
  for(;;){
    double up=u, wp=w, pp=phi;
    rk4(&u,&w,&phi,h,C);
    if(w<=0.0 && wp>0.0){
      double a0=acc(up,C), a1=acc(u,C), lo=0, hi=1, s=.5;
      for(int k=0;k<80;k++){
        double s2=s*s, s3=s2*s;
        double wv=wp*(2*s3-3*s2+1)+h*a0*(s3-2*s2+s)+w*(-2*s3+3*s2)+h*a1*(s3-s2);
        if(wv>0)lo=s;else hi=s; s=.5*(lo+hi);
      }
      double s2=s*s, s3=s2*s;
      if(u_out) *u_out = up*(2*s3-3*s2+1)+h*wp*(s3-2*s2+s)+u*(-2*s3+3*s2)+h*w*(s3-s2);
      return pp+s*h;
    }
    if(phi>CAP_PHI || !(u>0) || !isfinite(u)) return -1.0;
  }
}

static unsigned long rng_s;
static double urand(void){
  rng_s ^= rng_s<<13; rng_s ^= rng_s>>7; rng_s ^= rng_s<<17;
  return (double)((rng_s*0x2545F4914F6CDD1DUL)>>11)/9007199254740992.0;
}

typedef struct {
  double Ca, Ka;
  double F, dFC, dFK;
  double FCC, FCK, FKK;
  long nanch;
  double Hmax;
} Jet;

static double fd_rel = 1e-3;
static int jet_compile(Jet *j, double C, double K, double h, double *Fdiag){
  double up = peri_root(C,K); if(up<=0) return 0;
  double hc = fd_rel*fabs(C), hk = fd_rel*fabs(K);
  double F0 = cycle_from_h(C, up, NULL, h);                 if(F0<0) return 0;
  double Cp = cycle_from_h(C+hc, peri_root(C+hc,K), NULL, h); if(Cp<0) return 0;
  double Cm = cycle_from_h(C-hc, peri_root(C-hc,K), NULL, h); if(Cm<0) return 0;
  double Kp = cycle_from_h(C, peri_root(C,K+hk), NULL, h);    if(Kp<0) return 0;
  double Km = cycle_from_h(C, peri_root(C,K-hk), NULL, h);    if(Km<0) return 0;
  double pp1 = cycle_from_h(C+hc, peri_root(C+hc,K+hk), NULL, h); if(pp1<0) return 0;
  double pm1 = cycle_from_h(C-hc, peri_root(C-hc,K-hk), NULL, h); if(pm1<0) return 0;
  double pp2 = cycle_from_h(C+hc, peri_root(C+hc,K-hk), NULL, h); if(pp2<0) return 0;
  double pm2 = cycle_from_h(C-hc, peri_root(C-hc,K+hk), NULL, h); if(pm2<0) return 0;
  j->Ca=C; j->Ka=K; j->F=F0;
  j->dFC=(Cp-Cm)/(2*hc); j->dFK=(Kp-Km)/(2*hk);
  j->FCC=(Cp-2*F0+Cm)/(hc*hc);
  j->FKK=(Kp-2*F0+Km)/(hk*hk);
  j->FCK=(pp1-pm1-pp2+pm2)/(4*hc*hk);
  if(fabs(j->FCC)>j->Hmax) j->Hmax=fabs(j->FCC);
  if(Fdiag) *Fdiag = F0;
  return 1;
}

int main(int argc, char **argv){
  if(argc<9){ fprintf(stderr,"args: p e eps sign N floor margin seed [h=1e-3] [kpo=32] [tmode=2]\n"); return 1; }
  double p=atof(argv[1]), e=atof(argv[2]), eps=atof(argv[3]);
  int sign_mode=atoi(argv[4]); long N=atol(argv[5]);
  double floor_=atof(argv[6]), margin=atof(argv[7]); unsigned long seed=strtoul(argv[8],NULL,10);
  double h = argc>9? atof(argv[9]):1e-3;
  long KPO = argc>10? atol(argv[10]):32;
  int tmode = argc>11? atoi(argv[11]):2;
  fd_rel = argc>12? atof(argv[12]):1e-3;

  double upt=(1+e)/p, uat=(1-e)/p;
  double C0 = 0.5*((upt+uat) - 2.0*(upt*upt + upt*uat + uat*uat));
  double K0 = -2*C0*upt - 2*upt*upt*upt + upt*upt;
  double up0 = upt;
  if(acc(up0,C0)>=0){ fprintf(stderr,"not a turning point\n"); return 2; }

  rng_s = 0x9E3779B97F4A7C15UL*seed ^ (unsigned long)(p*1e6) ^ ((unsigned long)(e*1e7)<<12);

  double *str = malloc(sizeof(double)*N*KPO);
  for(long i=0;i<N*KPO;i++){ double s=2*urand()-1; if(sign_mode) s=1.0; str[i]=s; }

  /* ---- truth (shared by all paths; author's order: advance, record, kick) ---- */
  double *phi_true = malloc(sizeof(double)*(N+1));
  double u=up0, phi=0.0, C=C0, K=K0;
  long horizon=N;
  for(long o=0;o<N;o++){
    double up_i;
    double cyc=cycle_from_h(C,u,&up_i,h);
    if(cyc<0){ horizon=o; break; }
    phi+=cyc; phi_true[o+1]=phi; u=up_i;
    double net=0; for(long j=0;j<KPO;j++) net+=str[o*KPO+j];
    double dC=eps*C0*net, dK=-2*up_i*dC;
    C+=dC; K+=dK;
    if(C<=0 || acc(peri_root(C,K),C)>=0){ horizon=o+1; break; }
  }

  double cr = 2.0*16.0*log2((1+e)/(1-e)) + 8.0;   /* crossings per compile (B9, m=16) */

  /* ---- paths: jet(m=1), jet(m=margin4), stale, exact ---- */
  double modes[4][2] = { {floor_,1}, {floor_,4}, {0,1}, {-1,1} };
  int nm = floor_>0 ? 4 : 2;
  for(int mi=0; mi<nm; mi++){
    double fl=modes[mi][0], mg=modes[mi][1];
    double Chat=C0, Khat=K0, Phi=0.0, maxerr=0, lasterr=0, maxcons=0;
    Jet j; memset(&j,0,sizeof(j));
    double Hbase=0;
    if(fl>=0){
      double Fx;
      if(!jet_compile(&j,C0,K0,h,&Fx)){ printf("COMPILE_FAIL p=%.6g e=%.6g\n",p,e); continue; }
      Hbase=j.FCC;
    }
    long hz=horizon; int fail=0;
    for(long o=0;o<hz;o++){
      /* consume the next cycle's advance from the PRE-batch state */
      double Frep;
      if(fl<0){
        double f=cycle_from_h(Chat,peri_root(Chat,Khat),NULL,h);
        if(f<0){ hz=o; break; }
        Frep=f;
      } else {
        Frep=j.F + j.dFC*(Chat-j.Ca) + j.dFK*(Khat-j.Ka);
        if(fl>0){
          double fx=cycle_from_h(Chat,peri_root(Chat,Khat),NULL,h);
          if(fx>0){ double ce=fabs(fx-Frep); if(ce>maxcons) maxcons=ce; }
        }
      }
      Phi+=Frep;
      double err=Phi-phi_true[o+1];
      if(fabs(err)>maxerr)maxerr=fabs(err);
      lasterr=err;
      /* the batch: KPO sub-kicks at this periapsis */
      double upb = peri_root(Chat,Khat);
      for(long jj=0;jj<KPO;jj++){
        double dCj=eps*C0*str[o*KPO+jj];
        Chat+=dCj; Khat+=-2*upb*dCj;
        if(fl>0){
          double dC=Chat-j.Ca, dK=Khat-j.Ka;
          double q2 = (tmode==1) ? j.FCC*dC*dC
                       : j.FCC*dC*dC + 2*j.FCK*dC*dK + j.FKK*dK*dK;
          if(0.5*fabs(q2) > fl/mg){
            if(!jet_compile(&j,Chat,Khat,h,NULL)){ hz=o; fail=1; break; }
            j.nanch++;
          }
        }
      }
      if(fail) break;
    }
    double apo = hz>0 ? (double)j.nanch/hz : 0;
    int saturated = (hz>0 && j.nanch >= 0.95*((double)KPO*hz));
    printf("JET p=%.6g e=%.6g s=%.4g eps=%.3g sign=%d floor=%.1g margin=%g tmode=%d seed=%lu KPO=%ld Norb=%ld hz=%ld "
           "nanch=%ld anch_per_orbit=%.4f cr=%.1f evals_per_orbit=%.1f maxerr=%.6g lasterr=%.6g maxcons=%.3g "
           "Hbase=%.4g Hmax=%.4g sat=%d\n",
           p,e,(p-6-2*e)/p,eps,sign_mode,fl,mg,tmode,seed,KPO,N,hz,
           j.nanch,apo,cr,apo*cr,maxerr,lasterr,maxcons,Hbase,j.Hmax,saturated);
  }
  return 0;
}
