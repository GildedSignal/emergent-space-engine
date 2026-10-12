//! Independent checks: stored direct Hamiltonian integrations, the BL metric,
//! exact symmetries and the old compiler as zero-spin control. No B19 code here.
use emergent_space::{
    kerr::{
        self, ArcSegment, Catalogue, Constants, Cycle, Fate, Generator, Memo, Spin, TurningPassage,
    },
    orbit::{Orbit, OrbitKey, Scalar as S},
    Tube,
};
fn s(x: f64) -> S {
    if x == 0.0 {
        return S::ZERO;
    }
    let e = x.abs().log2().floor() as i32;
    S::raw((x * 2f64.powi(60 - e)).round() as i128, e - 60).unwrap()
}
fn d(x: S) -> f64 {
    x.significand() as f64 * 2f64.powi(x.exponent() as i32 - 62)
}
fn spin(a: f64) -> Spin {
    Spin::new(s(a)).unwrap()
}
fn ecc(e: f64) -> u64 {
    (e * 2f64.powi(48)).round() as u64
}
fn close(a: f64, b: f64, tol: f64) {
    assert!(
        if b == 0.0 {
            a.abs() < tol
        } else {
            (a / b - 1.0).abs() < tol
        },
        "{a} vs {b}"
    );
}

#[test]
fn bound_cycles_match_direct_hamiltonian_vectors() {
    // Provenance: 20261006-0030-q-kerr-compile-0528/test_vectors.json.
    // These increments were checked by direct Hamiltonian RK4, not Darwin.
    for (a, p, e, retro, phi, t, tau) in [
        (
            0.9,
            4.810153110795966,
            0.1,
            false,
            10.94572925383988,
            126.43618043592615,
            86.40570927652092,
        ),
        (
            0.9,
            22.148318632714066,
            0.9,
            true,
            7.787620343827078,
            8214.592404333464,
            8099.885317844605,
        ),
        (
            0.998,
            2.5937458051328415,
            0.1,
            false,
            16.074326272579998,
            83.5510778358974,
            38.354371309230326,
        ),
        (
            0.998,
            3.537677026578967,
            0.6,
            false,
            12.844784346684217,
            142.05385087736753,
            96.75214463662161,
        ),
        (
            0.998,
            19.709177440566453,
            0.3,
            true,
            8.139003936870065,
            793.0354606352269,
            733.8562982353002,
        ),
    ] {
        let c = Cycle::bound(spin(a), s(p), ecc(e), retro).unwrap();
        close(d(c.advance().unwrap()) + std::f64::consts::TAU, phi, 2e-9);
        close(d(c.period().unwrap()), t, 2e-9);
        close(d(c.proper_period().unwrap()), tau, 2e-9);
        assert_eq!(c.constants().fate(spin(a)).unwrap(), Fate::Bound);
        let inv = Cycle::from_constants(spin(a), c.constants()).unwrap();
        close(d(inv.period().unwrap()), t, 2e-8);
    }
}
#[test]
fn zero_spin_reuses_every_old_cycle_readout_bit() {
    for p in [8.0, 40.0, 1e6, 1e20] {
        for e in [0.0, 0.01, 0.7] {
            let old = Orbit::compile(OrbitKey::bound(s(p), ecc(e)).unwrap()).unwrap();
            let c = Cycle::bound(Spin::ZERO, s(p), ecc(e), false).unwrap();
            assert_eq!(c.advance().unwrap(), old.advance().unwrap());
            assert_eq!(c.period().unwrap(), old.period().unwrap());
            assert_eq!(c.proper_period().unwrap(), old.proper_period().unwrap());
            for f in [0.0, 0.13, 0.5, 0.91, 1.0, 13.12] {
                let t = old.period().unwrap().mul(s(f)).unwrap();
                assert_eq!(c.state(t).unwrap(), old.state(t).unwrap());
            }
        }
    }
    for b in [5.3, 10.0, 1e6] {
        let old = emergent_space::orbit::Passage::photon(s(b), s(2.0 * b))
            .unwrap()
            .unwrap();
        assert_eq!(
            kerr::deflection(Spin::ZERO, s(b)).unwrap().unwrap(),
            old.deflection().unwrap()
        );
    }
}
#[test]
fn circular_stability_and_critical_capture_are_dynamical() {
    for (a, isco, retro_isco, bp, bm, lmbp, lmbm) in [
        (
            0.5,
            4.233002529530826,
            7.554584714512358,
            4.096266658713868,
            -6.1381557247154515,
            3.414213562373095,
            -4.449489742783178,
        ),
        (
            0.9,
            2.320883041761887,
            8.717352279606489,
            2.8444214034761693,
            -6.832319230446666,
            2.632455532033676,
            -4.756809750418044,
        ),
        (
            0.998,
            1.2369706551751847,
            8.99437445480357,
            2.11088779455283,
            -6.996666271399958,
            2.0894427190999916,
            -4.827012557453539,
        ),
    ] {
        let a = spin(a);
        for (retro, r) in [(false, isco), (true, retro_isco)] {
            assert!(!a.circular(s(r * 0.999), retro).unwrap().unwrap().1);
            assert!(a.circular(s(r * 1.001), retro).unwrap().unwrap().1);
            assert!(Cycle::bound(a, s(r * 0.999), 0, retro).is_err());
            Cycle::bound(a, s(r * 1.001), 0, retro).unwrap();
        }
        for b in [bp, bm] {
            for f in [0.9, 0.9999, 1.0001, 1.1] {
                assert_eq!(
                    Constants::photon(s(b * f)).fate(a).unwrap(),
                    if f < 1.0 {
                        Fate::Captured
                    } else {
                        Fate::Scattered
                    }
                );
            }
        }
        for l in [lmbp, lmbm] {
            for f in [0.9, 0.9999, 1.0001, 1.1] {
                assert_eq!(
                    Constants::massive(S::ONE, s(l * f)).fate(a).unwrap(),
                    if f < 1.0 {
                        Fate::Captured
                    } else {
                        Fate::Scattered
                    }
                );
            }
        }
    }
}
fn check_metric(a: f64, c: Constants, state: &emergent_space::orbit::OrbitState) {
    let r = d(state.radius);
    let vr = d(state.radial_velocity);
    let omega = d(state.transverse_velocity) / r;
    let gtt = -(1.0 - 2.0 / r);
    let gtp = -2.0 * a / r;
    let gpp = r * r + a * a + 2.0 * a * a / r;
    let grr = r * r / (r * r - 2.0 * r + a * a);
    let rate = c.tube_rates(spin(a), state.radius).unwrap().unwrap();
    let tau = if c.null { 0.0 } else { d(rate[1]) };
    assert!(
        (gtt + 2.0 * gtp * omega + gpp * omega * omega + grr * vr * vr + tau * tau).abs() < 2e-8,
        "metric r={r} vr={vr}"
    );
    if !c.null {
        close(-(gtt + gtp * omega) / tau, d(c.energy), 2e-8);
        close((gtp + gpp * omega) / tau, d(c.angular), 2e-8);
    }
}
#[test]
fn cycle_readout_obeys_metric_and_repeats_without_evolution() {
    for a in [0.5, 0.998] {
        for retro in [false, true] {
            let c = Cycle::bound(spin(a), s(20.0), ecc(0.5), retro).unwrap();
            let period = c.period().unwrap();
            for f in [0.0, 0.1, 0.5, 0.8, 1.0] {
                let t = period.mul(s(f)).unwrap();
                let st = c.state(t).unwrap();
                check_metric(a, c.constants(), &st);
                c.state(period.mul(s(1000.23)).unwrap()).unwrap();
                assert_eq!(c.state(t).unwrap(), st);
            }
            let t = period.mul(s(0.21)).unwrap();
            let x = c.state(t).unwrap();
            let y = c
                .state(t.add(period.mul(s(1024.0)).unwrap()).unwrap())
                .unwrap();
            close(d(x.radius), d(y.radius), 2e-8);
        }
    }
}
#[test]
fn finite_massive_photon_and_plunge_readouts_share_the_metric() {
    for a in [0.5, 0.998] {
        let hole = spin(a);
        for c in [
            Constants::massive(s(1.1), s(7.0)),
            Constants::massive(s(1.3), s(-10.0)),
            Constants::photon(s(8.0)),
            Constants::photon(s(-10.0)),
        ] {
            let p = TurningPassage::compile(hole, c, s(50.0)).unwrap();
            let t = p.duration().unwrap();
            for f in [0.0, 0.1, 0.5, 0.75, 1.0] {
                let st = p.state(t.mul(s(f)).unwrap()).unwrap();
                check_metric(a, c, &st);
            }
        }
        for c in [
            Constants::massive(s(0.95), s(0.0)),
            Constants::massive(s(1.3), s(1.0)),
            Constants::photon(s(0.0)),
            Constants::photon(s(-1.0)),
        ] {
            let end = hole.horizon().unwrap().add(s(0.01)).unwrap();
            let p = ArcSegment::compile(hole, c, s(10.0), end).unwrap();
            for f in [0.0, 0.2, 0.8, 1.0] {
                let st = p.state(p.duration().mul(s(f)).unwrap()).unwrap();
                check_metric(a, c, &st);
                assert!(st.radial_velocity < S::ZERO);
            }
            assert!(ArcSegment::compile(hole, c, s(10.0), hole.horizon().unwrap()).is_err());
        }
    }
}
#[test]
fn negative_energy_is_future_directed_only_inside_and_split_conserves() {
    for a in [0.5, 0.9, 0.998] {
        let hole = spin(a);
        let r = hole
            .horizon()
            .unwrap()
            .add(s(2.0))
            .unwrap()
            .scale(-1)
            .unwrap();
        let [alpha, omega, sg] = hole.frame(r).unwrap();
        let gamma = s(1.25);
        let l = sg.mul(gamma).unwrap().mul(s(0.6)).unwrap();
        let e = alpha
            .mul(gamma)
            .unwrap()
            .add(omega.mul(l).unwrap())
            .unwrap();
        let c = Constants::massive(e, l);
        let [f, b] = c.split(hole, r).unwrap().unwrap();
        assert_eq!(f.energy.add(b.energy).unwrap(), c.energy);
        assert_eq!(f.angular.add(b.angular).unwrap(), c.angular);
        assert!(b.energy < S::ZERO && f.energy > c.energy);
        let inside = hole
            .horizon()
            .unwrap()
            .add(
                s(2.0)
                    .sub(hole.horizon().unwrap())
                    .unwrap()
                    .mul(s(0.05))
                    .unwrap(),
            )
            .unwrap();
        let [alpha, omega, sg] = hole.frame(inside).unwrap();
        let l = sg.mul(s(2.0)).unwrap().mul(s(-0.8660254037844386)).unwrap();
        let e = alpha
            .mul(s(2.0))
            .unwrap()
            .add(omega.mul(l).unwrap())
            .unwrap();
        assert!(e < S::ZERO);
        let negative = Constants::massive(e, l);
        let rates = negative.tube_rates(hole, inside).unwrap().unwrap();
        assert!(rates[0] > S::ZERO && rates[1] > S::ZERO);
        assert!(negative.tube_rates(hole, s(2.2)).unwrap().is_none());
        assert_eq!(negative.fate(hole).unwrap(), Fate::Plunge);
        let end = hole.horizon().unwrap().add(s(0.0001)).unwrap();
        let arc = ArcSegment::compile(hole, negative, inside, end).unwrap();
        check_metric(
            a,
            negative,
            &arc.state(arc.duration().scale(-1).unwrap()).unwrap(),
        );
    }
}
#[test]
fn spin_reflection_lt_scaling_and_memo_identity() {
    let mut memo = Memo::default();
    for a in [0.9, -0.9] {
        let c = memo.bound(spin(a), s(10000.0), ecc(0.3), a < 0.0).unwrap();
        let same = memo.bound(spin(a), s(10000.0), ecc(0.3), a < 0.0).unwrap();
        assert!(std::sync::Arc::ptr_eq(&c, &same));
    }
    assert_eq!(memo.len(), 2);
    let pro = Cycle::bound(spin(0.9), s(10000.0), ecc(0.3), false).unwrap();
    let dual = Cycle::bound(spin(-0.9), s(10000.0), ecc(0.3), true).unwrap();
    close(d(pro.advance().unwrap()), d(dual.advance().unwrap()), 1e-9);
    let retro = Cycle::bound(spin(0.9), s(10000.0), ecc(0.3), true).unwrap();
    let odd = (d(pro.advance().unwrap()) - d(retro.advance().unwrap())) / 2.0;
    let expected = -8.0 * std::f64::consts::PI * 0.9 / 10000f64.powf(1.5);
    close(odd, expected, 0.002);
    let mut cat = Catalogue::default();
    let id = cat
        .insert(Generator::Cycle(std::sync::Arc::new(pro)))
        .unwrap();
    let tube = Tube::new(id, 123, 0);
    assert_eq!(std::mem::size_of::<Tube>(), 16);
    let st = cat.state(tube, 1000, -4).unwrap();
    cat.state(tube, 1, -4).unwrap();
    assert_eq!(st, cat.state(tube, 1000, -4).unwrap());
}

