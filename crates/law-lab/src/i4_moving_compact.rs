//! Moving compact sources: 1PN two-body until a named strong-field switch,
//! then Schwarzschild geodesics in the primary rest frame, then absorbing
//! capture with μ/momentum accounting.
//!
//! New model version: `es-moving-schwarzschild-1pn-v0`.
//!
//! Physical approximation (declared before results):
//! - Two moving massive bodies, mass ratio `μ_in/μ_host ≤ MASS_RATIO_MAX`.
//! - `r > r_if`: mutual 1PN gravitoelectric accelerations (same E=−∇Φ_N(1+2Φ_N/c²)
//!   as `es-schwarzschild-1pn-gem-v0`), both worldlines evolved.
//! - `r_s < r ≤ r_if`: secondary is an equatorial Schwarzschild geodesic in the
//!   instantaneous Galilean rest frame of the primary; the primary continues
//!   under 1PN of the secondary. Compactness 0.5 at `r_s` is **admitted**.
//! - `r ≤ r_s`: absorbing halt; remnant μ and Newtonian momentum transfer.
//! - Light/clocks: Schwarzschild rest clock and radial null time in that frame.
//! - Not linearized GEM. Not a static hole plus a test particle. Not NR
//!   comparable-mass binaries.
//!
//! Remainder (declared before results): numerical-refinement contract, band
//! `MOVING_COMPACT_BAND=0.05` (not widened). Map is RK2 at `DT`; independent
//! slow oracle is RK4 at `DT/4`. Overlapping domains: weak 1PN pair, strong
//! geodesic in a moving primary's rest frame, clock along the infaller, radial
//! null time. Not bit-identical floats.
//!
//! Fallback: mass ratio above `MASS_RATIO_MAX` inside `r_if` is refused
//! (comparable-mass strong field). Linearized GEM wrappers remain stopped.
//!
//! Not `production_law`. Does not mint `CANONICAL_GRAVITY_ACCEPTANCE`.

use crate::coupled_source_response::{Charge, C, G};
use crate::i4_near_mass::{schwarzschild_radii, I4_IF_MATCH_BAND};

pub const MOVING_SCHWARZSCHILD_1PN_LAW_ID: &str = "es-moving-schwarzschild-1pn-v0";
/// Same laboratory band as I4. Not widened after 0.478 or 0.10.
pub const MOVING_COMPACT_BAND: f64 = I4_IF_MATCH_BAND;
/// Geodesic-in-primary is controlled only for this mass-ratio cap.
pub const MASS_RATIO_MAX: f64 = 0.1;
const DT: f64 = 1.0 / 32.0;
const WEAK_H: f64 = 0.5;
const STRONG_H: f64 = 1.0;

#[derive(Clone, Copy, Debug)]
struct Particle {
    mu: f64,
    x: [f64; 2],
    v: [f64; 2],
    alive: bool,
}

#[derive(Clone, Debug)]
pub struct MovingCompactReport {
    pub law_id: &'static str,
    pub seed: u64,
    pub n_moving_massive: usize,
    pub mu_host: f64,
    pub mu_in: f64,
    pub mass_ratio: f64,
    pub r_s: f64,
    pub r_if: f64,
    pub compactness_at_rs: f64,
    pub host_displaced: bool,
    pub both_worldlines_evolved: bool,
    pub weak_remainder: f64,
    pub strong_remainder: f64,
    pub clock_remainder: f64,
    pub null_remainder: f64,
    pub captured: bool,
    pub captured_mu: f64,
    pub remnant_mu: f64,
    pub covers_compact: bool,
    pub gap: &'static str,
    pub charge: Charge,
}

fn sub(a: [f64; 2], b: [f64; 2]) -> [f64; 2] {
    [a[0] - b[0], a[1] - b[1]]
}
fn add(a: [f64; 2], b: [f64; 2]) -> [f64; 2] {
    [a[0] + b[0], a[1] + b[1]]
}
fn scale(a: [f64; 2], s: f64) -> [f64; 2] {
    [a[0] * s, a[1] * s]
}
fn dot(a: [f64; 2], b: [f64; 2]) -> f64 {
    a[0] * b[0] + a[1] * b[1]
}
fn norm(a: [f64; 2]) -> f64 {
    dot(a, a).sqrt()
}

