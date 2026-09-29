//! The contract's interface (docs/gravity-law.md, "The interface"), mirrored for the harness.
//!
//! The canonical crate `emergent-geodesic` has no merged public API yet. These types have the
//! same names and shapes as the crate's, so wiring is a field-by-field conversion in
//! `adapter.rs`, or later a `pub use emergent_geodesic::{...}` in place of these definitions.
use crate::Result;
use serde_json::{json, Value};
use std::fmt;

#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub struct Field {
    pub m: i128,
}
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub struct Anchor {
    pub t: i128,
    pub x: [i128; 2],
    pub k: [i128; 2],
}
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub enum Motion {
    Timelike,
    Null,
}
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum At {
    Free([i128; 2]),
    Absorbed { chronon: i128 },
    OutOfRange { chronon: i128 },
    Before,
}
/// Construction failed. The message is the crate's own `AnchorError` text.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct AnchorError(pub String);
impl fmt::Display for AnchorError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.0)
    }
}
/// The crate's classes; the harness constructs only the ones the judge names.
#[allow(dead_code)]
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum OrbitClass {
    Bound,
    Unbound,
    Marginal,
    Plunging,
    Radial,
    Circular,
    Separatrix,
}
impl OrbitClass {
    pub fn name(self) -> &'static str {
        match self {
            OrbitClass::Bound => "bound",
            OrbitClass::Unbound => "unbound",
            OrbitClass::Marginal => "marginal",
            OrbitClass::Plunging => "plunging",
            OrbitClass::Radial => "radial",
            OrbitClass::Circular => "circular",
            OrbitClass::Separatrix => "separatrix",
        }
    }
}

/// Non-canonical f64 diagnostics. Lengths are in position quanta and times in chronons.
/// NaN means "not provided" (or undefined on this branch, for example the periods of an
/// unbound orbit). The judge decides which quantities a case must provide.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Orbit {
    /// Killing energy per unit mass.
    pub energy: f64,
    /// Angular momentum in quanta (signed).
    pub angular_momentum: f64,
    pub class: OrbitClass,
    /// Darwin semilatus rectum in units of M, and eccentricity.
    pub p: f64,
    pub e: f64,
    /// Radial period in river time T, and in proper time, in chronons.
    pub radial_period: f64,
    pub proper_radial_period: f64,
    /// Periapsis advance per radial period, in radians.
    pub periapsis_advance: f64,
    /// Total scattering angle minus pi, in radians.
    pub deflection: f64,
    /// d(tau)/dT of a static observer, sqrt(1 - 2M/r0), and of a circular orbit, sqrt(1 - 3M/r0),
    /// at the anchor's radius r0.
    pub static_clock_rate: f64,
    pub circular_clock_rate: f64,
}
impl Orbit {
    pub fn nothing() -> Orbit {
        let n = f64::NAN;
        Orbit {
            energy: n,
            angular_momentum: n,
            class: OrbitClass::Bound,
            p: n,
            e: n,
            radial_period: n,
            proper_radial_period: n,
            periapsis_advance: n,
            deflection: n,
            static_clock_rate: n,
            circular_clock_rate: n,
        }
    }
}

/// What construction returns.
pub type Built = std::result::Result<Box<dyn Body>, AnchorError>;

/// One validated geodesic (the crate's `Geodesic`). Queries cannot fail.
pub trait Body {
    fn position(&self, t: i128) -> At;
    fn orbit(&self) -> Orbit;
    fn proper_time(&self, t: i128) -> f64;
    /// Shapiro delay of a light ray with this anchor: the sum of the two legs, from the turning
    /// radius r0 out to r1 and to r2 (quanta), of (t(r0 -> r) - sqrt(r^2 - r0^2) / Q) in
    /// Schwarzschild t, in chronons: the H0178/H0183 oracle's definition. None: not provided.
    fn shapiro_delay(&self, _r1: f64, _r2: f64) -> Option<f64> {
        None
    }
}

/// The factory (the crate's `Geodesic::new`).
pub trait Evaluator: Sync {
    fn name(&self) -> String;
    /// False for the unwired crate adapter: the gate then fails at once and says why.
    fn wired(&self) -> bool {
        true
    }
    fn new_body(&self, field: Field, q: i128, anchor: Anchor, motion: Motion) -> Built;
    /// HOOK for the fallback cases of G2.1. Build the body with the TEST-ONLY reduced schedule
    /// `schedule` (fractional bits, 16/32/64), which forces the final-midpoint rule on
    /// near-integer cases. None: the evaluator has no such hook, and the gate fails.
    fn new_body_reduced(&self, _field: Field, _q: i128, _anchor: Anchor, _motion: Motion, _schedule: &[u32]) -> Option<Built> {
        None
    }
}

