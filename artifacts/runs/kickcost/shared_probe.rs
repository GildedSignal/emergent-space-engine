//! Carried shapes: exact event reconstruction and fixed cycle increments.
use emergent_space::{binding::{cartesian, Rebinding}, orbit::{Orbit, OrbitKey, Scalar}};
fn d(x: Scalar) -> f64 { x.significand() as f64 * 2f64.powi(x.exponent() as i32-62) }
fn main() {
    let (mut period_error, mut advance_error) = (0.0f64, 0.0f64);
    let mut reconstructed = 0;
    for i in 0..256u64 {
        let e = ((1u64<<48)-1) * (i+1) / 257;
        let key = OrbitKey::bound(Scalar::power_of_two(21+(i%20) as i16),e).unwrap();
        let exact = Orbit::compile(key).unwrap();
        let served = Orbit::compile_carried(key).unwrap();
        assert_eq!(served.key(),key);
        period_error = period_error.max((d(served.period().unwrap())/d(exact.period().unwrap())-1.0).abs());
        advance_error = advance_error.max((d(served.advance().unwrap())/d(exact.advance().unwrap())-1.0).abs());
        let t=Scalar::power_of_two(-10);
        let zero=served.at_phase(0,t).unwrap();
        for n in [1,100,10000] {
            let state=served.at_phase(n,t).unwrap();
            assert_eq!(state.advance,zero.advance.add(served.advance().unwrap().mul(Scalar::integer(n as i64)).unwrap()).unwrap());
            assert_eq!(state.proper_time,zero.proper_time.add(served.proper_period().unwrap().mul(Scalar::integer(n as i64)).unwrap()).unwrap());
        }
        let st=exact.state(exact.period().unwrap().scale(-3).unwrap()).unwrap();
        let input=cartesian(st, (i as u32).wrapping_mul(0x1234567), i%2==0, (st.radius.exponent()-60,st.radial_velocity.abs().max(st.transverse_velocity.abs()).exponent()-60)).unwrap();
        let fit=Rebinding::from_state_carried(input,Scalar::ZERO,None).unwrap();
        assert_eq!(fit.reconstruct().unwrap(),input);
        reconstructed+=1;
    }
    for delta in [1u64, 16, 256, 65536] {
        let key=OrbitKey::new(Scalar::power_of_two(27),(1u64<<48)-delta).unwrap();
        let served=Orbit::compile_carried(key).unwrap();
        let cell=served.shape().key().k;
        let exact_e=(1u64<<48) as f64/key.k as f64-1.0;
        let cell_e=(1u64<<48) as f64/cell as f64-1.0;
        println!("near_circle: delta={delta} exact_e={exact_e:.9e} cell_e={cell_e:.9e}");
    }
    println!("carried: seeds=256 period_relative_max={period_error:.9e} advance_relative_max={advance_error:.9e} event_reconstruction={reconstructed}/256 cycle_increment_checks=768/768");
}