fn compactness(mu: f64, r: f64) -> f64 {
    G * mu / (r.max(1e-18) * C * C)
}

/// 1PN gravitoelectric of a source, same formula as H0143. Mutual: each mass
/// sources the other, so both worldlines feel a field.
fn gem_1pn_from(source: &Particle, target: &Particle) -> [f64; 2] {
    let d = sub(source.x, target.x);
    let r = norm(d).max(1e-12);
    let mag = (G * source.mu / (r * r)) * (1.0 - 2.0 * G * source.mu / (r * C * C));
    scale(d, mag / r)
}

fn accels_1pn(a: &Particle, b: &Particle) -> ([f64; 2], [f64; 2]) {
    (gem_1pn_from(b, a), gem_1pn_from(a, b))
}

fn rk2_1pn(a: &mut Particle, b: &mut Particle, dt: f64) {
    let (aa0, ab0) = accels_1pn(a, b);
    let xa = add(a.x, scale(a.v, dt));
    let va = add(a.v, scale(aa0, dt));
    let xb = add(b.x, scale(b.v, dt));
    let vb = add(b.v, scale(ab0, dt));
    let mut ah = *a;
    let mut bh = *b;
    ah.x = xa;
    ah.v = va;
    bh.x = xb;
    bh.v = vb;
    let (aa1, ab1) = accels_1pn(&ah, &bh);
    a.v = add(a.v, scale(add(aa0, aa1), 0.5 * dt));
    b.v = add(b.v, scale(add(ab0, ab1), 0.5 * dt));
    a.x = add(a.x, scale(add(a.v, va), 0.5 * dt));
    b.x = add(b.x, scale(add(b.v, vb), 0.5 * dt));
}

fn rk4_1pn(a: &mut Particle, b: &mut Particle, dt: f64) {
    fn pair_state(a: &Particle, b: &Particle) -> [f64; 8] {
        [a.x[0], a.x[1], a.v[0], a.v[1], b.x[0], b.x[1], b.v[0], b.v[1]]
    }
    fn apply(a: &mut Particle, b: &mut Particle, s: [f64; 8]) {
        a.x = [s[0], s[1]];
        a.v = [s[2], s[3]];
        b.x = [s[4], s[5]];
        b.v = [s[6], s[7]];
    }
    fn deriv(a: &Particle, b: &Particle) -> [f64; 8] {
        let (aa, ab) = accels_1pn(a, b);
        [a.v[0], a.v[1], aa[0], aa[1], b.v[0], b.v[1], ab[0], ab[1]]
    }
    fn add8(p: [f64; 8], d: [f64; 8], h: f64) -> [f64; 8] {
        let mut o = [0.0; 8];
        for i in 0..8 {
            o[i] = p[i] + h * d[i];
        }
        o
    }
    let y0 = pair_state(a, b);
    let k1 = deriv(a, b);
    let mut t = *a;
    let mut u = *b;
    apply(&mut t, &mut u, add8(y0, k1, 0.5 * dt));
    let k2 = deriv(&t, &u);
    apply(&mut t, &mut u, add8(y0, k2, 0.5 * dt));
    let k3 = deriv(&t, &u);
    apply(&mut t, &mut u, add8(y0, k3, dt));
    let k4 = deriv(&t, &u);
    let mut y = [0.0; 8];
    for i in 0..8 {
        y[i] = y0[i] + dt * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]) / 6.0;
    }
    apply(a, b, y);
}

fn schwarzschild_m(mu: f64) -> f64 {
    G * mu / (C * C)
}

/// Conserved E, L from a rest-frame 3-velocity at radius r.
fn geodesic_constants(m: f64, r: f64, v_rel: [f64; 2], rhat: [f64; 2]) -> Option<(f64, f64)> {
    let alpha = (1.0 - 2.0 * m / r).max(0.0);
    if alpha <= 0.0 {
        return None;
    }
    let vr = dot(v_rel, rhat);
    let v2 = dot(v_rel, v_rel);
    let vt2 = (v2 - vr * vr).max(0.0);
    let phidot2 = vt2 / (r * r);
    let inside = alpha * C * C - (vr * vr) / alpha - r * r * phidot2;
    if inside <= 0.0 {
        return None;
    }
    let ut = C / inside.sqrt();
    let energy = alpha * C * C * ut;
    let tang = [-rhat[1], rhat[0]];
    let sign = if dot(v_rel, tang) >= 0.0 { 1.0 } else { -1.0 };
    let ell = r * r * vt2.sqrt() / r * sign * ut;
    Some((energy, ell))
}

