// B12 red-team probe: the 16 frozen ships' reference trajectories, raw (non-conserving) at three
// tolerances, plus one-ulp nudges of the initial state. Everything else (plants, statistics) is
// Python, independent of the gate's harness.
mod restricted;

use restricted::{Integrator, Model, Restricted, JUPITER};
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::mpsc;

pub const PERIODS: usize = 200;
pub const COARSE: usize = 8;

/// SplitMix64, as sample.rs.
struct Rng(u64);
impl Rng {
    fn next(&mut self) -> u64 {
        self.0 = self.0.wrapping_add(0x9E37_79B9_7F4A_7C15);
        let mut z = self.0;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
        z ^ (z >> 31)
    }
    fn unit(&mut self) -> f64 {
        (self.next() >> 11) as f64 / (1u64 << 53) as f64
    }
}

/// `n` handoff candidates, as sample::handoffs.
fn handoffs(n: usize) -> Vec<(f64, f64, f64)> {
    let mut rng = Rng(20261002);
    (0..n)
        .map(|_| {
            let side = if rng.next() >> 63 == 1 { 1.0 } else { -1.0 };
            let k = 1.5 + 1.5 * rng.unit();
            (side, k, (30.0 + 300.0 * rng.unit()).to_radians())
        })
        .collect()
}

/// sample::HANDOFF_KEPT.
const HANDOFF_KEPT: [usize; 16] = [32, 39, 53, 57, 70, 72, 78, 83, 85, 88, 101, 106, 138, 142, 148, 159];

/// handoff::ship.
fn ship(scene: &Restricted, side: f64, k: f64, alpha: f64) -> [f64; 4] {
    let r = scene.sep * (1.0 + side * scene.hill() / scene.sep * k);
    let v = r.powf(-0.5);
    [r * alpha.cos(), r * alpha.sin(), -v * alpha.sin(), v * alpha.cos()]
}

/// resonance::elements, (a, e) about the star (a in absolute units; divided by sep on output).
fn elements(scene: &Restricted, t: f64, s: &[f64; 4]) -> (f64, f64) {
    let (p, v) = scene.star(t);
    let (x, y, vx, vy) = (s[0] - p[0], s[1] - p[1], s[2] - v[0], s[3] - v[1]);
    let gm = 1.0 - scene.mu;
    let (r, v2, rv) = ((x * x + y * y).sqrt(), vx * vx + vy * vy, x * vx + y * vy);
    let k = v2 - gm / r;
    let (ex, ey) = ((k * x - rv * vx) / gm, (k * y - rv * vy) / gm);
    (1.0 / (2.0 / r - v2 / gm), ex.hypot(ey))
}

/// One ulp up (dir > 0) or down (dir < 0) in magnitude.
fn ulp(x: f64, dir: i64) -> f64 {
    if dir >= 0 { f64::from_bits(x.to_bits() + 1) } else { f64::from_bits(x.to_bits() - 1) }
}

fn main() {
    let scene = JUPITER;
    let draws = handoffs(HANDOFF_KEPT.iter().max().unwrap() + 1);
    let ships: Vec<[f64; 4]> = HANDOFF_KEPT.iter().map(|&i| ship(&scene, draws[i].0, draws[i].1, draws[i].2)).collect();
    let period = scene.period();
    let times: Vec<f64> = (0..=PERIODS * COARSE).map(|j| j as f64 * period / COARSE as f64).collect();

    // (name, rtol, nudge: None or (component, dir))
    let kinds: Vec<(&str, f64, Option<(usize, i64)>)> = vec![
        ("r11", 1e-11, None),
        ("r12", 1e-12, None),
        ("r13", 1e-13, None),
        ("nxp", 1e-12, Some((0, 1))),
        ("nxm", 1e-12, Some((0, -1))),
        ("nvxp", 1e-12, Some((2, 1))),
        ("nvyp", 1e-12, Some((3, 1))),
    ];

    let jobs: Vec<(usize, usize)> = (0..kinds.len()).flat_map(|k| (0..16).map(move |s| (k, s))).collect();
    let (tx, rx) = mpsc::channel::<(usize, usize, Option<Vec<f64>>, f64, usize)>();
    let counter = AtomicUsize::new(0);
    let scope_tx = tx.clone();
    std::thread::scope(|scope| {
        for _ in 0..4 {
            let tx = scope_tx.clone();
            let (jobs, kinds, ships, times, next) = (&jobs, &kinds, &ships, &times, &counter);
            scope.spawn(move || {
                let scene = JUPITER;
                loop {
                    let j = next.fetch_add(1, Ordering::Relaxed);
                    if j >= jobs.len() {
                        return;
                    }
                    let (ki, si) = jobs[j];
                    let (name, rtol, nudge) = kinds[ki];
                    let mut ic = ships[si];
                    if let Some((c, d)) = nudge {
                        ic[c] = ulp(ic[c], d);
                    }
                    let mut it = Integrator::new(&scene, Model::Full, rtol, ic).tracking();
                    let mut row = Vec::with_capacity(times.len() * 9);
                    let mut inside = scene.planet_distance(0.0, &ic) < scene.soi();
                    let mut crossings = 0usize;
                    let mut ok = true;
                    for &t in times.iter() {
                        let Some(st) = it.advance(t) else { ok = false; break };
                        let (a, e) = elements(&scene, t, &st);
                        let r2 = scene.planet_distance(t, &st);
                        let now = r2 < scene.soi();
                        crossings += (now != inside) as usize;
                        inside = now;
                        row.extend_from_slice(&[t, st[0], st[1], st[2], st[3], r2, a / scene.sep, e, scene.jacobi(t, &st)]);
                    }
                    println!("{name} ship {si}: {} (closest {:.3} planet radii, {crossings} soi crossings at P/8)", if ok { "ok" } else { "GAVE UP" }, it.closest() / scene.planet_radius);
                    tx.send((ki, si, if ok { Some(row) } else { None }, it.closest(), crossings)).unwrap();
                }
            });
        }
    });
    drop(scope_tx);
    drop(tx);

    let mut res: Vec<_> = rx.iter().collect();
    res.sort_by_key(|(ki, si, _, _, _)| (*ki, *si));
    std::fs::create_dir_all("out").unwrap();
    for (ki, _) in kinds.iter().enumerate() {
        let name = kinds[ki].0;
        let mut meta = String::new();
        let mut all = vec![f64::NAN; 16 * times.len() * 9];
        for (k, si, row, closest, crossings) in res.iter().filter(|(k, _, _, _, _)| *k == ki) {
            if let Some(r) = row {
                all[si * times.len() * 9..(si + 1) * times.len() * 9].copy_from_slice(r);
            }
            meta.push_str(&format!("{si} closest_planet_radii {:.6} crossings_p8 {crossings}\n", closest / scene.planet_radius));
        }
        let bytes: Vec<u8> = all.iter().flat_map(|x| x.to_le_bytes()).collect();
        std::fs::write(format!("out/{name}.f64"), bytes).unwrap();
        std::fs::write(format!("out/{name}_meta.txt"), meta).unwrap();
        println!("{name}: written");
    }
}
