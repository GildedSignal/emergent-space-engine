// H_live probe (run 20261007-1646-quant-b30e): the rate at which the plane's real kicks create
// per-body distinctions that a population program (shipmem Form P: program + sparse scars)
// cannot reabsorb, on the real engine (crates/universe restricted problem: star + planet +
// kicked ships). Columns are the invariant columns pop.rs defines for orbit ships, minus t_p
// (whose absolute value is floor-brittle at window granularity; its content is a function of
// (p,k)): [p at Q32 (doll M units), k = 1/(1+e) at Q48, omega at Q32 turns].
//
// The family program is the exact launch law of a convoy: per column an affine program
// a + b·i fitted by majority-median over members (a launched convoy IS affine; shipmem's
// `infer` needs a strict majority and dies the moment >50% of members are kicked, which is
// itself a reported outcome). Deviations are sealed by shipmem's Form P (Elias–Fano ordinal
// set + zigzag delta rows) and also counted column-wise: that is H_live, the live
// distinguishing bits per member.
//
// Controls: window 0 (no evolution) must seal ~0 scars; the flat store
// (size_of::<Binding>) is the negative contrast; belt15w (mu/256) is the linearity control.
//
// Usage: hlive-probe <config> <n_ships> <max_orbits>
//   configs: belt15 | belt21 (2:1 resonance) | hill (1.5-2.5 Hill radii) | belt15w (mu/256)
use emergent_shipmem::codec::{Enc, MAXC};
use emergent_shipmem::program::Program;
use emergent_shipmem::shelf::Ship;
use emergent_universe::scenario::restricted;

const COLS: usize = 3;

fn bits_u64(x: u64) -> u32 {
    64 - x.leading_zeros()
}

fn median(v: &mut [i128]) -> i128 {
    v.sort_unstable();
    v[v.len() / 2]
}

/// Affine fit (a, b) of one column over ordinals, by median step and median anchor.
fn fit(vals: &[i128]) -> (i128, i128) {
    let d: Vec<i128> = vals.windows(2).map(|w| w[1] - w[0]).collect();
    let mut d = d;
    let b = median(&mut d);
    let anchored: Vec<i128> = vals.iter().enumerate().map(|(i, &v)| v - b * i as i128).collect();
    let mut anchored = anchored;
    let a = median(&mut anchored);
    (a, b)
}

