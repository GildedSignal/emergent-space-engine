use emergent_space::orbit::{Orbit, OrbitKey};
use emergent_space::scaled::Scalar;
fn to_f64(s: Scalar) -> f64 { s.significand() as f64 * 2f64.powi(s.exponent() as i32 - 62) }
fn cyc(p: f64, e: f64) -> (f64, usize) {
    let key = OrbitKey::bound(Scalar::integer(p as i64), (e.min(0.999999999) * (1u64<<48) as f64) as u64).unwrap();
    let o = Orbit::compile(key).unwrap();
    (to_f64(o.period().unwrap()), o.shape().knots().len())
}
fn main() {
    let a = 2304.0;
    println!("fixed a: e -> rel diff from previous, knots");
    let mut prev = 0.0;
    for i in 0..8 {
        let e = 0.5 + i as f64 * 6e-8;
        let (t, k) = cyc(a*(1.0-e*e), e);
        if i > 0 { println!("e={e:.9}  dT/T={:.3e}  knots={k}", (t-prev)/t); } else { println!("e={e:.9}  T={t:.6} knots={k}"); }
        prev = t;
    }
    println!("fixed p:");
    let p = 2304.0; prev = 0.0;
    for i in 0..8 {
        let e = 0.5 + i as f64 * 6e-8;
        let (t, k) = cyc(p, e);
        if i > 0 { println!("e={e:.9}  dT/T={:.3e}  knots={k}", (t-prev)/t); } else { println!("e={e:.9}  T={t:.6} knots={k}"); }
        prev = t;
    }
    println!("fixed p near g=1:");
    for g in [1.0f64, 1.0-1e-7, 1.0-2e-7, 1.0-1e-3] {
        let e = (1.0-g).sqrt();
        let (t,k) = cyc(2304.0, e);
        println!("g={g:.9} e={e:.6} T={t:.4} knots={k}");
    }
    let e0 = 0.5f64; let g0 = 1.0-e0*e0; let h = 1e-3*g0;
    let ep = (1.0f64-(g0+h)).sqrt(); let em = (1.0f64-(g0-h)).sqrt();
    let (tp,_) = cyc(a*(g0+h), ep); let (tm,_) = cyc(a*(g0-h), em); let (t0,_) = cyc(a*g0, e0);
    println!("fixed-a: dT/dg={:.6e} T''''/T={:.3e}", (tp-tm)/(2.0*h), (tp-2.0*t0+tm)/(h*h)/t0);
    let (tp,_) = cyc(2304.0, ep); let (tm,_) = cyc(2304.0, em);
    println!("fixed-p: dT/dg={:.6e} (Kepler: {:.6e})", (tp-tm)/(2.0*h), -1.5*t0/g0);
}
