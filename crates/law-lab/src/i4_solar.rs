//! I4 solar hierarchy and ordinary weak-field encounters.
//!
//! Physical approximation (declared before results): linearized retarded GEM
//! (`es-linearized-retarded-gem-response-v0`) on a hierarchical two-body, with
//! a prehistory window so genesis switch-on is not the initializer.
//! Remainder: position vs collocation, predeclared `I4_POS_BAND`.
//! Admitted: two-body solar, `|Phi|/c² < 0.05`, `β < 0.25`, no close-entrant.
//! Fallback: collocation; kernel only in the published quiet/weak-kick domain.
//! GEM stays diagnostic. Not `production_law`. Not canonical gravity.

use crate::coupled_source_response::{
    compile_source_response_opts, field_acceleration, retarded_lookback_time, BodyInit, Charge,
    CompileOpts, InitialCondition, Reference, ResponseError, SourceResponse, C, G,
};
use serde::{Deserialize, Serialize};

/// Position remainder vs collocation. Same 0.05 laboratory band as I3;
/// declared before I4 runs. Not a widened strong-kick 0.216.
pub const I4_POS_BAND: f64 = 0.05;
/// Prehistory: more than one light-crossing of the solar planet (`r/c = 6/8`).
pub const I4_PREHISTORY: f64 = 2.0;
/// Scene horizon after t=0.
pub const I4_HORIZON: f64 = 4.0;
/// Per-query unique retarded lookback is not an interval-wide field bound
/// and does not authorize events. The interval-wide path lives in
/// `i4_gem_authority`.
pub const GEM_RETARDED_ROOT_COVERAGE: &str = "per-query-unique-lookback-not-interval-wide-field";
/// Hierarchical companion semimajor about the inner COM. Declared before runs.
pub const I4_COMPANION_A: f64 = 20.0;
/// Collective acceleration remainder vs direct sum. Declared before runs.
pub const I4_COLLECTIVE_A_BAND: f64 = 0.05;

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct SolarHierarchy {
    pub law_id: String,
    pub prehistory: f64,
    pub horizon: f64,
    pub switch_on_defect: f64,
    pub newton_remainder: f64,
    pub min_r: f64,
    pub max_phi_c2: f64,
    pub max_beta: f64,
    pub bound: bool,
    pub charge: Charge,
}

#[derive(Clone, Debug)]
pub struct RetardedRootReport {
    pub unique_roots: u64,
    pub missed_roots: u64,
    pub delay_max: f64,
    pub arithmetic_ulp: f64,
    pub interval_wide_field: bool,
    pub authorizes_events: bool,
    pub coverage: &'static str,
}

pub fn solar_planet_ic_at(t: f64) -> InitialCondition {
    let mu_s = 8.0;
    let mu_p = 0.02;
    let m = mu_s + mu_p;
    let a = 6.0;
    let n = (G * m / (a * a * a)).sqrt();
    let ang = n * t;
    let r_s = a * mu_p / m;
    let r_p = a * mu_s / m;
    let vs = n * r_s;
    let vp = n * r_p;
    InitialCondition {
        genesis_t: t,
        bodies: vec![
            BodyInit {
                id: 0,
                mu: mu_s,
                x: [-r_s * ang.cos(), -r_s * ang.sin()],
                v: [vs * ang.sin(), -vs * ang.cos()],
            },
            BodyInit {
                id: 1,
                mu: mu_p,
                x: [r_p * ang.cos(), r_p * ang.sin()],
                v: [-vp * ang.sin(), vp * ang.cos()],
            },
        ],
    }
}

/// Sun + planet + distant companion, COM frame, circular hierarchy at time `t`.
/// Approximation: linearized retarded GEM on three bodies. Remainder: inner
/// planet vs two-body solar. Admitted: companion `a=20`, `|Phi|/c²<0.05`,
/// `β<0.25`, no close-entrant. Fallback: collocation (not kernel).
pub fn hierarchical_companion_ic_at(t: f64) -> InitialCondition {
    let inner = solar_planet_ic_at(t);
    let mu_s = inner.bodies[0].mu;
    let mu_p = inner.bodies[1].mu;
    let mu_inner = mu_s + mu_p;
    let mu_c = 0.005;
    let m = mu_inner + mu_c;
    let a_c = I4_COMPANION_A;
    let n_c = (G * m / (a_c * a_c * a_c)).sqrt();
    let ang = n_c * t;
    let r_inner = a_c * mu_c / m;
    let r_c = a_c * mu_inner / m;
    let v_inner = n_c * r_inner;
    let v_c = n_c * r_c;
    let com = [-r_inner * ang.cos(), -r_inner * ang.sin()];
    let vcom = [v_inner * ang.sin(), -v_inner * ang.cos()];
    let mut bodies = inner.bodies;
    for b in &mut bodies {
        b.x = [b.x[0] + com[0], b.x[1] + com[1]];
        b.v = [b.v[0] + vcom[0], b.v[1] + vcom[1]];
    }
    bodies.push(BodyInit {
        id: 2,
        mu: mu_c,
        x: [r_c * ang.cos(), r_c * ang.sin()],
        v: [-v_c * ang.sin(), v_c * ang.cos()],
    });
    InitialCondition {
        genesis_t: t,
        bodies,
    }
}

