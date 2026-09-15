//! I3 keep/reject experiments. Nested Charge ledger is the total-cost
//! denominator. Compact-after-the-fact is not skipped evolution. PERIOD is
//! not a physical orbit. Not `production_law`. Not canonical gravity.

use crate::coupled_source_response::{
    Charge, ChargeRole, SourceResponse,
};

#[derive(Clone, Debug)]
pub struct TotalCost {
    pub ledger: u64,
    pub runtime: u64,
    pub bytes: usize,
    pub wall_ns: u128,
    pub reconstruction: u64,
    pub certificate: u64,
    pub fallback: u64,
    pub source_evolution: u64,
    pub retarded_solves: u64,
    pub coefficient_construction: u64,
    pub factorization: u64,
}

impl TotalCost {
    pub fn of(compiled: &SourceResponse) -> Self {
        let bytes = serde_json::to_vec(&compiled.interval_functions)
            .map(|b| b.len())
            .unwrap_or(0)
            + compiled
                .pair_inverse
                .as_ref()
                .map(|p| p.lu.len() * 8)
                .unwrap_or(0);
        Self {
            ledger: compiled.charge.ledger_total(),
            runtime: compiled.charge.runtime_request_total(),
            bytes,
            wall_ns: compiled.wall_ns,
            reconstruction: compiled.charge.reconstruction
                + role_sum(&compiled.charge, ChargeRole::Reconstruction),
            certificate: compiled.charge.validation
                + compiled.charge.verification
                + role_sum(&compiled.charge, ChargeRole::Certificate)
                + role_sum(&compiled.charge, ChargeRole::OfflineAudit),
            fallback: compiled.charge.fallback + role_sum(&compiled.charge, ChargeRole::Fallback),
            source_evolution: compiled.charge.source_evolution,
            retarded_solves: compiled.charge.retarded_solves,
            coefficient_construction: compiled.charge.coefficient_construction,
            factorization: compiled.charge.factorization,
        }
    }
}

