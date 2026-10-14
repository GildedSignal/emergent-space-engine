//! The exact integer impulse, delivered on the shipped representation (scout 29f4).
//! Read-only composition of shipped pub APIs: no engine file is modified.
//!
//! Per (p, e, t, impulse): prints the exact integer state, the shipped refit's key
//! (Rebinding::from_state via binding::cartesian), and the key-arm delivery
//! (E, L from the fit's exact algebra, kicked and un-kicked), all as exact integers.
//! Also prices: from_state, the delivery arithmetic, Cycle::compile (the deferred cost).
use emergent_space::binding::{cartesian, IntegerState, Rebinding, Trajectory};
use emergent_space::orbit::{Orbit, OrbitKey, Scalar};
use std::hint::black_box;
use std::time::Instant;

fn encode(x: f64) -> Scalar {
    let e = x.log2().floor() as i32;
    Scalar::raw((x * 2f64.powi(60 - e)).round() as i128, e - 60).unwrap()
}
fn key(p: f64, e: f64) -> OrbitKey {
    OrbitKey::bound(encode(p), (e * 2f64.powi(48)).round() as u64).unwrap()
}

/// The fit's exact invariant algebra (binding.rs fit_key), evaluated on a state:
/// kinetic = vr^2/lapse + vt^2; den = lapse - kinetic; L^2 = (r.vt)^2/den;
/// E^2 = lapse^2/den (= 1 + (kinetic - 2u.lapse)/den), with u = 1/r, lapse = 1 - 2u.
fn invariants(r: Scalar, vr: Scalar, vt: Scalar) -> (Scalar, Scalar) {
    let u = r.reciprocal().unwrap();
    let lapse = Scalar::ONE.sub(u.scale(1).unwrap()).unwrap();
    let kinetic = vr.mul(vr).unwrap().div(lapse).unwrap().add(vt.mul(vt).unwrap()).unwrap();
    let den = lapse.sub(kinetic).unwrap();
    let angular = r.mul(vt).unwrap();
    let l2 = angular.mul(angular).unwrap().div(den).unwrap();
    // E^2 = lapse^2/den = 1 + (kinetic - 2u*lapse)/den  (lapse^2 - den = kinetic - 2u*lapse).
    let e2 = Scalar::ONE
        .add(kinetic.sub(u.scale(1).unwrap().mul(lapse).unwrap()).unwrap().div(den).unwrap())
        .unwrap();
    (e2.sqrt().unwrap(), l2.sqrt().unwrap())
}

fn main() {
    let mut seed = 0x29f4_cafe_babeu64;
    let mut next = move || {
        seed = seed.wrapping_mul(6364136223846793005).wrapping_add(1);
        seed
    };
    let ps = [2048.0f64, 20000.0, 2e6];
    let es = [0.0f64, 0.07, 0.3];
    let times = [(5i128, -5i32), (16, -5), (25, -5)];
    let scales = [-50i32, -40, -30, -20, -10];
    let mut refit_states: Vec<(Scalar, IntegerState)> = Vec::new();
    let mut deliveries: Vec<(Scalar, Scalar, Scalar)> = Vec::new();
    println!("case p_sig p_exp e4 t dir dvrf dvtf refit_peri_sig refit_peri_exp refit_k E0_sig E0_exp L0_sig L0_exp Ep_sig Ep_exp Lp_sig Lp_exp");
    for &p in &ps {
        for &e in &es {
            let orbit = Orbit::compile(key(p, e)).unwrap();
            let period = orbit.period().unwrap();
            for &(tm, te) in &times {
                let elapsed = period.mul(Scalar::raw(tm, te).unwrap()).unwrap();
                let st = orbit.state(elapsed).unwrap();
                let (e0, l0) = invariants(st.radius, st.radial_velocity, st.transverse_velocity);
                let units = (
                    st.radius.exponent() - 60,
                    st.transverse_velocity.abs().exponent() - 60,
                );
                for &k in &scales {
                    for d in 0..3u64 {
                        let mut s2 = st;
                        let (dvrf, dvtf) = match d {
                            0 => (k, 99), // radial only
                            1 => (99, k), // transverse only
                            _ => (k, k),  // parallel to (vr, vt)
                        };
                        if dvrf != 99 {
                            s2.radial_velocity = s2
                                .radial_velocity
                                .add(st.radial_velocity.scale(dvrf).unwrap())
                                .unwrap();
                        }
                        if dvtf != 99 {
                            s2.transverse_velocity = s2
                                .transverse_velocity
                                .add(st.transverse_velocity.scale(dvtf).unwrap())
                                .unwrap();
                        }
                        let (ep, lp) =
                            invariants(s2.radius, s2.radial_velocity, s2.transverse_velocity);
                        let state = cartesian(s2.clone(), 0x2000_0000u32, false, units).unwrap();
                        let fit = Rebinding::from_state(state.clone(), elapsed, None);
                        let (rsig, rexp, rk) = match &fit {
                            Ok(f) => match &f.trajectory {
                                Trajectory::Cycle(o) => {
                                    let k2 = o.key();
                                    (k2.periapsis.significand(), k2.periapsis.exponent() as i128, k2.k as i128)
                                }
                                _ => (0, 0, -1),
                            },
                            Err(_) => (0, 0, -2),
                        };
                        let pe = encode(p);
                        println!(
                            "{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}",
                            pe.significand(),
                            pe.exponent(),
                            (e * 1e4) as i64,
                            tm,
                            d,
                            dvrf,
                            dvtf,
                            rsig,
                            rexp,
                            rk,
                            e0.significand(), e0.exponent(),
                            l0.significand(), l0.exponent(),
                            ep.significand(), ep.exponent(),
                            lp.significand(), lp.exponent()
                        );
                        if let Ok(_) = fit {
                            refit_states.push((elapsed, state));
                        }
                        deliveries.push((s2.radius, s2.radial_velocity, s2.transverse_velocity));
                        let _ = next();
                    }
                }
            }
        }
    }

    // Prices.
    let t0 = Instant::now();
    let mut n = 0u64;
    for (t, s) in &refit_states {
        let _ = black_box(Rebinding::from_state(black_box(s.clone()), black_box(*t), None));
        n += 1;
    }
    println!(
        "price from_state_ns_mean {} {}",
        t0.elapsed().as_nanos() / n.max(1) as u128,
        n
    );

    let t0 = Instant::now();
    let mut m = 0u64;
    for (r, vr, vt) in &deliveries {
        let _ = black_box(invariants(black_box(*r), black_box(*vr), black_box(*vt)));
        m += 1;
    }
    println!(
        "price delivery_ns_mean {} {}",
        t0.elapsed().as_nanos() / m.max(1) as u128,
        m
    );

    // Deferred compile price on the cycle stack (belt-band keys in darwin's domain).
    for (p16, e30) in [
        (2048u32 << 16, (0.07 * 2f64.powi(30)) as u32),
        (8000u32 << 16, (0.2 * 2f64.powi(30)) as u32),
    ] {
        let k = emergent_space::Key::darwin(p16, e30).unwrap();
        let t0 = Instant::now();
        let reps = 200;
        for _ in 0..reps {
            let _ = black_box(emergent_space::Cycle::compile(black_box(k)));
        }
        println!(
            "price cycle_compile_ns p{} {}",
            p16 >> 16,
            t0.elapsed().as_nanos() / reps as u128
        );
    }
}
