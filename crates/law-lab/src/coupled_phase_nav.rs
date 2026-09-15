//! Compact phase/residual stored response and navigation inversion.
//!
//! Isolated `es-linearized-retarded-gem-response-v0` helpers. Not `production_law`.
//! Not `Engine::advance`. Independent `Reference::from_genesis` is unchanged.
//! Enclosure still does not read compile residual.
//!
//! Regular motion is a polar phase generator (slowly changing r, θ) plus a
//! Chebyshev residual of admitted rank. A single smooth generator on an
//! interval that contains a finite Δv kick is refused when the residual
//! exceeds the admitted band (Gibbs / insufficient basis). Pieces split at
//! committed interventions **and** at causal arrivals of those events so a
//! receiver's pre-cone and post-cone motion are not mixed in one interpolant.
//!
//! `compile_source_response` stores this generator as the compiled interval
//! response. Causal-arrival split keeps a receiver's pre-cone and post-cone
//! motion in separate pieces. That is not enough for 1e-8 prefix identity at
//! the admitted \(10^{-4}\) band: control and kicked interpolants still differ
//! at band scale, and tightening the band to \(10^{-8}\) stores more pieces
//! than the stepper (a polyline, not compact). Worldtubes therefore remain a
//! named stepper remainder; decode fails closed when the generator refuses.
//!
//! Navigation inverts the already compiled ship transport. The focusing
//! identity B=0 at oscillator half-period is an explicit failure domain; this
//! inverter refuses singular STM / empty interval / horizon / unreachable
//! targets rather than inventing a route.

use crate::coupled_source_response::{
    body_state, fly_ship, Body, BodyInit, Charge, InitialCondition, Intervention, ResponseError,
    Segment, SourceResponse, C,
};
use serde::{Deserialize, Serialize};
use std::f64::consts::PI;

pub const ADMITTED_RANK: usize = 16;
pub const ADMITTED_BAND: f64 = 1e-4;
pub const CONSUMER_BAND: f64 = 5e-3;
pub const NAV_MIN_DET: f64 = 1e-8;

#[derive(Clone, Debug)]
pub struct CompactSpec {
    pub max_rank: usize,
    pub band: f64,
    pub split_at_interventions: bool,
    /// Split each body at light-cone arrivals of committed events, not only
    /// at local Δv times. Needed so B's pre-cone piece does not interpolate
    /// post-cone motion. Probe refuses (unsplitted rank-2 kick) keep this false.
    pub split_at_causal_arrivals: bool,
    /// Bisect pieces that exceed `band`. Compile uses this so longer
    /// laboratory intervals can still store a generator. Probe refuses
    /// (unsplitted rank-2 kick) keep this false.
    pub adaptive_bisect: bool,
}

impl Default for CompactSpec {
    fn default() -> Self {
        Self {
            max_rank: ADMITTED_RANK,
            band: ADMITTED_BAND,
            split_at_interventions: true,
            split_at_causal_arrivals: true,
            adaptive_bisect: false,
        }
    }
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct PhaseOrbit {
    pub com: [f64; 2],
    pub r0: f64,
    pub theta0: f64,
    pub omega: f64,
    pub rdot: f64,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct CompactPiece {
    pub id: u64,
    pub mu: f64,
    pub t0: f64,
    pub t1: f64,
    pub orbit: PhaseOrbit,
    pub residual_x: Vec<f64>,
    pub residual_y: Vec<f64>,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct CompactResponse {
    pub law_id: String,
    pub band: f64,
    pub max_error: f64,
    pub pieces: Vec<CompactPiece>,
    pub charge: Charge,
}

#[derive(Clone, Debug)]
pub struct CompactRefuse {
    pub why: String,
    pub max_error: f64,
    pub band: f64,
    pub stored_dof: usize,
    pub worldtube_segments: usize,
}

#[derive(Clone, Copy, Debug)]
pub struct NavigationDomain {
    pub t_min: f64,
    pub t_max: f64,
    pub vmax: f64,
    pub min_det: f64,
    pub max_iters: u32,
    pub tol: f64,
}

impl NavigationDomain {
    pub fn from_compiled(compiled: &SourceResponse) -> Self {
        let t_min = compiled
            .compact
            .pieces
            .iter()
            .map(|p| p.t0)
            .fold(f64::INFINITY, f64::min);
        Self {
            t_min: if t_min.is_finite() {
                t_min
            } else {
                compiled
                    .worldtubes
                    .first()
                    .and_then(|b| b.segments.first())
                    .map(|s| s.t0)
                    .unwrap_or(0.0)
            },
            t_max: compiled.domain.horizon,
            vmax: compiled.domain.beta_max.max(0.25) * C,
            min_det: NAV_MIN_DET,
            max_iters: 8,
            tol: 1e-7,
        }
    }
}

#[derive(Clone, Debug)]
pub struct TransportMap {
    pub t0: f64,
    pub t1: f64,
    pub x0: [f64; 2],
    pub v0: [f64; 2],
    pub x1: [f64; 2],
    pub stm: [[f64; 2]; 2],
    pub det_b: f64,
    pub tau: f64,
}

#[derive(Clone, Debug)]
pub struct NavSolution {
    pub v0: [f64; 2],
    pub arrival: [f64; 2],
    pub transport: TransportMap,
}

#[derive(Clone, Debug)]
pub enum NavError {
    OutsideDomain { why: String },
    SingularFocusing { det: f64, why: String },
    Unreachable { need_speed: f64, vmax: f64 },
    NewtonRefused { residual: f64 },
    Transport(ResponseError),
}

impl std::fmt::Display for NavError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            NavError::OutsideDomain { why } => write!(f, "OutsideDomain: {why}"),
            NavError::SingularFocusing { det, why } => {
                write!(f, "SingularFocusing det={det}: {why}")
            }
            NavError::Unreachable { need_speed, vmax } => {
                write!(f, "Unreachable need_speed={need_speed} vmax={vmax}")
            }
            NavError::NewtonRefused { residual } => write!(f, "NewtonRefused residual={residual}"),
            NavError::Transport(e) => write!(f, "transport: {e}"),
        }
    }
}

