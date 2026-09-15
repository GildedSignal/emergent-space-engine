//! Interval-wide GEM field authority on stored-a causal blocks.
//!
//! Physical approximation (declared before results): linearized retarded GEM
//! on constant-acceleration interval functions. Delay uniqueness from `|v|<c`
//! (`g'(u) ≤ C(β−1) < 0`) plus a Krawczyk-style contraction of the delay set
//! from axis-aligned boxes of the quadratics. Tidal Lipschitz per causal block
//! from the same boxes, not from 16 samples. Arithmetic error is an ulp
//! inflation of those boxes, in length, converted to time by `/c`.
//!
//! Remainder: box-distance vs actual retarded distance (conservative).
//! Admitted: two-body (or hierarchical) compiled interval functions with
//! `β_max < 1` and `r_lo > 0` on the interior after prehistory light-travel.
//! Fallback: pending/refusal, never a guessed root. Genesis prefix without
//! incoming field is an exact gap, not an authorized event.
//!
//! This path may set `authorizes_events` on that admitted interior. It does
//! not mint `CANONICAL_GRAVITY_ACCEPTANCE` or authorize inertial engine events.

use crate::coupled_source_response::{
    Charge, ChargeRole, ChargedOp, IntervalFunction, ResponseError, SourceResponse, C, G,
};

/// Coverage string for this procedure. Distinct from the I1 16-sample
/// enclosure and from per-query unique lookback.
pub const GEM_FIELD_INTERVAL_COVERAGE: &str =
    "causal-block-lipschitz-ka-delay-admitted-interior";

/// Position remainder band, declared before this slice. Same 0.05 laboratory
/// band; not a widened 0.216.
pub const I4_AUTHORITY_POS_BAND: f64 = 0.05;

#[derive(Clone, Copy, Debug)]
struct Aabb {
    xmin: f64,
    xmax: f64,
    ymin: f64,
    ymax: f64,
}

impl Aabb {
    fn union(self, other: Aabb) -> Aabb {
        Aabb {
            xmin: self.xmin.min(other.xmin),
            xmax: self.xmax.max(other.xmax),
            ymin: self.ymin.min(other.ymin),
            ymax: self.ymax.max(other.ymax),
        }
    }

    fn inflate(self, eps: f64) -> Aabb {
        Aabb {
            xmin: self.xmin - eps,
            xmax: self.xmax + eps,
            ymin: self.ymin - eps,
            ymax: self.ymax + eps,
        }
    }

    fn dist_lo(self, other: Aabb) -> f64 {
        let dx = if self.xmax < other.xmin {
            other.xmin - self.xmax
        } else if other.xmax < self.xmin {
            self.xmin - other.xmax
        } else {
            0.0
        };
        let dy = if self.ymax < other.ymin {
            other.ymin - self.ymax
        } else if other.ymax < self.ymin {
            self.ymin - other.ymax
        } else {
            0.0
        };
        hypot(dx, dy)
    }

    fn dist_hi(self, other: Aabb) -> f64 {
        let xs = [self.xmin, self.xmax];
        let ys = [self.ymin, self.ymax];
        let ox = [other.xmin, other.xmax];
        let oy = [other.ymin, other.ymax];
        let mut m = 0.0_f64;
        for &x in &xs {
            for &y in &ys {
                for &u in &ox {
                    for &w in &oy {
                        m = m.max(hypot(x - u, y - w));
                    }
                }
            }
        }
        m
    }
}

fn hypot(x: f64, y: f64) -> f64 {
    (x * x + y * y).sqrt()
}

fn quad_range(x0: f64, v0: f64, a: f64, h0: f64, h1: f64) -> (f64, f64) {
    let x = |h: f64| x0 + v0 * h + 0.5 * a * h * h;
    let mut lo = x(h0).min(x(h1));
    let mut hi = x(h0).max(x(h1));
    if a.abs() > 1e-18 {
        let vertex = -v0 / a;
        if vertex > h0 && vertex < h1 {
            let xv = x(vertex);
            lo = lo.min(xv);
            hi = hi.max(xv);
        }
    }
    (lo, hi)
}

fn speed_hi(v0: [f64; 2], a: [f64; 2], h0: f64, h1: f64) -> f64 {
    let vx = quad_range(v0[0], a[0], 0.0, h0, h1);
    let vy = quad_range(v0[1], a[1], 0.0, h0, h1);
    let candidates = [
        hypot(vx.0, vy.0),
        hypot(vx.0, vy.1),
        hypot(vx.1, vy.0),
        hypot(vx.1, vy.1),
    ];
    candidates.into_iter().fold(0.0_f64, f64::max)
}

