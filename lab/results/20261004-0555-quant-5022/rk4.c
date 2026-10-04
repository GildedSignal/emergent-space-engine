// RK4 on the raw CR3BP ODE (astrocentric, indirect included): verifies J* = v^2/2-1/r-mu/d-h+mu(r.r_p) is exact.
#include <stdio.h>
#include <math.h>
#include <string.h>
#define PI 3.14159265358979323846
static double mu=1e-3;
static void drv(double t,const double*q,double*d){
  double px=cos(t),py=sin(t), r3=pow(q[0]*q[0]+q[1]*q[1],1.5);
  double ax=px-q[0], ay=py-q[1], d3=pow(ax*ax+ay*ay,1.5);
  d[0]=q[2]; d[1]=q[3]; d[2]=-q[0]/r3+mu*(ax/d3-px); d[3]=-q[1]/r3+mu*(ay/d3-py);
}
static double Jstar(const double*q,double t){ double px=cos(t),py=sin(t);
  return 0.5*(q[2]*q[2]+q[3]*q[3])-1.0/hypot(q[0],q[1])-mu/hypot(px-q[0],py-q[1])-(q[0]*q[3]-q[1]*q[2])+mu*(q[0]*px+q[1]*py);
}
int main(){
  double a=0.55,e=0.05,om=0.7,P=2*PI*pow(a,1.5),M=1.0,E=M;
  for(int i=0;i<50;i++) E-=(E-e*sin(E)-M)/(1-e*cos(E));
  double cE=cos(E),sE=sin(E),sf=sqrt(1-e*e),dd=sqrt(a)*(1-e*cE);
  double xo=a*(cE-e), yo=a*sf*sE, vxo=-sE/dd, vyo=sf*cE/dd, co=cos(om),so=sin(om);
  double q[4]={xo*co-yo*so, xo*so+yo*co, vxo*co-vyo*so, vxo*so+vyo*co};
  double J0=Jstar(q,0), h=P/16384, t=0;
  for(long k=0;k<16384L*200;k++){
    double k1[4],k2[4],k3[4],k4[4],w[4];
    drv(t,q,k1); for(int i=0;i<4;i++) w[i]=q[i]+.5*h*k1[i]; drv(t+h/2,w,k2);
    for(int i=0;i<4;i++) w[i]=q[i]+.5*h*k2[i]; drv(t+h/2,w,k3);
    for(int i=0;i<4;i++) w[i]=q[i]+h*k3[i];    drv(t+h,w,k4);
    for(int i=0;i<4;i++) q[i]+=h/6*(k1[i]+2*k2[i]+2*k3[i]+k4[i]);
    t+=h;
    if(k%16384==0) printf("orbit %3ld dJ=%.3e\n",k/16384,Jstar(q,t)-J0);
  }
  return 0;
}