/// Weak-field equal-mass circular pair. Period T=2π/ω with ω=1/16; one horizon
/// is a small arc, stored as phase + residual rather than O(H/dt) kinks.
pub fn laboratory_circular_pair() -> InitialCondition {
    let omega = 1.0 / 16.0;
    let r = 4.0;
    let v = omega * r;
    InitialCondition {
        genesis_t: 0.0,
        bodies: vec![
            BodyInit {
                id: 0,
                mu: 1.0,
                x: [-r, 0.0],
                v: [0.0, -v],
            },
            BodyInit {
                id: 1,
                mu: 1.0,
                x: [r, 0.0],
                v: [0.0, v],
            },
        ],
    }
}

fn clenshaw(c: &[f64], u: f64) -> f64 {
    if c.is_empty() {
        return 0.0;
    }
    if c.len() == 1 {
        return c[0];
    }
    let mut b1 = 0.0;
    let mut b2 = 0.0;
    for &cj in c.iter().skip(1).rev() {
        let b0 = cj + 2.0 * u * b1 - b2;
        b2 = b1;
        b1 = b0;
    }
    c[0] + u * b1 - b2
}

fn chebyshev_fit(values: &[f64]) -> Vec<f64> {
    let n = values.len();
    if n == 0 {
        return Vec::new();
    }
    let mut c = vec![0.0; n];
    for j in 0..n {
        let mut s = 0.0;
        for (k, &fk) in values.iter().enumerate() {
            s += fk * (j as f64 * (k as f64 + 0.5) * PI / n as f64).cos();
        }
        c[j] = if j == 0 {
            s / n as f64
        } else {
            2.0 * s / n as f64
        };
    }
    c
}

fn trim_cheb(mut c: Vec<f64>, eps: f64) -> Vec<f64> {
    while c.len() > 1 && c.last().copied().unwrap_or(0.0).abs() < eps {
        c.pop();
    }
    c
}

fn map_u(t: f64, t0: f64, t1: f64) -> f64 {
    if (t1 - t0).abs() < 1e-18 {
        return 0.0;
    }
    (2.0 * (t - t0) / (t1 - t0) - 1.0).clamp(-1.0, 1.0)
}

fn du_dt(t0: f64, t1: f64) -> f64 {
    if (t1 - t0).abs() < 1e-18 {
        0.0
    } else {
        2.0 / (t1 - t0)
    }
}

fn phase_at(orbit: &PhaseOrbit, t: f64, t0: f64) -> ([f64; 2], [f64; 2]) {
    let dt = t - t0;
    let r = (orbit.r0 + orbit.rdot * dt).max(0.0);
    let th = orbit.theta0 + orbit.omega * dt;
    let (s, c) = th.sin_cos();
    let x = [orbit.com[0] + r * c, orbit.com[1] + r * s];
    let vr = orbit.rdot;
    let vth = orbit.omega * r;
    let v = [vr * c - vth * s, vr * s + vth * c];
    (x, v)
}

fn piece_state(piece: &CompactPiece, t: f64) -> ([f64; 2], [f64; 2]) {
    let t = t.clamp(piece.t0, piece.t1);
    let (xr, vr) = phase_at(&piece.orbit, t, piece.t0);
    let u = map_u(t, piece.t0, piece.t1);
    let dudt = du_dt(piece.t0, piece.t1);
    let eps = 1e-8;
    let rx = clenshaw(&piece.residual_x, u);
    let ry = clenshaw(&piece.residual_y, u);
    let drx = (clenshaw(&piece.residual_x, (u + eps).clamp(-1.0, 1.0))
        - clenshaw(&piece.residual_x, (u - eps).clamp(-1.0, 1.0)))
        / (2.0 * eps);
    let dry = (clenshaw(&piece.residual_y, (u + eps).clamp(-1.0, 1.0))
        - clenshaw(&piece.residual_y, (u - eps).clamp(-1.0, 1.0)))
        / (2.0 * eps);
    (
        [xr[0] + rx, xr[1] + ry],
        [vr[0] + drx * dudt, vr[1] + dry * dudt],
    )
}

impl CompactResponse {
    pub fn stored_dof(&self) -> usize {
        self.pieces
            .iter()
            .map(|p| 8 + p.residual_x.len() + p.residual_y.len())
            .sum()
    }

    pub fn state(&self, id: u64, t: f64) -> Result<([f64; 2], [f64; 2]), ResponseError> {
        let piece = self
            .pieces
            .iter()
            .rev()
            .find(|p| p.id == id && t + 1e-15 >= p.t0 && t <= p.t1 + 1e-15)
            .ok_or(ResponseError::UnsupportedDomain {
                why: format!("compact body {id} has no piece at t={t}"),
            })?;
        Ok(piece_state(piece, t))
    }

    /// Decode compact generators onto inertial segments for existing consumers.
    /// `template` supplies identity, μ and sample times only; positions and
    /// velocities come from the generator. Paid reconstruction.
    pub fn decode_from_template(
        &self,
        template: &[Body],
        charge: &mut Charge,
    ) -> Result<Vec<Body>, ResponseError> {
        let mut out = Vec::new();
        for body in template {
            let times: Vec<f64> = body.segments.iter().map(|s| s.t0).collect();
            let mu = body.segments.first().map(|s| s.mu).unwrap_or(0.0);
            let mut segs = Vec::new();
            for w in times.windows(2) {
                let t0 = w[0];
                let t1 = w[1];
                let (x, v) = self.state(body.id, t0)?;
                segs.push(Segment {
                    t0,
                    t1: Some(t1),
                    x0: x,
                    v,
                    a: [0.0, 0.0],
                    mu,
                });
                charge.reconstruction += 1;
            }
            if let Some(&t_last) = times.last() {
                let (x, v) = self.state(body.id, t_last)?;
                segs.push(Segment {
                    t0: t_last,
                    t1: None,
                    x0: x,
                    v,
                    a: [0.0, 0.0],
                    mu,
                });
                charge.reconstruction += 1;
            }
            out.push(Body {
                id: body.id,
                segments: segs,
            });
        }
        Ok(out)
    }

    /// Decode compact generators onto inertial segments for existing consumers.
    /// Paid reconstruction; the stored form remains the phase + residual.
    pub fn reconstruct_worldtubes(
        &self,
        compiled: &SourceResponse,
        charge: &mut Charge,
    ) -> Result<Vec<Body>, ResponseError> {
        self.decode_from_template(&compiled.worldtubes, charge)
    }
}

fn push_knot(ts: &mut Vec<f64>, t: f64, t0: f64, horizon: f64) {
    if t > t0 + 1e-12 && t < horizon - 1e-12 {
        ts.push(t);
    }
}

