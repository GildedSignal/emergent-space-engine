#!/usr/bin/env python3
"""Independent marker/content instrument: pure line regex, shares no code with
wiki.py's defuse (the v1 run's heal check shared the parser and was blind).

  inst.py count <file>          -> starts= mids= ends= runlines=
  inst.py subseq <orig> <new>   -> every non-marker line of <orig> appears in
                                   <new>, in order (content preservation)
  inst.py maxdepth <file>       -> max stack depth of marker lines
"""
import re, sys

START = re.compile(r"^<{7}( |$)")
MID = re.compile(r"^={7}$")
END = re.compile(r"^>{7}( |$)")
RUN = re.compile(r"^- \d{8}-\d{4}-")


def counts(text):
    ls = text.splitlines()
    return {"starts": sum(1 for l in ls if START.match(l)),
            "mids": sum(1 for l in ls if MID.match(l)),
            "ends": sum(1 for l in ls if END.match(l)),
            "runlines": sum(1 for l in ls if RUN.match(l))}


def nonmarker(lines):
    return [l for l in lines if not (START.match(l) or MID.match(l) or END.match(l))]
def subseq_text(orig, new):
    """subseq() on strings: every non-marker line of orig appears in new, in order."""
    it = iter(new.splitlines())
    for l in nonmarker(orig.splitlines()):
        if not l.strip():
            continue
        for h in it:
            if h == l:
                break
        else:
            return False, l
    return True, None


def subseq(orig, new):
    return subseq_text(open(orig, encoding="utf-8").read(), open(new, encoding="utf-8").read())


def maxdepth(text):
    d = m = 0
    for l in text.splitlines():
        if START.match(l):
            d += 1
            m = max(m, d)
        elif END.match(l):
            d = max(0, d - 1)
    return m


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "count":
        c = counts(open(sys.argv[2], encoding="utf-8").read())
        print(f"starts={c['starts']} mids={c['mids']} ends={c['ends']} runlines={c['runlines']}")
    elif cmd == "subseq":
        ok, miss = subseq(open(sys.argv[2], encoding="utf-8").read(),
                          open(sys.argv[3], encoding="utf-8").read())
        print("SUBSEQ_OK" if ok else f"SUBSEQ_FAIL first-missing={miss!r}")
    elif cmd == "maxdepth":
        print(maxdepth(open(sys.argv[2], encoding="utf-8").read()))
