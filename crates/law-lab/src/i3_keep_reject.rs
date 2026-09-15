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
        eprintln!("I3_REJECT resonance-skip as skipped GEM; fixture lives in i3_secular_kepler_does_not_collocate_the_skipped_interval");
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

    #[test]
    fn i3_secular_kepler_does_not_collocate_the_skipped_interval() {
        use crate::coupled_source_response::{
            compile_source_response_opts, CompileOpts,
        };
        use crate::i3_secular::{
            compile_secular_response, laboratory_circular_pair, laboratory_eccentric_pair,
            laboratory_resonant_kicks,
        };

        let mut rows = Vec::new();
        for h in [4.0_f64, 6.0] {
            let secular = compile_secular_response(laboratory_circular_pair(), vec![], h);
            let collocation = compile_source_response_opts(
                laboratory_circular_pair(),
                vec![],
                h,
                1.0 / 32.0,
                CompileOpts {
                    store_pair_inverse: false,
                },
            )
            .unwrap();
            let coll_cost = TotalCost::of(&collocation);
            match secular {
                Ok(secular) => {
                    let mut q_charge = Charge::default();
                    let t_eval = std::time::Instant::now();
                    let mut max_dx = 0.0_f64;
                    for k in 0..8 {
                        let t = h * (k as f64 + 0.5) / 8.0;
                        let xs = secular.eval(0, t, &mut q_charge).unwrap();
                        let xc = eval_interval_at(&collocation, t);
                        max_dx = max_dx.max((xs[0] - xc[0]).abs().max((xs[1] - xc[1]).abs()));
                    }
                    let eval_ns = t_eval.elapsed().as_nanos();
                    eprintln!(
                        "I3_SECULAR H={h} secular_ledger={} collocation_ledger={} secular_runtime={} collocation_runtime={} secular_bytes={} collocation_bytes={} secular_coeff={} collocation_coeff={} secular_factor={} collocation_factor={} secular_recon={} collocation_recon={} secular_cert={} collocation_cert={} remainder={} max_dx={} eval_ns={} secular_wall={} collocation_wall={} collocation_se={} collocation_ret={}",
                        secular.charge.ledger_total(),
                        coll_cost.ledger,
                        secular.charge.runtime_request_total(),
                        coll_cost.runtime,
                        secular.bytes(),
                        coll_cost.bytes,
                        secular.charge.coefficient_construction,
                        coll_cost.coefficient_construction,
                        secular.charge.factorization,
                        coll_cost.factorization,
                        secular.charge.reconstruction + q_charge.reconstruction,
                        coll_cost.reconstruction,
                        secular.charge.validation + secular.charge.verification,
                        coll_cost.certificate,
                        secular.max_remainder,
                        max_dx,
                        eval_ns,
                        secular.wall_ns,
                        coll_cost.wall_ns,
                        coll_cost.source_evolution,
                        coll_cost.retarded_solves
                    );
                    rows.push((
                        h,
                        Some(secular.charge.ledger_total()),
                        coll_cost.ledger,
                        Some(max_dx),
                        Some(secular.charge.source_evolution + secular.charge.retarded_solves),
                        coll_cost.source_evolution + coll_cost.retarded_solves,
                    ));
                }
                Err(err) => {
                    eprintln!(
                        "I3_SECULAR H={h} fallback={err} collocation_ledger={} collocation_se={} collocation_ret={} collocation_bytes={}",
                        coll_cost.ledger,
                        coll_cost.source_evolution,
                        coll_cost.retarded_solves,
                        coll_cost.bytes
                    );
                    rows.push((
                        h,
                        None,
                        coll_cost.ledger,
                        None,
                        None,
                        coll_cost.source_evolution + coll_cost.retarded_solves,
                    ));
                }
            }
        }
        let col_lo = rows[0].2;
        let col_hi = rows[1].2;
        let col_src_lo = rows[0].5;
        let col_src_hi = rows[1].5;
        assert!(
            col_hi > col_lo && col_src_hi > col_src_lo,
            "collocation must still grow with H as the baseline"
        );
        match (rows[0].1, rows[0].3, rows[1].1) {
            (Some(sec_lo), Some(dx_lo), Some(sec_hi)) => {
                let dx_hi = rows[1].3.unwrap();
                let sec_src_lo = rows[0].4.unwrap();
                let sec_src_hi = rows[1].4.unwrap();
                let matched = dx_hi < 0.25 && dx_lo < 0.25;
                let src_flat = sec_src_hi <= sec_src_lo.saturating_mul(2) + 8;
                if matched && src_flat && sec_hi < col_hi {
                    eprintln!(
                        "I3_KEEP secular Kepler+residual as evolution in circular-pair H=4..6: ledger {sec_hi} < collocation {col_hi}, source_ops {sec_src_lo}->{sec_src_hi} vs {col_src_lo}->{col_src_hi}, max_dx={dx_hi}"
                    );
                } else {
                    eprintln!(
                        "I3_REJECT secular Kepler+residual as skipped GEM: matched={matched} src_flat={src_flat} ledger {sec_lo}->{sec_hi} vs {col_lo}->{col_hi} max_dx_H4={dx_lo}"
                    );
                }
            }
            (Some(sec_lo), Some(dx_lo), None) => {
                eprintln!(
                    "I3_REJECT secular Kepler+residual as skipped GEM: H=4 ledger {sec_lo} vs collocation {col_lo} max_dx={dx_lo}; H=6 remainder refused, collocation {col_hi}. Construction skipped collocation but did not match GEM trajectories."
                );
            }
            _ => {
                eprintln!(
                    "I3_REJECT secular Kepler+residual: construction refused in the H=4..6 circular domain; collocation {col_lo}->{col_hi}"
                );
            }
        }

        let ecc = compile_secular_response(laboratory_eccentric_pair(), vec![], 6.0);
        match &ecc {
            Ok(s) => eprintln!(
                "I3_SECULAR_ECC ledger={} remainder={} e={}",
                s.charge.ledger_total(),
                s.max_remainder,
                s.elements.e
            ),
            Err(err) => eprintln!("I3_SECULAR_ECC fallback: {err}"),
        }

        let radial = compile_secular_response(laboratory_two_body(), vec![], 6.0);
        assert!(
            radial.is_err(),
            "radial rest pair is a close-encounter fallback, not a secular keep"
        );
        eprintln!("I3_ENCOUNTER_FIXTURE secular_radial_refuse={}", radial.unwrap_err());
        let recov = compile_source_response(laboratory_two_body(), vec![], 6.0, 1.0 / 32.0).unwrap();
        eprintln!(
            "I3_ENCOUNTER_FIXTURE collocation_fallback_ledger={}",
            TotalCost::of(&recov).ledger
        );

        let period = match compile_secular_response(laboratory_circular_pair(), vec![], 4.0) {
            Ok(s) => s.elements.period,
            Err(_) => 2.0,
        };
        let resonant = laboratory_resonant_kicks(period.min(2.0), 6.0);
        let res_try =
            compile_secular_response(laboratory_circular_pair(), resonant.clone(), 6.0);
        match res_try {
            Ok(s) => eprintln!(
                "I3_RESONANCE secular_pieces={} ledger={} kicks={}",
                s.pieces.len(),
                s.charge.ledger_total(),
                resonant.len()
            ),
            Err(err) => eprintln!("I3_RESONANCE fallback (fixture closed): {err}"),
        }
        let weak = vec![crate::coupled_source_response::Intervention {
            t: 1.25,
            body_id: 0,
            delta_v: [0.0, 0.02],
        }];
        let forced = compile_secular_response(laboratory_circular_pair(), weak, 6.0);
        match forced {
            Ok(s) => eprintln!(
                "I3_FORCE secular_pieces={} ledger={} remainder={}",
                s.pieces.len(),
                s.charge.ledger_total(),
                s.max_remainder
            ),
            Err(err) => eprintln!("I3_FORCE fallback: {err}"),
        }
    }

    #[test]
    fn i3_lazy_pair_inverse_defers_dense_setup() {
        use crate::coupled_source_response::{
            compile_source_response_opts, ensure_pair_inverse, CompileOpts,
        };
        let mut rows = Vec::new();
        for h in [3.0_f64, 6.0] {
            let eager =
                compile_source_response(laboratory_two_body(), vec![], h, 1.0 / 32.0).unwrap();
            let lazy = compile_source_response_opts(
                laboratory_two_body(),
                vec![],
                h,
                1.0 / 32.0,
                CompileOpts {
                    store_pair_inverse: false,
                },
            )
            .unwrap();
            let eager_c = TotalCost::of(&eager);
            let lazy_c = TotalCost::of(&lazy);
            assert!(lazy.pair_inverse.is_none());
            assert!(eager.pair_inverse.is_some());
            eprintln!(
                "I3_LAZY_INVERSE H={h} eager_ledger={} lazy_ledger={} eager_factor={} lazy_factor={} eager_bytes={} lazy_bytes={} eager_n={}",
                eager_c.ledger,
                lazy_c.ledger,
                eager_c.factorization,
                lazy_c.factorization,
                eager_c.bytes,
                lazy_c.bytes,
                eager.pair_inverse.as_ref().unwrap().n
            );
            rows.push((h, eager_c, lazy_c, eager.pair_inverse.as_ref().unwrap().n));
        }
        let mut on_demand = compile_source_response_opts(
            laboratory_two_body(),
            vec![],
            3.0,
            1.0 / 32.0,
            CompileOpts {
                store_pair_inverse: false,
            },
        )
        .unwrap();
        ensure_pair_inverse(&mut on_demand).unwrap();
        assert!(on_demand.pair_inverse.is_some());
        let n3 = rows[0].3;
        let n6 = rows[1].3;
        assert!(n6 > n3, "eager inverse dimension still grows with H");
        if rows[1].2.ledger < rows[1].1.ledger && rows[1].2.factorization < rows[1].1.factorization
        {
            eprintln!(
                "I3_KEEP lazy pair-inverse when no Schur consumer: H=6 ledger {} < eager {}, factor {} < {}",
                rows[1].2.ledger, rows[1].1.ledger, rows[1].2.factorization, rows[1].1.factorization
            );
        } else {
            eprintln!(
                "I3_REJECT lazy pair-inverse as a total-cost win: lazy {} vs eager {}",
                rows[1].2.ledger, rows[1].1.ledger
            );
        }
        eprintln!("I3_LAZY_INVERSE failure_case=Schur consumer still pays ensure_pair_inverse; H=3 Schur tide remains rejected");
    }

    #[test]
    fn i3_osculating_varies_elements_not_a_post_pass() {
        use crate::coupled_source_response::{
            compile_source_response_opts, laboratory_two_body, CompileOpts,
        };
        use crate::i3_secular::{
            compile_osculating_response, laboratory_circular_pair, laboratory_eccentric_pair,
            laboratory_resonant_kicks, OSC_POS_BAND,
        };

        assert_eq!(OSC_POS_BAND, 0.20, "gate declared before this slice's runs");
        let mut rows = Vec::new();
        for h in [4.0_f64, 6.0] {
            let osc = compile_osculating_response(laboratory_circular_pair(), vec![], h);
            let collocation = compile_source_response_opts(
                laboratory_circular_pair(),
                vec![],
                h,
                1.0 / 32.0,
                CompileOpts {
                    store_pair_inverse: false,
                },
            )
            .unwrap();
            let coll_cost = TotalCost::of(&collocation);
            match osc {
                Ok(osc) => {
                    let mut q_charge = Charge::default();
                    let t_eval = std::time::Instant::now();
                    let mut max_dx = 0.0_f64;
                    for k in 0..8 {
                        let t = h * (k as f64 + 0.5) / 8.0;
                        let xs = osc.eval(0, t, &mut q_charge).unwrap();
                        let xc = eval_interval_at(&collocation, t);
                        max_dx = max_dx.max((xs[0] - xc[0]).abs().max((xs[1] - xc[1]).abs()));
                    }
                    let eval_ns = t_eval.elapsed().as_nanos();
                    let a0 = osc.samples.first().map(|(_, e)| e.a).unwrap_or(0.0);
                    let a1 = osc.samples.last().map(|(_, e)| e.a).unwrap_or(0.0);
                    eprintln!(
                        "I3_OSC H={h} osc_ledger={} collocation_ledger={} osc_runtime={} collocation_runtime={} osc_bytes={} collocation_bytes={} osc_coeff={} collocation_coeff={} osc_factor={} collocation_factor={} osc_recon={} collocation_recon={} osc_cert={} collocation_cert={} remainder={} max_dx={} pos_band={} eval_ns={} osc_wall={} collocation_wall={} collocation_se={} collocation_ret={} samples={} a0={} a1={}",
                        osc.charge.ledger_total(),
                        coll_cost.ledger,
                        osc.charge.runtime_request_total(),
                        coll_cost.runtime,
                        osc.bytes(),
                        coll_cost.bytes,
                        osc.charge.coefficient_construction,
                        coll_cost.coefficient_construction,
                        osc.charge.factorization,
                        coll_cost.factorization,
                        osc.charge.reconstruction + q_charge.reconstruction,
                        coll_cost.reconstruction,
                        osc.charge.validation + osc.charge.verification,
                        coll_cost.certificate,
                        osc.max_remainder,
                        max_dx,
                        OSC_POS_BAND,
                        eval_ns,
                        osc.wall_ns,
                        coll_cost.wall_ns,
                        coll_cost.source_evolution,
                        coll_cost.retarded_solves,
                        osc.samples.len(),
                        a0,
                        a1
                    );
                    rows.push((
                        h,
                        Some(osc.charge.ledger_total()),
                        coll_cost.ledger,
                        Some(max_dx),
                        Some(osc.charge.source_evolution + osc.charge.retarded_solves),
                        coll_cost.source_evolution + coll_cost.retarded_solves,
                        (a1 - a0).abs() > 1e-8,
                    ));
                }
                Err(err) => {
                    eprintln!(
                        "I3_OSC H={h} fallback={err} collocation_ledger={} collocation_se={} collocation_ret={}",
                        coll_cost.ledger, coll_cost.source_evolution, coll_cost.retarded_solves
                    );
                    rows.push((
                        h,
                        None,
                        coll_cost.ledger,
                        None,
                        None,
                        coll_cost.source_evolution + coll_cost.retarded_solves,
                        false,
                    ));
                }
            }
        }
        let col_lo = rows[0].2;
        let col_hi = rows[1].2;
        assert!(col_hi > col_lo, "collocation must still grow with H");
        match (rows[0].1, rows[0].3, rows[1].1, rows[1].3) {
            (Some(osc_lo), Some(dx_lo), Some(osc_hi), Some(dx_hi)) => {
                let matched = dx_lo < OSC_POS_BAND && dx_hi < OSC_POS_BAND;
                let varied = rows[0].6 || rows[1].6;
                let cheaper = osc_hi < col_hi && osc_lo < col_lo;
                if matched && cheaper && varied {
                    eprintln!(
                        "I3_KEEP osculating Kepler in circular a=4 H=4..6: ledger {osc_lo}->{osc_hi} < collocation {col_lo}->{col_hi}, max_dx {dx_lo}->{dx_hi} < {OSC_POS_BAND}"
                    );
                } else {
                    eprintln!(
                        "I3_REJECT osculating Kepler as skipped GEM: matched={matched} varied={varied} cheaper={cheaper} ledger {osc_lo}->{osc_hi} vs {col_lo}->{col_hi} max_dx {dx_lo}->{dx_hi} band={OSC_POS_BAND}"
                    );
                }
            }
            (Some(osc_lo), Some(dx_lo), None, _) => {
                eprintln!(
                    "I3_REJECT osculating Kepler: H=4 ledger {osc_lo} max_dx={dx_lo}; H=6 refused. collocation {col_lo}->{col_hi}"
                );
            }
            _ => {
                eprintln!(
                    "I3_REJECT osculating Kepler: construction refused in H=4..6; collocation {col_lo}->{col_hi}"
                );
            }
        }

        let ecc = compile_osculating_response(laboratory_eccentric_pair(), vec![], 6.0);
        match &ecc {
            Ok(s) => eprintln!(
                "I3_OSC_ECC ledger={} remainder={} samples={} e0={}",
                s.charge.ledger_total(),
                s.max_remainder,
                s.samples.len(),
                s.samples[0].1.e
            ),
            Err(err) => eprintln!("I3_OSC_ECC fallback: {err}"),
        }

        let radial = compile_osculating_response(laboratory_two_body(), vec![], 6.0);
        assert!(
            radial.is_err(),
            "radial rest pair remains a close-encounter fallback"
        );
        eprintln!("I3_OSC_ENCOUNTER refuse={}", radial.unwrap_err());

        let period = compile_osculating_response(laboratory_circular_pair(), vec![], 4.0)
            .map(|s| s.samples[0].1.period)
            .unwrap_or(2.0);
        let resonant = laboratory_resonant_kicks(period.min(2.0), 6.0);
        match compile_osculating_response(laboratory_circular_pair(), resonant, 6.0) {
            Ok(s) => eprintln!(
                "I3_OSC_RESONANCE samples={} ledger={} remainder={}",
                s.samples.len(),
                s.charge.ledger_total(),
                s.max_remainder
            ),
            Err(err) => eprintln!("I3_OSC_RESONANCE fallback: {err}"),
        }
        let weak = vec![crate::coupled_source_response::Intervention {
            t: 1.25,
            body_id: 0,
            delta_v: [0.0, 0.02],
        }];
        match compile_osculating_response(laboratory_circular_pair(), weak, 6.0) {
            Ok(s) => eprintln!(
                "I3_OSC_FORCE samples={} ledger={} remainder={}",
                s.samples.len(),
                s.charge.ledger_total(),
                s.max_remainder
            ),
            Err(err) => eprintln!("I3_OSC_FORCE fallback: {err}"),
        }
    }

    #[test]
    fn i3_memory_kernel_does_not_collocate_the_skipped_interval() {
        use crate::coupled_source_response::{
            compile_source_response_opts, laboratory_distant_tide, laboratory_two_body, CompileOpts,
        };
        use crate::i3_kernel::{
            compile_memory_kernel_response, laboratory_tight_pair, KERNEL_A_BAND, KERNEL_MEMORY,
            KERNEL_POS_BAND, KERNEL_RANK_MAX, KERNEL_STEP,
        };
        use crate::i3_secular::{
            laboratory_circular_pair, laboratory_eccentric_pair, laboratory_resonant_kicks,
        };

        assert_eq!(KERNEL_POS_BAND, 0.05, "gate declared before this slice's runs");
        assert_eq!(KERNEL_A_BAND, 0.05, "gate declared before this slice's runs");
        assert_eq!(KERNEL_RANK_MAX, 16);
        assert_eq!(KERNEL_MEMORY, 1.0);
        assert_eq!(KERNEL_STEP, 0.5);

        let mut rows = Vec::new();
        for h in [4.0_f64, 6.0] {
            let kernel = compile_memory_kernel_response(laboratory_circular_pair(), vec![], h);
            let collocation = compile_source_response_opts(
                laboratory_circular_pair(),
                vec![],
                h,
                1.0 / 32.0,
                CompileOpts {
                    store_pair_inverse: false,
                },
            )
            .unwrap();
            let coll_cost = TotalCost::of(&collocation);
            let coll_nfun = collocation.interval_functions.len();
            match kernel {
                Ok(k) => {
                    let mut q_charge = Charge::default();
                    let mut max_dx = 0.0_f64;
                    let mut max_da = 0.0_f64;
                    for i in 0..8 {
                        let t = h * (i as f64 + 0.5) / 8.0;
                        let xs = k.eval(0, t, &mut q_charge).unwrap();
                        let xc = eval_interval_at(&collocation, t);
                        max_dx = max_dx.max((xs[0] - xc[0]).abs().max((xs[1] - xc[1]).abs()));
                        if let (Ok(ak), Some(fun)) = (
                            k.accel(0, t),
                            collocation.interval_functions.iter().find(|f| {
                                f.body_id == 0 && t + 1e-15 >= f.t0 && t <= f.t1 + 1e-15
                            }),
                        ) {
                            max_da = max_da
                                .max((ak[0] - fun.a[0]).abs().max((ak[1] - fun.a[1]).abs()));
                        }
                    }
                    eprintln!(
                        "I3_KERNEL H={h} kernel_ledger={} collocation_ledger={} kernel_runtime={} collocation_runtime={} kernel_bytes={} collocation_bytes={} kernel_coeff={} collocation_coeff={} kernel_factor={} collocation_factor={} kernel_recon={} collocation_recon={} kernel_cert={} collocation_cert={} remainder={} discarded={} max_dx={} max_da={} pos_band={} a_band={} rank={} k_n={} memory_len={} fill_in={} stored_funs={} coll_nfun={} kernel_se={} collocation_se={} collocation_ret={} min_r={}",
                        k.charge.ledger_total(),
                        coll_cost.ledger,
                        k.charge.runtime_request_total(),
                        coll_cost.runtime,
                        k.bytes(),
                        coll_cost.bytes,
                        k.charge.coefficient_construction,
                        coll_cost.coefficient_construction,
                        k.charge.factorization,
                        coll_cost.factorization,
                        k.charge.reconstruction + q_charge.reconstruction,
                        coll_cost.reconstruction,
                        k.charge.validation + k.charge.verification,
                        coll_cost.certificate,
                        k.max_remainder,
                        k.discarded_energy,
                        max_dx,
                        max_da,
                        KERNEL_POS_BAND,
                        KERNEL_A_BAND,
                        k.boundary_rank,
                        k.jacobian_n,
                        k.memory_len,
                        k.fill_in,
                        k.stored_funs(),
                        coll_nfun,
                        k.charge.source_evolution,
                        coll_cost.source_evolution,
                        coll_cost.retarded_solves,
                        k.min_r
                    );
                    rows.push((
                        h,
                        Some(k.charge.ledger_total()),
                        coll_cost.ledger,
                        Some(max_dx),
                        Some(max_da),
                        k.boundary_rank,
                        k.jacobian_n,
                        k.memory_len,
                        k.fill_in,
                        k.stored_funs(),
                        coll_nfun,
                    ));
                }
                Err(err) => {
                    eprintln!(
                        "I3_KERNEL H={h} fallback={err} collocation_ledger={} collocation_se={} collocation_ret={} coll_nfun={}",
                        coll_cost.ledger,
                        coll_cost.source_evolution,
                        coll_cost.retarded_solves,
                        coll_nfun
                    );
                    rows.push((
                        h, None, coll_cost.ledger, None, None, 0, 0, 0, 0, 0, coll_nfun,
                    ));
                }
            }
        }
        let col_lo = rows[0].2;
        let col_hi = rows[1].2;
        assert!(col_hi > col_lo, "collocation must still grow with H");
        match (rows[0].1, rows[0].3, rows[1].1, rows[1].3) {
            (Some(k_lo), Some(dx_lo), Some(k_hi), Some(dx_hi)) => {
                let da_lo = rows[0].4.unwrap_or(f64::INFINITY);
                let da_hi = rows[1].4.unwrap_or(f64::INFINITY);
                let matched = dx_lo < KERNEL_POS_BAND
                    && dx_hi < KERNEL_POS_BAND
                    && da_lo < KERNEL_A_BAND
                    && da_hi < KERNEL_A_BAND;
                let cheaper = k_hi < col_hi && k_lo < col_lo;
                let rank_grew = rows[1].5 > rows[0].5;
                let kn_grew = rows[1].6 > rows[0].6;
                let mem_grew = rows[1].7 > rows[0].7;
                let fill_grew = rows[1].8 > rows[0].8;
                // Plan kill: rank/memory/fill-in growing like the dense pair-inverse.
                // Coarse marched samples still grow with H (slower than collocation nfun);
                // that is the trajectory, not operator fill-in.
                let like_dense = kn_grew || fill_grew || rank_grew || mem_grew;
                if matched && cheaper && !like_dense {
                    eprintln!(
                        "I3_KEEP memory-kernel in circular a=4 H=4..6: ledger {k_lo}->{k_hi} < collocation {col_lo}->{col_hi}, max_dx {dx_lo}->{dx_hi} < {KERNEL_POS_BAND}, da {da_lo}->{da_hi} < {KERNEL_A_BAND}, rank {}->{}, memory {}->{}, fill {}->{}, stored {}->{} vs coll_nfun {}->{}",
                        rows[0].5, rows[1].5, rows[0].7, rows[1].7, rows[0].8, rows[1].8, rows[0].9, rows[1].9, rows[0].10, rows[1].10
                    );
                } else {
                    eprintln!(
                        "I3_REJECT memory-kernel as skipped GEM: matched={matched} cheaper={cheaper} like_dense={like_dense} ledger {k_lo}->{k_hi} vs {col_lo}->{col_hi} max_dx {dx_lo}->{dx_hi} da {da_lo}->{da_hi} rank {}->{} k_n {}->{} memory {}->{} fill {}->{} stored {}->{} coll_nfun {}->{}",
                        rows[0].5, rows[1].5, rows[0].6, rows[1].6, rows[0].7, rows[1].7, rows[0].8, rows[1].8, rows[0].9, rows[1].9, rows[0].10, rows[1].10
                    );
                }
            }
            _ => {
                eprintln!(
                    "I3_REJECT memory-kernel: construction refused in H=4..6; collocation {col_lo}->{col_hi}"
                );
            }
        }

        match compile_memory_kernel_response(laboratory_eccentric_pair(), vec![], 6.0) {
            Ok(s) => {
                let ecc_col = compile_source_response_opts(
                    laboratory_eccentric_pair(),
                    vec![],
                    6.0,
                    1.0 / 32.0,
                    CompileOpts {
                        store_pair_inverse: false,
                    },
                )
                .unwrap();
                let mut q = Charge::default();
                let mut ecc_dx = 0.0_f64;
                for i in 0..8 {
                    let t = 6.0 * (i as f64 + 0.5) / 8.0;
                    let xs = s.eval(0, t, &mut q).unwrap();
                    let xc = eval_interval_at(&ecc_col, t);
                    ecc_dx = ecc_dx.max((xs[0] - xc[0]).abs().max((xs[1] - xc[1]).abs()));
                }
                eprintln!(
                    "I3_KERNEL_ECC ledger={} collocation_ledger={} remainder={} rank={} memory_len={} max_dx={} pos_band={}",
                    s.charge.ledger_total(),
                    ecc_col.charge.ledger_total(),
                    s.max_remainder,
                    s.boundary_rank,
                    s.memory_len,
                    ecc_dx,
                    KERNEL_POS_BAND
                );
            }
            Err(err) => eprintln!("I3_KERNEL_ECC fallback: {err}"),
        }
        match compile_memory_kernel_response(laboratory_tight_pair(), vec![], 6.0) {
            Ok(s) => eprintln!(
                "I3_KERNEL_COUPLE ledger={} remainder={} rank={} min_r={}",
                s.charge.ledger_total(),
                s.max_remainder,
                s.boundary_rank,
                s.min_r
            ),
            Err(err) => eprintln!("I3_KERNEL_COUPLE fallback: {err}"),
        }
        let radial = compile_memory_kernel_response(laboratory_two_body(), vec![], 6.0);
        assert!(
            radial.is_err(),
            "radial rest pair remains a close-encounter fallback"
        );
        eprintln!("I3_KERNEL_ENCOUNTER refuse={}", radial.unwrap_err());
        let resonant = laboratory_resonant_kicks(2.0, 6.0);
        match compile_memory_kernel_response(laboratory_circular_pair(), resonant, 6.0) {
            Ok(s) => eprintln!(
                "I3_KERNEL_RESONANCE ledger={} remainder={}",
                s.charge.ledger_total(),
                s.max_remainder
            ),
            Err(err) => eprintln!("I3_KERNEL_RESONANCE fallback: {err}"),
        }
        match compile_memory_kernel_response(laboratory_distant_tide(), vec![], 4.0) {
            Ok(s) => eprintln!("I3_KERNEL_ENTRANT ledger={}", s.charge.ledger_total()),
            Err(err) => eprintln!("I3_KERNEL_ENTRANT fallback: {err}"),
        }
    }

    #[test]
    fn i3_kernel_amortizes_bootstrap_and_wires_kicks() {
        use crate::coupled_source_response::{
            compile_source_response_opts, laboratory_distant_tide, laboratory_encounter,
            laboratory_kick, repair_from_committed, CompileOpts, Intervention,
        };
        use crate::i3_kernel::{
            compile_kernel_with_kick, compile_memory_kernel_response, recouple_kernel_suffix,
            KERNEL_A_BAND, KERNEL_KICK_A_BAND, KERNEL_KICK_POS_BAND, KERNEL_POS_BAND,
        };
        use crate::i3_secular::laboratory_circular_pair;

        assert_eq!(KERNEL_POS_BAND, 0.05, "quiet gate declared before this slice");
        assert_eq!(KERNEL_A_BAND, 0.05, "quiet gate declared before this slice");
        assert_eq!(KERNEL_KICK_POS_BAND, 0.05, "kick gate declared before this slice");
        assert_eq!(KERNEL_KICK_A_BAND, 0.05, "kick gate declared before this slice");

        let mut quiet_rows = Vec::new();
        for h in [8.0_f64, 12.0] {
            let kernel = compile_memory_kernel_response(laboratory_circular_pair(), vec![], h)
                .expect("quiet kernel at longer H");
            let collocation = compile_source_response_opts(
                laboratory_circular_pair(),
                vec![],
                h,
                1.0 / 32.0,
                CompileOpts {
                    store_pair_inverse: false,
                },
            )
            .unwrap();
            let coll_cost = TotalCost::of(&collocation);
            let split = kernel.split();
            let mut q = Charge::default();
            let mut max_dx = 0.0_f64;
            let mut max_da = 0.0_f64;
            let mut t_at_max_da = 0.0_f64;
            for i in 0..8 {
                let t = h * (i as f64 + 0.5) / 8.0;
                let xs = kernel.eval(0, t, &mut q).unwrap();
                let xc = eval_interval_at(&collocation, t);
                max_dx = max_dx.max((xs[0] - xc[0]).abs().max((xs[1] - xc[1]).abs()));
                if let (Ok(ak), Some(fun)) = (
                    kernel.accel(0, t),
                    collocation
                        .interval_functions
                        .iter()
                        .rev()
                        .find(|f| f.body_id == 0 && t + 1e-15 >= f.t0 && t <= f.t1 + 1e-15),
                ) {
                    let da = (ak[0] - fun.a[0]).abs().max((ak[1] - fun.a[1]).abs());
                    if da > max_da {
                        max_da = da;
                        t_at_max_da = t;
                    }
                }
            }
            let advance_share = split.advance as f64 / split.total.max(1) as f64;
            let boot_share = split.bootstrap as f64 / split.total.max(1) as f64;
            eprintln!(
                "I3_KERNEL_AMORT H={h} total={} bootstrap={} jacobian={} advance={} cert={} recon={} fallback={} collocation={} coll_se={} max_dx={} max_da={} t_at_max_da={} rank={} k_n={} memory={} fill={} boot_share={:.3} advance_share={:.3}",
                split.total,
                split.bootstrap,
                split.jacobian,
                split.advance,
                split.certificate,
                split.reconstruction + q.reconstruction,
                split.fallback,
                coll_cost.ledger,
                coll_cost.source_evolution,
                max_dx,
                max_da,
                t_at_max_da,
                kernel.boundary_rank,
                kernel.jacobian_n,
                kernel.memory_len,
                kernel.fill_in,
                boot_share,
                advance_share
            );
            quiet_rows.push((
                h,
                split,
                coll_cost.ledger,
                max_dx,
                max_da,
                kernel.boundary_rank,
                kernel.jacobian_n,
                kernel.memory_len,
                kernel.fill_in,
            ));
        }
        let a0 = &quiet_rows[0];
        let a1 = &quiet_rows[1];
        let rank_bounded = a0.5 == a1.5 && a0.6 == a1.6 && a0.7 == a1.7 && a0.8 == a1.8;
        let matched = a0.3 < KERNEL_POS_BAND
            && a1.3 < KERNEL_POS_BAND
            && a0.4 < KERNEL_A_BAND
            && a1.4 < KERNEL_A_BAND;
        let cheaper = a0.1.total < a0.2 && a1.1.total < a1.2;
        let advance_grows = a1.1.advance > a0.1.advance;
        let bootstrap_flat = a1.1.bootstrap == a0.1.bootstrap;
        let boot_still_dominates = a1.1.bootstrap as f64 > 0.5 * a1.1.total as f64;
        if matched && cheaper && rank_bounded && advance_grows && bootstrap_flat {
            eprintln!(
                "I3_KEEP quiet kernel amortization H=8..12: ledger {}->{} < collocation {}->{}, Δx {}->{}, advance {}->{}, bootstrap {} (dominates={})",
                a0.1.total, a1.1.total, a0.2, a1.2, a0.3, a1.3, a0.1.advance, a1.1.advance, a1.1.bootstrap, boot_still_dominates
            );
        } else {
            eprintln!(
                "I3_REJECT quiet kernel amortization: matched={matched} cheaper={cheaper} rank_bounded={rank_bounded} advance_grows={advance_grows} bootstrap_flat={bootstrap_flat} boot_dominates={boot_still_dominates}"
            );
        }
        if boot_still_dominates {
            eprintln!(
                "I3_KERNEL_AMORT bootstrap remains {:.3} of H=12 ledger {}; not invented amortization of setup",
                a1.1.bootstrap as f64 / a1.1.total.max(1) as f64,
                a1.1.total
            );
        }

        let h = 8.0_f64;
        let weak = vec![Intervention {
            t: 2.0,
            body_id: 0,
            delta_v: [0.0, 0.02],
        }];
        let kicked_col = compile_source_response_opts(
            laboratory_circular_pair(),
            weak.clone(),
            h,
            1.0 / 32.0,
            CompileOpts {
                store_pair_inverse: false,
            },
        )
        .unwrap();
        let col_kick = TotalCost::of(&kicked_col);
        let mut kick_keep = false;
        match compile_kernel_with_kick(laboratory_circular_pair(), weak.clone(), h) {
            Ok(resumed) => {
                let split = resumed.split();
                let mut q = Charge::default();
                let mut max_dx = 0.0_f64;
                let mut max_da = 0.0_f64;
                for i in 0..8 {
                    let t = h * (i as f64 + 0.5) / 8.0;
                    let xs = resumed.eval(0, t, &mut q).unwrap();
                    let xc = eval_interval_at(&kicked_col, t);
                    max_dx = max_dx.max((xs[0] - xc[0]).abs().max((xs[1] - xc[1]).abs()));
                    if let (Ok(ak), Some(fun)) = (
                        resumed.accel(0, t),
                        kicked_col.interval_functions.iter().rev().find(|f| {
                            f.body_id == 0 && t + 1e-15 >= f.t0 && t <= f.t1 + 1e-15
                        }),
                    ) {
                        max_da = max_da
                            .max((ak[0] - fun.a[0]).abs().max((ak[1] - fun.a[1]).abs()));
                    }
                }
                eprintln!(
                    "I3_KERNEL_KICK resume total={} bootstrap={} jacobian={} advance={} factor={} collocation={} max_dx={} max_da={} pos_band={} a_band={} rank={} memory={}",
                    split.total,
                    split.bootstrap,
                    split.jacobian,
                    split.advance,
                    resumed.charge.factorization,
                    col_kick.ledger,
                    max_dx,
                    max_da,
                    KERNEL_KICK_POS_BAND,
                    KERNEL_KICK_A_BAND,
                    resumed.boundary_rank,
                    resumed.memory_len
                );
                let matched = max_dx < KERNEL_KICK_POS_BAND && max_da < KERNEL_KICK_A_BAND;
                if matched && split.total < col_kick.ledger {
                    kick_keep = true;
                    eprintln!(
                        "I3_KEEP kernel-resume after weak kick H=8: ledger {} < collocation {}, Δx={max_dx}",
                        split.total, col_kick.ledger
                    );
                } else {
                    eprintln!(
                        "I3_REJECT kernel-resume after weak kick: matched={matched} cheaper={} Δx={max_dx} da={max_da}",
                        split.total < col_kick.ledger
                    );
                    let prefix =
                        compile_memory_kernel_response(laboratory_circular_pair(), vec![], 2.0)
                            .unwrap();
                    match recouple_kernel_suffix(&prefix, &weak, h) {
                        Ok(suffix) => {
                            let suf = TotalCost::of(&suffix);
                            eprintln!(
                                "I3_KERNEL_KICK recouple_suffix ledger={} collocation={}",
                                suf.ledger, col_kick.ledger
                            );
                            if suf.ledger < col_kick.ledger {
                                eprintln!(
                                    "I3_KEEP kernel-prefix + recouple-suffix H=8: {} < {}",
                                    suf.ledger, col_kick.ledger
                                );
                                kick_keep = true;
                            } else {
                                eprintln!(
                                    "I3_REJECT kernel-prefix + recouple-suffix as break-even: {} >= {}",
                                    suf.ledger, col_kick.ledger
                                );
                            }
                        }
                        Err(err) => eprintln!("I3_KERNEL_KICK recouple_suffix fallback: {err}"),
                    }
                    let quiet = compile_source_response_opts(
                        laboratory_circular_pair(),
                        vec![],
                        h,
                        1.0 / 32.0,
                        CompileOpts {
                            store_pair_inverse: false,
                        },
                    )
                    .unwrap();
                    match repair_from_committed(&quiet, &weak, h, 1.0 / 32.0) {
                        Ok(repaired) => {
                            let rc = TotalCost::of(&repaired);
                            eprintln!(
                                "I3_KERNEL_KICK prefix-repair ledger={} recouple={}",
                                rc.ledger, col_kick.ledger
                            );
                        }
                        Err(err) => eprintln!("I3_KERNEL_KICK prefix-repair fallback: {err}"),
                    }
                }
            }
            Err(err) => {
                eprintln!("I3_KERNEL_KICK resume fallback: {err}");
                eprintln!(
                    "I3_FALLBACK kicked collocation ledger={}",
                    col_kick.ledger
                );
            }
        }

        let strong = laboratory_kick();
        let strong_col = compile_source_response_opts(
            laboratory_circular_pair(),
            strong.clone(),
            8.0,
            1.0 / 32.0,
            CompileOpts {
                store_pair_inverse: false,
            },
        )
        .unwrap();
        match compile_kernel_with_kick(laboratory_circular_pair(), strong, 8.0) {
            Ok(s) => {
                let mut q = Charge::default();
                let mut dx = 0.0_f64;
                for i in 0..8 {
                    let t = 8.0 * (i as f64 + 0.5) / 8.0;
                    let xs = s.eval(0, t, &mut q).unwrap();
                    let xc = eval_interval_at(&strong_col, t);
                    dx = dx.max((xs[0] - xc[0]).abs().max((xs[1] - xc[1]).abs()));
                }
                eprintln!(
                    "I3_KERNEL_KICK_STRONG ledger={} collocation={} max_dx={} pos_band={}",
                    s.charge.ledger_total(),
                    TotalCost::of(&strong_col).ledger,
                    dx,
                    KERNEL_KICK_POS_BAND
                );
                if dx >= KERNEL_KICK_POS_BAND {
                    eprintln!(
                        "I3_REJECT strong kick (Δv=0.125) as skipped GEM: max_dx={dx} >= {KERNEL_KICK_POS_BAND}"
                    );
                }
            }
            Err(err) => eprintln!("I3_KERNEL_KICK_STRONG fallback: {err}"),
        }
        let (enc_ic, _) = laboratory_encounter();
        let enc = compile_kernel_with_kick(enc_ic.clone(), vec![Intervention {
            t: 2.0,
            body_id: 0,
            delta_v: [0.0, 0.02],
        }], 4.0);
        assert!(enc.is_err(), "close-entrant stays a recouple/collocation fallback");
        eprintln!("I3_KERNEL_KICK_ENCOUNTER refuse={}", enc.unwrap_err());
        let enc_col = compile_source_response_opts(
            enc_ic,
            vec![],
            4.0,
            1.0 / 32.0,
            CompileOpts {
                store_pair_inverse: false,
            },
        )
        .unwrap();
        eprintln!(
            "I3_KERNEL_KICK_ENCOUNTER recouple_ledger={}",
            TotalCost::of(&enc_col).ledger
        );
        let tide = compile_kernel_with_kick(laboratory_distant_tide(), vec![Intervention {
            t: 2.0,
            body_id: 0,
            delta_v: [0.0, 0.02],
        }], 4.0);
        eprintln!(
            "I3_KERNEL_KICK_TIDE fallback={}",
            tide.err()
                .map(|e| e.to_string())
                .unwrap_or_else(|| "unexpected keep".into())
        );

        if !kick_keep {
            eprintln!(
                "I3_INCOMPLETE kick path has no total-cost break-even under predeclared 0.05 gates; I3 exit is not proven"
            );
        } else {
            eprintln!(
                "I3_KERNEL_KICK admitted in weak-kick H=8; I3 exit still requires a horizon where sequential collocation would have dominated including kicks"
            );
        }
    }

    #[test]
    fn i3_kernel_kick_patch_then_resume_is_the_last_strong_kick_method() {
        use crate::coupled_source_response::{
            compile_source_response_opts, laboratory_encounter, laboratory_kick, CompileOpts,
        };
        use crate::i3_kernel::{
            compile_kernel_kick_patch, KERNEL_PATCH_LEN, KERNEL_PATCH_POS_BAND,
        };
        use crate::i3_secular::laboratory_circular_pair;

        assert_eq!(KERNEL_PATCH_POS_BAND, 0.05, "gate declared before this slice");
        assert_eq!(KERNEL_PATCH_LEN, 1.0, "patch length declared before this slice");

        let h = 8.0_f64;
        let strong = laboratory_kick();
        let collocation = compile_source_response_opts(
            laboratory_circular_pair(),
            strong.clone(),
            h,
            1.0 / 32.0,
            CompileOpts {
                store_pair_inverse: false,
            },
        )
        .unwrap();
        let col = TotalCost::of(&collocation);
        match compile_kernel_kick_patch(laboratory_circular_pair(), strong, h) {
            Ok(patched) => {
                let split = patched.split();
                let mut q = Charge::default();
                let mut max_dx = 0.0_f64;
                for i in 0..8 {
                    let t = h * (i as f64 + 0.5) / 8.0;
                    let xs = patched.eval(0, t, &mut q).unwrap();
                    let xc = eval_interval_at(&collocation, t);
                    max_dx = max_dx.max((xs[0] - xc[0]).abs().max((xs[1] - xc[1]).abs()));
                }
                eprintln!(
                    "I3_KERNEL_PATCH H=8 total={} bootstrap={} jacobian={} advance={} patch={} collocation={} max_dx={} pos_band={} rank={} memory={}",
                    split.total,
                    split.bootstrap,
                    split.jacobian,
                    split.advance,
                    split.patch,
                    col.ledger,
                    max_dx,
                    KERNEL_PATCH_POS_BAND,
                    patched.boundary_rank,
                    patched.memory_len
                );
                let matched = max_dx < KERNEL_PATCH_POS_BAND;
                let cheaper = split.total < col.ledger;
                if matched && cheaper {
                    eprintln!(
                        "I3_KEEP kick-patch then kernel-resume H=8: ledger {} < {}, Δx={max_dx} < {KERNEL_PATCH_POS_BAND}",
                        split.total, col.ledger
                    );
                } else {
                    eprintln!(
                        "I3_REJECT kick-patch then kernel-resume: matched={matched} cheaper={cheaper} ledger {} vs {} max_dx={max_dx} band={KERNEL_PATCH_POS_BAND}; stop shopping",
                        split.total, col.ledger
                    );
                }
            }
            Err(err) => {
                eprintln!(
                    "I3_REJECT kick-patch construction: {err}; collocation={}; stop shopping",
                    col.ledger
                );
            }
        }

        let (enc_ic, _) = laboratory_encounter();
        let enc = compile_kernel_kick_patch(
            enc_ic.clone(),
            vec![crate::coupled_source_response::Intervention {
                t: 2.0,
                body_id: 0,
                delta_v: [0.0, 0.125],
            }],
            4.0,
        );
        assert!(enc.is_err(), "close-entrant is not a kernel-patch domain");
        eprintln!("I3_KERNEL_PATCH_ENCOUNTER refuse={}", enc.unwrap_err());
        let enc_col = compile_source_response_opts(
            enc_ic,
            vec![],
            4.0,
            1.0 / 32.0,
            CompileOpts {
                store_pair_inverse: false,
            },
        )
        .unwrap();
        eprintln!(
            "I3_KERNEL_PATCH_ENCOUNTER recouple_ledger={}",
            TotalCost::of(&enc_col).ledger
        );
        eprintln!(
            "I3_DOMAIN admitted=quiet_kernel H=4..12, weak_kick_resume H=8; failure=strong_kernel_resume, strong_kick_patch_measured_above, close_entrant_recouple, Kepler, PERIOD, compact-after-the-fact, Schur tide, population-solved"
        );
    }
}