fn light_arrival_on_segment(
    seg: &Segment,
    t_lo: f64,
    t_hi: f64,
    t_ev: f64,
    x_ev: [f64; 2],
) -> Option<f64> {
    let v = seg.v;
    let x_lin = [
        seg.x0[0] + v[0] * (t_ev - seg.t0) - x_ev[0],
        seg.x0[1] + v[1] * (t_ev - seg.t0) - x_ev[1],
    ];
    let a = v[0] * v[0] + v[1] * v[1] - C * C;
    let b = 2.0 * (x_lin[0] * v[0] + x_lin[1] * v[1]);
    let c0 = x_lin[0] * x_lin[0] + x_lin[1] * x_lin[1];
    let in_range =
        |t: f64| t.is_finite() && t + 1e-12 >= t_lo && t <= t_hi + 1e-12 && t + 1e-12 >= t_ev;
    let mut best: Option<f64> = None;
    let mut consider = |t: f64| {
        if in_range(t) {
            best = Some(best.map_or(t, |b| b.min(t)));
        }
    };
    if a.abs() < 1e-18 {
        if c0 <= 0.0 {
            consider(t_ev.max(t_lo));
        } else {
            consider(t_ev + c0.sqrt() / C);
        }
        return best;
    }
    let disc = b * b - 4.0 * a * c0;
    if disc < 0.0 {
        return None;
    }
    let s = disc.sqrt();
    consider(t_ev + (-b - s) / (2.0 * a));
    consider(t_ev + (-b + s) / (2.0 * a));
    best
}

fn light_arrival(observer: &Body, t_ev: f64, x_ev: [f64; 2]) -> Option<f64> {
    let mut best: Option<f64> = None;
    for seg in &observer.segments {
        let t_lo = seg.t0.max(t_ev);
        let t_hi = seg.t1.unwrap_or(f64::INFINITY);
        if t_hi <= t_lo + 1e-15 {
            continue;
        }
        if let Some(t) = light_arrival_on_segment(seg, t_lo, t_hi, t_ev, x_ev) {
            best = Some(best.map_or(t, |b| b.min(t)));
        }
    }
    best
}

/// Local interventions plus iterated light-cone arrivals of those events.
/// Each body keeps its own knots so a receiver is not split at a distant
/// kick time that has not yet arrived.
fn knots_for_body(
    id: u64,
    t0: f64,
    horizon: f64,
    incoming: &[Intervention],
    worldtubes: &[Body],
    spec: &CompactSpec,
) -> Vec<f64> {
    let mut ts = vec![t0, horizon];
    if spec.split_at_interventions && !spec.split_at_causal_arrivals {
        for iv in incoming {
            push_knot(&mut ts, iv.t, t0, horizon);
        }
    }
    if spec.split_at_interventions && spec.split_at_causal_arrivals {
        for iv in incoming {
            if iv.body_id == id {
                push_knot(&mut ts, iv.t, t0, horizon);
            }
        }
    }
    if spec.split_at_causal_arrivals {
        #[derive(Clone, Copy)]
        struct CausalEvent {
            body_id: u64,
            t: f64,
            x: [f64; 2],
        }
        let mut events: Vec<CausalEvent> = Vec::new();
        for iv in incoming {
            if let Ok((x, _)) = body_state(worldtubes, iv.body_id, iv.t) {
                events.push(CausalEvent {
                    body_id: iv.body_id,
                    t: iv.t,
                    x,
                });
            }
        }
        let mut i = 0;
        while i < events.len() && i < 64 {
            let ev = events[i];
            for observer in worldtubes {
                if observer.id == ev.body_id {
                    continue;
                }
                let Some(t_arr) = light_arrival(observer, ev.t, ev.x) else {
                    continue;
                };
                if (t_arr - ev.t).abs() < 1e-12 {
                    continue;
                }
                if observer.id == id {
                    push_knot(&mut ts, t_arr, t0, horizon);
                }
                if let Ok((x, _)) = body_state(worldtubes, observer.id, t_arr) {
                    let dup = events
                        .iter()
                        .any(|e| e.body_id == observer.id && (e.t - t_arr).abs() < 1e-12);
                    if !dup && t_arr > t0 + 1e-12 && t_arr < horizon - 1e-12 {
                        events.push(CausalEvent {
                            body_id: observer.id,
                            t: t_arr,
                            x,
                        });
                    }
                }
            }
            i += 1;
        }
    }
    ts.sort_by(|a, b| a.partial_cmp(b).unwrap());
    ts.dedup_by(|a, b| (*a - *b).abs() < 1e-12);
    // Split at interval-operator knots so a Chebyshev piece does not mix
    // two causal blocks of the compiled interval function.
    if let Some(body) = worldtubes.iter().find(|b| b.id == id) {
        for seg in &body.segments {
            push_knot(&mut ts, seg.t0, t0, horizon);
            if let Some(t1) = seg.t1 {
                push_knot(&mut ts, t1, t0, horizon);
            }
        }
    }
    ts.sort_by(|a, b| a.partial_cmp(b).unwrap());
    ts.dedup_by(|a, b| (*a - *b).abs() < 1e-12);
    ts
}

fn mass_com(worldtubes: &[Body], t: f64) -> Result<([f64; 2], [f64; 2]), ResponseError> {
    let mut m = 0.0;
    let mut x = [0.0, 0.0];
    let mut v = [0.0, 0.0];
    for body in worldtubes {
        let mu = body.segments.first().map(|s| s.mu).unwrap_or(0.0);
        let (xi, vi) = body_state(worldtubes, body.id, t)?;
        m += mu;
        x[0] += mu * xi[0];
        x[1] += mu * xi[1];
        v[0] += mu * vi[0];
        v[1] += mu * vi[1];
    }
    if m < 1e-18 {
        return Ok((x, v));
    }
    Ok(([x[0] / m, x[1] / m], [v[0] / m, v[1] / m]))
}

