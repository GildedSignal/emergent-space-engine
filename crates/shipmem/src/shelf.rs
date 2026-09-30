//! A shelf: the ships of one doll (or one slice of it), as groups of blocks in one arena.
//!
//! - A **group** is a shared description written once: its reference (its first member, a
//!   real ship) and, for a formation, its lattice (two steps between real members). Members
//!   follow in a canonical order that time does not change: slot order for a formation,
//!   sorted order otherwise (a convoy by periapsis time, which is its order along the orbit).
//! - A **block** holds up to `bsize` consecutive members, encoded by `codec`.
//! - **Events** go to the hot tier: the old slot is marked dead, the new state is appended in
//!   working form (O(1)). `compact` (idle time) seals them as scars: exact deltas from the
//!   packed base, at the ship's own slot (identity is provenance), in a sparse layer per group.
//!   A group whose scars outgrow half its blocks is repacked.
use crate::bits::*;
use crate::codec::*;
use crate::program::{Scars, RB};
use std::cmp::Ordering;
use std::collections::HashMap;
use std::hash::{BuildHasherDefault, Hasher};
use std::time::Instant;

pub type Ship = [u64; MAXC];
/// The largest group: a domain of at most 2^16 slots.
pub const MAXG: usize = 1 << 16;

#[derive(Default)]
pub struct Fx(u64);
impl Hasher for Fx {
    fn finish(&self) -> u64 {
        self.0
    }
    fn write(&mut self, bytes: &[u8]) {
        for &b in bytes {
            self.0 = (self.0 ^ b as u64).wrapping_mul(0x9E37_79B9_7F4A_7C15);
        }
    }
    fn write_u32(&mut self, x: u32) {
        self.0 = (x as u64).wrapping_mul(0x9E37_79B9_7F4A_7C15);
    }
}
pub type FxMap<K, V> = HashMap<K, V, BuildHasherDefault<Fx>>;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Kind {
    /// Slot order; `grid` > 0: members sit on a lattice of `grid` columns.
    Slot { grid: u16 },
    /// Sorted by `orders[order]`.
    Sorted { order: u8 },
}

#[derive(Clone, Copy, Debug)]
pub struct BlockRef {
    pub off: u32,
    pub start: u32,
    pub group: u32,
    pub len: u16,
    pub n: u16,
}
#[derive(Clone, Copy, Debug)]
pub struct GroupRef {
    pub first: u32,
    pub nb: u32,
    pub n: u32,
    pub ref_off: u32,
    pub kind: Kind,
    pub mask: u8,
}
#[derive(Clone, Copy)]
pub struct Hot {
    pub ship: Ship,
    pub handle: u32,
    pub group: u32,
}
struct Hdr {
    refs: [u64; MAXC],
    b1: [Step; MAXC],
    b2: [Step; MAXC],
    end: usize,
}

#[derive(Default, Debug, Clone)]
pub struct CompactStats {
    pub blocks_rewritten: u64,
    pub repacks: u64,
    pub max_step_ns: u64,
    pub arena_compactions: u64,
    pub arena_ns: u64,
}

pub fn cmp(a: &Ship, b: &Ship, order: &[u8; MAXC], cols: usize) -> Ordering {
    for &f in &order[..cols] {
        match a[f as usize].cmp(&b[f as usize]) {
            Ordering::Equal => {}
            o => return o,
        }
    }
    Ordering::Equal
}

/// A lattice step as an exact rational: `num / den` per row or column, taken between two
/// real members `den` slots apart (so a member's jitter is divided, never multiplied).
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
pub struct Step {
    pub num: i64,
    pub den: u32,
}
impl Step {
    #[inline]
    fn at(self, x: i64) -> i64 {
        match x.checked_mul(self.num) {
            Some(p) => p.div_euclid(self.den as i64),
            None => ((x as i128 * self.num as i128).div_euclid(self.den as i128)) as i64,
        }
    }
}
#[inline]
fn lattice(refv: u64, row: Step, col: Step, rank: usize, grid: usize) -> u64 {
    let (r, c) = ((rank / grid) as i64, (rank % grid) as i64);
    refv.wrapping_add(row.at(r) as u64)
        .wrapping_add(col.at(c) as u64)
}

