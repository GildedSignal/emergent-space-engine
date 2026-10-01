//! The frozen Arb-certified Schwarzschild bank (`artifacts/evidence/g2-reference-20260928/`,
//! 212,408 answers) run against `crates/space`'s law, unchanged.
//!
//! ```text
//! cargo run --release -p emergent-space --example certified_bank -- RUNG [--part i/n] [--from k]
//!     [--budget secs] [--out DIR]          RUNG: R0 R1 R2 R3 R4 R5 G22 G24 G24edge FB
//! python3 crates/space/examples/certified_bank.py DIR      (summary of the rows in DIR)
//! ```
//!
//! **What maps.** The bank's cases are river (Painleve-Gullstrand) states of a test body or
//! photon in lattice units: position X (integers), velocity k (integers), mass M and
//! light speed Q in lattice units, and river times T in chronons. The law is the Darwin
//! compiler in Schwarzschild coordinates, G = c = M = 1. The boundary adapter below converts
//! (all floats, confined to this file, never inside the law):
//!   k/Q = dX/dT the coordinate velocity of a body (for light k only gives the direction of u),
//!   u = k/Q - beta the velocity relative to the flow, w = sqrt(2M/r), a = 1 - 2M/r,
//!   E = gamma (1 - w u_r), L = r gamma u_t,
//!   dr/dt = a (u_r - w) / (1 - w u_r), r dphi/dt = a u_t / (1 - w u_r),
//!   T = t + h(r), h = 2 sqrt(2Mr) + 2M ln|(sqrt r - sqrt 2M)/(sqrt r + sqrt 2M)|.
//! The state goes into `Rebinding::from_state` (the law's own inverse at an event: fit,
//! compile, residual). A query at river time T is read by solving T = t + h(r(t)) for the
//! law's coordinate time t (Newton, bracketed; dT/dt lies in [1 - w, 1 + w]).
//!   - bound orbit (`Trajectory::Cycle`), circular included: positions are compared.
//!   - unbound with a turning point (`Trajectory::Passage`): positions are compared. The
//!     window edge is chosen by this harness from the largest radius the reference reports.
//!   - refusals (`NoBoundOrbit`, `Range`) are counted and classified, never hidden.
//!   - not supplied by the law, counted and skipped: radial paths (L = 0), plunge and horizon
//!     times, outgoing escapes with no turning point, photon positions (photon class and
//!     deflection are checked through `scatter`, the law's photon path), T < T0.
//! Per rung the exact counts of mapped and skipped answers are printed.
//!
//! **Tolerances, frozen before the full run** (the law is a quantized algorithm, so exactness
//! is not the question; `certified_bank.py` holds the same numbers). Per answered position,
//! with n the radial cycles elapsed (the law's own period) and r the reference radius:
//!   design:    |dX| <= 2 quanta + 1e-5 (1 + n) r      (the law's designed ~1e-6 per cycle)
//!   behaviour: |dX| <= 2 quanta + 1e-3 (1 + n) r      (gate B2's 0.1% period, scaled by n)
//! judged for n <= 10 only: after that a position is a statement about the period to better
//! than 1/(2 pi n), which the law never promised (the first draft judged every n and was
//! vacuous beyond n = 1000, so it was replaced before the unseen 94% of the bank ran; the new
//! rule is stricter). For n > 10 the error TYPE is judged: the angle error against the linear
//! drift the law's own period and advance errors predict (G22, with Arb diagnostics).
//! Exact floor agreement is reported only where r < 2^45 quanta (f64 resolves it).
//! Class: a refusal of an inbound state with no turning point reads as "absorbed"; the law
//! itself returns only `NoBoundOrbit`.
use emergent_space::{
    binding::{IntegerState, Rebinding, Trajectory},
    orbit::{OrbitState, Scalar},
    scatter, Error, Key, Outcome,
};
use std::{collections::HashMap, fmt::Write as _, io::Write as _, panic, process::Command, time::Instant};

const BANK: &str = "artifacts/evidence/g2-reference-20260928";
/// `BANK_DIR=/abs/dir` reads `RUNG.cases.jsonl.gz` and `RUNG.answers.jsonl.gz` from that directory instead
/// (new cases solved by the Arb judge in the archive, same file format).

