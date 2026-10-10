/* Shearing-sheet belt probe: exact epicyclic motion (Hill/Wisdom-Tremaine local
 * patch), elastic hard encounters of radius R, event stream recorded.
 * Units: Omega = 1.  x = xc + e cos(th);  y = yc - 1.5 xc t - 2 e sin(th);
 * vx = -e sin(th); vy = -1.5 xc - 2 e cos(th).
 * Shearing-periodic in x (compensated), periodic in y.
 * Deterministic per seed (splitmix64).
 * usage: sim N Lx Ly R e0 T seed cap_events outprefix   */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

static unsigned long long rng;
static inline unsigned long long sm64(void){ rng += 0x9E3779B97F4A7C15ULL; unsigned long long z=rng; z=(z^(z>>30))*0xBF58476D1CE4E5B9ULL; z=(z^(z>>27))*0x94D049BB133111EBULL; return z^(z>>31);} 
static inline double ur(void){ return (sm64()>>11)*0x1.0p-53; }
static int dcmp(const void*a,const void*b){ double x=*(const double*)a,y=*(const double*)b; return x<y?-1:(x>y?1:0); }
static inline double wrap(double v, double L){ while(v> L/2) v-=L; while(v< -L/2) v+=L; return v; }
static double EPS_REST = 0.7; /* restitution: 1 = elastic, 0 = fully inelastic */

