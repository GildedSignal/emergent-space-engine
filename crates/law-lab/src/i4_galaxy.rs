//! Galaxy-like retarded multipole vs direct small-world GEM sums.
//!
//! Physical approximation (declared before results): two-cluster retarded
//! monopole + dipole + quadrupole of linearized GEM sources. Every represented
//! μ contributes. No distance cutoff. Remainder vs direct `field_acceleration`,
//! predeclared `I4_COLLECTIVE_A_BAND`. Explicit next-order bound is the
//! octupole envelope `4 G μ ℓ³ / R⁵` plus measured GEM−Newton.
//! Admitted: N=4 square, all μ retained. Fallback: keep the direct sum.
//! Not `production_law`. Not canonical gravity.

use crate::coupled_source_response::{
    body_state, field_acceleration, Body, Charge, Reference, ResponseError, C, G,
};
use crate::i4_solar::{collective_square_ic, I4_COLLECTIVE_A_BAND};

#[derive(Clone, Copy, Debug)]
struct Moments {
    mu: f64,
    com: [f64; 2],
    dipole: [f64; 2],
    quad: [[f64; 2]; 2],
    ell: f64,
}

fn hypot(x: f64, y: f64) -> f64 {
    (x * x + y * y).sqrt()
}

fn cluster_moments(pts: &[(f64, [f64; 2])], ids: &[usize]) -> Moments {
    let mut mu = 0.0;
    let mut com = [0.0, 0.0];
    for &i in ids {
        mu += pts[i].0;
        com[0] += pts[i].0 * pts[i].1[0];
        com[1] += pts[i].0 * pts[i].1[1];
    }
    if mu > 0.0 {
        com[0] /= mu;
        com[1] /= mu;
    }
    let mut dipole = [0.0, 0.0];
    let mut quad = [[0.0, 0.0], [0.0, 0.0]];
    let mut ell = 0.0_f64;
    for &i in ids {
        let d = [pts[i].1[0] - com[0], pts[i].1[1] - com[1]];
        let d2 = d[0] * d[0] + d[1] * d[1];
        ell = ell.max(d2.sqrt());
        dipole[0] += pts[i].0 * d[0];
        dipole[1] += pts[i].0 * d[1];
        quad[0][0] += pts[i].0 * (3.0 * d[0] * d[0] - d2);
        quad[0][1] += pts[i].0 * (3.0 * d[0] * d[1]);
        quad[1][0] += pts[i].0 * (3.0 * d[1] * d[0]);
        quad[1][1] += pts[i].0 * (3.0 * d[1] * d[1] - d2);
    }
    Moments {
        mu,
        com,
        dipole,
        quad,
        ell,
    }
}

/// Newtonian multipole acceleration through quadrupole.
fn accel_multipole(m: &Moments, x_obs: [f64; 2]) -> [f64; 2] {
    let dx = x_obs[0] - m.com[0];
    let dy = x_obs[1] - m.com[1];
    let r = hypot(dx, dy).max(1e-12);
    let n = [dx / r, dy / r];
    let a_m = [
        -G * m.mu * n[0] / (r * r),
        -G * m.mu * n[1] / (r * r),
    ];
    let dn = m.dipole[0] * n[0] + m.dipole[1] * n[1];
    let a_d = [
        G * (3.0 * dn * n[0] - m.dipole[0]) / (r * r * r),
        G * (3.0 * dn * n[1] - m.dipole[1]) / (r * r * r),
    ];
    let qn = [
        m.quad[0][0] * n[0] + m.quad[0][1] * n[1],
        m.quad[1][0] * n[0] + m.quad[1][1] * n[1],
    ];
    let nqn = n[0] * qn[0] + n[1] * qn[1];
    let a_q = [
        G * (2.5 * nqn * n[0] - qn[0]) / (r * r * r * r),
        G * (2.5 * nqn * n[1] - qn[1]) / (r * r * r * r),
    ];
    [a_m[0] + a_d[0] + a_q[0], a_m[1] + a_d[1] + a_q[1]]
}