fn arith_len(fun: &IntervalFunction) -> f64 {
    let h = (fun.t1 - fun.t0).abs();
    let scale = 1.0
        + fun.x0[0].abs()
        + fun.x0[1].abs()
        + (fun.v0[0].abs() + fun.v0[1].abs()) * h
        + 0.5 * (fun.a[0].abs() + fun.a[1].abs()) * h * h;
    32.0 * f64::EPSILON * scale
}

fn function_box(fun: &IntervalFunction, t0: f64, t1: f64) -> Option<Aabb> {
    let lo = t0.max(fun.t0);
    let hi = t1.min(fun.t1);
    if hi + 1e-15 < lo {
        return None;
    }
    let h0 = lo - fun.t0;
    let h1 = hi - fun.t0;
    let (xmin, xmax) = quad_range(fun.x0[0], fun.v0[0], fun.a[0], h0, h1);
    let (ymin, ymax) = quad_range(fun.x0[1], fun.v0[1], fun.a[1], h0, h1);
    Some(
        Aabb {
            xmin,
            xmax,
            ymin,
            ymax,
        }
        .inflate(arith_len(fun)),
    )
}

fn body_ids(functions: &[IntervalFunction]) -> Vec<u64> {
    let mut ids: Vec<u64> = functions.iter().map(|f| f.body_id).collect();
    ids.sort_unstable();
    ids.dedup();
    ids
}

fn functions_for<'a>(functions: &'a [IntervalFunction], id: u64) -> Vec<&'a IntervalFunction> {
    functions.iter().filter(|f| f.body_id == id).collect()
}

fn covers_interval(funs: &[&IntervalFunction], t0: f64, t1: f64) -> bool {
    if t1 + 1e-15 < t0 {
        return true;
    }
    let mut spans: Vec<(f64, f64)> = funs
        .iter()
        .filter_map(|f| {
            let lo = f.t0.max(t0);
            let hi = f.t1.min(t1);
            if hi + 1e-15 >= lo {
                Some((f.t0, f.t1))
            } else {
                None
            }
        })
        .collect();
    if spans.is_empty() {
        return false;
    }
    spans.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap());
    let mut cur = t0;
    for (a, b) in spans {
        if a > cur + 1e-12 {
            return false;
        }
        cur = cur.max(b);
        if cur + 1e-12 >= t1 {
            return true;
        }
    }
    cur + 1e-12 >= t1
}

fn union_box(funs: &[&IntervalFunction], t0: f64, t1: f64) -> Option<Aabb> {
    let mut acc: Option<Aabb> = None;
    for fun in funs {
        if let Some(b) = function_box(fun, t0, t1) {
            acc = Some(match acc {
                Some(prev) => prev.union(b),
                None => b,
            });
        }
    }
    acc
}

fn beta_hi(funs: &[&IntervalFunction], t0: f64, t1: f64) -> f64 {
    let mut v = 0.0_f64;
    for fun in funs {
        let lo = t0.max(fun.t0);
        let hi = t1.min(fun.t1);
        if hi + 1e-15 < lo {
            continue;
        }
        v = v.max(speed_hi(fun.v0, fun.a, lo - fun.t0, hi - fun.t0));
    }
    v / C
}

fn source_t0(funs: &[&IntervalFunction]) -> f64 {
    funs.iter()
        .map(|f| f.t0)
        .fold(f64::INFINITY, f64::min)
}

#[derive(Clone, Debug)]
pub struct DelayBlock {
    pub observer_id: u64,
    pub source_id: u64,
    pub t0: f64,
    pub t1: f64,
    pub u_lo: f64,
    pub u_hi: f64,
    pub r_lo: f64,
    pub r_hi: f64,
    pub beta_hi: f64,
    pub lipschitz: f64,
    pub field_bound: f64,
    pub unique: bool,
    pub covered: bool,
    pub why: Option<String>,
}

#[derive(Clone, Debug)]
pub struct GemFieldAuthority {
    pub law_id: String,
    pub coverage: &'static str,
    pub units_delay: &'static str,
    pub units_field: &'static str,
    pub units_lipschitz: &'static str,
    pub units_arith: &'static str,
    pub genesis_t: f64,
    pub horizon: f64,
    pub admitted_t0: f64,
    pub admitted_t1: f64,
    pub prefix_gap: Option<String>,
    pub interior_gap: Option<String>,
    pub alternatives: Vec<String>,
    pub max_u_hi: f64,
    pub min_r_lo: f64,
    pub max_lipschitz: f64,
    pub max_field_bound: f64,
    pub max_beta: f64,
    pub arithmetic_ulp: f64,
    pub blocks_total: u64,
    pub blocks_covered: u64,
    pub interval_wide_field: bool,
    pub authorizes_events: bool,
    pub charge: Charge,
}

