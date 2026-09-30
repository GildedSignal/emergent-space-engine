//! [`Kickable`] for [`MetalChronon`]: the free-fall frame's hooks (`crates/engine`) on the GPU
//! order. A kick or a rebase happens between chronons, with the GPU idle (every command buffer
//! is waited on before `advance` returns), so the hooks edit the shared buffers directly and
//! leave the next dense batch to read them. They have [`emergent_lattice::chronon::Chronon`]'s
//! semantics: the same legality checks ([`kicked`], [`rebased_ok`]), a refusal applies nothing,
//! a body whose velocity changes revises (`rev + 1`), carries and residuals are untouched.
//!
//! What the GPU derives from a body's velocity or position, and how each stays coherent:
//! - `dy[i].k`, `dy[i].rev` (canonical) and `kq[i]` (the i16 copy the kernels read): written
//!   together, as the response does.
//! - `mask[i]`, the row's bloom filter of consumed contacts: zero after a revision, as the
//!   response does (a revised body's row is all dead; stale bits in other rows only cost a table
//!   read, never a wrong answer).
//! - `ctl.bincell`, the cell side the bins were built with: a kick moves no position, so the bins
//!   stay valid (the next `plan` re-bins when the new velocities change the cell side); a rebase
//!   moves positions, so it marks the bins stale (0), as the CPU chronon does.
//! - `xmax` (the cell-coordinate bound) and `p1` (the C·(K + 1) ≤ 2^28 precondition): refreshed
//!   from the new state.
//! - The reference's pruning of consumed contacts (every 64th tick) runs lazily here (`prune_due`):
//!   it is settled first, since the reference had already pruned before the kick, and a per-body
//!   rebase can change which entries survive it.
use super::*;
use emergent_lattice::{kicked, rebased_ok, Kickable, Motion};

impl MetalChronon {
    /// Do the pruning the reference did at the end of its last chronon, if still owed.
    fn settle_prune(&mut self) {
        if std::mem::take(&mut self.prune_due) {
            self.prune();
        }
    }

    /// The GPU precondition for the velocities now held (the rule `cpu_step` ends with).
    fn refresh_p1(&mut self) {
        let k = self.gpu.dy.get().iter().map(|d| kval(d.k)).max().unwrap_or(0);
        let cell = (self.reach_max + 2 * k).max(1);
        self.p1 = cell as i128 * (k as i128 + 1) > LIMIT;
    }
}

impl Kickable for MetalChronon {
    fn motions(&self, out: &mut Vec<Motion>) {
        out.clear();
        out.extend(self.gpu.pos.get().iter().zip(self.gpu.dy.get()).map(|(x, d)| Motion { x: *x, k: d.k }));
    }

    fn kick(&mut self, dk: &[[i64; 2]]) -> Result<(), law::LawError> {
        let n = self.bodies.len();
        if dk.len() != n {
            return Err(law::LawError(format!("{} kicks for {} bodies", dk.len(), n)));
        }
        for (d, k) in self.gpu.dy.get().iter().zip(dk) {
            kicked(self.law, self.q, d.k, *k)?;
        }
        self.settle_prune();
        let (dy, kq, mask) = (self.gpu.dy.get_mut(), self.gpu.kq.get_mut(), self.gpu.mask.get_mut());
        for (i, d) in dk.iter().enumerate() {
            if *d != [0, 0] {
                let k = [dy[i].k[0] + d[0], dy[i].k[1] + d[1]];
                dy[i].k = k;
                dy[i].rev += 1;
                kq[i] = narrow(k);
                mask[i] = 0;
            }
        }
        self.refresh_p1();
        Ok(())
    }

    fn masses(&self, out: &mut Vec<i64>) {
        out.clear();
        out.extend(self.bodies.iter().map(|b| b.mass));
    }

    fn rebase(&mut self, dx: &[[i64; 2]], dk: &[[i64; 2]]) -> Result<(), law::LawError> {
        let n = self.bodies.len();
        if dk.len() != n || dx.len() != n {
            return Err(law::LawError(format!("{} shifts and {} kicks for {} bodies", dx.len(), dk.len(), n)));
        }
        let bodies = self.gpu.pos.get().iter().zip(self.gpu.dy.get()).map(|(x, d)| Motion { x: *x, k: d.k });
        rebased_ok(self.law, self.q, self.container.is_some(), bodies, dx, dk)?;
        self.settle_prune();
        let (pos, dy, kq, mask) = (self.gpu.pos.get_mut(), self.gpu.dy.get_mut(), self.gpu.kq.get_mut(), self.gpu.mask.get_mut());
        let mut moved = false;
        for (i, (s, d)) in dx.iter().zip(dk).enumerate() {
            if *s != [0, 0] {
                pos[i] = [pos[i][0] + s[0], pos[i][1] + s[1]];
                moved = true;
            }
            if *d != [0, 0] {
                let k = [dy[i].k[0] + d[0], dy[i].k[1] + d[1]];
                dy[i].k = k;
                dy[i].rev += 1;
                kq[i] = narrow(k);
                mask[i] = 0;
            }
        }
        if moved {
            self.xmax = self.gpu.pos.get().iter().map(|x| x[0].abs().max(x[1].abs())).max().unwrap_or(0);
            self.gpu.ctl.get_mut()[0].bincell = 0; // the bins were built from the old positions
        }
        self.refresh_p1();
        Ok(())
    }
}