/// Predictions for ranks start..start+n, row by row (no division per member).
fn lattice_run(refv: u64, row: Step, col: Step, start: usize, grid: usize, out: &mut [u64]) {
    let mut ct = [0i64; 64];
    for (c, t) in ct.iter_mut().enumerate().take(grid) {
        *t = col.at(c as i64);
    }
    let (mut r, mut c) = (start / grid, start % grid);
    let mut rt = row.at(r as i64);
    for o in out.iter_mut() {
        *o = refv.wrapping_add(rt as u64).wrapping_add(ct[c] as u64);
        c += 1;
        if c == grid {
            c = 0;
            r += 1;
            rt = row.at(r as i64);
        }
    }
}

/// Pick, per column, the row and column steps (from pairs of real members far apart) that make
/// the residuals smallest; keep the lattice only where it beats plain offsets from the reference.
fn choose_grid(m: &[Ship], k: usize, cols: usize) -> ([Step; MAXC], [Step; MAXC], u8) {
    let n = m.len();
    let (mut rs, mut cs, mut mask) = ([Step::default(); MAXC], [Step::default(); MAXC], 0u8);
    let sample: Vec<usize> = (0..n).step_by(n.div_ceil(256).max(1)).collect();
    let step = |f: usize, a: usize, b: usize, den: usize| Step {
        num: m[b][f].wrapping_sub(m[a][f]) as i64,
        den: den as u32,
    };
    let rows = n / k;
    for f in 0..cols {
        let plain: u64 = sample
            .iter()
            .map(|&i| bitlen(zz64(m[i][f].wrapping_sub(m[0][f]) as i64)) as u64)
            .sum();
        let mut best = (plain, Step::default(), Step::default(), false);
        let mut cc = vec![Step { num: 0, den: 1 }];
        for q in 0..rows.min(2) {
            for (a, b) in [(0, k - 1), (1, k - 1), (0, k - 2), (1, k - 2)] {
                if b > a {
                    cc.push(step(f, q * k + a, q * k + b, b - a));
                }
            }
        }
        let mut rc = vec![Step { num: 0, den: 1 }];
        if rows >= 2 {
            let r = rows - 1;
            for (a, b, c0) in [
                (0, r, 0),
                (0, r, 1),
                (1, r, 0),
                (1, r, 1),
                (0, r.saturating_sub(1), 0),
            ] {
                if b > a && c0 < k {
                    rc.push(step(f, a * k + c0, b * k + c0, b - a));
                }
            }
        }
        // Separable choice: the column step against each row's first member, then the row step.
        let row_first = |i: usize| m[(i / k) * k][f];
        let col_cost = |c: Step| -> u64 {
            sample
                .iter()
                .map(|&i| {
                    bitlen(zz64(
                        m[i][f]
                            .wrapping_sub(row_first(i))
                            .wrapping_sub(c.at((i % k) as i64) as u64)
                            as i64,
                    )) as u64
                })
                .sum()
        };
        let c = *cc.iter().min_by_key(|&&c| col_cost(c)).unwrap();
        for &r in &rc {
            let cost: u64 = sample
                .iter()
                .map(|&i| {
                    bitlen(zz64(
                        m[i][f].wrapping_sub(lattice(m[0][f], r, c, i, k)) as i64
                    )) as u64
                })
                .sum();
            if cost < best.0 {
                best = (cost, r, c, true);
            }
        }
        if best.3 {
            (rs[f], cs[f]) = (best.1, best.2);
            mask |= 1 << f;
        }
    }
    (rs, cs, mask)
}

