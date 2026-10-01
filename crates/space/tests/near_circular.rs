//! Behave-independent checks of the law against GR. The oracle is Darwin's integrals in f64
//! (dφ/dχ = sqrt(p/(p − 6 − 2e cos χ)), u = (1 + e cos χ)/p), composite eight-point
//! Gauss–Legendre with panels refined geometrically toward χ = 0 for the separatrix. It shares
//! no code with the crate or with `behave`.
use emergent_space::orbit::{Orbit, OrbitKey, OrbitState, Scalar};
use std::f64::consts::{PI, TAU};

fn gl8() -> [(f64, f64); 8] {
    let mut out = [(0.0, 0.0); 8];
    for (i, o) in out.iter_mut().enumerate() {
        let mut x = (PI * (i as f64 + 0.75) / 8.5).cos();
        for _ in 0..100 {
            let (mut p0, mut p1) = (1.0, x);
            for k in 2..=8 {
                (p0, p1) = (
                    p1,
                    ((2 * k - 1) as f64 * x * p1 - (k - 1) as f64 * p0) / k as f64,
                );
            }
            let dp = 8.0 * (x * p1 - p0) / (x * x - 1.0);
            x -= p1 / dp;
            *o = (x, 2.0 / ((1.0 - x * x) * dp * dp));
        }
    }
    out
}
/// (advance, coordinate period, proper period) of the Schwarzschild orbit (p, e).
fn gr(p: f64, e: f64) -> (f64, f64, f64) {
    let l = (p * p / (p - 3.0 - e * e)).sqrt();
    let en = (((p - 2.0).powi(2) - 4.0 * e * e) / (p * (p - 3.0 - e * e))).sqrt();
    let mut cuts = vec![0.0];
    let mut x = 1e-7;
    while x < 0.05 {
        cuts.push(x);
        x *= 1.25;
    }
    cuts.extend((0..=600).map(|i| 0.05 + (PI - 0.05) * i as f64 / 600.0));
    let (mut phi, mut t, mut tau) = (0.0, 0.0, 0.0);
    let nodes = gl8();
    for w in cuts.windows(2) {
        for (x, wt) in nodes {
            let chi = 0.5 * (w[0] + w[1]) + 0.5 * (w[1] - w[0]) * x;
            let h = 0.5 * (w[1] - w[0]) * wt;
            let dphi = (p / (p - 6.0 - 2.0 * e * chi.cos())).sqrt() * h;
            let u = (1.0 + e * chi.cos()) / p;
            phi += dphi;
            tau += dphi / (l * u * u);
            t += dphi * en / (l * u * u * (1.0 - 2.0 * u));
        }
    }
    (2.0 * phi - TAU, 2.0 * t, 2.0 * tau)
}
fn scalar(x: f64) -> Scalar {
    let e = x.abs().log2().floor() as i32;
    Scalar::raw((x * 2f64.powi(60 - e)).round() as i128, e - 60).unwrap()
}
fn decoded(x: Scalar) -> f64 {
    x.significand() as f64 * 2f64.powi(x.exponent() as i32 - 62)
}
fn key(p: f64, e: f64) -> OrbitKey {
    OrbitKey::bound(scalar(p), (e * 2f64.powi(48)).round() as u64).unwrap()
}
/// Worst (advance, period) relative errors over the orbits; panics on a compile failure.
fn worst(orbits: impl Iterator<Item = (f64, f64)>) -> (f64, f64, usize) {
    let (mut wa, mut wp, mut n) = (0f64, 0f64, 0);
    for (p, e) in orbits {
        let c = Orbit::compile(key(p, e)).unwrap_or_else(|err| panic!("p={p} e={e}: {err:?}"));
        // The boundary accepts Q16 p and Q30 e. Near the separatrix even p's input
        // rounding matters: compare the represented input, retaining the original gates.
        let k = c.key();
        let eq = 1.0 / (k.k as f64 / 2f64.powi(48)) - 1.0;
        let pq = decoded(k.periapsis) * (1.0 + eq);
        let (a, t, tau) = gr(pq, eq);
        let adv = decoded(c.advance().unwrap());
        let ea = (adv / a - 1.0).abs();
        let ep = (decoded(c.period().unwrap()) / t - 1.0)
            .abs()
            .max((decoded(c.proper_period().unwrap()) / tau - 1.0).abs());
        assert!(
            ea <= 0.01 && ep <= 1e-3,
            "p={p} e={e}: advance {adv} vs GR {a} ({ea:.2e}), period error {ep:.2e}"
        );
        (wa, wp, n) = (wa.max(ea), wp.max(ep), n + 1);
    }
    (wa, wp, n)
}
fn ps() -> Vec<f64> {
    let mut v: Vec<f64> = (0..=72)
        .map(|i| 7.0 * (8192.0f64 / 7.0).powf(i as f64 / 72.0))
        .collect();
    v.extend([
        7.5, 8., 9., 10., 11., 12., 13., 15., 16., 17., 20., 24., 30., 31., 32., 33., 48., 64.,
        100., 128., 200., 256., 512., 1000.,
    ]);
    v
}

