//! Candidate B12 detector; local-affine slow-state adjustment, then exposure ranks.
//! Adapted from GLM 20261006-1545-q-b12-design-9242. Its published variance was
//! twice too large for a ship and inconsistent in the pool. Rank scores here
//! are diagnostics, NOT independent-sample significance: returns are correlated.
use super::handoff::{COARSE, FLOOR, PERIODS};
use super::restricted::Restricted;
// A recurrence within one standard deviation in normalized slow state.
const D_MAX: f64 = 1.0;
// Enough rows for two nuisance gradients and a separately identifiable time term.
const MIN_PAIRS: usize = 3;
// Two initial synodic periods; derived afresh from the ship's starting orbit.
fn gap(scene: &Restricted, ship: &[f64; 4]) -> f64 {
    let (a, _, _, _) = super::resonance::elements(scene, 0.0, ship);
    2.0 / (1.0 - (a / scene.sep).powf(-1.5)).abs()
}
pub struct ShipStat {
    pub z: f64,
    pub n: usize,
    pub ties: usize,
    pub worst: f64,
    pub gap_mean: f64,
    /// Median |Δ| of the matched pairs' error magnitudes: the state-gradient noise the leak must
    /// rise above (the detection floor's denominator).
    pub diff_med: f64,
    /// The dt coefficient: the error the law gains per horizon at a fixed state.
    pub leak: f64,
    pub above_floor: bool,
    pub bad: bool,
}

