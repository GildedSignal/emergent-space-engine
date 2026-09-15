//! GEM-to-absorbing-horizon family for *moving* sources.
//!
//! New model version: `es-gem-absorbing-horizon-v0`.
//! Physical approximation (declared before results): linearized retarded GEM
//! while `|Φ|/c² ≤ HORIZON_GEM_PHI_C2`, absorbing halt with μ transfer at
//! `r ≤ r_s = 2Gμ/c²`. Not a static Schwarzschild anchor. Not 1PN-at-interface.
//! Remainder: compiled collocation vs independent slow Euler on the same
//! moving pair, predeclared `HORIZON_POS_BAND=0.05` (not widened). Compact
//! cover requires that remainder **and** compactness at `r_s` inside the GEM
//! band. Capture accounting is a halt map, not a compact-field GR model.
//! Not `production_law`. Does not mint `CANONICAL_GRAVITY_ACCEPTANCE`.

use crate::coupled_source_response::{
    compile_source_response_opts, Body, BodyInit, Charge, CompileOpts, InitialCondition,
    Reference, ResponseError, C, G,
};
use crate::i4_near_mass::{schwarzschild_radii, I4_IF_COMPACTNESS, I4_IF_MATCH_BAND};

pub const GEM_ABSORBING_HORIZON_LAW_ID: &str = "es-gem-absorbing-horizon-v0";
/// Same laboratory band as I4. Not widened after 0.478 or 0.10.
pub const HORIZON_POS_BAND: f64 = I4_IF_MATCH_BAND;
/// Linearized GEM `|Φ|/c²` gate. Same number as the named interface compactness.
pub const HORIZON_GEM_PHI_C2: f64 = I4_IF_COMPACTNESS;
const DT: f64 = 1.0 / 32.0;
const WEAK_H: f64 = 0.5;
const COMPACT_H: f64 = 0.25;

#[derive(Clone, Debug)]
pub struct MovingHorizonReport {
    pub law_id: &'static str,
    pub seed: u64,
    pub n_moving_massive: usize,
    pub mu_host: f64,
    pub mu_in: f64,
    pub r_s: f64,
    pub r_if: f64,
    pub compactness_at_rs: f64,
    pub compactness_at_if: f64,
    pub start_r: f64,
    pub start_compactness: f64,
    pub weak_remainder: Option<f64>,
    pub compact_compile: String,
    pub captured_mu: f64,
    pub remnant_mu: f64,
    pub captured_in_gem_domain: bool,
    pub covers_compact: bool,
    pub shopping_stopped: bool,
    pub gap: &'static str,
    pub charge: Charge,
}

/// Compactness `|Φ_N|/c² = Gμ/(r c²)` at the absorbing radius. Algebraic:
/// `r_s = 2Gμ/c²` ⇒ compactness `1/2`.
pub fn compactness_at_horizon(mu: f64) -> f64 {
    let (r_s, _, _) = schwarzschild_radii(mu);
    G * mu / (r_s * C * C)
}

pub fn moving_horizon_ic(seed: u64, start_r: f64) -> InitialCondition {
    let ang = ((seed % 7) as f64) * std::f64::consts::TAU / 7.0;
    let (ca, sa) = (ang.cos(), ang.sin());
    let mu_host = 8.0;
    let mu_in = 0.5;
    // Both sources move. Host has a small lab velocity; infaller heads inward.
    InitialCondition {
        genesis_t: 0.0,
        bodies: vec![
            BodyInit {
                id: 0,
                mu: mu_host,
                x: [0.0, 0.0],
                v: [0.02 * ca, 0.02 * sa],
            },
            BodyInit {
                id: 1,
                mu: mu_in,
                x: [start_r * ca, start_r * sa],
                v: [-0.08 * ca, -0.08 * sa],
            },
        ],
    }
}

fn body_xy(body: &Body, t: f64) -> Option<[f64; 2]> {
    let seg = body.segments.iter().rev().find(|s| {
        t + 1e-15 >= s.t0 && s.t1.map(|t1| t <= t1 + 1e-15).unwrap_or(true)
    })?;
    let dt = t - seg.t0;
    Some([
        seg.x0[0] + seg.v[0] * dt + 0.5 * seg.a[0] * dt * dt,
        seg.x0[1] + seg.v[1] * dt + 0.5 * seg.a[1] * dt * dt,
    ])
}