int main(int argc,char**argv){
  if(argc<10){fprintf(stderr,"usage: sim N Lx Ly R e0 T seed cap outprefix [eps]\n");return 1;}
  int N=atoi(argv[1]); double Lx=atof(argv[2]), Ly=atof(argv[3]), R=atof(argv[4]);
  double e0=atof(argv[5]), T_end=atof(argv[6]);
  rng=strtoull(argv[7],0,10)*2654435761ULL+12345; long cap=atol(argv[8]);
  if(argc>10) EPS_REST=atof(argv[10]);
  const char*out=argv[9];
  double *xc=malloc(sizeof(double)*N),*yc=malloc(sizeof(double)*N),*ee=malloc(sizeof(double)*N),*th=malloc(sizeof(double)*N);
  double *px=malloc(sizeof(double)*N),*py=malloc(sizeof(double)*N),*vx=malloc(sizeof(double)*N),*vy=malloc(sizeof(double)*N);
  for(int i=0;i<N;i++){
    xc[i]=(ur()-0.5)*Lx; yc[i]=(ur()-0.5)*Ly; th[i]=ur()*2*M_PI;
    double u=ur(); if(u<1e-300)u=1e-300; ee[i]= e0>0? e0*sqrt(-2*log(u)) : 0.0; /* Rayleigh */
  }
  int gx=(int)(Lx/R); if(gx<4)gx=4; if(gx>128)gx=128;
  int gy=(int)(Ly/R); if(gy<4)gy=4; if(gy>128)gy=128;
  double csx=Lx/gx, csy=Ly/gy; int ncell=gx*gy;
  int *cnt=calloc(ncell+1,sizeof(int)), *ord=malloc(sizeof(int)*N), *cellid=malloc(sizeof(int)*N);

  char buf[512]; snprintf(buf,sizeof buf,"%s.events.bin",out);
  FILE*fe=fopen(buf,"wb");
  snprintf(buf,sizeof buf,"%s.samples.txt",out); FILE*fs=fopen(buf,"w");
  snprintf(buf,sizeof buf,"%s.summary.txt",out); FILE*fu=fopen(buf,"w");
  long nev=0, steps=0; double t_now=0, dt=0; int early=0;
  double e_p95=0.95*e0+0.05*R;
  double *eb=malloc(sizeof(double)*N);
  static const int ox[5]={0,1,-1,0,1}, oy[5]={0,0,1,1,1};
  while(t_now<T_end){
    double ep=e_p95<5.0?e_p95:5.0;
    double vest=1.5*(2*ep+2*R)+4*ep+1e-9;
    dt=0.12*R/vest; if(dt>0.1)dt=0.1;
    for(int i=0;i<N;i++){
      th[i]+=dt; if(th[i]>=2*M_PI) th[i]-=2*M_PI;
      double c=cos(th[i]), s=sin(th[i]);
      double x=xc[i]+ee[i]*c, y=yc[i]-1.5*xc[i]*t_now-2*ee[i]*s;
      if(x>Lx/2){ xc[i]-=Lx; yc[i]+=1.5*Lx*t_now; x-=Lx; }
      else if(x<-Lx/2){ xc[i]+=Lx; yc[i]-=1.5*Lx*t_now; x+=Lx; }
      double yw=wrap(y,Ly); yc[i]+=yw-y; y=yw;
      px[i]=x; py[i]=y; vx[i]=-ee[i]*s; vy[i]=-1.5*xc[i]-2*ee[i]*c;
    }
    memset(cnt,0,(ncell+1)*sizeof(int));
    for(int i=0;i<N;i++){ int cx=(int)((px[i]+Lx/2)/csx); if(cx<0)cx=0; if(cx>=gx)cx=gx-1;
      int cy=(int)((py[i]+Ly/2)/csy); if(cy<0)cy=0; if(cy>=gy)cy=gy-1;
      int c=cy*gx+cx; cellid[i]=c; cnt[c]++; }
    int acc=0; for(int c=0;c<ncell;c++){int k=cnt[c];cnt[c]=acc;acc+=k;}
    int *fill=malloc(sizeof(int)*(ncell+1)); memcpy(fill,cnt,(ncell+1)*sizeof(int));
    for(int i=0;i<N;i++) ord[fill[cellid[i]]++]=i;
    free(fill);
    for(int cy=0;cy<gy;cy++)for(int cx=0;cx<gx;cx++){
      int c0=cy*gx+cx; int a=cnt[c0], b=cnt[c0+1];
      if(a==b) continue;
      for(int k=0;k<5;k++){
        int nx=cx+ox[k], ny=cy+oy[k];
        if(nx<0)nx+=gx; if(nx>=gx)nx-=gx; if(ny>=gy)ny-=gy;
        int c1=ny*gx+nx; int a1=cnt[c1], b1=cnt[c1+1];
        for(int p=a;p<b;p++){ int i=ord[p];
          int q0=(k==0)?p+1:a1;
          for(int q=q0;q<b1;q++){ int j=ord[q];
            double dx=px[j]-px[i], dy=py[j]-py[i];
            double d2=dx*dx+dy*dy;
            if(d2<R*R && d2>1e-18){
              double d=sqrt(d2), nxr=dx/d, nyr=dy/d;
              double rvx=vx[i]-vx[j], rvy=vy[i]-vy[j];
              double vn=rvx*nxr+rvy*nyr;
              if(vn>0){
                double imp=0.5*(1.0+EPS_REST)*vn;
                double dvx=-imp*nxr, dvy=-imp*nyr; /* impulse on i (restitution) */
                double vxi=vx[i]+dvx, vyi=vy[i]+dvy;
                double vxj=vx[j]-dvx, vyj=vy[j]-dvy;
                double xi=px[i], yi=py[i], xj=px[j], yj=py[j];
                double xci=2*(vyi+2*xi), eci=xi-xci, esi=-vxi;
                xc[i]=xci; ee[i]=sqrt(eci*eci+esi*esi);
                th[i]=atan2(esi,eci); if(th[i]<0)th[i]+=2*M_PI;
                yc[i]=yi+1.5*xci*t_now+2*esi;
                double xcj=2*(vyj+2*xj), ecj=xj-xcj, esj=-vxj;
                xc[j]=xcj; ee[j]=sqrt(ecj*ecj+esj*esj);
                yc[j]=yj+1.5*xcj*t_now+2*esj;
                vx[i]=vxi; vy[i]=vyi; vx[j]=vxj; vy[j]=vyj;
                float tf=(float)t_now; int32_t ii=i,jj=j;
                fwrite(&tf,4,1,fe); fwrite(&ii,4,1,fe); fwrite(&jj,4,1,fe);
                if(++nev>=cap){early=1; goto done;}
              }
            }
          }
        }
      }
    }
    t_now+=dt; steps++;
    if(steps%200==0){
      double sm2=0; for(int i=0;i<N;i++){sm2+=ee[i]; eb[i]=ee[i];}
      qsort(eb,N,sizeof(double),dcmp);
      e_p95=eb[(int)(0.95*(N-1))];
      double ke=0; for(int i=0;i<N;i++) ke+=vx[i]*vx[i]+vy[i]*vy[i];
      fprintf(fs,"%g %g %g %g %g\n",t_now,sm2/N,e_p95,ke/N,dt);
      fflush(fs);
    }
  }
done:;
  double sm=0,s2=0; for(int i=0;i<N;i++){sm+=ee[i]; s2+=ee[i]*ee[i];}
  double tau=N*M_PI*R*R/(Lx*Ly);
  fprintf(fu,"N %d Lx %g Ly %g R %g tau %g e0 %g T_end %g T_done %g steps %ld events %ld early %d dt_last %g e_mean_final %g e_rms_final %g\n",
    N,Lx,Ly,R,tau,e0,T_end,t_now,steps,nev,early,dt,sm/N,sqrt(s2/N));
  fclose(fu); fclose(fs); fclose(fe);
  fprintf(stderr,"done T=%.3g ev=%ld early=%d\n",t_now,nev,early);
  return 0;
}
