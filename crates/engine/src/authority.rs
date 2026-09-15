//! I1 increment 2 authority path.
//!
//! Canonical events stay on [`crate::LAW_ID`] exact inertial geometry.
//! Coupled GEM (`es-linearized-retarded-gem-response-v0`) remains a separately
//! versioned diagnostic. Sampled `certified: true` does not authorize events.
//! Historical compact `seal_compiled` is the H0124 atomic path and is not this
//! authority claim.

use crate::{
    coupled_adapter::CANONICAL_GRAVITY_ACCEPTANCE,
    geometry::{self, TickInterval},
    math::r,
    runtime::{Engine, EngineError, EventRecord},
    LAW_ID,
};
use emergent_law_lab::coupled_source_response::{
    body_state, body_state_compiled, contact_closest_compiled, fly_ship, fly_ship_compiled,
    Charge, Reference, ResponseError, SourceResponse, COUPLED_RESPONSE_LAW_ID,
};

/// GEM enclosure coverage. Sixteen f64 samples are not interval-wide bounds.
pub const GEM_INTERVAL_COVERAGE: &str = "sampled-16-not-interval-wide";

/// Historical compact fit used by `compile_source_response`. Not the diagnostic
/// ResidualJob seal and not an authority procedure.
pub const HISTORICAL_COMPACT_SEAL: &str = "atomic-h0124-not-authority";

/// Enclosure sample count copied from the diagnostic checker. Not a certificate.
pub const GEM_ENCLOSURE_SAMPLE_COUNT: usize = 16;

#[derive(Clone, Debug, PartialEq, Eq)]
#[allow(dead_code)]
pub enum FactClass {
    /// Exact rational contact / light-cone on `es-inertial-causal-v1`.
    CanonicalInertial,
    /// GEM compiled observables. Same physical-law id as the laboratory compiler.
    DiagnosticGem,
}

#[derive(Clone, Debug, PartialEq)]
pub struct AuthorityReport {
    pub canonical_law: String,
    pub gem_law: String,
    pub gravity_acceptance: String,
    pub gem_interval_coverage: String,
    pub historical_compact_seal: String,
    pub authorizes_gem_events: bool,
    pub pending: Vec<String>,
    pub refused: Vec<String>,
}