fn fit_piece(
    worldtubes: &[Body],
    id: u64,
    mu: f64,
    t0: f64,
    t1: f64,
    rank: usize,
    charge: &mut Charge,
) -> Result<CompactPiece, ResponseError> {
    let (com, vcom) = mass_com(worldtubes, t0)?;
    let (x0, v0) = body_state(worldtubes, id, t0)?;
    let rho = [x0[0] - com[0], x0[1] - com[1]];
    let r0 = (rho[0] * rho[0] + rho[1] * rho[1]).sqrt();
    let theta0 = if r0 < 1e-12 {
        0.0
    } else {
        rho[1].atan2(rho[0])
    };
    let vrel = [v0[0] - vcom[0], v0[1] - vcom[1]];
    let (rdot, omega) = if r0 < 1e-12 {
        (0.0, 0.0)
    } else {
        let rhat = [rho[0] / r0, rho[1] / r0];
        let rdot = vrel[0] * rhat[0] + vrel[1] * rhat[1];
        let omega = (rho[0] * vrel[1] - rho[1] * vrel[0]) / (r0 * r0);
        (rdot, omega)
    };
    let orbit = PhaseOrbit {
        com,
        r0,
        theta0,
        omega,
        rdot,
    };
    let n = rank.max(1);
    let mut fx = vec![0.0; n];
    let mut fy = vec![0.0; n];
    for k in 0..n {
        let u = ((k as f64 + 0.5) * PI / n as f64).cos();
        let t = t0 + (u + 1.0) * 0.5 * (t1 - t0);
        let (x, _) = body_state(worldtubes, id, t)?;
        let (xr, _) = phase_at(&orbit, t, t0);
        fx[k] = x[0] - xr[0];
        fy[k] = x[1] - xr[1];
        charge.coefficient_construction += 1;
    }
    charge.factorization += 1;
    Ok(CompactPiece {
        id,
        mu,
        t0,
        t1,
        orbit,
        residual_x: trim_cheb(chebyshev_fit(&fx), 1e-12),
        residual_y: trim_cheb(chebyshev_fit(&fy), 1e-12),
    })
}

fn worldtube_segments(worldtubes: &[Body]) -> usize {
    worldtubes.iter().map(|b| b.segments.len()).sum()
}

fn interval_error(piece: &CompactPiece, worldtubes: &[Body]) -> f64 {
    let mut max_error = 0.0_f64;
    for i in 0..24 {
        let t = piece.t0 + (i as f64) * (piece.t1 - piece.t0) / 23.0;
        let (xc, _) = piece_state(piece, t);
        if let Ok((xw, _)) = body_state(worldtubes, piece.id, t) {
            let dx = xc[0] - xw[0];
            let dy = xc[1] - xw[1];
            max_error = max_error.max((dx * dx + dy * dy).sqrt());
        }
    }
    max_error
}

fn fit_interval(
    worldtubes: &[Body],
    id: u64,
    mu: f64,
    t0: f64,
    t1: f64,
    spec: &CompactSpec,
    charge: &mut Charge,
    depth: u32,
) -> Result<Vec<CompactPiece>, CompactRefuse> {
    let piece = match fit_piece(worldtubes, id, mu, t0, t1, spec.max_rank, charge) {
        Ok(p) => p,
        Err(e) => {
            return Err(CompactRefuse {
                why: format!("fit failed: {e}"),
                max_error: f64::INFINITY,
                band: spec.band,
                stored_dof: 0,
                worldtube_segments: worldtube_segments(worldtubes),
            });
        }
    };
    let err = interval_error(&piece, worldtubes);
    if err <= spec.band {
        return Ok(vec![piece]);
    }
    if spec.adaptive_bisect && depth < 12 && (t1 - t0) > 1e-3 {
        let mid = 0.5 * (t0 + t1);
        let mut left = fit_interval(worldtubes, id, mu, t0, mid, spec, charge, depth + 1)?;
        let mut right = fit_interval(worldtubes, id, mu, mid, t1, spec, charge, depth + 1)?;
        left.append(&mut right);
        return Ok(left);
    }
    if spec.adaptive_bisect {
        return Err(CompactRefuse {
            why: format!(
                "adaptive bisect exhausted at depth {depth} residual {err} exceeds band {}; split_at_interventions={} split_at_causal_arrivals={}",
                spec.band, spec.split_at_interventions, spec.split_at_causal_arrivals
            ),
            max_error: err,
            band: spec.band,
            stored_dof: 0,
            worldtube_segments: worldtube_segments(worldtubes),
        });
    }
    Ok(vec![piece])
}

/// Fit a compact stored response from jointly evolved bodies. Refuses when
/// the admitted basis cannot reconstruct those bodies inside `spec.band`.
pub fn compact_from_bodies(
    law_id: &str,
    horizon: f64,
    incoming: &[Intervention],
    worldtubes: &[Body],
    spec: CompactSpec,
) -> Result<CompactResponse, CompactRefuse> {
    let mut charge = Charge {
        init: 1,
        ..Charge::default()
    };
    let t0 = worldtubes
        .first()
        .and_then(|b| b.segments.first())
        .map(|s| s.t0)
        .unwrap_or(0.0);
    let mut pieces = Vec::new();
    for body in worldtubes {
        let mu = body.segments.first().map(|s| s.mu).unwrap_or(0.0);
        let ts = knots_for_body(body.id, t0, horizon, incoming, worldtubes, &spec);
        for w in ts.windows(2) {
            pieces.extend(fit_interval(
                worldtubes,
                body.id,
                mu,
                w[0],
                w[1],
                &spec,
                &mut charge,
                0,
            )?);
        }
    }
    let compact = CompactResponse {
        law_id: law_id.into(),
        band: spec.band,
        max_error: 0.0,
        pieces,
        charge,
    };
    let mut max_error = 0.0_f64;
    for piece in &compact.pieces {
        max_error = max_error.max(interval_error(piece, worldtubes));
    }
    if max_error > spec.band || !max_error.is_finite() {
        return Err(CompactRefuse {
            why: format!(
                "admitted rank {} residual {max_error} exceeds band {}; split_at_interventions={} split_at_causal_arrivals={}",
                spec.max_rank, spec.band, spec.split_at_interventions, spec.split_at_causal_arrivals
            ),
            max_error,
            band: spec.band,
            stored_dof: compact.stored_dof(),
            worldtube_segments: worldtube_segments(worldtubes),
        });
    }
    Ok(CompactResponse {
        max_error,
        ..compact
    })
}

/// Fit a compact stored response. Refuses when the admitted basis cannot
/// reconstruct compiled worldtubes inside `spec.band`.
pub fn compact_source_response(
    compiled: &SourceResponse,
    spec: CompactSpec,
) -> Result<CompactResponse, CompactRefuse> {
    compact_from_bodies(
        &compiled.law_id,
        compiled.domain.horizon,
        &compiled.incoming,
        &compiled.worldtubes,
        spec,
    )
}

fn det2(m: [[f64; 2]; 2]) -> f64 {
    m[0][0] * m[1][1] - m[0][1] * m[1][0]
}

