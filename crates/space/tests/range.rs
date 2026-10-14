//! R1 (integrator, 13 October): 3/10/30/100 AU, E=1.001/3/1000, zero
//! refusals and relative position/velocity error <=1e-6. Independent Schwarzschild
//! proper-time ODE, integrated by step-doubled RK4; no engine formula in the judge.
use emergent_space::binding::{IntegerState, Rebinding, cartesian};
use emergent_space::orbit::Scalar;
const AU: i64 = 101_300_000;
const LEAVE: i64 = 1 << 40;
fn scalar(v: f64) -> Scalar {
    Scalar::raw((v * 2f64.powi(40)) as i128, -40).unwrap()
}
fn rhs(y: [f64; 4], q: f64, a: f64, b: f64) -> [f64; 4] {
    let r = y[0];
    [
        y[1],
        -a / (r * r) + 1.0 / r.powi(3) - 3.0 * q / r.powi(4),
        1.0 / (r * r),
        b / (1.0 - 2.0 * q / r),
    ]
}
fn rk(y: [f64; 4], h: f64, q: f64, a: f64, b: f64) -> [f64; 4] {
    let plus = |k: [f64; 4], d: f64| std::array::from_fn(|i| y[i] + d * k[i]);
    let k1 = rhs(y, q, a, b);
    let k2 = rhs(plus(k1, h / 2.0), q, a, b);
    let k3 = rhs(plus(k2, h / 2.0), q, a, b);
    let k4 = rhs(plus(k3, h), q, a, b);
    std::array::from_fn(|i| y[i] + h * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]) / 6.0)
}
fn reference(rp: f64, v: f64, tol: f64) -> Vec<[f64; 4]> {
    let q = 1.0 / rp;
    let f = 1.0 - 2.0 * q;
    let ell = v / (f - v * v).sqrt();
    let energy = f / (f - v * v).sqrt();
    let (a, b) = (q / (ell * ell), energy / ell);
    let mut y = [1.0, 0.0, 0.0, 0.0];
    let mut h = 0.01f64;
    let mut out = vec![y];
    // Fixed proper-time checkpoints span the turn, the phase/radial join and the leave.
    let end = ((LEAVE as f64 / rp).powi(2) - 1.0).sqrt() * 0.999;
    let mut at = 0.0;
    for j in 1..=80 {
        let target = (1.0 + end).powf(j as f64 / 80.0) - 1.0;
        while at < target {
            let dt = h.min(target - at);
            let full = rk(y, dt, q, a, b);
            let half = rk(rk(y, dt / 2.0, q, a, b), dt / 2.0, q, a, b);
            let err = (0..4)
                .map(|i| (full[i] - half[i]).abs() / (1.0 + half[i].abs()))
                .fold(0.0, f64::max);
            if err <= tol {
                y = half;
                at += dt;
            }
            h = dt * (0.9 * (tol / err.max(1e-30)).powf(0.2)).clamp(0.2, 2.0);
        }
        out.push(y);
    }
    out
}
#[test]
fn r1_far_flybys() {
    let mut refused = 0;
    let mut worst_x = 0.0f64;
    let mut worst_v = 0.0f64;
    let mut convergence = 0.0f64;
    for au in [3, 10, 30, 100] {
        for e in [1.001f64, 3.0, 1000.0] {
            let rp = (au * AU) as f64;
            let f = 1.0 - 2.0 / rp;
            let v = (f - f * f / (e * e)).sqrt();
            let st = IntegerState {
                position: [au * AU, 0],
                velocity: [0, (v * 2f64.powi(60)) as i64],
                length_exponent: 0,
                velocity_exponent: -60,
            };
            let fit = match Rebinding::from_state(st, Scalar::ZERO, Some(Scalar::integer(LEAVE))) {
                Ok(fit) => fit,
                Err(err) => {
                    refused += 1;
                    println!("R1 {au} AU E={e}: REFUSED {err:?}");
                    continue;
                }
            };
            let v = st.velocity[1] as f64 * 2f64.powi(-60);
            let refs = reference(rp, v, 1e-13);
            let finer = reference(rp, v, 1e-15);
            let mut wx = 0.0f64;
            let mut wv = 0.0f64;
            for (y, z) in refs.iter().zip(finer.iter()) {
                for i in 0..4 {
                    convergence = convergence.max((y[i] - z[i]).abs() / (1.0 + z[i].abs()));
                }
                for sign in [-1.0, 1.0] {
                    let t = scalar(sign * z[3] * rp).sub(fit.periapsis_time).unwrap();
                    let read = fit.trajectory.state(t).unwrap();
                    let got =
                        cartesian(read, fit.periapsis_angle, fit.clockwise, (0, -60)).unwrap();
                    let phi = sign * z[2];
                    let r = z[0];
                    let speed = v / f * (1.0 - 2.0 / (rp * r));
                    let vr = sign * speed * z[1];
                    let vt = speed / r;
                    let x = [rp * r * phi.cos(), rp * r * phi.sin()];
                    let vel = [
                        vr * phi.cos() - vt * phi.sin(),
                        vr * phi.sin() + vt * phi.cos(),
                    ];
                    let dx = ((got.position[0] as f64 - x[0]).powi(2)
                        + (got.position[1] as f64 - x[1]).powi(2))
                    .sqrt()
                        / (rp * r);
                    let dv = ((got.velocity[0] as f64 * 2f64.powi(-60) - vel[0]).powi(2)
                        + (got.velocity[1] as f64 * 2f64.powi(-60) - vel[1]).powi(2))
                    .sqrt()
                        / v;
                    assert!(dx.is_finite() && dv.is_finite());
                    wx = wx.max(dx);
                    wv = wv.max(dv);
                }
            }
            println!("R1 {au} AU E={e}: position={wx:.3e} velocity={wv:.3e}");
            worst_x = worst_x.max(wx);
            worst_v = worst_v.max(wv);
        }
    }
    println!(
        "R1 refusals={refused}/12 worst_position={worst_x:.3e} worst_velocity={worst_v:.3e} oracle_convergence={convergence:.3e}"
    );
    assert_eq!(refused, 0);
    assert!(convergence < 1e-9);
    assert!(worst_x <= 1e-6 && worst_v <= 1e-6);
}