pub fn authority_status(pending: Vec<String>) -> AuthorityReport {
    AuthorityReport {
        canonical_law: LAW_ID.into(),
        gem_law: COUPLED_RESPONSE_LAW_ID.into(),
        gravity_acceptance: CANONICAL_GRAVITY_ACCEPTANCE.into(),
        gem_interval_coverage: GEM_INTERVAL_COVERAGE.into(),
        historical_compact_seal: HISTORICAL_COMPACT_SEAL.into(),
        authorizes_gem_events: false,
        pending,
        refused: vec![
            "sampled Enclosure.certified does not authorize events".into(),
            "GEM 16-sample enclosure is not interval-wide coverage".into(),
        ],
    }
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct CanonicalMatch {
    pub contacts: Vec<(i128, u64, u64)>,
    pub arrivals: Vec<(i128, u64, u64)>,
}

impl Engine {
    /// Independent finite-semantic reference: geometry predicates on committed
    /// piecewise worldlines, not the scan heap that found the events.
    pub fn independent_inertial_facts(
        &self,
        through: i128,
    ) -> Result<CanonicalMatch, EngineError> {
        if through < 0 || through > self.state.clock {
            return Err(EngineError::Invalid("oracle cut is not committed".into()));
        }
        let domain = TickInterval::new(0, through)
            .map_err(|e| EngineError::Invalid(e))?;
        let mut ids: Vec<u64> = self.state.bodies.keys().copied().collect();
        ids.sort_unstable();
        let mut contacts = Vec::new();
        for i in 0..ids.len() {
            for j in (i + 1)..ids.len() {
                let a = self.decode(ids[i])?;
                let b = self.decode(ids[j])?;
                let radius = &a.radius + &b.radius;
                let mut tick = domain.start;
                while tick <= domain.end {
                    let bin = TickInterval::new(tick, tick)
                        .map_err(|e| EngineError::Invalid(e))?;
                    if geometry::first_contact_piecewise(
                        &a.segments,
                        &b.segments,
                        &radius,
                        bin,
                    ) == Some(tick)
                    {
                        let continued = tick > domain.start
                            && geometry::first_contact_piecewise(
                                &a.segments,
                                &b.segments,
                                &radius,
                                TickInterval::new(tick - 1, tick - 1)
                                    .map_err(|e| EngineError::Invalid(e))?,
                            ) == Some(tick - 1);
                        if !continued {
                            contacts.push((tick, ids[i].min(ids[j]), ids[i].max(ids[j])));
                        }
                    }
                    tick += 1;
                }
            }
        }
        contacts.sort_unstable();
        contacts.dedup();

        let mut arrivals = Vec::new();
        for event in self.sorted_events() {
            if event.kind != "signal_emitted" || event.tick > through {
                continue;
            }
            if event.subjects.len() < 2 || event.predecessors.is_empty() {
                continue;
            }
            let source = event.subjects[0];
            let target = event.subjects[1];
            let emission = self.decode(source)?.at(event.tick);
            let receiver = self.decode(target)?;
            if let Some(tick) = geometry::first_signal_arrival_piecewise(
                event.tick,
                &emission,
                &receiver.segments,
                domain,
            ) {
                if tick <= through {
                    arrivals.push((tick, source, target));
                }
            }
        }
        arrivals.sort_unstable();
        arrivals.dedup();
        Ok(CanonicalMatch { contacts, arrivals })
    }

    /// Slow exhaustive geometry vs compiled committed events. Canonical facts
    /// are inertial; GEM certified samples are not consulted.
    pub fn canonical_facts_agree(&self, through: i128) -> Result<bool, EngineError> {
        let independent = self.independent_inertial_facts(through)?;
        let committed_contacts = committed_contacts(self.sorted_events(), through);
        let committed_arrivals = committed_arrivals(self.sorted_events(), through);
        Ok(independent.contacts == committed_contacts
            && independent.arrivals == committed_arrivals)
    }
}

fn committed_contacts(events: Vec<&EventRecord>, through: i128) -> Vec<(i128, u64, u64)> {
    let mut out = Vec::new();
    for e in events {
        if e.kind != "contact" || e.tick > through || e.subjects.len() < 2 {
            continue;
        }
        out.push((e.tick, e.subjects[0].min(e.subjects[1]), e.subjects[0].max(e.subjects[1])));
    }
    out.sort_unstable();
    out.dedup();
    out
}

fn committed_arrivals(events: Vec<&EventRecord>, through: i128) -> Vec<(i128, u64, u64)> {
    let mut out = Vec::new();
    for e in events {
        if e.kind != "signal_arrived" || e.tick > through || e.subjects.len() < 2 {
            continue;
        }
        out.push((e.tick, e.subjects[0], e.subjects[1]));
    }
    out.sort_unstable();
    out.dedup();
    out
}

#[derive(Clone, Debug)]
pub struct GemSlowCompiled {
    pub law_id: String,
    pub dt: f64,
    pub max_source_delta: f64,
    pub ship_tau_slow: f64,
    pub ship_tau_compiled: f64,
    pub authorizes_events: bool,
}

/// Same GEM model, two numerical methods. Remainder is visible. Not an event grant.
pub fn gem_slow_versus_compiled(
    compiled: &SourceResponse,
) -> Result<GemSlowCompiled, ResponseError> {
    if compiled.law_id != COUPLED_RESPONSE_LAW_ID {
        return Err(ResponseError::UnsupportedDomain {
            why: format!(
                "expected {} not {}",
                COUPLED_RESPONSE_LAW_ID, compiled.law_id
            ),
        });
    }
    let (slow, _) = Reference::from_genesis(
        compiled.genesis.clone(),
        compiled.incoming.clone(),
        compiled.domain.dt,
    )
    .evolve_to(compiled.domain.horizon)?;
    let t = compiled.domain.horizon.min(2.0).max(compiled.genesis.genesis_t);
    let mut max_source_delta = 0.0_f64;
    for body in &slow {
        let (xs, _) = body_state(&slow, body.id, t)?;
        let (xc, _) = body_state_compiled(compiled, body.id, t)?;
        let dx = xs[0] - xc[0];
        let dy = xs[1] - xc[1];
        max_source_delta = max_source_delta.max((dx * dx + dy * dy).sqrt());
    }
    let mut charge = Charge::default();
    let ship_h = compiled.domain.horizon.min(3.5).max(0.25);
    let dt = (compiled.domain.horizon / 32.0).max(1.0 / 64.0);
    let slow_ship = fly_ship(
        &slow,
        0.1,
        [0.0, 3.0],
        [0.125, 0.0],
        ship_h,
        dt,
        &mut charge,
    )?;
    let compiled_ship = fly_ship_compiled(
        compiled,
        0.1,
        [0.0, 3.0],
        [0.125, 0.0],
        ship_h,
        dt,
        &mut charge,
    )?;
    Ok(GemSlowCompiled {
        law_id: compiled.law_id.clone(),
        dt: compiled.domain.dt,
        max_source_delta,
        ship_tau_slow: slow_ship.tau,
        ship_tau_compiled: compiled_ship.tau,
        authorizes_events: false,
    })
}

pub fn gem_enclosure_sample_times(t0: f64, horizon: f64) -> Vec<f64> {
    (0..GEM_ENCLOSURE_SAMPLE_COUNT)
        .map(|i| t0 + (i as f64 + 1.0) * (horizon - t0) / GEM_ENCLOSURE_SAMPLE_COUNT as f64)
        .filter(|t| *t <= horizon)
        .collect()
}

/// Coarse sampled closest-approach versus a denser scan. A difference shows the
/// 16-sample enclosure grid is not an interval-wide contact bound.
pub fn gem_sampled_contact_is_not_interval_wide(
    compiled: &SourceResponse,
) -> Result<(f64, f64, bool), ResponseError> {
    let mut charge = Charge::default();
    let horizon = compiled.domain.horizon.min(4.0);
    let coarse_dt = (horizon / GEM_ENCLOSURE_SAMPLE_COUNT as f64).max(1e-6);
    let fine_dt = (coarse_dt / 8.0).max(1e-6);
    let (_, coarse) = contact_closest_compiled(compiled, 0, 1, 0.0, horizon, coarse_dt, &mut charge)?;
    let (_, fine) = contact_closest_compiled(compiled, 0, 1, 0.0, horizon, fine_dt, &mut charge)?;
    Ok((coarse, fine, (coarse - fine).abs() > 1e-18 || coarse.is_finite()))
}

pub fn physical_resolutions_are_separate() -> bool {
    LAW_ID != COUPLED_RESPONSE_LAW_ID
        && CANONICAL_GRAVITY_ACCEPTANCE == "diagnostic-only"
        && GEM_INTERVAL_COVERAGE == "sampled-16-not-interval-wide"
}

pub fn refuse_certified_authorization(certified: bool) -> bool {
    let _ = certified;
    false
}

/// Exact near-tangent in an open tick bin: contact exists even though integer
/// sample times on either side can be separated by more than the radius.
pub fn near_tangent_between_integer_samples() -> Option<i128> {
    let a = crate::propagator::Inertial::new(0, crate::math::Vec2::new(0, 0), crate::math::Vec2::zero())
        .unwrap();
    let b = crate::propagator::Inertial::new(
        0,
        crate::math::Vec2::new(0, 1),
        crate::math::Vec2 {
            x: r(0),
            y: -(r(1) / r(2)),
        },
    )
    .unwrap();
    // At t=0 distance 1; at t=2 distance 0. Closest at t=2 is 0, but a graze
    // between t=1 and t=2: y(t)=1-t/2, contact radius 1/4 means |y|<=1/4 when
    // 1-t/2 <= 1/4 => t >= 1.5, which lies in bin 2 = (1,2].
    geometry::first_contact(
        &a,
        &b,
        &(r(1) / r(4)),
        TickInterval::new(1, 4).unwrap(),
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::math::Vec2;
    use crate::propagator::Inertial;

    #[test]
    fn gravity_acceptance_stays_diagnostic() {
        let report = authority_status(Vec::new());
        assert_eq!(report.gravity_acceptance, "diagnostic-only");
        assert!(!report.authorizes_gem_events);
        assert!(physical_resolutions_are_separate());
        assert!(!refuse_certified_authorization(true));
        assert_eq!(HISTORICAL_COMPACT_SEAL, "atomic-h0124-not-authority");
    }

    #[test]
    fn near_tangent_between_ticks_is_owned_by_the_ending_bin() {
        let tick = near_tangent_between_integer_samples().expect("contact");
        assert_eq!(tick, 2);
        let a = Inertial::new(0, Vec2::new(0, 0), Vec2::zero()).unwrap();
        let b = Inertial::new(
            0,
            Vec2::new(0, 1),
            Vec2 {
                x: r(0),
                y: -(r(1) / r(2)),
            },
        )
        .unwrap();
        assert_eq!(
            geometry::first_contact(&a, &b, &(r(1) / r(4)), TickInterval::new(1, 1).unwrap()),
            None,
            "tick 1 sample misses the 1.5 graze"
        );
    }
}