/// Match early and late far-field returns in standardized (a,e), without reuse.
/// Remove a through-origin affine gradient from the SIGNED Jacobi differences;
/// then rank residual magnitudes against exposure. The scale is the untied,
/// independent-rank variance; temporal dependence is NOT removed by this fit.
pub fn arrow(scene: &Restricted, ship: [f64; 4], times: &[f64], states: &[[f64; 4]]) -> ShipStat {
    let c0 = scene.jacobi(0.0, &ship);
    let mut bad = states.len() != times.len() || states.iter().flatten().any(|x| !x.is_finite());
    let cerr = |t: f64, s: &[f64; 4]| (scene.jacobi(t, s) - c0) / c0.abs();
    let err: Vec<f64> = if bad {
        vec![f64::INFINITY; times.len()]
    } else {
        times
            .iter()
            .zip(states)
            .map(|(&t, s)| cerr(t, s).abs())
            .collect()
    };
    bad |= err.iter().any(|e| !e.is_finite());
    let worst = err.iter().fold(0.0f64, |m, e| {
        if e.is_nan() || m.is_nan() {
            f64::NAN
        } else {
            m.max(*e)
        }
    });
    if bad {
        return ShipStat {
            z: f64::INFINITY,
            n: 0,
            ties: 0,
            worst: f64::INFINITY,
            gap_mean: 0.0,
            diff_med: 0.0,
            leak: 0.0,
            above_floor: true,
            bad: true,
        };
    }
    let far: Vec<usize> = (0..times.len())
        .filter(|&j| scene.planet_distance(times[j], &states[j]) > 3.0 * scene.hill())
        .collect();
    let el: Vec<Option<(f64, f64)>> = far
        .iter()
        .map(
            |&j| match super::resonance::elements(scene, times[j], &states[j]) {
                (a, e, _, _) if a.is_finite() && e.is_finite() => Some((a / scene.sep, e)),
                _ => None,
            },
        )
        .collect();
    let good: Vec<(f64, f64)> = el.iter().filter_map(|x| *x).collect();
    let (mut z, mut n, mut ties, mut gap_mean, mut diff_med, mut leak) =
        (0.0f64, 0usize, 0usize, 0.0f64, 0.0f64, 0.0f64);
    if good.len() >= MIN_PAIRS * 3 && !bad {
        let (ma, me) = good
            .iter()
            .fold((0.0, 0.0), |(a, e), (x, y)| (a + x, e + y));
        let (ma, me) = (ma / good.len() as f64, me / good.len() as f64);
        let sd = |xs: &[f64], m: f64| {
            (xs.iter().map(|x| (x - m) * (x - m)).sum::<f64>() / xs.len() as f64)
                .sqrt()
                .max(f64::EPSILON)
        };
        let (sa, se) = (
            sd(&good.iter().map(|x| x.0).collect::<Vec<_>>(), ma),
            sd(&good.iter().map(|x| x.1).collect::<Vec<_>>(), me),
        );
        let half = 0.5 * PERIODS as f64;
        let u = |x: (f64, f64)| ((x.0 - ma) / sa, (x.1 - me) / se);
        let mut used = vec![false; far.len()];
        // [da, de, dt, d_signed]
        let mut rows: Vec<[f64; 4]> = Vec::new();
        let mut gaps = Vec::new();
        for (idx, &i) in far.iter().enumerate() {
            if (i / COARSE) as f64 > half {
                continue;
            }
            let Some(ei) = el[idx] else { continue };
            let (ui, vi) = u(ei);
            let mut best: Option<(f64, usize)> = None;
            for (k, &j) in far.iter().enumerate() {
                if used[k] || (j / COARSE) as f64 <= half {
                    continue;
                }
                let dt = (j - i) as f64 / COARSE as f64;
                if dt < gap(scene, &ship) {
                    continue;
                }
                let Some(ej) = el[k] else { continue };
                let (uj, vj) = u(ej);
                let d2 = (ui - uj) * (ui - uj) + (vi - vj) * (vi - vj);
                if d2 > D_MAX * D_MAX {
                    continue;
                }
                if best.map_or(true, |(b, _)| d2 < b) {
                    best = Some((d2, k));
                }
            }
            if let Some((_, k)) = best {
                used[k] = true;
                let j = far[k];
                let dt = (j - i) as f64 / COARSE as f64;
                gaps.push(dt);
                let d = cerr(times[j], &states[j]) - cerr(times[i], &states[i]);
                {
                    let ((ai, ei2), (aj, ej)) = (el[idx].unwrap(), el[k].unwrap());
                    rows.push([(aj - ai) / sa, (ej - ei2) / se, dt / PERIODS as f64, d]);
                    ties += (d == 0.0) as usize;
                }
            }
        }
        n = rows.len();
        if n >= MIN_PAIRS {
            // The state adjustment: through-origin fit of d on (da, de).
            let mut xtx = [[0.0f64; 2]; 2];
            let mut xty = [0.0f64; 2];
            for r in &rows {
                for a in 0..2 {
                    xty[a] += r[a] * r[3];
                    for b in 0..2 {
                        xtx[a][b] += r[a] * r[b];
                    }
                }
            }
            if let Some(inv) = invert2(xtx) {
                let beta: Vec<f64> = (0..2)
                    .map(|a| (0..2).map(|b| inv[a][b] * xty[b]).sum())
                    .collect();
                let rs: Vec<(f64, f64)> = rows
                    .iter()
                    .map(|r| (r[2], (r[3] - (beta[0] * r[0] + beta[1] * r[1])).abs()))
                    .collect();
                z = rank_score(&rs);
                // The leak estimate: the dt coefficient of d ~ da + de + dt, its size per horizon.
                let mut x3y = [0.0f64; 3];
                let mut m33 = [[0.0f64; 3]; 3];
                for r in &rows {
                    let cols = [r[0], r[1], r[2]];
                    for a in 0..3 {
                        x3y[a] += cols[a] * r[3];
                        for b in 0..3 {
                            m33[a][b] += cols[a] * cols[b];
                        }
                    }
                }
                leak = match invert3(m33) {
                    Some(i3) => (0..3).map(|a| i3[2][a] * x3y[a]).sum::<f64>(),
                    None => 0.0,
                };
                let mut ad: Vec<f64> = rs.iter().map(|x| x.1).collect();
                ad.sort_by(f64::total_cmp);
                diff_med = ad[ad.len() / 2];
            } else {
                n = 0;
            }
        }
        gaps.sort_by(f64::total_cmp);
        gap_mean = gaps.iter().sum::<f64>() / gaps.len() as f64;
    }
    ShipStat {
        z,
        n,
        ties,
        worst,
        gap_mean,
        diff_med,
        leak,
        above_floor: worst > FLOOR,
        bad,
    }
}

/// The inverse of a symmetric positive-definite 2x2 matrix. None: singular.
fn invert2([[a, b], [_, d]]: [[f64; 2]; 2]) -> Option<[[f64; 2]; 2]> {
    let det = a * d - b * b;
    if det <= 0.0 || !(det.is_finite()) {
        return None;
    }
    Some([[d / det, -b / det], [-b / det, a / det]])
}

