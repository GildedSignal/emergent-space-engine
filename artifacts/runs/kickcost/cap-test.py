#!/usr/bin/env python3
"""Cargo test runner: preserve Cargo's package cwd and cap each binary at 59 s."""
import os, signal, subprocess, sys
print('cargo-cap:', sys.argv[1], 'cwd='+os.getcwd(), flush=True)
child=subprocess.Popen(sys.argv[1:],start_new_session=True)
try:
    status=child.wait(timeout=59)
except subprocess.TimeoutExpired:
    os.killpg(child.pid,signal.SIGKILL)
    child.wait()
    status=124
raise SystemExit(status)
