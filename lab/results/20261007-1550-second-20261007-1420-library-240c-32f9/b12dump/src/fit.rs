//! The growth-exponent fit of the v1 probe 2 (`gv1b.fit_slope`, `run_energy.py`): the slope of
//! log|error| against log t. Errors that stay bounded give 0, a random walk 0.5, a steady drift 1.
//! Where the probe fitted the running maximum on cycles 10^3..10^4 of one series, this fits the
//! last 90% of any series in log-spaced windows, so it needs no cycle count.

/// Number of log-spaced windows.
const WINDOWS: usize = 16;

/// The growth exponent of `err`, where `err[k]` is the error magnitude after cycle `k`
/// (`err[0]` is the reference cycle). The first 10% is dropped, the rest is cut into
/// `WINDOWS` windows of equal ratio in `k`, and each window contributes its largest error at its
/// geometric-mean cycle; the result is the least-squares slope over the windows.
///
/// - An error that is exactly zero throughout has exponent 0.
/// - NaN, infinity, a series too short to fill half the windows (under about 50 cycles), or
///   fewer than 3 nonzero windows give NaN, so the comparison `exponent <= limit` fails.
pub fn growth_exponent(err: &[f64]) -> f64 {
    let n = err.len();
    let first = (n / 10).max(1);
    if n <= first || err.iter().any(|e| !e.is_finite()) {
        return f64::NAN;
    }
    let edge = |j: usize| if j == WINDOWS { n } else { (first as f64 * (n as f64 / first as f64).powf(j as f64 / WINDOWS as f64)).round() as usize };
    let (mut used, mut pts) = (0, Vec::new());
    for j in 0..WINDOWS {
        let (a, b) = (edge(j), edge(j + 1));
        if b <= a {
            continue;
        }
        used += 1;
        let top = err[a..b].iter().fold(0.0f64, |m, e| m.max(e.abs()));
        if top > 0.0 {
            pts.push((((a * (b - 1)) as f64).sqrt().ln(), top.ln()));
        }
    }
    if used < WINDOWS / 2 {
        return f64::NAN;
    }
    if pts.is_empty() {
        return 0.0;
    }
    if pts.len() < 3 {
        return f64::NAN;
    }
    let m = pts.len() as f64;
    let (mx, my) = (pts.iter().map(|p| p.0).sum::<f64>() / m, pts.iter().map(|p| p.1).sum::<f64>() / m);
    pts.iter().map(|p| (p.0 - mx) * (p.1 - my)).sum::<f64>() / pts.iter().map(|p| (p.0 - mx).powi(2)).sum::<f64>()
}