#[test]
fn near_circular_orbits_across_bands_within_one_percent_of_gr() {
    for e in [0.0, 1e-6, 1e-3, 0.01, 0.03] {
        let (wa, wp, n) = worst(ps().into_iter().map(|p| (p, e)));
        println!("e={e:<6} {n} orbits, p 7..8192: worst advance {wa:.2e}, worst period {wp:.2e}");
    }
}
#[test]
fn the_old_regime_boundary_and_eccentric_orbits() {
    for e in [0.032, 0.035, 0.04, 0.05, 0.1, 0.3, 0.5, 0.7, 0.9] {
        let (wa, wp, n) = worst(
            ps().into_iter()
                .filter(|&p| p > 6.0 + 2.0 * e + 0.5)
                .map(|p| (p, e)),
        );
        println!("e={e:<6} {n} orbits: worst advance {wa:.2e}, worst period {wp:.2e}");
    }
}
#[test]
fn the_whirl_near_the_separatrix() {
    for e in [0.0, 0.01, 0.1, 0.3, 0.5, 0.7] {
        let (wa, wp, n) = worst(
            [1e-3, 3e-3, 1e-2, 0.1, 0.5]
                .into_iter()
                .map(|d| (6.0 + 2.0 * e + d, e)),
        );
        println!(
            "e={e:<6} p - (6+2e) in [1e-3, 0.5], {n} orbits: worst advance {wa:.2e}, worst period {wp:.2e}"
        );
    }
}
#[test]
fn every_cycle_is_the_compiled_one() {
    for (p, e) in [
        (7.2, 0.0),
        (20.0, 0.5),
        (12.0, 1e-3),
        (500.0, 0.03),
        (8.0, 0.9),
    ] {
        let c = Orbit::compile(key(p, e)).unwrap();
        let again = Orbit::compile(key(p, e)).unwrap();
        assert_eq!(c.shape(), again.shape());
        let scale = c
            .key()
            .periapsis
            .mul(c.key().periapsis.sqrt().unwrap())
            .unwrap();
        let normalized = c.period().unwrap().div(scale).unwrap();
        for fraction in 0..13 {
            let offset = normalized
                .mul(Scalar::integer(fraction))
                .unwrap()
                .div(Scalar::integer(13))
                .unwrap();
            let first = c.at_phase(0, offset).unwrap();
            for n in [1, 10_000, 1_000_000] {
                let late = c.at_phase(n, offset).unwrap();
                assert_eq!(
                    (late.psi, late.radius, late.outbound),
                    (first.psi, first.radius, first.outbound)
                );
                assert_eq!(
                    late.advance,
                    first
                        .advance
                        .add(c.advance().unwrap().mul(Scalar::integer(n as i64)).unwrap())
                        .unwrap()
                );
                assert_eq!(
                    late.proper_time,
                    first
                        .proper_time
                        .add(
                            c.proper_period()
                                .unwrap()
                                .mul(Scalar::integer(n as i64))
                                .unwrap()
                        )
                        .unwrap()
                );
            }
        }
    }
}
#[test]
fn a_position_moves_smoothly_through_the_cycle() {
    for (p, e) in [(20.0, 0.5), (9.0, 0.05), (300.0, 0.0), (7.0, 0.3)] {
        let c = Orbit::compile(key(p, e)).unwrap();
        let mut last: Option<OrbitState> = None;
        for i in 0..997 {
            let t = c
                .period()
                .unwrap()
                .mul(Scalar::integer(i))
                .unwrap()
                .div(Scalar::integer(997))
                .unwrap();
            let pos = c.state(t).unwrap();
            if let Some(prev) = last {
                let angle =
                    |s: OrbitState| s.radial_angle as f64 / 2f64.powi(61) + decoded(s.advance);
                assert!(angle(pos) >= angle(prev) && pos.proper_time >= prev.proper_time);
                if pos.outbound && prev.outbound {
                    assert!(pos.radius >= prev.radius);
                } else if !pos.outbound && !prev.outbound {
                    assert!(pos.radius <= prev.radius);
                }
            }
            assert!(pos.radius >= c.key().periapsis);
            last = Some(pos);
        }
    }
}