// ---------------------------------------------------------------- json
#[derive(Debug, Clone)]
enum J {
    Null,
    Num(f64),
    Str(String),
    Arr(Vec<J>),
    Obj(Vec<(String, J)>),
}
impl J {
    fn get(&self, k: &str) -> &J {
        if let J::Obj(v) = self {
            for (a, b) in v {
                if a == k {
                    return b;
                }
            }
        }
        &J::Null
    }
    fn s(&self) -> &str {
        if let J::Str(s) = self {
            s
        } else {
            ""
        }
    }
    fn a(&self) -> &[J] {
        if let J::Arr(v) = self {
            v
        } else {
            &[]
        }
    }
    fn i(&self) -> i128 {
        match self {
            J::Str(s) => s.parse().unwrap_or(0),
            J::Num(n) => *n as i128,
            _ => 0,
        }
    }
    fn f(&self) -> f64 {
        match self {
            J::Str(s) => s.parse().unwrap_or(f64::NAN),
            J::Num(n) => *n,
            _ => f64::NAN,
        }
    }
    fn is_null(&self) -> bool {
        matches!(self, J::Null)
    }
}
fn ws(b: &[u8], i: &mut usize) {
    while *i < b.len() && (b[*i] as char).is_whitespace() {
        *i += 1;
    }
}
fn parse(b: &[u8], i: &mut usize) -> J {
    ws(b, i);
    match b[*i] {
        b'{' => {
            *i += 1;
            let mut v = vec![];
            loop {
                ws(b, i);
                if b[*i] == b'}' {
                    *i += 1;
                    return J::Obj(v);
                }
                if b[*i] == b',' {
                    *i += 1;
                    continue;
                }
                let k = match parse(b, i) {
                    J::Str(s) => s,
                    _ => panic!("key"),
                };
                ws(b, i);
                *i += 1; // ':'
                v.push((k, parse(b, i)));
            }
        }
        b'[' => {
            *i += 1;
            let mut v = vec![];
            loop {
                ws(b, i);
                if b[*i] == b']' {
                    *i += 1;
                    return J::Arr(v);
                }
                if b[*i] == b',' {
                    *i += 1;
                    continue;
                }
                v.push(parse(b, i));
            }
        }
        b'"' => {
            *i += 1;
            let mut s = Vec::new();
            while b[*i] != b'"' {
                if b[*i] == b'\\' {
                    *i += 1;
                }
                s.push(b[*i]);
                *i += 1;
            }
            *i += 1;
            J::Str(String::from_utf8_lossy(&s).into_owned())
        }
        b'n' => {
            *i += 4;
            J::Null
        }
        b't' => {
            *i += 4;
            J::Num(1.0)
        }
        b'f' => {
            *i += 5;
            J::Num(0.0)
        }
        _ => {
            let st = *i;
            while *i < b.len() && matches!(b[*i], b'-' | b'+' | b'.' | b'e' | b'E' | b'0'..=b'9') {
                *i += 1;
            }
            J::Num(std::str::from_utf8(&b[st..*i]).unwrap().parse().unwrap_or(f64::NAN))
        }
    }
}
fn read_gz(root: &str, name: &str) -> Vec<J> {
    let dir = std::env::var("BANK_DIR").unwrap_or_else(|_| format!("{root}/{BANK}"));
    let out = Command::new("gzip").arg("-dc").arg(format!("{dir}/{name}")).output().expect("gzip");
    assert!(out.status.success(), "cannot read {name}");
    out.stdout
        .split(|&c| c == b'\n')
        .filter(|l| !l.is_empty())
        .map(|l| {
            let mut i = 0;
            parse(l, &mut i)
        })
        .collect()
}

