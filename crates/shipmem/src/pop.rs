//! Populations, generated deterministically, every random draw charged to an entropy account.
//! The floor of a population is the entropy of its draws (group descriptions included), minus
//! log2(n!) for a group whose members are exchangeable (identity is the state).
//! Orbit ships are stored as columns [t_p, kind, E (Q48), L (Q32), ω (u32)]; battle members as
//! [x0, x1, k0, k1, c0, c1, kind, rev] relative to their free-fall frame.
use crate::codec::MAXC;
use crate::program::Prog;
use crate::shelf::{Kind, Ship};
use emergent_space::Key;

pub struct Rng {
    s: u64,
    pub bits: f64,
}
impl Rng {
    pub fn new(seed: u64) -> Self {
        let mut r = Self { s: seed, bits: 0.0 };
        r.next();
        r
    }
    pub fn next(&mut self) -> u64 {
        self.s = self.s.wrapping_add(0x9E37_79B9_7F4A_7C15);
        let mut z = self.s;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
        z ^ (z >> 31)
    }
    /// Uniform in [0, n).
    pub fn below(&mut self, n: u64) -> u64 {
        self.bits += (n as f64).log2();
        ((self.next() as u128 * n as u128) >> 64) as u64
    }
    pub fn range(&mut self, lo: u64, hi: u64) -> u64 {
        lo + self.below(hi - lo)
    }
    pub fn bitsn(&mut self, w: u32) -> u64 {
        self.bits += w as f64;
        if w == 0 {
            0
        } else {
            self.next() >> (64 - w)
        }
    }
    /// Gap ≥ 1, geometric with mean 2^g.
    pub fn geometric(&mut self, g: u32) -> u64 {
        let p = 0.5f64.powi(g as i32);
        self.bits += h2(p) / p;
        let u = ((self.next() >> 11) + 1) as f64 / (1u64 << 53) as f64;
        1 + (u.ln() / (1.0 - p).ln()).floor() as u64
    }
    /// True with probability 2^-k.
    pub fn bernoulli(&mut self, k: u32) -> bool {
        self.bits += h2(0.5f64.powi(k as i32));
        self.next() >> (64 - k) == 0
    }
    /// True with probability p.
    pub fn bernoulli_p(&mut self, p: f64) -> bool {
        if p <= 0.0 {
            return false;
        }
        if p >= 1.0 {
            return true;
        }
        self.bits += h2(p);
        (self.next() as f64) < p * 18446744073709551616.0
    }
    /// Kind k with P = 2^-(k+1) for k < 7, P(7) = 2^-7: 1.984375 bits.
    pub fn skewed8(&mut self) -> u64 {
        self.bits += 1.984375;
        (self.next().trailing_zeros() as u64).min(7)
    }
}
pub fn h2(p: f64) -> f64 {
    -(p * p.log2() + (1.0 - p) * (1.0 - p).log2())
}
pub fn log2_factorial(n: u64) -> f64 {
    if n < 2 {
        return 0.0;
    }
    let x = n as f64;
    (x * x.ln() - x + 0.5 * (2.0 * std::f64::consts::PI * x).ln() + 1.0 / (12.0 * x))
        / std::f64::consts::LN_2
}

fn seed(pop: u64, g: u64) -> u64 {
    let mut r = Rng {
        s: pop << 40 ^ g,
        bits: 0.0,
    };
    r.next()
}

/// A bound orbit's key from Darwin's p in [100, 8000) and e in [0, 0.6), through the law's own
/// boundary conversion.
fn orbit(r: &mut Rng) -> (u64, u64) {
    let p = r.range(100 << 16, 8000 << 16) as u32;
    let e = r.below((0.6 * (1u64 << 30) as f64) as u64) as u32;
    let k = Key::darwin(p, e).expect("bound orbit");
    (k.energy.get(), k.angular.get())
}

