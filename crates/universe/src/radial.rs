//! Where each doll's bodies can be, by radius: the player's neighbourhood scan reads the bodies of its doll that can be near the player,
//! not every body of it.
//!
//! **The certificate.** A body's tube is a Kepler orbit between its events, so its distance from the doll's centre stays within
//! `[periapsis, apoapsis]` of the key (the *apsidal filter* of conjunction screening: two bodies in one plane can be close only if their
//! radial ranges overlap), widened by what the binding carries beyond the tube (the residual and the rounding of the readout, in quanta of
//! its word). The scan's predicate is the lattice law's `hit`: the linear relative motion over the interval comes within `reach`
//! (`reach = 2^ENCOUNTER_LOG2 (r_a + r_b)`), which implies `|d| ≤ reach + |w|`, `|w| ≤ (|v_a| + |v_b|)·h`, hence
//! `|r_b − r_a| ≤ reach + (|v_a| + |v_b|)·h`: a body whose radial range misses that window cannot be a hit, and is not read. Every term of
//! the window is rounded up (floats widened by a percent, far above their own rounding); the window only ever drops pairs that cannot meet,
//! so no outcome depends on a float: the candidates it keeps go through the exact predicate unchanged.
//!
//! **What is registered.** Every binding a body has had that a reader can still ask for (the current one and the retained history: the
//! registration is the hull of their radial ranges, only widened by an event and recomputed when the history is pruned), in the bins of
//! its radial range (sixteenth-octaves). A body whose tube has no bounded range (a passage, a plunge, a planet, a moon, the player) is
//! registered as *unbounded* in the doll: always a candidate. When the window covers most of what is registered (the player is inside
//! the belt), the caller reads every body as before: the filter costs nothing it does not save.
use crate::bind::Binding;
use crate::body::Kind;
use crate::num::to_f64;
use emergent_space::{binding::Trajectory, orbit::Scalar};
use std::collections::HashMap;

/// Bins per octave of radius.
const PER_OCTAVE: f64 = 16.0;

fn bin_of(r: f64) -> i32 {
    (r.max(1e-30).log2() * PER_OCTAVE).floor() as i32
}

/// Where one body is registered in one doll: the bins `lo..=hi`, or unbounded.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
struct Reg {
    doll: u16,
    lo: i32,
    hi: i32,
}
const NONE: Reg = Reg { doll: u16::MAX, lo: 0, hi: 0 };
const UNBOUNDED: i32 = i32::MAX;

#[derive(Default)]
struct DollIndex {
    /// Bin → the ids registered in it, ascending.
    bins: HashMap<i32, Vec<u32>>,
    /// Ids registered without a bound, ascending.
    unbounded: Vec<u32>,
    /// Entries in `bins` (a body counts once a bin it is in), for the caller's choice between the window and everything.
    entries: usize,
    /// The largest radius (as the scan reads it) and the speed bound of any body registered with a range.
    radius_cap: f64,
    speed_cap: f64,
}

#[derive(Default)]
pub struct Radial {
    dolls: Vec<DollIndex>,
    /// Per body: its registration in the first doll it was seen in; more dolls (a ship captured by a planet's doll, rare) in `extra`.
    first: Vec<Reg>,
    extra: HashMap<(u32, u16), Reg>,
    /// Bodies registered (with or without a range).
    pub bodies: usize,
}

