import pathlib, sys
def sub(path, old, new, count=1):
    p = pathlib.Path(path); t = p.read_text()
    if t.count(old) != count:
        print(f"FATAL {path}: count {t.count(old)} != {count}: {old[:70]!r}"); sys.exit(1)
    p.write_text(t.replace(old, new)); print(f"ok {path}: {old[:44]!r}")
B = "crates/universe/src/bind.rs"
sub(B, "        entry,\n        residual: Residual { position: [0; 2], velocity: [0; 2] },",
"""        entry: EntrySlot::Live(entry),
        residual: Residual { position: [0; 2], velocity: [0; 2] },""")
sub("crates/universe/src/body.rs", "        let shape = match &r.b.entry.trajectory {",
"""        let shape = match &r.b.entry {
            crate::bind::EntrySlot::Demoted { .. } => 0,
            crate::bind::EntrySlot::Live(a) => match &a.trajectory {""")
sub("crates/universe/src/body.rs", "            emergent_space::binding::Trajectory::Plunge(p) => p.retained_bytes(),\n        }",
"""                emergent_space::binding::Trajectory::Plunge(p) => p.retained_bytes(),
            },
        }""")
sub("crates/universe/src/encounter.rs", "    Arc::ptr_eq(&a.entry, &b.entry)",
"""    matches!(
        (&a.entry, &b.entry),
        (crate::bind::EntrySlot::Live(x), crate::bind::EntrySlot::Live(y)) if Arc::ptr_eq(x, y)
    )""")
sub("crates/universe/src/ext.rs", '    let Trajectory::Cycle(c) = &b.entry.trajectory else { return Err(Error::Refused("a source without a period")) };',
"""    let e = b.entry.get()?;
    let Trajectory::Cycle(c) = &e.trajectory else { return Err(Error::Refused("a source without a period")) };""")
sub("crates/universe/src/radial.rs", "    let Trajectory::Cycle(_) = &b.entry.trajectory else { return None };\n    let key = b.entry.trajectory.key()?;",
"""    if !b.entry.is_cycle() {
        return None;
    }
    let key = b.entry.key()?;""")
sub("crates/universe/src/scenario.rs", ".b.entry.trajectory.key()", ".b.entry.key()")
S = "crates/universe/src/step.rs"
sub(S, "    let mut period = b.to_doll(match &b.entry.trajectory {",
"""    let e = b.entry.get()?;
    let mut period = b.to_doll(match &e.trajectory {""")
sub(S, "        if b.entry.trajectory.key().is_some_and(|k| b.to_doll(k.periapsis).is_ok_and(|r| r < edge)) {",
"        if b.entry.key().is_some_and(|k| b.to_doll(k.periapsis).is_ok_and(|r| r < edge)) {")
sub(S, "    let apex = match &b.entry.trajectory {",
"""    let e = b.entry.get()?;
    let apex = match &e.trajectory {""")
sub(S, "    let end = if matches!(b.entry.trajectory, Trajectory::Passage(_)) {",
"    let end = if matches!(e.trajectory, Trajectory::Passage(_)) {")
sub(S, "    if let (true, Trajectory::Passage(p)) = (guess, &b.entry.trajectory) {",
"    if let (true, Trajectory::Passage(p)) = (guess, &e.trajectory) {")
sub(S, "        let guess = b.entry.unit.to_tube(edge)", "        let guess = b.entry.unit().to_tube(edge)")
sub(S, "    let at = match &b.entry.trajectory {",
"""    let e = b.entry.get()?;
    let at = match &e.trajectory {""")
sub(S, "    if matches!(b.entry.trajectory, Trajectory::Plunge(_)) {",
"    if matches!(e.trajectory, Trajectory::Plunge(_)) {")
sub(S, "    if b.entry.trajectory.key().is_some_and(|k| b.to_doll(k.periapsis).is_ok_and(|r| r >= surface)) {",
"    if b.entry.key().is_some_and(|k| b.to_doll(k.periapsis).is_ok_and(|r| r >= surface)) {")
sub(S, "    let whole = match &b.entry.trajectory {", "    let whole = match &e.trajectory {")
sub(S, "            entry: bound.entry.clone(),", "            entry: crate::bind::EntrySlot::Live(bound.entry.clone()),")
sub(S, "&& self.rec.b.entry.trajectory.key().is_some_and(|key|", "&& self.rec.b.entry.key().is_some_and(|key|")
sub(S, "        let is_passage = matches!(b.entry.trajectory, Trajectory::Passage(_));",
"        let is_passage = matches!(b.entry.get()?.trajectory, Trajectory::Passage(_));")
U = "crates/universe/src/universe.rs"
sub(U, ".b.entry.trajectory.key()", ".b.entry.key()", 1)
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
