//! Boxes, separation, islands and the certificate's coalescing step.
use emergent_lattice::law::World;
use serde::Serialize;
use std::collections::HashMap;

/// Axis-aligned box of body centres, in 1/Q units, inclusive. Empty when lo > hi.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize)]
pub struct Aabb {
    pub lo: [i64; 2],
    pub hi: [i64; 2],
}

/// Far beyond the law's coordinate range (2^39) and still safe to grow and compare.
const FAR: i64 = 1 << 61;

impl Aabb {
    pub const EMPTY: Aabb = Aabb { lo: [i64::MAX; 2], hi: [i64::MIN; 2] };
    pub const EVERYWHERE: Aabb = Aabb { lo: [-FAR; 2], hi: [FAR; 2] };

    pub fn of<'a>(xs: impl IntoIterator<Item = &'a [i64; 2]>) -> Aabb {
        xs.into_iter().fold(Aabb::EMPTY, |b, x| Aabb {
            lo: [b.lo[0].min(x[0]), b.lo[1].min(x[1])],
            hi: [b.hi[0].max(x[0]), b.hi[1].max(x[1])],
        })
    }

    pub fn is_empty(&self) -> bool {
        self.lo[0] > self.hi[0] || self.lo[1] > self.hi[1]
    }

    pub fn grow(&self, g: i64) -> Aabb {
        if self.is_empty() {
            return *self;
        }
        let g = g.clamp(0, FAR);
        Aabb {
            lo: [(self.lo[0] - g).max(-FAR), (self.lo[1] - g).max(-FAR)],
            hi: [(self.hi[0] + g).min(FAR), (self.hi[1] + g).min(FAR)],
        }
    }

    pub fn hull(&self, o: &Aabb) -> Aabb {
        if self.is_empty() {
            return *o;
        }
        if o.is_empty() {
            return *self;
        }
        Aabb { lo: [self.lo[0].min(o.lo[0]), self.lo[1].min(o.lo[1])], hi: [self.hi[0].max(o.hi[0]), self.hi[1].max(o.hi[1])] }
    }

    /// Intersection; empty when the two promises are inconsistent (verification will then fail).
    pub fn meet(&self, o: &Aabb) -> Aabb {
        Aabb { lo: [self.lo[0].max(o.lo[0]), self.lo[1].max(o.lo[1])], hi: [self.hi[0].min(o.hi[0]), self.hi[1].min(o.hi[1])] }
    }

    pub fn contains(&self, o: &Aabb) -> bool {
        o.is_empty() || (!self.is_empty() && (0..2).all(|c| self.lo[c] <= o.lo[c] && o.hi[c] <= self.hi[c]))
    }

    /// Euclidean distance from a point to the box (0 inside), in 1/Q units.
    pub fn distance(&self, p: [i64; 2]) -> f64 {
        if self.is_empty() {
            return f64::INFINITY;
        }
        let d = |c: usize| (self.lo[c] as f64 - p[c] as f64).max(p[c] as f64 - self.hi[c] as f64).max(0.0);
        d(0).hypot(d(1))
    }
}

/// No body of one box can hit a body of the other: on some axis the centre gap exceeds the
/// largest possible reach. The bin predicate only sees positions on the segment between two
/// ticks, which stays inside a box that holds both ends (convexity).
pub fn separated(a: &Aabb, ra: i64, b: &Aabb, rb: i64) -> bool {
    if a.is_empty() || b.is_empty() {
        return true;
    }
    let reach = ra as i128 + rb as i128;
    (0..2).any(|c| b.lo[c] as i128 - a.hi[c] as i128 > reach || a.lo[c] as i128 - b.hi[c] as i128 > reach)
}

pub(crate) struct Uf(Vec<usize>);

impl Uf {
    pub fn new(n: usize) -> Self {
        Uf((0..n).collect())
    }
    pub fn find(&mut self, mut i: usize) -> usize {
        while self.0[i] != i {
            self.0[i] = self.0[self.0[i]];
            i = self.0[i];
        }
        i
    }
    pub fn union(&mut self, a: usize, b: usize) -> bool {
        let (a, b) = (self.find(a), self.find(b));
        if a == b {
            return false;
        }
        let (lo, hi) = (a.min(b), a.max(b));
        self.0[hi] = lo;
        true
    }
    /// Groups of indices by root, ordered by their smallest member.
    pub fn groups(&mut self) -> Vec<Vec<usize>> {
        let n = self.0.len();
        let mut at: HashMap<usize, usize> = HashMap::new();
        let mut out: Vec<Vec<usize>> = Vec::new();
        for i in 0..n {
            let r = self.find(i);
            let g = *at.entry(r).or_insert_with(|| {
                out.push(Vec::new());
                out.len() - 1
            });
            out[g].push(i);
        }
        out
    }
}

/// A planning entity: a set of members, the box their centres are promised to stay in over one
/// window, and their largest radius.
#[derive(Clone, Debug)]
pub(crate) struct Ent<T> {
    pub ids: Vec<T>,
    pub bbox: Aabb,
    pub r: i64,
}