/// The inverse of a symmetric positive-definite 3x3 matrix. None: singular.
fn invert3(m: [[f64; 3]; 3]) -> Option<[[f64; 3]; 3]> {
    let (a, b, c) = (m[0][0], m[0][1], m[0][2]);
    let (d, e, f) = (m[1][1], m[1][2], m[2][2]);
    let det = a * (d * f - e * e) - b * (b * f - e * c) + c * (b * e - d * c);
    if det <= 0.0 || !det.is_finite() {
        return None;
    }
    let adj = |i: usize, j: usize| {
        let (p, q) = ((i + 1) % 3, (i + 2) % 3);
        let (r, s) = ((j + 1) % 3, (j + 2) % 3);
        m[p][r] * m[q][s] - m[p][s] * m[q][r]
    };
    let mut inv = [[0.0f64; 3]; 3];
    for i in 0..3 {
        for j in 0..3 {
            inv[i][j] = adj(j, i) / det;
        }
    }
    Some(inv)
}

/// Ties contribute zero; the untied variance is conservative for tied ranks.
fn rank_score(rs: &[(f64, f64)]) -> f64 {
    let mut sum = 0i64;
    for x in 0..rs.len() {
        for y in x + 1..rs.len() {
            let (a, b) = (rs[x].0 - rs[y].0, rs[x].1 - rs[y].1);
            if a != 0.0 && b != 0.0 {
                sum += if a * b > 0.0 { 1 } else { -1 };
            }
        }
    }
    let n = rs.len() as f64;
    if n < 2.0 {
        0.0
    } else {
        sum as f64 / (n * (n - 1.0) * (2.0 * n + 5.0) / 18.0).sqrt()
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn b12_rank_scale_has_the_exact_small_permutation_variance() {
        fn permutations(v: &mut [usize], at: usize, out: &mut Vec<f64>) {
            if at == v.len() {
                out.push(rank_score(
                    &v.iter()
                        .enumerate()
                        .map(|(i, x)| (i as f64, *x as f64))
                        .collect::<Vec<_>>(),
                ));
                return;
            }
            for j in at..v.len() {
                v.swap(at, j);
                permutations(v, at + 1, out);
                v.swap(at, j);
            }
        }
        let mut zs = Vec::new();
        permutations(&mut [0, 1, 2, 3, 4], 0, &mut zs);
        assert_eq!(zs.len(), 120);
        assert!(zs.iter().sum::<f64>().abs() < 1e-12);
        assert!((zs.iter().map(|x| x * x).sum::<f64>() / 120.0 - 1.0).abs() < 1e-12);
        assert_eq!(rank_score(&[(0.0, 1.0), (1.0, 1.0), (2.0, 1.0)]), 0.0);
    }
}

/// Add a known downward Jacobi leak while retaining the sampled positions.
/// Independently check the delivered invariant shift at every sample; power
/// cannot be certified by an injection that rounded away or saturated.
pub fn inject_leak(
    scene: &Restricted,
    ship: [f64; 4],
    times: &[f64],
    states: &[[f64; 4]],
    total: f64,
) -> Option<Vec<[f64; 4]>> {
    if states.len() != times.len() {
        return None;
    }
    let c0 = scene.jacobi(0.0, &ship).abs();
    let omega = scene.omega();
    states
        .iter()
        .zip(times)
        .map(|(s, &t)| {
            let want = c0 * total * t / (PERIODS as f64 * scene.period());
            let u = [s[2] + omega * s[1], s[3] - omega * s[0]];
            let speed2 = u[0] * u[0] + u[1] * u[1];
            if !(speed2 > 0.0 && speed2.is_finite()) {
                return None;
            }
            let gain = (1.0 + want / speed2).sqrt();
            let out = [
                s[0],
                s[1],
                gain * u[0] - omega * s[1],
                gain * u[1] + omega * s[0],
            ];
            let actual = scene.jacobi(t, &out) - scene.jacobi(t, s);
            if !actual.is_finite() || ((actual + want) / c0).abs() > FLOOR {
                None
            } else {
                Some(out)
            }
        })
        .collect()
}

/// Reference normalization, not an unconditional significance calculation.
pub fn pooled_score(stats: &[ShipStat]) -> f64 {
    let (mut sum, mut variance) = (0.0, 0.0);
    for st in stats {
        if st.above_floor && st.n >= MIN_PAIRS && !st.bad {
            let n = st.n as f64;
            let w = (n * (n - 1.0) * (2.0 * n + 5.0) / 18.0).sqrt();
            sum += st.z * w;
            variance += w * w;
        }
    }
    if variance > 0.0 {
        sum / variance.sqrt()
    } else {
        0.0
    }
}
