//! B11 binaries (docs/law.md; principles 2 and 13: behaviours, and errors that do not compound).
//! Two comparable masses form one doll, and ν enters through the 1PN energy map. The judge draws
//! 1024 binaries (p log-uniform in [20, 1000], e in [0, 0.6], ν in [0.01, 0.25]), turns each into
//! its 1PN reduced energy and angular momentum (the oracle's `eih_invariants`, harmonic gauge), and
//! asks the law for one radial cycle: the periapsis advance and the radial period. The oracle is
//! Damour-Deruelle (`damour_deruelle`).
//!
//! - Precession: |Δφ_law − Δφ_oracle| ≤ (0.01 + 16/p)·Δφ_oracle. The 16/p is the 1PN oracle's own
//!   uncertainty: its next term is of relative order 1/p.
//! - Period, only where the oracle's next term is negligible (5/a² ≤ 5e-4, a = p/(1 − e²)): within 1e-3.
//! - PASS iff at least 99% of all seeds pass precession and at least 99% of at least 64 judged
//!   seeds pass the period. A law that answers None fails every seed.
use super::{oracle, rel, sample, worst, Gate, Law};

pub const SEEDS: usize = 1024;
/// The precession tolerance is this plus `PRECESSION_OVER_P`/p, relative.
pub const PRECESSION_TOL: f64 = 0.01;
pub const PRECESSION_OVER_P: f64 = 16.0;
pub const PERIOD_TOL: f64 = 1e-3;
/// A seed is judged for period when the oracle's next-term estimate 5/a² is at most this.
pub const NEXT_TERM_MAX: f64 = 5e-4;
pub const JUDGED_MIN: usize = 64;

pub fn b11(law: &dyn Law) -> Gate {
    let (mut prec_ok, mut judged, mut period_ok) = (0, 0, 0);
    let (mut prec_worst, mut period_worst) = (Vec::new(), Vec::new());
    for (p, e, nu) in sample::binaries(SEEDS) {
        let (_, _, energy, angular) = oracle::eih_invariants(p, e, nu);
        let (advance, period) = oracle::damour_deruelle(energy, angular, nu);
        let answer = law.binary_cycle(energy, angular, nu);
        let prec_err = answer.map_or(f64::INFINITY, |a| rel(a.0, advance) / (PRECESSION_TOL + PRECESSION_OVER_P / p));
        prec_ok += (prec_err <= 1.0) as usize;
        prec_worst.push(prec_err);
        let a = p / (1.0 - e * e);
        if 5.0 / (a * a) <= NEXT_TERM_MAX {
            judged += 1;
            let period_err = answer.map_or(f64::INFINITY, |a| rel(a.1, period));
            period_ok += (period_err <= PERIOD_TOL) as usize;
            period_worst.push(period_err);
        }
    }
    let pass = prec_ok * 100 >= 99 * SEEDS && judged >= JUDGED_MIN && period_ok * 100 >= 99 * judged;
    let detail = format!(
        "binaries: precession {prec_ok}/{SEEDS} within (1% + 16/p), worst {:.2} of the allowance; period {period_ok}/{judged} judged within {PERIOD_TOL:.0e}, worst {:.2e} (needs {JUDGED_MIN} judged)",
        worst(prec_worst.into_iter()),
        worst(period_worst.into_iter())
    );
    Gate { id: "B11", pass, detail, secs: 0.0 }
}

#[cfg(test)]
mod tests {
    use super::super::laws::{Echo, Events, Fault, Planted, Silent};
    use super::*;

    fn events(binary: impl Fn((f64, f64)) -> Option<(f64, f64)> + 'static) -> Events {
        Events { binary: Box::new(binary), restricted: Box::new(|scene, ship, times| Echo.restricted(scene, ship, times)) }
    }

    #[test]
    fn echo_passes_every_seed_and_judges_most_of_them_for_period() {
        let g = b11(&Echo);
        assert!(g.pass && g.detail.contains("precession 1024/1024") && g.detail.contains("period 620/620"), "{}", g.detail);
    }

    #[test]
    fn newtons_law_fails_both_the_precession_and_the_period() {
        let g = b11(&Planted(Fault::Newton));
        assert!(!g.pass && g.detail.contains("precession 0/1024") && g.detail.contains("period 0/620"), "{}", g.detail);
    }

    #[test]
    fn a_law_that_answers_nothing_fails() {
        let g = b11(&Silent);
        assert!(!g.pass && g.detail.contains("precession 0/1024") && g.detail.contains("period 0/620"), "{}", g.detail);
    }

    #[test]
    fn precession_off_by_4_percent_fails_where_the_allowance_is_small_and_by_1_percent_passes() {
        // The allowance is 1% + 16/p: 4% is inside it for p up to 533 and outside above, 16% of the seeds.
        assert!(!b11(&events(|(a, t)| Some((a * 1.04, t)))).pass);
        assert!(b11(&events(|(a, t)| Some((a * 1.01, t)))).pass);
        // Only the period is judged to 1e-3: 5e-4 passes, 2e-3 fails, and the precession is then fine.
        assert!(b11(&events(|(a, t)| Some((a, t * 1.0005)))).pass);
        let g = b11(&events(|(a, t)| Some((a, t * 1.002))));
        assert!(!g.pass && g.detail.contains("precession 1024/1024") && g.detail.contains("period 0/620"), "{}", g.detail);
    }

    #[test]
    fn nan_answers_fail() {
        assert!(!b11(&events(|(_, t)| Some((f64::NAN, t)))).pass);
        assert!(!b11(&events(|(a, _)| Some((a, f64::NAN)))).pass);
    }

    #[test]
    fn ten_wrong_seeds_of_1024_are_forgiven_and_eleven_are_not() {
        // The law doubles the advance on the k seeds with the largest advances (the smallest p).
        let mut advances: Vec<f64> = sample::binaries(SEEDS).iter().map(|&(p, e, nu)| {
            let (_, _, energy, angular) = oracle::eih_invariants(p, e, nu);
            oracle::damour_deruelle(energy, angular, nu).0
        }).collect();
        advances.sort_by(|a, b| b.total_cmp(a));
        let (ten, eleven) = (advances[9], advances[10]);
        // Precession is judged relative to (1% + 16/p), which is at least 80% at p = 20: doubling is wrong for all p.
        assert!(b11(&events(move |(a, t)| Some((if a >= ten { 2.0 * a } else { a }, t)))).pass);
        let g = b11(&events(move |(a, t)| Some((if a >= eleven { 2.0 * a } else { a }, t))));
        assert!(!g.pass && g.detail.contains("precession 1013/1024"), "{}", g.detail);
    }
}