/// What a group shares beyond its reference: for a few columns, a dictionary of the values its
/// members take (indices are stored instead), or a map from an earlier dictionary column's index
/// (L follows E: residuals are stored, zero unless scarred). Dictionaries grow at scars. A
/// column is shared only when that costs less than the per-block dictionaries it replaces.
#[derive(Default, Clone)]
pub struct Share {
    pub cols: Vec<ShareCol>,
}
#[derive(Clone)]
pub struct ShareCol {
    pub f: u8,
    /// 255: a dictionary; otherwise the dictionary column this one is a function of.
    pub src: u8,
    pub vals: Vec<u64>,
}
impl Share {
    fn bytes(&self) -> usize {
        std::mem::size_of::<Self>()
            + self
                .cols
                .iter()
                .map(|c| std::mem::size_of::<ShareCol>() + c.vals.capacity() * 8)
                .sum::<usize>()
    }
    /// Values → stored form, in place (dictionary columns become indices).
    fn forward(&mut self, buf: &mut Buf) {
        let n = buf.n;
        let mut idx: Vec<(u8, [u64; MAXB])> = Vec::new();
        for c in self.cols.iter_mut().filter(|c| c.src == 255) {
            let mut ix = [0u64; MAXB];
            for (i, x) in ix.iter_mut().enumerate().take(n) {
                let v = buf.col[c.f as usize][i];
                *x = match c.vals.iter().position(|&y| y == v) {
                    Some(k) => k as u64,
                    None => {
                        c.vals.push(v);
                        (c.vals.len() - 1) as u64
                    }
                };
            }
            idx.push((c.f, ix));
        }
        for c in self.cols.iter_mut().filter(|c| c.src != 255) {
            let ix = &idx.iter().find(|x| x.0 == c.src).unwrap().1;
            let f = c.f as usize;
            for i in 0..n {
                let k = ix[i] as usize;
                if k >= c.vals.len() {
                    c.vals.resize(k + 1, buf.col[f][i]);
                }
                buf.col[f][i] = zz64(buf.col[f][i].wrapping_sub(c.vals[k]) as i64);
            }
        }
        for (f, ix) in idx {
            buf.col[f as usize][..n].copy_from_slice(&ix[..n]);
        }
    }
    fn inverse(&self, col: &mut [[u64; MAXB]], n: usize) {
        for c in self.cols.iter().filter(|c| c.src != 255) {
            let (f, src) = (c.f as usize, c.src as usize);
            for i in 0..n {
                col[f][i] = c.vals[col[src][i] as usize].wrapping_add(unzz64(col[f][i]) as u64);
            }
        }
        for c in self.cols.iter().filter(|c| c.src == 255) {
            let f = c.f as usize;
            for i in 0..n {
                col[f][i] = c.vals[col[f][i] as usize];
            }
        }
    }
    fn inverse1(&self, out: &mut Ship) {
        for c in self.cols.iter().filter(|c| c.src != 255) {
            out[c.f as usize] =
                c.vals[out[c.src as usize] as usize].wrapping_add(unzz64(out[c.f as usize]) as u64);
        }
        for c in self.cols.iter().filter(|c| c.src == 255) {
            out[c.f as usize] = c.vals[out[c.f as usize] as usize];
        }
    }
    fn is_shared(&self, f: usize) -> bool {
        self.cols.iter().any(|c| c.f as usize == f)
    }
    /// `skip` marks lattice columns; `bs` is the block size.
    fn choose(m: &[Ship], cols: usize, skip: u8, bs: usize) -> Option<Box<Share>> {
        let n = m.len();
        let nb = n.div_ceil(bs);
        let mut sh = Share::default();
        for f in 0..cols {
            if skip >> f & 1 == 1 {
                continue;
            }
            let mut d: Vec<u64> = Vec::new();
            for s in m {
                if !d.contains(&s[f]) {
                    d.push(s[f]);
                    if d.len() > 256 {
                        break;
                    }
                }
            }
            if d.len() < 2 || d.len() > 256 {
                continue;
            }
            let mut sorted = d.clone();
            sorted.sort_unstable();
            let span = sorted[sorted.len() - 1] - sorted[0];
            let entry_bytes = (bitlen(span / sorted.len() as u64 + 1) as usize)
                .div_ceil(7)
                .max(1);
            let per_block = d.len().min(bs) * entry_bytes + 3;
            let cost = std::mem::size_of::<ShareCol>() + 8 * d.len() + 16;
            if nb * per_block <= cost {
                continue;
            }
            let pos = |c: &ShareCol, v: u64| c.vals.iter().position(|&x| x == v).unwrap();
            let tie = sh.cols.iter().filter(|c| c.src == 255).find(|c| {
                let mut map = vec![None::<u64>; c.vals.len()];
                m.iter()
                    .all(|s| *map[pos(c, s[c.f as usize])].get_or_insert(s[f]) == s[f])
            });
            let col = match tie {
                Some(c) => {
                    let mut map = vec![0u64; c.vals.len()];
                    for s in m {
                        map[pos(c, s[c.f as usize])] = s[f];
                    }
                    ShareCol {
                        f: f as u8,
                        src: c.f,
                        vals: map,
                    }
                }
                None => ShareCol {
                    f: f as u8,
                    src: 255,
                    vals: d,
                },
            };
            sh.cols.push(col);
        }
        (!sh.cols.is_empty()).then(|| Box::new(sh))
    }
}

