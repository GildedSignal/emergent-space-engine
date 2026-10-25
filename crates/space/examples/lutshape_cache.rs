use emergent_space::{binding::{cartesian, Rebinding}, orbit::{clear_shape_cache, shape_cache_stats, Orbit, OrbitKey, Scalar, ShapeGrid}};
use std::{hint::black_box,time::Instant};
fn report(name:&str, mut ns:Vec<u128>) { let mean=ns.iter().sum::<u128>() as f64/ns.len() as f64/1000.;ns.sort_unstable();println!("cache_rebind: {name} samples={} mean_us={mean:.3} p50_us={:.3} p99_us={:.3}",ns.len(),ns[ns.len()/2] as f64/1000.,ns[ns.len()*99/100] as f64/1000.); }
fn main(){
 let args:Vec<_>=std::env::args().collect();
 let grid=ShapeGrid{bits:args[1].parse().unwrap(),order:args[2].parse().unwrap()};
 let mut inputs=Vec::new();
 for i in 0..128u64 {
  let key=OrbitKey::bound(Scalar::power_of_two(30),((1u64<<48)-1)*(2*i+1)/257).unwrap();
  let orbit=Orbit::compile(key).unwrap();
  let st=orbit.state(orbit.period().unwrap().scale(-3).unwrap()).unwrap();
  let input=cartesian(st,(i as u32).wrapping_mul(0x1234567),i%2==0,(st.radius.exponent()-60,st.radial_velocity.abs().max(st.transverse_velocity.abs()).exponent()-60)).unwrap();
  inputs.push(input);
 }
 let mut scrub=vec![1u64;4*1024*1024];
 for (label,g) in [("exact",None),("interpolated",Some(grid))] {
  for mode in ["empty", "warm", "evicted_cpu"] {
   let mut times=Vec::new();clear_shape_cache();
   for input in &inputs {
    if mode=="empty" {clear_shape_cache();} else {black_box(Rebinding::from_state_grid(*input,Scalar::ZERO,None,g).unwrap());}
    if mode=="evicted_cpu" {for x in scrub.iter_mut().step_by(8) {*x=x.wrapping_add(1);} black_box(&scrub);}
    let now=Instant::now();
    let fit=Rebinding::from_state_grid(black_box(*input),Scalar::ZERO,None,g).unwrap();
    times.push(now.elapsed().as_nanos());
    assert_eq!(fit.reconstruct().unwrap(),*input);
    black_box(fit);
   }
   report(&format!("{label}/{mode}"),times);println!("cache_stats: {label}/{mode} {:?}",shape_cache_stats());
  }
 }
}
