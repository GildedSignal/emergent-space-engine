//! Gates for `xtask galaxy`, frozen before the first run. Run with `cargo test --release -p xtask galaxy`
//! (the lattice compile test is ~30× slower in a debug build).
use super::draw::{Opts, Renderer, View};
use super::scene::{allocate, cell_valid, parallel, Config, KeyRec, Scene, CELLS, NE, NP};

/// G-track: the drawn (r, angle) is within 1e-4 of r and 1e-4 rad of the integer law's readout.
const TRACK_R_REL: f64 = 1e-4;
const TRACK_ANGLE_RAD: f64 = 1e-4;
/// G-conserve: the density image of a whole-galaxy view holds the ship count to 1e-4 (f32 planes).
const CONSERVE_REL: f64 = 1e-4;

fn scene(tubes: u64, ships: u64, seed: u64, family_size: u64, threads: usize) -> Scene {
    Scene::build(&Config { seed, ships, tubes, family_size, fleets: 0.3, threads }).unwrap()
}

#[test]
fn the_lattice_is_all_compilable_orbits() {
    let cells: Vec<usize> = (0..CELLS).filter(|&c| cell_valid(c)).collect();
    assert!(cells.len() > 8000, "{}", cells.len());
    let errs: Vec<Option<String>> = parallel(cells.len(), 4, |i| KeyRec::build(cells[i]).err());
    assert!(errs.iter().all(|e| e.is_none()), "{:?}", errs.iter().flatten().take(3).collect::<Vec<_>>());
}

#[test]
fn allocation_is_exact_and_deterministic() {
    let w: Vec<f64> = (1..200).map(|i| (i as f64).sqrt()).collect();
    for total in [0u64, 1, 199, 12_345, 1_000_000_007] {
        let a = allocate(total, &w);
        assert_eq!(a.iter().sum::<u64>(), total);
        assert_eq!(a, allocate(total, &w));
    }
}

#[test]
fn a_familys_materialized_ships_are_the_same_on_every_call() {
    let a = scene(2000, 3_000_000, 7, 50_000, 1);
    let b = scene(2000, 3_000_000, 7, 50_000, 4);
    let c = scene(2000, 3_000_000, 8, 50_000, 4);
    assert_eq!(a.families, b.families, "the family generators are the same, whatever the thread count");
    assert_eq!(a.tubes, b.tubes, "tubes are the same, whatever the thread count");
    assert_ne!(a.families, c.families, "another seed is another galaxy");
    let mut distinct = 0;
    for f in 0..a.families.len() {
        let n = a.families[f].count;
        for i in [0, 1, 7, n / 3, n / 2, n - 1] {
            let (x, y, z) = (a.materialize(f, i), a.materialize(f, i), b.materialize(f, i));
            assert_eq!(x, y);
            assert_eq!(x, z);
            distinct += usize::from(x != c.materialize(f, i));
        }
    }
    assert!(distinct > 0);
    // A ship's phase lies inside its family's window: fleets are narrow, belts wrap the orbit.
    for (f, fam) in a.families.iter().enumerate() {
        for i in 0..fam.count.min(500) {
            let s = a.materialize(f, i);
            let period = a.keys[s.key as usize].period as f64;
            let frac = s.tube.phase.get() as f64 / period;
            assert!(frac >= fam.ph0 - 1e-9 && frac <= fam.ph0 + fam.width + 1e-9, "{frac} outside [{}, +{}]", fam.ph0, fam.width);
        }
    }
}

#[test]
fn drawn_ships_are_exactly_the_materialized_ones_when_the_budget_allows() {
    // Two families; a budget far above their counts: every ship is drawn once, at weight 1.
    let s = scene(0, 20_000, 3, 10_000, 2);
    let v = View { w: 400, h: 400, cx: 0.0, cy: 0.0, scale: 2.0 * 22000.0 / 400.0, t: 123_456_789 };
    let o = Opts { threads: 2, tube_cap: 1 << 30, fam_budget: 1 << 30 };
    let mut r = Renderer::new();
    let st = r.accumulate(&s, &v, &o);
    assert_eq!(st.materialized, 20_000);
    assert_eq!(st.fam_samples, 20_000);
    // The same plane, built by materializing every ship on this test's side.
    let sc = super::draw::sincos_table();
    let mut expect = vec![0u32; 400 * 400];
    for (f, fam) in s.families.iter().enumerate() {
        for i in 0..fam.count {
            let ship = s.materialize(f, i);
            let (rad, a) = s.keys[ship.key as usize].locate(v.t.wrapping_add(ship.tube.phase.get()));
            let a = a.wrapping_add(ship.omega0);
            let (c, sn) = (sc[(a >> 20) as usize], sc[(a >> 20) as usize + 1]);
            let f = ((a >> 4) & 0xFFFF) as f32 / 65536.0;
            let (cos, sin) = (c[0] + (sn[0] - c[0]) * f, c[1] + (sn[1] - c[1]) * f);
            let px = (rad as f64 * cos as f64) / v.scale + 200.0;
            let py = (rad as f64 * sin as f64) / v.scale + 200.0;
            if (0.0..400.0).contains(&px) && (0.0..400.0).contains(&py) {
                expect[py as usize * 400 + px as usize] += 1;
            }
        }
    }
    let mut out = Vec::new();
    r.tone(400, 400, 2, &mut out);
    let got: f64 = r.plane_sum();
    assert_eq!(got as u64, expect.iter().map(|&x| x as u64).sum::<u64>());
    assert_eq!(r.plane_pixels(400 * 400).iter().zip(&expect).filter(|(a, b)| **a != **b as f32).count(), 0);
}

