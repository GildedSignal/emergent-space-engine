// The second author's decisive experiment (run 20261008-0743, checker's gold condition): the
// display-quantum row cache (`view::RowCache`) run beside the truth — the shipped `gather_cached`
// — in the bench's exact loop (canonical burn script, wall-budgeted engine). Each frame: the
// engine step, then two gathers over the same state, truth first on even frames and served first
// on odd (to cancel order bias), timing both; then every row the cache served is gated against
// the truth row, field by field, at the display quantum. The gate's quanta: angle one pixel
// (0.05° at 1080p, 0.02° at 4K), shift one palette step (1e-3, 2e-4), distances relative like
// the shift, a member's staleness one whole tick, colour one palette step, luminosity 4× the
// shift (it is shift⁴).
// `quantum_view [SECONDS] [RTF] [SEED] [ENGINE_MS] [MEMBERS] [QUANTUM: 1080p|4k]`
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane;
use emergent_universe::view::{gather_cached, gather_quantized, Quantum, RowCache, ViewCache, TICK_SECONDS};
use emergent_universe::{Budget, Config};
use std::collections::BTreeMap;
use std::time::Instant;

fn script(frame: usize) -> u8 {
    let slot = frame / 240;
    if frame % 240 < 20 {
        [1, 9, 2, 4, 1, 1 | 4, 2, 8][slot % 8]
    } else {
        0
    }
}

use std::cell::Cell;
thread_local! { static DUMPS: Cell<u32> = Cell::new(0); }

fn angle_deg(a: [f64; 2], b: [f64; 2]) -> f64 {
    (a[0] * b[0] + a[1] * b[1]).clamp(-1.0, 1.0).acos().to_degrees()
}
struct Gate {
    checks: u64,
    viol: BTreeMap<&'static str, u64>,
    worst: BTreeMap<&'static str, f64>,
    /// Violations by row kind (4 = fleet member, else a body) and the worst id.
    by_kind: BTreeMap<u8, u64>,
    worst_id: BTreeMap<&'static str, usize>,
}

impl Gate {
    fn check(&mut self, name: &'static str, kind: u8, id: usize, err: f64, q: f64) {
        let r = err / q;
        let e = self.worst.entry(name).or_insert(0.0);
        if r > *e {
            *e = r;
            self.worst_id.insert(name, id);
        }
        if r > 1.0 {
            *self.viol.entry(name).or_insert(0) += 1;
            *self.by_kind.entry(kind).or_insert(0) += 1;
        }
    }
}

