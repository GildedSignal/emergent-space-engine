//! B7 derived clocks (docs/law.md, docs/PRINCIPLES.md principle 3: nothing is evolved that can be
//! derived when looked at). A law reads a clock rate from its geometry, never by stepping it, so the
//! rate must equal the oracle's closed form: √(1 − 2M/r) for a static observer, √(1 − 3M/r) for a
//! circular orbit (r > 3M). All 64 radii of both kinds must agree to 1e-12 relative: a closed form
//! has no tail to forgive. A law that has not implemented a rate fails (the trait default is None).
use super::{oracle, rel, sample, worst, Gate, Law};

pub const SEEDS: usize = 64;
pub const TOL: f64 = 1e-12;

/// One kind of clock over the seeded radii: (answered within tol, unanswered, worst error).
fn kind(radii: &[f64], ask: &dyn Fn(f64) -> Option<f64>, truth: fn(f64) -> f64) -> (usize, usize, f64) {
    let errs: Vec<Option<f64>> = radii.iter().map(|&r| ask(r).map(|v| rel(v, truth(r)))).collect();
    let ok = errs.iter().filter(|e| e.is_some_and(|e| e <= TOL)).count();
    let missing = errs.iter().filter(|e| e.is_none()).count();
    // An unanswered radius shows as infinity, a NaN answer as NaN.
    (ok, missing, worst(errs.into_iter().map(|e| e.unwrap_or(f64::INFINITY))))
}

pub fn b7(law: &dyn Law) -> Gate {
    let radii = sample::clock_radii(SEEDS);
    let s = kind(&radii, &|r| law.static_clock_rate(r), oracle::static_clock_rate);
    let c = kind(&radii, &|r| law.circular_clock_rate(r), oracle::circular_clock_rate);
    let show = |name: &str, (ok, missing, w): (usize, usize, f64)| format!("{name} {ok}/{SEEDS} within {TOL:.0e} worst {w:.2e}{}", if missing > 0 { format!(" ({missing} unanswered)") } else { String::new() });
    Gate {
        id: "B7",
        pass: s.0 == SEEDS && c.0 == SEEDS,
        detail: format!("clocks: {}, {}, radii log-uniform in [3, 1e4]", show("static", s), show("circular", c)),
        secs: 0.0,
    }
}

#[cfg(test)]
mod tests {
    use super::super::laws::{Echo, Fault, Planted};
    use super::*;

    /// The oracle's clocks with a hook on each kind, and everything else silent.
    struct Skew {
        stat: fn(f64) -> Option<f64>,
        circ: fn(f64) -> Option<f64>,
    }
    impl Law for Skew {
        fn advance_per_cycle(&self, _: f64, _: f64) -> Option<(f64, f64, f64)> {
            None
        }
        fn deflection(&self, _: f64) -> Option<f64> {
            None
        }
        fn captured(&self, _: f64, _: f64) -> bool {
            false
        }
        fn photon_captured(&self, _: f64) -> bool {
            false
        }
        fn long_run(&self, _: f64, _: f64, _: usize) -> Vec<(f64, f64, f64, f64)> {
            Vec::new()
        }
        fn static_clock_rate(&self, r: f64) -> Option<f64> {
            (self.stat)(r)
        }
        fn circular_clock_rate(&self, r: f64) -> Option<f64> {
            (self.circ)(r)
        }
    }
    fn exact_static(r: f64) -> Option<f64> {
        Echo.static_clock_rate(r)
    }
    fn exact_circular(r: f64) -> Option<f64> {
        Echo.circular_clock_rate(r)
    }

    #[test]
    fn echo_passes_and_reports_zero_error() {
        let g = b7(&Echo);
        assert!(g.pass, "{}", g.detail);
        assert!(g.detail.contains("static 64/64") && g.detail.contains("circular 64/64"), "{}", g.detail);
    }

    #[test]
    fn a_rate_off_by_1e_6_fails_and_so_does_each_kind_alone() {
        let g = b7(&Planted(Fault::Clock));
        assert!(!g.pass && g.detail.contains("static 0/64") && g.detail.contains("circular 0/64"), "{}", g.detail);
        let stat_only = Skew { stat: |r| exact_static(r).map(|x| x * (1.0 + 1e-6)), circ: exact_circular };
        let circ_only = Skew { stat: exact_static, circ: |r| exact_circular(r).map(|x| x * (1.0 + 1e-6)) };
        let (a, b) = (b7(&stat_only), b7(&circ_only));
        assert!(!a.pass && a.detail.contains("static 0/64") && a.detail.contains("circular 64/64"), "{}", a.detail);
        assert!(!b.pass && b.detail.contains("static 64/64") && b.detail.contains("circular 0/64"), "{}", b.detail);
    }

    #[test]
    fn the_tolerance_is_1e_12_relative_not_looser() {
        // 5e-13 off is inside, 5e-12 off is outside.
        let near = Skew { stat: |r| exact_static(r).map(|x| x * (1.0 + 5e-13)), circ: |r| exact_circular(r).map(|x| x * (1.0 - 5e-13)) };
        assert!(b7(&near).pass);
        let far = Skew { stat: |r| exact_static(r).map(|x| x * (1.0 + 5e-12)), circ: exact_circular };
        assert!(!b7(&far).pass);
    }

    #[test]
    fn unimplemented_nan_and_one_bad_radius_all_fail() {
        let none = Skew { stat: |_| None, circ: |_| None };
        let g = b7(&none);
        assert!(!g.pass && g.detail.contains("(64 unanswered)"), "{}", g.detail);
        let nan = Skew { stat: |_| Some(f64::NAN), circ: exact_circular };
        assert!(!b7(&nan).pass);
        // Wrong at a single radius: the gate has no 99% slack.
        let one = Skew { stat: |r| exact_static(r).map(|x| if r > 2000.0 { x * 1.001 } else { x }), circ: exact_circular };
        let radii = sample::clock_radii(SEEDS);
        assert!(radii.iter().any(|&r| r > 2000.0) && !b7(&one).pass);
        // Only the static rate answered: still a failure.
        assert!(!b7(&Skew { stat: exact_static, circ: |_| None }).pass);
    }
}
