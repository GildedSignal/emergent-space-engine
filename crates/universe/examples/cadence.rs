//! Each body's own clock (14 October): the N ladder's belt (`scenario::ladder_ship`, the same births) about the plane's star
//! and its three planets, run by the clock of 7 October (`own_clock = false`: 2^step_log2 steps per period of the doll's shortest
//! secondary, Cinder; the reference) and by each body's own clock at `k_s` (`smooth_log2`: 2^k_s steps per its own period, finer
//! where it can meet a secondary). Reports, per run: kicks per body per game-second (the ships' steps: a kick and a boundary each), the steps per own period each body is given
//! (its constants), and against the reference the belt's error at log-spaced times: |Δa|/a and |Δe| of the osculating orbit about
//! the star, and |Δx|/a, as the median and worst over the bodies, with the growth exponent of the worst-so-far over the last four
//! octaves of time (0: an offset that does not grow; 0.5: a walk; 1: a drift). With `giant`, the Giant alone (a control: the same
//! run without the fast inner planets, whose forcing a coarse step aliases).
//!
//! cargo run --release -p emergent-universe --example cadence -- <bodies> <years> <k_s[:k_f],...> [giant]
use emergent_space::orbit::Scalar;
use emergent_universe::num::s;
use emergent_universe::observe::root_state;
use emergent_universe::scenario::{ladder_ship, PLANETS, STAR_RADIUS};
use emergent_universe::view::TICK_SECONDS;
use emergent_universe::{Config, Kind, OrbitSpec, Universe};
use std::time::Instant;

const YEAR: f64 = 365.25 * 86_400.0;

fn build(cfg: Config, n: usize, giant_only: bool) -> (Universe, Vec<usize>) {
    let mut u = Universe::new(s(STAR_RADIUS), cfg);
    u.threads = 1;
    for p in PLANETS.iter().filter(|p| !giant_only || p.name == "Giant") {
        let b = u
            .add_body(Kind::Planet, OrbitSpec { doll: 0, periapsis: s(p.periapsis), e_q48: p.e_q48, clockwise: false, angle: p.angle, phase: p.phase }, Scalar::ZERO)
            .unwrap();
        u.add_doll(p.name, b, p.mass_log2, Scalar::raw(p.radius as i128, -p.mass_log2).unwrap()).unwrap();
    }
    // The ladder's belt: ship k of a ladder of a million (its first 300 are the locals about Home, not made here).
    let ids = (0..n as u64)
        .map(|k| {
            let (spec, radius) = ladder_ship(1, 300 + k, 1_000_000, 0).unwrap();
            u.add_body(Kind::Ship, spec, radius).unwrap()
        })
        .collect();
    u.start().unwrap();
    (u, ids)
}

/// Osculating (a, e) about the star (G = M = c = 1 in root units) from a root state.
fn elements(x: [f64; 2], v: [f64; 2]) -> (f64, f64) {
    let r = (x[0] * x[0] + x[1] * x[1]).sqrt();
    let v2 = v[0] * v[0] + v[1] * v[1];
    let a = 1.0 / (2.0 / r - v2);
    let rv = x[0] * v[0] + x[1] * v[1];
    let ex = (v2 - 1.0 / r) * x[0] - rv * v[0];
    let ey = (v2 - 1.0 / r) * x[1] - rv * v[1];
    (a, (ex * ex + ey * ey).sqrt())
}

struct Run {
    /// per sample, per body: (x, v)
    states: Vec<Vec<([f64; 2], [f64; 2])>>,
    kicks_per_body_gs: f64,
    steps_per_period: Vec<f64>,
    wall: f64,
}

fn run(cfg: Config, n: usize, ticks: &[i64], giant_only: bool) -> Run {
    let t0 = Instant::now();
    let (mut u, ids) = build(cfg, n, giant_only);
    // The steps a body's own period gets far from the secondaries: P / (Δs·f'(c)).
    let steps_per_period = ids
        .iter()
        .map(|&i| {
            let r = u.rec(i);
            let p = match &r.b.entry.trajectory {
                emergent_space::binding::Trajectory::Cycle(c) => emergent_universe::num::to_f64(r.b.to_doll(c.period().unwrap()).unwrap()),
                _ => f64::NAN,
            };
            let ext = r.ext.expect("a ship of the root doll");
            let step = emergent_universe::num::to_f64(ext.ds) * emergent_universe::num::to_f64(emergent_universe::ext::fprime(ext.c, ext.b).unwrap());
            p / step
        })
        .collect();
    // The ships' own steps: each is a kick and a boundary (the root doll's clock has no levels); the planets' kicks are not theirs.
    let e0: u64 = ids.iter().map(|&i| u.rec(i).events).sum();
    let mut states = Vec::new();
    for &t in ticks {
        u.settle(t);
        let ctx = u.ctx();
        states.push(ids.iter().map(|&i| root_state(&ctx, i, t).unwrap_or(([f64::NAN; 2], [f64::NAN; 2]))).collect());
    }
    let game = *ticks.last().unwrap() as f64 * TICK_SECONDS;
    let e1: u64 = ids.iter().map(|&i| u.rec(i).events).sum();
    Run { states, kicks_per_body_gs: (e1 - e0) as f64 / 2.0 / n as f64 / game, steps_per_period, wall: t0.elapsed().as_secs_f64() }
}

fn pct(v: &mut [f64], p: f64) -> f64 {
    v.sort_by(f64::total_cmp);
    v[((v.len() - 1) as f64 * p).round() as usize]
}

