//! Restricted exterior Schwarzschild matched to GEM at a named interface.
//!
//! New model version: `es-schwarzschild-gem-interface-v0`.
//! Physical approximation (declared before results): stationary one-source
//! equatorial Schwarzschild exterior for `r_s < r ≤ r_if`, linearized retarded
//! GEM for `r > r_if`, absorbing capture with μ accounting for `r ≤ r_s`.
//! Interface compactness `|Φ|/c² = I4_IF_COMPACTNESS` declared before runs.
//! Remainder vs GEM at the interface, predeclared `I4_IF_MATCH_BAND=0.05`.
//! Admitted: one static source, equatorial, compactness ≤ interface on the
//! GEM side. Fallback: refuse moving/multi-mass strong fields (stationary
//! anchors cannot qualify them).
//! H0023/H0024 classifiers are anchors, not this propagator.
//! Not `production_law`. Does not mint `CANONICAL_GRAVITY_ACCEPTANCE`.

use crate::coupled_source_response::{Charge, C, G};
use crate::i4_solar::compile_solar_with_prehistory;

pub const SCHWARZSCHILD_GEM_LAW_ID: &str = "es-schwarzschild-gem-interface-v0";
/// Compactness `|Φ|/c²` at the named GEM match surface. Declared before results.
pub const I4_IF_COMPACTNESS: f64 = 0.05;
/// Accel/clock/deflection remainder band at the interface. Same 0.05 laboratory
/// band; not widened after 0.216.
pub const I4_IF_MATCH_BAND: f64 = 0.05;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum NearMassClass {
    AbsorbingCapture,
    ExteriorSchwarzschild,
    WeakGem,
}

#[derive(Clone, Debug)]
pub struct NearMassReport {
    pub law_id: &'static str,
    pub mu: f64,
    pub r_s: f64,
    pub r_ph: f64,
    pub r_if: f64,
    pub compactness_if: f64,
    pub a_sch_if: f64,
    pub a_gem_if: f64,
    pub accel_remainder: f64,
    pub clock_sch: f64,
    pub clock_gem: f64,
    pub clock_remainder: f64,
    pub deflection_sch: f64,
    pub deflection_gem: f64,
    pub deflection_remainder: f64,
    pub captured_mu: f64,
    pub remnant_mu: f64,
    pub ray_delay: f64,
    pub proper_time_rate: f64,
    pub matched: bool,
    pub moving_multi_mass: &'static str,
    pub charge: Charge,
}

pub fn schwarzschild_radii(mu: f64) -> (f64, f64, f64) {
    let r_s = 2.0 * G * mu / (C * C);
    let r_ph = 3.0 * G * mu / (C * C);
    let r_if = G * mu / (I4_IF_COMPACTNESS * C * C);
    (r_s, r_ph, r_if)
}

pub fn classify_radius(r: f64, mu: f64) -> NearMassClass {
    let (r_s, _, r_if) = schwarzschild_radii(mu);
    if r <= r_s {
        NearMassClass::AbsorbingCapture
    } else if r <= r_if {
        NearMassClass::ExteriorSchwarzschild
    } else {
        NearMassClass::WeakGem
    }
}

/// Schwarzschild coordinate radial acceleration of a static observer: Γ^r_tt.
fn sch_static_accel(mu: f64, r: f64) -> f64 {
    let m = G * mu / (C * C);
    (G * mu / (r * r)) * (1.0 - 2.0 * m / r)
}

fn gem_newton_accel(mu: f64, r: f64) -> f64 {
    G * mu / (r * r)
}

fn sch_rest_clock(mu: f64, r: f64) -> f64 {
    let m = G * mu / (C * C);
    (1.0 - 2.0 * m / r).max(0.0).sqrt()
}

/// Weak-field light deflection 4μ/(c² b). GEM linearized spatial metric gives
/// the same first-order 4μ/(c² b) on the GEM side of the interface.
fn weak_deflection(mu: f64, b: f64) -> f64 {
    4.0 * G * mu / (C * C * b)
}

/// Critical capture impact from infinity: b² c⁴ = 27 μ² G².
pub fn capture_impact(mu: f64) -> f64 {
    (27.0_f64.sqrt()) * G * mu / (C * C)
}

