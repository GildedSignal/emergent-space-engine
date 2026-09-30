//! The galaxy scene: one doll (a static central mass, G = c = M = 1) with ships of two kinds.
//!
//! * **Tubes**: real `emergent_space::Tube`s (16 bytes), stored grouped by compiled cycle.
//! * **Families**: a generator (mean key patch, phase window, orientation, count, seed). Ship `i`
//!   is materialized from the seed alone (`Scene::materialize`); nothing per ship is stored.
//!
//! Every orbit is a lattice cell: p = 12·2^(ip/32), e = ie/64, so keys repeat and share one
//! compiled `Cycle` (the memo). The display track below is a derived cache: it decides nothing.
use emergent_space::{Cycle, Key, Tube, Words};
use std::sync::atomic::{AtomicUsize, Ordering};
use std::time::Instant;

pub(crate) const NP: usize = 270;
pub(crate) const NE: usize = 52;
pub(crate) const CELLS: usize = NP * NE;
/// Ships per octave of p grow as p^GAMMA: a cusp of ships toward the centre.
const GAMMA: f64 = 0.5;
/// Display-track knots per half orbit (uniform in coordinate time).
pub(crate) const KNOTS: usize = 512;
const TAU: f64 = std::f64::consts::TAU;
const NO_REC: u32 = u32::MAX;

// ---------------------------------------------------------------- seeded hashing

pub(crate) fn mix(z: u64) -> u64 {
    let mut z = z.wrapping_add(0x9E37_79B9_7F4A_7C15);
    z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
    z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
    z ^ (z >> 31)
}
pub(crate) fn h2(a: u64, b: u64) -> u64 {
    mix(a ^ mix(b.wrapping_add(0x5851_F42D_4C95_7F2D)))
}
/// Uniform in [0, 1).
pub(crate) fn unit(x: u64) -> f64 {
    (x >> 11) as f64 / (1u64 << 53) as f64
}

// ---------------------------------------------------------------- the lattice of orbits

pub(crate) fn cell_pe(cell: usize) -> (f64, f64) {
    let (ip, ie) = (cell / NE, cell % NE);
    (12.0 * (ip as f64 / 32.0).exp2(), ie as f64 / 64.0)
}
/// A cell is used when its pericentre is at least 7 M (well inside the bound envelope).
pub(crate) fn cell_valid(cell: usize) -> bool {
    let (p, e) = cell_pe(cell);
    p / (1.0 + e) >= 7.0
}
pub(crate) fn cell_key(cell: usize) -> Result<Key, String> {
    let (p, e) = cell_pe(cell);
    Key::darwin((p * 65536.0).round() as u32, (e * 1073741824.0).round() as u32).map_err(|x| format!("cell {cell}: {x:?}"))
}
fn cell_weight(cell: usize) -> f64 {
    let (p, _) = cell_pe(cell);
    p.powf(GAMMA) * ((cell % NE) as f64 + 0.5)
}

/// Largest-remainder split of `total` by weights (deterministic, exact sum).
pub(crate) fn allocate(total: u64, w: &[f64]) -> Vec<u64> {
    let sum: f64 = w.iter().sum();
    let ideal = |i: usize| w[i] / sum * total as f64;
    let mut out: Vec<u64> = (0..w.len()).map(|i| ideal(i).floor() as u64).collect();
    let mut rem = total - out.iter().sum::<u64>();
    let mut frac: Vec<(f64, usize)> = (0..w.len()).map(|i| (ideal(i) - ideal(i).floor(), i)).collect();
    frac.sort_by(|a, b| b.0.total_cmp(&a.0).then(a.1.cmp(&b.1)));
    for (_, i) in frac {
        if rem == 0 {
            break;
        }
        out[i] += 1;
        rem -= 1;
    }
    out
}

// ---------------------------------------------------------------- the display track (a derived cache)