pub struct Shelf {
    pub cols: usize,
    pub shares: Vec<Option<Box<Share>>>,
    pub bsize: usize,
    pub arena: Vec<u8>,
    pub garbage: usize,
    pub blocks: Vec<BlockRef>,
    pub dead: Vec<u16>,
    pub groups: Vec<GroupRef>,
    pub orders: Vec<[u8; MAXC]>,
    pub scars: Vec<Option<Box<Scars>>>,
    trial_k: Vec<u32>,
    pub hot: Vec<Hot>,
    pub forward: FxMap<u32, u32>,
    pub enc: Enc,
    pub buf: Buf,
    pub n: u64,
    scratch: Vec<u8>,
}

impl Shelf {
    pub fn new(cols: usize, bsize: usize, orders: Vec<[u8; MAXC]>, chord: bool) -> Self {
        assert!(cols <= MAXC && bsize <= MAXB / 2 && bsize > 0);
        Self {
            cols,
            bsize,
            arena: vec![0; PAD],
            garbage: 0,
            blocks: Vec::new(),
            dead: Vec::new(),
            groups: Vec::new(),
            shares: Vec::new(),
            orders,
            scars: Vec::new(),
            trial_k: Vec::new(),
            hot: Vec::new(),
            forward: FxMap::default(),
            enc: Enc::new(chord),
            buf: Buf::default(),
            n: 0,
            scratch: Vec::new(),
        }
    }

    /// Bytes held: arena, block and group tables, hot tier and its forwarding map.
    pub fn bytes(&self) -> usize {
        self.arena.capacity()
            + self.blocks.capacity() * std::mem::size_of::<BlockRef>()
            + self.dead.capacity() * 2
            + self.groups.capacity() * std::mem::size_of::<GroupRef>()
            + self.shares.capacity() * 8
            + self
                .shares
                .iter()
                .flatten()
                .map(|s| s.bytes())
                .sum::<usize>()
            + self.scars.capacity() * 8
            + self.trial_k.capacity() * 4
            + self
                .scars
                .iter()
                .flatten()
                .map(|s| s.bytes())
                .sum::<usize>()
            + self.hot.capacity() * std::mem::size_of::<Hot>()
            + self.forward.capacity() * 9
    }
    pub fn shrink(&mut self) {
        self.shares.shrink_to_fit();
        self.arena.shrink_to_fit();
        self.blocks.shrink_to_fit();
        self.dead.shrink_to_fit();
        self.groups.shrink_to_fit();
        self.hot.shrink_to_fit();
        self.forward.shrink_to_fit();
    }

    fn append(&mut self, bytes: &[u8]) -> u32 {
        let off = self.arena.len() - PAD;
        self.arena.truncate(off);
        self.arena.extend_from_slice(bytes);
        self.arena.extend_from_slice(&[0; PAD]);
        u32::try_from(off).expect("shelf arena above 4 GB")
    }

    fn hdr(&self, g: usize) -> Hdr {
        let gr = &self.groups[g];
        let mut p = gr.ref_off as usize;
        let a = &self.arena;
        let mut h = Hdr {
            refs: [0; MAXC],
            b1: [Step::default(); MAXC],
            b2: [Step::default(); MAXC],
            end: 0,
        };
        for f in 0..self.cols {
            h.refs[f] = get_uv(a, &mut p) as u64;
        }
        if matches!(gr.kind, Kind::Slot { grid } if grid > 0) {
            for f in 0..self.cols {
                if gr.mask >> f & 1 == 1 {
                    h.b1[f] = Step {
                        num: get_zz(a, &mut p) as i64,
                        den: get_uv(a, &mut p) as u32,
                    };
                    h.b2[f] = Step {
                        num: get_zz(a, &mut p) as i64,
                        den: get_uv(a, &mut p) as u32,
                    };
                }
            }
        }
        h.end = p;
        h
    }
    fn brefs(&self, g: usize, h: &Hdr) -> [u64; MAXC] {
        let mask = self.groups[g].mask;
        let mut r = h.refs;
        for (f, x) in r.iter_mut().enumerate() {
            if mask >> f & 1 == 1 {
                *x = 0;
            }
        }
        if let Some(sh) = &self.shares[g] {
            for (f, x) in r.iter_mut().enumerate().take(self.cols) {
                if sh.is_shared(f) {
                    *x = 0;
                }
            }
        }
        r
    }
    fn grid(&self, g: usize) -> usize {
        match self.groups[g].kind {
            Kind::Slot { grid } => grid as usize,
            _ => 0,
        }
    }