fn enclose_pair_delay(
    obs: &IntervalFunction,
    t0: f64,
    t1: f64,
    srcs: &[&IntervalFunction],
    src_mu: f64,
    charge: &mut Charge,
) -> DelayBlock {
    charge.retarded_solves += 1;
    let mut why = None;
    let mut covered = false;
    let mut unique = false;
    let obs_box = match function_box(obs, t0, t1) {
        Some(b) => b,
        None => {
            return DelayBlock {
                observer_id: obs.body_id,
                source_id: srcs.first().map(|s| s.body_id).unwrap_or(0),
                t0,
                t1,
                u_lo: 0.0,
                u_hi: 0.0,
                r_lo: 0.0,
                r_hi: 0.0,
                beta_hi: 0.0,
                lipschitz: 0.0,
                field_bound: 0.0,
                unique: false,
                covered: false,
                why: Some("observer block empty on admitted slice".into()),
            };
        }
    };
    let src_origin = source_t0(srcs);
    let contemp = union_box(srcs, t0, t1);
    let r_hi0 = contemp.map(|b| obs_box.dist_hi(b)).unwrap_or(0.0);
    let beta0 = beta_hi(srcs, t0, t1).min(0.999);
    let mut u_lo = 0.0_f64;
    let mut u_hi = if beta0 < 1.0 {
        r_hi0 / (C * (1.0 - beta0)).max(1e-12)
    } else {
        (t1 - src_origin).abs() + 1.0
    };
    u_hi = u_hi.max(arith_len(obs) / C).min((t1 - src_origin).abs() + 8.0);

    let mut r_lo = 0.0;
    let mut r_hi = r_hi0;
    let mut beta = beta0;
    for _ in 0..8 {
        charge.coefficient_construction += 1;
        let look_lo = t0 - u_hi;
        let look_hi = t1 - u_lo;
        if look_lo + 1e-12 < src_origin {
            why = Some(format!(
                "lookback [{look_lo}, {look_hi}] starts before source genesis {src_origin}; incoming field missing"
            ));
            break;
        }
        if !covers_interval(srcs, look_lo, look_hi) {
            why = Some(format!(
                "source worldtube does not cover lookback [{look_lo}, {look_hi}]"
            ));
            break;
        }
        let src_box = match union_box(srcs, look_lo, look_hi) {
            Some(b) => b,
            None => {
                why = Some("source box empty on lookback".into());
                break;
            }
        };
        r_lo = obs_box.dist_lo(src_box);
        r_hi = obs_box.dist_hi(src_box);
        beta = beta_hi(srcs, look_lo, look_hi);
        if beta >= 1.0 {
            why = Some(format!("β={beta} ≥ 1; delay uniqueness fails"));
            break;
        }
        let new_lo = (r_lo / (C * (1.0 + beta)) - arith_len(obs) / C).max(0.0);
        let new_hi = r_hi / (C * (1.0 - beta).max(1e-12)) + arith_len(obs) / C;
        if new_hi <= u_hi + 1e-12 && new_lo + 1e-12 >= u_lo {
            u_lo = new_lo;
            u_hi = new_hi;
            break;
        }
        u_lo = new_lo.min(u_lo);
        u_hi = new_hi.max(u_hi);
    }
    // Uniqueness is g'(u) ≤ C(β−1) < 0, not nested iteration. Existence
    // needs the source worldtube to cover the enclosed lookback and r_lo>0.
    if why.is_none() {
        let look_lo = t0 - u_hi;
        let look_hi = t1 - u_lo;
        if look_lo + 1e-12 < src_origin || !covers_interval(srcs, look_lo, look_hi) {
            why = Some(format!(
                "lookback [{look_lo}, {look_hi}] not covered after delay enclosure"
            ));
        } else if beta >= 1.0 {
            why = Some(format!("β={beta} ≥ 1; delay uniqueness fails"));
        } else if r_lo <= 0.0 {
            why = Some("AABB overlap; r_lo=0 cannot bound GEM-a or unique delay".into());
        } else if u_hi + 1e-12 < u_lo {
            why = Some("delay enclosure inverted".into());
        } else {
            unique = true;
            covered = true;
        }
    }
    let lip = if r_lo > 0.0 {
        2.0 * G * src_mu / (r_lo * r_lo * r_lo) * (1.0 + 4.0 * beta)
    } else {
        f64::INFINITY
    };
    let field = if r_lo > 0.0 {
        G * src_mu / (r_lo * r_lo) * (1.0 + 4.0 * beta)
    } else {
        f64::INFINITY
    };
    DelayBlock {
        observer_id: obs.body_id,
        source_id: srcs.first().map(|s| s.body_id).unwrap_or(0),
        t0,
        t1,
        u_lo,
        u_hi,
        r_lo,
        r_hi,
        beta_hi: beta,
        lipschitz: lip,
        field_bound: field,
        unique,
        covered,
        why,
    }
}

