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
for name in ('crates','xtask','.cargo'):
    shutil.copytree(root/name, scratch/name, dirs_exist_ok=True, ignore=shutil.ignore_patterns('target','__pycache__'))

def change(path, old, new):
    p = scratch/path
    text = p.read_text()
    assert text.count(old) == 1, (path, old, text.count(old))
    p.write_text(text.replace(old, new))

change('crates/engine/src/frame.rs','            shift: 0,', '''            shift: if std::env::var("ENGINE_JUDGE_MUTANT").as_deref() == Ok("late") && std::any::type_name::<S>().contains("EventCore") { 1 } else { 0 },''')
# Drop the velocity rotation, retaining the tide forcing coefficients; this is a
# missing Coriolis kick, not a reversed gravity sign or a changed scene.
change('crates/engine/src/frame.rs','        let rx = cc * kx + ss * ky', '''        let (cc, ss) = if std::env::var("ENGINE_JUDGE_MUTANT").as_deref() == Ok("coriolis") { (1i128 << CARRY_BITS, 0) } else { (cc, ss) };
        let rx = cc * kx + ss * ky''')
change('crates/engine/src/anchor.rs','                    flush[i][c] = round_shift(self.pcarry[i][c], CARRY_BITS) as i64;', '''                    flush[i][c] = if std::env::var("ENGINE_JUDGE_MUTANT").as_deref() == Ok("drift") { 0 } else { round_shift(self.pcarry[i][c], CARRY_BITS) as i64 };''')
# Target only the sparse kick hook, not contact/rebase revisions.
change('crates/lattice-event/src/lib.rs','''            h.rev += 1;
            // The prediction that follows''','''            if std::env::var("ENGINE_JUDGE_MUTANT").as_deref() != Ok("rev") { h.rev += 1; }
            // The prediction that follows''')
# A shared target reuses dependencies. Preserve the running baseline binary first:
# building scratch replaces target/release/xtask but never the baseline source.
target = root/'target'
outdir = root/'artifacts/runs/engine-judge'
baseline = target/'release/xtask'
if baseline.exists(): shutil.copy2(baseline, outdir/'baseline-xtask')
subprocess.run(['cargo','build','--offline','--release','-p','xtask','--target-dir',str(target)],cwd=scratch,check=True)
shutil.copy2(target/'release/xtask',outdir/'mutant-xtask')
if (outdir/'baseline-xtask').exists(): shutil.copy2(outdir/'baseline-xtask',target/'release/xtask')
print(outdir/'mutant-xtask')
