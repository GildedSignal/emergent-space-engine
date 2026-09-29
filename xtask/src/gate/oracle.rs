//! The H0178/H0183 oracle's functions (crate::gr_oracle), evaluated in the oracle's own units
//! (G = c = M = 1) and converted to chronons here. Nothing is reimplemented except the
//! one-line clock-rate closed forms that the oracle writes inline.
use crate::gr_oracle;
use crate::gr_oracle::extended;

/// Periapsis advance per radial period, radians, at the Darwin (p, e).
pub fn periapsis_advance(p: f64, e: f64) -> f64 {
    gr_oracle::periapsis_elliptic(p, e)
}
/// Radial period in Schwarzschild t and in proper time, in units of M. For a full radial period
/// the river time T = t + f(r) has the same period as t (r returns to itself).
pub fn radial_periods(p: f64, e: f64) -> (f64, f64) {
    extended::bound_period_quad(p, e)
}
/// Light deflection (total angle minus pi), radians, at impact parameter b (units of M).
pub fn deflection(b: f64) -> f64 {
    gr_oracle::deflection_quadrature(b)
}
/// The null turning radius (units of M) for impact parameter b (units of M).
pub fn null_turning_radius(b: f64) -> f64 {
    extended::null_turning_radius(b)
}
/// Shapiro delay, units of M: the oracle's one-way excess, the sum of the two legs from the
/// turning radius r0 out to r1 and r2 (all units of M).
pub fn shapiro(r0: f64, r1: f64, r2: f64) -> f64 {
    extended::shapiro_quad_leg(r0, r1) + extended::shapiro_quad_leg(r0, r2)
}
/// The endpoints the gate uses for Shapiro, as multiples of r0: the oracle's own rows use
/// (100 r0, 120 r0) (r0 = 10, 30, 100 with r1 = 100 r0, r2 = 120 r0).
pub const SHAPIRO_ENDPOINTS: (f64, f64) = (100.0, 120.0);
/// d(tau)/dt of a static observer at r (units of M).
pub fn static_clock_rate(r: f64) -> f64 {
    (1.0 - 2.0 / r).sqrt()
}
/// d(tau)/dt of a circular orbit at r (units of M); NaN at r <= 3.
pub fn circular_clock_rate(r: f64) -> f64 {
    if r > 3.0 {
        (1.0 - 3.0 / r).sqrt()
    } else {
        f64::NAN
    }
}
/// |x| / M, from integers (the anchor's radius in units of M).
pub fn radius_over_m(x: [i128; 2], m: i128) -> f64 {
    (x[0] as f64).hypot(x[1] as f64) / m as f64
}
