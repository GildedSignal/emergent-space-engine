//! The read-only context an event is resolved in: the dolls, the static facts of each body, and
//! the bodies' histories. An event reads other bodies' tubes at its own tick and writes only its
//! own body, so events of independent bodies can be resolved in any order and on any number of
//! threads, and give the same bits.
use crate::body::{BodyStore, Kind};
use crate::force::Secondary;
use crate::num::{scale2, Res, Tick, V2};
use crate::world::{pow2, DollRec, Unit};
use emergent_space::orbit::Scalar;

/// What never changes about a body.
#[derive(Clone, Copy, Debug)]
pub struct BodyInfo {
    pub kind: Kind,
    /// `G·m` in units of the doll the body sits in: its pull as a secondary (zero for a test particle).
    pub gm: Scalar,
    /// Its sphere of influence in the units of the doll it sits in (zero for a test particle).
    pub soi: Scalar,
    /// The child doll it is the centre of, if any.
    pub doll: Option<u16>,
    /// Surface radius in the units of the doll it sits in.
    pub radius: Scalar,
    /// A member of a fleet's frame that left it: (fleet, member), so the view keeps its identity.
    pub from: Option<(u16, u16)>,
    /// The tick it was handed out at (0 for a body made with the universe): it is there for readers after it.
    pub born: Tick,
}

#[derive(Clone, Copy, Debug)]
pub struct Config {
    /// Thrust: rapidity per root time unit, as a power of two (the ship's proper acceleration).
    pub thrust_log2: i32,
    /// Turning while a turn key is held: turns per root time unit, as a power of two.
    pub turn_log2: i32,
    /// A body farther than this from the star (root units) has left the system.
    pub leave_log2: i32,
    /// Kicks per radial period, as a power of two: of a tube of a planet's doll; for a ship of the root doll, of the period of
    /// every secondary its orbit can meet (the passage regime, [`crate::ext::constants`]); for the player, of the doll's
    /// shortest secondary.
    pub step_log2: i32,
    /// Kicks per the ship's own radial period, as a power of two, for a ship of the root doll (the smooth regime and the floor of
    /// the passage regime, [`crate::ext::constants`]).
    pub smooth_log2: i32,
    /// Steps per period of the doll's shortest secondary, as a power of two, for a ship of the root doll on its own clock: the
    /// frame's fall toward every secondary (the indirect term) forces every body of the doll at that period ([`crate::ext::constants`]).
    pub forcing_log2: i32,
    /// Each ship of the root doll on its own clock (its own period, the secondaries it can meet, a phase from its id); false is
    /// the clock of 7 October (every ship of the doll on the doll's shortest secondary, phase zero), kept as the reference.
    pub own_clock: bool,
    /// A burn's kick moves the velocity by at most `2^-thrust_quantum_log2` of the local speed.
    pub thrust_quantum_log2: i32,
}
impl Default for Config {
    fn default() -> Self {
        Self { thrust_log2: -44, turn_log2: -30, leave_log2: 40, step_log2: 7, smooth_log2: 4, forcing_log2: 2, own_clock: true, thrust_quantum_log2: 6 }
    }
}

pub struct Ctx<'a> {
    pub dolls: &'a [DollRec],
    pub bodies: &'a dyn BodyStore,
    pub info: &'a [BodyInfo],
    /// Per doll: the bodies that pull others in it (secondaries), in id order.
    pub sources: &'a [Vec<usize>],
    pub cfg: &'a Config,
    /// Where each doll's bodies can be, by radius: who a scan must read.
    pub radial: &'a crate::radial::Radial,
}

impl Ctx<'_> {
    /// Body `j`'s position and velocity at `t` in the units of the doll it sits in.
    pub fn state_of(&self, j: usize, t: Tick) -> Res<(V2, V2)> {
        let b = self.bodies.binding_at(j, t).ok_or(crate::num::Error::Refused("history pruned"))?;
        b.cartesian(t)
    }

    /// The units body `i`'s tube is compiled in, in doll `d`: about the doll's centre alone for a test particle,
    /// and about the centre plus its own mass for a secondary (two bodies fall toward each other: their relative
    /// orbit is the Kepler problem of the total mass, which is what makes the doll's origin falling toward the
    /// secondary, and the secondary's own orbit, one motion).
    pub fn tube_unit(&self, i: usize, d: u16) -> Res<Unit> {
        let host = self.dolls[d as usize].unit;
        if self.info[i].gm.is_zero() {
            return Ok(host);
        }
        Unit::of(host.mu.add(self.info[i].gm)?)
    }

    /// The secondaries of doll `d` at `t` (excluding `except`), in `d`'s units.
    pub fn secondaries(&self, d: u16, t: Tick, except: usize) -> Res<Vec<Secondary>> {
        let mut out = Vec::new();
        for &j in &self.sources[d as usize] {
            if j == except {
                continue;
            }
            let (pos, vel) = self.state_of(j, t)?;
            out.push(Secondary { gm: self.info[j].gm, pos, vel, edge: self.info[j].soi });
        }
        Ok(out)
    }

    /// The radius of body `j`'s own surface, in the units of the doll `host` it sits in: the surface of the doll it is the
    /// centre of (in that doll's units), converted. None for a body that is not the centre of a doll.
    pub fn surface_in(&self, j: usize, host: u16) -> Res<Option<Scalar>> {
        let Some(c) = self.info[j].doll else { return Ok(None) };
        let (child, host) = (&self.dolls[c as usize], &self.dolls[host as usize]);
        Ok(Some(child.surface.scale(host.shift as i32 - child.shift as i32)?))
    }

    /// The parent's tide on doll `d`: the parent's mass (its mantissa included) and the doll centre's
    /// position in the parent's frame, both in `d`'s units.
    pub fn tide(&self, d: u16, t: Tick) -> Res<Option<(Scalar, V2)>> {
        let doll = &self.dolls[d as usize];
        let (Some(p), Some(c)) = (doll.parent, doll.centre) else { return Ok(None) };
        let k = pow2(doll.shift as i32 - self.dolls[p as usize].shift as i32);
        let (pos, _) = self.state_of(c, t)?;
        Ok(Some((self.dolls[p as usize].unit.to_doll(k)?, scale2(pos, k)?)))
    }

    /// The centre of doll `d` at `t`, in its parent's units (position, velocity).
    pub fn centre(&self, d: u16, t: Tick) -> Res<(V2, V2)> {
        let c = self.dolls[d as usize].centre.ok_or(crate::num::Error::Refused("the root has no centre"))?;
        self.state_of(c, t)
    }
}