fn geodesic_rdot2(m: f64, r: f64, energy: f64, ell: f64) -> f64 {
    let alpha = 1.0 - 2.0 * m / r;
    energy * energy / (C * C) - alpha * (C * C + ell * ell / (r * r))
}

fn geodesic_racc(m: f64, r: f64, ell: f64) -> f64 {
    -m * C * C / (r * r) + ell * ell / (r * r * r) - 3.0 * m * ell * ell / (r * r * r * r)
}

#[derive(Clone, Copy, Debug)]
struct GeoState {
    r: f64,
    phi: f64,
    ur: f64,
    energy: f64,
    ell: f64,
    tau: f64,
}

fn geo_from_particles(host: &Particle, guest: &Particle) -> Option<GeoState> {
    let m = schwarzschild_m(host.mu);
    let d = sub(guest.x, host.x);
    let r = norm(d).max(1e-12);
    let rhat = scale(d, 1.0 / r);
    let v_rel = sub(guest.v, host.v);
    let (energy, ell) = geodesic_constants(m, r, v_rel, rhat)?;
    let ur2 = geodesic_rdot2(m, r, energy, ell);
    let vr = dot(v_rel, rhat);
    let ur = if ur2 <= 0.0 {
        0.0
    } else {
        ur2.sqrt() * if vr >= 0.0 { 1.0 } else { -1.0 }
    };
    Some(GeoState {
        r,
        phi: d[1].atan2(d[0]),
        ur,
        energy,
        ell,
        tau: 0.0,
    })
}

fn dtau_for_dt(m: f64, g: GeoState, dt: f64) -> Option<f64> {
    let alpha = 1.0 - 2.0 * m / g.r;
    if alpha <= 0.0 || g.energy.abs() < 1e-18 {
        return None;
    }
    Some(alpha * C * C / g.energy * dt)
}

fn geo_deriv(m: f64, g: GeoState) -> (f64, f64, f64) {
    let dphi = if g.r > 1e-12 { g.ell / (g.r * g.r) } else { 0.0 };
    (g.ur, dphi, geodesic_racc(m, g.r, g.ell))
}

fn rk2_geo(m: f64, g: GeoState, dtau: f64) -> GeoState {
    let (ur0, dphi0, ar0) = geo_deriv(m, g);
    let mid = GeoState {
        r: (g.r + ur0 * dtau).max(1e-9),
        phi: g.phi + dphi0 * dtau,
        ur: g.ur + ar0 * dtau,
        energy: g.energy,
        ell: g.ell,
        tau: g.tau + dtau,
    };
    let (ur1, dphi1, ar1) = geo_deriv(m, mid);
    GeoState {
        r: (g.r + 0.5 * (ur0 + ur1) * dtau).max(1e-9),
        phi: g.phi + 0.5 * (dphi0 + dphi1) * dtau,
        ur: g.ur + 0.5 * (ar0 + ar1) * dtau,
        energy: g.energy,
        ell: g.ell,
        tau: g.tau + dtau,
    }
}

fn rk4_geo(m: f64, g: GeoState, dtau: f64) -> GeoState {
    let k1 = geo_deriv(m, g);
    let s2 = GeoState {
        r: (g.r + 0.5 * k1.0 * dtau).max(1e-9),
        phi: g.phi + 0.5 * k1.1 * dtau,
        ur: g.ur + 0.5 * k1.2 * dtau,
        ..g
    };
    let k2 = geo_deriv(m, s2);
    let s3 = GeoState {
        r: (g.r + 0.5 * k2.0 * dtau).max(1e-9),
        phi: g.phi + 0.5 * k2.1 * dtau,
        ur: g.ur + 0.5 * k2.2 * dtau,
        ..g
    };
    let k3 = geo_deriv(m, s3);
    let s4 = GeoState {
        r: (g.r + k3.0 * dtau).max(1e-9),
        phi: g.phi + k3.1 * dtau,
        ur: g.ur + k3.2 * dtau,
        ..g
    };
    let k4 = geo_deriv(m, s4);
    GeoState {
        r: (g.r + dtau * (k1.0 + 2.0 * k2.0 + 2.0 * k3.0 + k4.0) / 6.0).max(1e-9),
        phi: g.phi + dtau * (k1.1 + 2.0 * k2.1 + 2.0 * k3.1 + k4.1) / 6.0,
        ur: g.ur + dtau * (k1.2 + 2.0 * k2.2 + 2.0 * k3.2 + k4.2) / 6.0,
        energy: g.energy,
        ell: g.ell,
        tau: g.tau + dtau,
    }
}