fn pair_remainder(
    compiled: &[Body],
    slow: &[Body],
    t: f64,
    r0: f64,
) -> Option<f64> {
    let mut max_rel = 0.0_f64;
    for id in [0_u64, 1] {
        let a = compiled.iter().find(|b| b.id == id).and_then(|b| body_xy(b, t))?;
        let b = slow.iter().find(|b| b.id == id).and_then(|b| body_xy(b, t))?;
        let dx = (a[0] - b[0]).hypot(a[1] - b[1]);
        max_rel = max_rel.max(dx / r0.max(1e-12));
    }
    Some(max_rel)
}

fn n_moving_massive(ic: &InitialCondition) -> usize {
    ic.bodies
        .iter()
        .filter(|b| b.mu > 0.0 && (b.v[0].hypot(b.v[1]) > 0.0))
        .count()
}

fn compactness(mu: f64, r: f64) -> f64 {
    G * mu / (r.max(1e-18) * C * C)
}

/// One attempt: moving GEM pair + absorbing halt. Compact cover is a
/// conjunction of remainder band and compactness-at-`r_s` inside GEM `|Φ|/c²`.
pub fn measure_moving_horizon() -> Result<MovingHorizonReport, ResponseError> {
    measure_moving_horizon_seed(0)
}

pub fn measure_moving_horizon_seed(seed: u64) -> Result<MovingHorizonReport, ResponseError> {
    let mut charge = Charge {
        init: 1,
        ..Charge::default()
    };
    let weak_r = 6.0;
    let compact_r = 2.7;
    let weak_ic = moving_horizon_ic(seed, weak_r);
    let compact_ic = moving_horizon_ic(seed, compact_r);
    let mu_host = weak_ic.bodies[0].mu;
    let mu_in = weak_ic.bodies[1].mu;
    let (r_s, _, r_if) = schwarzschild_radii(mu_host);
    let compactness_at_rs = compactness_at_horizon(mu_host);
    let compactness_at_if = compactness(mu_host, r_if);
    let start_compactness = compactness(mu_host, compact_r);
    let n_moving = n_moving_massive(&weak_ic);

    let no_inverse = CompileOpts {
        store_pair_inverse: false,
    };
    let weak_remainder = match (
        compile_source_response_opts(weak_ic.clone(), vec![], WEAK_H, DT, CompileOpts {
            store_pair_inverse: false,
        }),
        Reference::from_genesis(weak_ic.clone(), vec![], DT).evolve_to(WEAK_H),
    ) {
        (Ok(compiled), Ok((slow, _))) => {
            charge.consumers += 1;
            charge.verification += 1;
            pair_remainder(&compiled.worldtubes, &slow, WEAK_H, weak_r)
        }
        (Err(e), _) => {
            charge.fallback += 1;
            eprintln!("I4_MOVING_HORIZON weak compile refused: {e}");
            None
        }
        (_, Err(e)) => {
            charge.fallback += 1;
            eprintln!("I4_MOVING_HORIZON weak Euler refused: {e}");
            None
        }
    };

    let compact_compile = match compile_source_response_opts(
        compact_ic,
        vec![],
        COMPACT_H,
        DT,
        no_inverse,
    ) {
        Ok(compiled) => {
            charge.consumers += 1;
            format!(
                "compiled H={COMPACT_H} max_phi_c2={:.6}",
                compiled.residual.max_phi_c2
            )
        }
        Err(e) => {
            charge.fallback += 1;
            format!("refused before r_s: {e}")
        }
    };

    // Halt-map capture accounting: independent of GEM evolution through r_s.
    let captured_mu = mu_in;
    let remnant_mu = mu_host + captured_mu;
    charge.history += 1;
    let captured_in_gem_domain = compactness_at_rs <= HORIZON_GEM_PHI_C2;
    let remainder_ok = weak_remainder
        .map(|r| r <= HORIZON_POS_BAND)
        .unwrap_or(false);
    let covers_compact = remainder_ok
        && captured_in_gem_domain
        && n_moving >= 2
        && compactness_at_rs <= HORIZON_POS_BAND;
    let shopping_stopped = !covers_compact;
    let gap = "exact gap: compactness at r_s is 0.5 > linearized GEM |Phi|/c^2 band 0.05; the interval r_s < r <= r_if has no GEM field and this family has no other field. Halt μ-transfer is capture accounting, not a compact moving multi-mass field. Alternatives already tried: (a) 1PN GEM at a stationary Schwarzschild interface, (b) this GEM-to-absorbing-horizon family. Shopping stopped.";

    Ok(MovingHorizonReport {
        law_id: GEM_ABSORBING_HORIZON_LAW_ID,
        seed,
        n_moving_massive: n_moving,
        mu_host,
        mu_in,
        r_s,
        r_if,
        compactness_at_rs,
        compactness_at_if,
        start_r: compact_r,
        start_compactness,
        weak_remainder,
        compact_compile,
        captured_mu,
        remnant_mu,
        captured_in_gem_domain,
        covers_compact,
        shopping_stopped,
        gap,
        charge,
    })
}

