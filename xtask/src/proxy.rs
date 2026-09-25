//! HEVC proxy experiment (Julien, 25 September 2026): is the hardware encoder's residual a
//! sensor of new dynamical information? Six worlds with known ground truth (the engine's
//! committed events per frame) are rasterised two ways, position density and the x–vx
//! phase plane, as raw 8-bit luma for tools/hevc-probe. Advisory tier only: nothing here
//! feeds canonical state.
use emergent_lattice::{chronon::Chronon, worlds, Response, Stepper, World};
use std::{fs, io::Write, path::Path};

const Q: i64 = 1024;
const N: u64 = 16384;
const PX: usize = 512;

fn scenario(name: &str) -> World {
    let seed = 2_718_281_828;
    match name {
        "gas" => worlds::gas(N, 0.1, Q, 256, seed),
        "shock" => {
            let mut w = worlds::gas(N, 0.1, Q, 256, seed);
            let mid = w.container.unwrap().max[0] / 2;
            for b in &mut w.bodies {
                let dir = if b.x[0] < mid { 1 } else { -1 };
                b.k = [dir * 320 + b.k[0] / 8, b.k[1] / 8];
            }
            w
        }
        "random" => worlds::random(N, 400, Q, 1, seed, Response::Pass),
        "translate" => {
            let mut w = worlds::random(N, 400, Q, 1, seed, Response::Pass);
            for b in &mut w.bodies {
                b.k = [300, 100];
            }
            w
        }
        "swirl" => {
            let mut w = worlds::random(N, 400, Q, 1, seed, Response::Pass);
            let c = 1280 * Q;
            for b in &mut w.bodies {
                let (dx, dy) = (b.x[0] - c, b.x[1] - c);
                // Tangential velocity growing with radius, edge ~0.4c.
                b.k = [(-dy as i128 * 400 / (1300 * Q) as i128) as i64, (dx as i128 * 400 / (1300 * Q) as i128) as i64];
            }
            w
        }
        "static" => {
            let mut w = worlds::random(N, 400, Q, 1, seed, Response::Pass);
            for b in &mut w.bodies {
                b.k = [0, 0];
            }
            w
        }
        _ => panic!("unknown scenario"),
    }
}

/// (min, max) of x and y over the genesis world, padded by the travel of the run.
fn frame_box(w: &World, ticks: i64) -> ([i64; 2], [i64; 2]) {
    if let Some(c) = w.container {
        return (c.min, c.max);
    }
    let pad = Q / 2 * ticks;
    let lo = [0, 1].map(|a| w.bodies.iter().map(|b| b.x[a]).min().unwrap() - pad);
    let hi = [0, 1].map(|a| w.bodies.iter().map(|b| b.x[a]).max().unwrap() + pad);
    (lo, hi)
}

/// 0: position plane (x, y). 1: phase plane (x, vx). 2: worldtube-intercept plane
/// (x − vx·t, vx): free motion is exactly static there, so only interactions leave residual.
fn raster(w: &World, lo: [i64; 2], hi: [i64; 2], rep: u8, out: &mut Vec<u8>) {
    let mut f = vec![0u16; PX * PX];
    for b in &w.bodies {
        let bin = |v: i64, lo: i64, hi: i64| (((v - lo) as i128 * PX as i128) / ((hi - lo) as i128 + 1)).clamp(0, PX as i128 - 1) as usize;
        let x = if rep == 2 { b.x[0] - b.k[0] * w.tick } else { b.x[0] };
        let col = bin(x, lo[0], hi[0]);
        let row = if rep == 0 { bin(b.x[1], lo[1], hi[1]) } else { bin(b.k[0], -Q, Q) };
        f[row * PX + col] += 1;
    }
    out.extend(f.iter().map(|&c| (c.min(4) * 63) as u8));
}

/// Writes <out>/<scenario>-<pos|phase>.raw and <scenario>-events.txt (events per frame).
pub fn run(out: &Path, frames: usize, ticks_per_frame: i64) -> Result<(), Box<dyn std::error::Error>> {
    fs::create_dir_all(out)?;
    for name in ["gas", "shock", "random", "translate", "swirl", "static"] {
        let w0 = scenario(name);
        let (lo, hi) = frame_box(&w0, frames as i64 * ticks_per_frame);
        let mut c = Chronon::new(w0, false)?;
        let (mut pos, mut phase, mut tube) = (Vec::new(), Vec::new(), Vec::new());
        let mut events = fs::File::create(out.join(format!("{name}-events.txt")))?;
        let mut last = 0;
        for f in 0..frames {
            if f > 0 {
                c.run_to(f as i64 * ticks_per_frame);
            }
            let w = c.world();
            raster(&w, lo, hi, 0, &mut pos);
            raster(&w, lo, hi, 1, &mut phase);
            raster(&w, lo, hi, 2, &mut tube);
            let fired = c.metrics().fired;
            writeln!(events, "{f} {}", fired - last)?;
            last = fired;
        }
        fs::write(out.join(format!("{name}-pos.raw")), &pos)?;
        fs::write(out.join(format!("{name}-phase.raw")), &phase)?;
        fs::write(out.join(format!("{name}-tube.raw")), &tube)?;
        eprintln!("{name}: {} events over {frames} frames", c.metrics().fired);
    }
    Ok(())
}