#[test]
fn shape_range_extends_below_both_fixed_point_quanta() {
    for re in [40i16, 64, 100, 200] {
        let st = IntegerState {
            position: [1 << 50, 0],
            velocity: [0, 1 << 59],
            length_exponent: re - 50,
            velocity_exponent: -60,
        };
        let radius = Scalar::power_of_two(re);
        let fit = Rebinding::from_state(st, Scalar::ZERO, Some(radius.scale(12).unwrap())).unwrap();
        assert_eq!(fit.reconstruct().unwrap(), st);
        let key = fit.trajectory.key().unwrap();
        assert!(key.k_exponent < 0 && !key.periodic());
        assert!(key.shape().unwrap().is_positive());
        let memo = key.memo_key().unwrap();
        assert!(memo.k_exponent < 0 && memo.gap.is_some());
        emergent_space::orbit::Passage::compile(memo, radius.scale(12).unwrap()).unwrap();
        for sign in [-1, 1] {
            let time = radius.mul(Scalar::integer(sign)).unwrap();
            let s = fit
                .trajectory
                .state(time.sub(fit.periapsis_time).unwrap())
                .unwrap();
            let got = cartesian(s, fit.periapsis_angle, fit.clockwise, (re - 50, -60)).unwrap();
            // At >=2^40 M the exact curvature correction is <1e-10 here.
            let x = got.position[0] as f64 / 2f64.powi(50);
            let y = got.position[1] as f64 / 2f64.powi(50);
            assert!(
                (x - 1.0).abs() < 1e-8 && (y - sign as f64 * 0.5).abs() < 1e-8,
                "2^{re}: {x} {y}"
            );
        }
    }
}

#[test]
fn invariant_compilation_carries_the_same_small_shape_and_clock() {
    use emergent_space::orbit::{OrbitKey, Passage};
    for re in [29, 34, 40, 60] {
        let r = Scalar::power_of_two(re);
        let f = Scalar::ONE
            .sub(r.reciprocal().unwrap().scale(1).unwrap())
            .unwrap();
        for energy in [3, 1000, 1_000_000] {
            let e = Scalar::integer(energy);
            let l = r
                .mul(
                    e.mul(e)
                        .unwrap()
                        .div(f)
                        .unwrap()
                        .sub(Scalar::ONE)
                        .unwrap()
                        .sqrt()
                        .unwrap(),
                )
                .unwrap();
            let key = OrbitKey::from_invariants(Scalar::integer(energy - 1), l).unwrap();
            assert!(key.k_exponent < 0 && key.gap.is_some());
            let p = Passage::compile(key, r.scale(8).unwrap()).unwrap();
            let t = r.scale(2).unwrap();
            let dt = r.scale(-10).unwrap();
            let tau = p
                .state(t.add(dt).unwrap())
                .unwrap()
                .proper_time
                .sub(p.state(t).unwrap().proper_time)
                .unwrap();
            let ratio = dt
                .div(tau)
                .unwrap()
                .div(e)
                .unwrap()
                .sub(Scalar::ONE)
                .unwrap()
                .abs();
            assert!(
                ratio < Scalar::power_of_two(-25),
                "r=2^{re} E={energy}: {ratio:?}"
            );
        }
    }
}
