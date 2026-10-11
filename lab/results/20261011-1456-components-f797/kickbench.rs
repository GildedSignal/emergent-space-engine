//! The kick's generator cost, split and floored (lab run 20261011-1456-components-f797).
//!
//! `cargo run --release -p emergent-universe --example kickbench`
//!
//! Measures, per scene (periapsis in M, eccentricity):
//!  - one compiled readout (`Orbit::state`),
//!  - `Orbit::compile` alone,
//!  - `Rebinding::from_state` (the plane's per-kick generator rebuild, minus unit plumbing),
//!  - `emergent_universe::bind::bind` (the plane's exact rebind: fit + compile + decode +
//!    turn + residual),
//!  - a kick loop at 1 / 2^8 / 2^16 velocity quanta: cost per fired kick and the fraction of
//!    fired kicks whose `OrbitKey` (a fresh compile) or exact `ShapeKey` (a shape-memo hit) changes,
//!  - the jet floor: a derivative table update, `(5·knots + 3)` components of
//!    `new = old + dE·∂E + dL·∂L`, in the crate's own `Scalar` arithmetic and in raw i128.
use emergent_space::binding::{cartesian, IntegerState, Rebinding, Trajectory};
use emergent_space::orbit::{Orbit, OrbitKey, Scalar, ShapeKey};
use emergent_universe::bind::bind;
use emergent_universe::num::time_of;
use emergent_universe::world::Unit;
use std::hint::black_box;
use std::time::{Duration, Instant};

fn bench<T>(n: u64, mut f: impl FnMut(u64) -> T) -> (f64, u64) {
    for i in 0..64 {
        black_box(f(i));
    }
    let t0 = Instant::now();
    let mut ok = 0;
    for i in 0..n {
        black_box(f(i));
        ok += 1;
    }
    let ns = t0.elapsed().as_secs_f64() * 1e9 / n as f64;
    (ns, ok)
}