fn inv_apply(m: [[f64; 2]; 2], b: [f64; 2]) -> Option<[f64; 2]> {
    let d = det2(m);
    if !d.is_finite() || d.abs() < NAV_MIN_DET {
        return None;
    }
    Some([
        (m[1][1] * b[0] - m[0][1] * b[1]) / d,
        (-m[1][0] * b[0] + m[0][0] * b[1]) / d,
    ])
}

fn vnorm(v: [f64; 2]) -> f64 {
    (v[0] * v[0] + v[1] * v[1]).sqrt()
}

fn sub2(a: [f64; 2], b: [f64; 2]) -> [f64; 2] {
    [a[0] - b[0], a[1] - b[1]]
}

/// Forward ship transport and ∂x₁/∂v₀ from the compiled GEM sources.
pub fn compile_ship_transport(
    sources: &[Body],
    t0: f64,
    x0: [f64; 2],
    v0: [f64; 2],
    t1: f64,
    dt: f64,
    charge: &mut Charge,
) -> Result<TransportMap, ResponseError> {
    let ship = fly_ship(sources, t0, x0, v0, t1, dt, charge)?;
    let eps = 1e-6;
    let mut stm = [[0.0; 2]; 2];
    for k in 0..2 {
        let mut vp = v0;
        let mut vm = v0;
        vp[k] += eps;
        vm[k] -= eps;
        let sp = fly_ship(sources, t0, x0, vp, t1, dt, charge)?;
        let sm = fly_ship(sources, t0, x0, vm, t1, dt, charge)?;
        stm[0][k] = (sp.x[0] - sm.x[0]) / (2.0 * eps);
        stm[1][k] = (sp.x[1] - sm.x[1]) / (2.0 * eps);
    }
    Ok(TransportMap {
        t0,
        t1,
        x0,
        v0,
        x1: ship.x,
        stm,
        det_b: det2(stm),
        tau: ship.tau,
    })
}