/// Unite entities whose boxes are not separated, re-hulling until none conflict (a united
/// hull can reach a third entity). Sweep on x keeps it O(E log E) when boxes are sparse.
pub(crate) fn coalesce<T>(mut ents: Vec<Ent<T>>) -> Vec<Ent<T>> {
    loop {
        let rmax = ents.iter().map(|e| e.r).max().unwrap_or(0) as i128;
        let mut order: Vec<usize> = (0..ents.len()).filter(|&i| !ents[i].bbox.is_empty()).collect();
        order.sort_by_key(|&i| ents[i].bbox.lo[0]);
        let mut uf = Uf::new(ents.len());
        let mut any = false;
        for (a, &i) in order.iter().enumerate() {
            let (bi, ri) = (ents[i].bbox, ents[i].r);
            for &j in &order[a + 1..] {
                if ents[j].bbox.lo[0] as i128 - bi.hi[0] as i128 > ri as i128 + rmax {
                    break;
                }
                if !separated(&bi, ri, &ents[j].bbox, ents[j].r) {
                    any |= uf.union(i, j);
                }
            }
        }
        if !any {
            return ents;
        }
        let groups = uf.groups();
        let mut slots: Vec<Option<Ent<T>>> = ents.into_iter().map(Some).collect();
        ents = groups
            .into_iter()
            .map(|g| {
                let mut it = g.into_iter().map(|i| slots[i].take().expect("each entity joins one group"));
                let mut acc = it.next().expect("groups are non-empty");
                for e in it {
                    acc.ids.extend(e.ids);
                    acc.bbox = acc.bbox.hull(&e.bbox);
                    acc.r = acc.r.max(e.r);
                }
                acc
            })
            .collect();
    }
}

/// Islands of a world: bodies i, j are linked when on both axes |x_i − x_j| ≤ r_i + r_j + extra
/// (their boxes grown by extra/2 touch), and consumed contacts always link (a region's
/// stepper must see both ends of a live consumed pair). Grid cells of side 2·r_min + extra
/// link everything inside one cell for free; neighbouring cells stop at their first link.
pub fn components(w: &World, extra: i64) -> Vec<Vec<usize>> {
    let n = w.bodies.len();
    if n == 0 {
        return vec![];
    }
    let rmin = w.bodies.iter().map(|b| b.radius).min().unwrap_or(1);
    let rmax = w.max_radius();
    let extra = extra.clamp(0, FAR);
    let cell = (2 * rmin + extra).max(1);
    let span = ((2 * rmax + extra) + cell - 1) / cell;
    let mut grid: HashMap<(i64, i64), Vec<usize>> = HashMap::new();
    for (i, b) in w.bodies.iter().enumerate() {
        grid.entry((b.x[0].div_euclid(cell), b.x[1].div_euclid(cell))).or_default().push(i);
    }
    let mut uf = Uf::new(n);
    for list in grid.values() {
        for &i in &list[1..] {
            uf.union(list[0], i);
        }
    }
    let linked = |i: usize, j: usize| {
        let (a, b) = (&w.bodies[i], &w.bodies[j]);
        let lim = a.radius as i128 + b.radius as i128 + extra as i128;
        (0..2).all(|c| (a.x[c] as i128 - b.x[c] as i128).abs() <= lim)
    };
    let mut keys: Vec<(i64, i64)> = grid.keys().copied().collect();
    keys.sort_unstable();
    for &(cx, cy) in &keys {
        let a = &grid[&(cx, cy)];
        for dx in -span..=span {
            for dy in -span..=span {
                if (dx, dy) <= (0, 0) {
                    continue;
                }
                let Some(o) = grid.get(&(cx + dx, cy + dy)) else { continue };
                if uf.find(a[0]) == uf.find(o[0]) {
                    continue;
                }
                'pairs: for &i in a {
                    for &j in o {
                        if linked(i, j) {
                            uf.union(i, j);
                            break 'pairs;
                        }
                    }
                }
            }
        }
    }
    for c in &w.consumed {
        if let (Some(i), Some(j)) = (w.index_of(c.a), w.index_of(c.b)) {
            uf.union(i, j);
        }
    }
    uf.groups()
}

/// Islands worth a region: [`components`] at the given link distance, doubled until at most a
/// tenth of the bodies sit in islands smaller than `min` (or everything is one island). A
/// zero or tiny forecast speed would otherwise cut a cluster into single bodies.
pub fn islands(w: &World, extra: i64, min: usize) -> Vec<Vec<usize>> {
    let mut x = extra.max(0);
    loop {
        let c = components(w, x);
        let small: usize = c.iter().filter(|g| g.len() < min).map(|g| g.len()).sum();
        if c.len() <= 1 || small * 10 <= w.bodies.len() || x >= FAR {
            return c;
        }
        x = x.max(2 * w.max_radius()).saturating_mul(2).min(FAR);
    }
}