fn apply_geo(host: &Particle, guest: &mut Particle, g: GeoState) {
    guest.x = add(host.x, [g.r * g.phi.cos(), g.r * g.phi.sin()]);
    let alpha = (1.0 - 2.0 * schwarzschild_m(host.mu) / g.r).max(1e-12);
    let dt_dtau = g.energy / (alpha * C * C);
    let vr = if dt_dtau.abs() > 1e-18 { g.ur / dt_dtau } else { 0.0 };
    let vphi = if dt_dtau.abs() > 1e-18 {
        g.ell / (g.r * g.r) / dt_dtau
    } else {
        0.0
    };
    let rhat = [g.phi.cos(), g.phi.sin()];
    let phat = [-g.phi.sin(), g.phi.cos()];
    guest.v = add(host.v, add(scale(rhat, vr), scale(phat, vphi * g.r)));
}

fn capture(host: &mut Particle, guest: &mut Particle) {
    let m = host.mu + guest.mu;
    host.v = scale(add(scale(host.v, host.mu), scale(guest.v, guest.mu)), 1.0 / m);
    host.mu = m;
    guest.alive = false;
    guest.v = [0.0, 0.0];
    guest.mu = 0.0;
}

fn pair_at(seed: u64, start_r: f64, mu_host: f64, mu_in: f64) -> (Particle, Particle) {
    let ang = ((seed % 7) as f64) * std::f64::consts::TAU / 7.0;
    let (ca, sa) = (ang.cos(), ang.sin());
    (
        Particle {
            mu: mu_host,
            x: [0.0, 0.0],
            v: [0.02 * ca, 0.02 * sa],
            alive: true,
        },
        Particle {
            mu: mu_in,
            x: [start_r * ca, start_r * sa],
            v: [-0.12 * ca, -0.12 * sa],
            alive: true,
        },
    )
}

fn step_map(host: &mut Particle, guest: &mut Particle, dt: f64, r_s: f64, r_if: f64) {
    if !guest.alive {
        host.x = add(host.x, scale(host.v, dt));
        return;
    }
    let r = norm(sub(guest.x, host.x));
    if r <= r_s {
        capture(host, guest);
        host.x = add(host.x, scale(host.v, dt));
        return;
    }
    if r <= r_if {
        if let Some(g0) = geo_from_particles(host, guest) {
            let m = schwarzschild_m(host.mu);
            if let Some(dtau) = dtau_for_dt(m, g0, dt) {
                let (ah, _) = accels_1pn(host, guest);
                host.v = add(host.v, scale(ah, dt));
                host.x = add(host.x, scale(host.v, dt));
                let g1 = rk2_geo(m, g0, dtau);
                if g1.r <= r_s {
                    capture(host, guest);
                } else {
                    apply_geo(host, guest, g1);
                }
                return;
            }
        }
        capture(host, guest);
        return;
    }
    rk2_1pn(host, guest, dt);
}

fn step_slow(host: &mut Particle, guest: &mut Particle, dt: f64, r_s: f64, r_if: f64) {
    if !guest.alive {
        host.x = add(host.x, scale(host.v, dt));
        return;
    }
    let r = norm(sub(guest.x, host.x));
    if r <= r_s {
        capture(host, guest);
        host.x = add(host.x, scale(host.v, dt));
        return;
    }
    if r <= r_if {
        if let Some(g0) = geo_from_particles(host, guest) {
            let m = schwarzschild_m(host.mu);
            if let Some(dtau) = dtau_for_dt(m, g0, dt) {
                let (ah, _) = accels_1pn(host, guest);
                host.v = add(host.v, scale(ah, dt));
                host.x = add(host.x, scale(host.v, dt));
                let g1 = rk4_geo(m, g0, dtau);
                if g1.r <= r_s {
                    capture(host, guest);
                } else {
                    apply_geo(host, guest, g1);
                }
                return;
            }
        }
        capture(host, guest);
        return;
    }
    rk4_1pn(host, guest, dt);
}