impl MovingHorizonReport {
    pub fn gate_evidence(&self) -> String {
        let rem = match self.weak_remainder {
            Some(r) => format!("{r:.3e}"),
            None => "none".into(),
        };
        format!(
            "{} seed={} moving={} weak_remainder={} vs band {}; compactness_at_rs={:.3} (r_s={:.4}, r_if={:.4}); captured_in_gem={}; μ {}->{} ; {}; shopping_stopped={}",
            self.law_id,
            self.seed,
            self.n_moving_massive,
            rem,
            HORIZON_POS_BAND,
            self.compactness_at_rs,
            self.r_s,
            self.r_if,
            self.captured_in_gem_domain,
            self.captured_mu,
            self.remnant_mu,
            self.gap,
            self.shopping_stopped
        )
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn i4_moving_horizon_gates_declared_before_results() {
        assert_eq!(HORIZON_POS_BAND, 0.05);
        assert_eq!(HORIZON_GEM_PHI_C2, 0.05);
        assert_eq!(HORIZON_POS_BAND, crate::i4_solar::I4_POS_BAND);
        assert_eq!(GEM_ABSORBING_HORIZON_LAW_ID, "es-gem-absorbing-horizon-v0");
        let mu = 8.0;
        let c_rs = compactness_at_horizon(mu);
        assert!((c_rs - 0.5).abs() < 1e-12, "horizon compactness is 1/2, got {c_rs}");
        assert!(c_rs > HORIZON_GEM_PHI_C2);
    }

    #[test]
    fn i4_moving_horizon_cannot_cover_compact_fields() {
        let report = measure_moving_horizon().expect("horizon");
        eprintln!(
            "I4_MOVING_HORIZON law={} seed={} moving={} rem={:?} c_rs={} c_if={} start_c={} r_s={} r_if={} compile={} capture {}->{} in_gem={} covers={} stopped={}",
            report.law_id,
            report.seed,
            report.n_moving_massive,
            report.weak_remainder,
            report.compactness_at_rs,
            report.compactness_at_if,
            report.start_compactness,
            report.r_s,
            report.r_if,
            report.compact_compile,
            report.captured_mu,
            report.remnant_mu,
            report.captured_in_gem_domain,
            report.covers_compact,
            report.shopping_stopped
        );
        assert_eq!(report.law_id, GEM_ABSORBING_HORIZON_LAW_ID);
        assert!(report.n_moving_massive >= 2);
        assert!((report.remnant_mu - report.mu_host - report.captured_mu).abs() < 1e-12);
        assert!(report.compactness_at_rs > HORIZON_POS_BAND);
        assert!(!report.captured_in_gem_domain);
        assert!(!report.covers_compact);
        assert!(report.shopping_stopped);
        assert!(report.gap.contains("Shopping stopped"));
        if let Some(rem) = report.weak_remainder {
            assert!(
                rem.is_finite() && rem >= 0.0,
                "remainder is a band, not leftover==0; got {rem}"
            );
        }
        // Many-seed capable: compactness at r_s is algebraic, not a single-seed pin.
        for seed in [1_u64, 2, 5] {
            let ic = moving_horizon_ic(seed, 2.7);
            assert!(ic.bodies.iter().filter(|b| b.mu > 0.0 && b.v[0].hypot(b.v[1]) > 0.0).count() >= 2);
            assert!((compactness_at_horizon(ic.bodies[0].mu) - 0.5).abs() < 1e-12);
        }
    }
}