#[test]
fn drawn_positions_agree_with_cycle_readouts() {
    let mut worst = (0.0f64, 0.0f64);
    // Extremes of the lattice, and a spread of ordinary orbits.
    let mut cells = vec![];
    let emax = |ip: usize| (0..NE).rev().find(|&ie| cell_valid(ip * NE + ie)).unwrap();
    for ip in [0, 1, 40, 100, 160, 220, NP - 1] {
        cells.extend([ip * NE, ip * NE + emax(ip), ip * NE + emax(ip) / 2]);
    }
    let times: [u64; 6] = [0, 1_000_003, 987_654_321_012, 77_000_000_000_000, 3_000_000_000_000_000, 9_000_000_000_000_000];
    for &cell in &cells {
        let rec = KeyRec::build(cell).unwrap();
        let period = rec.period;
        assert!((rec.locate(0).0 - rec.rmin).abs() / rec.rmin < 1e-5, "periapsis");
        assert!((rec.locate(rec.half).0 - rec.rmax).abs() / rec.rmax < 1e-5, "apoapsis");
        for k in 0..97u64 {
            let phase = period / 97 * k + k * 7;
            for &t in &times {
                let e = t + phase;
                let (r, a) = rec.locate(e);
                let (xr, xturns) = rec.exact(e).expect("readout");
                let dr = (r as f64 - xr).abs() / xr;
                let mut da = (a as f64 / 4294967296.0 - xturns).abs();
                da = da.min(1.0 - da) * std::f64::consts::TAU;
                worst = (worst.0.max(dr), worst.1.max(da));
                assert!(dr <= TRACK_R_REL, "cell {cell} e {e}: r {r} vs {xr} (rel {dr:e})");
                assert!(da <= TRACK_ANGLE_RAD, "cell {cell} e {e}: angle error {da:e} rad");
            }
        }
    }
    println!("track vs exact readouts: worst r rel {:e}, worst angle {:e} rad over {} orbits", worst.0, worst.1, cells.len());
}

#[test]
fn a_single_tube_lands_on_its_exact_pixel() {
    let s = scene(1, 1, 5, 1, 1);
    let rec = &s.keys[s.tube_groups[0].key as usize];
    let tube = s.tubes[0];
    let scale = 20.0;
    let t = 5_000_000_000_000u64;
    let v = View { w: 2000, h: 2000, cx: 0.0, cy: 0.0, scale, t };
    let mut r = Renderer::new();
    r.accumulate(&s, &v, &Opts { threads: 1, tube_cap: 10, fam_budget: 10 });
    let lit: Vec<usize> = r.plane_pixels(2000 * 2000).iter().enumerate().filter(|(_, &d)| d > 0.0).map(|(i, _)| i).collect();
    assert_eq!(lit.len(), 1);
    let (xr, xturns) = rec.exact(t + tube.phase.get()).unwrap();
    let ang = xturns * std::f64::consts::TAU;
    let (px, py) = (xr * ang.cos() / scale + 1000.0, xr * ang.sin() / scale + 1000.0);
    let (gx, gy) = ((lit[0] % 2000) as f64 + 0.5, (lit[0] / 2000) as f64 + 0.5);
    assert!((gx - px).abs() < 1.5 && (gy - py).abs() < 1.5, "drew ({gx}, {gy}), exact ({px:.2}, {py:.2})");
}

#[test]
fn the_density_at_far_zoom_conserves_the_ship_count() {
    let s = scene(30_000, 30_000_000, 11, 100_000, 3);
    assert_eq!(s.total_ships, 30_000_000);
    let far = |w: usize, h: usize| View { w, h, cx: 0.0, cy: 0.0, scale: 2.0 * super::server::R_FAR / h as f64, t: 41_000_000_000_000 };
    let mut r = Renderer::new();
    // Every tube drawn and the family budget above one sample per pixel; then strided tubes and a thin family budget.
    for (o, label) in [
        (Opts { threads: 3, tube_cap: 1 << 30, fam_budget: 1 << 30 }, "all"),
        (Opts::for_size(480, 270, 3), "one sample per pixel"),
        (Opts { threads: 2, tube_cap: 5000, fam_budget: 3000 }, "starved"),
    ] {
        let v = far(480, 270);
        let st = r.accumulate(&s, &v, &o);
        let sum = r.plane_sum();
        let rel = (sum - s.total_ships as f64).abs() / s.total_ships as f64;
        println!("{label}: {} samples stand for {sum:.0} of {} ships (rel {rel:e}); stride {}, m_max {}", st.samples, s.total_ships, st.stride, st.m_max);
        assert!(rel < CONSERVE_REL, "{label}: image holds {sum} of {}", s.total_ships);
    }
}

#[test]
fn the_memo_shares_cycles() {
    let s = scene(200_000, 200_000_000, 2, 100_000, 4);
    let st = &s.stats;
    assert!(st.compiled <= st.cells_valid);
    assert_eq!(st.lookups, 200_000 + s.cell_groups.iter().map(|&g| g as u64).sum::<u64>());
    assert!(st.hit_rate > 0.9, "hit rate {}", st.hit_rate);
    assert!((st.hit_rate - (1.0 - st.compiled as f64 / st.lookups as f64)).abs() < 1e-12);
}

#[test]
fn the_view_query_refuses_what_it_cannot_draw() {
    use super::server::view_of;
    assert!(view_of("w=640&h=480&cx=1&cy=-2&scale=3.5&t=99").is_ok());
    for bad in ["w=8", "w=4000", "scale=0", "scale=1e9", "cx=nan", "t=-1", "w=abc", "scale"] {
        assert!(view_of(bad).is_err(), "{bad}");
    }
}