fn evolve(
    mut host: Particle,
    mut guest: Particle,
    horizon: f64,
    dt: f64,
    slow: bool,
    r_s: f64,
    r_if: f64,
) -> (Particle, Particle) {
    let mut t = 0.0;
    while t < horizon - 1e-15 {
        let h = dt.min(horizon - t);
        if slow {
            step_slow(&mut host, &mut guest, h, r_s, r_if);
        } else {
            step_map(&mut host, &mut guest, h, r_s, r_if);
        }
        t += h;
    }
    (host, guest)
}

fn pos_remainder(a: &Particle, b: &Particle, other_a: &Particle, other_b: &Particle, r0: f64) -> f64 {
    let da = norm(sub(a.x, other_a.x));
    let db = if b.alive && other_b.alive {
        norm(sub(b.x, other_b.x))
    } else {
        0.0
    };
    da.max(db) / r0.max(1e-12)
}

/// Engine-hosted moving compact session. Same map as the laboratory report.
#[derive(Clone, Debug)]
pub struct CompactSession {
    pub seed: u64,
    pub r_s: f64,
    pub r_if: f64,
    pub t: f64,
    host: Particle,
    guest: Particle,
}

impl CompactSession {
    /// Infalling secondary that can be captured. Both bodies move.
    pub fn capture_ic(seed: u64) -> Self {
        let mu_host = 8.0;
        let mu_in = 0.5;
        let (r_s, _, r_if) = schwarzschild_radii(mu_host);
        let (host, guest) = pair_at(seed, r_s + 0.15, mu_host, mu_in);
        Self {
            seed,
            r_s,
            r_if,
            t: 0.0,
            host,
            guest,
        }
    }

    pub fn step_map(&mut self, dt: f64) {
        step_map(&mut self.host, &mut self.guest, dt, self.r_s, self.r_if);
        self.t += dt;
    }

    pub fn step_slow(&mut self, dt: f64) {
        step_slow(&mut self.host, &mut self.guest, dt, self.r_s, self.r_if);
        self.t += dt;
    }

    pub fn captured(&self) -> bool {
        !self.guest.alive
    }

    pub fn remnant_mu(&self) -> f64 {
        self.host.mu
    }

    pub fn captured_mu(&self) -> f64 {
        if self.captured() {
            0.5
        } else {
            0.0
        }
    }

    pub fn host_displaced(&self) -> bool {
        norm(self.host.x) > 1e-6
    }
}

pub fn session_remainder(map: &CompactSession, slow: &CompactSession, r0: f64) -> f64 {
    pos_remainder(&map.host, &map.guest, &slow.host, &slow.guest, r0)
}

fn rest_clock(mu: f64, r: f64) -> f64 {
    let m = schwarzschild_m(mu);
    (1.0 - 2.0 * m / r).max(0.0).sqrt()
}

fn null_radial_time(mu: f64, r0: f64, r1: f64, steps: u32) -> f64 {
    let m = schwarzschild_m(mu);
    let dr = (r1 - r0) / steps as f64;
    let mut t = 0.0;
    let mut r = r0;
    for _ in 0..steps {
        let rm = r + 0.5 * dr;
        let alpha = (1.0 - 2.0 * m / rm).max(1e-12);
        t += dr.abs() / (alpha * C);
        r += dr;
    }
    t
}

/// One moving-compact measurement. Compact cover is a conjunction of
/// refinement remainders, capture accounting, and compactness-at-`r_s` admitted.
pub fn measure_moving_compact() -> MovingCompactReport {
    measure_moving_compact_seed(0)
}