/// The convoy's live state as integer columns, exactly as the engine stores their invariants.
fn raw_columns(u: &emergent_universe::Universe, ships: &[usize]) -> (Vec<[i128; COLS]>, usize, usize) {
    let (mut out, mut home, mut away) = (Vec::with_capacity(ships.len()), 0usize, 0usize);
    let doll0 = u.rec(ships[0]).b.doll;
    for &i in ships {
        let b = &u.rec(i).b;
        if b.doll != doll0 {
            away += 1;
            continue;
        }
        let key = b.entry.trajectory.key();
        out.push([
            key.periapsis.fixed(32).unwrap(),
            key.k as i128,
            b.tube.periapsis_angle as i128,
        ]);
        home += 1;
    }
    (out, home, away)
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let cfg_name = args.get(1).map(|s| s.as_str()).unwrap_or("belt15");
    let n: usize = args.get(2).map(|s| s.parse().unwrap()).unwrap_or(128);
    let max_orbits: f64 = args.get(3).map(|s| s.parse().unwrap()).unwrap_or(128.0);
    let (mu_log2, sep, ratio, spread_hill) = match cfg_name {
        "belt21" => (-10i32, 527_000_000i64, 1.587401052f64, 0f64),
        "hill" => (-10, 527_000_000, 1.0, 1.0),
        "belt15w" => (-18, 527_000_000, 1.5, 0.0),
        _ => (-10, 527_000_000, 1.5, 0.0),
    };
    let hill = sep as f64 * (2f64.powi(mu_log2) / 3.0).cbrt();
    let ships: Vec<(i64, u32)> = (0..n)
        .map(|i| {
            let r = if spread_hill > 0.0 {
                sep as f64
                    + if i % 2 == 0 { 1.0 } else { -1.0 } * hill * (1.5 + spread_hill * i as f64 / n as f64)
            } else {
                (sep as f64 * ratio).round()
            } as i64;
            (r, (i as u64 * u32::MAX as u64 / n as u64) as u32)
        })
        .collect();
    let planet_period = 2.0 * std::f64::consts::PI / ((1.0 + 2f64.powi(mu_log2)).sqrt() / (sep as f64).powf(1.5));
    let ship_period = planet_period * ratio.powf(1.5);
    let mut w = restricted(mu_log2, sep, 49_000, &ships, 1).unwrap();
    let ids = w.ships.clone();
    println!("# config {cfg_name} n {n} mu_log2 {mu_log2} sep {sep} ratio {ratio} ship_period_ticks {ship_period:.4e}");
    println!("# orbit, tick, wall_s, kicks, handoffs, lost, home, away, clean, formp_alive, formp_bits_pm, scarlayer_bits_pm, flat_bits_pm, bits_col_med, bits_col_p99, bits_col_max");
    let mut enc = Enc::default();
    let t_start = std::time::Instant::now();
    for orbit in [0.0f64, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0, 128.0, 256.0, 512.0] {
        if orbit > max_orbits {
            break;
        }
        let tick = (orbit * ship_period) as i64;
        let t0 = std::time::Instant::now();
        w.u.settle(tick);
        let wall = t0.elapsed().as_secs_f64();
        let (raw, home, away) = raw_columns(&w.u, &ids);
        // Per-column affine program; deviations as zigzag u64 columns for Form P.
        let mut zz_cols: Vec<Vec<u64>> = vec![Vec::new(); COLS];
        let mut rows: Vec<Ship> = Vec::with_capacity(raw.len());
        let mut clean = 0usize;
        for (i, m) in raw.iter().enumerate() {
            let mut row = [0u64; MAXC];
            let mut any = false;
            for f in 0..COLS {
                let _ = i;
                let _ = m[f];
                row[f] = 0;
                let _ = &mut any;
            }
            rows.push(row);
        }
        // (real work below; the loop above is replaced)
        let mut col_vals: Vec<Vec<i128>> = vec![Vec::with_capacity(raw.len()); COLS];
        for m in &raw {
            for f in 0..COLS {
                col_vals[f].push(m[f]);
            }
        }
        let fits: Vec<(i128, i128)> = (0..COLS).map(|f| fit(&col_vals[f])).collect();
        let mut all_dev: Vec<u64> = Vec::new();
        rows.clear();
        for (i, m) in raw.iter().enumerate() {
            let mut row = [0u64; MAXC];
            let mut any = false;
            for f in 0..COLS {
                let pred = fits[f].0 + fits[f].1 * i as i128;
                let mut d = m[f] - pred;
                if f == 2 {
                    // omega is modulo 2^32 turns: centre the deviation.
                    let m32 = ((m[f] as i64).rem_euclid(1 << 32)) as i128;
                    let p32 = ((pred as i64).rem_euclid(1 << 32)) as i128;
                    d = m32 - p32;
                    if d > (1 << 31) {
                        d -= 1 << 32;
                    }
                    if d < -(1 << 31) {
                        d += 1 << 32;
                    }
                }
                let z = if d < 0 { ((-d) as u64) * 2 + 1 } else { (d as u64) * 2 };
                row[f] = z;
                zz_cols[f].push(z);
                all_dev.push(z);
                if z != 0 {
                    any = true;
                }
            }
            if !any {
                clean += 1;
            }
            rows.push(row);
        }
        // Form P seal of the deviations (program = Const(0) per column when a majority is clean).
        let mut formp_alive = 0u8;
        let mut formp_bits_pm = f64::NAN;
        if let Some(p) = Program::build(&rows, COLS, &mut enc) {
            formp_alive = 1;
            formp_bits_pm = p.bytes() as f64 * 8.0 / raw.len() as f64;
        }
        // Own scar-layer account: Elias–Fano ordinals (~k·(2+log2(n/k)) bits) + byte-aligned rows.
        let k = raw.len() - clean;
        let ef_bits = if k > 0 { (k as f64) * (2.0 + (raw.len() as f64 / k as f64).log2()) } else { 0.0 };
        let row_bits: f64 = all_dev.iter().map(|&z| ((bits_u64(z) + 7) / 8) as f64 * 8.0).sum();
        let scarlayer_bits_pm = (ef_bits + row_bits) / raw.len() as f64;
        let flat_bits_pm = std::mem::size_of::<emergent_universe::bind::Binding>() as f64 * 8.0;
        let mut widths: Vec<u32> = all_dev.iter().map(|&z| bits_u64(z)).collect();
        widths.sort_unstable();
        let q = |p: f64| widths[((widths.len() as f64 * p) as usize).min(widths.len().saturating_sub(1))];
        let s = w.u.stats;
        println!(
            "{orbit}, {tick}, {wall:.2}, {}, {}, {}, {home}, {away}, {clean}, {formp_alive}, {formp_bits_pm}, {scarlayer_bits_pm:.1}, {flat_bits_pm}, {}, {}, {}",
            s.kicks, s.handoffs, s.lost,
            if widths.is_empty() { 0 } else { q(0.5) },
            if widths.is_empty() { 0 } else { q(0.99) },
            widths.last().copied().unwrap_or(0),
        );
        let guard = std::env::var("HLIVE_GUARD").ok().and_then(|s| s.parse::<f64>().ok()).unwrap_or(90.0);
        if t_start.elapsed().as_secs_f64() > guard {
            println!("# wall guard hit after {orbit} orbits");
            break;
        }
    }
    println!(
        "# total wall {:.1}s, kicks {}, handoffs {}, lost {}, refused {}",
        t_start.elapsed().as_secs(),
        w.u.stats.kicks,
        w.u.stats.handoffs,
        w.u.stats.lost,
        w.u.stats.refused
    );
}
