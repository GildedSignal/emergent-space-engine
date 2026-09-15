//! I3 long-time representation: Kepler two-body + slow residual as the
//! evolution. Construction does not collocate interval functions over H.
//! Compact-after-the-fact and Packet 3 PERIOD are not this object.
//! Not `production_law`. Not canonical gravity.

use crate::coupled_source_response::{
    field_acceleration, Body, BodyInit, Charge, ChargeRole, InitialCondition, Intervention,
    ResponseError, Segment, C, COUPLED_RESPONSE_LAW_ID, G,
};
use serde::{Deserialize, Serialize};

const SECULAR_BAND: f64 = 5e-2;
const MAX_ECCENTRICITY: f64 = 0.85;
const MIN_PERIAPSIS_OVER_A: f64 = 0.15;
const RESIDUAL_MODES: usize = 3;
const SAMPLES_PER_ORBIT: usize = 16;
const MAX_LOOKBACK_SEGMENTS: usize = 64;

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct KeplerElements {
    pub t0: f64,
    pub mu0: f64,
    pub mu1: f64,
    pub id0: u64,
    pub id1: u64,
    pub com: [f64; 2],
    pub vcom: [f64; 2],
    pub a: f64,
    pub e: f64,
    pub n: f64,
    pub period: f64,
    pub periapsis: f64,
    pub m0: f64,
    pub omega: f64,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct SlowResidual {
    pub period: f64,
    pub mean: [f64; 2],
    pub cos: Vec<[f64; 2]>,
    pub sin: Vec<[f64; 2]>,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct SecularResponse {
    pub law_id: String,
    pub horizon: f64,
    pub genesis: InitialCondition,
    pub incoming: Vec<Intervention>,
    pub elements: KeplerElements,
    pub pieces: Vec<(f64, f64, KeplerElements)>,
    pub residual: SlowResidual,
    pub charge: Charge,
    pub wall_ns: u128,
    pub max_remainder: f64,
}

impl SecularResponse {
    pub fn bytes(&self) -> usize {
        serde_json::to_vec(self).map(|b| b.len()).unwrap_or(0)
    }

    pub fn eval(&self, id: u64, t: f64, charge: &mut Charge) -> Result<[f64; 2], ResponseError> {
        charge.reconstruction = charge.reconstruction.saturating_add(1);
        let el = self
            .pieces
            .iter()
            .find(|(a, b, _)| t + 1e-15 >= *a && t <= *b + 1e-15)
            .map(|(_, _, e)| e)
            .unwrap_or(&self.elements);
        let (x, _) = el.state(id, t)?;
        let a_res = self.residual.accel(t);
        let dt = t - el.t0;
        Ok([
            x[0] + 0.5 * a_res[0] * dt * dt,
            x[1] + 0.5 * a_res[1] * dt * dt,
        ])
    }
}

impl SlowResidual {
    fn accel(&self, t: f64) -> [f64; 2] {
        if self.period <= 1e-18 {
            return self.mean;
        }
        let m = std::f64::consts::TAU * (t / self.period);
        let mut a = self.mean;
        for k in 0..self.cos.len() {
            let km = (k as f64 + 1.0) * m;
            a[0] += self.cos[k][0] * km.cos() + self.sin[k][0] * km.sin();
            a[1] += self.cos[k][1] * km.cos() + self.sin[k][1] * km.sin();
        }
        a
    }
}

impl KeplerElements {
    fn from_pair(a: &BodyInit, b: &BodyInit, t0: f64) -> Result<Self, ResponseError> {
        let m = a.mu + b.mu;
        if m <= 1e-18 {
            return Err(ResponseError::UnsupportedDomain {
                why: "Kepler pair needs positive mass".into(),
            });
        }
        let com = [
            (a.mu * a.x[0] + b.mu * b.x[0]) / m,
            (a.mu * a.x[1] + b.mu * b.x[1]) / m,
        ];
        let vcom = [
            (a.mu * a.v[0] + b.mu * b.v[0]) / m,
            (a.mu * a.v[1] + b.mu * b.v[1]) / m,
        ];
        let r = [b.x[0] - a.x[0], b.x[1] - a.x[1]];
        let v = [b.v[0] - a.v[0], b.v[1] - a.v[1]];
        let rmag = hypot(r[0], r[1]);
        if rmag < 1e-12 {
            return Err(ResponseError::Singular);
        }
        let gm = G * m;
        let h = r[0] * v[1] - r[1] * v[0];
        let v2 = v[0] * v[0] + v[1] * v[1];
        let energy = 0.5 * v2 - gm / rmag;
        if energy >= -1e-12 {
            return Err(ResponseError::UnsupportedDomain {
                why: format!("unbound two-body (energy={energy}); secular Kepler refuses"),
            });
        }
        let sma = -gm / (2.0 * energy);
        let ev = [
            (v[1] * h) / gm - r[0] / rmag,
            (-v[0] * h) / gm - r[1] / rmag,
        ];
        let e = hypot(ev[0], ev[1]).min(0.999999);
        let periapsis = sma * (1.0 - e);
        if e > MAX_ECCENTRICITY || periapsis < MIN_PERIAPSIS_OVER_A * sma {
            return Err(ResponseError::UnsupportedDomain {
                why: format!(
                    "close-encounter / high-e Kepler (e={e}, periapsis={periapsis}, a={sma}); fallback to collocation"
                ),
            });
        }
        let n = (gm / (sma * sma * sma)).sqrt();
        let period = std::f64::consts::TAU / n;
        let omega = ev[1].atan2(ev[0]);
        let cos_w = omega.cos();
        let sin_w = omega.sin();
        let x_pf = r[0] * cos_w + r[1] * sin_w;
        let y_pf = -r[0] * sin_w + r[1] * cos_w;
        let ecc_arg = ((sma - rmag) / (sma * e.max(1e-15))).clamp(-1.0, 1.0);
        let mut ea = if y_pf >= 0.0 {
            ecc_arg.acos()
        } else {
            -ecc_arg.acos()
        };
        if e < 1e-8 {
            ea = y_pf.atan2(x_pf);
        }
        let m0 = ea - e * ea.sin();
        Ok(Self {
            t0,
            mu0: a.mu,
            mu1: b.mu,
            id0: a.id,
            id1: b.id,
            com,
            vcom,
            a: sma,
            e,
            n,
            period,
            periapsis,
            m0,
            omega,
        })
    }

    fn relative(&self, t: f64) -> Result<([f64; 2], [f64; 2]), ResponseError> {
        let dt = t - self.t0;
        let mean = self.m0 + self.n * dt;
        let ea = kepler_ea(mean, self.e)?;
        let cos_e = ea.cos();
        let sin_e = ea.sin();
        let x_pf = self.a * (cos_e - self.e);
        let y_pf = self.a * (1.0 - self.e * self.e).sqrt() * sin_e;
        let edot = self.n / (1.0 - self.e * cos_e).max(1e-15);
        let vx_pf = -self.a * sin_e * edot;
        let vy_pf = self.a * (1.0 - self.e * self.e).sqrt() * cos_e * edot;
        let c = self.omega.cos();
        let s = self.omega.sin();
        let rel = [x_pf * c - y_pf * s, x_pf * s + y_pf * c];
        let vrel = [vx_pf * c - vy_pf * s, vx_pf * s + vy_pf * c];
        Ok((rel, vrel))
    }

    fn state(&self, id: u64, t: f64) -> Result<([f64; 2], [f64; 2]), ResponseError> {
        let (rel, vrel) = self.relative(t)?;
        let m = self.mu0 + self.mu1;
        let com = [
            self.com[0] + self.vcom[0] * (t - self.t0),
            self.com[1] + self.vcom[1] * (t - self.t0),
        ];
        let vcom = self.vcom;
        if id == self.id0 {
            let f = self.mu1 / m;
            Ok((
                [com[0] - f * rel[0], com[1] - f * rel[1]],
                [vcom[0] - f * vrel[0], vcom[1] - f * vrel[1]],
            ))
        } else if id == self.id1 {
            let f = self.mu0 / m;
            Ok((
                [com[0] + f * rel[0], com[1] + f * rel[1]],
                [vcom[0] + f * vrel[0], vcom[1] + f * vrel[1]],
            ))
        } else {
            Err(ResponseError::UnsupportedDomain {
                why: format!("body {id} is not in the Kepler pair"),
            })
        }
    }

    fn newtonian_a(&self, id: u64, t: f64) -> Result<[f64; 2], ResponseError> {
        let (rel, _) = self.relative(t)?;
        let r = hypot(rel[0], rel[1]).max(1e-15);
        let gm = G * (self.mu0 + self.mu1);
        let a_rel = [-gm * rel[0] / (r * r * r), -gm * rel[1] / (r * r * r)];
        let m = self.mu0 + self.mu1;
        if id == self.id0 {
            let f = self.mu1 / m;
            Ok([f * a_rel[0], f * a_rel[1]])
        } else if id == self.id1 {
            let f = self.mu0 / m;
            Ok([-f * a_rel[0], -f * a_rel[1]])
        } else {
            Err(ResponseError::UnsupportedDomain {
                why: format!("body {id} is not in the Kepler pair"),
            })
        }
    }
}

fn kepler_ea(mean: f64, e: f64) -> Result<f64, ResponseError> {
    let mut ea = mean;
    if e > 0.8 {
        ea = std::f64::consts::PI;
    }
    for _ in 0..40 {
        let f = ea - e * ea.sin() - mean;
        let fp = 1.0 - e * ea.cos();
        if fp.abs() < 1e-18 {
            return Err(ResponseError::Singular);
        }
        let next = ea - f / fp;
        if (next - ea).abs() < 1e-14 {
            return Ok(next);
        }
        ea = next;
    }
    Err(ResponseError::UnsupportedDomain {
        why: "Kepler equation did not converge".into(),
    })
}

fn hypot(x: f64, y: f64) -> f64 {
    (x * x + y * y).sqrt()
}

pub fn laboratory_circular_pair() -> InitialCondition {
    let a = 4.0;
    let m = 2.0;
    let v = (G * m / a).sqrt() / 2.0;
    InitialCondition {
        genesis_t: 0.0,
        bodies: vec![
            BodyInit {
                id: 0,
                mu: 1.0,
                x: [-a / 2.0, 0.0],
                v: [0.0, -v],
            },
            BodyInit {
                id: 1,
                mu: 1.0,
                x: [a / 2.0, 0.0],
                v: [0.0, v],
            },
        ],
    }
}

pub fn laboratory_eccentric_pair() -> InitialCondition {
    let mut ic = laboratory_circular_pair();
    ic.bodies[0].v[1] *= 0.72;
    ic.bodies[1].v[1] *= 0.72;
    ic
}

pub fn laboratory_resonant_kicks(period: f64, horizon: f64) -> Vec<Intervention> {
    let mut kicks = Vec::new();
    let mut t = period;
    while t < horizon - 1e-9 {
        kicks.push(Intervention {
            t,
            body_id: 0,
            delta_v: [0.0, 0.02],
        });
        t += period;
    }
    kicks
}

fn kepler_lookback_bodies(
    el: &KeplerElements,
    t0: f64,
    horizon: f64,
) -> Result<Vec<Body>, ResponseError> {
    let n_orbits = ((horizon - t0).max(el.period) / el.period).ceil().max(1.0);
    let n = ((SAMPLES_PER_ORBIT as f64 * n_orbits) as usize)
        .clamp(SAMPLES_PER_ORBIT, MAX_LOOKBACK_SEGMENTS);
    let dt = (horizon - t0).max(el.period / SAMPLES_PER_ORBIT as f64) / n as f64;
    let mut bodies = vec![
        Body {
            id: el.id0,
            segments: Vec::new(),
        },
        Body {
            id: el.id1,
            segments: Vec::new(),
        },
    ];
    for i in 0..n {
        let t = t0 + dt * i as f64;
        let t1 = if i + 1 == n {
            Some(horizon.max(t + dt))
        } else {
            Some(t + dt)
        };
        let (x0, v0) = el.state(el.id0, t)?;
        let (x1, v1) = el.state(el.id1, t)?;
        bodies[0].segments.push(Segment {
            t0: t,
            t1,
            x0,
            v: v0,
            a: [0.0, 0.0],
            mu: el.mu0,
        });
        bodies[1].segments.push(Segment {
            t0: t,
            t1,
            x0: x1,
            v: v1,
            a: [0.0, 0.0],
            mu: el.mu1,
        });
    }
    Ok(bodies)
}

fn fit_residual(
    el: &KeplerElements,
    t0: f64,
    horizon: f64,
    charge: &mut Charge,
) -> Result<SlowResidual, ResponseError> {
    let sources = kepler_lookback_bodies(el, t0, horizon)?;
    charge.history += 1;
    let n = sources[0].segments.len().max(8);
    let mut samples: Vec<(f64, [f64; 2])> = Vec::new();
    for i in 0..n {
        let t = t0 + (horizon - t0) * (i as f64 + 0.5) / n as f64;
        charge.source_evolution += 2;
        let (x, v) = el.state(el.id0, t)?;
        let gem = field_acceleration(&sources, t, x, v, Some(el.id0), charge)?;
        charge.retarded_solves += 1;
        let newt = el.newtonian_a(el.id0, t)?;
        samples.push((t, [gem[0] - newt[0], gem[1] - newt[1]]));
    }
    let period = el.period;
    let mut mean = [0.0, 0.0];
    for (_, a) in &samples {
        mean[0] += a[0];
        mean[1] += a[1];
    }
    mean[0] /= samples.len() as f64;
    mean[1] /= samples.len() as f64;
    let mut cos = vec![[0.0, 0.0]; RESIDUAL_MODES];
    let mut sin = vec![[0.0, 0.0]; RESIDUAL_MODES];
    for k in 0..RESIDUAL_MODES {
        charge.coefficient_construction += 1;
        for (t, a) in &samples {
            let km = (k as f64 + 1.0) * std::f64::consts::TAU * ((t - t0) / period);
            let da = [a[0] - mean[0], a[1] - mean[1]];
            cos[k][0] += da[0] * km.cos();
            cos[k][1] += da[1] * km.cos();
            sin[k][0] += da[0] * km.sin();
            sin[k][1] += da[1] * km.sin();
        }
        let s = 2.0 / samples.len() as f64;
        cos[k][0] *= s;
        cos[k][1] *= s;
        sin[k][0] *= s;
        sin[k][1] *= s;
    }
    Ok(SlowResidual {
        period,
        mean,
        cos,
        sin,
    })
}

fn remainder_against_kepler_gem(
    el: &KeplerElements,
    residual: &SlowResidual,
    t0: f64,
    horizon: f64,
    charge: &mut Charge,
) -> Result<f64, ResponseError> {
    let sources = kepler_lookback_bodies(el, t0, horizon)?;
    let mut max_da = 0.0_f64;
    for k in 0..8 {
        let t = t0 + (horizon - t0) * (k as f64 + 0.5) / 8.0;
        let (x, v) = el.state(el.id0, t)?;
        let gem = field_acceleration(&sources, t, x, v, Some(el.id0), charge)?;
        charge.validation += 1;
        let newt = el.newtonian_a(el.id0, t)?;
        let pred = residual.accel(t);
        let da = hypot(
            gem[0] - newt[0] - pred[0],
            gem[1] - newt[1] - pred[1],
        );
        max_da = max_da.max(da);
    }
    Ok(max_da)
}

/// Construct Kepler+slow-residual evolution. Does not call interval collocation.
/// Strong kicks and high-e / close-encounter ICs refuse; collocation is the fallback.
pub fn compile_secular_response(
    ic: InitialCondition,
    incoming: Vec<Intervention>,
    horizon: f64,
) -> Result<SecularResponse, ResponseError> {
    let start = std::time::Instant::now();
    let mut charge = Charge {
        init: 1,
        ..Charge::default()
    };
    if ic.bodies.len() != 2 {
        charge.fallback += 1;
        return Err(ResponseError::UnsupportedDomain {
            why: "secular Kepler is a two-body representation".into(),
        });
    }
    if horizon > ic.genesis_t && (horizon - ic.genesis_t) * C < 1e-9 {
        return Err(ResponseError::UnsupportedDomain {
            why: "empty secular horizon".into(),
        });
    }
    let weak = incoming.iter().all(|k| hypot(k.delta_v[0], k.delta_v[1]) <= 0.03);
    if !incoming.is_empty() && !weak {
        charge.fallback += 1;
        charge.push_child(
            "secular-kick-fallback",
            ChargeRole::Fallback,
            Charge {
                fallback: 1,
                ..Charge::default()
            },
        );
        return Err(ResponseError::UnsupportedDomain {
            why: format!(
                "secular Kepler refuses {} strong interventions; collocation is the fallback",
                incoming.len()
            ),
        });
    }
    let mut kicks = incoming.clone();
    kicks.sort_by(|a, b| a.t.partial_cmp(&b.t).unwrap());
    let mut cuts = vec![ic.genesis_t];
    for k in &kicks {
        if k.t > ic.genesis_t + 1e-12 && k.t < horizon {
            cuts.push(k.t);
        }
    }
    cuts.push(horizon);
    cuts.dedup_by(|a, b| (*a - *b).abs() < 1e-12);
    let mut bodies = ic.bodies.clone();
    let mut pieces = Vec::new();
    for w in cuts.windows(2) {
        let ta = w[0];
        let tb = w[1];
        for k in &kicks {
            if (k.t - ta).abs() < 1e-12 {
                if let Some(b) = bodies.iter_mut().find(|b| b.id == k.body_id) {
                    b.v[0] += k.delta_v[0];
                    b.v[1] += k.delta_v[1];
                    charge.repair += 1;
                }
            }
        }
        let el = match KeplerElements::from_pair(&bodies[0], &bodies[1], ta) {
            Ok(el) => el,
            Err(err) => {
                charge.fallback += 1;
                return Err(err);
            }
        };
        let (x0, v0) = el.state(el.id0, tb)?;
        let (x1, v1) = el.state(el.id1, tb)?;
        bodies[0].x = x0;
        bodies[0].v = v0;
        bodies[1].x = x1;
        bodies[1].v = v1;
        pieces.push((ta, tb, el));
    }
    let el = pieces[0].2.clone();
    let residual = fit_residual(&el, ic.genesis_t, horizon.min(ic.genesis_t + el.period), &mut charge)?;
    let max_remainder =
        remainder_against_kepler_gem(&el, &residual, ic.genesis_t, pieces[0].1.min(ic.genesis_t + el.period), &mut charge)?;
    if max_remainder > SECULAR_BAND || !max_remainder.is_finite() {
        charge.fallback += 1;
        return Err(ResponseError::UnsupportedDomain {
            why: format!(
                "slow residual remainder {max_remainder} exceeds band {SECULAR_BAND}; not skipped evolution"
            ),
        });
    }
    if pieces.len() > 4 {
        charge.fallback += 1;
        return Err(ResponseError::UnsupportedDomain {
            why: format!(
                "resonance/forcing produced {} Kepler pieces; remainder may still pass but construction tracks kicks, not skipped GEM. Fallback to collocation",
                pieces.len()
            ),
        });
    }
    charge.verification += 1;
    Ok(SecularResponse {
        law_id: COUPLED_RESPONSE_LAW_ID.into(),
        horizon,
        genesis: ic,
        incoming,
        elements: el,
        pieces,
        residual,
        charge,
        wall_ns: start.elapsed().as_nanos(),
        max_remainder,
    })
}
