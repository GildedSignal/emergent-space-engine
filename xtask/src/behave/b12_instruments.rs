//! B12 v3: the non-overlapping R1 Allan estimator and decade running maxima.
//! IEEE measurements cross once into signed Q40; only integers decide thereafter.
//! The retired v2 fit remains in b12_stat as a diagnostic, never a verdict.
use num_bigint::BigUint;
use num_traits::ToPrimitive;
use serde::Serialize;

pub const SCALE: i128 = 1 << 40;
pub const HORIZON: usize = 10_000;
pub const SAMPLES_PER_PERIOD: usize = 8;

#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum Verdict {
    Pass,
    Fail,
    Missing,
}

/// Do not let Rust's saturating float-to-integer cast turn junk into evidence.
/// Round to nearest, ties to even, as in the lab's Python integerization.
pub fn integerize(relative: f64) -> Option<i64> {
    let q = (relative * SCALE as f64).round_ties_even();
    if !q.is_finite() || q < i64::MIN as f64 || q >= -(i64::MIN as f64) {
        None
    } else {
        Some(q as i64)
    }
}

#[derive(Debug, Serialize)]
pub struct Reading {
    pub verdict: Verdict,
    /// Report only. No floating-point value is read by the decision path.
    pub value: Option<f64>,
    /// Exact deciding numerator and denominator, also for independent replay.
    pub numerator: String,
    pub denominator: String,
}
impl Reading {
    fn missing() -> Self {
        Self {
            verdict: Verdict::Missing,
            value: None,
            numerator: "0".into(),
            denominator: "0".into(),
        }
    }
}

/// AVAR(m) = Σ(S[k+1]−S[k])² / (2 m² (K−1)), with exact block sums.
/// No rounding of means, no overlapping variant, no adjustment to zero variance.
fn avar(xs: &[i64], m: usize) -> Option<(BigUint, BigUint)> {
    if m == 0 || xs.len() % m != 0 || xs.len() / m < 2 {
        return None;
    }
    let sums: Vec<i128> = xs
        .chunks_exact(m)
        .map(|b| b.iter().map(|&x| x as i128).sum())
        .collect();
    let num = sums
        .windows(2)
        .map(|s| BigUint::from((s[1] - s[0]).unsigned_abs()).pow(2))
        .sum();
    let den = BigUint::from(2usize) * BigUint::from(m).pow(2) * BigUint::from(sums.len() - 1);
    Some((num, den))
}

pub fn allan(xs: &[i64]) -> Reading {
    if xs.len() < 32 || xs.len() % 32 != 0 {
        return Reading::missing();
    }
    let (n4, d4) = avar(xs, xs.len() / 4).unwrap();
    let (n32, d32) = avar(xs, xs.len() / 32).unwrap();
    let (a, b) = (n4 * d32, n32 * d4);
    let verdict = if a > b { Verdict::Fail } else { Verdict::Pass };
    let value = if b == BigUint::from(0usize) {
        None
    } else {
        Some(a.to_f64().unwrap() / b.to_f64().unwrap())
    };
    Reading {
        verdict,
        value,
        numerator: a.to_string(),
        denominator: b.to_string(),
    }
}

/// α_top = log10(M(T)/M(T/10)). α_top <= 1/5 iff M(T)^5 <= 10 M(T/10)^5.
/// Values at or below the reporting floor do not assert growth. Above-floor
/// growth from an unresolved starting maximum fails; it cannot quietly pass.
pub fn alpha(lo: u64, hi: u64) -> Reading {
    if hi < lo {
        return Reading::missing();
    }
    let (a, b) = (BigUint::from(hi).pow(5), BigUint::from(lo).pow(5) * 10u32);
    let verdict = if (hi as i128) * 1_000_000_000_000i128 <= SCALE || a <= b {
        Verdict::Pass
    } else {
        Verdict::Fail
    };
    let value = if hi == 0 {
        Some(0.0)
    } else if lo == 0 {
        None
    } else {
        Some((hi as f64 / lo as f64).log10())
    };
    Reading {
        verdict,
        value,
        numerator: a.to_string(),
        denominator: b.to_string(),
    }
}

#[derive(Debug, Serialize)]
pub struct Ship {
    pub ordinal: usize,
    pub n: usize,
    pub allan: Reading,
    pub alpha: Reading,
    pub maxima_q40: Vec<u64>,
    pub error_q40: u64,
    pub envelope_pass: bool,
    pub verdict: Verdict,
    pub disagreement: bool,
}