const GL_X: [f64; 2] = [0.339_981_043_584_856_3, 0.861_136_311_594_052_6];
const GL_W: [f64; 2] = [0.652_145_154_862_546_1, 0.347_854_845_137_453_8];

/// The compiled shape as floats: u = c + A cos ψ, dφ/dψ = g, dt/dψ = E g / (L u² (1 − 2u)).
struct Darwin {
    c: f64,
    a: f64,
    m3: f64,
    e: f64,
    l: f64,
}
impl Darwin {
    fn of(cycle: &Cycle) -> Self {
        let q = 2f64.powi(-62);
        let s = &cycle.shape;
        Self {
            c: s.c as f64 * q,
            a: s.a as f64 * q,
            m3: s.m3 as f64 * q,
            e: cycle.key.energy.get() as f64 * 2f64.powi(-48),
            l: cycle.key.angular.get() as f64 * 2f64.powi(-32),
        }
    }
    fn g(&self, psi: f64) -> f64 {
        1.0 / (2.0 * (self.m3 - self.a * psi.cos())).sqrt()
    }
    fn tdot(&self, psi: f64) -> f64 {
        let u = self.c + self.a * psi.cos();
        self.e * self.g(psi) / (self.l * u * u * (1.0 - 2.0 * u))
    }
    /// (∫ dt/dψ, ∫ dφ/dψ) over [lo, hi]: four-point Gauss–Legendre.
    fn integrate(&self, lo: f64, hi: f64) -> (f64, f64) {
        let (mid, half) = ((lo + hi) / 2.0, (hi - lo) / 2.0);
        let (mut t, mut p) = (0.0, 0.0);
        for i in 0..2 {
            for psi in [mid - half * GL_X[i], mid + half * GL_X[i]] {
                t += GL_W[i] * self.tdot(psi);
                p += GL_W[i] * self.g(psi);
            }
        }
        (t * half, p * half)
    }
}

/// Cubic Hermite value and slope (per unit x) on [0, 1] with endpoint values y and slopes d·h.
fn hermite(x: f64, y0: f64, y1: f64, m0: f64, m1: f64) -> (f64, f64) {
    let (x2, x3) = (x * x, x * x * x);
    let v = (2.0 * x3 - 3.0 * x2 + 1.0) * y0 + (x3 - 2.0 * x2 + x) * m0 + (-2.0 * x3 + 3.0 * x2) * y1 + (x3 - x2) * m1;
    let d = (6.0 * x2 - 6.0 * x) * y0 + (3.0 * x2 - 4.0 * x + 1.0) * m0 + (-6.0 * x2 + 6.0 * x) * y1 + (3.0 * x2 - 2.0 * x) * m1;
    (v, d)
}

