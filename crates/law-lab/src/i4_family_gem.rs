//! Family-sourced GEM: moments vs extract-and-collocate.
//!
//! Physical approximation (declared before results): an affine family of
//! equal-μ members is either (a) one COM/moment GEM source plus a retained
//! identity table, or (b) every member extracted into collocation. Direct
//! small-world sums remain the galaxy method; this is whether family mass
//! contributes. Remainder vs extract, predeclared `I4_FAMILY_POS_BAND=0.05`.
//! Do not drop mass, identities, or member history. Nested Charge vs
//! extracting every member. Not `production_law`. Not canonical gravity.

use crate::coupled_source_response::{
    body_state, compile_source_response_opts, field_acceleration, laboratory_two_body, BodyInit,
    Charge, CompileOpts, InitialCondition, ResponseError,
};
use crate::i4_solar::I4_HORIZON;

/// Same laboratory band as I3/I4; not widened after 0.216.
pub const I4_FAMILY_POS_BAND: f64 = 0.05;
pub const FAMILY_N: usize = 4;
pub const FAMILY_MU: f64 = 0.01;
pub const FAMILY_FIRST_ID: u64 = 10_000;

#[derive(Clone, Debug)]
pub struct FamilyIdentities {
    pub first_id: u64,
    pub count: u64,
    pub ids: Vec<u64>,
    pub mu_each: f64,
    pub mu_total: f64,
}

#[derive(Clone, Debug)]
pub struct FamilyGemReport {
    pub n_members: usize,
    pub mu_extract: f64,
    pub mu_moment: f64,
    pub remainder: f64,
    pub remainder_bound: f64,
    pub extract_ledger: u64,
    pub moment_ledger: u64,
    pub identities_retained: bool,
    pub matched: bool,
    pub admitted: &'static str,
    pub extract_charge: Charge,
    pub moment_charge: Charge,
}

fn hypot(x: f64, y: f64) -> f64 {
    (x * x + y * y).sqrt()
}

pub fn affine_family_members() -> (Vec<BodyInit>, FamilyIdentities) {
    let mut bodies = Vec::new();
    let mut ids = Vec::new();
    let stride = 0.4;
    for k in 0..FAMILY_N {
        let id = FAMILY_FIRST_ID + k as u64;
        ids.push(id);
        let x = -0.6 + k as f64 * stride;
        bodies.push(BodyInit {
            id,
            mu: FAMILY_MU,
            x: [x, 18.0],
            v: [0.0, 0.0],
        });
    }
    let identities = FamilyIdentities {
        first_id: FAMILY_FIRST_ID,
        count: FAMILY_N as u64,
        ids,
        mu_each: FAMILY_MU,
        mu_total: FAMILY_MU * FAMILY_N as f64,
    };
    (bodies, identities)
}

pub fn family_moment_source(members: &[BodyInit]) -> BodyInit {
    let mut mu = 0.0;
    let mut x = [0.0, 0.0];
    let mut v = [0.0, 0.0];
    for b in members {
        mu += b.mu;
        x[0] += b.mu * b.x[0];
        x[1] += b.mu * b.x[1];
        v[0] += b.mu * b.v[0];
        v[1] += b.mu * b.v[1];
    }
    if mu > 0.0 {
        x[0] /= mu;
        x[1] /= mu;
        v[0] /= mu;
        v[1] /= mu;
    }
    BodyInit {
        id: FAMILY_FIRST_ID,
        mu,
        x,
        v,
    }
}

fn with_family(mut ic: InitialCondition, extra: Vec<BodyInit>) -> InitialCondition {
    ic.bodies.extend(extra);
    ic
}

fn octupole_like_bound(members: &[BodyInit], x_obs: [f64; 2]) -> f64 {
    let com = family_moment_source(members);
    let mut ell = 0.0_f64;
    for b in members {
        ell = ell.max(hypot(b.x[0] - com.x[0], b.x[1] - com.x[1]));
    }
    let r = hypot(x_obs[0] - com.x[0], x_obs[1] - com.x[1]).max(1e-12);
    4.0 * com.mu * ell.powi(3) / r.powi(5)
}