impl At {
    pub fn kind(&self) -> &'static str {
        match self {
            At::Free(_) => "Free",
            At::Absorbed { .. } => "Absorbed",
            At::OutOfRange { .. } => "OutOfRange",
            At::Before => "Before",
        }
    }
    /// The chronon of Absorbed or OutOfRange.
    pub fn chronon(&self) -> Option<i128> {
        match self {
            At::Absorbed { chronon } | At::OutOfRange { chronon } => Some(*chronon),
            _ => None,
        }
    }
    pub fn to_json(self) -> Value {
        match self {
            At::Free(x) => json!({"at": "Free", "x": [x[0].to_string(), x[1].to_string()]}),
            At::Absorbed { chronon } => json!({"at": "Absorbed", "chronon": chronon.to_string()}),
            At::OutOfRange { chronon } => json!({"at": "OutOfRange", "chronon": chronon.to_string()}),
            At::Before => json!({"at": "Before"}),
        }
    }
}

/// What the judge says. UNSETTLED counts as a failure of the gate (the contract).
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Expect {
    Known(At),
    Unsettled(String),
}
impl Expect {
    pub fn to_json(&self) -> Value {
        match self {
            Expect::Known(a) => a.to_json(),
            Expect::Unsettled(why) => json!({"at": "UNSETTLED", "why": why}),
        }
    }
    pub fn matches(&self, got: &At) -> bool {
        matches!(self, Expect::Known(a) if a == got)
    }
}

/// A decimal integer (frozen files write every integer as a string).
pub fn parse_int(s: &str) -> Result<i128> {
    s.trim().parse::<i128>().map_err(|e| format!("bad integer {s:?}: {e}").into())
}
pub fn int_of(v: &Value) -> Result<i128> {
    match v {
        Value::String(s) => parse_int(s),
        Value::Number(n) => n.as_i64().map(|i| i as i128).ok_or_else(|| format!("bad integer {n}").into()),
        other => Err(format!("expected an integer, got {other}").into()),
    }
}
pub fn int_pair(v: &Value) -> Result<[i128; 2]> {
    let a = v.as_array().filter(|a| a.len() == 2).ok_or_else(|| format!("expected a pair, got {v}"))?;
    Ok([int_of(&a[0])?, int_of(&a[1])?])
}
/// An `At` (or UNSETTLED) from a judge answer record: {at, x | chronon, ...}.
pub fn expect_of(v: &Value) -> Result<Expect> {
    let at = v["at"].as_str().ok_or_else(|| format!("answer without `at`: {v}"))?;
    Ok(match at {
        "Free" => Expect::Known(At::Free(int_pair(&v["x"])?)),
        "Absorbed" => Expect::Known(At::Absorbed { chronon: int_of(&v["chronon"])? }),
        "OutOfRange" => Expect::Known(At::OutOfRange { chronon: int_of(&v["chronon"])? }),
        "Before" => Expect::Known(At::Before),
        _ => Expect::Unsettled(v.to_string()),
    })
}
/// The compact R2 answer: [floor x, floor y] | "A<chronon>" | "O<chronon>".
pub fn expect_of_r2(v: &Value) -> Result<Expect> {
    if v.is_array() {
        return Ok(Expect::Known(At::Free(int_pair(v)?)));
    }
    let s = v.as_str().ok_or_else(|| format!("bad R2 answer {v}"))?;
    if let Some(c) = s.strip_prefix('A') {
        return Ok(Expect::Known(At::Absorbed { chronon: parse_int(c)? }));
    }
    if let Some(c) = s.strip_prefix('O') {
        return Ok(Expect::Known(At::OutOfRange { chronon: parse_int(c)? }));
    }
    if s == "Before" {
        return Ok(Expect::Known(At::Before));
    }
    Ok(Expect::Unsettled(s.to_string()))
}
/// Ceiling of a non-negative-or-negative decimal string like "-12.53" without floats.
pub fn ceil_decimal(s: &str) -> Result<i128> {
    let s = s.trim();
    let (neg, body) = match s.strip_prefix('-') {
        Some(b) => (true, b),
        None => (false, s),
    };
    let (int, frac) = body.split_once('.').unwrap_or((body, ""));
    let i = parse_int(if int.is_empty() { "0" } else { int })?;
    let has_frac = frac.bytes().any(|c| c != b'0');
    if !frac.bytes().all(|c| c.is_ascii_digit()) {
        return Err(format!("bad decimal {s:?}").into());
    }
    // For a negative value, ceil moves toward zero: -12.5 -> -12.
    Ok(if neg {
        -i
    } else if has_frac {
        i + 1
    } else {
        i
    })
}
