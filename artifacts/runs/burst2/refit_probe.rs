//! Does an unforced tube survive repeated exact refits? One short diagnostic per invocation.
use emergent_universe::{Config, fleet::Order, scenario::plane, thrust::word, view::TICK_SECONDS, num::to_f64, bind::{Binding, Kick, bind_surface}};
fn dist(a:[f64;2],b:[f64;2])->f64 {((a[0]-b[0]).powi(2)+(a[1]-b[1]).powi(2)).sqrt()}
fn main(){
 let a:Vec<String>=std::env::args().collect();let seconds:f64=a[1].parse().unwrap();
 let mut p=plane(Config::default(),5,Order::Sparse,1,8).unwrap();let start=2_000_000;p.u.settle(start);p.u.input(start,word(1,4)).unwrap();
 let t=start+(seconds/TICK_SECONDS) as i64;p.u.settle(t);p.u.input(t,word(0,4)).unwrap();let b=p.u.rec(p.player).b;
 let d=&p.u.dolls[b.doll as usize]; let read=t+(100.0/TICK_SECONDS) as i64;let target=b.cartesian(read).unwrap();
 for h in [1<<20,1<<16,1<<12] {
  let mut r=b.clone();let mut at=t;
  while at<read {at=(at+h).min(read);let exact=r.readout(at).unwrap();let f=bind_surface(exact,at,r.clock_exp,Some(d.edge.scale(2).unwrap()),d.unit,Some(d.surface)).unwrap();
   r=Binding{doll:r.doll,tube:f.tube,entry:f.entry,residual:f.residual,turn:f.turn,units:f.units,clock_exp:r.clock_exp,event_time:at,kick:Kick::NONE,impact:None};
  }
  let got=r.cartesian(read).unwrap();println!("start={seconds}s h={}s pos_error_doll={:e} velocity_error_c={:e} target={:?}/{:?}",h as f64*TICK_SECONDS,dist(got.0.map(to_f64),target.0.map(to_f64)),dist(got.1.map(to_f64),target.1.map(to_f64)),target.0.map(to_f64),target.1.map(to_f64));
 }
}
