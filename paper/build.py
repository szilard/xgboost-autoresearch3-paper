#!/usr/bin/env python3
"""Expand {{table:NAME}} markers in paper.md with paper/tables/NAME.md, then run pandoc and LaTeX.

Usage: python3 build.py [--tex-only]
Outputs build/paper.md (expanded), build/main.tex, build/main.pdf.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE / "build"
BUILD.mkdir(exist_ok=True)
src = (HERE / "paper.md").read_text()


def expand(m):
    name = m.group(1)
    p = HERE / "tables" / f"{name}.md"
    if not p.exists():
        sys.exit(f"missing table {p}; run analysis/paper_tables.py")
    return p.read_text().strip() + "\n"


expanded = re.sub(r"\{\{table:([\w-]+)\}\}", expand, src)
# figures live in ../figures relative to paper/; the build runs in build/, so point one level further up
expanded = expanded.replace("](../figures/", "](../../figures/")
(BUILD / "paper.md").write_text(expanded)
bib = (HERE / "refs.bib").read_text()
# the note fields carry verification provenance for the authors, not for the reader
bib = re.sub(r"^\s*note\s*=\s*\{(?:[^{}]|\{[^{}]*\})*\},?\n", "", bib, flags=re.M)
(BUILD / "refs.bib").write_text(bib)
shutil.copy(HERE / "header.tex", BUILD / "header.tex")
cmd = ["pandoc", "paper.md", "--from", "markdown+smart", "--to", "latex", "--standalone", "--natbib",
       "--include-in-header", "header.tex", "--number-sections", "--output", "main.tex"]
subprocess.run(cmd, cwd=BUILD, check=True)
# arXiv wants \pdfoutput=1 within the first lines
tex = (BUILD / "main.tex").read_text()
if not tex.startswith("\\pdfoutput=1"):
    (BUILD / "main.tex").write_text("\\pdfoutput=1\n" + tex)
if "--tex-only" in sys.argv:
    print("wrote build/main.tex"); sys.exit(0)
for step in (["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main"], ["bibtex", "main"],
             ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main"], ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main"]):
    r = subprocess.run(step, cwd=BUILD, capture_output=True, text=True)
    if r.returncode != 0 and step[0] == "pdflatex":
        print(r.stdout[-3000:]); sys.exit(f"{step[0]} failed")
print("wrote build/main.pdf")