    /// Encode `buf` (full values) as block `bi`'s new content, or as a new block if `bi` is None.
    fn put(&mut self, g: usize, start: usize, bi: Option<usize>) -> usize {
        let h = self.hdr(g);
        let brefs = self.brefs(g, &h);
        let (mask, grid) = (self.groups[g].mask, self.grid(g));
        let n = self.buf.n;
        if mask != 0 {
            for f in 0..self.cols {
                if mask >> f & 1 == 1 {
                    let mut pred = [0u64; MAXB];
                    lattice_run(h.refs[f], h.b1[f], h.b2[f], start, grid, &mut pred[..n]);
                    for i in 0..n {
                        self.buf.col[f][i] = zz64(self.buf.col[f][i].wrapping_sub(pred[i]) as i64);
                    }
                }
            }
        }
        if let Some(mut sh) = self.shares[g].take() {
            sh.forward(&mut self.buf);
            self.shares[g] = Some(sh);
        }
        let mut out = std::mem::take(&mut self.scratch);
        out.clear();
        self.enc.block(self.cols, &self.buf, &brefs, &mut out);
        let len = u16::try_from(out.len()).expect("block above 64 KB");
        let idx = match bi {
            Some(bi) => {
                let old = self.blocks[bi];
                let off = if out.len() <= old.len as usize {
                    let o = old.off as usize;
                    self.arena[o..o + out.len()].copy_from_slice(&out);
                    self.garbage += old.len as usize - out.len();
                    old.off
                } else {
                    self.garbage += old.len as usize;
                    self.append(&out)
                };
                self.blocks[bi] = BlockRef {
                    off,
                    start: start as u32,
                    group: g as u32,
                    len,
                    n: n as u16,
                };
                bi
            }
            None => {
                let off = self.append(&out);
                self.blocks.push(BlockRef {
                    off,
                    start: start as u32,
                    group: g as u32,
                    len,
                    n: n as u16,
                });
                self.dead.push(0);
                self.blocks.len() - 1
            }
        };
        self.scratch = out;
        idx
    }

    /// Write a population: canonical order, then groups of at most `MAXG` members (a domain
    /// this size bounds every compaction step). Returns the range of group ids.
    pub fn add_group(&mut self, members: &mut [Ship], kind: Kind) -> std::ops::Range<u32> {
        let cols = self.cols;
        if let Kind::Sorted { order } = kind {
            let o = self.orders[order as usize];
            members.sort_unstable_by(|a, b| cmp(a, b, &o, cols));
        }
        let g0 = self.groups.len() as u32;
        for chunk in members.chunks_mut(MAXG) {
            self.add_one(chunk, kind);
        }
        g0..self.groups.len() as u32
    }