fn octupole_envelope(m: &Moments, x_obs: [f64; 2]) -> f64 {
    let r = hypot(x_obs[0] - m.com[0], x_obs[1] - m.com[1]).max(1e-12);
    4.0 * G * m.mu * m.ell.powi(3) / r.powi(5)
}

fn newton_direct(pts: &[(f64, [f64; 2])], x_obs: [f64; 2]) -> [f64; 2] {
    let mut a = [0.0, 0.0];
    for (mu, x) in pts {
        let dx = x_obs[0] - x[0];
        let dy = x_obs[1] - x[1];
        let r = hypot(dx, dy).max(1e-12);
        let s = G * *mu / (r * r * r);
        a[0] -= s * dx;
        a[1] -= s * dy;
    }
    a
}

fn pts_at(bodies: &[Body], t: f64) -> Result<Vec<(f64, [f64; 2])>, ResponseError> {
    let mut pts = Vec::new();
    for b in bodies {
        let (x, _) = body_state(bodies, b.id, t)?;
        let mu = b.segments.last().map(|s| s.mu).unwrap_or(0.0);
        pts.push((mu, x));
    }
    Ok(pts)
}

#[derive(Clone, Debug)]
pub struct GalaxyReport {
    pub n_bodies: usize,
    pub mu_direct: f64,
    pub mu_hier: f64,
    pub remainder_gem: f64,
    pub remainder_newton: f64,
    pub remainder_bound: f64,
    pub spatial_rank: usize,
    pub retained_history: usize,
    pub receiver_sensitivity: f64,
    pub repair_direct: u64,
    pub repair_multipole: u64,
    pub matched: bool,
    pub admitted: &'static str,
    pub charge: Charge,
}

