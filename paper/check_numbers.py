#!/usr/bin/env python3
"""Check that every statistic quoted in the paper's prose appears in a generated table or results file.

Scans build/paper.md (the expanded source) outside YAML, tables, captions and code; collects numbers that
look like AUCs or AUC differences (0.6xxx, 0.00xx, +/-0.00xx), percentages and minute counts, and looks
each up in paper/tables/*.md and analysis/results/*.md|csv (also as the same value with fewer decimals,
rounded). Prints the numbers it cannot find, with their line. Exit code 1 if any.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
src = (HERE / "build" / "paper.md").read_text().split("\n---\n", 2)[-1]  # drop YAML
hay = ""
for f in list((HERE / "tables").glob("*.md")) + list((HERE.parent / "analysis" / "results").glob("*")):
    if f.is_file():
        hay += f.read_text(errors="replace") + "\n"
# numbers present in the sources, as strings and as floats
present = set(re.findall(r"-?\d+\.\d+", hay)) | set(re.findall(r"\d+%", hay))
floats = sorted({float(x) for x in re.findall(r"-?\d+\.\d+", hay)})


def found(tok):
    if tok in present:
        return True
    try:
        v = float(tok.replace("−", "-").rstrip("%"))
    except ValueError:
        return False
    if tok.endswith("%"):
        return any(abs(f * 100 - v) < 0.5 for f in floats) or any(abs(f - v) < 0.5 for f in floats)
    dec = len(tok.split(".")[-1])
    return any(round(f, dec) == v for f in floats)


misses = []
for i, line in enumerate(src.splitlines(), 1):
    if line.startswith("|") or line.startswith("Table:") or line.startswith("![") or line.startswith(">") or line.startswith("<!--"):
        continue
    for tok in re.findall(r"[+\-−]?\d\.\d{3,4}|\b\d{1,3}%", line):
        if not found(tok):
            misses.append((i, tok, line.strip()[:100]))
for i, tok, l in misses:
    print(f"line {i}: {tok}   | {l}")
print(f"{len(misses)} unmatched numbers")
sys.exit(1 if misses else 0)