/// The radial range `[lo, hi]` a binding's readout can have (doll units) and a bound on its speed (c = 1): None where the tube is no
/// bounded cycle (a passage, a plunge), so no range is known.
pub fn range_of(b: &Binding) -> Option<(f64, f64, f64)> {
    let Trajectory::Cycle(_) = &b.entry.trajectory else { return None };
    let key = b.entry.trajectory.key()?;
    let k = Scalar::raw(key.k as i128, -48).ok()?;
    let two_k_less_one = k.scale(1).ok()?.sub(Scalar::ONE).ok()?;
    if !two_k_less_one.is_positive() {
        return None;
    }
    let (peri, apo) = (b.to_doll(key.periapsis).ok()?, b.to_doll(key.periapsis.div(two_k_less_one).ok()?).ok()?);
    // What the binding carries beyond the tube: the residual (exact, in quanta of the word) and the readout's rounding and turn (a few quanta).
    let (q_len, q_vel) = (2f64.powi(b.units.0 as i32), 2f64.powi(b.units.1 as i32));
    let beyond_len = ((b.residual.position[0].unsigned_abs() + b.residual.position[1].unsigned_abs()) as f64 + 8.0) * q_len;
    let beyond_vel = ((b.residual.velocity[0].unsigned_abs() + b.residual.velocity[1].unsigned_abs()) as f64 + 8.0) * q_vel;
    // The speed at periapsis, `√((1 + e)/p)` in the tube's units (the integer word is sized by twice this), four times it here; never above c.
    let v_peri = (1.0 / (to_f64(key.periapsis) * (key.k as f64 * 2f64.powi(-48)))).sqrt();
    let widen = 1.0 / 1024.0;
    Some((to_f64(peri) * (1.0 - widen) - beyond_len, to_f64(apo) * (1.0 + widen) + beyond_len, (4.0 * v_peri + beyond_vel).min(1.0)))
}

/// What a scan asks: the player's radius `r` and speed `v` at the scan's tick, its radius as the finder reads it (`reach_p`, before the
/// `2^near_log2`), and the interval `h` in the doll's time.
pub struct Window {
    pub r: f64,
    pub v: f64,
    pub reach_p: f64,
    pub near_log2: i32,
    pub h: f64,
}

impl Radial {
    fn doll_mut(&mut self, d: u16) -> &mut DollIndex {
        if self.dolls.len() <= d as usize {
            self.dolls.resize_with(d as usize + 1, DollIndex::default);
        }
        &mut self.dolls[d as usize]
    }

    fn reg(&self, i: usize, d: u16) -> Reg {
        let f = self.first.get(i).copied().unwrap_or(NONE);
        if f.doll == d {
            f
        } else {
            self.extra.get(&(i as u32, d)).copied().unwrap_or(NONE)
        }
    }

    fn set_reg(&mut self, i: usize, r: Reg) {
        if self.first.len() <= i {
            self.first.resize(i + 1, NONE);
        }
        if self.first[i].doll == u16::MAX {
            self.first[i] = r;
            self.bodies += 1;
        } else if self.first[i].doll == r.doll {
            self.first[i] = r;
        } else {
            self.extra.insert((i as u32, r.doll), r);
        }
    }

    fn put_in(list: &mut Vec<u32>, i: u32) -> bool {
        match list.binary_search(&i) {
            Ok(_) => false,
            Err(at) => {
                list.insert(at, i);
                true
            }
        }
    }
    fn take_from(list: &mut Vec<u32>, i: u32) -> bool {
        match list.binary_search(&i) {
            Ok(at) => {
                list.remove(at);
                true
            }
            Err(_) => false,
        }
    }

    /// Move body `i`'s registration in doll `d` to `new`, bin by bin.
    fn move_reg(&mut self, i: usize, d: u16, new: Reg) {
        let old = self.reg(i, d);
        let idx = self.doll_mut(d);
        let id = i as u32;
        if old.doll == d {
            if old.lo == UNBOUNDED {
                if new.lo != UNBOUNDED {
                    Self::take_from(&mut idx.unbounded, id);
                }
            } else {
                for b in old.lo..=old.hi {
                    if new.lo != UNBOUNDED && (new.lo..=new.hi).contains(&b) {
                        continue;
                    }
                    if let Some(list) = idx.bins.get_mut(&b) {
                        if Self::take_from(list, id) {
                            idx.entries -= 1;
                        }
                        if list.is_empty() {
                            idx.bins.remove(&b);
                        }
                    }
                }
            }
        }
        if new.lo == UNBOUNDED {
            Self::put_in(&mut idx.unbounded, id);
        } else {
            for b in new.lo..=new.hi {
                if Self::put_in(idx.bins.entry(b).or_default(), id) {
                    idx.entries += 1;
                }
            }
        }
        self.set_reg(i, new);
    }

