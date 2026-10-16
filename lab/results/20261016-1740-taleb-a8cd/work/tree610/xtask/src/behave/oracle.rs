//! What every law is judged against: thin wrappers over `gr_oracle` and `gr_oracle_extended`
//! (float64, G = c = M = 1, one static Schwarzschild mass in the equatorial plane), plus the
//! closed-form capture thresholds. Nothing here is a law, and no engine crate is imported.
use crate::gr_oracle::{self, extended};

/// Periapsis advance per radial cycle (the angle beyond 2π), radians, at Darwin (p, e).
pub fn periapsis_advance(p: f64, e: f64) -> f64 {
    gr_oracle::periapsis_elliptic(p, e)
}
/// Radial period in Schwarzschild coordinate time and in proper time, units of M.
pub fn radial_periods(p: f64, e: f64) -> (f64, f64) {
    extended::bound_period_quad(p, e)
}
/// The exact energy and angular momentum (per unit mass) of the bound orbit (p, e).
pub fn bound_invariants(p: f64, e: f64) -> (f64, f64) {
    extended::bound_constants(p, e)
}
/// Light deflection (total angle minus π), radians, at impact parameter b (units of M).
pub fn deflection(b: f64) -> f64 {
    gr_oracle::deflection_quadrature(b)
}

/// The critical impact parameter of light, b_c = 3√3·M: light with b < b_c is captured.
pub fn photon_critical_b() -> f64 {
    3.0 * 3.0f64.sqrt()
}
/// The critical angular momentum, units of M, of a massive body that arrives from infinity with
/// energy E >= 1 (per unit mass): it is captured iff L < this. NaN for E < 1. It is the
/// unstable circular orbit u_c (the double root of E² = (1 − 2u)(1 + L²u²), 1/L² = u(1 − 3u),
/// 4u² + (3E² − 4)u + 1 − E² = 0), so it is exactly 4 at E = 1 and tends to E·b_c as E grows.
/// Accurate to 1e-12 for E <= 10 (the judge asks E = 1); the root cancels beyond that.
pub fn capture_angular(energy: f64) -> f64 {
    let u = critical_u(energy);
    1.0 / (u * (1.0 - 3.0 * u)).sqrt()
}
/// 1/r of the unstable circular orbit at energy E (u = 1/4 at E = 1); NaN for E < 1.
fn critical_u(energy: f64) -> f64 {
    if energy < 1.0 {
        return f64::NAN;
    }
    (4.0 - 3.0 * energy * energy + energy * (9.0 * energy * energy - 8.0).sqrt()) / 8.0
}

/// dτ/dt of a static observer at r (units of M): √(1 − 2M/r). B7 reads it.
pub fn static_clock_rate(r: f64) -> f64 {
    gr_oracle::static_clock_rate(r)
}
/// dτ/dt of a circular orbit at r (units of M): √(1 − 3M/r); NaN at r <= 3. B7 reads it.
pub fn circular_clock_rate(r: f64) -> f64 {
    gr_oracle::circular_clock_rate(r)
}
// The 1PN two-body invariants are the surface of B11 (binaries).
/// 1PN two-body relative motion at Darwin-like (p, e) and symmetric mass ratio ν:
/// (periapsis radius, periapsis speed, reduced energy, reduced angular momentum).
pub fn eih_invariants(p: f64, e: f64, nu: f64) -> (f64, f64, f64, f64) {
    extended::eih_invariants(p, e, nu)
}
/// Damour–Deruelle 1PN (advance per cycle, radial period) from the reduced energy and angular momentum.
pub fn damour_deruelle(energy: f64, angular: f64, nu: f64) -> (f64, f64) {
    extended::damour_deruelle(energy, angular, nu)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::f64::consts::PI;

    #[test]
    fn capture_thresholds_are_the_textbook_ones() {
        assert_eq!(capture_angular(1.0), 4.0);
        assert!((photon_critical_b() - 5.196_152_422_706_632).abs() < 1e-14);
        assert!(capture_angular(0.99).is_nan());
        // Ultrarelativistic bodies follow light: L_c / E -> b_c (1.7e-5 away at E = 100).
        assert!((capture_angular(100.0) / 100.0 / photon_critical_b() - 1.0).abs() < 1e-4);
        // The threshold is the double root of the radial potential: R(u) = R'(u) = 0.
        for energy in [1.0, 1.3, 2.0, 10.0] {
            let l = capture_angular(energy);
            let uc = critical_u(energy);
            let v = |u: f64| (1.0 - 2.0 * u) * (1.0 + l * l * u * u);
            assert!((v(uc) / (energy * energy) - 1.0).abs() < 1e-9, "E = {energy}");
            let h = 1e-6;
            assert!(((v(uc + h) - v(uc - h)) / (2.0 * h)).abs() < 1e-8 * energy * energy, "E = {energy}");
        }
    }

    #[test]
    fn wrappers_agree_with_their_closed_limits() {
        // Weak field: advance 6π/p, deflection 4/b, periods 2π a^(3/2) (1 + 3/a) and (1 + 3/2a).
        let (p, e) = (1000.0, 0.3);
        assert!((periapsis_advance(p, e) * p / (6.0 * PI) - 1.0).abs() < 0.01);
        assert!((deflection(1000.0) * 1000.0 / 4.0 - 1.0).abs() < 0.01);
        let (t, tau) = radial_periods(p, e);
        let a = p / (1.0 - e * e);
        assert!((t / (2.0 * PI * a.powf(1.5) * (1.0 + 3.0 / a)) - 1.0).abs() < 1e-4);
        assert!((tau / (2.0 * PI * a.powf(1.5) * (1.0 + 1.5 / a)) - 1.0).abs() < 1e-4);
        // Circular Schwarzschild orbit: E = (1 − 2/r)/√(1 − 3/r), L = r/√(r − 3).
        let (energy, l) = bound_invariants(20.0, 0.0);
        assert!((energy - (1.0 - 2.0 / 20.0) / (1.0 - 3.0 / 20.0f64).sqrt()).abs() < 1e-14);
        assert!((l - 20.0 / 17.0f64.sqrt()).abs() < 1e-14);
        // Clock rates: the horizon stops static clocks, and no circular orbit exists at r <= 3.
        assert_eq!(static_clock_rate(2.0), 0.0);
        assert!((circular_clock_rate(6.0) - 0.5f64.sqrt()).abs() < 1e-15);
        assert!(circular_clock_rate(3.0).is_nan());
        // Test-mass limit (ν = 0) of the 1PN pair: its advance is Schwarzschild's to O(1/p).
        let (_, _, ee, ll) = eih_invariants(300.0, 0.3, 0.0);
        assert!((damour_deruelle(ee, ll, 0.0).0 / periapsis_advance(300.0, 0.3) - 1.0).abs() < 20.0 / 300.0);
    }
}
