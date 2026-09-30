/* Focused scan: precession error near the ISCO for low-e orbits (m=16, m=32). */
#include <stdio.h>
#include <math.h>
static int m_bands;
static double uk_of(double u){ if(u<=0)return 0; double k=floor(m_bands*log2(1.0/u)); return pow(2.0,-(k+0.5)/m_bands);} 
static double acc(int mode,double u,double invL2){double uk=(mode&1)?uk_of(u):0.0;
  return mode==0?invL2+3*u*u-u : mode==1?invL2-3*uk*uk-(1-6*uk)*u : 0;}
static void rk4(int m,double iL,double*u,double*w,double h){double a=*w,b=acc(m,*u,iL),c=*w+.5*h*b,d=acc(m,*u+.5*h*a,iL),e=*w+.5*h*d,f=acc(m,*u+.5*h*c,iL),g=*w+h*f,j=acc(m,*u+h*e,iL);*u+=h/6*(a+2*c+2*e+g);*w+=h/6*(b+2*d+2*f+j);}
/* returns dphi of cycle 2, or -1 capture, -2 no-cycle */
static double cyc(int mode,double up,double ua,double h){
  double iL=0.5*(up+ua)-(up*up+up*ua+ua*ua);
  double u=up,w=0,phi=0,pw=w,goal=-1;int n=0;
  for(long i=0;i<200000000L&&phi<200000; i++){
    rk4(mode,iL,&u,&w,h);phi+=h;
    if(u>=0.5)return -1;
    if(pw>0&&w<=0){double pp=goal; goal=pw/(pw-w)*h + (phi-h); if(n>=2) return goal-pp; n++;}
    pw=w;}
  return -2;}
int main(void){
  double h=1e-4; double es[]={0.02,0.05,0.1,0.3,0.7};
  printf("%5s %6s %4s | %-12s %-12s %-10s\n","e","r_p","m","band_dphi","exact_dphi","err");
  for(int ie=0;ie<5;ie++)for(int ir=0;ir<26;ir++){
    double e=es[ie],rp=5.9+0.06*ir,up=1.0/rp,ua=up*(1-e)/(1+e);
    for(int m=16,k=0;k<2;k++,m=32){ m_bands=m;
      double de=cyc(0,up,ua,h),db=cyc(1,up,ua,h);
      if(de<0||db<0){printf("%5.2f %6.2f %4d | %-12s %-12s %-10s\n",e,rp,m,db<0?(db==-1?"CAPTURE":"nocycle"):"-",de<0?(de==-1?"CAPTURE":"nocycle"):"-","-");continue;}
      double err=fabs(db-de)/de;
      printf("%5.2f %6.2f %4d | %-12.3f %-12.3f %-10.3e%s\n",e,rp,m,db,de,err,err>0.01?"  ** >1% **":"");
    }
  }
  return 0;}