    /// Write one group once: its reference, its lattice if any, then its blocks.
    fn add_one(&mut self, members: &mut [Ship], kind: Kind) -> u32 {
        let cols = self.cols;
        let n = members.len();
        assert!(n > 0);
        let grid = match kind {
            Kind::Slot { grid } => grid as usize,
            _ => 0,
        };
        assert!(grid <= 64);
        let (b1, b2, mask) = if grid > 1 && n > 1 {
            choose_grid(members, grid, cols)
        } else {
            ([Step::default(); MAXC], [Step::default(); MAXC], 0)
        };
        let share = Share::choose(members, cols, mask, self.bsize);
        let mut h = Vec::new();
        for f in 0..cols {
            put_uv(&mut h, members[0][f] as u128);
        }
        for f in 0..cols {
            if mask >> f & 1 == 1 {
                put_uv(&mut h, zz(b1[f].num as i128));
                put_uv(&mut h, b1[f].den as u128);
                put_uv(&mut h, zz(b2[f].num as i128));
                put_uv(&mut h, b2[f].den as u128);
            }
        }
        let ref_off = self.append(&h);
        let g = self.groups.len();
        self.groups.push(GroupRef {
            first: self.blocks.len() as u32,
            nb: 0,
            n: n as u32,
            ref_off,
            kind,
            mask,
        });
        self.shares.push(share);
        self.scars.push(None);
        self.trial_k.push(0);
        let bs = self.bsize;
        for (j, chunk) in members.chunks(bs).enumerate() {
            self.buf.n = chunk.len();
            for (i, s) in chunk.iter().enumerate() {
                for f in 0..cols {
                    self.buf.col[f][i] = s[f];
                }
            }
            self.put(g, j * bs, None);
        }
        self.groups[g].nb = (self.blocks.len() - self.groups[g].first as usize) as u32;
        self.n += n as u64;
        g as u32
    }

    /// Block `bi` as its packed base (full values, before scars), into `buf`.
    fn decode_base(&self, bi: usize, buf: &mut Buf) {
        let br = self.blocks[bi];
        let g = br.group as usize;
        let h = self.hdr(g);
        let brefs = self.brefs(g, &h);
        decode_block(
            &self.arena[br.off as usize..],
            br.n as usize,
            self.cols,
            &brefs,
            buf,
        );
        let mask = self.groups[g].mask;
        if mask != 0 {
            let grid = self.grid(g);
            for f in 0..self.cols {
                if mask >> f & 1 == 1 {
                    let n = br.n as usize;
                    let mut pred = [0u64; MAXB];
                    lattice_run(
                        h.refs[f],
                        h.b1[f],
                        h.b2[f],
                        br.start as usize,
                        grid,
                        &mut pred[..n],
                    );
                    for i in 0..n {
                        buf.col[f][i] = pred[i].wrapping_add(unzz64(buf.col[f][i]) as u64);
                    }
                }
            }
        }
        if let Some(sh) = &self.shares[g] {
            sh.inverse(&mut buf.col, br.n as usize);
        }
    }

    /// Block `bi` (sealed state: base plus scars) into `buf`.
    pub fn decode_into(&self, bi: usize, buf: &mut Buf) {
        self.decode_base(bi, buf);
        let br = self.blocks[bi];
        if let Some(sc) = &self.scars[br.group as usize] {
            let (s0, s1) = (br.start as u64, br.start as u64 + br.n as u64);
            let mut d = [0u64; MAXC];
            for (j, r) in sc.ef.cursor(sc.ef.rank(s0)) {
                if r >= s1 {
                    break;
                }
                sc.row(j, &mut d, self.cols);
                let i = (r - s0) as usize;
                for f in 0..self.cols {
                    buf.col[f][i] = buf.col[f][i].wrapping_add(unzz64(d[f]) as u64);
                }
            }
        }
    }

    fn get_base(&self, bi: usize, slot: usize, out: &mut Ship) {
        let br = self.blocks[bi];
        let g = br.group as usize;
        let h = self.hdr(g);
        let brefs = self.brefs(g, &h);
        access(
            &self.arena[br.off as usize..],
            br.n as usize,
            self.cols,
            &brefs,
            slot,
            out,
        );
        let mask = self.groups[g].mask;
        if mask != 0 {
            let grid = self.grid(g);
            for f in 0..self.cols {
                if mask >> f & 1 == 1 {
                    let pred = lattice(h.refs[f], h.b1[f], h.b2[f], br.start as usize + slot, grid);
                    out[f] = pred.wrapping_add(unzz64(out[f]) as u64);
                }
            }
        }
        if let Some(sh) = &self.shares[g] {
            sh.inverse1(out);
        }
    }

    /// Random access by handle (block << 8 | slot).
    pub fn get(&self, handle: u32, out: &mut Ship) {
        let bi = (handle >> 8) as usize;
        let slot = (handle & 255) as usize;
        if self.dead[bi] > 0 {
            if let Some(&x) = self.forward.get(&handle) {
                *out = self.hot[x as usize].ship;
                return;
            }
        }
        self.get_base(bi, slot, out);
        let br = self.blocks[bi];
        if let Some(sc) = &self.scars[br.group as usize] {
            if let Some(j) = sc.ef.find(br.start as u64 + slot as u64) {
                let mut d = [0u64; MAXC];
                sc.row(j, &mut d, self.cols);
                Scars::apply(out, &d, self.cols);
            }
        }
    }

