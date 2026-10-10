//! The kick's latency budget, decomposed on the shipped path (Quant lens, run 20261010-2220).
//!
//! `decompose`: the real plane (`scenario::plane`, seed 1, rtf 1, members 48, the kick-bench's own
//! replay protocol), one timing sample per distinct pending ship kick at deterministic 60 Hz
//! snapshots: the full pure resolver `step::process`, then its parts re-timed on the same snapshot —
//! `ctx.secondaries` + `ctx.tide` (setup), `force::acceleration` (kernel), and an f64 twin of the
//! same formula on pre-converted data. Counts S, distinct (doll, tick) epochs, record width.
//!
//! `sweep`: the shipped `force::field` over synthetic deterministic Secondary arrays (plane-like
//! magnitudes), working set from 32 KB to 512 MB at S = 8, exact vs the f64 twin on pre-converted
//! mirrors: ns/eval vs cache residency. No reimplementation of the exact path anywhere.
use emergent_space::orbit::Scalar;
use emergent_universe::force::{self, Secondary};
use emergent_universe::num::V2;
use emergent_universe::scenario::plane;
use emergent_universe::step;
use emergent_universe::{body::What, Budget, Kind};
use std::collections::HashSet;
use std::hint::black_box;
use std::time::Instant;

fn f(s: Scalar) -> f64 {
    (s.significand() as f64) * 2f64.powi(s.exponent() as i32 - 62)
}

/// An f64 mirror of a Secondary; the twin computes `field`'s sums on these (force.rs docs).
struct FS {
    pos: [f64; 2],
    vel: [f64; 2],
    gm: f64,
}

impl FS {
    fn of(s: &Secondary) -> Self {
        Self { pos: [f(s.pos[0]), f(s.pos[1])], vel: [f(s.vel[0]), f(s.vel[1])], gm: f(s.gm) }
    }
}

/// The f64 twin of `field`: accel `Σ gm·(xj−x)/r³`, potential `Σ gm/r`, the origin's fall
/// `Σ gm·xj/|xj|³` and its rate `Σ gm·(vj − 3·xj·(xj·vj)/|xj|²)/|xj|³`.
fn twin(secs: &[FS], x: [f64; 2]) -> ([f64; 2], f64, [f64; 2], [f64; 2]) {
    let (mut ax, mut ay, mut u) = (0.0, 0.0, 0.0);
    let (mut fx, mut fy, mut frx, mut fry) = (0.0, 0.0, 0.0, 0.0);
    for s in secs {
        let (xj, yj, vjx, vjy, gm) = (s.pos[0], s.pos[1], s.vel[0], s.vel[1], s.gm);
        let (dx, dy) = (xj - x[0], yj - x[1]);
        let r2 = dx * dx + dy * dy;
        let r = r2.sqrt();
        let k = gm / (r2 * r);
        ax += k * dx;
        ay += k * dy;
        u += gm / r;
        let rj2 = xj * xj + yj * yj;
        let rj = rj2.sqrt();
        let kj = gm / (rj2 * rj);
        fx += kj * xj;
        fy += kj * yj;
        let dot = (xj * vjx + yj * vjy) / rj2;
        frx += kj * (vjx - 3.0 * xj * dot);
        fry += kj * (vjy - 3.0 * yj * dot);
    }
    ([ax, ay], u, [fx, fy], [frx, fry])
}

fn pct(v: &mut Vec<f64>, p: f64) -> f64 {
    v.sort_by(f64::total_cmp);
    v[((v.len() - 1) as f64 * p).round() as usize].max(0.0)
}

fn stats(v: &mut Vec<f64>) -> String {
    if v.is_empty() {
        return "n=0".into();
    }
    format!("median {:.3} p99 {:.3} max {:.3} (n={})", pct(v, 0.5), pct(v, 0.99), pct(v, 1.0), v.len())
}