    /// Body `i` has the binding `b` now (a creation, an event): register it, widening what is registered of it in `b`'s doll to cover it.
    /// Only a ship is given a range (`radius` is its radius as the finder reads it); everything else is unbounded in its doll.
    pub fn note(&mut self, i: usize, kind: Kind, radius: f64, b: &Binding) {
        let d = b.doll;
        let range = if kind == Kind::Ship { range_of(b) } else { None };
        let old = self.reg(i, d);
        let want = match range {
            Some((lo, hi, v)) => {
                let idx = self.doll_mut(d);
                idx.radius_cap = idx.radius_cap.max(radius);
                idx.speed_cap = idx.speed_cap.max(v);
                let (blo, bhi) = (bin_of(lo.max(1e-30)), bin_of(hi));
                if old.doll == d && old.lo != UNBOUNDED {
                    Reg { doll: d, lo: old.lo.min(blo), hi: old.hi.max(bhi) }
                } else if old.doll == d {
                    old // unbounded stays unbounded
                } else {
                    Reg { doll: d, lo: blo, hi: bhi }
                }
            }
            None => Reg { doll: d, lo: UNBOUNDED, hi: 0 },
        };
        if want != old {
            self.move_reg(i, d, want);
        }
    }

    /// Body `i`'s retained bindings are `bindings` now (the history was pruned): register the hull of what remains, per doll.
    pub fn rebuild<'a>(&mut self, i: usize, kind: Kind, radius: f64, bindings: impl Iterator<Item = &'a Binding>) {
        let mut hulls: Vec<(u16, Option<(i32, i32)>)> = Vec::new();
        for b in bindings {
            let range = if kind == Kind::Ship { range_of(b) } else { None };
            let at = match hulls.iter().position(|h| h.0 == b.doll) {
                Some(at) => at,
                None => {
                    hulls.push((b.doll, Some((i32::MAX - 1, i32::MIN))));
                    hulls.len() - 1
                }
            };
            hulls[at].1 = match (hulls[at].1, range) {
                (Some((lo, hi)), Some((rl, rh, v))) => {
                    let idx = self.doll_mut(b.doll);
                    idx.radius_cap = idx.radius_cap.max(radius);
                    idx.speed_cap = idx.speed_cap.max(v);
                    Some((lo.min(bin_of(rl.max(1e-30))), hi.max(bin_of(rh))))
                }
                _ => None,
            };
        }
        for (d, hull) in hulls {
            let want = match hull {
                Some((lo, hi)) => Reg { doll: d, lo, hi },
                None => Reg { doll: d, lo: UNBOUNDED, hi: 0 },
            };
            if want != self.reg(i, d) {
                self.move_reg(i, d, want);
            }
        }
    }

    /// The bodies of doll `d` that can be within the window of the player (ascending), or None when that is most of what is registered
    /// in the doll (the caller then reads every body, as it did before there was an index).
    pub fn candidates(&self, d: u16, w: &Window) -> Option<Vec<usize>> {
        let idx = self.dolls.get(d as usize)?;
        let near = (w.reach_p + idx.radius_cap) * 2f64.powi(w.near_log2);
        let reach = (near + (w.v + idx.speed_cap) * w.h) * 1.01 + w.r * 1e-9;
        let (lo, hi) = (bin_of((w.r - reach).max(1e-30)), bin_of(w.r + reach));
        if hi - lo > 4096 {
            return None;
        }
        let hit: usize = (lo..=hi).filter_map(|b| idx.bins.get(&b)).map(|l| l.len()).sum();
        if hit + idx.unbounded.len() > self.bodies / 4 + 64 {
            return None;
        }
        let mut ids: Vec<u32> = idx.unbounded.clone();
        for b in lo..=hi {
            if let Some(l) = idx.bins.get(&b) {
                ids.extend_from_slice(l);
            }
        }
        ids.sort_unstable();
        ids.dedup();
        Some(ids.into_iter().map(|i| i as usize).collect())
    }
}