/// Invert arrival using compiled transport sensitivities. Fails closed outside
/// `domain`. Does not search seeds for a lucky success.
pub fn invert_arrival(
    sources: &[Body],
    t0: f64,
    x0: [f64; 2],
    t1: f64,
    x_target: [f64; 2],
    dt: f64,
    domain: NavigationDomain,
    charge: &mut Charge,
) -> Result<NavSolution, NavError> {
    if t1 <= t0 + 1e-15 {
        return Err(NavError::SingularFocusing {
            det: 0.0,
            why: "empty interval; B=0 as in the oscillator half-period identity".into(),
        });
    }
    if t0 < domain.t_min - 1e-12 || t1 > domain.t_max + 1e-12 {
        return Err(NavError::OutsideDomain {
            why: format!(
                "[{t0},{t1}] not inside compiled [{},{}]",
                domain.t_min, domain.t_max
            ),
        });
    }
    let dt_int = t1 - t0;
    let need = vnorm(sub2(x_target, x0)) / dt_int;
    if need > domain.vmax * 4.0 {
        return Err(NavError::Unreachable {
            need_speed: need,
            vmax: domain.vmax,
        });
    }
    let mut v = [
        (x_target[0] - x0[0]) / dt_int,
        (x_target[1] - x0[1]) / dt_int,
    ];
    let mut last_res = f64::INFINITY;
    for _ in 0..domain.max_iters {
        if vnorm(v) >= domain.vmax {
            return Err(NavError::Unreachable {
                need_speed: vnorm(v),
                vmax: domain.vmax,
            });
        }
        let map = compile_ship_transport(sources, t0, x0, v, t1, dt, charge)
            .map_err(NavError::Transport)?;
        if map.det_b.abs() < domain.min_det {
            return Err(NavError::SingularFocusing {
                det: map.det_b,
                why: "STM B is singular; inverse is nonunique (focusing)".into(),
            });
        }
        let err = sub2(map.x1, x_target);
        last_res = vnorm(err);
        if last_res <= domain.tol {
            return Ok(NavSolution {
                v0: v,
                arrival: map.x1,
                transport: map,
            });
        }
        let Some(dv) = inv_apply(map.stm, err) else {
            return Err(NavError::SingularFocusing {
                det: map.det_b,
                why: "STM B cannot be inverted".into(),
            });
        };
        v = [v[0] - dv[0], v[1] - dv[1]];
    }
    Err(NavError::NewtonRefused { residual: last_res })
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::coupled_source_response::{
        acceleration_at, clock_rate, compile_source_response, fly_ray, laboratory_kick,
        laboratory_two_body, Reference,
    };

    fn a_scale() -> f64 {
        1.0 / 64.0
    }

    #[test]
    fn chebyshev_reproduces_quadratic() {
        let n = 8;
        let mut f = vec![0.0; n];
        for k in 0..n {
            let u = ((k as f64 + 0.5) * PI / n as f64).cos();
            f[k] = 1.0 + 2.0 * u + 3.0 * u * u;
        }
        let c = chebyshev_fit(&f);
        for k in 0..n {
            let u = ((k as f64 + 0.5) * PI / n as f64).cos();
            let got = clenshaw(&c, u);
            assert!((got - (1.0 + 2.0 * u + 3.0 * u * u)).abs() < 1e-12);
        }
    }

    #[test]
    fn compact_quiet_and_circular_reconstruct_or_refuse() {
        let quiet =
            compile_source_response(laboratory_two_body(), Vec::new(), 4.0, 1.0 / 32.0).unwrap();
        let compact = compact_source_response(&quiet, CompactSpec::default()).unwrap();
        let euler = Reference::from_genesis(laboratory_two_body(), Vec::new(), 1.0 / 32.0)
            .evolve_to(4.0)
            .unwrap()
            .0;
        assert!(
            worldtube_segments(&quiet.worldtubes) < worldtube_segments(&euler),
            "interval compile must be coarser than Euler-dt evolve"
        );
        assert!(compact.max_error <= compact.band);
        let (xw, _) = body_state(&quiet.worldtubes, 0, 3.5).unwrap();
        let (xc, _) = compact.state(0, 3.5).unwrap();
        let d = ((xc[0] - xw[0]).powi(2) + (xc[1] - xw[1]).powi(2)).sqrt();
        assert!(d <= ADMITTED_BAND, "quiet reconstruct d={d}");

        let circ =
            compile_source_response(laboratory_circular_pair(), Vec::new(), 6.0, 1.0 / 24.0)
                .unwrap();
        match compact_source_response(&circ, CompactSpec::default()) {
            Ok(c) => {
                let euler = Reference::from_genesis(laboratory_circular_pair(), Vec::new(), 1.0 / 24.0)
                    .evolve_to(6.0)
                    .unwrap()
                    .0;
                assert!(
                    worldtube_segments(&circ.worldtubes) < worldtube_segments(&euler),
                    "interval compile must be coarser than Euler-dt evolve"
                );
                assert!(c.max_error <= c.band);
                let (xw, _) = body_state(&circ.worldtubes, 0, 5.0).unwrap();
                let (xc, _) = c.state(0, 5.0).unwrap();
                let d = ((xc[0] - xw[0]).powi(2) + (xc[1] - xw[1]).powi(2)).sqrt();
                assert!(d <= ADMITTED_BAND, "circular reconstruct d={d}");
            }
            Err(refuse) => {
                assert!(
                    refuse.max_error > refuse.band,
                    "refuse must be honest: error {} vs band {}",
                    refuse.max_error,
                    refuse.band
                );
            }
        }
    }

    #[test]
    fn compact_kicked_aba_or_honest_refuse() {
        let control =
            compile_source_response(laboratory_two_body(), Vec::new(), 5.0, 1.0 / 32.0).unwrap();
        let kicked = compile_source_response(
            laboratory_two_body(),
            laboratory_kick(),
            5.0,
            1.0 / 32.0,
        )
        .unwrap();
        let spec = CompactSpec::default();
        let compact = match compact_source_response(&kicked, spec) {
            Ok(c) => c,
            Err(refuse) => {
                assert!(refuse.max_error > refuse.band);
                return;
            }
        };
        let euler = Reference::from_genesis(laboratory_two_body(), laboratory_kick(), 1.0 / 32.0)
            .evolve_to(5.0)
            .unwrap()
            .0;
        assert!(
            worldtube_segments(&kicked.worldtubes) < worldtube_segments(&euler),
            "interval compile must be coarser than Euler-dt evolve"
        );
        assert!(compact.max_error <= compact.band);

        let mut c0 = Charge::default();
        let reconstructed = compact.reconstruct_worldtubes(&kicked, &mut c0).unwrap();
        assert!(c0.reconstruction > 0);

        let t_pre = 2.0;
        let a_b_pre_c = acceleration_at(&control.worldtubes, 1, t_pre, &mut c0).unwrap();
        let a_b_pre_k = acceleration_at(&reconstructed, 1, t_pre, &mut c0).unwrap();
        let pre = ((a_b_pre_c[0] - a_b_pre_k[0]).powi(2) + (a_b_pre_c[1] - a_b_pre_k[1]).powi(2))
            .sqrt()
            / a_scale();
        assert!(pre < 1e-2, "pre-cone B must match control on compact, ratio={pre}");

        let t_post = 2.45;
        let a_b_post_c = acceleration_at(&control.worldtubes, 1, t_post, &mut c0).unwrap();
        let a_b_post_k = acceleration_at(&reconstructed, 1, t_post, &mut c0).unwrap();
        let post = ((a_b_post_c[0] - a_b_post_k[0]).powi(2) + (a_b_post_c[1] - a_b_post_k[1]).powi(2))
            .sqrt()
            / a_scale();
        assert!(post > 1e-3, "post-cone B must change on compact, ratio={post}");

        let t_back = 3.5;
        let a_a_c = acceleration_at(&control.worldtubes, 0, t_back, &mut c0).unwrap();
        let a_a_k = acceleration_at(&reconstructed, 0, t_back, &mut c0).unwrap();
        let back = ((a_a_c[0] - a_a_k[0]).powi(2) + (a_a_c[1] - a_a_k[1]).powi(2)).sqrt() / a_scale();
        assert!(back > 1e-3, "A must feel compact B feedback, ratio={back}");

        let ship_w = fly_ship(
            &kicked.worldtubes,
            1.1,
            [0.0, 3.0],
            [0.125, 0.0],
            3.5,
            1.0 / 32.0,
            &mut c0,
        )
        .unwrap();
        let ship_c = fly_ship(
            &reconstructed,
            1.1,
            [0.0, 3.0],
            [0.125, 0.0],
            3.5,
            1.0 / 32.0,
            &mut c0,
        )
        .unwrap();
        let sd = ((ship_w.x[0] - ship_c.x[0]).powi(2) + (ship_w.x[1] - ship_c.x[1]).powi(2)).sqrt();
        assert!(sd < CONSUMER_BAND, "held-out ship d={sd}");
        let ray_w = fly_ray(
            &kicked.worldtubes,
            1.1,
            [0.0, 3.0],
            [1.0, 0.0],
            8.0,
            0.05,
            &mut c0,
        )
        .unwrap();
        let ray_c = fly_ray(&reconstructed, 1.1, [0.0, 3.0], [1.0, 0.0], 8.0, 0.05, &mut c0)
            .unwrap();
        assert!((ray_w.t - ray_c.t).abs() < CONSUMER_BAND, "held-out ray");
        let rate_w = clock_rate(&kicked.worldtubes, ship_w.t, ship_w.x, ship_w.v, &mut c0).unwrap();
        let rate_c = clock_rate(&reconstructed, ship_c.t, ship_c.x, ship_c.v, &mut c0).unwrap();
        assert!((rate_w - rate_c).abs() < CONSUMER_BAND);
        assert!(
            ship_w.tau > 0.0 && rate_w > 0.0,
            "required consumers still return values"
        );
    }

    #[test]
    fn compact_unsplitted_kick_refuses_small_basis() {
        let kicked = compile_source_response(
            laboratory_two_body(),
            laboratory_kick(),
            5.0,
            1.0 / 32.0,
        )
        .unwrap();
        let spec = CompactSpec {
            max_rank: 2,
            band: 1e-5,
            split_at_interventions: false,
            split_at_causal_arrivals: false,
            adaptive_bisect: false,
        };
        let refuse = compact_source_response(&kicked, spec).expect_err(
            "one smooth generator of rank 2 cannot represent a Δv kink inside the band",
        );
        assert!(refuse.max_error > refuse.band);
        assert!(refuse.why.contains("split_at_interventions=false"));
    }

    #[test]
    fn compile_stores_generator_not_independent_worldtubes() {
        let compiled = compile_source_response(
            laboratory_two_body(),
            laboratory_kick(),
            5.0,
            1.0 / 32.0,
        )
        .unwrap();
        assert!(
            !compiled.compact.pieces.is_empty(),
            "compile storage must be the compact generator"
        );
        assert!(compiled.charge.reconstruction > 0);
        assert!(compiled.charge.coefficient_construction > 0);

        let mut charge = Charge::default();
        let decoded = compiled.decode_sources(&mut charge).unwrap();
        assert!(charge.reconstruction > 0);

        let t = 3.5;
        let (xg, _) = compiled.compact.state(0, t).unwrap();
        let (xd, _) = body_state(&decoded, 0, t).unwrap();
        let (xw, _) = body_state(&compiled.worldtubes, 0, t).unwrap();
        let d_view = ((xg[0] - xw[0]).powi(2) + (xg[1] - xw[1]).powi(2)).sqrt();
        let d_dec = ((xd[0] - xw[0]).powi(2) + (xd[1] - xw[1]).powi(2)).sqrt();
        assert!(
            d_view <= ADMITTED_BAND,
            "sidecar must lie in the generator band vs interval worldtubes, d={d_view}"
        );
        assert!(
            d_dec <= ADMITTED_BAND,
            "inertial decode of interval knots must follow compile worldtubes, d={d_dec}"
        );

        let mut diverged = compiled.clone();
        let t_knot = diverged.worldtubes[0].segments[0].t0;
        diverged.worldtubes[0].segments[0].x0[0] += 10.0;
        let (xw_bad, _) = body_state(&diverged.worldtubes, 0, t_knot).unwrap();
        let (xg_still, _) = diverged.compact.state(0, t_knot).unwrap();
        assert!(
            (xw_bad[0] - xg_still[0]).abs() > 1.0,
            "a second worldtube table can diverge; generator must remain truth"
        );
        let restored = diverged.decode_sources(&mut charge).unwrap();
        let (xr, _) = body_state(&restored, 0, t).unwrap();
        let d_rest = ((xr[0] - xg[0]).powi(2) + (xr[1] - xg[1]).powi(2)).sqrt();
        assert!(
            d_rest <= ADMITTED_BAND,
            "reconstruction from stored compact must restore generator, d={d_rest}"
        );

        let ship = fly_ship(&restored, 1.1, [0.0, 3.0], [0.125, 0.0], 3.5, 1.0 / 32.0, &mut charge)
            .unwrap();
        let ray = fly_ray(&restored, 1.1, [0.0, 3.0], [1.0, 0.0], 8.0, 0.05, &mut charge).unwrap();
        let rate = clock_rate(&restored, ship.t, ship.x, ship.v, &mut charge).unwrap();
        assert!(ship.tau > 0.0 && ray.t > 1.1 && rate > 0.0);
    }

    #[test]
    fn independent_reference_untouched_and_enclosure_unread() {
        let ic = laboratory_two_body();
        let kicks = laboratory_kick();
        let reference = Reference::from_genesis(ic.clone(), kicks.clone(), 1.0 / 128.0);
        let compiled = compile_source_response(ic, kicks, 4.0, 1.0 / 32.0).unwrap();
        let _ = compact_source_response(&compiled, CompactSpec::default());
        let (ref_bodies, _) = reference.evolve_to(4.0).unwrap();
        let (xr, _) = body_state(&ref_bodies, 0, 4.0).unwrap();
        let mut rec = Charge::default();
        let sources = compiled.decode_sources(&mut rec).unwrap();
        let (xc, _) = body_state(&sources, 0, 4.0).unwrap();
        let err = ((xc[0] - xr[0]).powi(2) + (xc[1] - xr[1]).powi(2)).sqrt();
        assert!(err < 0.05 * 8.0);
        assert!(
            compiled.residual.max_grad_rel.is_finite(),
            "compile residual still exists; compact/nav must not be the enclosure"
        );
    }

    #[test]
    fn navigation_reuses_transport_and_recovers_forward_v0() {
        let compiled = compile_source_response(
            laboratory_two_body(),
            laboratory_kick(),
            5.0,
            1.0 / 32.0,
        )
        .unwrap();
        let domain = NavigationDomain::from_compiled(&compiled);
        let mut charge = Charge::default();
        let sources = compiled.decode_sources(&mut charge).unwrap();
        let t0 = 1.1;
        let t1 = 3.2;
        let x0 = [0.0, 3.0];
        let v0 = [0.125, 0.0];
        let forward = fly_ship(&sources, t0, x0, v0, t1, 1.0 / 32.0, &mut charge)
            .unwrap();
        let inv = invert_arrival(
            &sources,
            t0,
            x0,
            t1,
            forward.x,
            1.0 / 32.0,
            domain,
            &mut charge,
        )
        .expect("forward image must invert on this weak-field slice");
        let dv = ((inv.v0[0] - v0[0]).powi(2) + (inv.v0[1] - v0[1]).powi(2)).sqrt();
        assert!(dv < 5e-3, "recovered v0 off by {dv}");
        assert!(inv.transport.det_b.abs() >= NAV_MIN_DET);
        assert!(charge.consumers > 0, "inversion charged existing transport");
    }

    #[test]
    fn navigation_fails_closed_outside_explicit_domain() {
        let compiled =
            compile_source_response(laboratory_two_body(), Vec::new(), 4.0, 1.0 / 32.0).unwrap();
        let domain = NavigationDomain::from_compiled(&compiled);
        let mut charge = Charge::default();
        let sources = compiled.decode_sources(&mut charge).unwrap();
        let x0 = [0.0, 3.0];

        match invert_arrival(
            &sources,
            1.0,
            x0,
            1.0,
            [0.1, 3.0],
            1.0 / 32.0,
            domain,
            &mut charge,
        ) {
            Err(NavError::SingularFocusing { .. }) => {}
            other => panic!("empty interval must be focusing/B=0, got {other:?}"),
        }

        match invert_arrival(
            &sources,
            1.0,
            x0,
            9.0,
            [0.1, 3.0],
            1.0 / 32.0,
            domain,
            &mut charge,
        ) {
            Err(NavError::OutsideDomain { .. }) => {}
            other => panic!("past compiled horizon must fail closed, got {other:?}"),
        }

        match invert_arrival(
            &sources,
            1.0,
            x0,
            2.0,
            [80.0, 3.0],
            1.0 / 32.0,
            domain,
            &mut charge,
        ) {
            Err(NavError::Unreachable { .. }) => {}
            other => panic!("far target must be unreachable, got {other:?}"),
        }
    }

    #[test]
    fn decode_precone_identity_after_causal_arrival_split() {
        let control =
            compile_source_response(laboratory_two_body(), Vec::new(), 5.0, 1.0 / 32.0).unwrap();
        let kicked = compile_source_response(
            laboratory_two_body(),
            laboratory_kick(),
            5.0,
            1.0 / 32.0,
        )
        .unwrap();
        assert!(
            !kicked.compact.pieces.is_empty(),
            "kicked A→B→A must store a generator"
        );

        let t_pre = 2.0;
        let t_post = 2.45;
        let b_bounds: Vec<(f64, f64)> = kicked
            .compact
            .pieces
            .iter()
            .filter(|p| p.id == 1)
            .map(|p| (p.t0, p.t1))
            .collect();
        assert!(
            b_bounds
                .iter()
                .any(|&(t0, t1)| (t0 - 2.25).abs() < 0.2 || (t1 - 2.25).abs() < 0.2),
            "B must split near causal arrival of A's kick, pieces={b_bounds:?}"
        );
        assert!(
            b_bounds
                .iter()
                .all(|&(t0, t1)| !(t0 < t_pre - 1e-9 && t1 > t_post + 1e-9)),
            "B must not mix pre-cone t=2.0 and post-cone t=2.45 in one piece, pieces={b_bounds:?}"
        );

        let mut c0 = Charge::default();
        let mut c1 = Charge::default();
        let a_step_c = acceleration_at(&control.worldtubes, 1, t_pre, &mut c0).unwrap();
        let a_step_k = acceleration_at(&kicked.worldtubes, 1, t_pre, &mut c1).unwrap();
        let stepper_pre = ((a_step_c[0] - a_step_k[0]).powi(2) + (a_step_c[1] - a_step_k[1]).powi(2))
            .sqrt()
            / a_scale();
        assert!(
            stepper_pre < 1e-8,
            "interval worldtubes must keep pre-cone identity, ratio={stepper_pre}"
        );

        let control_d = control.decode_sources(&mut c0).unwrap();
        let kicked_d = kicked.decode_sources(&mut c1).unwrap();
        let a_b_pre_c = acceleration_at(&control_d, 1, t_pre, &mut c0).unwrap();
        let a_b_pre_k = acceleration_at(&kicked_d, 1, t_pre, &mut c1).unwrap();
        let pre = ((a_b_pre_c[0] - a_b_pre_k[0]).powi(2) + (a_b_pre_c[1] - a_b_pre_k[1]).powi(2))
            .sqrt()
            / a_scale();
        assert!(
            pre < 1e-8,
            "interval-block decode must keep 1e-8 pre-cone identity (not the evolve-Chebyshev miss), ratio={pre}"
        );

        let tight = CompactSpec {
            max_rank: ADMITTED_RANK,
            band: 1e-8,
            split_at_interventions: true,
            split_at_causal_arrivals: true,
            adaptive_bisect: true,
        };
        if let Ok(ck) = compact_source_response(&kicked, tight) {
            let segs = worldtube_segments(&kicked.worldtubes);
            assert!(
                ck.pieces.len() >= segs,
                "a 1e-8 band that could meet prefix identity is a polyline not compact; pieces={} segments={segs}",
                ck.pieces.len()
            );
        }

        let a_b_post_c = acceleration_at(&control_d, 1, t_post, &mut c0).unwrap();
        let a_b_post_k = acceleration_at(&kicked_d, 1, t_post, &mut c1).unwrap();
        let post = ((a_b_post_c[0] - a_b_post_k[0]).powi(2)
            + (a_b_post_c[1] - a_b_post_k[1]).powi(2))
            .sqrt()
            / a_scale();
        assert!(post > 1e-3, "post-cone B must still change on decode, ratio={post}");
    }

    #[test]
    fn four_kick_high_h_meets_band_or_honestly_refuses() {
        let ic = laboratory_two_body();
        let kicks: Vec<Intervention> = (0..4)
            .map(|n| Intervention {
                t: 1.25 + 2.0 * n as f64,
                body_id: 0,
                delta_v: [0.0, 0.02],
            })
            .collect();
        let driven = compile_source_response(ic, kicks, 9.0, 1.0 / 24.0).unwrap();
        let mut rec = Charge::default();
        if driven.compact.pieces.is_empty() {
            assert!(
                driven.charge.fallback > 0,
                "empty compact must be an honest generator refuse, not a silent polyline"
            );
            assert!(
                driven.decode_sources(&mut rec).is_err(),
                "decode must fail closed when the generator refuses"
            );
        } else {
            assert!(
                driven.compact.max_error <= driven.compact.band,
                "stored compact must meet the admitted band, error {} vs {}",
                driven.compact.max_error,
                driven.compact.band
            );
            assert!(
                driven.decode_sources(&mut rec).is_ok(),
                "decode must succeed when the generator meets the band"
            );
            assert!(
                driven.charge.fallback == 0,
                "meeting the band must not also set fallback polyline-as-compact"
            );
        }
    }

    #[test]
    fn worldtubes_stay_named_remainder_not_decode_only() {
        let compiled = compile_source_response(
            laboratory_two_body(),
            laboratory_kick(),
            5.0,
            1.0 / 32.0,
        )
        .unwrap();
        assert!(
            !compiled.compact.pieces.is_empty(),
            "causal-arrival split must still store a generator on A→B→A"
        );
        let mut charge = Charge::default();
        let decoded = compiled.decode_sources(&mut charge).unwrap();
        let t_knot = compiled.worldtubes[1].segments[0].t0;
        let mut mutated = compiled.clone();
        mutated.worldtubes[1].segments[0].x0[0] += 10.0;
        let (xw_bad, _) = body_state(&mutated.worldtubes, 1, t_knot).unwrap();
        let (xg, _) = mutated.compact.state(1, t_knot).unwrap();
        assert!(
            (xw_bad[0] - xg[0]).abs() > 1.0,
            "remainder is not decode-only: mutating worldtubes diverges from the generator"
        );
        let restored = mutated.decode_sources(&mut charge).unwrap();
        let (xr, _) = body_state(&restored, 1, 2.0).unwrap();
        let (xd, _) = body_state(&decoded, 1, 2.0).unwrap();
        let d = ((xr[0] - xd[0]).powi(2) + (xr[1] - xd[1]).powi(2)).sqrt();
        assert!(
            d <= ADMITTED_BAND,
            "decode must follow the generator after remainder mutation, d={d}"
        );
    }
}
