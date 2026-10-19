//! The throttle sweep's first L15 frame, split only to inspect which operators it resolves.
use emergent_universe::{Config,Budget,fleet::Order,scenario::plane,thrust::word,body::What,force,num::{norm2,time_of,to_f64},view::TICK_SECONDS};
fn main(){
 let mut p=plane(Config::default(),1,Order::Sparse,1,48).unwrap();
 for f in 0..510 {if f>=60 && (f-60)%30==0 {p.u.input(p.u.now,word(1,((f-60)/30) as u8)).unwrap();}p.u.frame(1.0/60.0,100.0,Budget::unlimited());}
 p.u.input(p.u.now,word(1,15)).unwrap();
 let target=p.u.now+(100.0/60.0/TICK_SECONDS) as i64;
 let mut levels=[0usize;4];let mut zero=[0usize;4];let mut max_ratio=[0.0f64;4];let before=p.u.stats;
 loop {
  let r=p.u.rec(p.player);let t=r.plan.first().unwrap().t;if t>target {break;}
  for item in r.plan.iter().filter(|it|it.t==t) {if let What::Kick(l)=item.what {
   levels[l as usize]+=1;
   let ctx=p.u.ctx();let (x,_)=r.b.cartesian(t).unwrap();let a=force::acceleration(l,x,&ctx.secondaries(r.b.doll,t,p.player).unwrap(),ctx.tide(r.b.doll,t).unwrap()).unwrap();
   if a.iter().all(|x|x.is_zero()){zero[l as usize]+=1;}
   let dv=norm2(a).unwrap().mul(time_of(r.interval >> (2*l as i64),r.b.clock_exp).unwrap()).unwrap();
   let eta=(r.interval >> (2*l as i64)) as f64*2f64.powi(Config::default().thrust_log2+15);
   max_ratio[l as usize]=max_ratio[l as usize].max(to_f64(dv)/eta);
  }}
  p.u.settle(t);
 }
 p.u.settle(target);
 println!("player kicks by level={levels:?}; exactly zero gravity={zero:?}; max gravity/burn={max_ratio:?}; global kicks={}",p.u.stats.kicks-before.kicks);
}
