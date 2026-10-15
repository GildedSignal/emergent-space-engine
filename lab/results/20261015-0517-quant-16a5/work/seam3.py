import pathlib, sys
def sub(path, old, new, count=1):
    p = pathlib.Path(path); t = p.read_text()
    if t.count(old) != count:
        print(f"FATAL {path}: count {t.count(old)} != {count}: {old[:70]!r}"); sys.exit(1)
    p.write_text(t.replace(old, new)); print(f"ok: {old[:44]!r}")
U = "crates/universe/src/universe.rs"
sub(U, ".b.entry.trajectory.key()", ".b.entry.key()", 2)
sub(U, "        let b = Binding { doll, tube, entry: bound.entry, residual: bound.residual, turn: bound.turn, units: bound.units, clock_exp: d.clock_exp(), event_time: 0, kick: crate::bind::Kick::NONE, impact: None };\n        let heading = prograde(&b)?;",
"""        let mut b = Binding { doll, tube, entry: crate::bind::EntrySlot::Live(bound.entry), residual: bound.residual, turn: bound.turn, units: bound.units, clock_exp: d.clock_exp(), event_time: 0, kick: crate::bind::Kick::NONE, impact: None };
        let heading = prograde(&b)?;
        if crate::bind::lazy() && b.entry.demote() {
            self.cat.release(b.tube.key);
        }""")
sub(U, "        self.cat.release(rec.b.tube.key);",
"""        if rec.b.entry.is_live() {
            self.cat.release(rec.b.tube.key);
        }""")
sub(U, """        for seg in upd.retired.drain(..) {
            self.cat.release(seg.b.tube.key);
            self.bodies.retire(i, Segment { b: seg.b, until: seg.until });
        }
        if let Some(entry) = upd.new_entry.take() {
            if let Ok(id) = self.cat.insert(entry) {
                upd.rec.b.tube.key = id;
            }
        }""",
"""        for mut seg in upd.retired.drain(..) {
            if seg.b.entry.is_live() {
                self.cat.release(seg.b.tube.key);
            }
            if crate::bind::lazy() {
                seg.b.entry.demote();
            }
            self.bodies.retire(i, Segment { b: seg.b, until: seg.until });
        }
        if let Some(entry) = upd.new_entry.take() {
            if let Ok(id) = self.cat.insert(entry) {
                upd.rec.b.tube.key = id;
                if crate::bind::lazy() && upd.rec.b.entry.demote() {
                    self.cat.release(id);
                }
            }
        }""")
sub(U, "            let b = Binding { doll, tube, entry: bound.entry, residual: bound.residual, turn: bound.turn, units: bound.units, clock_exp, event_time: l.tick, kick: crate::bind::Kick::NONE, impact: None };",
"            let b = Binding { doll, tube, entry: crate::bind::EntrySlot::Live(bound.entry), residual: bound.residual, turn: bound.turn, units: bound.units, clock_exp, event_time: l.tick, kick: crate::bind::Kick::NONE, impact: None };")
sub(U, "            } else if let Trajectory::Plunge(p) = &r.b.entry.trajectory {",
"            } else if let Some(p) = r.b.entry.plunge() {")
sub(U, "            put(&mut h, r.b.entry.clockwise as i128);", "            put(&mut h, r.b.entry.clockwise() as i128);")
print("ALL APPLIED")