pub fn measure_family_sourced_gem() -> Result<FamilyGemReport, ResponseError> {
    let solar = laboratory_two_body();
    let (members, identities) = affine_family_members();
    let extract_ic = with_family(solar.clone(), members.clone());
    let moment_ic = with_family(solar, vec![family_moment_source(&members)]);
    let opts = CompileOpts {
        store_pair_inverse: false,
    };
    let extracted = compile_source_response_opts(
        extract_ic,
        vec![],
        I4_HORIZON.min(2.0),
        1.0 / 16.0,
        opts,
    )?;
    let moment = compile_source_response_opts(
        moment_ic,
        vec![],
        I4_HORIZON.min(2.0),
        1.0 / 16.0,
        opts,
    )?;
    let t = 1.0;
    let mut charge = Charge::default();
    let (xp, _) = body_state(&extracted.worldtubes, 1, t)?;
    let a_ex = field_acceleration(&extracted.worldtubes, t, xp, [0.0, 0.0], Some(1), &mut charge)?;
    let a_mo = field_acceleration(&moment.worldtubes, t, xp, [0.0, 0.0], Some(1), &mut charge)?;
    let scale = hypot(a_ex[0], a_ex[1]).max(1e-12);
    let remainder = hypot(a_ex[0] - a_mo[0], a_ex[1] - a_mo[1]) / scale;
    let remainder_bound = octupole_like_bound(&members, xp) / scale;
    let mu_extract: f64 = members.iter().map(|b| b.mu).sum();
    let mu_moment = family_moment_source(&members).mu;
    let identities_retained = identities.ids.len() == FAMILY_N
        && identities.mu_total == mu_extract
        && extracted.genesis.bodies.iter().any(|b| b.id == FAMILY_FIRST_ID);
    let matched = remainder <= I4_FAMILY_POS_BAND && (mu_extract - mu_moment).abs() < 1e-12;
    let admitted = if matched {
        "family-moment-gem-source"
    } else {
        "extract-and-collocate"
    };
    let extract_charge = extracted.charge.clone();
    let moment_charge = moment.charge.clone();
    Ok(FamilyGemReport {
        n_members: FAMILY_N,
        mu_extract,
        mu_moment,
        remainder,
        remainder_bound,
        extract_ledger: extract_charge.ledger_total(),
        moment_ledger: moment_charge.ledger_total(),
        identities_retained,
        matched,
        admitted,
        extract_charge,
        moment_charge,
    })
}

pub fn merge_family_into_genesis(
    mut genesis: InitialCondition,
    members: Vec<BodyInit>,
    use_moment: bool,
) -> (InitialCondition, FamilyIdentities) {
    let (_, identities) = affine_family_members();
    if use_moment {
        genesis.bodies.push(family_moment_source(&members));
    } else {
        genesis.bodies.extend(members);
    }
    (genesis, identities)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::i4_solar::I4_POS_BAND;

    #[test]
    fn i4_family_band_declared_before_results() {
        assert_eq!(I4_FAMILY_POS_BAND, 0.05);
        assert_eq!(I4_FAMILY_POS_BAND, I4_POS_BAND);
    }

    #[test]
    fn i4_family_sourced_gem_keep_or_extract() {
        let report = measure_family_sourced_gem().expect("family gem");
        eprintln!(
            "I4_FAMILY_GEM n={} mu_e={} mu_m={} rem={} bound={} extract_ledger={} moment_ledger={} ids={} matched={} admitted={}",
            report.n_members,
            report.mu_extract,
            report.mu_moment,
            report.remainder,
            report.remainder_bound,
            report.extract_ledger,
            report.moment_ledger,
            report.identities_retained,
            report.matched,
            report.admitted
        );
        eprintln!(
            "I4_FAMILY_NESTED extract init={} src={} recon={} fallback={} val={} fact={} hist={} query_field={} | moment init={} src={} recon={} fallback={} val={} fact={} hist={} query_field={}",
            report.extract_charge.init,
            report.extract_charge.source_evolution,
            report.extract_charge.reconstruction,
            report.extract_charge.fallback,
            report.extract_charge.validation,
            report.extract_charge.factorization,
            report.extract_charge.history,
            report.extract_charge.field_evals,
            report.moment_charge.init,
            report.moment_charge.source_evolution,
            report.moment_charge.reconstruction,
            report.moment_charge.fallback,
            report.moment_charge.validation,
            report.moment_charge.factorization,
            report.moment_charge.history,
            report.moment_charge.field_evals,
        );
        assert!(report.identities_retained);
        assert!(report.extract_ledger > 0 && report.moment_ledger > 0);
        if report.matched {
            eprintln!("I4_KEEP family moment as GEM source; identities retained in FamilyIdentities");
        } else {
            assert_eq!(report.admitted, "extract-and-collocate");
            eprintln!(
                "I4_FAMILY_REJECT moment rem {} > {}; admitted extract-and-collocate. Mass and identities retained. Alternatives: (a) extract-and-collocate members that must gravitate, (b) higher-rank family expansion with the same identity table",
                report.remainder, I4_FAMILY_POS_BAND
            );
        }
    }
}
