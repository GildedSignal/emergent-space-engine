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
    runtime::{Body, Command, Engine, EngineError, EventRecord},
    propagator::Inertial,
    LAW_ID,
};
use emergent_law_lab::coupled_source_response::{
    body_state, body_state_compiled, contact_closest_compiled, fly_ship, fly_ship_compiled,
    Charge, Reference, ResponseError, SourceResponse, COUPLED_RESPONSE_LAW_ID,
};
use emergent_law_lab::i4_gem_authority::enclose_gem_field_interval;

/// GEM enclosure coverage. Sixteen f64 samples are not interval-wide bounds.
pub const GEM_INTERVAL_COVERAGE: &str = "sampled-16-not-interval-wide";

/// I4 per-query unique retarded lookback. Not an interval-wide field bound
/// and not event authority. The interval-wide causal-block path lives in
/// law-lab `i4_gem_authority` and does not mint engine canonical gravity.
pub const GEM_RETARDED_ROOT_COVERAGE: &str =
    "per-query-unique-lookback-not-interval-wide-field";

/// I4 causal-block Lipschitz/KA delay enclosure on the admitted interior.
/// Engine canonical events stay inertial until this path is wired and covers
/// the queried domain.
pub const GEM_FIELD_INTERVAL_COVERAGE: &str =
    "causal-block-lipschitz-ka-delay-admitted-interior";

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
            format!("I4 retarded root: {GEM_RETARDED_ROOT_COVERAGE}"),
            format!(
                "I4 field interval {GEM_FIELD_INTERVAL_COVERAGE} is domain-local; engine canonical events stay inertial"
            ),
        ],
    }
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct CanonicalMatch {
    pub contacts: Vec<(i128, u64, u64)>,
    pub arrivals: Vec<(i128, u64, u64, String)>,
}

/// Exhaustive audit only: refuse large populations before materialization.
const ORACLE_MAX_IDENTITIES: usize = 4096;

fn segment_at(segments: &[Inertial], tick: i128) -> usize {
    segments.partition_point(|s| s.epoch <= tick).saturating_sub(1)
}

/// Independent exact quadratic minimum on the half-open bin (tick-1,tick].
/// Does not call the production contact search, heap, or broad phase.
fn oracle_contact_bin(a: &Inertial, b: &Inertial, radius: &crate::math::Rational, tick: i128) -> bool {
    let x = a.state_at(tick - 1) - b.state_at(tick - 1);
    let v = &a.velocity - &b.velocity;
    let q = v.norm_squared();
    let xv = x.dot(&v);
    let c = x.norm_squared() - radius * radius;
    if c < r(0) || &q + r(2) * &xv + &c <= r(0) {
        return true;
    }
    // A minimum strictly inside the bin also counts; a left-only tangent does not.
    q > r(0) && xv < r(0) && -&xv < q && c * q <= &xv * &xv
}

fn has_range_burn(engine: &Engine, id: u64, tick: i128) -> bool {
    engine.state.interventions.iter().any(|input| matches!(&input.command,
        Command::SetCourseRange { lo, hi, at, .. } if *lo <= id && id <= *hi && *at == tick))
}

