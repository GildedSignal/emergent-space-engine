/* Premise red-team: can a cycle's stored derivatives absorb kicks by a multiply-add?
 * Law: 1PN Binet u'' = C + 3u^2 - u (G=c=M=1), C = 1/L^2, first integral
 *      w^2 = 2*C*u + 2u^3 - u^2 + K.   Truth: RK4 (h), kicks at each periapsis
 *      as element jumps with (u, u') continuous: C+=dC, K-=2*u_p*dC.
 * Design paths carry only the cycle map F(C,K) (apsidal advance per radial cycle):
 *   ignore     : F(C0,K0) forever                        (negative control)
 *   stale      : F0 + dF*(element offsets); one compile  (representation.md literal)
 *   bucketed q : memo keyed by quantized (C,K), fresh exact F+dF per bucket, linear inside
 *   recompile  : F(C,K) each cycle                       (positive control)
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

static double H_STEP = 1e-3;
static double CAP_PHI = 400.0;

static inline double acc(double u, double C){ return C + 3.0*u*u - u; }
static inline double P3(double u, double C, double K){ return 2*u*u*u - u*u + 2*C*u + K; }

/* periapsis root of P3 (the middle root, where P3' = 2*acc < 0), trig method */
static double peri_root(double C, double K){
  double a=2.0, b=-1.0;
  double P=(3.0*a*2.0*C - b*b)/(3.0*a*a);          /* 3ac-b^2 / 3a^2, c=2C */
  double Q=(2.0*b*b*b - 9.0*a*b*2.0*C + 27.0*a*a*K)/(27.0*a*a*a);
  double shift=b/(3.0*a);
  double mp=-P/3.0, r=sqrt(mp*mp*mp);
  double cl=(Q/2.0)/r; if(cl>1)cl=1; if(cl<-1)cl=-1;
  double best=-1;
  double th=acos(-cl)/3.0;
  for(int k=0;k<3;k++){
    double u=2.0*sqrt(mp)*cos(th-2.0*M_PI*k/3.0)-shift;
    for(int it=0; it<60; it++){            /* Newton polish */
      double f=P3(u,C,K), fp=6*u*u-2*u+2*C;
      if(fp==0) break;
      double un=u-f/fp;
      if(un<=0) break;
      if(fabs(un-u)<1e-16*(1+u)){ u=un; break; }
      u=un;
    }
    if(u>0 && fabs(P3(u,C,K))<1e-9*(1.0+fabs(K)) && 6*u*u-2*u+2*C<0 && u>best) best=u;
  }
  return best;   /* -1 if none: caller treats as failure */
}

static void rk4(double *u, double *w, double *phi, double h, double C){
  double k1u=*w,            k1w=acc(*u,C);
  double u2=*u+.5*h*k1u,    w2=*w+.5*h*k1w, k2u=w2, k2w=acc(u2,C);
  double u3=*u+.5*h*k2u,    w3=*w+.5*h*k2w, k3u=w3, k3w=acc(u3,C);
  double u4=*u+h*k3u,       w4=*w+h*k3w,    k4u=w4, k4w=acc(u4,C);
  *u+=h/6.*(k1u+2*k2u+2*k3u+k4u); *w+=h/6.*(k1w+2*k2w+2*k3w+k4w); *phi+=h;
}

/* from a turning point (ustart, 0): advance to next periapsis; returns dphi and
 * writes the periapsis u; -1 on cap/plunge. */
static double cycle_from(double C, double ustart, double *u_out){
  if(acc(ustart,C)>=0) return -1.0;   /* must start at a periapsis-type turning point */
  double u=ustart, w=0.0, phi=0.0;
  for(;;){
    double up=u, wp=w, pp=phi;
    rk4(&u,&w,&phi,H_STEP,C);
    if(w<=0.0 && wp>0.0){
      double a0=acc(up,C), a1=acc(u,C), lo=0, hi=1, s=.5;
      for(int k=0;k<80;k++){
        double s2=s*s, s3=s2*s;
        double wv=wp*(2*s3-3*s2+1)+H_STEP*a0*(s3-2*s2+s)+w*(-2*s3+3*s2)+H_STEP*a1*(s3-s2);
        if(wv>0)lo=s;else hi=s; s=.5*(lo+hi);
      }
      double s2=s*s, s3=s2*s;
      if(u_out) *u_out = up*(2*s3-3*s2+1)+H_STEP*wp*(s3-2*s2+s)+u*(-2*s3+3*s2)+H_STEP*w*(s3-s2);
      return pp+s*H_STEP;
    }
    if(phi>CAP_PHI || !(u>0) || !isfinite(u)) return -1.0;
  }
}

static unsigned long rng_s=20261009UL;
static double urand(void){
  rng_s ^= rng_s<<13; rng_s ^= rng_s>>7; rng_s ^= rng_s<<17;
  return (double)((rng_s*0x2545F4914F6CDD1DUL)>>11)/9007199254740992.0;
}

typedef struct { double F, dFC, dFK; } Memo;


typedef struct { long kc, kk; Memo m; } Ent;
static Ent *tab; static long tab_n, tab_cap;