/// Uniform-time samples of (r, φ in turns) over the outbound half orbit, padded one knot each side
/// by the mirror symmetries (r even and φ odd about periapsis; the reverse about apoapsis).
fn build_pad(cycle: &Cycle) -> Vec<[f32; 2]> {
    const K: usize = 128;
    let d = Darwin::of(cycle);
    let h = std::f64::consts::PI / K as f64;
    let (mut tk, mut pk) = ([0.0f64; K + 1], [0.0f64; K + 1]);
    for k in 0..K {
        let (t, p) = d.integrate(k as f64 * h, (k + 1) as f64 * h);
        tk[k + 1] = tk[k] + t;
        pk[k + 1] = pk[k] + p;
    }
    // Normalize to the law's own half-orbit totals (Q20 time, Q30 angle): the cache never disagrees
    // with the compiled period or advance.
    let half_t = cycle.half.t.get() as f64 * 2f64.powi(-20);
    let half_phi = cycle.half.phi.get() as f64 * 2f64.powi(-30);
    let (ft, fp) = (half_t / tk[K], half_phi / pk[K]);
    for k in 0..=K {
        tk[k] *= ft;
        pk[k] *= fp;
    }
    let tdot: Vec<f64> = (0..=K).map(|k| d.tdot(k as f64 * h) * ft).collect();
    let gdot: Vec<f64> = (0..=K).map(|k| d.g(k as f64 * h) * fp).collect();
    let mut knots = Vec::with_capacity(KNOTS + 1);
    let mut k = 0;
    for j in 0..=KNOTS {
        let s = half_t * j as f64 / KNOTS as f64;
        while k + 1 < K && tk[k + 1] < s {
            k += 1;
        }
        let (y0, y1) = (tk[k], tk[k + 1]);
        let (m0, m1) = (tdot[k] * h, tdot[k + 1] * h);
        let mut x = ((s - y0) / (y1 - y0)).clamp(0.0, 1.0);
        for _ in 0..6 {
            let (v, dv) = hermite(x, y0, y1, m0, m1);
            if dv <= 0.0 {
                break;
            }
            x = (x - (v - s) / dv).clamp(0.0, 1.0);
        }
        let psi = (k as f64 + x) * h;
        let (phi, _) = hermite(x, pk[k], pk[k + 1], gdot[k] * h, gdot[k + 1] * h);
        let u = d.c + d.a * psi.cos();
        knots.push([(1.0 / u) as f32, (phi / TAU) as f32]);
    }
    let mut pad = Vec::with_capacity(KNOTS + 3);
    pad.push([knots[1][0], -knots[1][1]]);
    pad.extend_from_slice(&knots);
    let last = knots[KNOTS];
    pad.push([knots[KNOTS - 1][0], 2.0 * last[1] - knots[KNOTS - 1][1]]);
    pad
}

#[inline(always)]
fn cr(p0: f32, p1: f32, p2: f32, p3: f32, f: f32) -> f32 {
    0.5 * (2.0 * p1 + (p2 - p0) * f + (2.0 * p0 - 5.0 * p1 + 4.0 * p2 - p3) * f * f + (3.0 * p1 - p0 - 3.0 * p2 + p3) * f * f * f)
}

/// One compiled orbit: the exact `Cycle` plus what the view derives from it.
pub(crate) struct KeyRec {
    pub cell: u32,
    /// The exact compiled cycle: the authority the display track is checked against.
    #[allow(dead_code)]
    pub cycle: Cycle,
    /// Coordinate period and half period (Q20), and the precession per cycle in wrapping turns.
    pub period: u64,
    pub half: u64,
    pub adv: u64,
    pub rmin: f32,
    pub rmax: f32,
    inv: f64,
    pad: Vec<[f32; 2]>,
}
impl KeyRec {
    pub(crate) fn build(cell: usize) -> Result<Self, String> {
        let cycle = Cycle::compile(cell_key(cell)?).map_err(|e| format!("cell {cell}: compile {e:?}"))?;
        let (period, half) = (cycle.increments.t.get(), cycle.half.t.get());
        let turns = cycle.increments.phi.get() as f64 / (1073741824.0 * TAU);
        let adv = ((turns - turns.floor()) * 18446744073709551616.0) as u64;
        let q = 2f64.powi(62);
        let (rmin, rmax) = ((q / cycle.shape.up as f64) as f32, (q / cycle.shape.ua as f64) as f32);
        let pad = build_pad(&cycle);
        Ok(Self { cell: cell as u32, cycle, period, half, adv, rmin, rmax, inv: KNOTS as f64 / half as f64, pad })
    }
    /// Elapsed time since periapsis `e` (Q20) → (r in M, angle in 32-bit turns), without orientation.
    #[inline(always)]
    pub fn locate(&self, e: u64) -> (f32, u32) {
        let n = e / self.period;
        let s = e - n * self.period;
        let inbound = s > self.half;
        let sx = if inbound { self.period - s } else { s };
        let x = sx as f64 * self.inv;
        let i = (x as usize).min(KNOTS - 1);
        let f = (x - i as f64) as f32;
        let p = &self.pad[i..i + 4];
        let r = cr(p[0][0], p[1][0], p[2][0], p[3][0], f);
        let ph = cr(p[0][1], p[1][1], p[2][1], p[3][1], f);
        let phu = (ph as f64 * 4294967296.0) as u32;
        let base = ((if inbound { n.wrapping_add(1) } else { n }).wrapping_mul(self.adv) >> 32) as u32;
        (r, if inbound { base.wrapping_sub(phu) } else { base.wrapping_add(phu) })
    }
    /// The exact integer-law readout: (r in M, angle in turns [0, 1)).
    #[cfg(test)]
    pub fn exact(&self, e: u64) -> Option<(f64, f64)> {
        let p = self.cycle.position(Words::new(e)).ok()?;
        let turns = p.phi.get() as f64 / (1073741824.0 * TAU);
        Some((2f64.powi(62) / p.u as f64, turns - turns.floor()))
    }
}