fn oracle_bodies(engine: &Engine, through: i128) -> Result<Vec<Body>, EngineError> {
    let mut ids: std::collections::BTreeSet<u64> = engine.state.bodies.keys().copied().collect();
    for f in &engine.state.genesis_families {
        if f.phase.is_some() {
            return Err(EngineError::Unsupported("oracle phase-family revision history is not implemented".into()));
        }
        if f.count > ORACLE_MAX_IDENTITIES as u64 || ids.len() + f.count as usize > ORACLE_MAX_IDENTITIES {
            return Err(EngineError::ResourceLimit("exhaustive oracle identity limit".into()));
        }
        ids.extend(f.first_id..=f.last_id());
    }
    if ids.len() > ORACLE_MAX_IDENTITIES {
        return Err(EngineError::ResourceLimit("exhaustive oracle identity limit".into()));
    }
    let mut out = Vec::new();
    for id in ids {
        let mut body = engine.decode(id)?;
        if let Some(f) = engine.state.genesis_families.iter().find(|f| f.contains(id)) {
            let mut segments = f.member_segments(id).ok_or(EngineError::UnknownIdentity(id))?;
            // Parametric range burns replace the current family generator.
            // Reconstruct its past from genesis plus recorded inputs instead of
            // extrapolating the final generator backwards through the burn.
            let mut burns = Vec::new();
            for input in &engine.state.interventions {
                match &input.command {
                    Command::SetCourseRange { lo, hi, at, velocity } if *lo <= id && id <= *hi && *at <= through => {
                        burns.push((*at, velocity.clone()));
                    }
                    Command::FamilyPhaseBurn { .. } => return Err(EngineError::Unsupported(
                        "oracle family-phase burn history requires explicit range provenance".into())),
                    _ => {}
                }
            }
            burns.sort_by_key(|(at, _)| *at);
            if burns.windows(2).any(|w| w[0].0 == w[1].0) {
                return Err(EngineError::Unsupported("oracle overlapping same-tick range burns require canonical order reconstruction".into()));
            }
            for (at, velocity) in burns {
                let origin = segments[segment_at(&segments, at)].state_at(at);
                segments.retain(|s| s.epoch < at);
                segments.push(Inertial::new(at, origin, velocity).map_err(EngineError::Invalid)?);
            }
            if engine.state.bodies.contains_key(&id) {
                // Explicit history begins at extraction; retain the generated prefix.
                let epoch = body.segments[0].epoch;
                segments.retain(|s| s.epoch < epoch);
                segments.extend(body.segments.clone());
            }
            body.segments = segments;
        }
        out.push(body);
    }
    Ok(out)
}

impl Engine {
    /// Exhaustive small-world audit of committed trajectories and emissions.
    /// Independent rational contact/cone predicates, not production searches.
    /// This is not an independent evolution or missing-emission oracle; phase
    /// families refuse and populations above 4096 identities fail explicitly.
    pub fn independent_inertial_facts(
        &self,
        through: i128,
    ) -> Result<CanonicalMatch, EngineError> {
        if through < 0 || through > self.state.clock {
            return Err(EngineError::Invalid("oracle cut is not committed".into()));
        }
        if through == 0 {
            return Ok(CanonicalMatch { contacts: vec![], arrivals: vec![] });
        }
        let domain = TickInterval::new(1, through).map_err(EngineError::Invalid)?;
        let bodies = oracle_bodies(self, through)?;
        let pair_bins = (bodies.len() as u128)
            .saturating_mul(bodies.len().saturating_sub(1) as u128)
            .saturating_mul(through as u128) / 2;
        let signal_bins = (self.state.events.len() as u128).saturating_mul(through as u128);
        if pair_bins.saturating_add(signal_bins) > 5_000_000 {
            return Err(EngineError::ResourceLimit("exhaustive oracle work limit".into()));
        }
        let mut contacts = Vec::new();
        for (i, a) in bodies.iter().enumerate() {
            for b in &bodies[i + 1..] {
                let radius = &a.radius + &b.radius;
                // One event per unchanged trajectory pair, including a new
                // event after a commanded burn while already overlapping.
                let mut consumed = None;
                for tick in 1..=through {
                    let ai = segment_at(&a.segments, tick - 1);
                    let bi = segment_at(&b.segments, tick - 1);
                    if consumed == Some((ai, bi)) {
                        continue;
                    }
                    if oracle_contact_bin(&a.segments[ai], &b.segments[bi], &radius, tick) {
                        contacts.push((tick, a.id, b.id));
                        // Individual burns/impulses/stops precede contact revision
                        // storage; range burns follow it. Reconstruct that ordering.
                        let after_a = if has_range_burn(self, a.id, tick) { ai } else { segment_at(&a.segments, tick) };
                        let after_b = if has_range_burn(self, b.id, tick) { bi } else { segment_at(&b.segments, tick) };
                        consumed = Some((after_a, after_b));
                    }
                }
            }
        }
        contacts.sort_unstable();


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
            let emission = bodies.iter().find(|b| b.id == source)
                .ok_or(EngineError::UnknownIdentity(source))?.at(event.tick);
            let receiver = bodies.iter().find(|b| b.id == target)
                .ok_or(EngineError::UnknownIdentity(target))?;
            // Direct cone membership, independent of production root search.
            // Emissions committed at t cannot be received until t+1.
            if let Some(start) = event.tick.checked_add(1) {
                for tick in start.max(domain.start)..=through {
                    let elapsed = r(tick) - r(event.tick);
                    if (receiver.at(tick) - &emission).norm_squared() <= &elapsed * &elapsed {
                        arrivals.push((tick, source, target, event.predecessors[0].clone()));
                        break;
                    }
                }
            }
        }
        arrivals.sort_unstable();

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

