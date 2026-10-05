#!/usr/bin/env python3
"""Only edits a disposable source copy; one runtime-selectable mutation per process.
Compilation is preparation, outside the per-test 55 s watchdog. No baseline crate edits.
"""
import hashlib, json, pathlib, shutil, subprocess, sys
root = pathlib.Path(__file__).resolve().parents[3]
scratch = root / 'artifacts/runs/engine-judge/scratch'
outdir = root / 'artifacts/runs/engine-judge'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inputs():
    files = [root/'Cargo.toml', root/'Cargo.lock', pathlib.Path(__file__).resolve()]
    files += [p for folder in ('crates', 'xtask/src') for p in (root/folder).rglob('*')
              if p.is_file() and p.suffix in ('.rs', '.metal', '.toml')
              and 'target' not in p.relative_to(root).parts]
    return {str(p.relative_to(root)): sha(p) for p in sorted(set(files))}

if len(sys.argv) == 3 and sys.argv[1] == '--verify':
    binary = pathlib.Path(sys.argv[2]).resolve()
    try:
        record = json.loads((binary.parent/'prepared-mutants.json').read_text())
        assert record['inputs'] == inputs(), 'baseline or preparation recipe changed'
        assert record['binary_sha256'] == sha(binary), 'binary differs from prepared artifact'
        assert all(sha(scratch/p) == digest for p, digest in record['patched_sources'].items()), 'patched source changed'
    except (OSError, ValueError, KeyError, AssertionError) as error:
        print(f'stale_or_unverified_mutants: {error}; run engine-judge --prepare-mutants')
        sys.exit(1)
    print('prepared_mutants_verified')
    sys.exit(0)

if len(sys.argv) != 1:
    sys.exit('usage: prepare_mutants.py [--verify BINARY]')

scratch.mkdir(parents=True, exist_ok=True)
for name in ('Cargo.toml','Cargo.lock'):
    shutil.copy2(root/name, scratch/name)
for name in ('crates','xtask','.cargo','scenarios'):
    shutil.copytree(root/name, scratch/name, dirs_exist_ok=True, ignore=shutil.ignore_patterns('target','__pycache__'))

patched = set()
def change(path, old, new):
    p = scratch/path
    text = p.read_text()
    assert text.count(old) == 1, (path, old, text.count(old))
    p.write_text(text.replace(old, new))
    patched.add(path)

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
subprocess.run(['cargo','build','--offline','--release','-p','xtask','--target-dir',str(target)],cwd=scratch,check=True)
shutil.copy2(target/'release/xtask',outdir/'mutant-xtask')
(outdir/'prepared-mutants.json').write_text(json.dumps({
    'inputs': inputs(), 'binary_sha256': sha(outdir/'mutant-xtask'),
    'patched_sources': {p: sha(scratch/p) for p in sorted(patched)},
}, indent=2) + '\n')
print(outdir/'mutant-xtask')