    /// An event changed one ship: the hot path (no re-encoding).
    pub fn update(&mut self, handle: u32, ship: Ship) {
        let bi = (handle >> 8) as usize;
        if self.dead[bi] > 0 {
            if let Some(&x) = self.forward.get(&handle) {
                self.hot[x as usize].ship = ship;
                return;
            }
        }
        self.dead[bi] += 1;
        self.forward.insert(handle, self.hot.len() as u32);
        self.hot.push(Hot {
            ship,
            handle,
            group: self.blocks[bi].group,
        });
    }

    /// Stream every live member, block by block (hot ships last, one per call).
    pub fn for_each(&self, buf: &mut Buf, mut f: impl FnMut(&Buf, Option<&[bool]>)) {
        let mut deadmask = [false; MAXB];
        for bi in 0..self.blocks.len() {
            if self.blocks[bi].n == 0 {
                continue;
            }
            self.decode_into(bi, buf);
            if self.dead[bi] > 0 {
                for (s, d) in deadmask.iter_mut().enumerate().take(buf.n) {
                    *d = self.forward.contains_key(&((bi as u32) << 8 | s as u32));
                }
                f(buf, Some(&deadmask[..buf.n]));
            } else {
                f(buf, None);
            }
        }
        for h in &self.hot {
            buf.n = 1;
            for c in 0..self.cols {
                buf.col[c][0] = h.ship[c];
            }
            f(buf, None);
        }
    }

    /// Bytes of group `g`'s blocks if its scars were folded in (nothing is committed).
    fn trial_bytes(&self, g: usize, enc: &mut Enc, buf: &mut Buf) -> usize {
        let gr = self.groups[g];
        let h = self.hdr(g);
        let brefs = self.brefs(g, &h);
        let mut share = self.shares[g].clone();
        let (mask, grid) = (gr.mask, self.grid(g));
        let mut out = Vec::new();
        let mut total = 0;
        for bi in gr.first as usize..(gr.first + gr.nb) as usize {
            self.decode_into(bi, buf);
            let (n, start) = (buf.n, self.blocks[bi].start as usize);
            for f in 0..self.cols {
                if mask >> f & 1 == 1 {
                    let mut pred = [0u64; MAXB];
                    lattice_run(h.refs[f], h.b1[f], h.b2[f], start, grid, &mut pred[..n]);
                    for i in 0..n {
                        buf.col[f][i] = zz64(buf.col[f][i].wrapping_sub(pred[i]) as i64);
                    }
                }
            }
            if let Some(sh) = share.as_mut() {
                sh.forward(buf);
            }
            out.clear();
            enc.block(self.cols, buf, &brefs, &mut out);
            total += out.len();
        }
        total
    }