int main(int argc, char **argv){
  /* argv: p e eps sign(0=rand,1=sys) N q...
     q: -2 ignore, -1 stale, -3 recompile, >0 bucket width (relative) */
  double p=atof(argv[1]), e=atof(argv[2]), eps=atof(argv[3]);
  int sign_mode=atoi(argv[4]); long N=atol(argv[5]);
  double up0, C0, K0;
  { /* exact turning points: periapsis (1+e)/p and apoapsis (1-e)/p are both roots of P3 */
    double upt=(1+e)/p, uat=(1-e)/p;
    C0 = 0.5*((upt+uat) - 2.0*(upt*upt + upt*uat + uat*uat));
    K0 = -2*C0*upt - 2*upt*upt*upt + upt*upt;
    up0 = upt;
  }
  if(acc(up0,C0)>=0){ fprintf(stderr,"not a turning point\n"); return 2; }
  rng_s=20261009UL ^ (unsigned long)(p*1e6) ^ ((unsigned long)(e*1e7)<<12) ^ ((unsigned long)(sign_mode+1)<<28);
  double *dC_arr=malloc(sizeof(double)*N), *dK_arr=malloc(sizeof(double)*N);
  double *phi_true=malloc(sizeof(double)*(N+1));
  double u=up0, phi=0.0, C=C0, K=K0;
  double F0=cycle_from(C0,up0,NULL);
  long horizon=N;
  for(long i=0;i<N;i++){
    double up_i;
    double cyc=cycle_from(C,u,&up_i);
    if(cyc<0){ horizon=i; break; }
    phi+=cyc; phi_true[i+1]=phi; u=up_i;
    double s=2*urand()-1; if(sign_mode) s=1.0;
    double dC=eps*C0*s;
    dC_arr[i]=dC; dK_arr[i]=-2*up_i*dC;
    C+=dC; K+=dK_arr[i];
    if(C<=0 || acc(peri_root(C,K),C)>=0){ horizon=i+1; break; }
  }

  /* curvature of F in C at the base orbit (fixed ustart=root) */
  double hC=1e-4*fabs(C0);
  double Fm=cycle_from(C-hC,peri_root(C-hC,K0),NULL);
  double Fp=cycle_from(C+hC,peri_root(C+hC,K0),NULL);
  double curv=(Fm<0||Fp<0)?NAN:(Fp-2*F0+Fm)/(hC*hC);

  int nq=argc-6;
  for(int pi=0;pi<nq;pi++){
    double q=atof(argv[6+pi]);
    double Chat=C0, Khat=K0, Phi=0.0, maxerr=0, lasterr=0;
    unsigned long ncomp=0, nbuck=0;
    long hz=horizon;
    Memo m0={0,0,0};
    if(q==-2||q==-1){
      m0.F=F0;
      if(q==-1){
        double hc=1e-5*fabs(C0), hk=1e-5*fabs(K0);
        double FcP=cycle_from(C0+hc,peri_root(C0+hc,K0),NULL);
        double FcM=cycle_from(C0-hc,peri_root(C0-hc,K0),NULL);
        double FkP=cycle_from(C0,peri_root(C0,K0+hk),NULL);
        double FkM=cycle_from(C0,peri_root(C0,K0-hk),NULL);
        m0.dFC=(FcP-FcM)/(2*hc); m0.dFK=(FkP-FkM)/(2*hk); ncomp+=5;
      } else ncomp+=1;
    }
    tab_n=0; tab_cap=512; tab=malloc(tab_cap*sizeof(Ent));
    for(long i=0;i<hz;i++){
      double Frep=0;
      if(q==-2) Frep=m0.F;
      else if(q==-1) Frep=m0.F+m0.dFC*(Chat-C0)+m0.dFK*(Khat-K0);
      else if(q==-3){
        double f=cycle_from(Chat,peri_root(Chat,Khat),NULL);
        if(f<0){hz=i;break;} Frep=f; ncomp++;
      } else {
        double qC=q*C0, qK=q*fabs(K0);
        long kc=lround(Chat/qC), kk=lround(Khat/qK);
        Ent *hit=NULL;
        for(long j=0;j<tab_n;j++) if(tab[j].kc==kc&&tab[j].kk==kk){hit=&tab[j];break;}
        if(!hit){
          double Cc=kc*qC, Kk=kk*qK, ur=peri_root(Cc,Kk);
          double hc=1e-5*fabs(Cc), hk=1e-5*fabs(Kk);
          double Fb=cycle_from(Cc,ur,NULL);
          if(Fb<0){hz=i;break;}
          double FcP=cycle_from(Cc+hc,peri_root(Cc+hc,Kk),NULL);
          double FcM=cycle_from(Cc-hc,peri_root(Cc-hc,Kk),NULL);
          double FkP=cycle_from(Cc,peri_root(Cc,Kk+hk),NULL);
          double FkM=cycle_from(Cc,peri_root(Cc,Kk-hk),NULL);
          if(FcP<0||FcM<0||FkP<0||FkM<0){hz=i;break;}
          if(tab_n==tab_cap){tab_cap*=2;tab=realloc(tab,tab_cap*sizeof(Ent));}
          hit=&tab[tab_n++];
          hit->kc=kc; hit->kk=kk; hit->m.F=Fb;
          hit->m.dFC=(FcP-FcM)/(2*hc); hit->m.dFK=(FkP-FkM)/(2*hk);
          ncomp+=5; nbuck++;
        }
        Frep=hit->m.F+hit->m.dFC*(Chat-kc*qC)+hit->m.dFK*(Khat-kk*qK);
      }
      Phi+=Frep;
      double err=Phi-phi_true[i+1];
      if(fabs(err)>maxerr)maxerr=fabs(err);
      lasterr=err;
      Chat+=dC_arr[i]; Khat+=dK_arr[i];
    }
    printf("RESULT p=%.6g e=%.6g eps=%.3g sign=%d N=%ld q=%.3g F0=%.6f curv=%.4g maxerr=%.6g lasterr=%.6g ncomp=%lu nbuck=%lu horizon=%ld\n",
           p,e,eps,sign_mode,N,q,F0,curv,maxerr,lasterr,ncomp,nbuck,hz);
    free(tab);
  }
  printf("CURV p=%.6g e=%.6g F0=%.6f curv=%.6g\n",p,e,F0,curv);
  return 0;
}
