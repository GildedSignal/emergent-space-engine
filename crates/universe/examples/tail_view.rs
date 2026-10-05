// The view's tail: the frame loop of the bench (a wall budget for the engine, then the gather), every gather timed with
// the readouts it took, and the slowest listed. `tail_view [SECONDS] [RTF] [SEED] [ENGINE_MS]`.
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane;
use emergent_universe::view::{gather_cached, ViewCache};
use emergent_universe::{Budget, Config};
use std::time::Instant;

#[repr(C)]
struct Timespec {
    sec: i64,
    nsec: i64,
}
extern "C" {
    fn clock_gettime(clk: u32, ts: *mut Timespec) -> i32;
}
/// This thread's CPU time in ms (macOS: CLOCK_THREAD_CPUTIME_ID is 16): the work, without the waiting.
fn cpu_ms() -> f64 {
    let mut ts = Timespec { sec: 0, nsec: 0 };
    unsafe { clock_gettime(16, &mut ts) };
    ts.sec as f64 * 1e3 + ts.nsec as f64 / 1e6
}

fn main() {
    let a: Vec<String> = std::env::args().skip(1).collect();
    let seconds: f64 = a.first().map(|s| s.parse().unwrap()).unwrap_or(30.0);
    let rtf: f64 = a.get(1).map(|s| s.parse().unwrap()).unwrap_or(1.0);
    let seed: u64 = a.get(2).map(|s| s.parse().unwrap()).unwrap_or(1);
    let engine_ms: f64 = a.get(3).map(|s| s.parse().unwrap()).unwrap_or(5.0);
    let mut p = plane(Config::default(), seed, Order::Sparse, 1, 48).unwrap();
    let mut cache = ViewCache::default();
    let mut rows: Vec<(f64, f64, u64, usize, i64, bool, f64)> = Vec::new();
    let mut engine_cpu: Vec<f64> = Vec::new();
    for f in 0..(seconds * 60.0) as usize {
        let (t0, ce) = (Instant::now(), cpu_ms());
        let fr = p.u.frame(1.0 / 60.0, rtf, Budget::wall(engine_ms));
        let eng = t0.elapsed().as_secs_f64() * 1e3;
        engine_cpu.push(cpu_ms() - ce);
        let (t1, c1) = (Instant::now(), cpu_ms());
        let v = gather_cached(&p.u, &p.names, &mut cache).unwrap();
        rows.push((t1.elapsed().as_secs_f64() * 1e3, eng, cache.readouts, v.seen.len(), fr.ticks, fr.overflow, cpu_ms() - c1));
        let _ = f;
    }
    let mut idx: Vec<usize> = (0..rows.len()).collect();
    idx.sort_by(|&a, &b| rows[b].0.total_cmp(&rows[a].0));
    let mut g: Vec<f64> = rows.iter().map(|r| r.0).collect();
    g.sort_by(f64::total_cmp);
    let mut e = engine_cpu.clone();
    e.sort_by(f64::total_cmp);
    println!("engine cpu ms per frame: p50 {:.3} p99 {:.3} p99.9 {:.3} max {:.3}; frames above 5.5 ms {} above 16.7 ms {}", e[e.len() / 2], e[e.len() * 99 / 100], e[e.len() * 999 / 1000], e[e.len() - 1], e.iter().filter(|&&x| x > 5.5).count(), e.iter().filter(|&&x| x > 16.7).count());
    let mut c: Vec<f64> = rows.iter().map(|r| r.6).collect();
    c.sort_by(f64::total_cmp);
    println!("gather cpu ms: p50 {:.3} p99 {:.3} max {:.3}", c[c.len() / 2], c[c.len() * 99 / 100], c[c.len() - 1]);
    println!("gather wall ms: p50 {:.3} p99 {:.3} max {:.3}; frames with overflow {}", g[g.len() / 2], g[g.len() * 99 / 100], g[g.len() - 1], rows.iter().filter(|r| r.5).count());
    for &i in idx.iter().take(8) {
        let r = rows[i];
        println!("  frame {i:>5}: gather {:7.3} ms wall, {:6.3} ms cpu ({} readouts, {} seen) engine {:6.2} ms ticks {} overflow {}", r.0, r.6, r.2, r.3, r.1, r.4, r.5);
    }
}