    /// Fold the hot tier into each touched group's scar layer (idle time). Every ship keeps its
    /// slot (identity is provenance); a ship back at its base is reabsorbed. A group whose scars
    /// cost more than half its blocks is repacked: the scars are folded into fresh blocks.
    pub fn compact(&mut self) -> CompactStats {
        let mut st = CompactStats::default();
        let hot = std::mem::take(&mut self.hot);
        self.forward.clear();
        let cols = self.cols;
        // (group, rank, new state)
        let mut ev: Vec<(u32, u64, Ship, u32)> = hot
            .iter()
            .map(|h| {
                let bi = (h.handle >> 8) as usize;
                self.dead[bi] = 0;
                (
                    h.group,
                    self.blocks[bi].start as u64 + (h.handle & 255) as u64,
                    h.ship,
                    h.handle,
                )
            })
            .collect();
        ev.sort_unstable_by_key(|e| (e.0, e.1));
        let mut enc = std::mem::take(&mut self.enc);
        let mut buf = Buf::default();
        let mut i = 0;
        while i < ev.len() {
            let t0 = Instant::now();
            let g = ev[i].0 as usize;
            let mut j = i;
            while j < ev.len() && ev[j].0 as usize == g {
                j += 1;
            }
            // Merge the old scars (as deltas) with the new states (deltas from the base).
            let mut rows: Vec<(u64, Ship)> = Vec::new();
            let mut q = i;
            let push_new = |rows: &mut Vec<(u64, Ship)>, e: &(u32, u64, Ship, u32), me: &Self| {
                let mut base = [0u64; MAXC];
                me.get_base((e.3 >> 8) as usize, (e.3 & 255) as usize, &mut base);
                let mut d = [0u64; MAXC];
                for f in 0..cols {
                    d[f] = zz64(e.2[f].wrapping_sub(base[f]) as i64);
                }
                rows.push((e.1, d));
            };
            if let Some(sc) = self.scars[g].take() {
                let mut cur = usize::MAX;
                for (k, r) in sc.ef.cursor(0) {
                    while q < j && ev[q].1 < r {
                        push_new(&mut rows, &ev[q], self);
                        q += 1;
                    }
                    if q < j && ev[q].1 == r {
                        push_new(&mut rows, &ev[q], self);
                        q += 1;
                        continue;
                    }
                    if k / RB != cur {
                        cur = k / RB;
                        sc.row_block(cur, cols, &mut buf);
                    }
                    let mut d = [0u64; MAXC];
                    for f in 0..cols {
                        d[f] = buf.col[f][k % RB];
                    }
                    rows.push((r, d));
                }
            }
            while q < j {
                push_new(&mut rows, &ev[q], self);
                q += 1;
            }
            let sc = Scars::from_deltas(self.groups[g].n as u64, cols, &rows, &mut enc);
            let gr = self.groups[g];
            let block_bytes: usize = (gr.first..gr.first + gr.nb)
                .map(|b| self.blocks[b as usize].len as usize)
                .sum();
            let k = sc.k();
            // Switch forms by cost: when the scars have doubled since the last trial and weigh
            // at least a quarter of the blocks, encode the group repacked and keep the cheaper.
            let mut repack = false;
            if k > 0 && sc.bytes() * 4 > block_bytes && k >= 2 * self.trial_k[g] as usize {
                self.trial_k[g] = k as u32;
                self.scars[g] = Some(Box::new(sc));
                let trial = self.trial_bytes(g, &mut enc, &mut buf);
                let sc = self.scars[g].take().unwrap();
                repack = trial < block_bytes + sc.bytes();
                self.scars[g] = Some(sc);
            } else {
                self.scars[g] = (k > 0).then(|| Box::new(sc));
            }
            if repack {
                // Repack: fold the scars into fresh blocks.
                for bi in gr.first as usize..(gr.first + gr.nb) as usize {
                    self.decode_into(bi, &mut buf);
                    std::mem::swap(&mut self.buf, &mut buf);
                    std::mem::swap(&mut self.enc, &mut enc);
                    self.put(g, self.blocks[bi].start as usize, Some(bi));
                    std::mem::swap(&mut self.enc, &mut enc);
                    std::mem::swap(&mut self.buf, &mut buf);
                    st.blocks_rewritten += 1;
                }
                self.scars[g] = None;
                self.trial_k[g] = 0;
                st.repacks += 1;
            }
            st.max_step_ns = st.max_step_ns.max(t0.elapsed().as_nanos() as u64);
            i = j;
        }
        self.enc = enc;
        if self.garbage * 4 > self.arena.len() {
            let t0 = Instant::now();
            self.compact_arena();
            st.arena_compactions += 1;
            st.arena_ns = t0.elapsed().as_nanos() as u64;
        }
        st
    }

    /// Idle-time tidy: reclaim garbage and slack.
    pub fn tidy(&mut self) {
        self.compact_arena();
        self.shrink();
    }

    fn compact_arena(&mut self) {
        let mut a = Vec::with_capacity(self.arena.len() - self.garbage);
        for g in 0..self.groups.len() {
            let h = self.hdr(g);
            let off = a.len();
            a.extend_from_slice(&self.arena[self.groups[g].ref_off as usize..h.end]);
            self.groups[g].ref_off = off as u32;
        }
        for b in self.blocks.iter_mut() {
            let off = a.len();
            a.extend_from_slice(&self.arena[b.off as usize..b.off as usize + b.len as usize]);
            b.off = off as u32;
        }
        a.extend_from_slice(&[0; PAD]);
        self.arena = a;
        self.garbage = 0;
    }
}