#[test]
fn small_spin_near_circular_and_near_separatrix_limits_are_continuous() {
    for a in [1e-9, 0.5, 0.998] {
        let c0 = Cycle::bound(spin(a), s(20.0), 0, false).unwrap();
        let c1 = Cycle::bound(spin(a), s(20.0), ecc(1e-6), false).unwrap();
        close(d(c0.advance().unwrap()), d(c1.advance().unwrap()), 1e-8);
        close(d(c0.period().unwrap()), d(c1.period().unwrap()), 1e-8);
    }
    // Circular epicyclic closed form, κ²/Ω²=1-6/r+8a/r^(3/2)-3a²/r².
    for (a, isco) in [(0.9, 2.320883041761887), (0.998, 1.2369706551751847)] {
        let r = isco * (1.0 + 1e-5);
        let c = Cycle::bound(spin(a), s(r), 0, false).unwrap();
        let omega = 1.0 / (r.powf(1.5) + a);
        let kappa = omega * (1.0 - 6.0 / r + 8.0 * a / r.powf(1.5) - 3.0 * a * a / (r * r)).sqrt();
        close(d(c.period().unwrap()), std::f64::consts::TAU / kappa, 2e-7);
        close(
            d(c.advance().unwrap()) + std::f64::consts::TAU,
            std::f64::consts::TAU * omega / kappa,
            2e-7,
        );
    }
}

