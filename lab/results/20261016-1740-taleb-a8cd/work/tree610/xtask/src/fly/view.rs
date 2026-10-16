//! Gather-only interface: replace these straight generators with curved tubes later.
//! Units here are light-seconds and seconds (c=1), independent of display c-scale.
use super::flight::{Flight, Segment, Q, TPS};
use emergent_lattice::Stepper;
use serde::Serialize;

fn dot(a: [f64; 2], b: [f64; 2]) -> f64 {
    a[0] * b[0] + a[1] * b[1]
}
fn at(s: Segment, t: f64) -> [f64; 2] {
    std::array::from_fn(|i| {
        s.x[i] as f64 / (Q * TPS) as f64
            + s.k[i] as f64 / Q as f64 * (t - s.tick as f64 / TPS as f64)
    })
}

/// |r - v Δt|² = Δt². Stable positive root, including radial approach near c.
pub fn crossing(s: Segment, observer: [f64; 2], now: f64) -> (f64, [f64; 2]) {
    let x = at(s, now);
    let r = [x[0] - observer[0], x[1] - observer[1]];
    let v = s.k.map(|k| k as f64 / Q as f64);
    let a = 1. - dot(v, v);
    let b = dot(r, v);
    let rr = dot(r, r);
    let root = (b * b + a * rr).sqrt();
    let delay = if b >= 0. {
        if root + b == 0. {
            0.
        } else {
            rr / (root + b)
        }
    } else {
        (root - b) / a
    };
    (now - delay, [r[0] - v[0] * delay, r[1] - v[1] * delay])
}

/// f(t)=t+|x(t)-observer|-now is strictly increasing for every subluminal
/// segment. Binary search its event epochs; the first segment extends into prehistory.
pub fn gather(history: &[Segment], observer: [f64; 2], now: f64) -> (usize, f64, [f64; 2]) {
    let mut lo = 0;
    let mut hi = history.len();
    while lo < hi {
        let m = (lo + hi) / 2;
        let s = history[m];
        let r = [
            s.x[0] as f64 / (Q * TPS) as f64 - observer[0],
            s.x[1] as f64 / (Q * TPS) as f64 - observer[1],
        ];
        if s.tick as f64 / TPS as f64 + dot(r, r).sqrt() <= now {
            lo = m + 1;
        } else {
            hi = m;
        }
    }
    let i = lo.saturating_sub(1);
    let (t, r) = crossing(history[i], observer, now);
    (i, t, r)
}

/// n points TOWARD the emitter, opposite the photon's propagation vector.
/// Lorentz-transform that null momentum: sky aberration and −p·u together.
pub fn aberration(n: [f64; 2], beta: [f64; 2]) -> ([f64; 2], f64) {
    let bb = dot(beta, beta);
    let g = 1. / (1. - bb).sqrt();
    let bn = dot(beta, n);
    let d = g * (1. + bn);
    let w = if bb == 0. { 1. } else { g + (g - 1.) * bn / bb };
    (std::array::from_fn(|i| (n[i] + w * beta[i]) / d), d)
}

/// Rest-frame blackbody sampled at R/G/B wavelengths. A spectral palette, not
/// a calibrated display spectrum; Doppler shifts T itself before this sampling.
pub fn blackbody(temperature: f64) -> [f64; 3] {
    let t = temperature.clamp(100., 1e7);
    let samples =
        [700e-9_f64, 546e-9, 435e-9].map(|w| 1. / (w.powi(5) * (0.01438776877 / (w * t)).exp_m1()));
    let max = samples.into_iter().fold(0., f64::max);
    samples.map(|s| (s / max).powf(1. / 2.2))
}

#[derive(Serialize)]
pub struct Seen {
    pub id: usize,
    pub direction: [f64; 2],
    pub range: f64, // observer-frame null distance, in display units
    pub angular_radius: f64,
    pub color: [f64; 3],
    pub intensity: f64,
    pub doppler: f64,
    pub emission: f64,
    pub kind: u8,
}

/// Geometry supplies arriving light; photometry does not know how a worldline
/// was made. A future curved tube can implement this instead of straight segments.
pub struct Photon {
    pub direction: [f64; 2], // outward sky direction in the reference frame
    pub distance: f64,
    pub emission: f64,
    pub frequency: f64, // reference-frame frequency / emitter rest frequency
}

pub trait LightConeSource {
    fn photon(&self, observer: [f64; 2], now: f64) -> Photon;
}

impl LightConeSource for [Segment] {
    fn photon(&self, observer: [f64; 2], now: f64) -> Photon {
        let (segment, emission, r) = gather(self, observer, now);
        let distance = dot(r, r).sqrt().max(1e-12);
        let direction = r.map(|v| v / distance);
        let emitter = self[segment].k.map(|k| k as f64 / Q as f64);
        let d_em = (1. + dot(emitter, direction)) / (1. - dot(emitter, emitter)).sqrt();
        Photon {
            direction,
            distance,
            emission,
            frequency: 1. / d_em,
        }
    }
}

#[derive(Serialize)]
pub struct Frame {
    pub tick: i64,
    pub coordinate: f64,
    pub proper: f64,
    pub beta: [f64; 2],
    pub heading: [f64; 2],
    pub contacts: u64,
    pub burns: u64,
    pub digest: String,
    pub c_scale: f64,
    pub seen: Vec<Seen>,
}