pub struct Group {
    pub members: Vec<Ship>,
    pub kind: Kind,
    pub bits: f64,
    pub exchangeable: bool,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Pop {
    Formation,
    Convoy,
    Stream,
    Battle,
    Traders,
    Random,
}
pub const DOLL: usize = 1_000_000;
pub const FRAME: usize = 1 << 16;

impl Pop {
    pub const ALL: [Pop; 6] = [
        Pop::Formation,
        Pop::Convoy,
        Pop::Stream,
        Pop::Battle,
        Pop::Traders,
        Pop::Random,
    ];
    pub fn name(self) -> &'static str {
        match self {
            Pop::Formation => "formation",
            Pop::Convoy => "convoy",
            Pop::Stream => "stream",
            Pop::Battle => "battle",
            Pop::Traders => "traders",
            Pop::Random => "random",
        }
    }
    pub fn parse(s: &str) -> Option<Pop> {
        Self::ALL.into_iter().find(|p| p.name() == s)
    }
    pub fn cols(self) -> usize {
        if self == Pop::Battle {
            8
        } else {
            5
        }
    }
    pub fn orders(self) -> Vec<[u8; MAXC]> {
        if self == Pop::Battle {
            vec![[6, 0, 1, 2, 3, 4, 5, 7]]
        } else {
            vec![[0, 1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 0, 5, 6, 7]]
        }
    }

    pub fn group(self, g: u64) -> Group {
        let mut r = Rng::new(seed(self as u64 + 1, g));
        let mut members: Vec<Ship> = Vec::new();
        let ship = |a: [u64; 5]| -> Ship { [a[0], a[1], a[2], a[3], a[4], 0, 0, 0] };
        let (kind, exchangeable) = match self {
            Pop::Formation => {
                let m = r.range(64, 1025);
                let k = r.range(8, 33);
                let kind0 = r.below(64);
                let (e0, l0) = orbit(&mut r);
                let (w0, t0) = (r.bitsn(32), r.bitsn(48));
                let se = r.range(1 << 10, 1 << 11);
                let sl = r.range(1 << 12, 1 << 13);
                let st = r.range(1 << 14, 1 << 15);
                let sw = r.range(1 << 6, 1 << 7);
                for i in 0..m {
                    let (row, col) = (i / k, i % k);
                    let (jt, je, jl, jw) = if r.bernoulli(5) {
                        (14, 10, 10, 10)
                    } else {
                        (6, 4, 5, 3)
                    };
                    let kind = kind0 + if r.bernoulli(3) { 64 } else { 0 };
                    let t = t0 + col * st + r.bitsn(jt);
                    let e = e0 + row * se + r.bitsn(je);
                    let l = l0 + row * sl + r.bitsn(jl);
                    let w = (w0 + col * sw + r.bitsn(jw)) & 0xFFFF_FFFF;
                    members.push(ship([t, kind, e, l, w]));
                }
                (Kind::Slot { grid: k as u16 }, false)
            }
            Pop::Convoy => {
                let m = r.range(64, 1025);
                let kind = r.below(64);
                let (e, l) = orbit(&mut r);
                let w = r.bitsn(32);
                let mut t = r.bitsn(48);
                for _ in 0..m {
                    t += r.geometric(12);
                    members.push(ship([t, kind, e, l, w]));
                }
                (Kind::Slot { grid: 0 }, false)
            }
            Pop::Stream => {
                let m = r.range(4096, 16385);
                let keys: Vec<(u64, u64)> = (0..4).map(|_| orbit(&mut r)).collect();
                let w0 = r.bitsn(32);
                let om = r.range(1 << 16, 1 << 17);
                let t0 = r.bitsn(48);
                let mut t = t0;
                for _ in 0..m {
                    t += r.geometric(14);
                    let kind = r.skewed8();
                    let (e, l) = keys[r.below(4) as usize];
                    let w = (w0 + (((t - t0) * om) >> 20)) & 0xFFFF_FFFF;
                    members.push(ship([t, kind, e, l, w]));
                }
                (Kind::Slot { grid: 0 }, false)
            }
            Pop::Battle => {
                for _ in 0..FRAME {
                    members.push([
                        r.bitsn(24),
                        r.bitsn(24),
                        r.bitsn(14),
                        r.bitsn(14),
                        r.bitsn(48),
                        r.bitsn(48),
                        r.below(8),
                        r.geometric(3) - 1,
                    ]);
                }
                (Kind::Sorted { order: 0 }, true)
            }
            Pop::Traders => {
                let k = Key::darwin(100 << 16, 0).unwrap();
                let (elo, llo) = (k.energy.get(), k.angular.get());
                for _ in 0..DOLL {
                    let t = r.bitsn(48);
                    let kind = r.below(64);
                    let e = elo + r.bitsn(40);
                    let l = llo + r.bitsn(38);
                    members.push(ship([t, kind, e, l, r.bitsn(32)]));
                }
                (Kind::Sorted { order: 1 }, true)
            }
            Pop::Random => {
                for _ in 0..DOLL {
                    let t = r.bitsn(64);
                    let kind = r.bitsn(16);
                    let e = 1 + r.below(16 << 48);
                    let l = (1 << 30) + r.below((4096u64 << 32) - (1 << 30) + 1);
                    members.push(ship([t, kind, e, l, r.bitsn(32)]));
                }
                (Kind::Sorted { order: 1 }, true)
            }
        };
        Group {
            members,
            kind,
            bits: r.bits,
            exchangeable,
        }
    }

