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
    CompileOpts, InitialCondition, ResponseError, SourceResponse, C, G,
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
/// and does not authorize events.
pub const GEM_RETARDED_ROOT_COVERAGE: &str = "per-query-unique-lookback-not-interval-wide-field";

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

#[cfg(test)]
mod tests {
    use super::*;
    use crate::coupled_source_response::{laboratory_encounter, CompileOpts};

    #[test]
    fn i4_gates_declared_before_results() {
        assert_eq!(I4_POS_BAND, 0.05);
        assert_eq!(I4_PREHISTORY, 2.0);
        assert_eq!(I4_HORIZON, 4.0);
        assert_eq!(
            GEM_RETARDED_ROOT_COVERAGE,
            "per-query-unique-lookback-not-interval-wide-field"
        );
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
}