fn decompose() {
    let wall0 = Instant::now();
    let mut p = plane(Default::default(), 1, emergent_universe::fleet::Order::Sparse, 1, 48)
        .map_err(|e| format!("plane: {e:?}")).unwrap();
    let made_n = p.u.n_bodies();
    let mut last: Vec<Option<i64>> = vec![None; made_n];
    let (mut total, mut setup, mut kernel, mut tw, mut s_count) = (Vec::new(), Vec::new(), Vec::new(), Vec::new(), Vec::new());
    let mut epochs: HashSet<(u16, i64)> = HashSet::new();
    let mut kicks = 0u64;
    let mut rebinds = 0u64;
    let mut refused = 0u64;
    let seconds = 6.0f64;
    for n in 1..=(seconds * 60.0) as usize {
        if wall0.elapsed().as_secs_f64() >= 50.0 { break; }
        last.resize(p.u.n_bodies(), None);
        for i in 0..last.len() {
            let rec = p.u.rec(i);
            if rec.kind != Kind::Ship || !rec.alive { continue; }
            let Some(item) = rec.plan.first().copied() else { continue; };
            if !matches!(item.what, What::Kick(_)) || last[i] == Some(item.t) { continue; }
            let (doll, tick) = (rec.b.doll, item.t);
            kicks += 1;
            epochs.insert((doll, tick));
            let ctx = p.u.ctx();
            let t0 = Instant::now();
            let upd = step::process(black_box(&ctx), i, black_box(rec));
            total.push(t0.elapsed().as_secs_f64() * 1e6);
            refused += u64::from(upd.kind != step::Resolved::Kick);
            rebinds += u64::from(upd.new_entry.is_some());
            let t1 = Instant::now();
            let secs = ctx.secondaries(doll, tick, i).map_err(|e| format!("{e:?}")).unwrap();
            let tide = ctx.tide(doll, tick).map_err(|e| format!("{e:?}")).unwrap();
            setup.push(t1.elapsed().as_secs_f64() * 1e6);
            s_count.push(secs.len() as f64);
            let x = ctx.state_of(i, tick).map_err(|e| format!("{e:?}")).unwrap().0;
            let fsecs: Vec<FS> = secs.iter().map(FS::of).collect();
            let fx = [f(x[0]), f(x[1])];
            let t2 = Instant::now();
            let a = force::acceleration(black_box(0), black_box(x), black_box(&secs), black_box(tide))
                .map_err(|e| format!("{e:?}")).unwrap();
            kernel.push(t2.elapsed().as_secs_f64() * 1e6);
            let t3 = Instant::now();
            let ft = twin(black_box(&fsecs), black_box(fx));
            tw.push(t3.elapsed().as_secs_f64() * 1e6);
            black_box((a, ft));
        }
        p.u.frame(1.0 / 60.0, 1.0, Budget::unlimited());
        p.u.settle(p.u.now);
    }
    let size_sec = std::mem::size_of::<Secondary>();
    println!("decompose {{");
    println!("  seconds_game: {seconds}, bodies_made: {made_n}, kicks: {kicks}, refused: {refused}, distinct_epochs: {} ({:.1} kicks per epoch)", epochs.len(), kicks as f64 / epochs.len().max(1) as f64);
    println!("  S_secondaries: {}", stats(&mut s_count));
    println!("  total_process_us: {}", stats(&mut total));
    println!("  setup_secondaries_tide_us: {}", stats(&mut setup));
    println!("  kernel_acceleration_us: {}", stats(&mut kernel));
    println!("  twin_f64_us: {}", stats(&mut tw));
    if !total.is_empty() {
        let (tm, sm, km, nm) = (pct(&mut total, 0.5), pct(&mut setup, 0.5), pct(&mut kernel, 0.5), pct(&mut tw, 0.5));
        println!("  shares_median: setup {:.1}% kernel {:.1}% residual {:.1}%  (of total {:.2} us)", 100.0 * sm / tm, 100.0 * km / tm, 100.0 * (tm - sm - km) / tm, tm);
        println!("  rebind_rate: {:.3}", rebinds as f64 / kicks.max(1) as f64);
    }
    println!("  secondary_record_bytes: {size_sec} ({} per 128 B line when aligned)", 128 / size_sec.max(1));
    println!("}}");
}