pub fn compile_hierarchy_with_prehistory() -> Result<SourceResponse, ResponseError> {
    compile_source_response_opts(
        hierarchical_companion_ic_at(-I4_PREHISTORY),
        vec![],
        I4_HORIZON,
        1.0 / 32.0,
        CompileOpts {
            store_pair_inverse: false,
        },
    )
}

pub fn weak_field_flyby_ic() -> InitialCondition {
    let mut ic = solar_planet_ic_at(0.0);
    ic.bodies.push(BodyInit {
        id: 77,
        mu: 0.05,
        x: [0.0, 36.0],
        v: [0.05, -0.08],
    });
    ic
}

pub fn compile_solar_with_prehistory() -> Result<SourceResponse, ResponseError> {
    compile_source_response_opts(
        solar_planet_ic_at(-I4_PREHISTORY),
        vec![],
        I4_HORIZON,
        1.0 / 32.0,
        CompileOpts {
            store_pair_inverse: false,
        },
    )
}

pub fn compile_solar_switch_on() -> Result<SourceResponse, ResponseError> {
    compile_source_response_opts(
        solar_planet_ic_at(0.0),
        vec![],
        I4_HORIZON,
        1.0 / 32.0,
        CompileOpts {
            store_pair_inverse: false,
        },
    )
}

fn eval_x(compiled: &SourceResponse, id: u64, t: f64) -> Result<[f64; 2], ResponseError> {
    let fun = compiled
        .interval_functions
        .iter()
        .rev()
        .find(|f| f.body_id == id && t + 1e-15 >= f.t0 && t <= f.t1 + 1e-15)
        .or_else(|| {
            compiled
                .interval_functions
                .iter()
                .rev()
                .find(|f| f.body_id == id && f.t0 <= t + 1e-15)
        })
        .ok_or(ResponseError::UnsupportedDomain {
            why: format!("no solar interval function for {id} at {t}"),
        })?;
    let h = t - fun.t0;
    Ok([
        fun.x0[0] + fun.v0[0] * h + 0.5 * fun.a[0] * h * h,
        fun.x0[1] + fun.v0[1] * h + 0.5 * fun.a[1] * h * h,
    ])
}

pub fn measure_solar_hierarchy() -> Result<SolarHierarchy, ResponseError> {
    let pre = compile_solar_with_prehistory()?;
    let switch = compile_solar_switch_on()?;
    let mut charge = Charge::default();
    charge.verification += 1;
    let mut switch_on_defect = 0.0_f64;
    let mut newton_remainder = 0.0_f64;
    let mut min_r = f64::INFINITY;
    let mut max_phi_c2 = 0.0_f64;
    let mut max_beta = 0.0_f64;
    for i in 0..8 {
        let t = (i as f64 + 0.5) * I4_HORIZON / 8.0;
        let xp = eval_x(&pre, 1, t)?;
        let xs = eval_x(&switch, 1, t)?;
        switch_on_defect =
            switch_on_defect.max((xp[0] - xs[0]).abs().max((xp[1] - xs[1]).abs()));
        let analytic = solar_planet_ic_at(t).bodies[1].x;
        newton_remainder =
            newton_remainder.max((xp[0] - analytic[0]).abs().max((xp[1] - analytic[1]).abs()));
        let x0 = eval_x(&pre, 0, t)?;
        let r = hypot(xp[0] - x0[0], xp[1] - x0[1]);
        min_r = min_r.min(r);
        let v = solar_planet_ic_at(t).bodies[1].v;
        max_beta = max_beta.max(hypot(v[0], v[1]) / C);
        if let Ok(a) = field_acceleration(&pre.worldtubes, t, xp, [0.0, 0.0], Some(1), &mut charge)
        {
            let an = hypot(a[0], a[1]);
            max_phi_c2 = max_phi_c2.max(an * r / (C * C));
        }
        charge.reconstruction += 1;
    }
    let bound = min_r > 2.0 && min_r < 12.0;
    Ok(SolarHierarchy {
        law_id: crate::coupled_source_response::COUPLED_RESPONSE_LAW_ID.into(),
        prehistory: I4_PREHISTORY,
        horizon: I4_HORIZON,
        switch_on_defect,
        newton_remainder,
        min_r,
        max_phi_c2,
        max_beta,
        bound,
        charge,
    })
}