    /// An event: a kick on an orbit ship; a contact on a battle member.
    pub fn kick(self, s: &Ship, r: &mut Rng) -> Ship {
        let mut s = *s;
        let d = |r: &mut Rng, b: u32| r.below(2 << b).wrapping_sub(1 << b);
        if self == Pop::Battle {
            s[0] = s[0].wrapping_add(d(r, 10)) & ((1 << 24) - 1);
            s[1] = s[1].wrapping_add(d(r, 10)) & ((1 << 24) - 1);
            s[2] = s[2].wrapping_add(d(r, 6)) & ((1 << 14) - 1);
            s[3] = s[3].wrapping_add(d(r, 6)) & ((1 << 14) - 1);
            s[4] = r.bitsn(48);
            s[5] = r.bitsn(48);
            s[7] += 1;
        } else {
            s[0] = s[0].wrapping_add(d(r, 16));
            s[2] = s[2].wrapping_add(d(r, 10));
            s[3] = s[3].wrapping_add(d(r, 10));
            s[4] = s[4].wrapping_add(d(r, 10)) & 0xFFFF_FFFF;
        }
        s
    }
}

/// The degradation ladder: a convoy launched every 2^12 time quanta (a perfect program), each
/// member kicked with probability `rate`; or a convoy with Poisson launches (no program); or
/// every field uniform over the law's ranges. Returns the members in birth order, the entropy
/// of the draws, and the launch program when there is one.
#[derive(Clone, Copy, Debug)]
pub enum Rung {
    Rate(f64),
    Poisson,
    Random,
}
pub fn ladder(rung: Rung, m: usize, g: u64) -> (Vec<Ship>, f64, Option<[Prog; MAXC]>) {
    let mut r = Rng::new(seed(99, g));
    let mut out = Vec::with_capacity(m);
    match rung {
        Rung::Rate(x) => {
            let kind = r.below(64);
            let (e, l) = orbit(&mut r);
            let (w, t0) = (r.bitsn(32), r.bitsn(48));
            let mut prog = [Prog::Const(0); MAXC];
            prog[0] = Prog::Affine { a: t0, b: 1 << 12 };
            (prog[1], prog[2], prog[3], prog[4]) = (
                Prog::Const(kind),
                Prog::Const(e),
                Prog::Const(l),
                Prog::Const(w),
            );
            for i in 0..m as u64 {
                let mut s = [0u64; MAXC];
                for f in 0..5 {
                    s[f] = prog[f].at(i);
                }
                if r.bernoulli_p(x) {
                    s = Pop::Convoy.kick(&s, &mut r);
                }
                out.push(s);
            }
            (out, r.bits, Some(prog))
        }
        Rung::Poisson => {
            let kind = r.below(64);
            let (e, l) = orbit(&mut r);
            let (w, mut t) = (r.bitsn(32), r.bitsn(48));
            for _ in 0..m {
                t += r.geometric(12);
                out.push([t, kind, e, l, w, 0, 0, 0]);
            }
            (out, r.bits, None)
        }
        Rung::Random => {
            for _ in 0..m {
                let t = r.bitsn(64);
                let kind = r.bitsn(16);
                let e = 1 + r.below(16 << 48);
                let l = (1 << 30) + r.below((4096u64 << 32) - (1 << 30) + 1);
                out.push([t, kind, e, l, r.bitsn(32), 0, 0, 0]);
            }
            (out, r.bits, None)
        }
    }
}