/// Deterministic LCG; positions in the star doll's units, plane-like magnitudes.
fn lcg(state: &mut u64) -> u64 {
    *state = state.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
    *state
}

fn sec_at(seed: &mut u64) -> Secondary {
    let raw = |s: &mut u64, lo: i64, hi: i64| Scalar::raw((lo + ((lcg(s) >> 16) as i64).rem_euclid(hi - lo)) as i128, -24).unwrap();
    Secondary {
        gm: raw(seed, 1, 64), // ~2^-30..2^-24: planet-to-star mass ratios
        pos: [raw(seed, 64, 1 << 14), raw(seed, -(1 << 14), -64)],
        vel: [raw(seed, -(1 << 8), 1 << 8), raw(seed, -(1 << 8), 1 << 8)],
        edge: Scalar::raw(1 << 10, -12).unwrap(),
    }
}

fn sweep() {
    const S: usize = 8;
    let sizes: [(usize, &str); 5] = [(32 * 1024, "32KB"), (256 * 1024, "256KB"), (8 << 20, "8MB"), (64 << 20, "64MB"), (320 << 20, "320MB")];
    let per_body = S * std::mem::size_of::<Secondary>() + 32;
    let mut seed = 0xC0FFEEu64;
    println!("sweep {{ S: {S}, secondary_record_bytes: {}, ns_per_body_and_per_eval: [", std::mem::size_of::<Secondary>());
    for (bytes, name) in sizes {
        let n = (bytes / per_body).max(8);
        let secs: Vec<Secondary> = (0..S).map(|_| sec_at(&mut seed)).collect();
        let fsecs: Vec<FS> = secs.iter().map(FS::of).collect();
        // Bodies far from every secondary and from zero: no refusal, no cancellation blowups.
        let bodies: Vec<V2> = (0..n)
            .map(|_| {
                let x = |s: &mut u64| Scalar::raw((1 + ((lcg(s) >> 20) as i64).rem_euclid(16)) as i128, -6).unwrap();
                [x(&mut seed), x(&mut seed)]
            })
            .collect();
        let fbodies: Vec<[f64; 2]> = bodies.iter().map(|b| [f(b[0]), f(b[1])]).collect();
        let t0 = Instant::now();
        let mut acc = 0u64;
        for b in &bodies {
            let fld = force::field(black_box(&secs), black_box(*b)).map_err(|e| format!("{e:?}")).unwrap();
            acc = acc.wrapping_add(fld.accel[0].significand() as u64);
        }
        let exact_ns = t0.elapsed().as_secs_f64() / (n as f64) * 1e9;
        let t1 = Instant::now();
        let mut facc = 0f64;
        for b in &fbodies {
            let (a, u, fl, fr) = twin(black_box(&fsecs), black_box(*b));
            facc += a[0] + u + fl[0] + fr[1];
        }
        let twin_ns = t1.elapsed().as_secs_f64() / (n as f64) * 1e9;
        println!("  {{ ws: \"{name}\", bodies: {n}, exact_ns_per_body: {exact_ns:.1}, exact_ns_per_eval: {:.1}, twin_ns_per_eval: {:.2}, ratio: {:.1} }},", exact_ns / S as f64, twin_ns / S as f64, exact_ns / twin_ns);
        black_box((acc, facc));
    }
    println!("]}}");
}

fn main() {
    let arg = std::env::args().nth(1).unwrap_or_default();
    match arg.as_str() {
        "decompose" => decompose(),
        "sweep" => sweep(),
        _ => {
            decompose();
            sweep();
        }
    }
}