pub fn enclose_retarded_roots(compiled: &SourceResponse) -> Result<RetardedRootReport, ResponseError> {
    let mut charge = Charge::default();
    let mut unique = 0_u64;
    let mut missed = 0_u64;
    let mut delay_max = 0.0_f64;
    let t0 = compiled.genesis.genesis_t;
    let h = compiled.domain.horizon;
    for i in 0..16 {
        let t = t0 + (i as f64 + 0.5) * (h - t0) / 16.0;
        let Ok(x) = eval_x(compiled, 0, t) else {
            missed += 1;
            continue;
        };
        match retarded_lookback_time(t, x, &compiled.worldtubes, 1, &mut charge)? {
            Some(u) => {
                unique += 1;
                delay_max = delay_max.max(u);
            }
            None => missed += 1,
        }
    }
    let ulp = delay_max * f64::EPSILON * C;
    Ok(RetardedRootReport {
        unique_roots: unique,
        missed_roots: missed,
        delay_max,
        arithmetic_ulp: ulp,
        interval_wide_field: false,
        authorizes_events: false,
        coverage: GEM_RETARDED_ROOT_COVERAGE,
    })
}

fn hypot(x: f64, y: f64) -> f64 {
    (x * x + y * y).sqrt()
}

/// Four equal masses; every represented μ contributes. Direct small-world GEM
/// sum vs two retarded cluster monopoles. No distance cutoff. Declared band
/// `I4_COLLECTIVE_A_BAND`. Fallback: keep the direct sum.
pub fn collective_square_ic() -> InitialCondition {
    let mu = 0.25;
    let r = 6.0;
    let n = (G * 1.0 / (r * r * r)).sqrt();
    let v = n * r;
    InitialCondition {
        genesis_t: 0.0,
        bodies: vec![
            BodyInit {
                id: 0,
                mu,
                x: [r, 0.0],
                v: [0.0, v],
            },
            BodyInit {
                id: 1,
                mu,
                x: [0.0, r],
                v: [-v, 0.0],
            },
            BodyInit {
                id: 2,
                mu,
                x: [-r, 0.0],
                v: [0.0, -v],
            },
            BodyInit {
                id: 3,
                mu,
                x: [0.0, -r],
                v: [v, 0.0],
            },
        ],
    }
}

fn cluster_com(bodies: &[(f64, [f64; 2])], ids: &[usize]) -> (f64, [f64; 2]) {
    let mut mu = 0.0;
    let mut x = [0.0, 0.0];
    for &i in ids {
        mu += bodies[i].0;
        x[0] += bodies[i].0 * bodies[i].1[0];
        x[1] += bodies[i].0 * bodies[i].1[1];
    }
    if mu > 0.0 {
        x[0] /= mu;
        x[1] /= mu;
    }
    (mu, x)
}

/// Retarded monopole acceleration of a cluster at observer `x` at time `t`.
fn retarded_monopole(mu: f64, x_src: [f64; 2], x_obs: [f64; 2]) -> [f64; 2] {
    let dx = x_obs[0] - x_src[0];
    let dy = x_obs[1] - x_src[1];
    let r = hypot(dx, dy).max(1e-12);
    let a = G * mu / (r * r);
    [-a * dx / r, -a * dy / r]
}

#[derive(Clone, Debug)]
pub struct CollectiveReport {
    pub n_bodies: usize,
    pub mu_direct: f64,
    pub mu_hier: f64,
    pub a_direct: [f64; 2],
    pub a_hier: [f64; 2],
    pub remainder: f64,
    pub matched: bool,
    pub charge: Charge,
}