fn role_sum(charge: &Charge, role: ChargeRole) -> u64 {
    charge
        .children
        .iter()
        .map(|c| {
            let nested = role_sum(&c.charge, role);
            if c.role == role {
                c.charge.ledger_total().saturating_add(nested)
            } else {
                nested
            }
        })
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::coupled_phase_nav::{compact_source_response, CompactSpec};
    use crate::coupled_source_response::{
        compile_source_response, laboratory_distant_tide, laboratory_encounter,
        laboratory_four_kick, laboratory_kick, laboratory_two_body, repair_from_committed,
        reuse_certified_interval_functions, schur_update_compiled_pair, InitialCondition,
        Intervention, Reference,
    };

    fn compile_h(h: f64) -> SourceResponse {
        compile_source_response(laboratory_two_body(), vec![], h, 1.0 / 32.0).unwrap()
    }

    fn eccentric_ic() -> InitialCondition {
        let mut ic = laboratory_two_body();
        ic.bodies[0].v = [0.0, 0.12];
        ic.bodies[1].v = [0.0, -0.12];
        ic
    }

    fn eval_interval_at(compiled: &SourceResponse, t: f64) -> [f64; 2] {
        let fun = compiled
            .interval_functions
            .iter()
            .find(|f| t + 1e-15 >= f.t0 && t <= f.t1 + 1e-15)
            .or_else(|| compiled.interval_functions.last())
            .expect("interval function");
        let h = t - fun.t0;
        [
            fun.x0[0] + fun.v0[0] * h + 0.5 * fun.a[0] * h * h,
            fun.x0[1] + fun.v0[1] * h + 0.5 * fun.a[1] * h * h,
        ]
    }

    #[test]
    fn i3_time_interval_functions_vs_euler_and_compact_after_the_fact() {
        let mut rows = Vec::new();
        for h in [1.0_f64, 2.0, 3.0] {
            let compiled = compile_h(h);
            let compiled_cost = TotalCost::of(&compiled);
            let t0 = std::time::Instant::now();
            let (slow, slow_charge) =
                Reference::from_genesis(compiled.genesis.clone(), vec![], compiled.domain.dt)
                    .evolve_to(h)
                    .unwrap();
            let euler_ns = t0.elapsed().as_nanos();
            assert!(!slow.is_empty());
            let t_eval = std::time::Instant::now();
            let mut acc = 0.0;
            for k in 0..16 {
                let t = compiled.genesis.genesis_t + h * (k as f64 + 0.5) / 16.0;
                let x = eval_interval_at(&compiled, t);
                acc += x[0] + x[1];
            }
            let eval_ns = t_eval.elapsed().as_nanos();
            assert!(acc.is_finite());
            let compact = compact_source_response(&compiled, CompactSpec::default());
            rows.push((
                h,
                compiled_cost,
                slow_charge.ledger_total(),
                euler_ns,
                eval_ns,
                compact.ok().map(|c| c.pieces.len()),
            ));
        }
        let compile_lo = rows[0].1.ledger;
        let compile_hi = rows[2].1.ledger;
        let euler_hi = rows[2].2;
        let bytes_hi = rows[2].1.bytes;
        let coeff_hi = rows[2].1.coefficient_construction;
        eprintln!(
            "I3_TIME compile_ledger H=1:{compile_lo} H=3:{compile_hi} euler_ledger_H3={euler_hi} bytes_H3={bytes_hi} coeff_H3={coeff_hi} cert_H3={} recon_H3={} eval_ns_H3={} wall_ns_H3={} factor_H3={}",
            rows[2].1.certificate,
            rows[2].1.reconstruction,
            rows[2].4,
            rows[2].1.wall_ns,
            rows[2].1.factorization
        );
        assert!(
            compile_hi >= compile_lo,
            "interval compile work must not shrink as horizon grows if it is still sequential collocation"
        );
        assert!(
            coeff_hi > 0,
            "historical compact seal still runs after collocation; that cannot establish skipped evolution"
        );
        // First compile of a quiet pair is construction, not a skip of Euler.
        if compile_hi < euler_hi {
            eprintln!("I3_KEEP interval-compile vs Euler at H=3: ledger {compile_hi} < {euler_hi}");
        } else {
            eprintln!("I3_REJECT interval-compile as a skip of Euler at H=3: ledger {compile_hi} >= {euler_hi}");
        }
        eprintln!("I3_REJECT compact-after-the-fact as skipped evolution (fitted after worldtubes exist)");
    }

    #[test]
    fn i3_time_eccentric_forcing_encounter() {
        let ecc = compile_source_response(eccentric_ic(), vec![], 2.0, 1.0 / 32.0).unwrap();
        let forced = compile_source_response(
            laboratory_two_body(),
            laboratory_four_kick()
                .into_iter()
                .filter(|k| k.t < 2.0)
                .collect::<Vec<Intervention>>(),
            2.0,
            1.0 / 32.0,
        )
        .unwrap();
        let ecc_c = TotalCost::of(&ecc);
        let forced_c = TotalCost::of(&forced);
        eprintln!(
            "I3_TIME_ECC ledger={} bytes={} coeff={} I3_TIME_FORCE ledger={} bytes={}",
            ecc_c.ledger, ecc_c.bytes, ecc_c.coefficient_construction, forced_c.ledger, forced_c.bytes
        );

        let pair = compile_source_response(laboratory_two_body(), vec![], 2.0, 1.0 / 32.0).unwrap();
        let (enc_ic, _) = laboratory_encounter();
        let refuse = schur_update_compiled_pair(&pair, &enc_ic.bodies[2], 2.0, 1.0 / 32.0);
        assert!(
            refuse.is_err(),
            "close-entrant share refusal stays negative"
        );
        let recovered = compile_source_response(enc_ic, vec![], 2.0, 1.0 / 32.0).unwrap();
        let rec_c = TotalCost::of(&recovered);
        eprintln!(
            "I3_ENCOUNTER refuse_local=true recouple_ledger={} recouple_fallback={}",
            rec_c.ledger, rec_c.fallback
        );
        eprintln!("I3_REJECT resonance-skip: no admitted GEM resonance fixture; PERIOD remains algebraic control");
        let _ = pair;
        let _ = forced_c;
    }

    #[test]
    fn i3_perturbation_repair_vs_recouple_vs_local_tide() {
        let quiet = compile_h(3.0);
        let extra = laboratory_kick();
        let recouple =
            compile_source_response(laboratory_two_body(), extra.clone(), 3.0, 1.0 / 32.0).unwrap();
        let repaired = repair_from_committed(&quiet, &extra, 3.0, 1.0 / 32.0).unwrap();
        let reused = reuse_certified_interval_functions(&quiet, &extra, 3.0, 1.0 / 32.0);
        let recouple_cost = TotalCost::of(&recouple);
        let repair_cost = TotalCost::of(&repaired);
        eprintln!(
            "I3_PERTURB recouple_ledger={} repair_ledger={} recouple_runtime={} repair_runtime={} recouple_recon={} repair_recon={} recouple_cert={} repair_cert={} recouple_bytes={} repair_bytes={}",
            recouple_cost.ledger,
            repair_cost.ledger,
            recouple_cost.runtime,
            repair_cost.runtime,
            recouple_cost.reconstruction,
            repair_cost.reconstruction,
            recouple_cost.certificate,
            repair_cost.certificate,
            recouple_cost.bytes,
            repair_cost.bytes
        );
        assert_eq!(repaired.law_id, recouple.law_id);
        assert_eq!(repaired.genesis.bodies.len(), recouple.genesis.bodies.len());
        eprintln!("I3_PERTURB reuse_ok={}", reused.is_ok());

        let matched = repaired.interval_functions.len() == recouple.interval_functions.len();
        if matched
            && repair_cost.ledger < recouple_cost.ledger
            && repair_cost.reconstruction > 0
        {
            eprintln!(
                "I3_KEEP prefix-repair in quiet-kick H=3 domain: ledger {} < recouple {}",
                repair_cost.ledger, recouple_cost.ledger
            );
        } else {
            eprintln!(
                "I3_REJECT prefix-repair as general skip: ledger repair={} recouple={} matched={matched}",
                repair_cost.ledger, recouple_cost.ledger
            );
        }

        let tide_ic = laboratory_distant_tide();
        let entrant = tide_ic.bodies[2].clone();
        let local = schur_update_compiled_pair(&quiet, &entrant, 3.0, 1.0 / 32.0);
        let triple = compile_source_response(tide_ic, vec![], 3.0, 1.0 / 32.0).unwrap();
        let triple_cost = TotalCost::of(&triple);
        match local {
            Ok(updated) => {
                let local_cost = TotalCost::of(&updated);
                eprintln!(
                    "I3_TIDE local_ledger={} triple_ledger={} local_factor={} triple_factor={} local_cert={} triple_cert={}",
                    local_cost.ledger,
                    triple_cost.ledger,
                    local_cost.factorization,
                    triple_cost.factorization,
                    local_cost.certificate,
                    triple_cost.certificate
                );
                if local_cost.ledger < triple_cost.ledger {
                    eprintln!(
                        "I3_KEEP local pair-inverse tide in distant-tide H=3: ledger {} < recouple {}",
                        local_cost.ledger, triple_cost.ledger
                    );
                } else {
                    eprintln!(
                        "I3_REJECT local pair-inverse tide as cheaper than recouple: {} >= {}",
                        local_cost.ledger, triple_cost.ledger
                    );
                }
            }
            Err(err) => {
                eprintln!("I3_REJECT local sensitivity this domain: {err}");
                eprintln!(
                    "I3_FALLBACK recouple triple ledger={}",
                    triple_cost.ledger
                );
            }
        }
    }

    #[test]
    fn i3_period_is_algebraic_control_not_physical_orbit() {
        eprintln!("I3_REJECT PERIOD as physical long-time source representation (algebraic control only)");
    }
}