// ---------------------------------------------------------------- populations

pub(crate) struct TubeGroup {
    pub key: u32,
    pub start: usize,
    pub len: usize,
}

/// A generator of ships sharing a patch of neighbouring orbits (up to 3 × 3 lattice cells).
#[derive(Clone, Debug, PartialEq)]
pub(crate) struct Family {
    pub seed: u64,
    pub count: u64,
    pub cells: [u32; 9],
    pub nc: u8,
    /// Orientation of the periapsis at epoch, in 32-bit turns.
    pub omega0: u32,
    /// The phase window at t = 0, as fractions of the orbit's own period: [ph0, ph0 + width).
    pub ph0: f64,
    pub width: f64,
}
impl Family {
    pub fn group_count(&self, j: usize) -> u64 {
        let s = self.nc as u64;
        self.count / s + u64::from((j as u64) < self.count % s)
    }
    /// Ship `i` is member `i / S` of group `i % S`.
    #[allow(dead_code)]
    pub fn split(&self, i: u64) -> (usize, u64) {
        ((i % self.nc as u64) as usize, i / self.nc as u64)
    }
    /// Member `m` of group `j` (of `cj` members) has its phase in stratum `m` of the window, jittered
    /// by the seed: a stratified necklace along the orbit, the same on every call.
    pub fn phase(&self, j: usize, m: u64, cj: u64, period: u64) -> u64 {
        let u = unit(h2(self.seed ^ ((j as u64 + 1) << 56), m));
        let frac = self.ph0 + (m as f64 + u) / cj as f64 * self.width;
        (frac * period as f64) as u64
    }
}

/// A ship materialized from a seed.
#[allow(dead_code)]
#[derive(Clone, Copy, Debug, PartialEq)]
pub(crate) struct Ship {
    pub key: u32,
    pub tube: Tube,
    pub omega0: u32,
}

#[derive(Clone, Debug)]
pub(crate) struct Config {
    pub seed: u64,
    /// Total ships; the tubes are part of it and the rest are families.
    pub ships: u64,
    pub tubes: u64,
    /// Ships per family.
    pub family_size: u64,
    /// Fraction of families that are fleets (a narrow phase window) instead of belts.
    pub fleets: f64,
    pub threads: usize,
}
impl Default for Config {
    fn default() -> Self {
        Self { seed: 1, ships: 1_000_000_000, tubes: 1_000_000, family_size: 100_000, fleets: 0.1, threads: 4 }
    }
}

#[derive(Clone, Debug, Default)]
pub(crate) struct BuildStats {
    pub cells_valid: usize,
    pub compiled: usize,
    /// Key requests: every tube asks for its key and every family group asks for its key.
    pub lookups: u64,
    pub hit_rate: f64,
    pub ships_per_compile: f64,
    pub compile_wall_s: f64,
    pub tubes_wall_s: f64,
    pub total_wall_s: f64,
}