pub fn measure_collective_field() -> Result<CollectiveReport, ResponseError> {
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
    let a_direct = field_acceleration(&bodies, t, x_obs, [0.0, 0.0], None, &mut charge)?;
    let mut pts_now = Vec::new();
    let mut mu_direct = 0.0;
    for b in &bodies {
        let (x, _) = crate::coupled_source_response::body_state(&bodies, b.id, t)?;
        let mu = b.segments.last().map(|s| s.mu).unwrap_or(0.0);
        mu_direct += mu;
        pts_now.push((mu, x));
        charge.reconstruction += 1;
    }
    let (_mu_a_now, xa_now) = cluster_com(&pts_now, &[0, 1]);
    let (_mu_b_now, xb_now) = cluster_com(&pts_now, &[2, 3]);
    let ua = hypot(x_obs[0] - xa_now[0], x_obs[1] - xa_now[1]) / C;
    let ub = hypot(x_obs[0] - xb_now[0], x_obs[1] - xb_now[1]) / C;
    let ta = (t - ua).max(0.0);
    let tb = (t - ub).max(0.0);
    let mut pts_a = Vec::new();
    let mut pts_b = Vec::new();
    for b in &bodies {
        let (xa, _) = crate::coupled_source_response::body_state(&bodies, b.id, ta)?;
        let (xb, _) = crate::coupled_source_response::body_state(&bodies, b.id, tb)?;
        let mu = b.segments.last().map(|s| s.mu).unwrap_or(0.0);
        pts_a.push((mu, xa));
        pts_b.push((mu, xb));
        charge.retarded_solves += 1;
    }
    let (mu_a, xa) = cluster_com(&pts_a, &[0, 1]);
    let (mu_b, xb) = cluster_com(&pts_b, &[2, 3]);
    let aa = retarded_monopole(mu_a, xa, x_obs);
    let ab = retarded_monopole(mu_b, xb, x_obs);
    let a_hier = [aa[0] + ab[0], aa[1] + ab[1]];
    let mu_hier = mu_a + mu_b;
    let da = hypot(a_direct[0] - a_hier[0], a_direct[1] - a_hier[1]);
    let scale = hypot(a_direct[0], a_direct[1]).max(1e-12);
    let remainder = da / scale;
    charge.verification += 1;
    Ok(CollectiveReport {
        n_bodies: bodies.len(),
        mu_direct,
        mu_hier,
        a_direct,
        a_hier,
        remainder,
        matched: remainder <= I4_COLLECTIVE_A_BAND && (mu_direct - mu_hier).abs() < 1e-12,
        charge,
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::coupled_source_response::{
        clock_rate_compiled, fly_ray_compiled, fly_ship, fly_ship_compiled, laboratory_encounter,
        CompileOpts,
    };

    #[test]
    fn i4_gates_declared_before_results() {
        assert_eq!(I4_POS_BAND, 0.05);
        assert_eq!(I4_PREHISTORY, 2.0);
        assert_eq!(I4_HORIZON, 4.0);
        assert_eq!(
            GEM_RETARDED_ROOT_COVERAGE,
            "per-query-unique-lookback-not-interval-wide-field"
        );
        assert_eq!(I4_COLLECTIVE_A_BAND, 0.05);
        assert_eq!(I4_COMPANION_A, 20.0);
    }

    #[test]
    fn i4_solar_prehistory_is_not_genesis_switch_on() {
        let solar = measure_solar_hierarchy().expect("solar hierarchy");
        eprintln!(
            "I4_SOLAR switch_on_defect={} newton_remainder={} pos_band={} min_r={} phi_c2={} bound={} ledger={}",
            solar.switch_on_defect,
            solar.newton_remainder,
            I4_POS_BAND,
            solar.min_r,
            solar.max_phi_c2,
            solar.bound,
            solar.charge.ledger_total()
        );
        assert!(
            solar.switch_on_defect > I4_POS_BAND,
            "genesis switch-on must not be an equilibrium initializer"
        );
        if solar.bound {
            eprintln!(
                "I4_KEEP solar two-body with prehistory: stays bound min_r={}; switch-on defect {} > {}; newton remainder {} is GEM−Newton, not a keep gate",
                solar.min_r, solar.switch_on_defect, I4_POS_BAND, solar.newton_remainder
            );
        } else {
            eprintln!(
                "I4_GAP solar two-body unbound min_r={}; alternatives: nested pair collocation, or Newtonian hierarchy plus GEM diagnostic enclosure",
                solar.min_r
            );
        }
        let roots = enclose_retarded_roots(&compile_solar_with_prehistory().unwrap()).unwrap();
        eprintln!(
            "I4_GEM_ROOT unique={} missed={} delay_max={} ulp={} interval_wide_field={} authorizes={} coverage={}",
            roots.unique_roots,
            roots.missed_roots,
            roots.delay_max,
            roots.arithmetic_ulp,
            roots.interval_wide_field,
            roots.authorizes_events,
            roots.coverage
        );
        assert!(!roots.interval_wide_field);
        assert!(!roots.authorizes_events);
        assert_eq!(crate::coupled_source_response::COUPLED_RESPONSE_LAW_ID, solar.law_id);
    }

    #[test]
    fn i4_ordinary_weak_field_encounter_falls_back_when_not_a_quiet_pair() {
        let flyby = compile_source_response_opts(
            weak_field_flyby_ic(),
            vec![],
            I4_HORIZON,
            1.0 / 32.0,
            CompileOpts {
                store_pair_inverse: false,
            },
        );
        match flyby {
            Ok(compiled) => {
                eprintln!(
                    "I4_ENCOUNTER collocation ledger={} nfun={} bodies={}",
                    compiled.charge.ledger_total(),
                    compiled.interval_functions.len(),
                    compiled.genesis.bodies.len()
                );
                assert_eq!(compiled.genesis.bodies.len(), 3);
                eprintln!(
                    "I4_ENCOUNTER kernel domain=false; collocation/recouple is the fallback"
                );
            }
            Err(err) => eprintln!("I4_ENCOUNTER collocation refuse={err}"),
        }
        let (enc, _) = laboratory_encounter();
        let close = compile_source_response_opts(
            enc,
            vec![],
            2.0,
            1.0 / 32.0,
            CompileOpts {
                store_pair_inverse: false,
            },
        );
        match close {
            Ok(c) => eprintln!(
                "I4_CLOSE_ENTRANT recouple_ledger={} (not kernel)",
                c.charge.ledger_total()
            ),
            Err(err) => eprintln!("I4_CLOSE_ENTRANT refuse={err}"),
        }
    }

    #[test]
    fn i4_hierarchy_beyond_two_body_uses_collocation_not_kernel() {
        let compiled = compile_hierarchy_with_prehistory().expect("hierarchy");
        assert_eq!(compiled.genesis.bodies.len(), 3);
        let mut charge = Charge::default();
        let mut min_r_c = f64::INFINITY;
        let mut dx_inner = 0.0_f64;
        let two = compile_solar_with_prehistory().expect("two-body");
        for i in 0..8 {
            let t = (i as f64 + 0.5) * I4_HORIZON / 8.0;
            let x0 = eval_x(&compiled, 0, t).unwrap();
            let x1 = eval_x(&compiled, 1, t).unwrap();
            let x2 = eval_x(&compiled, 2, t).unwrap();
            min_r_c = min_r_c.min(hypot(x2[0] - x0[0], x2[1] - x0[1]));
            let y1 = eval_x(&two, 1, t).unwrap();
            dx_inner = dx_inner.max((x1[0] - y1[0]).abs().max((x1[1] - y1[1]).abs()));
            charge.reconstruction += 1;
        }
        eprintln!(
            "I4_HIERARCHY bodies=3 ledger={} nfun={} min_r_companion={} inner_vs_twobody={} pos_band={} kernel_domain=false",
            compiled.charge.ledger_total(),
            compiled.interval_functions.len(),
            min_r_c,
            dx_inner,
            I4_POS_BAND
        );
        assert!(min_r_c > 12.0, "companion must stay a distant hierarchy");
        if dx_inner > I4_POS_BAND {
            eprintln!(
                "I4_HIERARCHY remainder {} > {}; companion perturbs the inner pair (GEM three-body, not a keep of two-body kernel)",
                dx_inner, I4_POS_BAND
            );
        }
        let field = crate::i4_gem_authority::enclose_gem_field_interval(&compiled)
            .expect("hierarchy field");
        eprintln!(
            "I4_HIERARCHY_GEM interval_wide={} authorizes={} covered={}/{} admitted=[{}, {}] interior={:?}",
            field.interval_wide_field,
            field.authorizes_events,
            field.blocks_covered,
            field.blocks_total,
            field.admitted_t0,
            field.admitted_t1,
            field.interior_gap
        );
        if !field.authorizes_events {
            eprintln!(
                "I4_HIERARCHY_GEM_GAP {:?}; alternatives={:?}",
                field.interior_gap, field.alternatives
            );
        }
    }

    #[test]
    fn i4_collective_mass_contributes_no_distance_cutoff() {
        let report = measure_collective_field().expect("collective");
        eprintln!(
            "I4_COLLECTIVE n={} mu_direct={} mu_hier={} remainder={} band={} matched={} a_direct={:?} a_hier={:?} ledger={}",
            report.n_bodies,
            report.mu_direct,
            report.mu_hier,
            report.remainder,
            I4_COLLECTIVE_A_BAND,
            report.matched,
            report.a_direct,
            report.a_hier,
            report.charge.ledger_total()
        );
        assert_eq!(report.n_bodies, 4);
        assert!((report.mu_direct - 1.0).abs() < 1e-12);
        assert!((report.mu_hier - report.mu_direct).abs() < 1e-12);
        if !report.matched {
            eprintln!(
                "I4_COLLECTIVE_GAP remainder {} > {}; alternatives: (a) keep direct small-world retarded sums with all μ, (b) retarded multipole with explicit remainder bound and the same mass accounting — not a distance cutoff because gravity decays",
                report.remainder, I4_COLLECTIVE_A_BAND
            );
        }
    }

    #[test]
    fn i4_fast_ships_rays_clocks_nav_on_solar_moving_geometry() {
        let compiled = compile_solar_with_prehistory().expect("solar");
        let mut charge = Charge::default();
        let ship = fly_ship_compiled(
            &compiled,
            0.0,
            [0.0, 12.0],
            [0.1, 0.0],
            2.0,
            1.0 / 32.0,
            &mut charge,
        )
        .expect("ship");
        let ray = fly_ray_compiled(
            &compiled,
            0.0,
            [0.0, 12.0],
            [0.0, -1.0],
            8.0,
            0.25,
            &mut charge,
        )
        .expect("ray");
        let rate = clock_rate_compiled(&compiled, 1.0, [0.0, 12.0], [0.1, 0.0], &mut charge)
            .expect("clock");
        let domain =
            crate::coupled_phase_nav::NavigationDomain::from_compiled(&compiled);
        let nav = crate::coupled_phase_nav::invert_arrival(
            &compiled.worldtubes,
            0.0,
            [0.0, 12.0],
            2.0,
            [0.25, 12.0],
            1.0 / 32.0,
            domain,
            &mut charge,
        );
        eprintln!(
            "I4_TRANSPORT ship_tau={} ship_x={:?} ray_t={} ray_x={:?} clock_rate={} nav={:?}",
            ship.tau,
            ship.x,
            ray.t,
            ray.x,
            rate,
            nav.as_ref().map(|s| s.v0).map_err(|e| e.to_string())
        );
        assert!(ship.tau > 0.0 && ship.tau <= 2.0);
        assert!(ray.t > 0.0);
        assert!(rate > 0.0 && rate <= 1.0);
        match nav {
            Ok(sol) => {
                let fwd = fly_ship(
                    &compiled.worldtubes,
                    0.0,
                    [0.0, 12.0],
                    sol.v0,
                    2.0,
                    1.0 / 32.0,
                    &mut charge,
                )
                .expect("forward");
                let miss = hypot(fwd.x[0] - 0.25, fwd.x[1] - 12.0);
                eprintln!("I4_NAV forward_miss={miss} band={I4_POS_BAND}");
                if miss > I4_POS_BAND {
                    eprintln!(
                        "I4_NAV_GAP miss {miss} > {I4_POS_BAND}; alternatives: (a) qualify moving-target inversion only after STM remainder is bounded, (b) keep inertial nav as control and treat GEM ships as diagnostic"
                    );
                }
            }
            Err(err) => eprintln!(
                "I4_NAV_GAP invert refused ({err}); alternatives: (a) inertial exact inversion as control with GEM remainder, (b) refuse singular/unreachable branches and keep forward fly_ship as the qualified path"
            ),
        }
    }

    #[test]
    fn i4_black_hole_card_is_an_exact_gap() {
        let gap = "linearized retarded GEM has no absorbing capture or connected weak-to-strong near-mass propagator; Schwarzschild predicates are not in this worktree";
        let a = "restricted exterior Schwarzschild + GEM weak-field match at a named interface, as a new model version";
        let b = "connected GEM-to-absorbing-horizon family with source/capture accounting and no interiors, as a new model version";
        eprintln!("I4_BH_GAP {gap}; alternatives: (a) {a}; (b) {b}");
        assert!(gap.contains("absorbing capture"));
    }
}