// ---------------------------------------------------------------- the bank
#[derive(Clone, Copy, PartialEq, Debug)]
enum Kind {
    Free,
    Absorbed,
    OutOfRange,
    Before,
    Unsettled,
}
impl Kind {
    fn c(self) -> char {
        match self {
            Kind::Free => 'F',
            Kind::Absorbed => 'A',
            Kind::OutOfRange => 'O',
            Kind::Before => 'B',
            Kind::Unsettled => 'U',
        }
    }
}
#[derive(Clone)]
struct Ans {
    t: i128,
    kind: Kind,
    x: [i128; 2],
}
#[derive(Default, Clone)]
#[allow(dead_code)]
struct Diag {
    e: f64,
    l_quanta: f64,
    p: f64,
    ecc: f64,
    period_t: f64,
    advance: f64,
    defl: f64,
    b_m: f64,
    roots: [f64; 3],
}
struct Case {
    id: String,
    cat: String,
    light: bool,
    m: i128,
    q: i128,
    t0: i128,
    x: [i128; 2],
    k: [i128; 2],
    ans: Vec<Ans>,
    diag: Option<Diag>,
}
fn kind_of(s: &str) -> Kind {
    match s {
        "Free" => Kind::Free,
        "Absorbed" => Kind::Absorbed,
        "OutOfRange" => Kind::OutOfRange,
        "Before" => Kind::Before,
        _ => Kind::Unsettled,
    }
}
fn load(root: &str, rung: &str) -> Vec<Case> {
    let mut out = vec![];
    if rung == "R2" {
        for (n, rec) in read_gz(root, "R2.answers.jsonl.gz").iter().skip(1).enumerate() {
            let a = rec.a();
            let ans = a[4]
                .a()
                .iter()
                .enumerate()
                .map(|(i, v)| {
                    let t = i as i128 + 1;
                    match v {
                        J::Str(s) if s.starts_with('A') => Ans { t, kind: Kind::Absorbed, x: [0; 2] },
                        J::Str(_) => Ans { t, kind: Kind::OutOfRange, x: [0; 2] },
                        J::Arr(p) => Ans { t, kind: Kind::Free, x: [p[0].i(), p[1].i()] },
                        _ => Ans { t, kind: Kind::Unsettled, x: [0; 2] },
                    }
                })
                .collect();
            out.push(Case {
                id: format!("R2-{n:05}"),
                cat: "R2".into(),
                light: false,
                m: 1,
                q: 25,
                t0: 0,
                x: [a[0].i(), a[1].i()],
                k: [a[2].i(), a[3].i()],
                ans,
                diag: None,
            });
        }
        return out;
    }
    let cases = read_gz(root, &format!("{rung}.cases.jsonl.gz"));
    let mut answers: HashMap<String, J> = HashMap::new();
    let files: Vec<String> = if rung == "R5" {
        (0..10).map(|i| format!("R5-slice{i}.answers.jsonl.gz")).collect()
    } else {
        vec![format!("{rung}.answers.jsonl.gz")]
    };
    for f in files {
        for r in read_gz(root, &f) {
            answers.insert(r.get("id").s().to_string(), r);
        }
    }
    for c in &cases {
        let id = c.get("id").s().to_string();
        let r = &answers[&id];
        let ts: Vec<i128> = c.get("T").a().iter().map(|v| v.i()).collect();
        let ans = r
            .get("answers")
            .a()
            .iter()
            .map(|a| {
                let kind = kind_of(a.get("at").s());
                let x = if kind == Kind::Free { [a.get("x").a()[0].i(), a.get("x").a()[1].i()] } else { [0; 2] };
                Ans { t: a.get("T").i(), kind, x }
            })
            .collect::<Vec<_>>();
        assert_eq!(ans.len(), ts.len(), "{id}");
        let d = r.get("diag");
        let diag = (!d.is_null()).then(|| Diag {
            e: d.get("E").f(),
            l_quanta: d.get("L_quanta").f(),
            p: d.get("p_over_M").f(),
            ecc: d.get("e").f(),
            period_t: d.get("period_T_chronons").f(),
            advance: d.get("advance_rad").f(),
            defl: d.get("deflection_rad").f(),
            b_m: d.get("b_over_M").f(),
            roots: {
                let r = d.get("roots_u_times_M").a();
                if r.len() == 3 { [r[0].f(), r[1].f(), r[2].f()] } else { [f64::NAN; 3] }
            },
        });
        let cat = c.get("class").a().iter().map(|v| v.s().to_string()).collect::<Vec<_>>().join("+");
        out.push(Case {
            id,
            cat,
            light: c.get("motion").s() == "null",
            m: c.get("M").i(),
            q: c.get("Q").i(),
            t0: c.get("t0").i(),
            x: [c.get("x").a()[0].i(), c.get("x").a()[1].i()],
            k: [c.get("k").a()[0].i(), c.get("k").a()[1].i()],
            ans,
            diag,
        });
    }
    out
}