/// Growth exponent of the running maximum of `err` against `t`, least squares over the samples of the last four octaves.
fn exponent(t: &[f64], err: &[f64]) -> f64 {
    let mut m = 0.0f64;
    let run: Vec<f64> = err.iter().map(|&e| {
        m = m.max(e);
        m
    }).collect();
    let last = *t.last().unwrap();
    let pts: Vec<(f64, f64)> = t.iter().zip(&run).filter(|(&ti, &e)| ti >= last / 16.0 && e > 0.0).map(|(&ti, &e)| (ti.ln(), e.ln())).collect();
    let k = pts.len() as f64;
    let (sx, sy) = (pts.iter().map(|p| p.0).sum::<f64>(), pts.iter().map(|p| p.1).sum::<f64>());
    let (sxx, sxy) = (pts.iter().map(|p| p.0 * p.0).sum::<f64>(), pts.iter().map(|p| p.0 * p.1).sum::<f64>());
    (k * sxy - sx * sy) / (k * sxx - sx * sx)
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let n: usize = args.get(1).and_then(|s| s.parse().ok()).unwrap_or(16);
    let years: f64 = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(20.0);
    // `k_s` or `k_s:k_f` (k_f: steps per period of the doll's shortest secondary, the frame's forcing; -60 is none).
    let ks: Vec<(i32, i32)> = args.get(3).map_or(vec![(4, Config::default().forcing_log2)], |s| {
        s.split(',')
            .map(|k| match k.split_once(':') {
                Some((a, b)) => (a.parse().unwrap(), b.parse().unwrap()),
                None => (k.parse().unwrap(), Config::default().forcing_log2),
            })
            .collect()
    });
    let giant_only = args.get(4).is_some_and(|s| s == "giant");
    // Samples: four an octave, from 1/256 of the horizon to the horizon.
    let horizon = years * YEAR / TICK_SECONDS;
    let ticks: Vec<i64> = (0..=32).map(|i| (horizon * 2f64.powf((i as f64 - 32.0) / 4.0)) as i64).collect();
    let tyears: Vec<f64> = ticks.iter().map(|&t| t as f64 * TICK_SECONDS / YEAR).collect();
    let reference = run(Config { own_clock: false, ..Config::default() }, n, &ticks, giant_only);
    println!(
        "cadence: {n} belt bodies over {years} years ({}); reference (the clock of 7 October, 2^7 steps per Cinder's period): {:.3e} kicks/body/game-s, steps per own period median {:.0}, {:.1} s",
        if giant_only { "the Giant alone" } else { "the plane's three planets" },
        reference.kicks_per_body_gs,
        pct(&mut reference.steps_per_period.clone(), 0.5),
        reference.wall
    );
    for &(k, kf) in &ks {
        let law = run(Config { smooth_log2: k, forcing_log2: kf, ..Config::default() }, n, &ticks, giant_only);
        let mut spp = law.steps_per_period.clone();
        let near = spp.iter().filter(|&&x| x > 2f64.powi(k + 1) * 1.01).count();
        let (mut da, mut de, mut dx) = (Vec::new(), Vec::new(), Vec::new());
        for (s_ref, s_law) in reference.states.iter().zip(&law.states) {
            let (mut a1, mut e1, mut x1) = (Vec::new(), Vec::new(), Vec::new());
            for (r, l) in s_ref.iter().zip(s_law) {
                let ((ar, er), (al, el)) = (elements(r.0, r.1), elements(l.0, l.1));
                a1.push(((al - ar) / ar).abs());
                e1.push((el - er).abs());
                x1.push(((l.0[0] - r.0[0]).powi(2) + (l.0[1] - r.0[1]).powi(2)).sqrt() / ar);
            }
            da.push(a1);
            de.push(e1);
            dx.push(x1);
        }
        let worst = |m: &Vec<Vec<f64>>| -> Vec<f64> { m.iter().map(|v| v.iter().cloned().filter(|x| x.is_finite()).fold(0.0, f64::max)).collect() };
        let median = |m: &Vec<Vec<f64>>| -> Vec<f64> { m.iter().map(|v| pct(&mut v.clone(), 0.5)).collect() };
        let (wa, we, wx) = (worst(&da), worst(&de), worst(&dx));
        let (ma, me, mx) = (median(&da), median(&de), median(&dx));
        println!(
            "k_s = {k}, k_f = {kf}: {:.3e} kicks/body/game-s ({:.1}x fewer), steps per own period min {:.0} median {:.0} max {:.0} ({near} of {n} finer than 2^(k_s+1): a secondary it can meet, or the forcing), {:.1} s",
            law.kicks_per_body_gs,
            reference.kicks_per_body_gs / law.kicks_per_body_gs,
            pct(&mut spp, 0.0),
            pct(&mut spp, 0.5),
            pct(&mut spp, 1.0),
            law.wall
        );
        for i in (0..ticks.len()).step_by(4) {
            println!(
                "  t {:>8.3} yr: |da|/a median {:.2e} worst {:.2e}; |de| median {:.2e} worst {:.2e}; |dx|/a median {:.2e} worst {:.2e}",
                tyears[i], ma[i], wa[i], me[i], we[i], mx[i], wx[i]
            );
        }
        println!(
            "  growth exponent of the worst (last four octaves): da {:.2}, de {:.2}, dx {:.2}; of the median: da {:.2}, de {:.2}, dx {:.2}",
            exponent(&tyears, &wa),
            exponent(&tyears, &we),
            exponent(&tyears, &wx),
            exponent(&tyears, &ma),
            exponent(&tyears, &me),
            exponent(&tyears, &mx)
        );
    }
}
