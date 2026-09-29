fn gauss_legendre(n: usize) -> Vec<(f64, f64)> {
    (1..=n)
        .map(|i| {
            let mut x = (PI * (i as f64 - 0.25) / (n as f64 + 0.5)).cos();
            let mut dp = 0.0;
            for _ in 0..100 {
                let (mut p0, mut p1) = (1.0, x);
                for k in 2..=n {
                    let p2 = ((2 * k - 1) as f64 * x * p1 - (k - 1) as f64 * p0) / k as f64;
                    (p0, p1) = (p1, p2);
                }
                dp = n as f64 * (x * p1 - p0) / (x * x - 1.0);
                let dx = p1 / dp;
                x -= dx;
                if dx.abs() < 1e-16 {
                    break;
                }
            }
            (x, 2.0 / ((1.0 - x * x) * dp * dp))
        })
        .collect()
}

pub(crate) fn deflection_quadrature(b: f64) -> f64 {
    let mut u0 = 1.0 / b;
    for _ in 0..100 {
        let (h, dh) = (2.0 * u0 * u0 * u0 - u0 * u0 + 1.0 / (b * b), 6.0 * u0 * u0 - 2.0 * u0);