// ---------------------------------------------------------------- adapter (floats live here)
fn pow2(e: i32) -> f64 {
    if e > 1023 {
        f64::INFINITY
    } else if e < -1022 {
        0.0
    } else {
        f64::from_bits(((e + 1023) as u64) << 52)
    }
}
fn to_scalar(x: f64) -> Option<Scalar> {
    if x == 0.0 {
        return Some(Scalar::ZERO);
    }
    if !x.is_finite() || x.abs() < 1e-290 {
        return None;
    }
    let bits = x.abs().to_bits();
    let exp = ((bits >> 52) & 0x7ff) as i32 - 1023;
    let man = ((bits & ((1 << 52) - 1)) | (1 << 52)) as i128;
    Scalar::raw(if x < 0.0 { -man } else { man }, exp - 52).ok()
}
fn sf(x: Scalar) -> f64 {
    x.significand() as f64 * pow2(x.exponent() as i32 - 62)
}
/// River time offset h(rho) in M/c, T = t + h(rho).
fn hfun(rho: f64) -> f64 {
    let s = rho.sqrt();
    let r2 = std::f64::consts::SQRT_2;
    2.0 * r2 * s + 2.0 * ((s - r2) / (s + r2)).abs().ln()
}
fn hprime(rho: f64) -> f64 {
    (2.0 / rho).sqrt() / (1.0 - 2.0 / rho)
}
struct Conv {
    rho: f64,
    e: f64,
    l: f64, // L/M, signed (positive counter-clockwise)
    vr: f64,
    vt: f64,
    inbound: bool,
}
/// River state to Schwarzschild constants and coordinate velocity. For a body, k/Q is the
/// coordinate velocity dX/dT (the bank's v = k/Q), and u = k/Q - beta is relative to the flow;
/// for light, k only gives the direction of u (|u| = 1), as PROVENANCE.md states.
fn convert(c: &Case) -> Result<Conv, &'static str> {
    let (x, y) = (c.x[0] as f64, c.x[1] as f64);
    let r = x.hypot(y);
    let rho = r / c.m as f64;
    if !(rho > 2.0) {
        return Err("inside");
    }
    let (kx, ky) = (c.k[0] as f64, c.k[1] as f64);
    let w = (2.0 / rho).sqrt();
    let a = (rho - 2.0) / rho;
    if c.light {
        let kn = kx.hypot(ky);
        if kn == 0.0 {
            return Err("convert");
        }
        let (ur, ut) = ((kx * x + ky * y) / (r * kn), (x * ky - y * kx) / (r * kn));
        let den = 1.0 - w * ur;
        if !(den > 0.0) {
            return Err("convert");
        }
        return Ok(Conv { rho, e: den, l: rho * ut, vr: f64::NAN, vt: f64::NAN, inbound: ur < w });
    }
    let q = c.q as f64;
    let (kr, kt) = ((kx * x + ky * y) / (r * q), (x * ky - y * kx) / (r * q));
    let (ur, ut) = (kr + w, kt);
    let omu2 = 1.0 - ur * ur - ut * ut;
    let den = a - w * kr; // = 1 - w u_r
    if !(omu2 > 0.0) || !(den > 0.0) {
        return Err("convert");
    }
    let gamma = 1.0 / omu2.sqrt();
    Ok(Conv {
        rho,
        e: gamma * den,
        l: rho * gamma * ut,
        vr: a * kr / den,
        vt: a * kt / den,
        inbound: kr < 0.0,
    })
}
fn integer_state(c: &Case, cv: &Conv) -> IntegerState {
    let m = c.m as f64;
    let (x, y) = (c.x[0] as f64, c.x[1] as f64);
    let r = x.hypot(y);
    let (px, py) = (x / m, y / m);
    let big = px.abs().max(py.abs());
    let pe = big.log2().floor() as i32 + 1 - 62;
    let (n, t) = ([x / r, y / r], [-y / r, x / r]);
    let eps: f64 = std::env::var("BANK_PERTURB").ok().and_then(|v| v.parse().ok()).unwrap_or(0.0);
    let v = [(cv.vr * n[0] + cv.vt * t[0]) * (1.0 + eps), (cv.vr * n[1] + cv.vt * t[1]) * (1.0 + eps)];
    IntegerState {
        position: [(px / pow2(pe)).round() as i64, (py / pow2(pe)).round() as i64],
        velocity: [(v[0] * pow2(62)).round() as i64, (v[1] * pow2(62)).round() as i64],
        length_exponent: pe as i16,
        velocity_exponent: -62,
    }
}
fn istate_f(s: &IntegerState) -> ([f64; 2], [f64; 2]) {
    let (pe, ve) = (pow2(s.length_exponent as i32), pow2(s.velocity_exponent as i32));
    (
        [s.position[0] as f64 * pe, s.position[1] as f64 * pe],
        [s.velocity[0] as f64 * ve, s.velocity[1] as f64 * ve],
    )
}

// ---------------------------------------------------------------- the law's readout
fn state_at(rb: &Rebinding, s: f64) -> Result<OrbitState, Error> {
    let t = to_scalar(s).ok_or(Error::Range)?;
    rb.trajectory.state(t.sub(rb.periapsis_time)?)
}
fn azimuth(rb: &Rebinding, st: &OrbitState) -> f64 {
    let phase = st.radial_angle as f64 / pow2(61) + sf(st.advance);
    let ori = rb.periapsis_angle as f64 / 4294967296.0 * std::f64::consts::TAU;
    ori + if rb.clockwise { -phase } else { phase }
}
/// The law's coordinate time s (M/c, since the event) at which the river time elapsed is dt_m.
fn solve(rb: &Rebinding, dt_m: f64, h0: f64) -> Result<(f64, OrbitState), &'static str> {
    let eval = |s: f64| -> Result<(f64, f64, OrbitState), Error> {
        let st = state_at(rb, s)?;
        let rho = sf(st.radius);
        let vr = sf(st.radial_velocity);
        Ok((s + hfun(rho) - h0 - dt_m, 1.0 + hprime(rho) * vr, st))
    };
    if dt_m == 0.0 {
        return eval(0.0).map(|(_, _, st)| (0.0, st)).map_err(|_| "range");
    }
    let (mut lo, mut hi) = (0.0f64, dt_m.max(1e-300));
    let mut fh = eval(hi).map_err(|_| "range")?;
    let mut n = 0;
    while fh.0 < 0.0 {
        lo = hi;
        hi *= 2.0;
        n += 1;
        if n > 200 {
            return Err("nosolve");
        }
        fh = eval(hi).map_err(|_| "range")?;
    }
    let mut s = hi;
    let mut cur = fh;
    for _ in 0..80 {
        let (f, fp) = (cur.0, cur.1);
        if f == 0.0 {
            break;
        }
        if f > 0.0 {
            hi = s;
        } else {
            lo = s;
        }
        let mut next = s - f / fp;
        if !(fp > 0.0) || !(next > lo && next < hi) {
            next = 0.5 * (lo + hi);
        }
        let done = (next - s).abs() <= 2e-16 * next.abs().max(1e-300) || (hi - lo) <= 4e-16 * hi;
        s = next;
        cur = eval(s).map_err(|_| "range")?;
        if done {
            break;
        }
    }
    Ok((s, cur.2))
}