fn main() {
    // An exactly circular integer state (x=[r,0], v=[0,sqrt(M/r)], both dyadic): does the
    // plane's rebind accept it? `word_for` divides by k-1, and k = 1 exactly here.
    {
        use emergent_space::binding::IntegerState;
        let circle = IntegerState {
            position: [1 << 20, 0],
            velocity: [0, 1 << 50],
            length_exponent: 0,
            velocity_exponent: -60,
        };
        match bind(circle, 1 << 40, -10, None, Unit::ONE) {
            Ok(_) => println!("exact-circle bind: Ok"),
            Err(e) => println!("exact-circle bind: Err {e:?}"),
        }
    }
    let e = |num: u64| (num * (1u64 << 48)) / 10u64; // eccentricity in Q48 tenths
    let scenes: &[(&str, i64, u64)] = &[
        ("strong rp=16M e=0.0", 16, 0),
        ("strong rp=16M e=0.5", 16, e(5)),
        ("strong rp=16M e=0.9", 16, e(9)),
        ("mid    rp=2^10M e=0.2", 1 << 10, e(2)),
        ("mid    rp=2^10M e=0.6", 1 << 10, e(6)),
        ("belt   rp=2^17M e=0.0", 1 << 17, 0),
        ("belt   rp=2^17M e=0.3", 1 << 17, e(3)),
        ("belt   rp=2^17M e=0.6", 1 << 17, e(6)),
        ("belt   rp=2^17M e=0.9", 1 << 17, e(9)),
    ];
    println!("scene | knots crossings | readout ns | compile ns | from_state ns | bind ns | bind_hd ns | kick(q) ns key% shape% | jet_scalar ns | jet_i128 ns");
    println!("---|---|---|---|---|---|---|---|---");
    for &(label, rp, eq) in scenes {
        let key = match OrbitKey::bound(Scalar::integer(rp), eq) {
            Ok(k) => k,
            Err(_) => {
                println!("{label} | compile refused");
                continue;
            }
        };
        let orbit = match Orbit::compile(key) {
            Ok(o) => o,
            Err(_) => {
                println!("{label} | compile refused");
                continue;
            }
        };
        let knots = orbit.shape().knots().len();
        let crossings = orbit.shape().crossings().len();
        let period = orbit.period().unwrap();
        // Eight phases to read at, so the Newton solve is not one memorised path.
        let phases: Vec<Scalar> = (0..8)
            .map(|i| period.mul(Scalar::raw((2 * i + 1) as i128, -4).unwrap()).unwrap())
            .collect();
        let st0 = orbit.state(phases[3]).unwrap();
        let units = (
            (st0.radius.exponent() - 60) as i16,
            (st0.transverse_velocity.abs().exponent() - 60) as i16,
        );
        let state = cartesian(st0, 0x20000000, false, units).unwrap();

        let (ns_state, _) = bench(2000, |i| orbit.state(phases[(i % 8) as usize]));
        let (ns_compile, _) = bench(2000, |_| Orbit::compile(key).unwrap());
        let (ns_from, ok_from) = bench(
            1000,
            |i| Rebinding::from_state(state, phases[(i % 8) as usize], None).unwrap(),
        );
        assert_eq!(ok_from, 1000);

        // The plane's rebind: ticks at half the period, clock exponent set so ticks ~ 2^49.
        let clock_exp = (period.exponent() - 50) as i16;
        let tick = (period.fixed(-(clock_exp as i32)).unwrap() / 2) as i64;
        let t0_tick = tick / 3;
        let (ns_bind, ok_bind) = bench(
            1000,
            |_| bind(state, black_box(t0_tick), clock_exp, None, Unit::ONE).unwrap(),
        );
        assert_eq!(ok_bind, 1000);

        // The same state expressed at a word with 4x headroom: the tube's periapsis speed
        // fits without the rebind's second, coarser-word compile (binding.rs `bind`).
        let state_hd = cartesian(st0, 0x20000000, false, (units.0 - 2, units.1 - 2)).unwrap();
        // The kick loop: every kick fires (dv >= 1 velocity quantum).
        let dt = period.mul(Scalar::raw(1, -6).unwrap()).unwrap();
        let (ns_bind_hd, ok_hd) = bench(
            1000,
            |_| bind(state_hd, black_box(t0_tick), clock_exp, None, Unit::ONE).unwrap(),
        );
        assert_eq!(ok_hd, 1000);

        let mut kick_cols = Vec::new();
        for q in [1i64, 1 << 8, 1 << 16] {
            let mut st = state;
            let mut t = phases[3];
            let mut prev_key = None;
            let mut prev_shape = None;
            let mut key_chg = 0u64;
            let mut shape_chg = 0u64;
            let n = 400u64;
            let t0 = Instant::now();
            for i in 0..n {
                st.velocity[0] = st.velocity[0].wrapping_add(q);
                t = t.add(dt).unwrap();
                let r = Rebinding::from_state(st, t, None).unwrap();
                let k = match &r.trajectory {
                    Trajectory::Cycle(o) => o.key(),
                    Trajectory::Passage(p) => p.key(),
                };
                let sh = ShapeKey::for_orbit(k).unwrap();
                if let Some(pk) = prev_key {
                    if pk != k {
                        key_chg += 1;
                    }
                }
                if let Some(ps) = prev_shape {
                    if ps != sh {
                        shape_chg += 1;
                    }
                }
                prev_key = Some(k);
                prev_shape = Some(sh);
                black_box(&r);
            }
            let per = t0.elapsed().as_secs_f64() * 1e9 / n as f64;
            kick_cols.push(format!(
                "{:.0} {}% {}%",
                per,
                key_chg * 100 / (n - 1),
                shape_chg * 100 / (n - 1)
            ));
        }

        // The jet floor: (5·knots + 3) components, two Scalar muls + two adds each.
        let comps = 5 * knots as u64 + 3;
        let (jet_scalar, _) = bench(400, |i| {
            let de = Scalar::integer(((i & 3) + 1) as i64);
            let dl = Scalar::integer(((i & 3) + 2) as i64);
            let mut pe = Scalar::integer(3);
            let mut pl = Scalar::integer(5);
            let mut acc = Scalar::integer(1);
            let mut c = 0u64;
            for _ in 0..comps {
                c = c.wrapping_add(1);
                acc = acc
                    .add(de.mul(pe).unwrap())
                    .unwrap()
                    .add(dl.mul(pl).unwrap())
                    .unwrap();
                pe = pl;
                pl = if c & 1 == 0 { Scalar::integer(5) } else { Scalar::integer(7) };
            }
            acc
        });
        let (jet_raw, _) = bench(400, |i| {
            let (de, dl) = (0x1234_5678_9abc_def0i128, 0x0fed_cba9_8765_4321i128);
            let mut acc = (i as i128) | 1;
            let mut pe = 0x5555_5555_5555_5555i128;
            let mut pl = 0x3333_3333_3333_3333i128;
            for _ in 0..comps {
                acc = acc
                    .wrapping_add(de.wrapping_mul(pe))
                    .wrapping_add(dl.wrapping_mul(pl));
                pe = acc;
                pl = pl.wrapping_add(1);
            }
            acc
        });

        println!(
            "{label} | {knots} {crossings} | {ns_state:.0} | {ns_compile:.0} | {ns_from:.0} | {ns_bind:.0} | {ns_bind_hd:.0} | {} / {} / {} | {jet_scalar:.0} | {jet_raw:.0}",
            kick_cols[0], kick_cols[1], kick_cols[2]
        );
    }
}