/// Interval-wide GEM field bound on compiled causal blocks.
///
/// Covers the admitted interior after light-travel from genesis. Queries on
/// `[genesis, admitted_t0)` are a prefix gap (two alternatives recorded), not
/// guessed roots. `authorizes_events` is true only when every interior block
/// has a unique enclosed delay, finite tidal L, and reported arithmetic error.
pub fn enclose_gem_field_interval(
    compiled: &SourceResponse,
) -> Result<GemFieldAuthority, ResponseError> {
    let mut charge = Charge {
        init: 1,
        ..Charge::default()
    };
    let functions = &compiled.interval_functions;
    if functions.is_empty() {
        return Err(ResponseError::UnsupportedDomain {
            why: "no interval functions; cannot enclose GEM field".into(),
        });
    }
    let ids = body_ids(functions);
    if ids.len() < 2 {
        return Err(ResponseError::UnsupportedDomain {
            why: "need at least two bodies for retarded GEM field".into(),
        });
    }
    let genesis_t = compiled.genesis.genesis_t;
    let horizon = compiled.domain.horizon;
    // Contemporaneous estimate of light-travel so the admitted interior is
    // named before per-block contraction.
    let mut u_est = 0.0_f64;
    let mut beta_est = 0.0_f64;
    for &obs_id in &ids {
        let obs_funs = functions_for(functions, obs_id);
        for &src_id in &ids {
            if src_id == obs_id {
                continue;
            }
            let srcs = functions_for(functions, src_id);
            if let (Some(ob), Some(sb)) = (
                union_box(&obs_funs, genesis_t, horizon),
                union_box(&srcs, genesis_t, horizon),
            ) {
                beta_est = beta_est.max(beta_hi(&srcs, genesis_t, horizon));
                let r_hi = ob.dist_hi(sb);
                if beta_est < 1.0 {
                    u_est = u_est.max(r_hi / (C * (1.0 - beta_est).max(1e-12)));
                }
            }
        }
    }
    let admitted_t0 = genesis_t + u_est;
    let admitted_t1 = horizon;
    let mut blocks = Vec::new();
    for obs in functions {
        let slice_lo = obs.t0.max(admitted_t0);
        let slice_hi = obs.t1.min(admitted_t1);
        if slice_hi + 1e-15 < slice_lo {
            continue;
        }
        for &src_id in &ids {
            if src_id == obs.body_id {
                continue;
            }
            let srcs = functions_for(functions, src_id);
            let mu = srcs.last().map(|s| s.mu).unwrap_or(0.0);
            blocks.push(enclose_pair_delay(
                obs, slice_lo, slice_hi, &srcs, mu, &mut charge,
            ));
        }
    }
    charge.verification += 1;
    charge.validation += 1;

    let blocks_total = blocks.len() as u64;
    let blocks_covered = blocks.iter().filter(|b| b.covered).count() as u64;
    let max_u_hi = blocks.iter().map(|b| b.u_hi).fold(0.0_f64, f64::max);
    let min_r_lo = blocks
        .iter()
        .filter(|b| b.covered)
        .map(|b| b.r_lo)
        .fold(f64::INFINITY, f64::min);
    let max_lipschitz = blocks
        .iter()
        .filter(|b| b.covered)
        .map(|b| b.lipschitz)
        .fold(0.0_f64, f64::max);
    let max_field_bound = blocks
        .iter()
        .filter(|b| b.covered)
        .map(|b| b.field_bound)
        .fold(0.0_f64, f64::max);
    let max_beta = blocks.iter().map(|b| b.beta_hi).fold(0.0_f64, f64::max);
    let arithmetic_ulp = 32.0 * f64::EPSILON * (1.0 + max_u_hi * C);

    let prefix_gap = if admitted_t0 > genesis_t + 1e-12 {
        Some(format!(
            "queries on [{genesis_t}, {admitted_t0}) lack unique retarded roots: source worldtube does not exist before genesis (light-travel estimate {u_est})"
        ))
    } else {
        None
    };
    let interior_fail = blocks.iter().find(|b| !b.covered);
    let interior_gap = interior_fail.map(|b| {
        b.why.clone().unwrap_or_else(|| {
            format!(
                "observer {} source {} on [{}, {}] not covered",
                b.observer_id, b.source_id, b.t0, b.t1
            )
        })
    });
    let interval_wide_field = interior_gap.is_none()
        && blocks_total > 0
        && blocks_covered == blocks_total
        && admitted_t0 < admitted_t1
        && min_r_lo.is_finite()
        && min_r_lo > 0.0
        && max_beta < 1.0
        && max_lipschitz.is_finite();
    let authorizes_events = interval_wide_field;
    let alternatives = if interval_wide_field {
        Vec::new()
    } else {
        vec![
            "Lipschitz/tidal-L per causal block with prescribed incoming retarded field on the genesis prefix (extend prehistory by ≥ u_hi)".into(),
            "Interval/KA enclosure of the retarded-delay polynomial on stored-a blocks after a longer incoming-field initializer, or a restricted exterior-match model that does not query before the first complete lookback".into(),
        ]
    };

    charge.children.push(ChargedOp {
        name: "delay_enclosure".into(),
        role: ChargeRole::Certificate,
        charge: Box::new(Charge {
            retarded_solves: charge.retarded_solves,
            coefficient_construction: charge.coefficient_construction,
            ..Charge::default()
        }),
    });

    Ok(GemFieldAuthority {
        law_id: compiled.law_id.clone(),
        coverage: GEM_FIELD_INTERVAL_COVERAGE,
        units_delay: "lab-time",
        units_field: "length/time^2",
        units_lipschitz: "1/time^2",
        units_arith: "length",
        genesis_t,
        horizon,
        admitted_t0,
        admitted_t1,
        prefix_gap,
        interior_gap,
        alternatives,
        max_u_hi,
        min_r_lo: if min_r_lo.is_finite() { min_r_lo } else { 0.0 },
        max_lipschitz,
        max_field_bound,
        max_beta,
        arithmetic_ulp,
        blocks_total,
        blocks_covered,
        interval_wide_field,
        authorizes_events,
        charge,
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::i4_solar::{compile_solar_with_prehistory, I4_POS_BAND};

    #[test]
    fn i4_gates_authority_declared_before_results() {
        assert_eq!(I4_AUTHORITY_POS_BAND, 0.05);
        assert_eq!(I4_AUTHORITY_POS_BAND, I4_POS_BAND);
        assert_eq!(
            GEM_FIELD_INTERVAL_COVERAGE,
            "causal-block-lipschitz-ka-delay-admitted-interior"
        );
    }

    #[test]
    fn i4_gem_field_interval_covers_admitted_interior_or_names_the_gap() {
        let compiled = compile_solar_with_prehistory().expect("solar compile");
        let report = enclose_gem_field_interval(&compiled).expect("authority");
        eprintln!(
            "I4_GEM_AUTH admitted=[{}, {}] genesis={} horizon={} covered={}/{} u_hi={} r_lo={} L={} a_bound={} beta={} ulp={} interval_wide={} authorizes={} prefix={:?} interior={:?} coverage={} units_delay={} units_field={} arith_unit={}",
            report.admitted_t0,
            report.admitted_t1,
            report.genesis_t,
            report.horizon,
            report.blocks_covered,
            report.blocks_total,
            report.max_u_hi,
            report.min_r_lo,
            report.max_lipschitz,
            report.max_field_bound,
            report.max_beta,
            report.arithmetic_ulp,
            report.interval_wide_field,
            report.authorizes_events,
            report.prefix_gap,
            report.interior_gap,
            report.coverage,
            report.units_delay,
            report.units_field,
            report.units_arith
        );
        assert_eq!(report.coverage, GEM_FIELD_INTERVAL_COVERAGE);
        assert!(report.prefix_gap.is_some(), "genesis prefix must stay an exact gap");
        assert!(report.admitted_t0 > report.genesis_t);
        assert_eq!(
            report.authorizes_events, report.interval_wide_field,
            "events only if the admitted interior is actually covered"
        );
        if !report.interval_wide_field {
            assert_eq!(report.alternatives.len(), 2);
            eprintln!(
                "I4_GEM_AUTH_GAP interior={:?}; alternatives={:?}",
                report.interior_gap, report.alternatives
            );
        } else {
            assert!(report.min_r_lo > 0.0);
            assert!(report.max_beta < 1.0);
            assert!(report.max_lipschitz.is_finite());
            assert!(report.blocks_covered == report.blocks_total);
            assert!(report.alternatives.is_empty());
        }
        assert_ne!(
            crate::coupled_source_response::COUPLED_RESPONSE_LAW_ID,
            "production"
        );
    }
}
