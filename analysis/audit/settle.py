#!/usr/bin/env python3
"""Settle the manual audit: merge the three per-LLM verdict files into verified.csv.

The yes/no verdicts are taken as read (after the checks recorded in SETTLED.md); the disagreements with
the script are recomputed here from the script's own values rather than taken from the readers' lists.
Model settings are written once per distinct value, in the order of the file.
"""
import csv
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE.parent / "results"
GROUPS = ("astra6_n20", "sol6_n20", "luna6_n20")
YESNO = ("dom_cat", "month_cat", "doy", "holiday", "ensemble")
SETTINGS = ("depth", "trees", "learning_rate")


def script_values():
    rows = {r["run"]: r for r in csv.DictReader(open(RESULTS / "feature_audit_per_run.csv"))}
    return {run: {k: int(r.get("script_" + k, r[k])) for k in YESNO} for run, r in rows.items()}


def tidy(value):
    """'3, 4, 3 (dart)' -> '3, 4'; '10 (lossguide, 31 leaves)' -> '31 leaves (depth 10)'; repeated values once."""
    m = re.fullmatch(r"(\d+) \(lossguide, (\d+) leaves\)", value.strip())
    if m:
        return f"{m.group(2)} leaves (depth {m.group(1)})"
    value = re.sub(r"\s*\((?!default)[^)]*\)", "", value)
    parts = [p.strip() for p in value.split(",") if p.strip()]
    return ", ".join(dict.fromkeys(parts))


def main():
    script = script_values()
    out = []
    for g in GROUPS:
        for r in csv.DictReader(open(HERE / f"{g}.csv")):
            run = r["run"]
            differs = [k for k in YESNO if int(r[k] == "yes") != script[run][k]]
            differs += [k for k in SETTINGS if k in r["disagrees_with_script"].split()]
            row = {k: r[k] for k in ("run",) + YESNO[:4]}
            row.update({k: tidy(r[k]) for k in SETTINGS})
            row.update(ensemble=r["ensemble"], disagrees_with_script=" ".join(differs) or "none", evidence=r["evidence"], note=r["note"])
            out.append(row)
    cols = ["run", *YESNO[:4], *SETTINGS, "ensemble", "disagrees_with_script", "evidence", "note"]
    with open(HERE / "verified.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(out)
    print(f"wrote verified.csv: {len(out)} runs, {sum(r['disagrees_with_script'] != 'none' for r in out)} with a correction")
    for k in YESNO:
        print(f"  {k}: {sum(k in r['disagrees_with_script'].split() for r in out)} corrected")


if __name__ == "__main__":
    main()
