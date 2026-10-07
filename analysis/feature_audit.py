#!/usr/bin/env python3
"""Heuristic audit of each run's final train.py, with ambiguity flags for the manual check.

Columns per run: whether DayofMonth and Month are still categories (in the last `cat_cols = [...]`
assignment), numeric conversions of them, holiday features, day-of-year-like features, tree depth or
leaves, number of trees, learning rate, ensembles, DART, interaction constraints, target or rate
encodings. `verified` is left empty for the manual pass (plan 03, decision 8).
"""
import csv
import re
import statistics as st
from common import MODELS, RESULTS, SHORT, load_runs, md_table, runs_repo, write

repo = runs_repo()
runs = load_runs(repo, with_session=False)


def audit(src):
    code = "\n".join(l for l in src.splitlines() if not l.strip().startswith("#"))
    lists = re.findall(r"^cat_cols\s*=\s*\[([^\]]*)\]", code, re.M)
    cat = lists[-1] if lists else ""
    incat = lambda c: f'"{c}"' in cat or f"'{c}'" in cat
    def inprepare():
        m = re.search(r"def prepare\(.*?(?=^\S)", code, re.S | re.M)
        return m.group(0) if m else ""
    prep = inprepare()
    num_dom = bool(re.search(r"DayofMonth[\"'\]]*\)?\s*\.(str|astype|map|apply)|int\(\w+\[2:\]\)\s*for\s+\w+\s+in\s+df\[.DayofMonth|DayofMonth.{0,40}(astype\(int|\[2:\]|float\()", code))
    num_month = bool(re.search(r"[\"']Month[\"'\]]*\)?\s*\.(str|astype|map|apply)|int\(\w+\[2:\]\)\s*for\s+\w+\s+in\s+df\[.Month|[\"']Month[\"'].{0,40}(astype\(int|\[2:\]|float\()", code))
    holiday = bool(re.search(r"holiday|thanksgiving|christmas|memorial|labor.?day|july.?4|independence|new.?year", code, re.I))
    holiday_comment_only = (not holiday) and bool(re.search(r"holiday|thanksgiving|christmas", src, re.I))
    doy = bool(re.search(r"day_?of_?year|\bdoy\b|dayofyear|fortnight|week_?of_?year|woy", code, re.I))
    depth = re.findall(r"max_depth\s*=\s*(\d+)(?=\s*(?:[,)#]|$))", code, re.M); leaves = re.findall(r"max_leaves\s*=\s*(\d+)(?=\s*(?:[,)#]|$))", code, re.M)
    trees = re.findall(r"n_estimators\s*=\s*(\d+)(?=\s*(?:[,)#]|$))", code, re.M); lr = re.findall(r"learning_rate\s*=\s*([\d.]+)(?=\s*(?:[,)#]|$))", code, re.M)
    n_models = len(re.findall(r"XGB(?:Classifier|RF\w*)\(|xgb\.train\(", code))
    ensemble = n_models > 1 or bool(re.search(r"num_parallel_tree|seeds?\s*=\s*\[|for seed in|VotingClassifier|blend|average of|members", code, re.I))
    dart = bool(re.search(r"booster\s*=\s*[\"']dart", code))
    inter = bool(re.search(r"interaction_constraints|monotone_constraints", code))
    enc = bool(re.search(r"target_?enc|TargetEncoder|delay_rate|target_rate|(?<!learning)_rate\b|leave.one.out|cross.?fit|\bwoe\b|mean_target", code, re.I))
    flags = []
    if incat("DayofMonth") and num_dom: flags.append("dom_both")
    if len(lists) != 1: flags.append("cat_cols_" + ("missing" if not lists else "multi"))
    if holiday_comment_only: flags.append("holiday_comment_only")
    if not prep: flags.append("no_prepare")
    if not incat("DayofMonth") and "DayofMonth" in prep and not num_dom: flags.append("dom_in_prepare_unclear")
    if src.count("DayofMonth") > 4: flags.append("dom_many_refs")
    return dict(dom_cat=int(incat("DayofMonth")), month_cat=int(incat("Month")), dom_numeric=int(num_dom), month_numeric=int(num_month),
                holiday=int(holiday), doy=int(doy), max_depth=depth[-1] if depth else "", max_leaves=leaves[-1] if leaves else "",
                n_estimators=trees[-1] if trees else "", learning_rate=lr[-1] if lr else "", n_models=n_models, ensemble=int(ensemble),
                dart=int(dart), constraints=int(inter), encodings=int(enc), flags=" ".join(flags), verified="")


A = {}
for r in runs:
    A[r["run"]] = audit((r["dir"] / "train.py").read_text())
rows = []
for m in MODELS:
    rr = [r for r in runs if r["model"] == m]; a = [A[r["run"]] for r in rr]
    kept = [r["holdout_auc"] for r, x in zip(rr, a) if x["dom_cat"]]; dropped = [r["holdout_auc"] for r, x in zip(rr, a) if not x["dom_cat"]]
    depths = [int(x["max_depth"]) for x in a if x["max_depth"]]
    rows.append([SHORT[m], len(rr), len(dropped), len(kept), sum(x["month_cat"] for x in a), sum(x["doy"] for x in a), sum(x["holiday"] for x in a),
                 f"{st.mean(dropped):.4f}" if dropped else "-", f"{st.mean(kept):.4f}" if kept else "-",
                 f"{st.mean(dropped)-st.mean(kept):+.4f}" if kept and dropped else "-",
                 sum(1 for d in depths if d <= 4), len(depths), sum(x["ensemble"] for x in a), sum(x["dart"] for x in a), sum(x["constraints"] for x in a),
                 sum(x["encodings"] for x in a), sum(bool(x["flags"]) for x in a)])
out = "## Final models by LLM (heuristic audit; provisional until the manual check)\n\n" + md_table(
    ["LLM", "runs", "dropped DayofMonth as a category", "kept it", "Month still a category", "day-of-year-like feature", "holiday features",
     "mean holdout, dropped", "mean holdout, kept", "difference", "max_depth ≤ 4 (of runs with max_depth set)", "runs with max_depth set",
     "ensembles", "DART", "interaction or monotone constraints", "target or rate encodings", "runs with ambiguity flags"], rows)
amb = [(r["run"], A[r["run"]]["flags"]) for r in runs if A[r["run"]]["flags"]]
out += f"\nRuns with ambiguity flags, to read by hand first: {len(amb)} (see feature_audit_ambiguous.md). The manual check of all 60 files fills the `verified` column of feature_audit_per_run.csv.\n"
write("table_feature_audit.md", out, repo)
write("feature_audit_ambiguous.md", "## Files to read by hand first\n\n" + md_table(["run", "flags"], amb) +
      "\nFlags: dom_both = DayofMonth both in the category list and converted to a number; cat_cols_multi/missing = the category list is "
      "not a single plain assignment; holiday_comment_only = holiday words only in comments; no_prepare = no prepare() found; "
      "dom_in_prepare_unclear = DayofMonth used in prepare() without a recognised conversion; dom_many_refs = more than four references.\n", repo)
with open(RESULTS / "feature_audit_per_run.csv", "w", newline="") as f:
    cols = ["run", "model", "holdout_auc"] + list(next(iter(A.values())).keys())
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
    for r in runs:
        w.writerow(dict(run=r["run"], model=r["model"], holdout_auc=f"{r['holdout_auc']:.4f}", **A[r["run"]]))
print("wrote results/feature_audit_per_run.csv")