pub(crate) struct Scene {
    pub cfg: Config,
    pub keys: Vec<KeyRec>,
    pub cell_rec: Vec<u32>,
    pub cell_range: Vec<[f32; 2]>,
    pub cell_groups: Vec<u32>,
    pub tube_groups: Vec<TubeGroup>,
    pub tubes: Vec<Tube>,
    pub families: Vec<Family>,
    pub total_ships: u64,
    pub stats: BuildStats,
}

/// Run `f(i)` for i in 0..n on `threads` threads (work-stealing by an atomic counter).
pub(crate) fn parallel<T: Send>(n: usize, threads: usize, f: impl Fn(usize) -> T + Sync) -> Vec<T> {
    let next = AtomicUsize::new(0);
    let mut parts: Vec<Vec<(usize, T)>> = std::thread::scope(|s| {
        let hs: Vec<_> = (0..threads.max(1))
            .map(|_| {
                s.spawn(|| {
                    let mut mine = Vec::new();
                    loop {
                        let i = next.fetch_add(1, Ordering::Relaxed);
                        if i >= n {
                            return mine;
                        }
                        mine.push((i, f(i)));
                    }
                })
            })
            .collect();
        hs.into_iter().map(|h| h.join().unwrap()).collect()
    });
    let mut all: Vec<(usize, T)> = parts.drain(..).flatten().collect();
    all.sort_by_key(|x| x.0);
    all.into_iter().map(|x| x.1).collect()
}

