use std::f64::consts::TAU;
fn main(){
  let gm=9.765625e-4; let a=500_000_000.0f64/0.95; let e=0.05f64;
  let w=0xC000_0000u32 as f64/2f64.powi(32)*TAU; let m0=0xA000_0000u32 as f64/2f64.powi(32)*TAU;
  let n=1.0/(a*a*a).sqrt();
  let t=3.0e13f64;
  let mut m=m0+n*t; m%=TAU;
  let mut E=m; for _ in 0..40 {E-=(E-e*E.sin()-m)/(1.0-e*E.cos());}
  let xp=a*(E.cos()-e); let yp=a*(1.0-e*e).sqrt()*E.sin();
  let (sw,cw)=(w.sin(),w.cos());
  let (x,y)=(xp*cw-yp*sw, xp*sw+yp*cw);
  println!("giant t=3e13 pos=({:.3e},{:.3e}) |r|={:.3e} expect~{:.3e}",x,y,(x*x+y*y).sqrt(),a);
  // tidal check: family at 1.317e8, member offset 1e6 along the orbit; print Giant's differential pull
  let r=1.3169e8f64; let th=0.3f64; let dth=1e6f64/r;
  for (name,xx,yy) in [("x0",r*th.cos(),r*th.sin()),("xm",r*(th+dth).cos(),r*(th+dth).sin())] {
    let dx=x-xx; let dy=y-yy; let r2=dx*dx+dy*dy; let k=gm/(r2*r2.sqrt());
    println!("{} pull=({:.3e},{:.3e}) d={:.3e}",name,dx*k,dy*k,r2.sqrt());
  }
  let p0=(x-r*th.cos(), y-r*th.sin()); let pm=(x-r*(th+dth).cos(), y-r*(th+dth).sin());
  println!("diff=({:.3e},{:.3e}) |H*dx|~{:.3e}",p0.0-pm.0,p0.1-pm.1, gm/3.9e8f64.powi(3)*1e6);
}
