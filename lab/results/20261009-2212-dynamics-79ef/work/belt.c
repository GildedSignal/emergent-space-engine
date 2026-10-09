/* belt.c — self-stirring planetesimal belt, direct O(N^2) leapfrog.
 * Primary (M=1) fixed at origin; belt bodies equal mass m.
 * Encounter = pair distance below f * mutual Hill radius (R_H = ((2m)/3)^{1/3} * (r_i+r_j)/2),
 * counted once per approach (flag with hysteresis release at g*f*R_H).
 * Logs every encounter: t, i, j, d/R_H, and heliocentric (a,e) of both bodies before/after.
 * Logs per-orbit diagnostics: t, e_rms, e_median, bound fraction, |dE/E|.
 * Build: gcc -O2 -march=native -o belt belt.c -lm
 * Usage: belt N seed m width e0 dt Torb f g outfile evfile [e0_hot]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>

static uint64_t rngstate;
static inline uint64_t rnd64(void){ rngstate ^= rngstate<<13; rngstate ^= rngstate>>7; rngstate ^= rngstate<<17; return rngstate; }
static inline double u01(void){ return (rnd64()>>11)*(1.0/9007199254740992.0); }

static void elements(double x,double y,double z,double vx,double vy,double vz,double*ae,double*ee){
  double r=sqrt(x*x+y*y+z*z), v2=vx*vx+vy*vy+vz*vz;
  *ae = 1.0/(2.0/r - v2);
  double hx=y*vz-z*vy, hy=z*vx-x*vz, hz=x*vy-y*vx;
  double ex=vy*hz-vz*hy - x/r, ey=vz*hx-vx*hz - y/r, ez=vx*hy-vy*hx - z/r;
  *ee=sqrt(ex*ex+ey*ey+ez*ez);
}

int main(int argc,char**argv){
  if(argc<12){fprintf(stderr,"args: N seed m width e0 dt Torb f g outfile evfile [e0_hot]\n");return 1;}
  int N=atoi(argv[1]); uint64_t seed=strtoull(argv[2],0,10); double m=atof(argv[3]);
  double width=atof(argv[4]); double e0=atof(argv[5]); double dt=atof(argv[6]);
  double Torb=atof(argv[7]); double f=atof(argv[8]); double g=atof(argv[9]);
  const char*outfile=argv[10]; const char*evfile=argv[11];
  if(argc>12) e0=atof(argv[12]); /* hot start overrides e0 */

  rngstate=seed*0x9E3779B97F4A7C15ULL+12345;
  for(int i=0;i<20;i++) rnd64();

  double *x=malloc(N*sizeof(double)),*y=malloc(N*sizeof(double)),*z=malloc(N*sizeof(double));
  double *vx=malloc(N*sizeof(double)),*vy=malloc(N*sizeof(double)),*vz=malloc(N*sizeof(double));
  double *ax=malloc(N*sizeof(double)),*ay=malloc(N*sizeof(double)),*az=malloc(N*sizeof(double));

  /* init: Rayleigh e (scale e0), i=e/2, random a in [1,1+width], random orientation & phase (E~M+e sinM, fine for e<=0.2) */
  for(int i=0;i<N;i++){
    double a=1.0+width*u01();
    double e=e0*sqrt(-2.0*log(1.0-0.999999*u01()+1e-12));
    if(e>0.9) e=0.9;
    double inc=0.5*e; double Om=2.0*M_PI*u01(); double om=2.0*M_PI*u01(); double M=2.0*M_PI*u01();
    double E=M+e*sin(M);
    double r=a*(1.0-e*cos(E));
    double n=sqrt(1.0/(a*a*a));
    /* velocity on osculating orbit: true anomaly from E */
    double cO=cos(Om),sO=sin(Om),co=cos(om),so=sin(om),ci=cos(inc),si=sin(inc);
    /* perifocal position/velocity */
    double sn=sqrt(1.0-e*e)*sin(E)/(1.0-e*cos(E)), cn=(cos(E)-e)/(1.0-e*cos(E));
    double px=r*cn, py=r*sn;
    double k=n*a/(1.0-e*cos(E));
    double vpx=-k*sin(E), vpy=k*sqrt(1.0-e*e)*cos(E);
    /* rotate: perifocal -> ecliptic via (Om, inc, om) */
    double m11=cO*co-sO*so*ci, m12=-cO*so-sO*co*ci, m21=sO*co+cO*so*ci, m22=-sO*so+cO*co*ci, m31=so*si, m32=co*si;
    x[i]=m11*px+m12*py; y[i]=m21*px+m22*py; z[i]=m31*px+m32*py;
    vx[i]=m11*vpx+m12*vpy; vy[i]=m21*vpx+m22*vpy; vz[i]=m31*vpx+m32*vpy;
  }

  long npr=N*(long)N;
  uint8_t*flag=calloc(npr,1);
  double T=Torb*2.0*M_PI;
  long nsteps=(long)(T/dt);
  double Cm=pow(2.0*m/3.0,1.0/3.0); /* (2m/3)^{1/3} */
  double eH= Cm; /* Hill eccentricity scale at a=1 */
  FILE*fev=fopen(evfile,"w");
  fprintf(fev,"# eH=%.6g f=%g g=%g N=%d m=%g width=%g dt=%g e0=%g seed=%llu\n",eH,f,g,N,m,width,dt,e0,(unsigned long long)seed);
  fprintf(fev,"t i j dRH a1b e1b a1a e1a a2b e2b a2a e2a\n");

  /* pending-release bookkeeping: flag[p]==2 -> pending, index stored in pend_idx */
  int cap=4096, npend=0;
  int *pi_=malloc(cap*sizeof(int)), *pj_=malloc(cap*sizeof(int));
  double *pt=malloc(cap*sizeof(double)),*pd=malloc(cap*sizeof(double));
  double *pa1b=malloc(cap*sizeof(double)),*pe1b=malloc(cap*sizeof(double)),*pa2b=malloc(cap*sizeof(double)),*pe2b=malloc(cap*sizeof(double));

  double E0=0; int E0set=0; long nev=0;
  FILE*fout=fopen(outfile,"w");
  fprintf(fout,"t e_rms e_med bound dE\n");

  /* accel + detection loop */
  #define ACCEL(DETECT) do{ \
    for(int i=0;i<N;i++){ax[i]=-x[i];ay[i]=-y[i];az[i]=-z[i];} \
    for(int i=0;i<N;i++){ \
      double xi=x[i],yi=y[i],zi=z[i], ri=sqrt(xi*xi+yi*yi+zi*zi); \
      for(int j=i+1;j<N;j++){ \
        double dx=x[j]-xi,dy=y[j]-yi,dz=z[j]-zi; double d2=dx*dx+dy*dy+dz*dz; \
        if(DETECT){ \
          double rj=sqrt(x[j]*x[j]+y[j]*y[j]+z[j]*z[j]); \
          double th=f*Cm*0.5*(ri+rj), th2=th*th, threl=g*th; \
          long p=(long)i*N+j; \
          if(flag[p]==2){ /* pending: released? */ \
            double dd=sqrt(d2); \
            if(dd>threl){ double a1,e1,a2,e2; elements(x[i],y[i],z[i],vx[i],vy[i],vz[i],&a1,&e1); elements(x[j],y[j],z[j],vx[j],vy[j],vz[j],&a2,&e2); \
              int k; for(k=0;k<npend;k++) if(pi_[k]==i&&pj_[k]==j) break; if(k<npend){ \
                fprintf(fev,"%.6f %d %d %.4f %.8f %.6f %.8f %.6f %.8f %.6f %.8f %.6f\n", pt[k],i,j,pd[k], pa1b[k],pe1b[k],a1,e1, pa2b[k],pe2b[k],a2,e2); nev++; \
                pi_[k]=pi_[npend-1];pj_[k]=pj_[npend-1];pt[k]=pt[npend-1];pd[k]=pd[npend-1]; \
                pa1b[k]=pa1b[npend-1];pe1b[k]=pe1b[npend-1];pa2b[k]=pa2b[npend-1];pe2b[k]=pe2b[npend-1]; npend--; flag[p]=0; } \
            } \
          } else if(d2<th2 && flag[p]==0){ \
            double dd=sqrt(d2); double a1,e1,a2,e2; \
            elements(x[i],y[i],z[i],vx[i],vy[i],vz[i],&a1,&e1); elements(x[j],y[j],z[j],vx[j],vy[j],vz[j],&a2,&e2); \
            if(npend==cap){cap*=2; pi_=realloc(pi_,cap*sizeof(int));pj_=realloc(pj_,cap*sizeof(int)); \
              pt=realloc(pt,cap*sizeof(double));pd=realloc(pd,cap*sizeof(double)); \
              pa1b=realloc(pa1b,cap*sizeof(double));pe1b=realloc(pe1b,cap*sizeof(double)); \
              pa2b=realloc(pa2b,cap*sizeof(double));pe2b=realloc(pe2b,cap*sizeof(double));} \
            pi_[npend]=i;pj_[npend]=j;pt[npend]=t_now;pd[npend]=dd/th; \
            pa1b[npend]=a1;pe1b[npend]=e1;pa2b[npend]=a2;pe2b[npend]=e2; npend++; flag[p]=2; \
          } \
        } \
        double inv=1.0/(d2*sqrt(d2)); double fx=dx*inv,fy=dy*inv,fz=dz*inv; \
        ax[i]-=m*fx;ay[i]-=m*fy;az[i]-=m*fz; \
        ax[j]+=m*fx;ay[j]+=m*fy;az[j]+=m*fz; \
      } \
    } \
  }while(0)

  double t_now=0;
  ACCEL(0); /* initial accel */
  for(long s=0;s<nsteps;s++){
    for(int i=0;i<N;i++){vx[i]+=0.5*dt*ax[i];vy[i]+=0.5*dt*ay[i];vz[i]+=0.5*dt*az[i];}
    for(int i=0;i<N;i++){x[i]+=dt*vx[i];y[i]+=dt*vy[i];z[i]+=dt*vz[i];}
    t_now+=dt;
    ACCEL(1);
    for(int i=0;i<N;i++){vx[i]+=0.5*dt*ax[i];vy[i]+=0.5*dt*ay[i];vz[i]+=0.5*dt*az[i];}

    /* once per orbit: diagnostics + energy */
    if((s+1)%(long)(2.0*M_PI/dt)==0){
      double s2=0; static double etab[100000]; int nb=0;
      for(int i=0;i<N;i++){double a,e;elements(x[i],y[i],z[i],vx[i],vy[i],vz[i],&a,&e);
        if(a>0&&a<10){s2+=e*e;etab[nb++]=e;}}
      double erms=sqrt(s2/(nb>0?nb:1));
      /* energy */
      double E=0;
      for(int i=0;i<N;i++){double r=sqrt(x[i]*x[i]+y[i]*y[i]+z[i]*z[i]);double v2=vx[i]*vx[i]+vy[i]*vy[i]+vz[i]*vz[i];
        E+=0.5*v2-1.0/r;
        for(int j=i+1;j<N;j++){double dx=x[j]-x[i],dy=y[j]-y[i],dz=z[j]-z[i];
          E-=m/sqrt(dx*dx+dy*dy+dz*dz);} }
      if(!E0set){E0=E;E0set=1;}
      fprintf(fout,"%.4f %.6f %.6f %.4f %.3e\n",t_now,erms,0.0,(double)nb/N,fabs((E-E0)/E0));
      fflush(fout);
    }
  }
  fclose(fout); fclose(fev);
  fprintf(stderr,"done: %ld events, eH=%.4g\n",nev,eH);
  return 0;
}