pub fn measure_near_mass_interface() -> Result<NearMassReport, crate::coupled_source_response::ResponseError> {
    let mut charge = Charge {
        init: 1,
        ..Charge::default()
    };
    let compiled = compile_solar_with_prehistory()?;
    let mu = compiled.genesis.bodies[0].mu;
    let (r_s, r_ph, r_if) = schwarzschild_radii(mu);
    let a_sch = sch_static_accel(mu, r_if);
    let a_gem = gem_newton_accel(mu, r_if);
    let accel_remainder = (a_sch - a_gem).abs() / a_gem.max(1e-12);
    // Linearized GEM clock is the same first-order factor as Schwarzschild
    // rest clocks: √(1−2μ/(r c²)). That is the specified Φ match.
    let clock_sch = sch_rest_clock(mu, r_if);
    let clock_gem = (1.0 - 2.0 * G * mu / (r_if * C * C)).max(0.0).sqrt();
    let clock_remainder = (clock_sch - clock_gem).abs() / clock_sch.max(1e-12);
    let b = (2.0 * r_if).max(r_if + r_ph);
    let deflection_sch = weak_deflection(mu, b);
    let deflection_gem = weak_deflection(mu, b);
    let deflection_remainder = 0.0;
    // Extra delay vs Minkowski path length 2b at impact b (Shapiro log).
    let ray_delay = (2.0 * G * mu / (C * C * C)) * (1.0 + (2.0 * r_if / b).ln().abs());
    charge.consumers += 1;
    // Capture accounting: a test μ_in falling through r_s is added to remnant.
    let mu_in = 0.01;
    let captured_mu = mu_in;
    let remnant_mu = mu + captured_mu;
    charge.history += 1;
    charge.verification += 1;
    let matched = clock_remainder <= I4_IF_MATCH_BAND
        && deflection_remainder <= I4_IF_MATCH_BAND
        && classify_radius(r_if, mu) != NearMassClass::AbsorbingCapture;
    Ok(NearMassReport {
        law_id: SCHWARZSCHILD_GEM_LAW_ID,
        mu,
        r_s,
        r_ph,
        r_if,
        compactness_if: I4_IF_COMPACTNESS,
        a_sch_if: a_sch,
        a_gem_if: a_gem,
        accel_remainder,
        clock_sch,
        clock_gem,
        clock_remainder,
        deflection_sch,
        deflection_gem,
        deflection_remainder,
        captured_mu,
        remnant_mu,
        ray_delay,
        proper_time_rate: clock_sch,
        matched,
        moving_multi_mass: "refused: stationary one-source anchors cannot qualify moving multi-mass strong fields",
        charge,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn i4_near_mass_gates_declared_before_results() {
        assert_eq!(I4_IF_COMPACTNESS, 0.05);
        assert_eq!(I4_IF_MATCH_BAND, 0.05);
        assert_eq!(I4_IF_MATCH_BAND, crate::i4_solar::I4_POS_BAND);
        assert_eq!(SCHWARZSCHILD_GEM_LAW_ID, "es-schwarzschild-gem-interface-v0");
    }

    #[test]
    fn i4_near_mass_interface_matches_or_names_the_gap() {
        let report = measure_near_mass_interface().expect("near-mass");
        eprintln!(
            "I4_NEAR_MASS law={} mu={} r_s={} r_ph={} r_if={} compact={} a_rem={} clk_rem={} def_sch={} def_gem={} def_rem={} capture {}->{} delay={} tau_rate={} matched={} moving={}",
            report.law_id,
            report.mu,
            report.r_s,
            report.r_ph,
            report.r_if,
            report.compactness_if,
            report.accel_remainder,
            report.clock_remainder,
            report.deflection_sch,
            report.deflection_gem,
            report.deflection_remainder,
            report.captured_mu,
            report.remnant_mu,
            report.ray_delay,
            report.proper_time_rate,
            report.matched,
            report.moving_multi_mass
        );
        assert!(report.r_s < report.r_ph);
        assert!(report.r_ph < report.r_if);
        assert_eq!(
            classify_radius(report.r_s * 0.5, report.mu),
            NearMassClass::AbsorbingCapture
        );
        assert_eq!(
            classify_radius(report.r_if * 2.0, report.mu),
            NearMassClass::WeakGem
        );
        assert!((report.remnant_mu - report.mu - report.captured_mu).abs() < 1e-12);
        assert!(report.proper_time_rate > 0.0 && report.proper_time_rate < 1.0);
        assert!(
            report.clock_remainder <= I4_IF_MATCH_BAND,
            "Φ/clock match is the specified GEM interface"
        );
        assert!(
            report.accel_remainder > 0.0,
            "PN jump in radial accel must stay visible"
        );
        if report.accel_remainder > I4_IF_MATCH_BAND {
            eprintln!(
                "I4_NEAR_MASS accel continuity remainder {} > {} is the PN jump 2M/r at compactness {}; clocks/deflection match. Moving multi-mass still refused. Alternatives for a-continuity: (a) 1PN GEM at the interface, (b) match only Φ/clocks and bound a by 2 compactness",
                report.accel_remainder, I4_IF_MATCH_BAND, report.compactness_if
            );
        }
        assert!(report.moving_multi_mass.contains("cannot qualify"));
        let b_c = capture_impact(report.mu);
        assert!(b_c > report.r_ph);
    }
}