/// Direct GEM sum vs retarded quadrupole clusters. Band declared in `i4_solar`.
pub fn measure_galaxy_multipole() -> Result<GalaxyReport, ResponseError> {
    let ic = collective_square_ic();
    let mut charge = Charge {
        init: 1,
        ..Charge::default()
    };
    let (bodies, evolved) = Reference::from_genesis(ic, vec![], 1.0 / 16.0).evolve_to(1.0)?;
    charge.history += evolved.history;
    charge.source_evolution += evolved.source_evolution;
    let t = 1.0;
    let x_obs = [0.0, 12.0];
    let a_gem = field_acceleration(&bodies, t, x_obs, [0.0, 0.0], None, &mut charge)?;
    let pts_now = pts_at(&bodies, t)?;
    charge.reconstruction += pts_now.len() as u64;
    let ma_now = cluster_moments(&pts_now, &[0, 1]);
    let mb_now = cluster_moments(&pts_now, &[2, 3]);
    let ua = hypot(x_obs[0] - ma_now.com[0], x_obs[1] - ma_now.com[1]) / C;
    let ub = hypot(x_obs[0] - mb_now.com[0], x_obs[1] - mb_now.com[1]) / C;
    let ta = (t - ua).max(0.0);
    let tb = (t - ub).max(0.0);
    let pts_a = pts_at(&bodies, ta)?;
    let pts_b = pts_at(&bodies, tb)?;
    charge.retarded_solves += 2;
    let ma = cluster_moments(&pts_a, &[0, 1]);
    let mb = cluster_moments(&pts_b, &[2, 3]);
    let a_hier = {
        let aa = accel_multipole(&ma, x_obs);
        let ab = accel_multipole(&mb, x_obs);
        [aa[0] + ab[0], aa[1] + ab[1]]
    };
    let mu_direct: f64 = pts_now.iter().map(|p| p.0).sum();
    let mu_hier = ma.mu + mb.mu;
    let scale = hypot(a_gem[0], a_gem[1]).max(1e-12);
    let remainder_gem = hypot(a_gem[0] - a_hier[0], a_gem[1] - a_hier[1]) / scale;
    let a_n = newton_direct(&pts_now, x_obs);
    let nscale = hypot(a_n[0], a_n[1]).max(1e-12);
    let remainder_newton = hypot(a_n[0] - a_hier[0], a_n[1] - a_hier[1]) / nscale;
    let gem_newton = hypot(a_gem[0] - a_n[0], a_gem[1] - a_n[1]) / scale;
    let remainder_bound = (octupole_envelope(&ma, x_obs) + octupole_envelope(&mb, x_obs)) / scale
        + gem_newton;

    let x_shift = [x_obs[0] + 1e-3, x_obs[1]];
    let a_gem_s = field_acceleration(&bodies, t, x_shift, [0.0, 0.0], None, &mut charge)?;
    let a_h_s = {
        let aa = accel_multipole(&ma, x_shift);
        let ab = accel_multipole(&mb, x_shift);
        [aa[0] + ab[0], aa[1] + ab[1]]
    };
    let d_direct = hypot(a_gem_s[0] - a_gem[0], a_gem_s[1] - a_gem[1]);
    let d_hier = hypot(a_h_s[0] - a_hier[0], a_h_s[1] - a_hier[1]);
    let receiver_sensitivity = (d_hier - d_direct).abs() / d_direct.max(1e-18);

    let mut kicked = bodies.clone();
    if let Some(seg) = kicked[0].segments.last_mut() {
        seg.v[0] += 0.02;
    }
    let t_repair = 1.0;
    let mut c_direct = Charge::default();
    let _ = field_acceleration(&kicked, t_repair, x_obs, [0.0, 0.0], None, &mut c_direct)?;
    let mut c_multi = Charge::default();
    let pts_k = pts_at(&kicked, t_repair)?;
    c_multi.reconstruction += pts_k.len() as u64;
    let mk = cluster_moments(&pts_k, &[0, 1]);
    let _ = accel_multipole(&mk, x_obs);
    c_multi.coefficient_construction += 1;

    charge.verification += 1;
    let matched = remainder_gem <= I4_COLLECTIVE_A_BAND
        && remainder_gem <= remainder_bound.max(I4_COLLECTIVE_A_BAND)
        && (mu_direct - mu_hier).abs() < 1e-12;
    let admitted = if matched {
        "retarded-quadrupole-clusters"
    } else {
        "direct-small-world-gem-sums"
    };
    Ok(GalaxyReport {
        n_bodies: bodies.len(),
        mu_direct,
        mu_hier,
        remainder_gem,
        remainder_newton,
        remainder_bound,
        spatial_rank: 2,
        retained_history: 2,
        receiver_sensitivity,
        repair_direct: c_direct.ledger_total(),
        repair_multipole: c_multi.ledger_total(),
        matched,
        admitted,
        charge,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn i4_galaxy_band_declared_before_results() {
        assert_eq!(I4_COLLECTIVE_A_BAND, 0.05);
    }

    #[test]
    fn i4_galaxy_multipole_keep_or_direct_fallback() {
        let report = measure_galaxy_multipole().expect("galaxy");
        eprintln!(
            "I4_GALAXY n={} mu_d={} mu_h={} rem_gem={} rem_newton={} bound={} rank={} hist={} sens={} repair_d={} repair_m={} matched={} admitted={} ledger={}",
            report.n_bodies,
            report.mu_direct,
            report.mu_hier,
            report.remainder_gem,
            report.remainder_newton,
            report.remainder_bound,
            report.spatial_rank,
            report.retained_history,
            report.receiver_sensitivity,
            report.repair_direct,
            report.repair_multipole,
            report.matched,
            report.admitted,
            report.charge.ledger_total()
        );
        assert_eq!(report.n_bodies, 4);
        assert!((report.mu_direct - report.mu_hier).abs() < 1e-12);
        assert_eq!(report.spatial_rank, 2);
        if report.matched {
            assert!(report.remainder_gem <= I4_COLLECTIVE_A_BAND);
            eprintln!("I4_KEEP retarded quadrupole clusters vs direct GEM");
        } else {
            assert_eq!(report.admitted, "direct-small-world-gem-sums");
            eprintln!(
                "I4_GALAXY_REJECT multipole rem_gem {} > {}; admitted={}; alternatives already: keep direct sums, or a higher-rank retarded expansion with the same mass accounting — not a distance cutoff",
                report.remainder_gem, I4_COLLECTIVE_A_BAND, report.admitted
            );
        }
    }
}
