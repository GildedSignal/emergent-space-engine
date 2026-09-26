//! How coarse can a chronon be? The same physical gas (radius, box, speeds as fractions of
//! c, physical duration) simulated with chronons s times longer: every length in light-
//! chronons shrinks by s, velocities in 1/Q per chronon stay (c is always Q per chronon),
//! and the run takes 1/s as many chronons. Physics that survives coarsening (collisions and
//! wall pressure per physical time, energy) versus cost per mode.
use emergent_lattice::{chronon::Chronon, worlds, Stepper, World};
use serde_json::{json, Value};
use std::time::Instant;

/// Chronons `num/den` times longer than the ladder gas's (lengths scale by den/num).
fn scaled(n: u64, num: i64, den: i64, seed: u64) -> World {
    let mut w = worlds::gas(n, 0.1, 1024, 256, seed);
    for b in &mut w.bodies {
        b.x = [b.x[0] * den / num, b.x[1] * den / num];
        b.radius = b.radius * den / num;
    }
    let c = w.container.as_mut().unwrap();
    c.max = [c.max[0] * den / num, c.max[1] * den / num];
    w
}

fn run(mode: &str, w: World, horizon: i64) -> Option<(f64, u64, u64, i128, [i64; 2])> {
    let mut s: Box<dyn Stepper> = match mode {
        "chronon" => Box::new(Chronon::new(w.clone(), false).ok()?),
        "event" => Box::new(emergent_lattice_event::EventCore::new(w.clone(), false).ok()?),
        "metal" => Box::new(emergent_lattice_metal::MetalChronon::new(w.clone(), false).ok()?),
        _ => return None,
    };
    let t = Instant::now();
    s.run_to(horizon);
    let end = s.world();
    Some((t.elapsed().as_secs_f64(), s.log().contacts, s.log().walls, end.energy() - w.energy() - end.residual(), end.wall_momentum))
}

pub fn run_all(n: u64, modes: &[&str]) -> Value {
    let mut rows = Vec::new();
    for (num, den) in [(1i64, 4i64), (1, 2), (1, 1), (2, 1), (4, 1), (8, 1), (16, 1), (32, 1)] {
        let w = scaled(n, num, den, 2_718_281_828);
        let horizon = 1024 * den / num;
        let s = num as f64 / den as f64;
        for &m in modes {
            if m == "chronon" && n > 16384 {
                continue;
            }
            if let Some((secs, contacts, walls, ledger, wm)) = run(m, w.clone(), horizon) {
                // Physical duration is the same at every s, so total wall momentum is the pressure.
                let pressure = (wm[0] as f64).abs() + (wm[1] as f64).abs();
                let row = json!({"s": s, "mode": m, "chronons": horizon, "seconds": secs, "contacts": contacts, "walls": walls,
                    "energy_ledger_exact": ledger == 0, "wall_momentum_per_physical_time": pressure});
                println!("{row}");
                rows.push(row);
            }
        }
    }
    json!(rows)
}
