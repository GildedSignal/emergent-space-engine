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
}
