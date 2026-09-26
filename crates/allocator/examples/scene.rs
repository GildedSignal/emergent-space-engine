//! Frame harness on a 16-cluster scene: the frame thread never simulates, workers on
//! performance and efficiency cores compute ahead in least-slack order. Prints the monitoring
//! report (JSON) for a cruise phase and an overload phase in which off-screen regions use
//! their causal slack and, last, time acceleration drops while frames stay under 5 ms.
//!
//!     cargo run -p emergent-allocator --release --offline --example scene
use emergent_allocator::{scenes, Allocator, Config, FrameConfig, Report};
use emergent_lattice::chronon::Chronon;
use std::sync::Arc;

fn main() {
    let q = 256;
    let scene = scenes::galaxy(q, 4, 4, 250, 900, 16, 42);
    let bodies: usize = scene.iter().map(|w| w.bodies.len()).sum();
    // The observer sits inside cluster 0: its news arrives at once; the far corner has
    // ~3,000 chronons of light delay.
    let c0 = emergent_allocator::geom::Aabb::of(scene[0].bodies.iter().map(|b| &b.x));
    let observer = [(c0.lo[0] + c0.hi[0]) / 2, (c0.lo[1] + c0.hi[1]) / 2];
    // `scene round2` runs the round-2 scheduler in the same build (before/after).
    // `scene noaimd` keeps fixed 32-chronon strides with every other round-3 change.
    let has = |m: &str| std::env::args().any(|a| a == m);
    let base = if has("round2") {
        Config::round2()
    } else if has("noaimd") {
        Config { aimd: false, stride: 2, ..Config::default() }
    } else {
        Config::default()
    };
    let cfg = Config { p_workers: 3, e_workers: 4, observer, view_radius: 150 * q, ..base };
    let factory: emergent_allocator::Factory<Chronon> = Arc::new(|w| Chronon::new(w, false).expect("valid region world"));
    let mut a = Allocator::new(scene, factory, cfg).expect("scene");
    eprintln!("{bodies} bodies in {} regions; 3 performance + 4 efficiency workers; frame thread at user-interactive QoS", a.regions());
    for (name, fc) in [
        ("cruise", FrameConfig { hz: 120.0, seconds: 3.0, rate: 400.0, ahead_seconds: 0.25, record: false }),
        ("overload", FrameConfig { hz: 120.0, seconds: 3.0, rate: 8000.0, ahead_seconds: 0.25, record: false }),
    ] {
        let rep = a.run_frames(&fc);
        summary(name, &rep);
        println!("{}", serde_json::to_string_pretty(&rep).expect("report serialises"));
    }
}

fn summary(name: &str, r: &Report) {
    let f = r.frames.as_ref().expect("frame report");
    eprintln!(
        "{name}: {} frames, work p50 {:.3} p99.9 {:.3} max {:.3} ms, interval p99.9 {:.2} ms | present {:.0} → {:.0} ({:.0}/s of {:.0}/s target), accel drops {}, deadline misses {}, final lead max {:.0}, buffer p50 {:.0} | regions {}→{} merges {} splits {} rollbacks {} | {:.0} region-chronons/s, units p99 {:.3} max {:.3} ms (stepper advance max {:.3}, measure max {:.3}, lock wait p99 {:.3}; over budget {} units, max ×{:.1}) | rollbacks {} | utilisation {:?} | frames under 5 ms: {}",
        f.frames, f.work_ms.p50, f.work_ms.p999, f.work_ms.max, f.interval_ms.p999,
        r.sim.present_start, r.sim.present_end, r.sim.present_chronons_per_wall_second, f.target_rate, f.acceleration_drops, f.deadline_misses, f.final_lead_chronons.max, f.buffer_chronons.p50,
        r.regions.initial, r.regions.last, r.regions.merges, r.regions.splits, r.regions.rollbacks,
        r.sim.region_chronons_per_wall_second, r.units.ms.p99, r.units.ms.max, r.units.stepper_advance_ms.max, r.units.allocator_measure_ms.max, r.units.lock_wait_ms.p99, r.units.over_budget_units, r.units.max_ops_over_budget_ratio, r.regions.rollbacks,
        r.workers.iter().map(|w| (w.utilisation * 100.0).round() as i64).collect::<Vec<_>>(),
        f.work_ms.max < 5.0,
    );
}
