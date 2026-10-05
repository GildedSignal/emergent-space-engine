#!/usr/bin/env python3
"""Only edits a disposable source copy; one runtime-selectable mutation per process.
Compilation is preparation, outside the per-test 55 s watchdog. No baseline crate edits.
"""
import pathlib, shutil, subprocess, sys
root = pathlib.Path(__file__).resolve().parents[3]
scratch = root / 'artifacts/runs/engine-judge/scratch'
scratch.mkdir(parents=True, exist_ok=True)
for name in ('Cargo.toml','Cargo.lock'):
    shutil.copy2(root/name, scratch/name)
for name in ('crates','xtask','.cargo','scenarios'):
    shutil.copytree(root/name, scratch/name, dirs_exist_ok=True, ignore=shutil.ignore_patterns('target','__pycache__'))

def change(path, old, new):
    p = scratch/path
    text = p.read_text()
    assert text.count(old) == 1, (path, old, text.count(old))
    p.write_text(text.replace(old, new))

change('crates/engine/src/frame.rs','        self.shift = shift;', '''        self.shift = shift + if std::env::var("ENGINE_JUDGE_MUTANT").as_deref() == Ok("late") && std::any::type_name::<S>().contains("EventCore") { 1 } else { 0 };''')
# Corrupt the first tidal row with a spurious radial coefficient.
change('crates/engine/src/frame.rs','        let rx = cc * kx + ss * ky', '''        let (cc, ss) = if std::env::var("ENGINE_JUDGE_MUTANT").as_deref() == Ok("tide-row") { (1i128 << CARRY_BITS, 0) } else { (cc, ss) };
        let rx = cc * kx + ss * ky''')
change('crates/engine/src/anchor.rs','                    flush[i][c] = round_shift(self.pcarry[i][c], CARRY_BITS) as i64;', '''                    flush[i][c] = if std::env::var("ENGINE_JUDGE_MUTANT").as_deref() == Ok("drift") { 0 } else { round_shift(self.pcarry[i][c], CARRY_BITS) as i64 };''')
# Target only the sparse kick hook, not contact/rebase revisions.
change('crates/lattice-event/src/lib.rs','''            h.rev += 1;
            // The prediction that follows''','''            if std::env::var("ENGINE_JUDGE_MUTANT").as_deref() != Ok("rev") { h.rev += 1; }
            // The prediction that follows''')
# E9 defects act on the copied tube's tensor, independently of the row defect.
change('crates/engine/src/tube.rs', '        let (x, _) = self.readout(units, tick)?;', '''        let tick = if std::env::var("ENGINE_JUDGE_MUTANT").as_deref() == Ok("static-tide") { 0 } else { tick };
        let (x, _) = self.readout(units, tick)?;''')
change('crates/engine/src/tube.rs', '        Ok([[diag(c)?, off], [off, diag(s)?]])', '''        let sign = if std::env::var("ENGINE_JUDGE_MUTANT").as_deref() == Ok("sign-tide") { -1 } else { 1 };
        Ok([[sign * diag(c)?, sign * off], [sign * off, sign * diag(s)?]])''')
# Cargo can reuse the scratch executable's embedded manifest path when both
# workspaces share a target, even after restoring target/release/xtask. Isolate
# scratch artifacts so the next ordinary cargo run really runs the baseline.
target = scratch/'target'
outdir = root/'artifacts/runs/engine-judge'
subprocess.run(['cargo','build','--offline','--release','-p','xtask','--target-dir',str(target)],cwd=scratch,check=True)
shutil.copy2(target/'release/xtask',outdir/'mutant-xtask')
print(outdir/'mutant-xtask')