/// xs includes t=0; Allan uses the N samples ending at T, not N+1 uneven blocks.
/// Every original sample contributes to the running maxima and magnitude cap.
pub fn judge(ordinal: usize, xs: &[i64]) -> Ship {
    let complete = xs.len() == HORIZON * SAMPLES_PER_PERIOD + 1;
    let mut max = 0u64;
    let mut maxima = Vec::new();
    for (i, x) in xs.iter().enumerate() {
        max = max.max(x.unsigned_abs());
        if [1, 10, 100, 1000, 10000]
            .iter()
            .any(|&p| i == p * SAMPLES_PER_PERIOD)
        {
            maxima.push(max);
        }
    }
    let a = if complete {
        allan(&xs[1..])
    } else {
        Reading::missing()
    };
    let b = if complete {
        alpha(maxima[3], maxima[4])
    } else {
        Reading::missing()
    };
    let envelope_pass = complete && max as i128 * 10_000 <= SCALE;
    let disagreement = complete && a.verdict != b.verdict;
    let verdict = if !complete {
        Verdict::Missing
    } else if !envelope_pass || (a.verdict == Verdict::Fail && b.verdict == Verdict::Fail) {
        Verdict::Fail
    } else if disagreement {
        Verdict::Missing
    } else {
        Verdict::Pass
    };
    Ship {
        ordinal,
        n: xs.len(),
        allan: a,
        alpha: b,
        maxima_q40: maxima,
        error_q40: max,
        envelope_pass,
        verdict,
        disagreement,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn b12_integerization_rejects_junk_and_rounds_even() {
        assert_eq!(integerize(f64::NAN), None);
        assert_eq!(integerize(f64::INFINITY), None);
        assert_eq!(integerize(2f64.powi(23)), None);
        assert_eq!(integerize(0.5 / SCALE as f64), Some(0));
        assert_eq!(integerize(1.5 / SCALE as f64), Some(2));
        assert_eq!(integerize(-1.5 / SCALE as f64), Some(-2));
    }
    #[test]
    fn b12_allan_exact_boundary_and_offset_invariance() {
        let flat = vec![27; 320];
        assert_eq!(allan(&flat).verdict, Verdict::Pass); // equality is PASS
        let ramp: Vec<i64> = (0..320).collect();
        let a = allan(&ramp);
        assert_eq!(a.verdict, Verdict::Fail);
        assert_eq!(a.value, Some(64.0));
        assert_eq!(
            a.numerator,
            allan(&ramp.iter().map(|x| x + 1_000_000).collect::<Vec<_>>()).numerator
        );
        assert_eq!(
            allan(&ramp.iter().map(|x| -x * 16).collect::<Vec<_>>()).verdict,
            a.verdict
        );
        let periodic: Vec<i64> = (0..320).map(|i| if i % 2 == 0 { 1 } else { -1 }).collect();
        assert_eq!(allan(&periodic).verdict, Verdict::Pass);
        assert_eq!(allan(&[0; 31]).verdict, Verdict::Missing);
    }
    #[test]
    fn b12_alpha_has_an_exact_fifth_power_threshold() {
        assert_eq!(alpha(10_000, 15_848).verdict, Verdict::Pass);
        assert_eq!(alpha(10_000, 15_849).verdict, Verdict::Fail);
        assert_eq!(alpha(0, 1).verdict, Verdict::Pass); // below floor
        assert_eq!(alpha(0, 2).verdict, Verdict::Fail);
        assert_eq!(alpha(1, 0).verdict, Verdict::Missing);
        assert_eq!(alpha(u64::MAX / 2, u64::MAX).verdict, Verdict::Fail); // no overflow
    }
    #[test]
    fn b12_per_ship_minority_and_disagreement_cannot_be_pooled_away() {
        let flat = vec![0; HORIZON * SAMPLES_PER_PERIOD + 1];
        let ramp: Vec<i64> = (0..flat.len()).map(|i| i as i64).collect();
        assert_eq!(judge(0, &flat).verdict, Verdict::Pass);
        assert_eq!(judge(1, &ramp).verdict, Verdict::Fail);
        assert_eq!(judge(0, &flat[..80000]).verdict, Verdict::Missing);
        let step: Vec<i64> = (0..flat.len())
            .map(|i| if i > flat.len() / 2 { 100 } else { 0 })
            .collect();
        let s = judge(0, &step);
        assert!(!s.envelope_pass || s.verdict != Verdict::Pass);
    }
    #[test]
    fn b12_envelope_integer_boundary_and_all_samples_count() {
        let cap = (SCALE / 10_000) as i64;
        let mut xs = vec![cap; HORIZON * SAMPLES_PER_PERIOD + 1];
        assert!(judge(0, &xs).envelope_pass);
        xs[17] = cap + 1;
        assert!(!judge(0, &xs).envelope_pass);
    }
}