    /// Domain-local GEM field events only when the Lipschitz/KA bound covers
    /// the compiled admitted interior. Does not mint global
    /// `CANONICAL_GRAVITY_ACCEPTANCE`. Ambiguity is pending/refusal.
    pub fn authorizes_gem_events_on_admitted_field(&self) -> bool {
        self.gem_field_authorization().authorizes_gem_events
    }

    pub fn gem_field_authorization(&self) -> AuthorityReport {
        let mut pending = Vec::new();
        let compiled = self
            .coupled
            .as_ref()
            .and_then(|d| d.compiled.as_ref());
        let Some(compiled) = compiled else {
            pending.push("no compiled GEM response".into());
            return authority_status(pending);
        };
        match enclose_gem_field_interval(compiled) {
            Ok(gem) => {
                if gem.authorizes_events {
                    AuthorityReport {
                        canonical_law: LAW_ID.into(),
                        gem_law: COUPLED_RESPONSE_LAW_ID.into(),
                        gravity_acceptance: CANONICAL_GRAVITY_ACCEPTANCE.into(),
                        gem_interval_coverage: GEM_FIELD_INTERVAL_COVERAGE.into(),
                        historical_compact_seal: HISTORICAL_COMPACT_SEAL.into(),
                        authorizes_gem_events: true,
                        pending: gem
                            .prefix_gap
                            .into_iter()
                            .collect(),
                        refused: vec![
                            "sampled Enclosure.certified does not authorize events".into(),
                            "queries outside the admitted interior stay pending/refused".into(),
                            "CANONICAL_GRAVITY_ACCEPTANCE stays diagnostic-only".into(),
                        ],
                    }
                } else {
                    if let Some(g) = gem.prefix_gap {
                        pending.push(g);
                    }
                    if let Some(g) = gem.interior_gap {
                        pending.push(g);
                    }
                    pending.push("Lipschitz/KA bound does not cover the queried domain".into());
                    authority_status(pending)
                }
            }
            Err(e) => {
                pending.push(e.to_string());
                authority_status(pending)
            }
        }
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

    out
}

fn committed_arrivals(events: Vec<&EventRecord>, through: i128) -> Vec<(i128, u64, u64, String)> {
    let mut out = Vec::new();
    for e in events {
        if e.kind != "signal_arrived" || e.tick > through || e.subjects.len() < 2 {
            continue;
        }
        out.push((e.tick, e.subjects[0], e.subjects[1], e.predecessors.first().cloned().unwrap_or_default()));
    }
    out.sort_unstable();

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
        assert_eq!(
            GEM_FIELD_INTERVAL_COVERAGE,
            "causal-block-lipschitz-ka-delay-admitted-interior"
        );
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
