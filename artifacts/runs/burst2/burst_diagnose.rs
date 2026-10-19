//! T1 ablation probe: runs one cadence/level per invocation (under 60 s).
use emergent_universe::{Config, fleet::Order, scenario::plane, thrust::word, observe::{root_state, root_state_raw}, num::to_f64, view::TICK_SECONDS};
fn main() {
 let a:Vec<String>=std::env::args().collect();
 let q:i32=a[1].parse().unwrap(); let level:u8=a[2].parse().unwrap(); let mode=a.get(3).map(String::as_str).unwrap_or("burn");
 let d=Config::default(); let cfg=Config{step_log2:d.step_log2+q,thrust_quantum_log2:d.thrust_quantum_log2+q,..d};
 let mut p=plane(cfg,5,Order::Sparse,1,8).unwrap();
 let start=2_000_000; let end=start+(2000.0/TICK_SECONDS) as i64; let read=end+(100.0/TICK_SECONDS) as i64;
 p.u.settle(start);
 if mode=="no-tide" { p.u.sources.iter_mut().for_each(Vec::clear); }
 if mode!="coast" {p.u.input(start,word(if mode=="cancelled" {3} else {1},level)).unwrap();}
 let mut overpaid_force=[0.0;2]; let mut max_weight_ratio=0.0f64; let mut estimate_error_s=0.0f64; let mut max_estimate_error_s=0.0f64; let mut residual_drift=[0.0;2]; let mut max_residual_speed=0.0f64; let mut integrated_force=[0.0;2]; let mut last=start; let proper0=to_f64(p.u.rec(p.player).proper);
 let mut doll=p.u.rec(p.player).b.doll; let mut transitions=Vec::new();
 loop {
  let r=p.u.rec(p.player); let t=r.plan.first().map(|i|i.t).unwrap_or(end);
  if t>end {break;}
  let dt=(t-last) as f64;
  for c in 0..2 { let dv=r.b.residual.velocity[c] as f64*2f64.powi(r.b.units.1 as i32); residual_drift[c]+=dv*dt; max_residual_speed=max_residual_speed.max(dv.abs()); }
  if let Some(it)=r.plan.first().filter(|it|matches!(it.what, emergent_universe::body::What::Kick(_))) {
   let level=if let emergent_universe::body::What::Kick(l)=it.what {l} else {0};
   let (x,_) = r.b.cartesian(t).unwrap();
   let ctx=p.u.ctx(); let secs=ctx.secondaries(r.b.doll,t,p.player).unwrap();
   let acc=emergent_universe::force::acceleration(level,x,&secs,ctx.tide(r.b.doll,t).unwrap()).unwrap();
   let h=(r.interval >> (2*level as i64)) as f64 * 2f64.powi(r.b.clock_exp as i32);
   for c in 0..2 { integrated_force[c]+=to_f64(acc[c])*h; }
   if let Some(ext) = r.ext {
    let field=emergent_universe::force::field(&secs,x).unwrap();
    let w=to_f64(ext.time(ext.y(field.potential).unwrap(),ext.ds).unwrap());
    max_weight_ratio=max_weight_ratio.max(w/h);
    for c in 0..2 {overpaid_force[c]+=to_f64(field.accel[c])*(w-h);}
   }
  }
  let before = r.clone();
  p.u.settle(t); last=t;
  let after = p.u.rec(p.player);
  if before.b.doll == after.b.doll && after.b.event_time == t && after.thrust.unwrap().since == t {
   let shift = p.u.dolls[after.b.doll as usize].shift;
   let level = match before.plan.first().map(|i|i.what) { Some(emergent_universe::body::What::Kick(l)) => l, _ => 0 };
   let end = t + (before.interval >> (2*level as i64))/2;
   let pre = emergent_universe::step::proper_since(&before.b,shift,t,end).unwrap();
   let post = emergent_universe::step::proper_since(&after.b,shift,t,end).unwrap();
   let e=(to_f64(pre)-to_f64(post)).abs()*TICK_SECONDS;
   estimate_error_s+=e; max_estimate_error_s=max_estimate_error_s.max(e);
  }
  let r=p.u.rec(p.player);
  if r.b.doll!=doll { transitions.push((t,r.b.doll)); doll=r.b.doll; }
  if !r.alive || t==end {break;}
 }
 p.u.settle(end);
 let r=p.u.rec(p.player);let th=r.thrust.unwrap();
 println!("root force overpayment_c={overpaid_force:?} max_weight_ratio={max_weight_ratio:e}");
 println!("estimate error_s sum={estimate_error_s:e} max={max_estimate_error_s:e}");
 println!("diagnostic residual_drift={residual_drift:?} max_residual_speed={max_residual_speed:e} integrated_force={integrated_force:?} elapsed_proper_s={:e}",(to_f64(r.proper)-proper0)*TICK_SECONDS);
 println!("cut q={q} L{level} mode={mode} doll={} binding={} since={} ahead_s={:.12e} proper_s={:.12e} carries={:?} transitions={transitions:?}",r.b.doll,r.b.event_time,th.since,to_f64(th.ahead)*TICK_SECONDS,to_f64(r.proper)*TICK_SECONDS,r.carry);
 if mode!="coast" {p.u.input(end,word(0,level)).unwrap();}
 p.u.settle(read);
 let r=p.u.rec(p.player); let (x,v)=root_state(&p.u.ctx(),p.player,read).unwrap();let raw=root_state_raw(&p.u.ctx(),p.player,read).unwrap();let local=r.b.cartesian(read).unwrap();
 println!("read q={q} L{level} mode={mode} doll={} alive={} refusals={} root={x:?}/{v:?} raw={raw:?} local={:?}/{:?}",r.b.doll,r.alive,r.refusals,local.0.map(to_f64),local.1.map(to_f64));
}