fn main() {
    let a: Vec<String> = std::env::args().skip(1).collect();
    let seconds: f64 = a.first().map(|s| s.parse().unwrap()).unwrap_or(20.0);
    let rtf: f64 = a.get(1).map(|s| s.parse().unwrap()).unwrap_or(100.0);
    let seed: u64 = a.get(2).map(|s| s.parse().unwrap()).unwrap_or(1);
    let engine_ms: f64 = a.get(3).map(|s| s.parse().unwrap()).unwrap_or(5.0);
    let members: u64 = a.get(4).map(|s| s.parse().unwrap()).unwrap_or(48);
    let label = a.get(5).map(|s| s.as_str()).unwrap_or("1080p").to_string();
    let q = if label == "4k" {
        Quantum { angle_deg: 0.02, shift_rel: 2e-4 }
    } else {
        Quantum { angle_deg: 0.05, shift_rel: 1e-3 }
    };
    let mut p = plane(Config::default(), seed, Order::Sparse, 1, members).unwrap();
    let frames = (seconds * 60.0) as usize;
    let per_frame = rtf / 60.0 / TICK_SECONDS;
    let (mut log, mut word) = (Vec::new(), 0u8);
    for n in 1..=frames {
        let w = emergent_universe::thrust::word(script(n), 0);
        if w != word {
            word = w;
            log.push((((n - 1) as f64 * per_frame).round() as i64, w));
        }
    }
    for &(t, k) in &log {
        p.u.schedule(t, k).unwrap();
    }
    let cut = (frames as f64 * rtf / 60.0 / TICK_SECONDS).round() as i64;
    let (mut vc_t, mut vc_s) = (ViewCache::default(), ViewCache::default());
    let mut rc = RowCache::default();
    let mut t_truth: Vec<f64> = Vec::new();
    let mut t_serv: Vec<f64> = Vec::new();
    let (mut served_rows, mut computed_rows, mut total_rows, mut kicks_end) = (0u64, 0u64, 0u64, 0u64);
    let (mut refused_basis, mut refused_body_basis, mut refused_max, mut refused_drift) = (0u64, 0u64, 0u64, 0u64);
    let (mut fleet_tc_changes, mut fleet_rows) = (0u64, 0u64);
    let mut gate = Gate { checks: 0, viol: BTreeMap::new(), worst: BTreeMap::new(), by_kind: BTreeMap::new(), worst_id: BTreeMap::new() };
    for frame in 0..frames {
        let _fr = p.u.frame_to(1.0 / 60.0, rtf, Budget::wall(engine_ms), cut);
        let (vt, vs, mt, ms) = if frame % 2 == 0 {
            let t0 = Instant::now();
            let vt = gather_cached(&p.u, &p.names, &mut vc_t).unwrap();
            let mt = t0.elapsed().as_secs_f64() * 1e3;
            let t1 = Instant::now();
            let vs = gather_quantized(&p.u, &p.names, &mut vc_s, &mut rc, q).unwrap();
            (vt, vs, mt, t1.elapsed().as_secs_f64() * 1e3)
        } else {
            let t1 = Instant::now();
            let vs = gather_quantized(&p.u, &p.names, &mut vc_s, &mut rc, q).unwrap();
            let ms = t1.elapsed().as_secs_f64() * 1e3;
            let t0 = Instant::now();
            let vt = gather_cached(&p.u, &p.names, &mut vc_t).unwrap();
            (vt, vs, t0.elapsed().as_secs_f64() * 1e3, ms)
        };
        t_truth.push(mt);
        t_serv.push(ms);
        served_rows += rc.served;
        refused_basis += rc.refused_basis;
        refused_body_basis += rc.refused_body_basis;
        fleet_tc_changes += rc.fleet_tc_changes;
        fleet_rows += rc.fleet_rows;
        refused_max += rc.refused_max;
        refused_drift += rc.refused_drift;
        computed_rows += rc.computed;
        total_rows += vs.seen.len() as u64;
        kicks_end = p.u.stats.kicks;
        // The gate: every served row against the truth, field by field.
        let truth: std::collections::HashMap<usize, _> = vt.seen.iter().map(|s| (s.id, s)).collect();
        let served: std::collections::HashMap<usize, _> = vs.seen.iter().map(|s| (s.id, s)).collect();
        for &id in &rc.served_ids {
            let (Some(s), Some(t)) = (served.get(&id), truth.get(&id)) else { continue };
            gate.checks += 1;
            let (k, rid) = (t.kind, id);
            gate.check("direction", k, rid, angle_deg(s.direction, t.direction), q.angle_deg);
            let doff = ((s.offset[0] - t.offset[0]).powi(2) + (s.offset[1] - t.offset[1]).powi(2)).sqrt();
            let toff = (t.offset[0].powi(2) + t.offset[1].powi(2)).sqrt().max(1e-12);
            gate.check("offset", k, rid, doff, q.angle_deg.to_radians().tan() * toff);
            gate.check("light_seconds", k, rid, (s.light_seconds - t.light_seconds).abs(), q.shift_rel * t.light_seconds.abs().max(1e-12));
            gate.check("age", k, rid, (s.age - t.age).abs(), q.shift_rel * t.light_seconds.abs().max(1e-9));
            if (s.age - t.age).abs() > 30.0 * q.shift_rel * t.light_seconds.abs().max(1e-9) && DUMPS.with(|d| d.get() < 3 && { d.set(d.get() + 1); true }) {
                println!("DUMP id {} kind {} held {} frames, ls {:+.6e}->{:+.6e} age {:+.4}->{:+.4} closing {:.3e}->{:.3e}",
                    id, t.kind, rc.held_frames(id).unwrap_or(u64::MAX), s.light_seconds, t.light_seconds, s.age, t.age, s.closing, t.closing);
            }
            gate.check("closing", k, rid, (s.closing - t.closing).abs(), q.shift_rel);
            gate.check("shift", k, rid, (s.shift - t.shift).abs(), q.shift_rel * t.shift.abs().max(1e-12));
            gate.check("color", k, rid, (0..3).map(|c| (s.color[c] - t.color[c]).abs()).fold(0.0, f64::max), 1e-2);
            gate.check("luminosity", k, rid, (s.luminosity - t.luminosity).abs(), 4.0 * q.shift_rel * t.luminosity.abs().max(1e-12));
            gate.check("lag", k, rid, (s.lag - t.lag).abs(), 1.0);
            gate.check("angular_radius", k, rid, (s.angular_radius - t.angular_radius).abs().to_degrees(), q.angle_deg);
        }
    }
    let pct = |v: &[f64], p: usize| {
        let mut g = v.to_vec();
        g.sort_by(f64::total_cmp);
        g[(g.len() * p / 100).min(g.len() - 1)]
    };
    println!("members {members} seed {seed} rtf {rtf} quantum {label} (angle {} deg, shift rel {})", q.angle_deg, q.shift_rel);
    println!(
        "gather truth   ms p50 {:.3} p90 {:.3} p99 {:.3} max {:.3}",
        pct(&t_truth, 50), pct(&t_truth, 90), pct(&t_truth, 99), t_truth.iter().cloned().fold(0.0, f64::max)
    );
    println!(
        "gather served  ms p50 {:.3} p90 {:.3} p99 {:.3} max {:.3}",
        pct(&t_serv, 50), pct(&t_serv, 90), pct(&t_serv, 99), t_serv.iter().cloned().fold(0.0, f64::max)
    );
    let delta: Vec<f64> = t_truth.iter().zip(&t_serv).map(|(a, b)| a - b).collect();
    println!(
        "saved ms/frame p50 {:.3} p90 {:.3} (of truth frame gather {:.3})",
        pct(&delta, 50), pct(&delta, 90), pct(&t_truth, 50)
    );
    println!(
        "rows: served {} ({:.1}% of {}), recomputed {}, refused basis {} (body {}) max {} drift {}, fleet tc changes {} over {} fleet-row visits, engine kicks {}",
        served_rows,
        100.0 * served_rows as f64 / total_rows as f64,
        total_rows,
        computed_rows,
        refused_basis,
        refused_body_basis,
        refused_max,
        refused_drift,
        fleet_tc_changes,
        fleet_rows,
        kicks_end
    );
    println!("gate: {} served-row checks over {} frames", gate.checks, frames);
    let mut fields: Vec<_> = gate.worst.iter().collect();
    fields.sort_by_key(|(f, _)| *f);
    let pass = gate.viol.is_empty();
    for (f, w) in fields {
        let id = gate.worst_id.get(f).copied().unwrap_or(0);
        println!("  {:>14}: worst err/quantum {:.3} at id {}{}", f, w, id, if w > &1.0 { " VIOLATION" } else { "" });
    }
    for (k, n) in gate.by_kind.iter() {
        println!("  violations on kind {}: {}", k, n);
    }
    if !gate.viol.is_empty() {
        let mut v: Vec<_> = gate.viol.iter().collect();
        v.sort_by_key(|(f, _)| *f);
        for (f, n) in v {
            println!("  {:>14}: {} violations", f, n);
        }
    }
    println!("GATE {}", if pass { "PASS" } else { "FAIL" });
}