// ---------------------------------------------------------------- rows
#[derive(Default)]
struct Rows {
    q: String,
    c: String,
    nq: usize,
}
fn polish(u0: f64, e: f64, l: f64) -> f64 {
    let mut u = u0;
    for _ in 0..60 {
        let f = e * e - 1.0 - l * l * u * u + 2.0 * u + 2.0 * l * l * u * u * u;
        let d = -2.0 * l * l * u + 2.0 + 6.0 * l * l * u * u;
        if d == 0.0 || !d.is_finite() {
            break;
        }
        let du = f / d;
        u -= du;
        if du.abs() < 1e-17 * u.abs() {
            break;
        }
    }
    u
}
/// The three roots of R(u) = E^2 - 1 + 2u - L^2 u^2 + 2 L^2 u^3 (u = M/r), ascending, if all real.
fn roots3(e: f64, l: f64) -> Option<[f64; 3]> {
    let (a, b, c, d) = (2.0 * l * l, -l * l, 2.0, e * e - 1.0);
    let (b, c, d) = (b / a, c / a, d / a);
    let (p, q) = (c - b * b / 3.0, 2.0 * b * b * b / 27.0 - b * c / 3.0 + d);
    if !(p < 0.0) {
        return None;
    }
    let m = 2.0 * (-p / 3.0).sqrt();
    let arg = (3.0 * q / (p * m)).clamp(-1.0, 1.0);
    let th = arg.acos() / 3.0;
    let mut r = [0.0; 3];
    for (k, rk) in r.iter_mut().enumerate() {
        let mut u = m * (th - 2.0 * std::f64::consts::PI * k as f64 / 3.0).cos() - b / 3.0;
        for _ in 0..8 {
            let f = ((u + b) * u + c) * u + d;
            let df = (3.0 * u + 2.0 * b) * u + c;
            if df == 0.0 {
                break;
            }
            u -= f / df;
        }
        *rk = u;
    }
    r.sort_by(|x, y| x.partial_cmp(y).unwrap());
    Some(r)
}
fn err_name(e: Error) -> &'static str {
    match e {
        Error::Range => "refused:Range",
        Error::NoBoundOrbit => "refused:NoBoundOrbit",
        Error::NotPeriodic => "refused:NotPeriodic",
        Error::Topology => "refused:Topology",
    }
}
fn process(c: &Case, rows: &mut Rows) {
    let law: String;
    let mut cm = String::new(); // case-row extras, tab separated
    let nfree = c.ans.iter().filter(|a| a.kind == Kind::Free).count();
    let nabs = c.ans.iter().filter(|a| a.kind == Kind::Absorbed).count();
    let mut e_val = f64::NAN;
    let mut l_val = f64::NAN;
    let mut rho0 = f64::NAN;
    let mut ok_pos = false;
    let mut rb_opt: Option<Rebinding> = None;
    let mut inbound = false;
    let (mut comp_us, mut knots, mut cross) = (f64::NAN, -1i64, -1i64);
    let (mut fitp, mut fitv, mut recon) = (f64::NAN, f64::NAN, -1i32);
    let (mut turn_p, mut turn_a) = (f64::NAN, f64::NAN);
    let (mut per_rel, mut adv_rel, mut defl_abs, mut defl_rel) = (f64::NAN, f64::NAN, f64::NAN, f64::NAN);
    let (mut e_err, mut l_err) = (f64::NAN, f64::NAN);
    let (mut law_per, mut law_adv) = (f64::NAN, f64::NAN);
    let (mut kper_rel, mut kadv_rel) = (f64::NAN, f64::NAN);
    let mut scat = String::from("-");
    let mut window = f64::NAN;
    let mut ecc = f64::NAN;
    let (mut margin, mut deltah, mut edge_ratio, mut rp_m) = (f64::NAN, f64::NAN, f64::NAN, f64::NAN);
    match convert(c) {
        Err(why) => law = format!("skip:{why}"),
        Ok(cv) => {
            e_val = cv.e;
            l_val = cv.l;
            rho0 = cv.rho;
            inbound = cv.inbound;
            // compile-only error: the law's orbit for the Arb diagnostics' own (p, e), no fit involved
            if let Some(d) = &c.diag {
                if d.p.is_finite() && d.ecc.is_finite() && d.ecc >= 0.0 && d.ecc < 1.0 && d.period_t.is_finite() {
                    if let Some(ps) = to_scalar(d.p) {
                        if let Ok(o) = emergent_space::orbit::OrbitKey::bound(ps, (d.ecc * pow2(48)).round() as u64).and_then(emergent_space::orbit::Orbit::compile) {
                            let per = sf(o.period().unwrap_or(Scalar::ZERO)) * c.m as f64 / c.q as f64;
                            kper_rel = (per - d.period_t).abs() / d.period_t;
                            kadv_rel = (sf(o.advance().unwrap_or(Scalar::ZERO)) - d.advance).abs() / d.advance;
                        }
                    }
                }
            }
            if !c.light && cv.e < 1.0 {
                if let Some(r) = roots3(cv.e, cv.l) {
                    let (ua, up) = (r[0], r[1]);
                    if ua > 0.0 {
                        let p = 2.0 / (ua + up);
                        let ecc = (up - ua) / (up + ua);
                        margin = (p - 6.0 - 2.0 * ecc) / p;
                        deltah = (r[2] - up) / ((up - ua) / 2.0);
                    }
                }
            }
            if let Some(d) = &c.diag {
                e_err = (cv.e - d.e).abs() / d.e.abs();
                l_err = (cv.l * c.m as f64 - d.l_quanta).abs() / d.l_quanta.abs();
            }
            if c.light {
                // The law's photon path: scatter(E = 1, L = b). Class and deflection only.
                let b = cv.l.abs() / cv.e;
                let q32 = b * pow2(32);
                law = if !(q32 < 1.8e19) {
                    "refused:Range".into()
                } else {
                    match Key::new(1 << 48, q32.round() as u64).and_then(|k| scatter(k, true)) {
                        Ok((Outcome::Absorbed, _)) => {
                            scat = "A".into();
                            "photon:absorbed".into()
                        }
                        Ok((Outcome::Escaped, half)) => {
                            scat = "E".into();
                            let defl = 2.0 * half.get() as f64 / pow2(30) - std::f64::consts::PI;
                            if let Some(d) = &c.diag {
                                defl_abs = (defl - d.defl).abs();
                                defl_rel = defl_abs / d.defl.abs();
                            }
                            "photon:escaped".into()
                        }
                        Err(e) => err_name(e).into(),
                    }
                };
            } else {
                // radial paths: L = 0 exactly (the law has no radial generator)
                let radial = c.x[0] * c.k[1] - c.x[1] * c.k[0] == 0;
                if radial {
                    law = "skip:radial".into();
                } else {
                    let rmax = c
                        .ans
                        .iter()
                        .filter(|a| a.kind == Kind::Free)
                        .map(|a| (a.x[0] as f64).hypot(a.x[1] as f64))
                        .fold(0.0, f64::max);
                    let edge = (2.0 * cv.rho).max(1.5 * rmax / c.m as f64);
                    let st = integer_state(c, &cv);
                    let t = Instant::now();
                    // The passage window must satisfy edge/periapsis < 2^62 (the phase word). If the
                    // wanted edge is refused as Range, shrink it by 2^10 and retry; queries beyond the
                    // window then read as `range` and are counted as such, not as a refusal of the case.
                    let mut edge_used = edge;
                    let res = loop {
                        let res = std::panic::catch_unwind(|| Rebinding::from_state(st, Scalar::ZERO, to_scalar(edge_used)));
                        if matches!(res, Ok(Err(Error::Range))) && edge_used > 4.0 * cv.rho {
                            edge_used = (edge_used / 1024.0).max(2.0 * cv.rho);
                            continue;
                        }
                        break res;
                    };
                    window = edge_used / edge;
                    if std::env::var_os("BANK_VERBOSE").is_some() {
                        eprintln!("{} state {:?} edge {:.4e} used {:.4e} -> {}", c.id, st, edge, edge_used, match &res { Ok(Ok(_)) => "ok".to_string(), Ok(Err(e)) => format!("{e:?}"), Err(_) => "panic".into() });
                    }
                    comp_us = t.elapsed().as_secs_f64() * 1e6;
                    match res {
                        Err(_) => law = "refused:panic".into(),
                        Ok(Err(e)) => {
                            law = err_name(e).into();
                            // legacy photon-free reading of a refused massive state: scatter(E, L)
                            if c.diag.is_none() && cv.e >= 1.0 && cv.l.abs() * pow2(32) < 1.8e19 && cv.e * pow2(48) < 1.8e19 {
                                if let Ok((o, _)) = Key::new((cv.e * pow2(48)) as u64, (cv.l.abs() * pow2(32)) as u64)
                                    .and_then(|k| scatter(k, false))
                                {
                                    scat = if o == Outcome::Absorbed { "A".into() } else { "E".into() };
                                }
                            }
                        }
                        Ok(Ok(rb)) => {
                            law = match rb.trajectory {
                                Trajectory::Cycle(_) => "cycle".into(),
                                Trajectory::Passage(_) => "passage".into(),
                            };
                            ok_pos = true;
                            // fit residual at the event, and the exact left inverse
                            if let Ok(dec) = rb.decoded_event() {
                                let (p0, v0) = istate_f(&st);
                                let (p1, v1) = istate_f(&dec);
                                fitp = (p1[0] - p0[0]).hypot(p1[1] - p0[1]) / p0[0].hypot(p0[1]);
                                fitv = (v1[0] - v0[0]).hypot(v1[1] - v0[1]);
                            }
                            recon = match rb.reconstruct() {
                                Ok(s2) => (s2 == st) as i32,
                                Err(_) => -1,
                            };
                            // turning points against the exact roots of R(u), polished in f64
                            let key = rb.trajectory.key();
                            ecc = pow2(48) / key.k as f64 - 1.0;
                            let rp = sf(key.periapsis);
                            edge_ratio = edge_used / rp;
                            rp_m = rp;
                            // exact turning points: the Arb roots where the bank has them (G22), else
                            // a float polish of R(u) (unreliable at a double root: circles, separatrix)
                            let (up, ua_exact) = match &c.diag {
                                Some(d) if d.roots[0].is_finite() => (d.roots[1], d.roots[0]),
                                _ => (polish(1.0 / rp, cv.e, cv.l), f64::NAN),
                            };
                            turn_p = (up - 1.0 / rp).abs() * rp;
                            if key.periodic() {
                                let kf = key.k as f64 / pow2(48);
                                let ra = rp / (2.0 * kf - 1.0);
                                let ua = if ua_exact.is_finite() { ua_exact } else { polish(1.0 / ra, cv.e, cv.l) };
                                turn_a = (ua - 1.0 / ra).abs() * ra;
                            }
                            if let Trajectory::Cycle(o) = &rb.trajectory {
                                law_per = sf(o.period().unwrap_or(Scalar::ZERO));
                                law_adv = sf(o.advance().unwrap_or(Scalar::ZERO));
                                knots = o.shape().knots().len() as i64;
                                cross = o.shape().crossings().len() as i64;
                                if let Some(d) = &c.diag {
                                    let per = sf(o.period().unwrap_or(Scalar::ZERO)) * c.m as f64 / c.q as f64;
                                    per_rel = (per - d.period_t).abs() / d.period_t;
                                    adv_rel = (sf(o.advance().unwrap_or(Scalar::ZERO)) - d.advance).abs() / d.advance;
                                }
                            }
                            rb_opt = Some(rb);
                        }
                    }
                }
            }
        }
    }
    // ---- queries
    let period_m = match &rb_opt {
        Some(rb) => match &rb.trajectory {
            Trajectory::Cycle(o) => o.period().map(sf).unwrap_or(f64::NAN),
            _ => f64::NAN,
        },
        None => f64::NAN,
    };
    let h0 = if rho0.is_finite() { hfun(rho0) } else { 0.0 };
    for (i, a) in c.ans.iter().enumerate() {
        let mut res = "-";
        let (mut ncyc, mut rref, mut dpos, mut rel, mut drr, mut dphi) = (0.0, f64::NAN, f64::NAN, f64::NAN, f64::NAN, f64::NAN);
        let mut floor = '-';
        if a.kind == Kind::Free {
            rref = ((a.x[0] as f64 + 0.5).hypot(a.x[1] as f64 + 0.5)).max(1.0);
        }
        if ok_pos && a.kind == Kind::Free && a.t >= c.t0 {
            let dt_m = (a.t - c.t0) as f64 * c.q as f64 / c.m as f64;
            let rb = rb_opt.as_ref().unwrap();
            match panic::catch_unwind(panic::AssertUnwindSafe(|| solve(rb, dt_m, h0))) {
                Err(_) => res = "panic",
                Ok(Err(why)) => res = why,
                Ok(Ok((s, st))) => {
                    res = "ok";
                    let rho = sf(st.radius);
                    if std::env::var_os("BANK_VERBOSE").is_some() {
                        eprintln!(
                            "{} q{} dT_m {:.6e} s {:.9e} rho_law {:.9e} rho_ref {:.9e} h0 {:.6e} n {:.3e} key {:?}",
                            c.id, i, dt_m, s, rho, rref / c.m as f64, h0, s / period_m, rb.trajectory.key()
                        );
                    }
                    let az = azimuth(rb, &st);
                    let mq = c.m as f64;
                    let (lx, ly) = (rho * mq * az.cos(), rho * mq * az.sin());
                    let (rx, ry) = (a.x[0] as f64 + 0.5, a.x[1] as f64 + 0.5);
                    dpos = (lx - rx).hypot(ly - ry);
                    rel = dpos / rref;
                    drr = (rho * mq - rref) / rref;
                    dphi = (rx * ly - ry * lx).atan2(rx * lx + ry * ly);
                    if !period_m.is_nan() {
                        ncyc = s / period_m;
                    }
                    if rref < pow2(45) && a.t != c.t0 {
                        floor = if lx.floor() as i128 == a.x[0] && ly.floor() as i128 == a.x[1] { '1' } else { '0' };
                    }
                }
            }
        } else if a.kind == Kind::Free && a.t < c.t0 {
            res = "before";
        }
        let _ = writeln!(
            rows.q,
            "{}\t{}\t{}\t{}\t{}\t{}\t{:.6e}\t{:.6e}\t{:.6e}\t{:.6e}\t{:.6e}\t{:.6e}\t{}",
            c.id, c.cat, law, a.kind.c(), res, i, ncyc, rref, dpos, rel, drr, dphi, floor
        );
        rows.nq += 1;
    }
    let _ = write!(
        cm,
        "{}\t{}\t{}\t{}\t{}\t{}\t{:.6e}\t{:.6e}\t{:.6e}\t{:.3}\t{}\t{}\t{:.3e}\t{:.3e}\t{}\t{:.3e}\t{:.3e}\t{:.3e}\t{:.3e}\t{:.3e}\t{:.3e}\t{}\t{}\t{:.3e}\t{:.3e}\t{:.4e}\t{:.3e}\t{:.6e}\t{:.6e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.3e}\t{:.3e}\t{}",
        c.id, c.cat, law, nfree, nabs, inbound as u8, e_val, l_val, rho0, comp_us, knots, cross, fitp, fitv, recon, turn_p, turn_a, per_rel, adv_rel, defl_abs, defl_rel, scat, c.diag.is_some() as u8, e_err, l_err, ecc, window, law_per, law_adv, margin, deltah, edge_ratio, rp_m, kper_rel, kadv_rel, c.light as u8
    );
    rows.c.push_str(&cm);
    rows.c.push('\n');
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let rung = args.first().expect("RUNG").clone();
    let opt = |k: &str| args.iter().position(|a| a == k).map(|i| args[i + 1].clone());
    let (part, parts) = opt("--part")
        .map(|s| {
            let (a, b) = s.split_once('/').unwrap();
            (a.parse::<usize>().unwrap(), b.parse::<usize>().unwrap())
        })
        .unwrap_or((0, 1));
    let from: usize = opt("--from").map(|s| s.parse().unwrap()).unwrap_or(0);
    let budget: f64 = opt("--budget").map(|s| s.parse().unwrap()).unwrap_or(55.0);
    let out = opt("--out");
    let root = std::env::var("BANK_ROOT").unwrap_or_else(|_| {
        // the checkout that holds the evidence: this worktree, else the live one
        let here = env!("CARGO_MANIFEST_DIR").to_string() + "/../..";
        if std::path::Path::new(&format!("{here}/{BANK}")).exists() {
            here
        } else {
            format!("{}/Research/emergent-space", std::env::var("HOME").unwrap())
        }
    });
    if std::env::var_os("BANK_VERBOSE").is_none() {
        panic::set_hook(Box::new(|_| {}));
    }
    let t0 = Instant::now();
    let cases = load(&root, &rung);
    let load_s = t0.elapsed().as_secs_f64();
    let mut rows = Rows::default();
    let t1 = Instant::now();
    let mut done = 0usize;
    let mut stopped = None;
    let only = opt("--only");
    for (i, c) in cases.iter().enumerate().filter(|(i, _)| i % parts == part && *i >= from) {
        if only.as_ref().is_some_and(|o| *o != c.id) {
            continue;
        }
        if t1.elapsed().as_secs_f64() > budget {
            stopped = Some(i);
            break;
        }
        // a panic inside the law is a finding: counted, not fatal
        if panic::catch_unwind(panic::AssertUnwindSafe(|| process(c, &mut rows))).is_err() {
            let _ = writeln!(rows.c, "{}\t{}\tpanic", c.id, c.cat);
        }
        done += 1;
    }
    let run_s = t1.elapsed().as_secs_f64();
    let tag = if parts > 1 { format!("{rung}.p{part}of{parts}") } else { rung.clone() };
    if let Some(dir) = out {
        std::fs::create_dir_all(&dir).unwrap();
        std::fs::File::create(format!("{dir}/{tag}.q.tsv")).unwrap().write_all(rows.q.as_bytes()).unwrap();
        std::fs::File::create(format!("{dir}/{tag}.c.tsv")).unwrap().write_all(rows.c.as_bytes()).unwrap();
    }
    println!(
        "{tag}: {} cases of {} ({} answers) in {run_s:.1} s (load {load_s:.1} s){}",
        done,
        cases.len(),
        rows.nq,
        match stopped {
            Some(i) => format!("; STOPPED at case {i} by the {budget} s budget: resume with --from {i}"),
            None => String::new(),
        }
    );
}