impl Scene {
    pub fn build(cfg: &Config) -> Result<Scene, String> {
        let t0 = Instant::now();
        let valid: Vec<usize> = (0..CELLS).filter(|&c| cell_valid(c)).collect();
        let weights: Vec<f64> = valid.iter().map(|&c| cell_weight(c)).collect();
        let total_w: f64 = weights.iter().sum();
        let mut cdf = Vec::with_capacity(weights.len());
        let mut acc = 0.0;
        for w in &weights {
            acc += w / total_w;
            cdf.push(acc);
        }
        let tubes = cfg.tubes.min(cfg.ships);
        let tube_counts = allocate(tubes, &weights);

        // Families: centres drawn from the same distribution of orbits.
        let fam_ships = cfg.ships - tubes;
        let n_fam = fam_ships.div_ceil(cfg.family_size.max(1));
        let mut families = Vec::with_capacity(n_fam as usize);
        let mut cell_groups = vec![0u32; CELLS];
        for f in 0..n_fam {
            let seed = h2(cfg.seed, f + 1);
            let pick = cdf.partition_point(|&x| x < unit(h2(seed, 1))).min(valid.len() - 1);
            let centre = valid[pick];
            let (ip, ie) = ((centre / NE) as i64, (centre % NE) as i64);
            let mut cells = [0u32; 9];
            let mut nc = 0;
            for di in -1..=1i64 {
                for dj in -1..=1i64 {
                    let (a, b) = (ip + di, ie + dj);
                    if a >= 0 && (a as usize) < NP && b >= 0 && (b as usize) < NE && cell_valid(a as usize * NE + b as usize) {
                        cells[nc] = (a as usize * NE + b as usize) as u32;
                        nc += 1;
                    }
                }
            }
            let count = cfg.family_size.min(fam_ships - f * cfg.family_size);
            let fleet = unit(h2(seed, 2)) < cfg.fleets;
            let (ph0, width) = if fleet { (unit(h2(seed, 3)), 0.004 + 0.05 * unit(h2(seed, 4))) } else { (0.0, 1.0) };
            for &c in &cells[..nc] {
                cell_groups[c as usize] += 1;
            }
            families.push(Family { seed, count, cells, nc: nc as u8, omega0: (h2(seed, 5) >> 32) as u32, ph0, width });
        }

        // The memo: every orbit that any tube or family group asks for is compiled once.
        let mut used = vec![false; CELLS];
        for (i, &c) in valid.iter().enumerate() {
            used[c] |= tube_counts[i] > 0;
        }
        for c in 0..CELLS {
            used[c] |= cell_groups[c] > 0;
        }
        let used_cells: Vec<usize> = (0..CELLS).filter(|&c| used[c]).collect();
        let t1 = Instant::now();
        let recs = parallel(used_cells.len(), cfg.threads, |i| KeyRec::build(used_cells[i]));
        let mut keys = Vec::with_capacity(recs.len());
        for r in recs {
            keys.push(r?);
        }
        let compile_wall_s = t1.elapsed().as_secs_f64();
        let mut cell_rec = vec![NO_REC; CELLS];
        let mut cell_range = vec![[0.0f32; 2]; CELLS];
        for (i, k) in keys.iter().enumerate() {
            cell_rec[k.cell as usize] = i as u32;
            cell_range[k.cell as usize] = [k.rmin, k.rmax];
        }

        // Tubes: grouped by cell, filled in parallel, each phase uniform over its own period.
        let t2 = Instant::now();
        let mut tube_groups = Vec::new();
        let mut start = 0usize;
        for (i, &c) in valid.iter().enumerate() {
            if tube_counts[i] > 0 {
                tube_groups.push(TubeGroup { key: cell_rec[c], start, len: tube_counts[i] as usize });
                start += tube_counts[i] as usize;
            }
        }
        let mut all_tubes = vec![Tube::new(Words::new(0), Words::new(0)); start];
        {
            let mut slices: Vec<&mut [Tube]> = Vec::with_capacity(tube_groups.len());
            let mut rest: &mut [Tube] = &mut all_tubes;
            for g in &tube_groups {
                let (a, b) = rest.split_at_mut(g.len);
                slices.push(a);
                rest = b;
            }
            let slots: Vec<std::sync::Mutex<&mut [Tube]>> = slices.into_iter().map(std::sync::Mutex::new).collect();
            parallel(tube_groups.len(), cfg.threads, |gi| {
                let g = &tube_groups[gi];
                let rec = &keys[g.key as usize];
                let salt = cfg.seed ^ ((rec.cell as u64) << 32) ^ 0x7A3B;
                let mut slot = slots[gi].lock().unwrap();
                for (m, tube) in slot.iter_mut().enumerate() {
                    let phase = (unit(h2(salt, m as u64)) * rec.period as f64) as u64;
                    *tube = Tube::new(Words::new(0), Words::new(phase));
                }
            });
        }
        let tubes_wall_s = t2.elapsed().as_secs_f64();

        let groups: u64 = cell_groups.iter().map(|&g| g as u64).sum();
        let lookups = tubes + groups;
        let total_ships = tubes + fam_ships;
        let stats = BuildStats {
            cells_valid: valid.len(),
            compiled: keys.len(),
            lookups,
            hit_rate: 1.0 - keys.len() as f64 / lookups.max(1) as f64,
            ships_per_compile: total_ships as f64 / keys.len().max(1) as f64,
            compile_wall_s,
            tubes_wall_s,
            total_wall_s: t0.elapsed().as_secs_f64(),
        };
        Ok(Scene { cfg: cfg.clone(), keys, cell_rec, cell_range, cell_groups, tube_groups, tubes: all_tubes, families, total_ships, stats })
    }

    /// Ship `i` of family `f`, from its seed alone (the same on every call).
    #[allow(dead_code)]
    pub fn materialize(&self, f: usize, i: u64) -> Ship {
        let fam = &self.families[f];
        let (j, m) = fam.split(i);
        let key = self.cell_rec[fam.cells[j] as usize];
        let rec = &self.keys[key as usize];
        let phase = fam.phase(j, m, fam.group_count(j), rec.period);
        Ship { key, tube: Tube::new(Words::new(0), Words::new(phase)), omega0: fam.omega0 }
    }
}