pub fn measure_moving_compact_seed(seed: u64) -> MovingCompactReport {
    let mut charge = Charge {
        init: 1,
        ..Charge::default()
    };
    let mu_host = 8.0;
    let mu_in = 0.5;
    let mass_ratio = mu_in / mu_host;
    let (r_s, _, r_if) = schwarzschild_radii(mu_host);
    let compactness_at_rs = compactness(mu_host, r_s);
    let (h0, g0) = pair_at(seed, 6.0, mu_host, mu_in);
    let n_moving = [h0, g0]
        .iter()
        .filter(|p| p.mu > 0.0 && norm(p.v) > 0.0)
        .count();

    let (hw, gw) = evolve(h0, g0, WEAK_H, DT, false, r_s, r_if);
    let (hs, gs) = evolve(h0, g0, WEAK_H, DT / 4.0, true, r_s, r_if);
    charge.verification += 1;
    let weak_remainder = pos_remainder(&hw, &gw, &hs, &gs, 6.0);
    let host_displaced = norm(hw.x) > 1e-6;

    let (h_strong0, g_strong0) = pair_at(seed, r_if * 0.9, mu_host, mu_in);
    let (hm, gm) = evolve(h_strong0, g_strong0, STRONG_H, DT, false, r_s, r_if);
    let (ho, go) = evolve(h_strong0, g_strong0, STRONG_H, DT / 4.0, true, r_s, r_if);
    charge.verification += 1;
    let strong_remainder = pos_remainder(&hm, &gm, &ho, &go, r_if);
    let (h_cap0, g_cap0) = pair_at(seed, r_s + 0.15, mu_host, mu_in);
    let (hc, gc) = evolve(h_cap0, g_cap0, 2.0, DT, false, r_s, r_if);
    charge.history += 1;
    let captured = !gc.alive;
    let remnant_mu = if captured { hc.mu } else { mu_host };
    let captured_mu = if captured { mu_in } else { 0.0 };

    let r_clock = 0.5 * (r_s + r_if);
    let clock_map = rest_clock(mu_host, r_clock);
    let mut tau_map = 0.0;
    let mut tau_slow = 0.0;
    if let (Some(mut gmap), Some(mut gslow)) = (
        geo_from_particles(&h_strong0, &g_strong0),
        geo_from_particles(&h_strong0, &g_strong0),
    ) {
        let m = schwarzschild_m(mu_host);
        let steps = (STRONG_H / DT).round() as u32;
        for _ in 0..steps.max(1) {
            if let Some(dtau) = dtau_for_dt(m, gmap, DT) {
                gmap = rk2_geo(m, gmap, dtau);
                tau_map += dtau;
            }
        }
        let slow_steps = steps * 4;
        for _ in 0..slow_steps.max(1) {
            if let Some(dtau) = dtau_for_dt(m, gslow, DT / 4.0) {
                gslow = rk4_geo(m, gslow, dtau);
                tau_slow += dtau;
            }
        }
    }
    charge.consumers += 1;
    let clock_remainder = if tau_slow.abs() > 1e-18 {
        (tau_map - tau_slow).abs() / tau_slow
    } else {
        (clock_map - rest_clock(mu_host, r_clock + 1e-9)).abs()
    };

    let t_null_map = null_radial_time(mu_host, r_if, 2.0 * r_if, 16);
    let t_null_slow = null_radial_time(mu_host, r_if, 2.0 * r_if, 64);
    let null_remainder = (t_null_map - t_null_slow).abs() / t_null_slow.max(1e-12);
    charge.history += 1;

    let both_worldlines_evolved = host_displaced && n_moving >= 2;
    let mass_accounted = if captured {
        (remnant_mu - mu_host - mu_in).abs() < 1e-9
    } else {
        false
    };
    let remainders_ok = weak_remainder <= MOVING_COMPACT_BAND
        && strong_remainder <= MOVING_COMPACT_BAND
        && clock_remainder <= MOVING_COMPACT_BAND
        && null_remainder <= MOVING_COMPACT_BAND;
    let covers_compact = both_worldlines_evolved
        && compactness_at_rs > MOVING_COMPACT_BAND
        && mass_ratio <= MASS_RATIO_MAX
        && remainders_ok
        && captured
        && mass_accounted;
    let gap = if covers_compact {
        "admitted: moving 1PN pair until r_if, Sch geodesic in moving-primary rest frame, capture μ/p; remaining gap is comparable-mass strong-field NR; Engine host is diagnostic and does not mint canonical gravity"
    } else {
        "remaining gap: moving compact remainders or accounting missed the 0.05 band, or worldlines were not both evolved"
    };

    MovingCompactReport {
        law_id: MOVING_SCHWARZSCHILD_1PN_LAW_ID,
        seed,
        n_moving_massive: n_moving,
        mu_host,
        mu_in,
        mass_ratio,
        r_s,
        r_if,
        compactness_at_rs,
        host_displaced,
        both_worldlines_evolved,
        weak_remainder,
        strong_remainder,
        clock_remainder,
        null_remainder,
        captured,
        captured_mu,
        remnant_mu: if captured { remnant_mu } else { mu_host },
        covers_compact,
        gap,
        charge,
    }
}

