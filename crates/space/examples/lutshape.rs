//! Scalar conversions are diagnostics only; the candidate interpolation is integer.
use emergent_space::{binding::{cartesian, Rebinding}, orbit::{Orbit, OrbitKey, Scalar, ShapeGrid}};
#[allow(dead_code)]
#[path = "../../../xtask/src/behave/sample.rs"] mod sample;
fn d(x: Scalar) -> f64 { x.significand() as f64 * 2f64.powi(x.exponent() as i32-62) }
fn scalar(x: f64) -> Scalar { let e=x.log2().floor() as i32; Scalar::raw((x*2f64.powi(60-e)).round() as i128,e-60).unwrap() }
fn main() {
    let args:Vec<_>=std::env::args().collect();
    let grid=ShapeGrid{bits:args[1].parse().unwrap(),order:args[2].parse().unwrap()};
    let mut keys=Vec::new();
    // Frozen G1/G2 keys, then their weak-scale equivalents: the original seeds
    // alone are all strong-field and cannot falsify a weak-table approximation.
    for (p,e) in sample::bound_orbits(256) {
        keys.push(OrbitKey::bound(scalar(p),(e*2f64.powi(48)).round() as u64).unwrap());
        keys.push(OrbitKey::bound(scalar(p*2f64.powi(30)),(e*2f64.powi(48)).round() as u64).unwrap());
    }
    for i in 0..256u64 {
        keys.push(OrbitKey::bound(Scalar::power_of_two(21+(i%20) as i16),((1u64<<48)-1)*(i+1)/257).unwrap());
    }
    for delta in [0u64,1,16,256,65536,1<<30] {
        keys.push(OrbitKey::new(Scalar::power_of_two(27),(1u64<<48)-delta).unwrap());
    }
    // Both sides of exponent boundaries and nearly parabolic Q48 limits.
    for b in 2..48 { for off in [-2i64,0,2] {
        let gap=((1u64<<b) as i64+off).max(2) as u64;
        keys.push(OrbitKey::new(Scalar::power_of_two(30),((1u64<<48)+gap)/2).unwrap());
    }}
    let (mut pe,mut ae,mut te,mut radius)=(0.0f64,0.0f64,0.0f64,0.0f64);
    let mut compiler_period=0.0f64;
    let mut above_native=0usize;
    let mut weak_count=0usize;
    let mut compiler_advance=0.0f64;
    let mut cycles=0;
    let mut reconstructed=0;
    for (i,key) in keys.iter().copied().enumerate() {
        let exact=Orbit::compile(key).unwrap();
        let served=Orbit::compile_interpolated(key,grid).unwrap();
        assert_eq!(served.key(),key);
        if d(key.compactness().unwrap()) <= 2f64.powi(-18) {
            let k=key.k as f64 / 2f64.powi(48);
            let g=2.0*k-1.0;
            let q=d(key.compactness().unwrap());
            let scale=d(key.periapsis).powf(1.5);
            let reference=2.0*std::f64::consts::PI*k.sqrt()*(k/g.powf(1.5)+3.0*q/g.sqrt())*scale;
            let native=(d(exact.period().unwrap())/reference-1.0).abs();
            let added=(d(served.period().unwrap())/d(exact.period().unwrap())-1.0).abs();
            weak_count+=1;
            if added > native.max(2e-15) { above_native+=1; }
            compiler_period=compiler_period.max(native);
            compiler_advance=compiler_advance.max((d(exact.advance().unwrap())/(6.0*std::f64::consts::PI*k*q)-1.0).abs());
        }
        pe=pe.max((d(served.period().unwrap())/d(exact.period().unwrap())-1.0).abs());
        ae=ae.max((d(served.advance().unwrap())/d(exact.advance().unwrap())-1.0).abs());
        te=te.max((d(served.proper_period().unwrap())/d(exact.proper_period().unwrap())-1.0).abs());
        let zero=served.at_phase(0,Scalar::power_of_two(-10)).unwrap();
        for n in [1,100,10000] {
            let st=served.at_phase(n,Scalar::power_of_two(-10)).unwrap();
            assert_eq!(st.radius,zero.radius);
            assert_eq!(st.advance,zero.advance.add(served.advance().unwrap().mul(Scalar::integer(n as i64)).unwrap()).unwrap());
            cycles+=1;
        }
        if i<768 {
            let t=exact.period().unwrap().scale(-3).unwrap();
            let st=exact.state(t).unwrap();
            let st2=served.state(t).unwrap();
            radius=radius.max((d(st2.radius)/d(st.radius)-1.0).abs());
            let input=cartesian(st,(i as u32).wrapping_mul(0x1234567),i%2==0,(st.radius.exponent()-60,st.radial_velocity.abs().max(st.transverse_velocity.abs()).exponent()-60)).unwrap();
            // The production rebinder is tested separately after the grid selection.
            let fit=Rebinding::from_state(input,Scalar::ZERO,None).unwrap();
            assert_eq!(fit.reconstruct().unwrap(),input);
            reconstructed+=1;
        }
    }
    println!("control: exact_vs_analytic_weak_period={compiler_period:.9e} advance={compiler_advance:.9e} added_exceeds_native={above_native}/{weak_count} arithmetic_comparison_floor=2e-15");
    println!("grid: bits={} order={} cases={} period={pe:.9e} advance={ae:.9e} proper={te:.9e} radius={radius:.9e} cycle_checks={cycles} exact_reconstruction={reconstructed} cache={:?}",grid.bits,grid.order,keys.len(),emergent_space::orbit::shape_cache_stats());
}