#[test]
fn windowed_plunges_match_direct_coordinate_time_integration() {
    // Independent float Hamiltonian first integrals in r, stepped only here.
    // The implementation integrates in a regular radial chart and inverts t.
    for (a, e, l, null) in [(0.9, 1.1, 1.0, false), (0.998, 1.0, -1.0, true)] {
        let constants = Constants {
            energy: s(e),
            angular: s(l),
            null,
        };
        let arc = ArcSegment::compile(spin(a), constants, s(10.0), s(2.0)).unwrap();
        let target = d(arc.duration()) * 0.7;
        let rhs = |y: [f64; 3]| {
            let r = y[0];
            let delta = r * r - 2.0 * r + a * a;
            let x = l - a * e;
            let pp = e * (r * r + a * a) - a * l;
            let t = a * x + (r * r + a * a) * pp / delta;
            let radial = pp * pp - delta * ((if null { 0.0 } else { r * r }) + x * x);
            [
                -radial.sqrt() / t,
                (x + a * pp / delta) / t,
                if null { 0.0 } else { r * r / t },
            ]
        };
        let add = |a: [f64; 3], b: [f64; 3], w: f64| std::array::from_fn(|i| a[i] + b[i] * w);
        let mut y = [10.0, 0.0, 0.0];
        let h = target / 4096.0;
        for _ in 0..4096 {
            let k1 = rhs(y);
            let k2 = rhs(add(y, k1, h / 2.0));
            let k3 = rhs(add(y, k2, h / 2.0));
            let k4 = rhs(add(y, k3, h));
            for i in 0..3 {
                y[i] += h * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]) / 6.0;
            }
        }
        let st = arc.state(s(target)).unwrap();
        close(d(st.radius), y[0], 1e-8);
        close(d(st.advance), y[1], 1e-8);
        close(d(st.proper_time), y[2], 1e-8);
    }
}