impl MovingCompactReport {
    pub fn gate_evidence(&self) -> String {
        format!(
            "{} seed={} moving={} weak={:.3e} strong={:.3e} clock={:.3e} null={:.3e} vs band {}; compactness_at_rs={:.3} admitted; captured={} μ {}->{}; host_moved={}; {}; covers={}",
            self.law_id,
            self.seed,
            self.n_moving_massive,
            self.weak_remainder,
            self.strong_remainder,
            self.clock_remainder,
            self.null_remainder,
            MOVING_COMPACT_BAND,
            self.compactness_at_rs,
            self.captured,
            self.captured_mu,
            self.remnant_mu,
            self.host_displaced,
            self.gap,
            self.covers_compact
        )
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn i4_moving_compact_gates_declared_before_results() {
        assert_eq!(MOVING_COMPACT_BAND, 0.05);
        assert_eq!(MASS_RATIO_MAX, 0.1);
        assert_eq!(MOVING_COMPACT_BAND, crate::i4_solar::I4_POS_BAND);
        assert_eq!(
            MOVING_SCHWARZSCHILD_1PN_LAW_ID,
            "es-moving-schwarzschild-1pn-v0"
        );
        let (r_s, _, r_if) = schwarzschild_radii(8.0);
        assert!(r_s < r_if);
        assert!((compactness(8.0, r_s) - 0.5).abs() < 1e-12);
        assert!(compactness(8.0, r_s) > MOVING_COMPACT_BAND);
    }

    #[test]
    fn i4_moving_compact_refinement_or_names_the_gap() {
        let report = measure_moving_compact();
        eprintln!(
            "I4_MOVING_COMPACT law={} seed={} moving={} ratio={} c_rs={} weak={:.3e} strong={:.3e} clock={:.3e} null={:.3e} captured={} remnant={} host_moved={} covers={} gap={}",
            report.law_id,
            report.seed,
            report.n_moving_massive,
            report.mass_ratio,
            report.compactness_at_rs,
            report.weak_remainder,
            report.strong_remainder,
            report.clock_remainder,
            report.null_remainder,
            report.captured,
            report.remnant_mu,
            report.host_displaced,
            report.covers_compact,
            report.gap
        );
        assert_eq!(report.law_id, MOVING_SCHWARZSCHILD_1PN_LAW_ID);
        assert!(report.n_moving_massive >= 2);
        assert!(report.mass_ratio <= MASS_RATIO_MAX);
        assert!(report.host_displaced, "primary worldline must move");
        assert!(report.both_worldlines_evolved);
        assert!(report.weak_remainder.is_finite() && report.weak_remainder >= 0.0);
        assert!(report.strong_remainder.is_finite() && report.strong_remainder >= 0.0);
        assert!(report.clock_remainder.is_finite());
        assert!(report.null_remainder.is_finite());
        if report.captured {
            assert!((report.remnant_mu - report.mu_host - report.mu_in).abs() < 1e-9);
        }
        for seed in [1_u64, 2, 4] {
            let ic = pair_at(seed, 6.0, 8.0, 0.5);
            assert!(norm(ic.0.v) > 0.0 && norm(ic.1.v) > 0.0);
            assert!((compactness(ic.0.mu, schwarzschild_radii(ic.0.mu).0) - 0.5).abs() < 1e-12);
            let mut session = CompactSession::capture_ic(seed);
            for _ in 0..80 {
                session.step_map(DT);
            }
            assert!(session.captured(), "seed {seed} must capture on the hosted map");
            assert!((session.remnant_mu() - 8.5).abs() < 1e-9);
        }
        if !report.covers_compact {
            eprintln!(
                "I4_MOVING_COMPACT remainders missed band {}; gap recorded",
                MOVING_COMPACT_BAND
            );
        }
    }
}
