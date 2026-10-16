"""Tests for lab/verdict.py. Run from the repo root: python3 -m unittest lab/test_verdict.py"""
import json, os, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import verdict

FENCE = "`" * 3
RUNG = f"""# toy rung
Prose: the question, the cases.
{FENCE}configs
good candidate
weak candidate
ctrl negative
{FENCE}
{FENCE}criteria
# id kind metric op threshold
A behaviour x >= 1.0
B cost y <= 10
{FENCE}
"""
OK = {"x": 2.0, "y": 5.0}
BAD = {"x": 0.0, "y": 50.0}
CHK = {"good": OK, "weak": BAD, "ctrl": BAD}

def first(lines):
    return lines[0]

class Verdicts(unittest.TestCase):
    def test_pass(self):
        out = verdict.judge(RUNG, CHK)
        self.assertTrue(first(out).startswith("Verdict: PASS; "))
        self.assertIn("killed: weak", first(out))
        self.assertIn("good candidate pass", out)
        self.assertIn("weak candidate fail A,B", out)
        self.assertIn("ctrl negative fail A,B", out)

    def test_positive_control_that_passes_is_neutral(self):
        rung = RUNG.replace("ctrl negative", "ctrl negative\nideal positive")
        out = verdict.judge(rung, dict(CHK, ideal=OK))
        self.assertTrue(first(out).startswith("Verdict: PASS; "))
        self.assertIn("ideal positive pass", out)

    def test_positive_control_that_fails_voids_the_rung(self):
        rung = RUNG.replace("ctrl negative", "ctrl negative\nideal positive")
        out = verdict.judge(rung, dict(CHK, ideal=BAD))
        self.assertTrue(first(out).startswith("Verdict: VOID; a positive control fails"))

    def test_kill_names_the_killed_configurations(self):
        out = verdict.judge(RUNG, {"good": {"x": 2.0, "y": 50.0}, "weak": BAD, "ctrl": BAD})
        self.assertTrue(first(out).startswith("Verdict: KILL; "))
        self.assertIn("killed: good, weak", first(out))
        self.assertIn("good candidate fail B", out)

    def test_void_missing_metric(self):
        chk = {"good": {"x": 2.0}, "weak": BAD, "ctrl": BAD}
        out = verdict.judge(RUNG, chk)
        self.assertTrue(first(out).startswith("Verdict: VOID; "))
        self.assertIn("good: y is missing or not a number", out)

    def test_void_non_numeric_and_missing_config(self):
        for bad in ("2.0", None, True, float("nan")):
            out = verdict.judge(RUNG, {"good": {"x": bad, "y": 5.0}, "weak": BAD, "ctrl": BAD})
            self.assertTrue(first(out).startswith("Verdict: VOID; "), bad)
        out = verdict.judge(RUNG, {"good": OK, "weak": BAD})
        self.assertTrue(first(out).startswith("Verdict: VOID; "))
        self.assertIn("ctrl: no such configuration", out)

    def test_void_negative_passes(self):
        out = verdict.judge(RUNG, {"good": OK, "weak": BAD, "ctrl": OK})
        self.assertTrue(first(out).startswith("Verdict: VOID; negative passes every criterion"))
        self.assertIn("ctrl", first(out))

    def test_void_checker_missing_or_rung_malformed(self):
        self.assertTrue(first(verdict.judge(RUNG, None)).startswith("Verdict: VOID; "))
        bad_rung = RUNG.replace("A behaviour x >= 1.0", "A behaviour x ~= 1.0")
        self.assertTrue(first(verdict.judge(bad_rung, CHK)).startswith("Verdict: VOID; "))

    def test_disputed_on_different_outcome(self):
        auth = {"good": {"x": 2.0, "y": 50.0}, "weak": BAD, "ctrl": BAD}  # author says good fails B
        out = verdict.judge(RUNG, CHK, auth)
        self.assertTrue(first(out).startswith("Verdict: DISPUTED; "))
        self.assertIn("good B: checker pass, author fail", out)

    def test_numeric_difference_alone_is_not_a_dispute(self):
        auth = {"good": {"x": 1.5, "y": 9.9}, "weak": {"x": 0.9, "y": 11.0}, "ctrl": BAD}
        self.assertTrue(first(verdict.judge(RUNG, CHK, auth)).startswith("Verdict: PASS; "))

    def test_disputed_when_the_author_has_no_number(self):
        out = verdict.judge(RUNG, CHK, {})
        self.assertTrue(first(out).startswith("Verdict: DISPUTED; "))

    def test_threshold_edges(self):
        edge = {"good": {"x": 1.0, "y": 10.0}, "weak": BAD, "ctrl": BAD}
        self.assertTrue(first(verdict.judge(RUNG, edge)).startswith("Verdict: PASS; "))
        strict = RUNG.replace("x >= 1.0", "x > 1.0").replace("y <= 10", "y < 10")
        self.assertTrue(first(verdict.judge(strict, edge)).startswith("Verdict: KILL; "))

class Cli(unittest.TestCase):
    def run_cli(self, rung, chk, auth=None):
        with tempfile.TemporaryDirectory() as d:
            paths = []
            for name, body in (("rung.md", rung), ("chk.json", chk), ("auth.json", auth)):
                if body is not None:
                    p = os.path.join(d, name)
                    with open(p, "w") as f:
                        f.write(body if isinstance(body, str) else json.dumps(body))
                    paths.append(p)
            r = subprocess.run([sys.executable, os.path.join(HERE, "verdict.py")] + paths,
                               capture_output=True, text=True)
            return r.returncode, r.stdout.splitlines()

    def test_exit_codes_and_first_line(self):
        code, out = self.run_cli(RUNG, CHK, CHK)
        self.assertEqual(code, 0)
        self.assertTrue(out[0].startswith("Verdict: PASS; "))
        code, out = self.run_cli(RUNG, "{not json")
        self.assertEqual((code, out[0][:13]), (0, "Verdict: VOID"))
        r = subprocess.run([sys.executable, os.path.join(HERE, "verdict.py")], capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        r = subprocess.run([sys.executable, os.path.join(HERE, "verdict.py"), "/nonexistent.md", "/nonexistent.json"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)

class Canaries(unittest.TestCase):
    def read(self, name):
        with open(os.path.join(HERE, "canaries", name)) as f:
            return f.read()

    def test_kepler_pass(self):
        good = {"energy_growth_exponent": 0.0, "bound_fraction": 1.0, "steps_per_orbit": 200}
        euler = {"energy_growth_exponent": 0.0, "bound_fraction": 0.0078, "steps_per_orbit": 200}
        out = verdict.judge(self.read("kepler-pass.md"), {"leapfrog": good, "euler": euler})
        self.assertTrue(first(out).startswith("Verdict: PASS; "))

    def test_kepler_kill(self):
        euler = {"energy_growth_exponent": 0.0, "bound_fraction": 0.0078, "steps_per_orbit": 200, "orbit_closure_count": 3}
        frozen = {"energy_growth_exponent": 0.0, "bound_fraction": 1.0, "steps_per_orbit": 200, "orbit_closure_count": 0}
        out = verdict.judge(self.read("kepler-kill.md"), {"euler": euler, "frozen": frozen})
        self.assertTrue(first(out).startswith("Verdict: KILL; "))
        self.assertIn("killed: euler", first(out))
        self.assertIn("frozen negative fail R1", out)

if __name__ == "__main__":
    unittest.main()