pub fn frame(f: &Flight, c_scale: f64) -> Frame {
    let w = f.core.world();
    let now = w.tick as f64 / TPS as f64;
    let observer = w.bodies[0].x.map(|x| x as f64 / (Q * TPS) as f64);
    let beta = w.bodies[0].k.map(|k| k as f64 / Q as f64);
    let mut seen = Vec::with_capacity(f.history.len() - 1);
    for i in 1..f.history.len() {
        let photon = f.history[i].as_slice().photon(observer, now);
        let distance = photon.distance;
        let (direction, d_obs) = aberration(photon.direction, beta);
        let doppler = d_obs * photon.frequency;
        let m = f.materials[i];
        seen.push(Seen {
            id: i + 1,
            direction,
            range: distance * d_obs * c_scale,
            angular_radius: (m.radius as f64 / (Q * TPS) as f64 / distance / d_obs).atan(),
            color: blackbody(m.temperature * doppler),
            intensity: m.luminosity * doppler.powi(4) / (1. + distance * distance / 64.),
            doppler,
            emission: photon.emission,
            kind: m.kind,
        });
    }
    Frame {
        tick: w.tick,
        coordinate: now,
        proper: f.proper_seconds(),
        beta,
        heading: f.heading_direction(),
        contacts: f.core.log().contacts,
        burns: f.burns,
        digest: f.digest(),
        c_scale,
        seen,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn comoving_emitter_has_no_doppler_shift() {
        for k in [
            [0, 0],
            [Q / 2, 0],
            [-Q * 9 / 10, 0],
            [Q * 7 / 10, Q * 7 / 10],
        ] {
            let h = [Segment {
                tick: 0,
                x: [Q * TPS * 3, Q * TPS * 4],
                k,
            }];
            let p = h.as_slice().photon([0., 0.], 2.);
            let beta = k.map(|k| k as f64 / Q as f64);
            assert!((aberration(p.direction, beta).1 * p.frequency - 1.).abs() < 1e-12);
        }
    }

    #[test]
    fn aberration_and_doppler_match_closed_forms() {
        for b in [0., 0.1, 0.5, 0.9, 0.999] {
            for i in 0..360 {
                let theta = i as f64 * std::f64::consts::TAU / 360.;
                let n = [theta.cos(), theta.sin()];
                let (p, d) = aberration(n, [b, 0.]);
                assert!((p[0] - (n[0] + b) / (1. + b * n[0])).abs() < 1e-11);
                assert!((p[1] - n[1] * (1. - b * b).sqrt() / (1. + b * n[0])).abs() < 1e-11);
                assert!((d - (1. + b * n[0]) / (1. - b * b).sqrt()).abs() < 1e-11);
                assert!((dot(p, p) - 1.).abs() < 1e-10);
                // Rotate both the observer and source; the result must rotate too.
                let rot = |a: [f64; 2]| [0.6 * a[0] - 0.8 * a[1], 0.8 * a[0] + 0.6 * a[1]];
                let (p2, d2) = aberration(rot(n), rot([b, 0.]));
                assert!((d - d2).abs() < 1e-10);
                assert!((p2[0] - rot(p)[0]).abs() < 1e-10);
            }
        }
        let d = aberration([1., 0.], [0.9, 0.]).1;
        assert!((d - 19_f64.sqrt()).abs() < 1e-12);
        assert!((d.powi(4) - 361.).abs() < 1e-10);
    }

    #[test]
    fn light_cone_matches_independent_brute_force_bisection() {
        for k in [
            [0, 0],
            [Q / 2, 0],
            [-Q * 9 / 10, 0],
            [Q * 7 / 10, -Q * 7 / 10],
            [Q - 1, 0],
        ] {
            for x in [
                [Q * TPS * 3, Q * TPS * 4],
                [-Q * TPS * 3, 0],
                [0, -Q * TPS * 9],
            ] {
                let s = Segment { tick: 0, x, k };
                let now = 2.;
                let obs = [0.3, -0.2];
                let residual = |t: f64| {
                    let a = at(s, t);
                    ((a[0] - obs[0]).powi(2) + (a[1] - obs[1]).powi(2)).sqrt() - (now - t)
                };
                let mut lo = -1e7;
                let mut hi = now;
                assert!(residual(lo) < 0.);
                for _ in 0..100 {
                    let m = (lo + hi) / 2.;
                    if residual(m) > 0. {
                        hi = m;
                    } else {
                        lo = m;
                    }
                }
                let (t, r) = crossing(s, obs, now);
                assert!((t - (lo + hi) / 2.).abs() < 1e-5, "k={k:?} x={x:?} t={t}");
                assert!((dot(r, r).sqrt() - (now - t)).abs() < 1e-8);
            }
        }
    }

    #[test]
    fn gather_selects_the_retarded_side_of_a_kink() {
        let h = [
            Segment {
                tick: 0,
                x: [Q * TPS * 4, 0],
                k: [0, 0],
            },
            Segment {
                tick: TPS,
                x: [Q * TPS * 4, 0],
                k: [Q / 2, 0],
            },
        ];
        let (s, t, _) = gather(&h, [0., 0.], 2.);
        assert_eq!(s, 0);
        assert!((t + 2.).abs() < 1e-12);
        let (s, t, _) = gather(&h, [0., 0.], 8.);
        assert_eq!(s, 1);
        assert!((t - 3.).abs() < 1e-12);
    }

    #[test]
    fn observation_and_c_scale_do_not_change_replay() {
        let mut f = Flight::new(9);
        f.advance(TPS).unwrap();
        let before = f.digest();
        let a = frame(&f, 200.);
        let b = frame(&f, 20.);
        assert_eq!(f.digest(), before);
        assert_eq!(a.seen.len(), 320);
        for (a, b) in a.seen.iter().zip(b.seen) {
            assert_eq!(a.direction, b.direction);
            assert_eq!(a.doppler, b.doppler);
            assert!((a.range / b.range - 10.).abs() < 1e-12);
        }
    }
}
